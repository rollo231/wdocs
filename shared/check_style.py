"""wdocs 점검: 한국어 팀 문서의 문체 표시, 코드 경로, 행 번호, 제목 형식, 문서 종류별 구조를 센다.

사용: python3 check_style.py --kind <roadmap|poc|prd|design> <문서.md>
코드 블록(```)과 인라인 코드(`...`) 안은 세지 않는다.
"""
import argparse
import re
import sys

CHECKS = [
    ("조사 띄어쓰기", r"[A-Za-z0-9_)\]`] (을|를|이|가|에|은|는|의|로|으로|와|과|에서|에게)(?=[ .,)]|$)"),
    ("가운뎃점 ·", r"·"),
    ("긴 대시 —", r"—"),
    ("낫표 「」", r"[「」]"),
    ("굵은 글씨 **", r"\*\*"),
    ("번호 참조 (§2, 5번 항목, 섹션 4, 3절)", r"§ ?\d|\d+번 항목|섹션 ?\d|\d+ ?절(?![\w가-힣])"),
    ("로컬 경로 (~/, /Users/, /home/, /tmp/)", r"~/|/Users/|/home/|/private/tmp/|/tmp/"),
]

RAW_CHECKS = [
    ("파일 경로", r"(?<![\w/])[\w.-]+/[\w./-]*\.(py|tsx?|jsx?|go|java|rb|sql)\b|\b[\w-]+\.(py|tsx?|jsx?)\b"),
    ("행 번호", r"\d+(-\d+)?행"),
]

# 문서 종류별로 반드시 있어야 하는 큰 제목(번호 뒤 이름). 목차와 Open issues 형식 점검 여부.
KINDS = {
    "roadmap": {"required": ["순서와 기준"], "toc": False, "issues": False},
    "poc": {
        "required": ["가설과 목표", "성공과 실패 기준", "범위와 하지 않는 것", "방법", "진행과 측정", "판정"],
        "toc": False,
        "issues": False,
    },
    "prd": {
        "required": ["문서 정보", "문제", "목표", "하지 않는 것", "성공 지표", "시나리오"],
        "toc": False,
        "issues": True,
    },
    "design": {
        "required": ["문서 정보", "목차", "맥락", "설계", "검토한 대안"],
        "toc": True,
        "issues": True,
    },
}


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "`x`", text)


def split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections, cur = {}, None
    for line in lines:
        m = re.match(r"^## \d+\. (.+)$", line)
        if m:
            cur = m.group(1).strip()
            sections[cur] = []
        elif cur:
            sections[cur].append(line)
    return sections


def heading_checks(lines: list[str]) -> list[str]:
    heads = [line for line in lines if line.startswith("## ")]
    bad = [h for h in heads if not re.match(r"^## \d+\. \S.*$", h)]
    nums = [int(m.group(1)) for h in heads if (m := re.match(r"^## (\d+)\. ", h))]
    if nums != list(range(1, len(nums) + 1)):
        bad.append(f"번호 순서: {nums}")
    return bad


def toc_checks(lines: list[str], sections: dict[str, list[str]]) -> list[str]:
    if "목차" not in sections:
        return ["목차 절이 없다"]
    out = []
    toc = sections["목차"]
    listed = [m.group(1) + ". " + re.sub(r"^\[(.+?)\]\(#[^)]*\)$", r"\1", m.group(2).strip())
              for line in toc if (m := re.match(r"^\s*(\d+)\. (.+)$", line))]
    unlinked = [line for line in toc if re.match(r"^\s*\d+\. ", line) and not re.search(r"\]\(#", line)]
    if unlinked:
        out.append(f"링크 없는 목차 항목 {len(unlinked)}개(예: {unlinked[0].strip()})")
    actual = [h[3:].strip() for h in lines if re.match(r"^## \d+\. ", h)]
    if listed != actual:
        missing = [x for x in actual if x not in listed]
        extra = [x for x in listed if x not in actual]
        out.append(f"목차와 제목이 다름. 없는 것 {missing}, 남는 것 {extra}")
    return out


def issue_checks(sections: dict[str, list[str]]) -> list[str]:
    out = []
    body = [line for name, ls in sections.items()
            if name not in ("Open issues", "Closed issues", "목차") for line in ls]
    for m in re.finditer(r"\(Open issues? \d+[^)]*\)", "\n".join(body)):
        out.append(f"본문에 이슈 표시가 있다: {m.group(0)}")
    blocks: dict[str, list[str]] = {}
    cur = None
    for line in sections.get("Open issues", []):
        m = re.match(r"^### Issue (\d+)\.", line)
        if m:
            cur = m.group(1)
            blocks[cur] = []
        elif line.startswith("### "):
            cur = None
        elif cur:
            blocks[cur].append(line)
    for num, block in blocks.items():
        first = next((line for line in block if line.strip()), "")
        if not first.startswith("Decision:"):
            out.append(f"Issue {num}: 블록 첫 줄이 Decision:이 아니다")
        aff = next((line for line in block if line.startswith("Affects:")), None)
        if not aff:
            out.append(f"Issue {num}: Affects:가 없다")
        else:
            for name in [x.strip() for x in aff[len("Affects:"):].split(",") if x.strip()]:
                if name.split("(")[0].strip() not in sections:
                    out.append(f"Issue {num}: Affects의 절 '{name}'이 문서에 없다")
        if not any(line.startswith("Next step:") for line in block):
            out.append(f"Issue {num}: Next step:이 없다")
    return out


def structure_checks(raw: str, kind: str) -> list[tuple[str, list[str]]]:
    lines = re.sub(r"```.*?```", "", raw, flags=re.S).splitlines()
    sections = split_sections(lines)
    spec = KINDS[kind]
    results = [("제목 형식(## N. 제목)", heading_checks(lines))]
    missing = [name for name in spec["required"] if name not in sections]
    results.append((f"{kind} 필수 절", [f"없는 절: {name}" for name in missing]))
    if spec["toc"]:
        results.append(("목차", toc_checks(lines, sections)))
    if spec["issues"]:
        results.append(("Open issues 형식", issue_checks(sections)))
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True, choices=sorted(KINDS))
    ap.add_argument("path")
    args = ap.parse_args()
    raw = open(args.path, encoding="utf-8").read()
    body = strip_code(raw)
    no_fence = re.sub(r"```.*?```", "", raw, flags=re.S)
    total = 0
    for label, pattern in RAW_CHECKS:
        hits = [(no, line.strip()[:80]) for no, line in enumerate(no_fence.splitlines(), 1) if re.search(pattern, line)]
        total += len(hits)
        print(f"{label}: {len(hits)}")
        for no, line in hits[:3]:
            print(f"    {no}: {line}")
    for label, pattern in CHECKS:
        hits = [(no, line.strip()[:80]) for no, line in enumerate(body.splitlines(), 1)
                for _ in re.finditer(pattern, line)]
        total += len(hits)
        print(f"{label}: {len(hits)}")
        for no, line in hits[:3]:
            print(f"    {no}: {line}")
    for label, hits in structure_checks(raw, args.kind):
        total += len(hits)
        print(f"{label}: {len(hits)}")
        for h in hits[:5]:
            print(f"    {h}")
    print(f"합계: {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
