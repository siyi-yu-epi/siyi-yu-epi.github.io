from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re

import pymupdf as fitz
from PIL import Image


PHONE_LABEL_RE = re.compile(r"\bphone\s*:", re.IGNORECASE)
PROFILE_CROP = (560, 900, 3088, 4060)
PROFILE_SIZE = (800, 1000)
PROFILE_MAX_BYTES = 500_000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_profile(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as original:
        if original.size != (3648, 5472):
            raise ValueError(f"Unexpected profile dimensions: {original.size}")
        derivative = (
            original.convert("RGB")
            .crop(PROFILE_CROP)
            .resize(PROFILE_SIZE, Image.Resampling.LANCZOS)
        )
        for quality in (88, 84, 80):
            derivative.save(
                target,
                format="JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
            )
            if target.stat().st_size <= PROFILE_MAX_BYTES:
                break
        else:
            raise ValueError(f"Profile derivative exceeds {PROFILE_MAX_BYTES} bytes")


def phone_row(page: fitz.Page) -> fitz.Rect:
    matches = [
        word
        for word in page.get_text("words")
        if str(word[4]).strip().lower() == "phone:"
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one Phone: label, found {len(matches)}")
    word = matches[0]
    return fitz.Rect(word[0] - 2, word[1] - 2, page.rect.x1 - 36, word[3] + 2)


def prepare_cv(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".tmp.pdf")
    if temporary.exists():
        temporary.unlink()

    with fitz.open(source) as document:
        if document.page_count != 2:
            raise ValueError(f"Expected a two-page CV, found {document.page_count} pages")
        page = document[0]
        page.add_redact_annot(phone_row(page), fill=(1, 1, 1))
        page.apply_redactions()
        document.save(temporary, garbage=4, deflate=True, clean=True)

    temporary.replace(target)
    with fitz.open(target) as public_document:
        text = "\n".join(page.get_text() for page in public_document)
        if PHONE_LABEL_RE.search(text):
            raise ValueError("Phone label remains in extractable public CV text")
        if public_document.page_count != 2:
            raise ValueError("Public CV page count changed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-source", required=True, type=Path)
    parser.add_argument("--cv-source", required=True, type=Path)
    parser.add_argument(
        "--profile-target",
        type=Path,
        default=Path("assets/img/profile.jpg"),
    )
    parser.add_argument(
        "--cv-target",
        type=Path,
        default=Path("assets/files/Siyi-Yu-CV.pdf"),
    )
    args = parser.parse_args()

    before = {
        args.profile_source: sha256(args.profile_source),
        args.cv_source: sha256(args.cv_source),
    }
    prepare_profile(args.profile_source, args.profile_target)
    prepare_cv(args.cv_source, args.cv_target)
    after = {path: sha256(path) for path in before}
    if before != after:
        raise RuntimeError("A source asset changed during derivative creation")


if __name__ == "__main__":
    main()
