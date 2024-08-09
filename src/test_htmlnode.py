import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_only_tag(self):
        node = HTMLNode("p")
        assert node.value == None
        assert node.children == None
        assert node.props == None
        
        
    def test_only_tag_value(self):
        node = HTMLNode("p", "This is a paragraph")
        assert node.children == None
        assert node.props == None
    
    def test_props_type(self):
        node = HTMLNode("p", "This is a paragraph", None, {"href": "https://boot.dev"})
        assert isinstance(node.props, dict)
        
        
    def test_props_to_html_no_attributes(self):
        node = HTMLNode(tag="a")
        assert node.props_to_html() == None
        
    
    def test_props_to_html_one_attribute(self):
        node = HTMLNode(tag="a", props={"href": "https://google.com"})        
        assert node.props_to_html() == ' href="https://google.com"'
        
        
    def test_props_to_html_with_multiple_attributes(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        assert node.props_to_html() == expected
    
    
    def test_repr(self):
        node = HTMLNode(
            "p", 
            "This is a paragraph", 
            [
                HTMLNode("span", "This is a span"), 
                HTMLNode("span", "This is another span")], 
            {"href": "https://boot.dev"})
        children = [(child.tag, child.value) for child in node.children]
        expected = f"HTMLNode: {node.tag} {node.value} {children}{node.props}"
        assert node.__repr__() == expected
            
        

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        assert node.to_html() == expected
        
    
    def test_to_html_attributes(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        assert node.to_html() == expected
        
        
    def test_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)
            
            
    def test_no_tag(self):
        node = LeafNode(value="This is a node without a tag")
        expected = "This is a node without a tag"
        assert node.to_html() == expected
        
    
    def test_complex(self):
        node = LeafNode(
            "p", 
            "This is a paragraph",             
            {
                "href": "https://www.google.com", 
                "target": "_blank", 
                "class" : "btn btn-primary"
                }
            )
        
        expected = '<p href="https://www.google.com" target="_blank" class="btn btn-primary">This is a paragraph</p>'
       
        assert node.to_html() == expected
        
        
class TestParentNode(unittest.TestCase):
    def test_no_children(self):         
        with self.assertRaises(ValueError):
            node = ParentNode("p")  
            
            
    def test_to_html_no_tag(self):
        node = ParentNode(tag=None, children=["p"]) 
        with self.assertRaises(ValueError):
            node.to_html()
    
    
    def test_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        
        assert node.to_html() == expected
    
    
    def test_nested_nodes(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "Top level text"),
                ParentNode(
                    "section",
                    [
                        LeafNode("p", "Nested text in section"),
                        ParentNode(
                            "article",
                            [
                                LeafNode("h1", "Deeply nested heading"),
                                LeafNode("p", "Another nested paragraph")
                            ],
                        ),
                    ],
                ),
                LeafNode("footer", "Bottom level text"),
            ],
        )  
        
        expected = "<div><span>Top level text</span><section><p>Nested text in section</p><article><h1>Deeply nested heading</h1><p>Another nested paragraph</p></article></section><footer>Bottom level text</footer></div>" 
        
        assert node.to_html() == expected      
        
        
    def test_nested_nodes_no_tag(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "Top level text"),
                ParentNode(
                    "section",
                    [
                        LeafNode("p", "Nested text in section"),
                        LeafNode(tag=None, value="Nested text with no paragraph"),
                        ParentNode(
                            "article",
                            [
                                LeafNode("h1", "Deeply nested heading"),
                                LeafNode("p", "Another nested paragraph")
                            ],
                        ),
                    ],
                ),
                LeafNode("footer", "Bottom level text"),
            ],
        )  
        
        expected = "<div><span>Top level text</span><section><p>Nested text in section</p>Nested text with no paragraph<article><h1>Deeply nested heading</h1><p>Another nested paragraph</p></article></section><footer>Bottom level text</footer></div>" 
        
        assert node.to_html() == expected   
        
        
    def test_special_character_handling(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "<Special> & characters!"),
                LeafNode("b", "Bold & beautiful"),
            ],
        )       
        expected = "<p><Special> & characters!<b>Bold & beautiful</b></p>"
        assert node.to_html() == expected
        
        
    def test_props_rendering(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", "Text with props")
            ]
        )
        node.props = {"class" : "highlight"}
        expected = '<div class="highlight"><span>Text with props</span></div>'
        assert node.to_html() == expected
        
        
    def test_empty_test_nodes(self):
        node = ParentNode(
            "div",
            [
                LeafNode("span", ""),
                LeafNode("p", "Non-empty text"),
            ],
        )
        expected = "<div><span></span><p>Non-empty text</p></div>"
        assert node.to_html() == expected
                        
            
if __name__ == "__main__":
    unittest.main()