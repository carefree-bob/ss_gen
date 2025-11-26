from textnode import TextNode, TextType



def main():
    node = TextNode("hello from the node", text_type=TextType.TEXT, url="http://www.neverssl.com")
    print(node)


if __name__ == "__main__":
    # print("hello world")
    main()
