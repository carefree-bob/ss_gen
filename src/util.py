import os
import shutil


def clean(dest):
    for root, dirs, files in os.walk(dest, topdown=False):
        if files:
            [os.remove(os.path.join(root, f)) for f in files]
        if dirs:
            [os.remove(os.path.join(root, d)) for d in dirs]
        if root != dest:
            os.remove(root)
    

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
