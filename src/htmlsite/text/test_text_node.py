import unittest

from htmlsite.text import extract_markdown_images, extract_markdown_links
from htmlsite.text.node import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    maxDiff = None

    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.plain)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.plain)
        node2 = TextNode("This is a text node", TextType.bold, "https://hola.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.plain)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_image_url(self):
        node = TextNode(
            "This is an image node",
            TextType.image,
            url="https://thispersondoesnotexist.com/",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": node.text})

    def test_text_to_text_nodes(self):

        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.plain),
                TextNode("text", TextType.bold),
                TextNode(" with an ", TextType.plain),
                TextNode("italic", TextType.italic),
                TextNode(" word and a ", TextType.plain),
                TextNode("code block", TextType.code),
                TextNode(" and an ", TextType.plain),
                TextNode(
                    "obi wan image", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.plain),
                TextNode("link", TextType.anchor, "https://boot.dev"),
            ],
        )


class TestSplitNodes(unittest.TestCase):
    maxDiff = None

    def test_split_nodes_one_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.plain),
                TextNode("code block", TextType.code),
                TextNode(" word", TextType.plain),
            ],
        )

    def test_split_nodes_multiple_delimiters(self):
        node = TextNode(
            "This is text with a `code block` word and another `code block`",
            TextType.plain,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.plain),
                TextNode("code block", TextType.code),
                TextNode(" word and another ", TextType.plain),
                TextNode("code block", TextType.code),
            ],
        )

    def test_split_nodes(self):
        node = TextNode("This is **text** with **bold** parts.", TextType.plain)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.plain),
                TextNode("text", TextType.bold),
                TextNode(" with ", TextType.plain),
                TextNode("bold", TextType.bold),
                TextNode(" parts.", TextType.plain),
            ],
        )

    def test_split_multiple_nodes(self):
        node = [TextNode("This is **text** with **bold** parts.", TextType.plain)] * 2
        new_nodes = split_nodes_delimiter(node, "**", TextType.bold)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.plain),
                TextNode("text", TextType.bold),
                TextNode(" with ", TextType.plain),
                TextNode("bold", TextType.bold),
                TextNode(" parts.", TextType.plain),
                TextNode("This is ", TextType.plain),
                TextNode("text", TextType.bold),
                TextNode(" with ", TextType.plain),
                TextNode("bold", TextType.bold),
                TextNode(" parts.", TextType.plain),
            ],
        )

    def test_split_nodes_ignore_not_plain_ones(self):
        node = [
            TextNode("This is **text** with **bold** parts.", TextType.plain),
            TextNode("i'm bold :)", TextType.bold),
        ]
        new_nodes = split_nodes_delimiter(node, "**", TextType.bold)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.plain),
                TextNode("text", TextType.bold),
                TextNode(" with ", TextType.plain),
                TextNode("bold", TextType.bold),
                TextNode(" parts.", TextType.plain),
                TextNode("i'm bold :)", TextType.bold),
            ],
        )

    def test_split_wrong_delimiters(self):
        node = [TextNode("This is a bad **text.", TextType.plain)]

        with self.assertRaises(ValueError):
            split_nodes_delimiter(node, "**", TextType.bold)

    def test_split_no_delimiters(self):
        node = [TextNode("This is a bad text.", TextType.plain)]
        new_nodes = split_nodes_delimiter(node, "**", TextType.bold)

        self.assertEqual(node, new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.plain,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.plain),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.plain),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_image_at_the_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.plain,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.plain),
                TextNode(
                    "second image", TextType.image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.plain,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.plain),
                TextNode("link", TextType.anchor, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.plain),
                TextNode(
                    "second link", TextType.anchor, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_with_link_at_the_start(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.plain,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("link", TextType.anchor, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.plain),
                TextNode(
                    "second link", TextType.anchor, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestExtractMethods(unittest.TestCase):
    maxDiff = None

    def test_extract_markdown_images(self):
        result = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, result)

    def test_extract_markdown_multiple_images(self):
        result = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)" * 7
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")] * 7
        self.assertListEqual(expected, result)

    def test_extract_markdown_images_nothing(self):
        result = extract_markdown_images(
            "This is text with an image](https://i.imgur.com/zjjcJKZ.png)" * 7
        )
        expected = []
        self.assertListEqual(expected, result)

    def test_extract_markdown_links(self):
        result = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("link", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, result)

    def test_extract_markdown_multiple_links(self):
        result = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)" * 7
        )
        expected = [("link", "https://i.imgur.com/zjjcJKZ.png")] * 7
        self.assertListEqual(expected, result)

    def test_extract_markdown_links_with_images_being_ignored(self):
        result = extract_markdown_links(
            "This is text with an ![im an ignored image :(](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = []
        self.assertListEqual(expected, result)

    def test_extract_markdown_links_nothing(self):
        result = extract_markdown_images(
            "This is text with an image](https://i.imgur.com/zjjcJKZ.png)" * 7
        )
        expected = []
        self.assertListEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
