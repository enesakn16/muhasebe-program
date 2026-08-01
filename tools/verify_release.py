#!/usr/bin/env python3
"""Validate distributable ZIP archives before they are published or installed."""

from __future__ import annotations

import argparse
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

MAX_UNCOMPRESSED_BYTES = 250 * 1024 * 1024
SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    "service-account.json",
    "service_role.key",
    "secrets.json",
}
REQUIRED_MEMBERS = {"VERSION.txt"}


class ReleaseValidationError(ValueError):
    """Raised when a release archive violates the distribution contract."""


def _normalise_member(name: str) -> PurePosixPath:
    normalised = name.replace("\\", "/")
    path = PurePosixPath(normalised)
    if not normalised or normalised.startswith("/") or path.is_absolute():
        raise ReleaseValidationError(f"unsafe absolute archive path: {name!r}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ReleaseValidationError(f"unsafe archive path traversal: {name!r}")
    return path


def validate_release(
    archive_path: Path,
    *,
    expected_version: str | None = None,
    max_uncompressed_bytes: int = MAX_UNCOMPRESSED_BYTES,
) -> dict[str, object]:
    if not archive_path.is_file():
        raise ReleaseValidationError(f"release archive not found: {archive_path}")

    seen: set[str] = set()
    total_uncompressed = 0

    try:
        with zipfile.ZipFile(archive_path) as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise ReleaseValidationError(f"CRC check failed for: {bad_member}")

            for info in archive.infolist():
                path = _normalise_member(info.filename)
                canonical = path.as_posix().casefold()
                if canonical in seen:
                    raise ReleaseValidationError(
                        f"duplicate archive member after normalisation: {info.filename}"
                    )
                seen.add(canonical)

                unix_mode = info.external_attr >> 16
                if stat.S_ISLNK(unix_mode):
                    raise ReleaseValidationError(
                        f"symbolic links are not allowed in releases: {info.filename}"
                    )

                if path.name.casefold() in SENSITIVE_NAMES:
                    raise ReleaseValidationError(
                        f"sensitive file must not be distributed: {info.filename}"
                    )

                total_uncompressed += info.file_size
                if total_uncompressed > max_uncompressed_bytes:
                    raise ReleaseValidationError(
                        "archive exceeds the allowed uncompressed size "
                        f"({max_uncompressed_bytes} bytes)"
                    )

            missing = {
                member
                for member in REQUIRED_MEMBERS
                if member.casefold() not in seen
            }
            if missing:
                raise ReleaseValidationError(
                    f"required archive members are missing: {', '.join(sorted(missing))}"
                )

            archived_version = archive.read("VERSION.txt").decode("utf-8-sig").strip()
            if not archived_version:
                raise ReleaseValidationError("VERSION.txt is empty")
            if expected_version is not None and archived_version != expected_version.strip():
                raise ReleaseValidationError(
                    "archive version mismatch: "
                    f"expected {expected_version.strip()!r}, got {archived_version!r}"
                )
    except zipfile.BadZipFile as exc:
        raise ReleaseValidationError(f"invalid ZIP archive: {archive_path}") from exc

    return {
        "archive": str(archive_path),
        "version": archived_version,
        "member_count": len(seen),
        "uncompressed_bytes": total_uncompressed,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="ZIP release archive to validate")
    parser.add_argument(
        "--version-file",
        type=Path,
        help="optional repository VERSION.txt that must match the archive",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    expected_version = None
    if args.version_file is not None:
        try:
            expected_version = args.version_file.read_text(encoding="utf-8-sig").strip()
        except OSError as exc:
            print(f"release validation failed: {exc}", file=sys.stderr)
            return 2

    try:
        result = validate_release(args.archive, expected_version=expected_version)
    except ReleaseValidationError as exc:
        print(f"release validation failed: {exc}", file=sys.stderr)
        return 1

    print(
        "release validated: "
        f"version={result['version']} members={result['member_count']} "
        f"uncompressed_bytes={result['uncompressed_bytes']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
