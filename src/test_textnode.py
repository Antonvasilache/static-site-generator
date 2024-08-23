import unittest

from textnode import TextNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        
        
    def test_text_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node.text, node2.text)
        
        
    def test_text_type_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node.text_type, node2.text_type)
        
        
    def test_text_url_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)
        
        
    def test_text_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node2", "bold")
        self.assertNotEqual(node.text, node2.text)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node2)
        
        
    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node.text_type, node2.text_type)
        self.assertNotEqual(node, node2)
        
        
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("This is plain text.", "text")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == ""
        assert html_node.value == "This is plain text."
        
        
    def test_bold(self):
        text_node = TextNode("This text should be bold.", "bold")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "b"
        assert html_node.value == "This text should be bold."
        
        
    def test_italic(self):
        text_node = TextNode("This text should be italic.", "italic")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "i"
        assert html_node.value == "This text should be italic."
        
        
    def test_code(self):
        text_node = TextNode("print('Hello world!')", "code")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "code"
        assert html_node.value == "print('Hello world!')"
        
        
    def test_link(self):
        text_node = TextNode("Click here", "link", "https://example.com")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "a"
        assert html_node.value == "Click here"
        assert html_node.props == {"href":"https://example.com"}
        
        
    def test_image(self):
        text_node = TextNode("", "image", "https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        assert html_node.tag == "img"
        assert html_node.value == ""
        assert html_node.props == {"src":"https://example.com/image.png", "alt":"Placeholder alt text"}
        
    def test_unknown(self):
        text_node = TextNode("This is a text", "unknown")
        with self.assertRaises(ValueError):
            html_node = text_node_to_html_node(text_node)
        
if __name__ == "__main__":
    unittest.main()