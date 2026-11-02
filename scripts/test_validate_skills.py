import json
import tempfile
import unittest
from pathlib import Path

import validate_skills


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "example"
        self.skill.mkdir()

    def create_skill(self):
        (self.skill / "SKILL.md").write_text(
            "---\nname: example\ndescription: Example skill.\n---\n# Example\n"
        )
        (self.skill / "README.md").write_text("# Example\n")
        (self.skill / "metadata.json").write_text(json.dumps({
            "version": "1.0.0", "author": "Example", "abstract": "Example",
            "categories": 1, "rules": 1,
            "sections": [{"prefix": "check", "name": "Check", "count": 1}],
        }))
        (self.skill / "rules").mkdir()
        (self.skill / "rules" / "check.md").write_text("# Check\n")

    def test_missing_skill_entry(self):
        self.assertTrue(any("missing SKILL.md" in e for e in validate_skills.validate_skill(self.skill)))

    def test_rule_count_checks_real_files(self):
        self.create_skill()
        self.assertEqual([], validate_skills.validate_skill(self.skill))
        (self.skill / "rules" / "check.md").unlink()
        self.assertTrue(any("count differs" in e for e in validate_skills.validate_skill(self.skill)))

    def test_invalid_or_duplicate_frontmatter_rejected(self):
        self.create_skill()
        (self.skill / "SKILL.md").write_text(
            '---\nname: example\nname: example\ndescription: [broken\n---\n'
        )
        errors = validate_skills.validate_skill(self.skill)
        self.assertTrue(any("duplicate" in e for e in errors))
        self.assertTrue(any("scalar" in e for e in errors))

    def test_link_heading_and_missing_file(self):
        document = self.skill / "README.md"
        document.write_text("# My heading\n[Good](#my-heading)\n[Bad](#missing)\n[File](absent.md)\n")
        errors = validate_skills.validate_links(document)
        self.assertEqual(2, len(errors))
        self.assertTrue(any("unresolved heading" in e for e in errors))
        self.assertTrue(any("unresolved link" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
