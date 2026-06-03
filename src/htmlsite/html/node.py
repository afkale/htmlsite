from dataclasses import dataclass, field
from typing import Self

from htmlsite.html.types import Tag


@dataclass
class HTMLNode:
    tag: Tag | None
    value: str | None
    children: list[Self] | None
    props: dict[str, str] | None = field(default_factory=dict)

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])


@dataclass
class LeafNode(HTMLNode):
    children: None = field(compare=False, init=False, hash=False, repr=False)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if not self.tag:
            return self.value

        html_props = self.props_to_html()
        props = f" {html_props}" if html_props else html_props

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


@dataclass
class ParentNode(HTMLNode):
    tag: Tag
    children: list[HTMLNode]
    value: None = field(compare=False, init=False, hash=False, repr=False)

    def to_html(self):

        children_html = ""
        for child in self.children:
            children_html += f"{child.to_html()}"

        return f"<{self.tag}>{children_html}</{self.tag}>"
