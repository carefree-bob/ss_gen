import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_create(self):
        node = TextNode("This is a text node", TextType.BOLD, url="foo")
        assert repr(node).startswith('TextNode(')

    def test_not_equal(self):
        node1 = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is not a text node", TextType.BOLD, url=None)
        assert node1 != node2 

    def test_not_equal2(self):
        node1 = TextNode("This is a text node", TextType.BOLD, url="foo")
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        assert node1 != node2


    def test_not_equal3(self):
        node1 = TextNode("This is a text node", TextType.CODE, url="foo")
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        assert node1 != node2

        







if __name__ == "__main__":
    unittest.main()
