from __future__ import annotations

import base64
import io
import shutil
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PARTS_DIR = ROOT / ".bootstrap"


def safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    destination = destination.resolve()
    for member in archive.getmembers():
        target = (destination / member.name).resolve()
        if destination not in target.parents and target != destination:
            raise RuntimeError(f"Güvensiz arşiv yolu engellendi: {member.name}")
    archive.extractall(destination)


def main() -> None:
    parts = sorted(PARTS_DIR.glob("xz.part*"))
    if not parts:
        raise SystemExit("Kaynak arşiv parçaları bulunamadı: .bootstrap/xz.part*")

    encoded = "".join(part.read_text(encoding="ascii") for part in parts)
    archive_bytes = base64.b64decode(encoded, validate=True)

    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:xz") as archive:
        safe_extract(archive, ROOT)

    shutil.rmtree(PARTS_DIR, ignore_errors=True)
    bootstrap_workflow = ROOT / ".github" / "workflows" / "bootstrap-source.yml"
    bootstrap_workflow.unlink(missing_ok=True)

    print("Türkmopet Muhasebe Programı v1.4.1 kaynak kodu repository köküne çıkarıldı.")
    print("Son adım: git add -A && git commit -m \"feat: add v1.4.1 source\" && git push")


if __name__ == "__main__":
    main()
