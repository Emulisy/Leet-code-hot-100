"""Offline local tests for Go, Python, Java and JavaScript solutions."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {"go": "go", "py": "python", "python": "python", "python3": "python",
             "js": "javascript", "javascript": "javascript", "java": "java", "all": "all"}


def environment() -> dict:
    env = os.environ.copy()
    env["GOMODCACHE"] = str(ROOT / ".cache/go-mod")
    env["GOCACHE"] = str(ROOT / ".cache/go-build")
    env["LEETGO_HOME"] = str(ROOT / ".cache/leetgo")
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def problems(language: str, qid: str = "all") -> list[tuple[Path, dict]]:
    language = LANGUAGES[language]
    folders = ("go", "python", "java", "javascript") if language == "all" else (language,)
    found = []
    for folder in folders:
        for config_path in (ROOT / folder).glob("*/problem.json"):
            config = json.loads(config_path.read_text(encoding="utf-8"))
            if qid == "all" or str(config["id"]) == str(int(qid)):
                found.append((config_path, config))
    if not found:
        raise ValueError(f"No solution found for {language} {qid}")
    return sorted(found, key=lambda item: (item[1]["language"], item[1]["id"]))


def read_cases(path: Path, nargs: int) -> list[dict]:
    """One JSON value per argument, with leetgo input:/output: delimiters."""
    lines = [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    cases, index = [], 0
    while index < len(lines):
        if lines[index] != "input:":
            raise ValueError(f"{path}: expected input: at nonblank line {index + 1}")
        start = index + 1
        output_index = start + nargs
        if output_index + 1 >= len(lines) or lines[output_index] != "output:":
            raise ValueError(f"{path}: each case needs {nargs} input lines and one expected output")
        args = [json.loads(line) for line in lines[start:output_index]]
        expected = json.loads(lines[output_index + 1])
        cases.append({"args": args, "expected": expected,
                      "stdin": "\n".join(lines[start:output_index]) + "\n"})
        index = output_index + 2
    if not cases:
        raise ValueError(f"{path}: no test cases")
    return cases


def normalize(value, unordered: list[int], depth: int = 0):
    if isinstance(value, list):
        value = [normalize(item, unordered, depth + 1) for item in value]
        if depth in unordered:
            value.sort(key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    return value


def same(actual, expected) -> bool:
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is type(expected) and actual == expected
    if type(actual) is int and type(expected) is int:
        return actual == expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, list):
        return len(actual) == len(expected) and all(same(a, e) for a, e in zip(actual, expected))
    return actual == expected


def matches(config: dict, case: dict, actual) -> bool:
    if config["id"] == 5:
        return (isinstance(actual, str) and len(actual) == len(case["expected"])
                and actual == actual[::-1] and actual in case["args"][0])
    if config["id"] == 2900:
        if not isinstance(actual, list) or len(actual) != len(case["expected"]):
            return False
        words, groups = case["args"]
        positions = {(-1, None)}
        for word in actual:
            positions = {(i, groups[i]) for last, group in positions
                         for i in range(last + 1, len(words))
                         if words[i] == word and groups[i] != group}
        return bool(positions)
    levels = config.get("unordered", [])
    return same(normalize(actual, levels), normalize(case["expected"], levels))


def check_prefix(config: dict, case: dict, result, mutated) -> bool:
    values = case["args"][config["check_prefix"]]
    if config["id"] == 27:
        expected = [x for x in values if x != case["args"][1]]
        expected.sort()
    else:
        limit = 2 if config["id"] == 80 else 1
        expected, count, previous = [], 0, object()
        for value in values:
            count = count + 1 if value == previous else 1
            previous = value
            if count <= limit:
                expected.append(value)
    if type(result) is not int or result != len(expected) or not isinstance(mutated, list):
        return False
    prefix = mutated[:result]
    if config["id"] == 27:
        prefix.sort()
    return prefix == expected


def tool(name: str) -> str:
    executable = shutil.which(name)
    if not executable:
        raise ValueError(f"{name} is not on PATH; see README.md for prerequisites")
    return executable


def compile_command(command: list[str], cwd: Path) -> None:
    result = subprocess.run(command, cwd=cwd, env=environment(), capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=120)
    if result.returncode:
        raise ValueError((result.stderr + result.stdout).strip())


def command_for(config_path: Path, config: dict, debug: bool = False,
                debug_input: Path | None = None) -> tuple[list[str], Path]:
    source = config_path.parent / config["file"]
    language = config["language"]
    if language == "javascript":
        command = [tool("node")]
        if debug:
            command += ["--inspect-brk=127.0.0.1:9229"]
        return command + [str(ROOT / "tools/run-js.cjs"), str(config_path)], ROOT
    if language == "python":
        python = ROOT / ("python/.venv/Scripts/python.exe" if os.name == "nt" else "python/.venv/bin/python")
        if not python.exists():
            raise ValueError("Missing Python environment; run tools/setup.ps1 or follow README.md")
        if debug:
            # debugpy reads the selected test through stdin after the debugger attaches.
            return [str(python), "-m", "debugpy", "--listen", "127.0.0.1:5678", "--wait-for-client", str(source)], ROOT
        return [str(python), str(source)], ROOT
    runner = ROOT / "tools/LocalRunner.java"
    dependencies = [source, runner] if language == "java" else [source, ROOT / "go/go.mod", ROOT / "go/go.sum"]
    digest = hashlib.sha256()
    for dependency in dependencies:
        digest.update(dependency.read_bytes())
    digest.update(str(debug).encode())
    build = ROOT / ".cache/build" / language / f'{config["id"]}-{digest.hexdigest()[:16]}'
    build.mkdir(parents=True, exist_ok=True)
    if language == "java":
        if not (build / "LocalRunner.class").exists():
            compile_command([tool("javac"), "-g", "-encoding", "UTF-8", "-d", str(build), str(runner), str(source)], ROOT)
        command = [tool("java")]
        if debug:
            command += ["-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=127.0.0.1:5005"]
        return command + ["-cp", str(build), "LocalRunner", config.get("class", "Solution"),
                          config["method"], str(config.get("output_arg", -1))], ROOT
    binary = build / ("solution.exe" if os.name == "nt" else "solution")
    if not binary.exists():
        command = [tool("go"), "build"]
        if debug:
            command += ["-gcflags=all=-N -l"]
        compile_command(command + ["-o", str(binary), str(source)], ROOT / "go")
    if debug:
        if debug_input is None:
            raise ValueError("Missing debugger input file")
        return [tool("dlv"), "exec", str(binary), "--headless", "--listen=127.0.0.1:2345",
                "--api-version=2", "--accept-multiclient", "--redirect=stdin:" + str(debug_input)], ROOT / "go"
    return [str(binary)], ROOT / "go"


def extract_output(stdout: str, marker: str = "output:"):
    outputs = re.findall(r"^" + re.escape(marker) + r"\s*(.*)$", stdout, flags=re.M)
    if not outputs:
        raise ValueError(f"Runner did not emit {marker}; output was {stdout.strip()!r}")
    return json.loads(outputs[-1])


def add_problem(language: str, qid: str) -> int:
    """Generate a new problem through leetgo, then register the local adapter."""
    from problem_data import UNORDERED, examples, metadata

    language = LANGUAGES[language]
    binary = ROOT / (".tools/leetgo.exe" if os.name == "nt" else ".tools/leetgo")
    if not binary.exists():
        raise ValueError("Run tools/setup.ps1 first to install leetgo")
    qid_number = int(qid)
    cache = ROOT / ".cache/leetgo/cache/leetcode-questions.json"
    if not cache.exists():
        subprocess.run([str(binary), "cache", "update"], cwd=ROOT, env=environment(), check=True)
    question_list = json.loads(cache.read_text(encoding="utf-8"))
    brief = next((q for q in question_list if q["questionFrontendId"] == str(qid_number)), None)
    if brief is None:
        raise ValueError(f"Unknown problem {qid}; try tools/leetgo.ps1 cache update")
    basename = f'{qid_number:04d}.{brief["titleSlug"]}'
    folder = ROOT / language / basename
    if folder.exists():
        raise ValueError(f"Already exists: {folder.relative_to(ROOT)}; no files were overwritten")
    question = metadata(qid_number, brief["titleSlug"])
    meta = question["metaData"]
    if meta.get("systemdesign"):
        raise ValueError("This adapter supports function-style problems; use a dedicated driver for design problems")
    case_text = examples(question)
    extension = {"java": ".java", "javascript": ".js"}.get(language)
    if extension:
        flat_source = ROOT / language / (basename + extension)
        flat_statement = ROOT / language / (basename + ".md")
        if flat_source.exists() or flat_statement.exists():
            raise ValueError("A flat leetgo file already exists for this problem; move it before adding")
    leetgo_lang = {"python": "python3", "javascript": "js"}.get(language, language)
    subprocess.run([str(binary), "pick", str(qid_number), "-l", leetgo_lang, "--skip-editor"],
                   cwd=ROOT, env=environment(), stdin=subprocess.DEVNULL, check=True)
    config = {"id": qid_number, "title": question["title"], "language": language,
              "method": meta["name"], "params": meta["params"],
              "return_type": meta["return"]["type"], "unordered": UNORDERED.get(qid_number, [])}
    if meta["return"]["type"] == "void":
        config["output_arg"] = (meta.get("output") or {}).get("paramindex", 0)
    if qid_number in (26, 27, 80):
        config["check_prefix"] = 0
    if extension:
        folder.mkdir(parents=True)
        if language == "java":
            source = flat_source.read_text(encoding="utf-8")
            class_match = re.search(r"(?m)^\s*(?:public\s+)?class\s+(\w+)", source)
            if not class_match:
                raise ValueError("Could not identify the generated Java class")
            class_name = f"Solution{qid_number}" if class_match[1] == "Solution" else class_match[1]
            source = re.sub(r"\b" + re.escape(class_match[1]) + r"\b", class_name, source)
            flat_source.write_text(source, encoding="utf-8")
            config["class"] = class_name
            config["file"] = class_name + ".java"
        else:
            config["file"] = "solution.js"
        shutil.move(str(flat_source), str(folder / config["file"]))
        if flat_statement.exists():
            shutil.move(str(flat_statement), str(folder / "question.md"))
    else:
        config["file"] = "solution.go" if language == "go" else "solution.py"
        if "check_prefix" in config:
            # These local mains must expose the actual mutated buffer as well as k.
            source = folder / config["file"]
            text = source.read_text(encoding="utf-8")
            if language == "go":
                index = text.rfind("}")
                text = text[:index] + '\tfmt.Println("mutated:", Serialize(nums))\n' + text[index:]
            else:
                text += '\n    print("mutated:", serialize(nums, "List[int]"))\n'
            source.write_text(text, encoding="utf-8")
    (folder / "testcases.txt").write_text(case_text, encoding="utf-8")
    (folder / "problem.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f'Added {folder.relative_to(ROOT)}. Edit {config["file"]}, then run:')
    print(f"python tools/leet.py test {language} {qid_number}")
    return 0


def run_tests(options) -> int:
    selected = problems(options.language, options.id)
    if options.debug and (len(selected) != 1 or options.cases):
        raise ValueError("Debug one problem at a time, using its own testcases.txt")
    if options.cases and len(selected) != 1:
        raise ValueError("--cases requires exactly one problem")
    passed = failed = 0
    reports = []
    for config_path, config in selected:
        label = f'{config["language"]} {config["id"]}'
        try:
            cases = read_cases(Path(options.cases) if options.cases else config_path.parent / "testcases.txt",
                               len(config["params"]))
            numbers = [options.case] if options.case is not None else list(range(1, len(cases) + 1))
            if options.debug:
                numbers = [options.case if options.case is not None else 1]
            if any(number < 1 or number > len(cases) for number in numbers):
                raise ValueError(f"--case must be between 1 and {len(cases)}")
            debug_input = None
            if options.debug:
                debug_input = ROOT / ".cache/debug" / f'{config["language"]}-{config["id"]}.txt'
                debug_input.parent.mkdir(parents=True, exist_ok=True)
                debug_input.write_text(cases[numbers[0] - 1]["stdin"], encoding="utf-8")
            command, cwd = command_for(config_path, config, options.debug, debug_input)
            if options.debug:
                print(f"Debugging {label}, case {numbers[0]}. Attach using the matching VS Code configuration.", flush=True)
                return subprocess.run(command, input=cases[numbers[0] - 1]["stdin"], text=True,
                                      encoding="utf-8", cwd=cwd, env=environment()).returncode
        except (ValueError, OSError, subprocess.TimeoutExpired) as error:
            failed += 1
            print(f"ERROR {label}: {error}", flush=True)
            reports.append({"problem": label, "status": "error", "detail": str(error)})
            continue
        for number in numbers:
            case = cases[number - 1]
            try:
                result = subprocess.run(command, input=case["stdin"], text=True, encoding="utf-8",
                                        errors="replace", capture_output=True, cwd=cwd,
                                        env=environment(), timeout=options.timeout)
                if result.returncode:
                    raise ValueError((result.stderr + result.stdout).strip())
                actual = extract_output(result.stdout)
                valid = matches(config, case, actual)
                if "check_prefix" in config:
                    valid = valid and check_prefix(config, case, actual, extract_output(result.stdout, "mutated:"))
                if not valid:
                    raise ValueError(f'expected {json.dumps(case["expected"])}; got {json.dumps(actual)}'
                                     + (" (also checking the mutated prefix)" if "check_prefix" in config else ""))
                passed += 1
                print(f"PASS {label} case {number}", flush=True)
                reports.append({"problem": label, "case": number, "status": "pass"})
            except (ValueError, OSError, subprocess.TimeoutExpired) as error:
                failed += 1
                detail = f"timed out after {options.timeout:g}s" if isinstance(error, subprocess.TimeoutExpired) else str(error)
                print(f"FAIL {label} case {number}: {detail}", flush=True)
                reports.append({"problem": label, "case": number, "status": "fail", "detail": detail})
    report = ROOT / ".cache/latest-test-results.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({"passed": passed, "failed": failed, "results": reports}, indent=2) + "\n", encoding="utf-8")
    print(f"\n{passed} passed; {failed} failed/errors across {len(selected)} solution(s).")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="action", required=True)
    test = subcommands.add_parser("test", help="run offline test cases")
    test.add_argument("language", choices=LANGUAGES)
    test.add_argument("id", nargs="?", default="all", help="problem ID or all")
    test.add_argument("--case", type=int, help="one case number (1-based)")
    test.add_argument("--cases", help="use a different testcase file")
    test.add_argument("--timeout", type=float, default=5, help="seconds per test case (default: 5)")
    test.add_argument("--debug", action="store_true", help="wait for a debugger; defaults to case 1")
    listing = subcommands.add_parser("list", help="list local solutions")
    listing.add_argument("language", nargs="?", default="all", choices=LANGUAGES)
    export = subcommands.add_parser("export", help="print submission code without the local I/O wrapper")
    export.add_argument("language", choices=[lang for lang in LANGUAGES if lang != "all"])
    export.add_argument("id")
    add = subcommands.add_parser("add", help="generate and register a new problem through leetgo (requires internet)")
    add.add_argument("language", choices=[lang for lang in LANGUAGES if lang != "all"])
    add.add_argument("id")
    options = parser.parse_args()
    try:
        if options.action == "add":
            return add_problem(options.language, options.id)
        if options.action == "test":
            if not math.isfinite(options.timeout) or options.timeout <= 0:
                raise ValueError("--timeout must be a positive finite number")
            return run_tests(options)
        if options.action == "list":
            for path, config in problems(options.language):
                print(f'{config["language"]:10} {config["id"]:4}  {path.parent.relative_to(ROOT)}')
            return 0
        path, config = problems(options.language, options.id)[0]
        text = (path.parent / config["file"]).read_text(encoding="utf-8")
        if config["language"] in ("go", "python"):
            text = text.split("@lc code=begin", 1)[1]
            text = re.split(r"(?m)^(?://|#) @lc code=end", text, maxsplit=1)[0].strip()
        elif config["language"] == "java":
            text = re.sub(r'\b' + re.escape(config["class"]) + r'\b', "Solution", text)
        print(text)
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
