from enum import StrEnum
import re

from htmlsite.html.types import Tag


class BlockType(StrEnum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_type_to_tag(block_type: BlockType, value: str) -> Tag | None:
    if block_type == BlockType.paragraph:
        return "p"
    if block_type == BlockType.heading:
        num = min(max(len(re.search(r"^(#+)", value).group(1)), 1), 6)
        return f"h{num}"
    if block_type == BlockType.code:
        return "code"
    if block_type == BlockType.quote:
        return "blockquote"
    if block_type == BlockType.unordered_list:
        return "ul"
    if block_type == BlockType.ordered_list:
        return "ol"
    return None


def block_to_block_type(block: str) -> BlockType:
    if re.search(r"^#{1,6}", block):
        return BlockType.heading
    if re.search(r"^```\n.*\n```", block, flags=re.MULTILINE | re.DOTALL):
        return BlockType.code
    if not re.search(r"^(?!>)", block, flags=re.MULTILINE):
        return BlockType.quote
    if not re.search(r"^(?!\- )", block, flags=re.MULTILINE):
        return BlockType.unordered_list
    if not re.search(r"^(?!(\d)\. )", block, flags=re.MULTILINE):
        numbers = re.findall(r"(\d)\. ", block, flags=re.MULTILINE)
        if all(int(n) == i for i, n in enumerate(numbers, 1)):
            return BlockType.ordered_list
    return BlockType.paragraph


def block_to_block_type_value(block: str) -> tuple[BlockType, str]:
    block_type = block_to_block_type(block)

    if block_type == BlockType.heading:
        value = re.search(r"^#{1,6} (.*)", block).group(1)
    if block_type == BlockType.code:
        value = re.search(
            r"^```\n(.*\n)```", block, flags=re.MULTILINE | re.DOTALL
        ).group(1)
    if block_type == BlockType.quote:
        value = re.compile(r"^> (.*)|>$", re.MULTILINE).sub("\\1", block)
    if block_type == BlockType.unordered_list:
        value = re.compile(r"^- (.*)|-$", re.MULTILINE).sub("\\1", block)
    if block_type == BlockType.ordered_list:
        value = re.compile(r"^\d\. (.*)|\d\.$", re.MULTILINE).sub("\\1", block)
    if block_type == BlockType.paragraph:
        value = block
    return block_type, value
