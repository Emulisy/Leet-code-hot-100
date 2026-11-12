"""Copy legacy solutions into isolated, leetgo-compatible problem directories.

Original files are never changed. Existing migrated directories are never overwritten.
Public problem metadata is cached in .cache/problems; fetching it needs internet access.
"""
from __future__ import annotations

import ast
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERY = """query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId title titleSlug content metaData exampleTestcases
  }
}"""

# These are ordering rules, not alternative expected answers. Duplicates still count.
UNORDERED = {15: [0], 17: [0], 18: [0], 22: [0], 30: [0], 39: [0],
             40: [0], 46: [0], 47: [0], 49: [0, 1], 51: [0],
             77: [0], 78: [0], 90: [0]}
EXCLUDED = {
    "1.py": "Contains find_remaining, not LeetCode 1 (Two Sum); kept in the legacy root.",
    "59.js": "Empty getPermutation draft; 60.js is the implemented version of LeetCode 60.",
}
NOTES = {
    "58.js": "The implementation is Spiral Matrix II (LeetCode 59); corrected its destination ID.",
    "90.go": "The existing implementation is unfinished/incorrect; retained for debugging.",
}


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def metadata(qid: int, slug: str) -> dict:
    cache = ROOT / ".cache" / "problems" / f"{qid}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    request = urllib.request.Request(
        "https://leetcode.com/graphql/",
        data=dump({"query": QUERY, "variables": {"titleSlug": slug}}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    question = result.get("data", {}).get("question")
    if not question:
        raise ValueError(f"Could not fetch {qid}: {result.get('errors', result)}")
    question["metaData"] = json.loads(question["metaData"])
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(dump(question), encoding="utf-8")
    return question


def python_body(source: str) -> str:
    """Retain imports, classes and functions; leave standalone demos in the original."""
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    demos = [(node.lineno - 1, node.end_lineno) for node in tree.body
             if (isinstance(node, ast.ClassDef) and node.name in ("ListNode", "TreeNode"))
             or not isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef,
                                      ast.FunctionDef, ast.AsyncFunctionDef))]
    for start, end in reversed(demos):
        del lines[start:end]
    return "".join(lines).strip()


def go_type(kind: str) -> str:
    if kind.endswith("[]"):
        return "[]" + go_type(kind[:-2])
    return {"integer": "int", "long": "int64", "boolean": "bool",
            "double": "float64", "character": "byte", "ListNode": "*ListNode",
            "TreeNode": "*TreeNode"}.get(kind, kind)


def py_type(kind: str) -> str:
    if kind.endswith("[]"):
        return "List[" + py_type(kind[:-2]) + "]"
    return {"integer": "int", "long": "int", "boolean": "bool",
            "double": "float", "string": "str", "character": "str"}.get(kind, kind)


def wrap_go(source: str, question: dict) -> str:
    meta = question["metaData"]
    body = re.sub(r"^package\s+\w+\s*", "", source, count=1).strip()
    # Node types are supplied by leetgo's I/O library and by LeetCode when submitted.
    body = re.sub(r"(?m)^type ListNode struct\s*\{[^}]*\}\s*", "", body).strip()
    header = ['"bufio"', '"fmt"', '"os"',
              '. "github.com/j178/leetgo/testutils/go"']
    main = ["func main() {", "\tstdin := bufio.NewReader(os.Stdin)"]
    for param in meta["params"]:
        main.append(f'\t{param["name"]} := Deserialize[{go_type(param["type"])}](ReadLine(stdin))')
    args = ", ".join(p["name"] for p in meta["params"])
    call = f'{meta["name"]}({args})'
    if meta["return"]["type"] == "void":
        main.append("\t" + call)
        index = (meta.get("output") or {}).get("paramindex", 0)
        main.append("\tans := " + meta["params"][index]["name"])
    else:
        main.append("\tans := " + call)
    main += ['\tfmt.Println("\\noutput:", Serialize(ans))', "}"]
    if int(question["questionFrontendId"]) in (26, 27, 80):
        main.insert(-1, '\tfmt.Println("mutated:", Serialize(' + meta["params"][0]["name"] + '))')
    return (f'// https://leetcode.com/problems/{question["titleSlug"]}/\n\n'
            + "package main\n\nimport (\n\t" + "\n\t".join(header) + ")\n\n"
            + "// @lc code=begin\n\n" + body + "\n\n// @lc code=end\n\n"
            + "\n".join(main) + "\n")


def wrap_python(source: str, question: dict) -> str:
    meta = question["metaData"]
    body = python_body(source)
    main = ['if __name__ == "__main__":']
    for param in meta["params"]:
        reader = (f'deserialize("{py_type(param["type"])}", read_line())'
                  if "Node" in param["type"] else 'json.loads(read_line())')
        main.append(f'    {param["name"]} = {reader}')
    args = ", ".join(p["name"] for p in meta["params"])
    call = f'Solution().{meta["name"]}({args})'
    if meta["return"]["type"] == "void":
        main.append("    " + call)
        index = (meta.get("output") or {}).get("paramindex", 0)
        main.append("    ans = " + meta["params"][index]["name"])
        kind = py_type(meta["params"][index]["type"])
    else:
        main.append("    ans = " + call)
        kind = py_type(meta["return"]["type"])
    encoder = f'serialize(ans, "{kind}")' if "Node" in kind else 'json.dumps(ans, ensure_ascii=False, allow_nan=False)'
    main.append(f'    print("\\noutput:", {encoder})')
    if int(question["questionFrontendId"]) in (26, 27, 80):
        main.append('    print("mutated:", json.dumps(' + meta["params"][0]["name"] + '))')
    return (f'# https://leetcode.com/problems/{question["titleSlug"]}/\n'
            + "import json\nfrom typing import *\nfrom leetgo_py import *\n\n"
            + "# @lc code=begin\n\n" + body + "\n\n# @lc code=end\n\n"
            + "\n".join(main) + "\n")


