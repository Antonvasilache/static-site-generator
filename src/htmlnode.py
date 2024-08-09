class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
        
    def to_html(self):
        raise NotImplementedError
    
    
    def props_to_html(self):
        result = ''
        if not self.props == None:
            for key in self.props:
                result = result + f" {key}=\"{self.props[key]}\""
            return result
        else:
            return None 
        
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children)              
            
    
    def __repr__(self):
        class_name = self.__class__.__name__
        if self.children:            
            children = [(child.tag, child.value) for child in self.children]
        else:
            children = ""
            
        if self.tag:
            tag = self.tag + ' '
        else:
            tag = ''
            
        if self.props:
            props = self.props
        else:
            props = ''
            
        return f"{class_name}: {tag}{self.value} {children}{props}"
    
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag=tag, value=value, props=props)
        self.children = None
        
    
    def to_html(self):  
        if not self.tag:
            return self.value  
        
        if self.props:
            props = self.props_to_html()  
        else:
            props = ''   
     
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
        

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None ):
        if children is None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag=tag, children=children, props=props)
        self.value = None
        
        
    def to_html(self):
        if self.tag == None:
            raise ValueError("Object must have a tag")
        
        
        
        if self.children == None:
            raise ValueError("Object must have children")
        
        if self.props:
            props = self.props_to_html()  
        else:
            props = ''  
            
        children = ''
        for child in self.children:
            children += child.to_html()
            
        if self.tag == "":
            return f"{children}"
            
        result = f"<{self.tag}{props}>{children}</{self.tag}>" 
        
        return result
