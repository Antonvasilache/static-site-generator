from htmlnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
        
    def __eq__(text_node_1, text_node_2):        
        if text_node_1.text != text_node_2.text:
            return False
        if text_node_1.text_type != text_node_2.text_type:
            return False
        if text_node_1.url != text_node_2.url:
            return False
        
        return True
    
     
    def __repr__(self):
        if self.url:
            url = ", " + self.url
        else:
            url = ''
        return f"TextNode({self.text}, {self.text_type}{url})"
     
        
def text_node_to_html_node(text_node):    
    match text_node.text_type:
        case "text":
            return LeafNode(tag="", value=text_node.text)
        
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        
        case "link":
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        
        case "image":
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": "Placeholder alt text"})
        
        case _:
            raise ValueError("Unknown text type")         