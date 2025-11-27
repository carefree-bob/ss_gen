import os

from textnode import TextNode, TextType
from src.util import copy_to_public
script_dir = os.path.dirname(__file__)
public_dir = os.path.abspath(os.path.join(script_dir, '..', 'public'))
static_dir = os.path.abspath(os.path.join(script_dir, '..', 'static'))


def main():
    print(f"copying {public_dir}...")
    print(f"deleting {static_dir}...")
    copy_to_public(static_dir, public_dir)

if __name__ == "__main__":
    # print("hello world")
    main()
