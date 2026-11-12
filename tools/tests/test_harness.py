"""Regression tests for sample parsing and local-runner failure detection."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import leet
import problem_data


class HarnessTests(unittest.TestCase):
    def setUp(self):
        (leet.ROOT / ".cache").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=leet.ROOT / ".cache")
        self.folder = Path(self.temp.name)
        self.assertTrue(self.folder.resolve().is_relative_to((leet.ROOT / ".cache").resolve()))
        self.addCleanup(self.temp.cleanup)

    def fixture(self, text, nargs):
        path = self.folder / "cases.txt"
        path.write_text(text, encoding="utf-8")
        return leet.read_cases(path, nargs)

    def test_pairs_statement_examples_instead_of_api_order(self):
        question = {"titleSlug": "count-and-say", "metaData": {"params": [{"name": "n"}]},
                    "exampleTestcases": "1\n4", "content":
                    '<p>Input: n = 4</p><p>Output: "1211"</p>'
                    '<p>Input: n = 1</p><p>Output: "1"</p>'}
        cases = self.fixture(problem_data.examples(question), 1)
        self.assertEqual([(c["args"], c["expected"]) for c in cases], [([4], "1211"), ([1], "1")])

    def test_multiline_example_and_in_place_output_annotation(self):
        question = {"titleSlug": "example", "metaData": {"params": [{"name": "nums"}]},
                    "content": '<pre>Input: nums = [1,1,2]\nOutput: 2, nums = [1,2,_]</pre>'
                               '<pre>Input: nums = []\nOutput: [\n&nbsp; "a  b",\n "c"\n]</pre>'}
        cases = self.fixture(problem_data.examples(question), 1)
        self.assertEqual(cases[0]["expected"], 2)
        self.assertEqual(cases[1]["expected"], ["a  b", "c"])

    def test_missing_expected_output_rejected(self):
        with self.assertRaises(ValueError):
            self.fixture('input:\n[1,2]\noutput:\n', 1)

    def test_wrong_argument_count_rejected(self):
        with self.assertRaises(ValueError):
            self.fixture('input:\n1\noutput:\n2\n', 2)

    def test_unordered_results_preserve_duplicate_counts(self):
        config = {"id": 78, "unordered": [0]}
        case = {"expected": [[], [1], [2]]}
        self.assertTrue(leet.matches(config, case, [[2], [], [1]]))
        self.assertFalse(leet.matches(config, case, [[1], [], [1]]))

    def test_boolean_and_large_integer_mismatches_fail(self):
        self.assertFalse(leet.same(True, 1))
        self.assertFalse(leet.same(10**12, 10**12 + 1))
        self.assertTrue(leet.same(0.1 + 0.2, 0.3))

    def test_returning_correct_k_without_mutating_fails(self):
        config = {"id": 80, "check_prefix": 0}
        case = {"args": [[1, 1, 1, 2, 2, 3]]}
        self.assertFalse(leet.check_prefix(config, case, 5, [1, 1, 1, 2, 2, 3]))
        self.assertTrue(leet.check_prefix(config, case, 5, [1, 1, 2, 2, 3, 3]))

    def test_missing_example_parameter_rejected(self):
        question = {"titleSlug": "example", "metaData": {"params": [{"name": "n"}]},
                    "content": "Input: other = 1\nOutput: 2"}
        with self.assertRaisesRegex(ValueError, "Missing example parameter n"):
            problem_data.examples(question)

    def execute(self, language, source, params, result_type, stdin):
        config = {"id": 999999, "language": language, "method": "echo",
                  "params": [{"name": f"arg{i}", "type": kind} for i, kind in enumerate(params)],
                  "return_type": result_type}
        if language == "java":
            config.update({"class": "Solution", "file": "Solution.java"})
        else:
            config["file"] = "solution.js" if language == "javascript" else "solution.py"
        path = self.folder / "problem.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        (self.folder / config["file"]).write_text(source, encoding="utf-8")
        command, cwd = leet.command_for(path, config)
        return subprocess.run(command, input=stdin, capture_output=True, text=True,
                              encoding="utf-8", cwd=cwd, env=leet.environment(), timeout=3)

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_javascript_linked_list_round_trip_and_demo_logging(self):
        result = self.execute("javascript", 'console.log("demo"); var echo = head => head;',
                              ["ListNode"], "ListNode", '[1,2,3]\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(leet.extract_output(result.stdout), [1, 2, 3])

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_javascript_infinite_loop_times_out(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            self.execute("javascript", 'var echo = () => { while (true) {} };', [], "integer", '')

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_javascript_exception_is_a_failure(self):
        result = self.execute("javascript", 'var echo = () => { throw Error("broken"); };', [], "integer", '')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("broken", result.stderr)

    @unittest.skipUnless(shutil.which("javac") and shutil.which("java"), "JDK is not installed")
    def test_java_char_matrix_and_escaped_string_round_trip(self):
        value = 'quote" slash\\ newline\n unicode\u4e2d'
        source = ('public class Solution { public String[] echo(char[][] board, String text) { '
                  'return new String[]{new String(board[0]), text}; } }')
        result = self.execute("java", source, ["character[][]", "string"], "string[]",
                              json.dumps([["a", "b"]]) + "\n" + json.dumps(value) + "\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(leet.extract_output(result.stdout), ["ab", value])

    def test_python_escaped_string_io(self):
        value = 'quote" slash\\ newline\n'
        config_path, config = leet.problems("python", "14")[0]
        command, cwd = leet.command_for(config_path, config)
        result = subprocess.run(command, input=json.dumps([value, value]) + "\n", capture_output=True,
                                text=True, encoding="utf-8", cwd=cwd, env=leet.environment(), timeout=3)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(leet.extract_output(result.stdout), value)


if __name__ == "__main__":
    unittest.main()
