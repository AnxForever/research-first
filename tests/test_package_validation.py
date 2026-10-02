"""Distribution checks exercise complete temporary skill packages."""

from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_package import validate_package  # noqa: E402


VALID_SKILL = """---
name: research-first
description: Research existing products, open-source solutions, reusable libraries, and primary documentation before selecting how to implement a substantial feature. Show alternatives and tradeoffs, and verify the result with evidence.
---
# Research First

Investigate existing products, open-source solutions, and reusable libraries.
Show reuse options and tradeoffs before implementing a material feature.
Verify each material feature with evidence and acceptance results.

Inline example: `[broken](missing-inline-example.md)`.

```markdown
[fenced example](missing-fenced-example.md)
```

[guide](references/guide.md)
[guide-reference][guide]
[guide]: references/guide.md "Reference guide"
[remote](https://example.com/guide.md)
[templated](<{{ docs_root }}/guide.md>)
"""


VALID_AGENT = """interface:
  display_name: Research First
  short_description: Research existing solutions and present alternatives
  default_prompt: >-
    Use $research-first to research existing products, open-source solutions,
    and reusable libraries; show reuse options and tradeoffs before implementing;
    verify the result with evidence.
"""


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / "research-first"
        (self.package / "agents").mkdir(parents=True)
        (self.package / "references").mkdir()
        (self.package / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
        self.write_skill(VALID_SKILL)
        self.write_agent(VALID_AGENT)

    def write_skill(self, content):
        (self.package / "SKILL.md").write_text(content, encoding="utf-8")

    def write_agent(self, content):
        (self.package / "agents" / "openai.yaml").write_text(content, encoding="utf-8")

    def test_complete_package_passes_and_ignores_urls_templates_and_code_examples(self):
        self.assertEqual(validate_package(self.package), [])

    def test_missing_local_reference_fails_with_file_and_line(self):
        with (self.package / "SKILL.md").open("a", encoding="utf-8") as skill:
            skill.write("\n[missing guide](references/not-shipped.md)\n")

        errors = validate_package(self.package)

        self.assertTrue(any("SKILL.md:" in error and "references/not-shipped.md" in error for error in errors))

    def test_reference_outside_distributable_package_fails(self):
        external = self.package.parent / "outside.md"
        external.write_text("# Outside\n", encoding="utf-8")
        (self.package / "README.md").write_text("[outside](../outside.md)\n", encoding="utf-8")

        errors = validate_package(self.package)

        self.assertTrue(any("README.md" in error and "../outside.md" in error for error in errors))

    def test_invalid_name_and_description_are_rejected(self):
        for invalid_name in ("Research_First", "réséarch-first", "research--first"):
            with self.subTest(name=invalid_name):
                self.write_skill(VALID_SKILL.replace("name: research-first", f"name: {invalid_name}", 1))
                errors = validate_package(self.package)
                self.assertTrue(any("name must be" in error for error in errors))

        description = (
            "Research existing products, open-source solutions, reusable libraries, and primary "
            "documentation before selecting how to implement a substantial feature. Show "
            "alternatives and tradeoffs, and verify the result with evidence."
        )
        self.write_skill(VALID_SKILL.replace(f"description: {description}", "description: []", 1))
        errors = validate_package(self.package)
        self.assertTrue(any("description must be" in error for error in errors))

    def test_incomplete_frontmatter_is_rejected(self):
        self.write_skill(VALID_SKILL.replace("name: research-first", "name: research-first\nTODO: choose a name", 1))
        errors = validate_package(self.package)

        self.assertTrue(any("unfinished scaffold marker" in error for error in errors))

    def test_unfinished_scaffold_instructions_are_rejected(self):
        self.write_skill(VALID_SKILL + "\nFIXME: replace this with final guidance\n")

        errors = validate_package(self.package)

        self.assertTrue(any("unfinished scaffold marker" in error for error in errors))

    def test_default_prompt_must_call_this_skill_without_a_wording_quota(self):
        wrong_skill = VALID_AGENT.replace("$research-first", "$other-skill", 1)
        self.write_agent(wrong_skill)
        errors = validate_package(self.package)
        self.assertTrue(any("must invoke $research-first" in error for error in errors))

        vague_prompt = VALID_AGENT.replace(
            "    Use $research-first to research existing products, open-source solutions,\n"
            "    and reusable libraries; show reuse options and tradeoffs before implementing;\n"
            "    verify the result with evidence.",
            "    Use $research-first to help with the task.",
        )
        self.write_agent(vague_prompt)
        errors = validate_package(self.package)
        self.assertEqual(errors, [])

    def test_checkout_directory_name_does_not_change_skill_identity(self):
        renamed = self.package.parent / "temporary-checkout"
        self.package.rename(renamed)
        self.assertEqual(validate_package(renamed), [])

    def test_missing_required_package_files_are_reported(self):
        (self.package / "agents" / "openai.yaml").unlink()

        errors = validate_package(self.package)

        self.assertTrue(any("missing agents/openai.yaml" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
