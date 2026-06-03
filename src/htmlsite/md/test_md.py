import unittest

from htmlsite.md import markdown_to_blocks, markdown_to_html_node
from htmlsite.md.types import BlockType, block_to_block_type


class TestMarkdownToHTML(unittest.TestCase):
    maxDiff = None

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestHeading(unittest.TestCase):
    def test_h1(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.heading)

    def test_h3(self):
        self.assertEqual(block_to_block_type("### Section"), BlockType.heading)

    def test_h6(self):
        self.assertEqual(block_to_block_type("###### Deep"), BlockType.heading)

    def test_no_space_still_matches(self):
        # startswith("#") is true even without a space — may or may not be desired
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.heading)


class TestCode(unittest.TestCase):
    def test_basic_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')\n```"), BlockType.code)

    def test_missing_opening_newline(self):
        self.assertNotEqual(block_to_block_type("```print('hi')\n```"), BlockType.code)

    def test_missing_closing_fence(self):
        self.assertNotEqual(block_to_block_type("```\nprint('hi')\n"), BlockType.code)

    def test_multiline_code(self):
        block = "```\ndef foo():\n    return 1\n```"
        self.assertEqual(block_to_block_type(block), BlockType.code)


class TestQuote(unittest.TestCase):
    def test_single_line_quote(self):
        self.assertEqual(block_to_block_type("> Hello"), BlockType.quote)

    def test_multiline_quote(self):
        self.assertEqual(block_to_block_type("> Line one\n> Line two"), BlockType.quote)

    def test_mixed_lines_not_quote(self):
        self.assertNotEqual(
            block_to_block_type("> Line one\nNot a quote"), BlockType.quote
        )


class TestUnorderedList(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(block_to_block_type("- Item"), BlockType.unordered_list)

    def test_multiline(self):
        self.assertEqual(
            block_to_block_type("- Item one\n- Item two\n- Item three"),
            BlockType.unordered_list,
        )

    def test_wrong_marker(self):
        self.assertNotEqual(block_to_block_type("* Item"), BlockType.unordered_list)

    def test_missing_space_after_dash(self):
        self.assertNotEqual(block_to_block_type("-Item"), BlockType.unordered_list)

    def test_mixed_lines_not_ul(self):
        self.assertNotEqual(
            block_to_block_type("- Item one\nNot an item"), BlockType.unordered_list
        )


class TestOrderedList(unittest.TestCase):
    def test_single_item(self):
        self.assertEqual(block_to_block_type("1. First"), BlockType.ordered_list)

    def test_sequential(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)

    def test_non_sequential_is_paragraph(self):
        block = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)

    def test_starting_at_wrong_number(self):
        block = "2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)


class TestParagraph(unittest.TestCase):
    def test_plain_text(self):
        self.assertEqual(block_to_block_type("Just some text."), BlockType.paragraph)

    def test_multiline_plain_text(self):
        self.assertEqual(block_to_block_type("Line one\nLine two"), BlockType.paragraph)

    def test_empty_string(self):
        self.assertEqual(block_to_block_type(""), BlockType.paragraph)


class TestMarkdownToHTMLFinal(unittest.TestCase):
    maxDiff = None

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.quote)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
