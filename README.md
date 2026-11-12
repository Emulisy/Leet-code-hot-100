# 🔥 LeetCode Hot 100

This repository contains my solutions to the [LeetCode Hot 100](https://leetcode.com/problem-list/top-100-liked-questions/) — a curated list of the most frequently asked and highly upvoted problems on LeetCode.

Solutions live in `go/`, `python/`, `java/`, and `javascript/`. Each problem has one working implementation, local tests, and debugger support. Separate standalone exercises are kept in `extras/`.

[j178/leetgo](https://github.com/j178/leetgo#language-support) handles Go/Python generation and native local tests. Java and JavaScript use small adapters because leetgo does not provide native local runners for those languages. A shared Python command runs all four languages with the same `testcases.txt` format.

Install Python 3.10+, Go 1.26+, Node.js 18+, and a JDK 21+ on `PATH`. Java 21+ is needed by the existing N-Queens solution. From the repository root on Windows, run:

```powershell
.\tools\setup.ps1
```

Setup installs leetgo v1.4.19 into `.tools/`, downloads the Go I/O library, and creates `python/.venv/` with the Python I/O library and debugger. Java and JavaScript need no npm, Maven, or Gradle dependencies. Tool downloads, environments, and build outputs stay in ignored directories.

Run a problem, a language, or the whole collection:

```powershell
python tools/leet.py test go 62
python tools/leet.py test python 3
python tools/leet.py test java 36
python tools/leet.py test js 53
python tools/leet.py test java
python tools/leet.py test all
python tools/leet.py list
```

`py` and `js` are aliases for `python` and `javascript`. Tests run offline once dependencies are installed. Each case runs in a separate process, with a five-second runtime limit. Builds are cached until source or runner contents change. A failed assertion, exception, timeout, compilation error, or malformed fixture produces a nonzero exit code. The latest report is written to `.cache/latest-test-results.json`.

```powershell
python tools/leet.py test js 53 --case 2
python tools/leet.py test go 62 --timeout 10
python tools/leet.py test java 36 --cases path/to/custom-testcases.txt
```

Each problem has its own directory:

```text
go/0062.unique-paths/
  solution.go
  problem.json
  testcases.txt
  question.md
java/0036.valid-sudoku/
  Solution36.java
  problem.json
  testcases.txt
  question.md
```

Go/Python solutions include a stdin/stdout entry point outside the `@lc code=begin` / `@lc code=end` markers. Edit your algorithm between those markers. Java retains its existing class names. JavaScript functions stay in LeetCode's normal format; no `module.exports` is required.

Add cases to the problem's `testcases.txt`: one JSON value per argument, then one JSON expected result. For example, Go 62 takes two integers:

```text
input:
3
7
output:
28

input:
1
5
output:
1
```

Use compact arrays on a single line for array, matrix, and linked-list inputs. Linked lists use LeetCode arrays such as `[1,2,3]`; an empty list is `[]`. For void methods, the harness compares the mutated argument identified by `output_arg` in `problem.json`. Problems 26, 27, and 80 also check the actual array prefix as well as the returned length. `unordered: [0]` allows the outer result list to be reordered; `[0,1]` also allows its inner lists to be reordered. Duplicate counts remain significant. Numeric floating-point results use a tolerance of `1e-9`.

Generate a **new problem** and register its local runner in one command (internet required):

```powershell
python tools/leet.py add go 1
python tools/leet.py add python 1
python tools/leet.py add java 1
python tools/leet.py add js 1
```

This calls leetgo, creates the language's problem directory, and pairs the statement's sample inputs with their outputs. Existing problem directories are protected from overwriting. Fill in the generated solution before testing it. Java classes are named `Solution<ID>` to keep the workspace free of duplicate `Solution` classes.

The adapters support function-style problems. The Java adapter accepts primitive values, strings, and nested arrays, including `char[][]`, and can serialize nested collection results. The JavaScript adapter also supplies `ListNode` and `TreeNode`. Design problems with operation sequences need a dedicated driver. Review comparison rules when adding a problem with multiple valid answers; custom validators are already provided for problems 5 and 2900.

You can also run the native leetgo commands through the PowerShell wrapper, which selects this workspace's caches:

```powershell
.\tools\leetgo.ps1 cache update
.\tools\leetgo.ps1 test 62 -L
.\tools\leetgo.ps1 test 3 -l python -L
```

Native leetgo commands may fetch LeetCode metadata even with `-L`. Use `python tools/leet.py test ...` for offline execution. The configuration uses public requests without credentials. To switch to leetcode.cn, change `leetcode.site` in `leetgo.yaml`.

For **breakpoint debugging**, start one selected case in a terminal:

```powershell
python tools/leet.py test js 53 --case 1 --debug
# Or choose one of these instead:
python tools/leet.py test java 36 --case 1 --debug
python tools/leet.py test python 3 --case 1 --debug
python tools/leet.py test go 62 --case 1 --debug
```

Open the migrated solution, set a breakpoint, and start the matching **Attach: … local test** configuration from `.vscode/launch.json`. The process waits for the debugger and receives the selected sample automatically. JavaScript debugging is built into VS Code; the other languages need the extensions listed in `.vscode/extensions.json`. Go debugging also requires `dlv` on `PATH`.

| Language | Debugger | Local address |
| --- | --- | --- |
| JavaScript | Node inspector | `127.0.0.1:9229` |
| Java | JVM JDWP | `127.0.0.1:5005` |
| Python | debugpy | `127.0.0.1:5678` |
| Go | Delve | `127.0.0.1:2345` |

Other IDEs can attach to the same endpoints; for example, use a Remote JVM Debug configuration in IntelliJ IDEA for Java. Debug mode runs the selected case interactively and does not apply the normal assertion/timeout loop. Stop the waiting process with Ctrl+C when finished. Attach configuration references: [Node](https://code.visualstudio.com/docs/nodejs/nodejs-debugging), [Java](https://code.visualstudio.com/docs/java/java-debugging), [Python](https://code.visualstudio.com/docs/python/debugging), [Go](https://github.com/golang/vscode-go/wiki/debugging#remote-debugging).

Print code for pasting into LeetCode, excluding the Go/Python local driver and renaming the Java class to `Solution`:

```powershell
python tools/leet.py export go 62
python tools/leet.py export java 36
```

Check the runner and solution regressions with:

```powershell
python -m unittest discover -s tools/tests -v
go -C go test ./0090.subsets-ii
```

The regression tests cover carries and zero values in linked-list addition, mixed bracket nesting, empty and duplicate-valued merge inputs, 5,000-node group reversal, repeated Sudoku solves, JavaScript strict mode, and duplicate-free subsets. The runnable problem fixtures also include additional edge cases for the repaired solutions.

The shared problem-data helper in `tools/problem_data.py` supports new-problem generation. Installed tools, dependencies, and runtime caches are ignored by Git.