def examples(question: dict) -> str:
    """Extract paired inputs and outputs from the public example blocks."""
    markup = re.sub(r"</?(?:p|pre|div|li|h[1-6]|br)\b[^>]*>", "\n", question["content"], flags=re.I)
    content = html.unescape(re.sub(r"<[^>]+>", "", markup)).replace("\xa0", " ")
    decoder = json.JSONDecoder()
    cases = []
    for match in re.finditer(r"\bInput:\s*(.*?)\bOutput:\s*", content, re.S):
        # Pair within each statement example. The API's exampleTestcases list can be
        # stale or differently ordered (notably Count and Say and problem 2900).
        input_text = match[1]
        args, offset = [], 0
        for param in question["metaData"]["params"]:
            assignment = re.search(r"\b" + re.escape(param["name"]) + r"\s*=\s*", input_text[offset:])
            if not assignment:
                raise ValueError(f"Missing example parameter {param['name']} for {question['titleSlug']}")
            start = offset + assignment.end()
            value, end = decoder.raw_decode(input_text[start:])
            args.append(dump(value))
            offset = start + end
        output = dump(decoder.raw_decode(content[match.end():].lstrip())[0])
        cases.append("input:\n" + "\n".join(args) + "\noutput:\n" + output)
    if not cases:
        raise ValueError(f"Unpaired examples for {question['titleSlug']}")
    return "\n\n".join(cases) + "\n"


def main() -> None:
    cache = ROOT / ".cache/leetgo/cache/leetcode-questions.json"
    if not cache.exists():
        sys.exit("Run .tools/leetgo cache update with LEETGO_HOME=.cache/leetgo first.")
    questions = {int(q["questionFrontendId"]): q for q in
                 json.loads(cache.read_text(encoding="utf-8"))
                 if q["questionFrontendId"].isdigit()}
    migrated, skipped, kept = [], [], []
    sources = sorted([*ROOT.glob("[0-9]*.py"), *ROOT.glob("[0-9]*.go"),
                      *ROOT.glob("[0-9]*.js"), *ROOT.glob("Solution*.java")], key=lambda p: p.name)
    for source in sources:
        if source.name in EXCLUDED:
            skipped.append({"source": source.name, "reason": EXCLUDED[source.name]})
            continue
        qid = int(re.search(r"\d+", source.stem)[0])
        if source.name == "58.js":
            qid = 59
        lang = {".py": "python", ".js": "javascript", ".java": "java", ".go": "go"}[source.suffix]
        slug = questions[qid]["titleSlug"]
        folder = ROOT / lang / f"{qid:04d}.{slug}"
        config_file = folder / "problem.json"
        if config_file.exists():
            kept.append(str(folder.relative_to(ROOT)))
            print(f"KEEP {folder.relative_to(ROOT)}", flush=True)
            continue
        question = metadata(qid, slug)
        meta = question["metaData"]
        config = {"id": qid, "title": question["title"], "language": lang,
                  "source": source.name, "method": meta["name"],
                  "params": meta["params"], "return_type": meta["return"]["type"],
                  "unordered": UNORDERED.get(qid, [])}
        if meta["return"]["type"] == "void":
            config["output_arg"] = (meta.get("output") or {}).get("paramindex", 0)
        if qid in (26, 27, 80):
            config["check_prefix"] = 0
        text = source.read_text(encoding="utf-8-sig")
        if lang == "go":
            filename, text = "solution.go", wrap_go(text, question)
        elif lang == "python":
            filename, text = "solution.py", wrap_python(text, question)
        else:
            filename = source.name if lang == "java" else "solution.js"
            if lang == "java":
                config["class"] = source.stem
        config["file"] = filename
        if source.name in NOTES:
            config["note"] = NOTES[source.name]
        case_text = examples(question)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / filename).write_text(text, encoding="utf-8")
        (folder / "testcases.txt").write_text(case_text, encoding="utf-8")
        # Full official statement remains available online; keep the local pointer concise.
        (folder / "question.md").write_text(
            f'# {qid}. {question["title"]}\n\n[Problem statement](https://leetcode.com/problems/{slug}/)\n',
            encoding="utf-8")
        config_file.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        migrated.append(str(folder.relative_to(ROOT)))
        print(f"MIGRATE {folder.relative_to(ROOT)}", flush=True)
    report = {"migrated": migrated, "kept": kept, "excluded": skipped}
    (ROOT / ".cache/migration.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Created {len(migrated)} new copies; kept {len(kept)} existing problem directories; "
          f"left {len(skipped)} unmatched/draft files in the root.")


if __name__ == "__main__":
    main()
