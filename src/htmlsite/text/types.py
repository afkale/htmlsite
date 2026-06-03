from enum import StrEnum

from htmlsite.html.types import Tag


class TextType(StrEnum):
    plain = "plain"
    bold = "bold"
    italic = "italic"
    code = "code"
    anchor = "anchor"
    image = "image"


def text_type_to_tag(text_type: TextType) -> Tag | None:
    if text_type == TextType.plain:
        return None
    if text_type == TextType.italic:
        return "i"
    if text_type == TextType.bold:
        return "b"
    if text_type == TextType.anchor:
        return "a"
    if text_type == TextType.image:
        return "img"
    if text_type == TextType.code:
        return "code"
