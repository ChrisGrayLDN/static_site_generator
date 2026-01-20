from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """docstring for TextNode."""

    def __init__(self, text, text_type, url=None):
        super(TextNode, self).__init__()
        self.text, self.text_type, self.url = text, text_type, url

    def __eq__(self, text_node: TextNode, /) -> bool:
        if self.text != text_node.text:
            return False

        if self.text_type != text_node.text_type:
            return False

        if self.url != text_node.url:
            return False

        return True

    def __repr__(self):
        return "TextNode({text}, {text_type}, {url})".format(
            text=self.text, text_type=self.text_type.value, url=self.url
        )


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception
