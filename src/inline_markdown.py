from textnode import TextNode, TextType

import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0 and len(split_text) > 1:
                raise Exception("Invalid markdown provided")
            for i in range(0, len(split_text)):
                if not split_text[i]:
                    continue
                else:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            images = extract_markdown_images(text)
            for alt, url in images:
                image_markdown = f"![{alt}]({url})"
                before, after = text.split(image_markdown, 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                text = after
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            links = extract_markdown_links(text)
            for descriptor, url in links:
                link_markdown = f"[{descriptor}]({url})"
                before, after = text.split(link_markdown, 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(descriptor, TextType.LINK, url))
                text = after
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    start_list = [TextNode(text, TextType.TEXT)]
    after_bold = split_nodes_delimiter(start_list, "**", TextType.BOLD)
    after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
    after_code = split_nodes_delimiter(after_italic, "`", TextType.CODE)
    after_images = split_nodes_image(after_code)
    after_links = split_nodes_link(after_images)
    return after_links
