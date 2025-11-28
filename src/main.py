
import sys
import os

from .htmlnode import markdown_to_html_node
from .util import copy_to_public
from .util import extract_title

script_dir = os.path.dirname(__file__)
public_dir = os.path.abspath(os.path.join(script_dir, '..', 'docs'))
static_dir = os.path.abspath(os.path.join(script_dir, '..', 'static'))
content_dir = os.path.abspath(os.path.join(script_dir, '..', 'content'))
root = os.path.abspath(os.path.join(script_dir, '..'))

def generate_page(from_path: str, template_path: str, dest_path: str, base_path="/")->None:
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as fp:
        m_down = fp.read()
    with open (template_path, 'r') as fp:
        templ = fp.read()

    html = markdown_to_html_node(m_down).to_html()
    title = extract_title(m_down)
    templ = templ.replace("{{ Title }}", title)
    templ = templ.replace("{{ Content }}", html)
    templ = templ.replace('href="/', f'href="{base_path}').replace('src="/',  f'src="{base_path}')
    with open(dest_path, 'w') as fp:
        fp.write(templ)

def generate_pages(src, template_path, dest, base_path='/'):
    """take all md templates under src, render them according to template
    and store under parallel directory in dest
    """
    for root_, dirs, files in os.walk(src):
        rel = os.path.relpath(root_, src)
        dst_dir = os.path.join(dest, rel)

        os.makedirs(dst_dir, exist_ok=True)

        for f in files:
            from_path = os.path.join(root_, f)
            dest_path = os.path.join(dst_dir,f).replace(".md", ".html")

            generate_page(from_path, template_path=template_path, dest_path=dest_path, base_path=base_path)



def main():
    if len(sys.argv) == 2:
        base_path = sys.argv[1]
    else:
        base_path = ""

    # empty public and fill with static resources
    print(f"deleting {public_dir}...")
    print(f"copying from {static_dir}...")
    copy_to_public(static_dir, public_dir)

    template_path = os.path.join(root, 'template.html')

    generate_pages(src=content_dir, template_path=template_path, dest=public_dir, base_path=base_path)


if __name__ == "__main__":
    # print("hello world")
    main()
