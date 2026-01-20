from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(markdown_block: str):
    lines = markdown_block.split("\n")

    if markdown_block.startswith("# "):
        return BlockType.HEADING

    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE

    if markdown_block.startswith("> "):
        return BlockType.QUOTE

    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1

        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for block in split_markdown:
        if block == "":
            continue
        blocks.append(block.strip())

    return blocks


def text_to_children(text):
    children = text_to_textnodes(text)
    nodes = []
    for child in children:
        html_node = text_node_to_html_node(child)
        nodes.append(html_node)

    return nodes


def paragraph_to_html_node(block):
    inline_children = text_to_children(" ".join(block.split("\n")))
    return ParentNode(tag="p", children=inline_children)


def heading_to_html_node(block):
    level = block.split(" ")[0].count("#")
    trimmed_string = block[level:].strip()
    inline_children = text_to_children(trimmed_string)
    return ParentNode(tag=f"h{level}", children=inline_children)


def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.startswith("> "):
            cleaned_lines.append(line[2:])
        elif line.startswith(">"):
            cleaned_lines.append(line[1:].lstrip())
        else:
            cleaned_lines.append(line)
    cleaned_string = "\n".join(cleaned_lines)
    inline_children = text_to_children(cleaned_string)
    return ParentNode(tag="blockquote", children=inline_children)


def code_to_html_node(block):
    lines = block.split("\n")
    inner_lines = lines[1:-1]
    raw_code = "\n".join(inner_lines) + "\n"
    text_node = TextNode(raw_code, TextType.CODE)
    code_node = text_node_to_html_node(text_node)
    pre_node = ParentNode(tag="pre", children=[code_node])
    return pre_node


def ulist_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        if line.startswith("- "):
            content = line[2:]
        elif line.startswith("-"):
            content = line[1:]
        else:
            content = line
        inline_children = text_to_children(content)
        li_nodes.append(HTMLNode("li", children=inline_children))
    return ParentNode(tag="ul", children=li_nodes)


def olist_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        if not line.strip():
            continue
        dot_index = line.find(".")
        if dot_index != -1:
            content = line[dot_index + 1 :].lstrip()
        else:
            content = line
        inline_children = text_to_children(content)
        li_nodes.append(HTMLNode("li", children=inline_children))
    return ParentNode(tag="ol", children=li_nodes)


def block_to_html_node(block: str):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)

    raise ValueError("Invalid block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode(tag="div", children=children)
