from dataclasses import dataclass

from htmlsite.html.node import LeafNode
from htmlsite.text import extract_markdown_images, extract_markdown_links
from htmlsite.text.types import TextType, text_type_to_tag


@dataclass
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    tag = text_type_to_tag(text_node.text_type)

    if text_node.text_type is TextType.image:
        return LeafNode(
            tag=tag, value="", props={"src": text_node.url, "alt": text_node.text}
        )
    if text_node.text_type is TextType.anchor:
        return LeafNode(tag=tag, value=text_node.text, props={"href": text_node.url})
    return LeafNode(tag=tag, value=text_node.text.replace("\n", " "))


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.plain:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Delimiter {delimiter} must have matching delimiters.")

        new_texts = old_node.text.split(delimiter)

        node_new_nodes = []
        text = old_node.text
        for new_text in new_texts:
            if not new_text:
                continue

            if (delimited_text := f"{delimiter}{new_text}{delimiter}") in text:
                node_new_nodes.append(TextNode(new_text, text_type))
                text = text.lstrip(delimited_text)
            else:
                node_new_nodes.append(TextNode(new_text, TextType.plain))
                text = text.lstrip(new_text)
        new_nodes.extend(node_new_nodes)

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.plain:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for alt, url in extract_markdown_images(old_node.text):
            new_node_text, text = text.split(f"![{alt}]({url})", 1)
            if new_node_text:
                new_nodes.append(TextNode(new_node_text, TextType.plain))

            new_nodes.append(TextNode(alt, TextType.image, url))

        if text:
            new_nodes.append(TextNode(text, TextType.plain))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.plain:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for alt, link in extract_markdown_links(old_node.text):
            new_node_text, text = text.split(f"[{alt}]({link})", 1)
            if new_node_text:
                new_nodes.append(TextNode(new_node_text, TextType.plain))
            new_nodes.append(TextNode(alt, TextType.anchor, link))

        if text:
            new_nodes.append(TextNode(text, TextType.plain))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    result = [TextNode(text, TextType.plain)]
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    result = split_nodes_delimiter(result, "**", TextType.bold)
    result = split_nodes_delimiter(result, "_", TextType.italic)
    result = split_nodes_delimiter(result, "`", TextType.code)
    return result
