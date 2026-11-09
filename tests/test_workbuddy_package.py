"""Contract tests for the standalone WorkBuddy package validator."""

from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_workbuddy import build_workbuddy  # noqa: E402
from validate_package import _frontmatter  # noqa: E402
from validate_workbuddy import validate_workbuddy  # noqa: E402
import yaml  # noqa: E402


class WorkBuddyPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / "research-first"
        (self.package / "references").mkdir(parents=True)
        (self.package / "templates").mkdir()
        (self.package / "references" / "guide.md").write_text(
            "# Guide\n\nTemplate @templates/report.md.\n", encoding="utf-8"
        )
        (self.package / "templates" / "report.md").write_text("# Report\n", encoding="utf-8")
        self.write_skill(self.skill_text())

    @staticmethod
    def skill_text(frontmatter=None, body=None):
        fields = frontmatter or {
            "name": "research-first",
            "description": "Research material feature choices.",
            "description_zh": "研究重要功能的方案选择。",
            "description_en": "Research choices for material features.",
            "version": "1.0.0",
            "author": "AnxForever",
        }
        yaml_text = "\n".join(f"{key}: {value!r}" for key, value in fields.items())
        return (
            f"---\n{yaml_text}\n---\n\n"
            + (body if body is not None else "Read @references/guide.md and use @templates/report.md.\n")
        )

    def write_skill(self, content):
        (self.package / "SKILL.md").write_text(content, encoding="utf-8")

    def test_complete_package_needs_no_openai_metadata(self):
        self.assertEqual(validate_workbuddy(self.package), [])
        self.assertFalse((self.package / "agents" / "openai.yaml").exists())

    def test_required_frontmatter_fields_must_be_nonempty_strings(self):
        complete = {
            "name": "research-first",
            "description": "English summary",
            "description_zh": "中文说明",
            "description_en": "English description",
            "version": "1.0.0",
            "author": "AnxForever",
        }
        for missing in ("description", "description_zh", "description_en", "version", "author"):
            with self.subTest(field=missing):
                fields = {key: value for key, value in complete.items() if key != missing}
                self.write_skill(self.skill_text(fields))
                errors = validate_workbuddy(self.package)
                self.assertTrue(any(f"{missing} must be" in error for error in errors))

        for invalid in ("", "   ", 7, False):
            with self.subTest(value=invalid):
                fields = dict(complete, author=invalid)
                self.write_skill(self.skill_text(fields))
                errors = validate_workbuddy(self.package)
                self.assertTrue(any("author must be" in error for error in errors))

    def test_name_is_optional_but_a_present_name_matches_the_package(self):
        optional = {
            "description": "English summary",
            "description_zh": "中文说明",
            "description_en": "English description",
            "version": "stable",
            "author": "AnxForever",
        }
        self.write_skill(self.skill_text(optional))
        self.assertEqual(validate_workbuddy(self.package), [])

        mismatch = dict(optional, name="different-skill")
        self.write_skill(self.skill_text(mismatch))
        errors = validate_workbuddy(self.package)
        self.assertTrue(any("must match package directory" in error for error in errors))

        explicit_null = dict(optional, name=None)
        self.write_skill(self.skill_text(explicit_null))
        errors = validate_workbuddy(self.package)
        self.assertTrue(any("name must be" in error for error in errors))

    def test_missing_and_traversing_resource_paths_are_rejected(self):
        for resource, expected in (
            ("@references/missing.md", "missing package resource"),
            ("@templates/../references/guide.md", "escapes templates/"),
            ("@references/%2e%2e/%2e%2e/outside.md", "escapes references/"),
            ("@templates//outside.md", "must stay under templates/"),
        ):
            with self.subTest(resource=resource):
                self.write_skill(self.skill_text(body=f"Use {resource}.\n"))
                errors = validate_workbuddy(self.package)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_entrypoint_uses_resource_directives_without_email_or_code_false_positives(self):
        body = (
            "Email team@references.example for help.\n"
            "Example: `@references/not-a-real-file.md`.\n"
            "```text\n@templates/not-a-real-file.md\n```\n"
            "Load @references/guide.md.\n"
        )
        self.write_skill(self.skill_text(body=body))
        self.assertEqual(validate_workbuddy(self.package), [])

        self.write_skill(self.skill_text(body="See [the guide](references/guide.md).\n"))
        errors = validate_workbuddy(self.package)
        self.assertTrue(any("use @references/..." in error for error in errors))

    def test_nested_reference_links_use_root_relative_directives(self):
        (self.package / "references" / "other.md").write_text("# Other\n", encoding="utf-8")
        (self.package / "references" / "guide.md").write_text(
            "[other](other.md)\n", encoding="utf-8"
        )
        errors = validate_workbuddy(self.package)
        self.assertTrue(any(
            "references/guide.md" in error and "use @references/..." in error
            for error in errors
        ))

    def test_markdown_links_are_checked_in_nested_docs_and_external_links_are_allowed(self):
        (self.package / "references" / "guide.md").write_text(
            "[external](https://example.org/docs)\n[missing](../absent.md)\n", encoding="utf-8"
        )
        self.write_skill(self.skill_text(body="Read @references/guide.md.\n"))
        errors = validate_workbuddy(self.package)
        self.assertTrue(any("missing or out-of-package Markdown target" in error for error in errors))

    def test_invalid_utf8_in_any_shipped_markdown_is_rejected(self):
        (self.package / "references" / "guide.md").write_bytes(b"\xff")
        errors = validate_workbuddy(self.package)
        self.assertTrue(any("references/guide.md: cannot be read as UTF-8" in error for error in errors))

    def test_missing_entrypoint_is_reported(self):
        (self.package / "SKILL.md").unlink()
        self.assertEqual(validate_workbuddy(self.package), ["missing SKILL.md"])

    def test_builder_archive_is_rooted_self_contained_and_contains_only_runtime_files(self):
        output_dir = self.package.parent / "release"
        archive_path, manifest_path = build_workbuddy(
            ROOT, output_dir, metadata_path=ROOT / "packaging" / "workbuddy.yaml"
        )

        with ZipFile(archive_path) as archive:
            names = set(archive.namelist())
            roots = {name.split("/", 1)[0] for name in names}
            self.assertEqual(roots, {"research-first"})
            relative = {name.removeprefix("research-first/") for name in names}
            self.assertTrue({
                "SKILL.md",
                "LICENSE",
                "references/jev-cases.json",
                "references/feature-evidence-ledger.md",
                "templates/research-report-template.md",
                "templates/project-identity-card.md",
                "scripts/jev_check.py",
                "scripts/requirements-jev.txt",
            }.issubset(relative))
            self.assertFalse(any(
                path.split("/", 1)[0] in {"agents", "assets", "evals", "tests", "packaging"}
                for path in relative
            ))
            self.assertFalse(any(path.startswith("scripts/") and path not in {
                "scripts/jev_check.py", "scripts/requirements-jev.txt"
            } for path in relative))

            extracted = self.package.parent / "unzipped"
            archive.extractall(extracted)

        shipped = extracted / "research-first"
        self.assertEqual(validate_workbuddy(shipped), [])
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["checks"]["package_structure"], "passed")
        self.assertEqual(manifest["checks"]["zip_round_trip"], "passed")
        self.assertEqual(manifest["checks"]["workbuddy_runtime"], "unverified")

        skill_text = (shipped / "SKILL.md").read_text(encoding="utf-8")
        metadata, error, body = _frontmatter(skill_text)
        self.assertIsNone(error)
        self.assertTrue({
            "description", "description_zh", "description_en", "version", "author"
        }.issubset(metadata))
        self.assertIn("@references/adapting-depth.md", body)
        self.assertIn("@templates/research-report-template.md", body)
        self.assertIn("Resolve @references/ and @templates/ paths", body)

    def test_builder_rejects_missing_workbuddy_metadata_before_writing_output(self):
        output_dir = self.package.parent / "bad-release"
        metadata_path = self.package.parent / "incomplete-workbuddy.yaml"
        metadata_path.write_text(
            "name: research-first\nversion: 1.0.0\n"
            "description: summary\ndescription_en: English\nauthor: AnxForever\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "description_zh"):
            build_workbuddy(ROOT, output_dir, metadata_path=metadata_path)
        self.assertFalse(output_dir.exists())


if __name__ == "__main__":
    unittest.main()
