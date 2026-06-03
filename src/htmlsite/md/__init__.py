from htmlsite.html.node import HTMLNode, LeafNode, ParentNode
from htmlsite.md.types import block_to_block_type_value, block_type_to_tag
from htmlsite.text.node import text_node_to_html_node, text_to_textnodes


def markdown_to_blocks(md: str) -> list[str]:
    return [b for block in md.strip().split("\n\n") if (b := block.strip())]


def markdown_to_html_node(md: str) -> HTMLNode:
    blocks = markdown_to_blocks(md)
    children = [__block_to_children(block) for block in blocks]
    return ParentNode(tag="div", children=children)


def __block_to_children(block: str) -> HTMLNode:
    block_type, value = block_to_block_type_value(block)
    tag = block_type_to_tag(block_type, block)

    if tag in ("ol", "ul"):
        return ParentNode(
            tag,
            [
                ParentNode(
                    "li", list(map(text_node_to_html_node, text_to_textnodes(text)))
                )
                for text in value.split("\n")
            ],
        )
    if tag == "code":
        return ParentNode("pre", children=[LeafNode(tag, value)])
    children = list(map(text_node_to_html_node, text_to_textnodes(value)))
    return ParentNode(tag, children)
