import re
from typing import Text
from enum import Enum

from src.textnode import TextNode
from src.textnode import TextType as TextType

mdown_link = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
mdown_img = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")

"""
Block Types:
paragraph
heading
code
quote
unordered_list
ordered_list
"""
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


class HTMLNode:
    def __init__(self, tag:str|None=None, value: str|None=None, children:list[HTMLNode]|None=None, props:dict[str,str] | None=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        """
            support href, target, alt, 

        """
        if self.props:
            attr_list = [f'{x}="{y}"' for x,y in self.props.items()]
            return " ".join(attr_list).replace('\n', ' ').strip()
        else:
            return ""

    def __repr__(self):
        return f"(HTMLNODE)(tag: {self.tag}\n\tvalue: {self.value}\n\tchildren: {self.children}\n\tprops: {self.props}\n)"


class LeafNode(HTMLNode):
    def __init__(self, tag:str|None=None, value: str|None=None, children:list[ParentNode | LeafNode | HTMLNode]|None=None, props:dict[str,str] | None=None):
        if children:
            raise ValueError("No kids allowed in Leafland!!")
        if not value:
            raise ValueError("We have values at Leafland!!")
        super().__init__(tag, value, children, props)
    
    def to_html(self):
        if not self.tag:
            return self.value
        if not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag:str|None=None, value: str|None=None, children:list[HTMLNode| ParentNode | LeafNode]|None=None, props:dict[str,str] | None=None):
        if not tag or not children:
            raise ValueError("What kind of parent are you?")
        if value:
            raise ValueError("No values allowed!!!!!!!!")
        super().__init__(tag, value, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag, no html")
        if not self.children:
            raise ValueError("Your kids suck")

        if self.props:
            res = f"<{self.tag} {self.props_to_html()}>"
        else:
            res = f"<{self.tag}>"

        for c in self.children:
            res += c.to_html()

        res += f"</{self.tag}>"
        return res

def text_node_to_html_node(text_node: TextNode)->LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.IMAGE:
            if not text_node.props:
                raise ValueError("missing properties for image type")

            new_props = {x:v for (x, v) in text_node.props.items() if x in ["alt", "src"]} 

            if not new_props:
                raise ValueError("missing attributes for image")

            return LeafNode(tag="a", value=None, props=new_props)
        case _:
            raise ValueError("Illegal type")
            

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type)-> list[TextNode]:
    accum = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            accum.append(node)
            continue

        splits = node.text.split(delimiter)
        for index, text_ in enumerate(splits, start=0):
            if index % 2 == 0:
                accum.append(TextNode(text=text_, text_type=TextType.TEXT))
            else:
                accum.append(TextNode(text=text_, text_type=text_type))
    return accum

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    res = re.findall(mdown_img, text)
    return res


