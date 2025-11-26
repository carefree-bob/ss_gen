import unittest

from htmlnode import HTMLNode, LeafNode

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





if __name__ == "__main__":
    unittest.main()

