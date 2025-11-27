import os

from .util import copy_to_public
from .htmlnode import markdown_to_html_node
from .util import extract_title

script_dir = os.path.dirname(__file__)
public_dir = os.path.abspath(os.path.join(script_dir, '..', 'public'))
static_dir = os.path.abspath(os.path.join(script_dir, '..', 'static'))
content_dir = os.path.abspath(os.path.join(script_dir, '..', 'content'))
root = os.path.abspath(os.path.join(script_dir, '..'))

def generate_page(from_path: str, template_path: str, dest_path: str)->None:
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as fp:
        m_down = fp.read()
    with open (template_path, 'r') as fp:
        templ = fp.read()

    html = markdown_to_html_node(m_down).to_html()
    title = extract_title(m_down)
    templ = templ.replace("{{ Title }}", title)
    templ = templ.replace("{{ Content }}", html)

    with open(dest_path, 'w') as fp:
        fp.write(templ)








def main():
    print(f"copying {public_dir}...")
    print(f"deleting {static_dir}...")
    copy_to_public(static_dir, public_dir)

    content_path = os.path.join(content_dir, 'index.md')
    template_path = os.path.join(root, 'template.html')
    index_path = os.path.join(public_dir, 'index.html')

    generate_page(content_path, template_path=template_path, dest_path=index_path)


if __name__ == "__main__":
    # print("hello world")
    main()