def extract_markdown_links(text: str) ->list[tuple[str, str]]:
    res = re.findall(mdown_link, text)
    return res

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_re(old_nodes, mdown_img, TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_re(old_nodes, mdown_link, TextType.LINKS)

def _split_nodes_re(old_nodes: list[TextNode], pattern: re.Pattern, text_type:TextType) ->list[TextNode]:
    accum = []
    for node in old_nodes:
        old_text = node.text
        old_type = node.text_type
        if old_type is not TextType.TEXT:
            accum.append(node)
            continue

        match_iter = re.finditer(pattern, node.text)

        curr_start = 0
        for match in match_iter:
            curr_end = match.start()
            if curr_start < curr_end:
                # there is space before the match
                accum.append(TextNode(text = old_text[curr_start:curr_end], text_type=old_type))

            # append the match
            accum.append(TextNode(text=match.group(1), url=match.group(2), text_type=text_type))

            # update position
            curr_start = match.end()

        if curr_start < len(old_text)-1:
            accum.append(TextNode(text=old_text[curr_start:], text_type=old_type))
    return accum

def text_to_textnodes(text):
    start_node = TextNode(text=text, text_type=TextType.TEXT)
    out_nodes = split_nodes_delimiter([start_node], delimiter="**", text_type=TextType.BOLD)
    out_nodes = split_nodes_delimiter(out_nodes, delimiter="_", text_type=TextType.ITALIC)
    out_nodes = split_nodes_delimiter(out_nodes, delimiter="`", text_type=TextType.CODE)
    out_nodes = split_nodes_image(out_nodes)
    out_nodes = split_nodes_link(out_nodes)
    return out_nodes


def markdown_to_blocks(markdown: str):
    """Take markdown and split into block: heading, paragraph, list"""
    # we require a blank line
    blocks = markdown.split("\n\n") 
    blocks = [b.strip() for b in blocks if b]
    return blocks

def block_to_block_type(markdown: str) -> BlockType:
    # we should be taking in only a single block
    assert "\n\n" not in markdown
    
    if markdown.startswith("#"):
        return BlockType.HEADING
    elif markdown.startswith('```') and markdown[-3:] == '```':
        return BlockType.CODE
    else:
        splits = [x.strip() for x in markdown.split('\n') if x.strip()]

        if splits[0].startswith('>'):
            for i in range(1, len(splits)):
                if not splits[i].startswith('>'):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
    
        elif splits[0].startswith('- '):
            for i in range(1, len(splits)):
                if not splits[i].startswith('- '):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST

        elif splits[0].startswith("1. "):
            for i in range(1, len(splits)):
                if not splits[i].startswith(f"{i+1}. "):
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def span_to_leaf_nodes(text: str) -> list[LeafNode]:
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(t) for t in nodes]


def block_to_html_nodes(markdown: str) -> list[ParentNode | LeafNode | HTMLNode]:
    b_type = block_to_block_type(markdown)
    match b_type:
        case BlockType.CODE:
            l = LeafNode(tag="code", value=markdown[3:-3].lstrip())
            r = ParentNode(tag="pre", value=None, children=[l])
            return [r]

        case BlockType.HEADING:
            lines = [x.strip() for x in markdown.split('\n') if x.strip()]
            match_ = re.findall(r'^(#+)', lines[0])
            heading_num = len(match_[0])
            hn = min(6, heading_num)
            accum = []
            for x in markdown.split('\n'):
                if not x.strip():
                    continue
                l=span_to_leaf_nodes(x[hn:])
                p=ParentNode(tag=f'h{heading_num}', children=l)
                accum.append(p)
            return accum

        case BlockType.UNORDERED_LIST:
            lines = [x.strip() for x in markdown.split('\n') if x.strip()]
            accum = []

            for line in lines:
                p = ParentNode(tag='li', children=span_to_leaf_nodes(line[2:]))
                accum.append(p)

            return [ParentNode(tag='ul', children=accum)]
        
        case BlockType.ORDERED_LIST:
            lines = [x for x in markdown.split('\n') if x.strip()]
            accum = []
            for line in lines:
                m = re.findall(r'^([0-9])\.', line)
                accum.append(ParentNode(tag='li', children=span_to_leaf_nodes(line[m[0].start:])))

            return [ParentNode(tag='ol', children=accum)]

        case BlockType.QUOTE:
            lines = [x for x in markdown.split('\n') if x.strip()]
            accum = []
            for line in lines:
                accum.append(ParentNode(tag='p', children=span_to_leaf_nodes(line[1:])))

            return [ParentNode(tag='blockquote', children=accum)]

        case _:
            return [ParentNode(tag='p', children=span_to_leaf_nodes(clean_markdown_whitespace(markdown)))]

def clean_markdown_whitespace(markdown: str) -> str:
    return re.sub(r'\s+', ' ', markdown).strip()

def markdown_to_html_node(text)->HTMLNode:
    blocks = markdown_to_blocks(text)
    accum = []
    for b in blocks:
        accum.extend(block_to_html_nodes(b))
    return ParentNode(tag='div', children=accum)


