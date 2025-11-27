import unittest


from htmlnode import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from htmlnode import text_node_to_html_node as t2h
from htmlnode import extract_markdown_images, extract_markdown_links, block_to_html
from htmlnode import split_nodes_delimiter as split_delim
from htmlnode import split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType



class TestNode(unittest.TestCase):
    def test_repr(self):
        a = HTMLNode(children=None, props={"href": "foo"}, tag="a", value="click me!")
        s = repr(a)
        print(s)
        assert s.startswith("(HTMLNODE)")

    def test_props_to_html(self):
        props = {"href":"foo"}
        a = HTMLNode(children=None, props=props, tag="a", value="click me!")
        s = a.props_to_html()
        self.assertEqual(s,'href="foo"')

    def test_constructor(self):
        a = HTMLNode()
        assert a.children is None

class TestLeaf(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        props = {"href":"foo"}
        node = LeafNode(tag="a", value="Click me now for great fun", props=props)
        self.assertEqual(node.to_html(),'<a href="foo">Click me now for great fun</a>')

    def test_constructor_error(self):
        self.assertRaises(ValueError, LeafNode, tag="a")
    
    def test_raw_render(self):
        node = LeafNode(None, "hi")
        self.assertEqual(node.to_html(), "hi")


class TestParent(unittest.TestCase):
    def test_render(self):
        children = [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        node = ParentNode("p", children=children)
        s = node.to_html()
        self.assertEqual(s, '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", children=[grandchild_node])
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

class GeneralTest(unittest.TestCase):
    def test_conv_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = t2h(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_delim([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_node_split(self):
        input = ("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)" +
             " and a [link](https://boot.dev)")

        out = text_to_textnodes(input)
        print("===================")
        print("\n".join([repr(x) for x in out]))
        print("\n==================")

        self.assertCountEqual(out, [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type_heading(self):
        mkdn = "# muh heading"
        assert block_to_block_type(mkdn) is BlockType.HEADING

    def test_block_type_code(self):
        m = "```muh code```"
        assert block_to_block_type(m) is BlockType.CODE

    def test_block_type_ulist(self):
        m = "- foo\n- bar"
        assert block_to_block_type(m) is BlockType.UNORDERED_LIST

    def test_block_type_olist(self):
        m = "1. muh\n2. list"
        print(f"****{block_to_block_type(m)}")
        assert block_to_block_type(m) is BlockType.ORDERED_LIST

    def test_block_type_vanilla(self):
        m = "muh vanilla"
        assert block_to_block_type(m) is BlockType.PARAGRAPH

    def test_block_to_html_h1(self):
        m1 = "- listen _to_ this\n- or **not**!!"
        res = block_to_html(m1)
        print(res)
        assert True





if __name__ == "__main__":
    unittest.main()

