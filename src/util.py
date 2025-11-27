import os
import shutil


def clean(dest):
    for root, dirs, files in os.walk(dest, topdown=False):
        if files:
            [os.remove(os.path.join(root, f)) for f in files if os.path.exists(
                os.path.join(root, f))
            ]
        if dirs:
            [os.rmdir(os.path.join(root, d)) for d in dirs if os.path.exists(
                os.path.join(root, d)
            )]


def copy_to_public(src, dest):
    clean(dest)

    for root, dirs, files in os.walk(src):
        # compute destination path
        rel = os.path.relpath(root, src)
        dst_dir = os.path.join(dest, rel)

        os.makedirs(dst_dir, exist_ok=True)

        for f in files:
            shutil.copy2(os.path.join(root, f),
                         os.path.join(dst_dir, f))


def extract_title(markdown: str) -> str:
    lines = [l.strip() for l in markdown.split("\n") if l.strip()]
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Could not extract title")

