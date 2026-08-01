from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.verify_release import ReleaseValidationError, validate_release


class VerifyReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)

    def create_archive(self, members: dict[str, bytes | str]) -> Path:
        archive_path = self.root / "release.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in members.items():
                archive.writestr(name, content)
        return archive_path

    def test_accepts_valid_release_and_matches_version(self) -> None:
        archive_path = self.create_archive(
            {
                "VERSION.txt": "1.4.2\n",
                "app/__init__.py": "",
                "app/main.py": "print('safe')\n",
            }
        )

        result = validate_release(archive_path, expected_version="1.4.2")

        self.assertEqual(result["version"], "1.4.2")
        self.assertEqual(result["member_count"], 3)

    def test_rejects_path_traversal(self) -> None:
        archive_path = self.create_archive(
            {"VERSION.txt": "1.4.2", "../outside.py": "unsafe"}
        )

        with self.assertRaisesRegex(ReleaseValidationError, "path traversal"):
            validate_release(archive_path)

    def test_rejects_sensitive_environment_file(self) -> None:
        archive_path = self.create_archive(
            {"VERSION.txt": "1.4.2", "config/.env": "SUPABASE_KEY=secret"}
        )

        with self.assertRaisesRegex(ReleaseValidationError, "sensitive file"):
            validate_release(archive_path)

    def test_rejects_missing_version_marker(self) -> None:
        archive_path = self.create_archive({"app/main.py": "print('missing version')"})

        with self.assertRaisesRegex(ReleaseValidationError, "required archive members"):
            validate_release(archive_path)

    def test_rejects_version_mismatch(self) -> None:
        archive_path = self.create_archive({"VERSION.txt": "1.4.1"})

        with self.assertRaisesRegex(ReleaseValidationError, "version mismatch"):
            validate_release(archive_path, expected_version="1.4.2")

    def test_rejects_uncompressed_size_limit(self) -> None:
        archive_path = self.create_archive(
            {"VERSION.txt": "1.4.2", "app/payload.bin": b"x" * 128}
        )

        with self.assertRaisesRegex(ReleaseValidationError, "uncompressed size"):
            validate_release(archive_path, max_uncompressed_bytes=64)


if __name__ == "__main__":
    unittest.main()
