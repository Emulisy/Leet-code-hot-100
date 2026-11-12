"""Correctness regressions for repaired solutions."""
import itertools
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import leet


class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def linked(values):
    head = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def nodes(head):
    result, seen = [], set()
    while head is not None:
        if id(head) in seen:
            raise AssertionError("Returned linked list contains a cycle")
        seen.add(id(head))
        result.append(head)
        head = head.next
    return result


def solution_paths(language, qid):
    path, config = leet.problems(language, str(qid))[0]
    return [path.parent / config["file"]]


def python_solution(path):
    # Exercise the algorithm with a shared node model, without the local stdin driver.
    text = path.read_text(encoding="utf-8")
    body = text.split("# @lc code=begin", 1)[1].split("# @lc code=end", 1)[0]
    namespace = {"ListNode": ListNode}
    exec(compile(body, str(path), "exec"), namespace)
    return namespace["Solution"]()


class SolutionRegressionTests(unittest.TestCase):
    def test_add_two_numbers_zero_carries_and_different_lengths(self):
        rng = random.Random(2)
        pairs = [(0, 0), (0, 123), (9, 1), (999, 1), (99, 9999)]
        pairs += [(rng.randrange(10**100), rng.randrange(10**100)) for _ in range(100)]
        for path in solution_paths("python", 2):
            solution = python_solution(path)
            for a, b in pairs:
                with self.subTest(source=str(path.relative_to(leet.ROOT)), a=a, b=b):
                    left = linked([int(x) for x in str(a)[::-1]])
                    right = linked([int(x) for x in str(b)[::-1]])
                    answer = solution.addTwoNumbers(left, right)
                    self.assertEqual([node.val for node in nodes(answer)], [int(x) for x in str(a + b)[::-1]])

    def test_parentheses_exhaustive_short_strings_and_mixed_nesting(self):
        cases = ["([{}])", "([]{})", "{[(])}", "((()))", "([)]"]
        cases += ["".join(chars) for size in range(1, 6)
                  for chars in itertools.product("()[]{}", repeat=size)]
        for path in solution_paths("python", 20):
            solution = python_solution(path)
            for text in cases:
                remaining = text
                while True:
                    reduced = remaining.replace("()", "").replace("[]", "").replace("{}", "")
                    if reduced == remaining:
                        break
                    remaining = reduced
                self.assertEqual(solution.isValid(text), remaining == "", (str(path), text))

    def test_merge_sorted_lists_empty_ties_and_unequal_lengths(self):
        values = [list(items) for size in range(4)
                  for items in itertools.combinations_with_replacement((-1, 0, 1), size)]
        for path in solution_paths("python", 21):
            solution = python_solution(path)
            for a, b in itertools.product(values, repeat=2):
                left, right = linked(a), linked(b)
                original_ids = {id(node) for node in nodes(left) + nodes(right)}
                result = nodes(solution.mergeTwoLists(left, right))
                self.assertEqual([node.val for node in result], sorted(a + b), (str(path), a, b))
                self.assertEqual({id(node) for node in result}, original_ids)

    def test_reverse_k_group_handles_5000_nodes_without_recursion(self):
        values = [i % 1000 for i in range(5000)]
        for path in solution_paths("python", 25):
            solution = python_solution(path)
            for size in (1, 2, 3, 4999, 5000):
                head = linked(values)
                original_ids = {id(node) for node in nodes(head)}
                expected = []
                for start in range(0, len(values), size):
                    group = values[start:start + size]
                    expected.extend(reversed(group) if len(group) == size else group)
                result = nodes(solution.reverseKGroup(head, size))
                self.assertEqual([node.val for node in result], expected, (str(path), size))
                self.assertEqual({id(node) for node in result}, original_ids)

    def test_atoi_signs_prefixes_and_overflow_keep_existing_parser(self):
        cases = ["", "   ", "+", "-", "words and 987", "  +-12", "  -0012a42", "0-1",
                 "+2147483648", "-2147483649", "2147483647", "  +0 123", ".1", "\t123", "\n123"]
        for path in solution_paths("python", 8):
            solution = python_solution(path)
            for text in cases:
                match = re.match(r" *([+-]?[0-9]+)", text)
                number = int(match[1]) if match else 0
                expected = max(-(2**31), min(2**31 - 1, number))
                self.assertEqual(solution.myAtoi(text), expected, (str(path), text))

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_jump_game_works_in_strict_mode_without_leaking_globals(self):
        for path in solution_paths("js", 55):
            script = ('"use strict";\n' + path.read_text(encoding="utf-8") + '\n'
                      'const cases = [[[2,3,1,1,4],true],[[3,2,1,0,4],false],[[0],true],[[1,0,1,0],false]];'
                      'for(const [input,expected] of cases) {'
                      'if(canJump(input)!==expected) throw Error("Wrong jump result"); }'
                      'if(Object.hasOwn(globalThis,"maxReach")) throw Error("Leaked maxReach");')
            result = subprocess.run([leet.tool("node"), "-e", script], capture_output=True,
                                    text=True, encoding="utf-8", timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(shutil.which("javac") and shutil.which("java"), "JDK is not installed")
    def test_sudoku_solver_can_be_reused_for_two_boards(self):
        config_path, config = leet.problems("java", "37")[0]
        case = leet.read_cases(config_path.parent / "testcases.txt", 1)[0]
        board_rows = ["".join(row) for row in case["args"][0]]
        expected_rows = ["".join(row) for row in case["expected"]]
        driver = '''
public class ReuseSudoku {
    public static void main(String[] args) {
        Solution37 solver = new Solution37();
        String[] rows = INPUT;
        String[] expected = EXPECTED;
        for (int run = 0; run < 2; run++) {
            char[][] board = new char[rows.length][];
            for (int i = 0; i < rows.length; i++) board[i] = rows[i].toCharArray();
            solver.solveSudoku(board);
            for (int i = 0; i < rows.length; i++) {
                if (!new String(board[i]).equals(expected[i])) {
                    throw new AssertionError("Incorrect Sudoku on invocation " + (run + 1));
                }
            }
        }
    }
}
'''
        driver = driver.replace("INPUT", "{" + ",".join(json.dumps(row) for row in board_rows) + "}")
        driver = driver.replace("EXPECTED", "{" + ",".join(json.dumps(row) for row in expected_rows) + "}")
        for path in solution_paths("java", 37):
            with tempfile.TemporaryDirectory(prefix="sudoku-regression-", dir=leet.ROOT / ".cache") as temporary:
                folder = Path(temporary).resolve()
                self.assertTrue(folder.is_relative_to((leet.ROOT / ".cache").resolve()))
                driver_path = folder / "ReuseSudoku.java"
                driver_path.write_text(driver, encoding="utf-8")
                compile_result = subprocess.run([leet.tool("javac"), "-encoding", "UTF-8", "-d", str(folder),
                                                 str(path), str(driver_path)], capture_output=True, text=True,
                                                encoding="utf-8", timeout=30)
                self.assertEqual(compile_result.returncode, 0, compile_result.stderr)
                result = subprocess.run([leet.tool("java"), "-cp", str(folder), "ReuseSudoku"],
                                        capture_output=True, text=True, encoding="utf-8", timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
