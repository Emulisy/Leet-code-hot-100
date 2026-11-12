"""Public problem metadata and sample-case parsing for new-problem generation."""
from __future__ import annotations

import html
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERY = """query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId title titleSlug content metaData exampleTestcases
  }
}"""

# List depths whose order is irrelevant. Duplicate counts still matter.
UNORDERED = {15: [0], 17: [0], 18: [0], 22: [0], 30: [0], 39: [0],
             40: [0], 46: [0], 47: [0], 49: [0, 1], 51: [0],
             77: [0], 78: [0], 90: [0]}


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


def examples(question: dict) -> str:
    """Pair inputs and outputs within each statement example, not API list order."""
    markup = re.sub(r"</?(?:p|pre|div|li|h[1-6]|br)\b[^>]*>", "\n", question["content"], flags=re.I)
    content = html.unescape(re.sub(r"<[^>]+>", "", markup)).replace("\xa0", " ")
    decoder = json.JSONDecoder()
    cases = []
    for match in re.finditer(r"\bInput:\s*(.*?)\bOutput:\s*", content, re.S):
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
