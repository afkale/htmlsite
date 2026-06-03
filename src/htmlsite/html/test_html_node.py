import unittest

from htmlsite.html.node import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_format_none(self):
        node = HTMLNode(
            tag="a", value="Best coding web ever!", children=None, props=None
        )
        expected = ""
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_props_format(self):
        node = HTMLNode(
            tag="a",
            value="Best coding web ever!",
            children=None,
            props={"src": "https://boot.dev/"},
        )
        expected = 'src="https://boot.dev/"'
        result = node.props_to_html()
        self.assertEqual(result, expected)

    def test_props_format_multi_key_value(self):
        node = HTMLNode(
            tag="a",
            value="Best coding web ever!",
            children=None,
            props={"src": "https://boot.dev/", "target": "_blank"},
        )
        expected = 'src="https://boot.dev/" target="_blank"'
        result = node.props_to_html()
        self.assertEqual(result, expected)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Hello, world!", {"src": "https://helloworld.dev/"})
        self.assertEqual(
            node.to_html(), '<a src="https://helloworld.dev/">Hello, world!</a>'
        )

    def test_leaf_prohibited_children(self):
        with self.assertRaises(TypeError):
            LeafNode("a", "Hello, world!", children=None)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_mandatory_params(self):
        with self.assertRaises(TypeError):
            # missing tag and children
            ParentNode()

        with self.assertRaises(TypeError):
            # missing children
            ParentNode("html")

        parent_node = ParentNode("html", children=[])
        self.assertEqual(parent_node.to_html(), "<html></html>")


if __name__ == "__main__":
    unittest.main()
