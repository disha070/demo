import os
import re
from pathlib import Path


def _issue_sections(body: str) -> dict[str, str]:
    headings = list(re.finditer(r"^### (.+?)\s*$", body, re.MULTILINE))
    sections = {}
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        sections[heading.group(1).strip()] = body[heading.end() : end].strip()
    return sections


def _required_section(sections: dict[str, str], name: str) -> str:
    value = sections.get(name, "").strip()
    if not value or value == "_No response_":
        raise ValueError(f"Issue is missing the required '{name}' field")
    return value


def _format_scenarios(source: str) -> str:
    source = re.sub(r"^\s*```(?:gherkin)?\s*$", "", source, flags=re.MULTILINE).strip()
    lines = source.splitlines()
    nonblank_indents = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
    if not nonblank_indents:
        raise ValueError("Scenarios field is empty")

    dedent_by = min(nonblank_indents)
    normalized = [line[dedent_by:].rstrip() if line.strip() else "" for line in lines]
    formatted = "\n".join(f"  {line}" if line else "" for line in normalized).rstrip()

    if not re.search(r"^  Scenario(?: Outline)?:\s+\S", formatted, re.MULTILINE):
        raise ValueError("Scenarios field must include a Scenario or Scenario Outline")
    if not re.search(r"^    (?:Given|When|Then|And|But)\s+\S", formatted, re.MULTILINE):
        raise ValueError("Scenarios field must include at least one Gherkin step")
    return formatted


def build_feature(issue_number: str, body: str) -> str:
    if not issue_number.isdigit():
        raise ValueError("Issue number must be numeric")

    sections = _issue_sections(body)
    feature_name = _required_section(sections, "Feature name").replace("\n", " ")
    story = _required_section(sections, "User story")
    story_lines = [line.strip() for line in story.splitlines() if line.strip()]
    if len(story_lines) != 3 or not story_lines[0].startswith("As ") or not story_lines[1].startswith("I want to ") or not story_lines[2].startswith("So that "):
        raise ValueError("User story must have 'As', 'I want to', and 'So that' lines")

    scenarios = _format_scenarios(_required_section(sections, "Scenarios (Gherkin)"))
    story_text = "\n".join(f"  {line}" for line in story_lines)
    return f"Feature: {feature_name}\n\n{story_text}\n\n{scenarios}\n"


def main() -> None:
    issue_number = os.environ["ISSUE_NUMBER"]
    issue_body = os.environ["ISSUE_BODY"]
    feature = build_feature(issue_number, issue_body)
    output = Path("features") / f"issue-{issue_number}.feature"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(feature, encoding="utf-8")


if __name__ == "__main__":
    main()