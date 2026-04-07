import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "update_from_upstreams.py"
SPEC = importlib.util.spec_from_file_location("update_from_upstreams", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class BuildUpstreamsMarkdownTests(unittest.TestCase):
    def test_uses_stable_repo_identifiers_not_runtime_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp)
            (skill_dir / "references").mkdir()
            (skill_dir / "scripts").mkdir()
            auto_summary = MODULE.RepoSummary(
                name="AutoResearchClaw",
                repo_dir=Path("/tmp/worker/AutoResearchClaw"),
                head="abc123",
                tracked_files=["README.md"],
                notes=[],
            )
            ai_summary = MODULE.RepoSummary(
                name="AI-Researcher",
                repo_dir=Path("/private/tmp/worker/AI-Researcher"),
                head="def456",
                tracked_files=["README.md"],
                notes=[],
            )

            markdown = MODULE.build_upstreams_markdown(skill_dir, auto_summary, ai_summary)

            self.assertIn("- Repo: `AutoResearchClaw`", markdown)
            self.assertIn("- Repo: `AI-Researcher`", markdown)
            self.assertNotIn("/tmp/worker/AutoResearchClaw", markdown)
            self.assertNotIn("/private/tmp/worker/AI-Researcher", markdown)


class ReviewRefreshTests(unittest.TestCase):
    def test_skips_review_refresh_when_recorded_heads_match(self) -> None:
        existing = (
            "# AutoAcad Upstreams\n\n"
            "## AutoResearchClaw\n\n"
            "- HEAD: `abc123`\n\n"
            "## AI-Researcher\n\n"
            "- HEAD: `def456`\n"
        )

        self.assertFalse(MODULE.should_refresh_review(existing, "abc123", "def456"))

    def test_refreshes_review_when_recorded_heads_change(self) -> None:
        existing = (
            "# AutoAcad Upstreams\n\n"
            "## AutoResearchClaw\n\n"
            "- HEAD: `abc123`\n\n"
            "## AI-Researcher\n\n"
            "- HEAD: `def456`\n"
        )

        self.assertTrue(MODULE.should_refresh_review(existing, "abc123", "zzz999"))

    def test_review_markdown_does_not_embed_runtime_timestamp(self) -> None:
        markdown = MODULE.build_review_markdown(
            "## Summary\n\nStable output.\n",
            "abc123",
            "def456",
        )

        self.assertNotIn("Generated:", markdown)
        self.assertIn("# AutoAcad Upstream Review", markdown)
        self.assertIn("Reviewed AutoResearchClaw HEAD: `abc123`", markdown)
        self.assertIn("Reviewed AI-Researcher HEAD: `def456`", markdown)
        self.assertIn("Stable output.", markdown)


if __name__ == "__main__":
    unittest.main()
