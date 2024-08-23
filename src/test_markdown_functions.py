import unittest

from textnode import TextNode
from htmlnode import ParentNode
from markdown_functions import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block_middle(self):
        node = TextNode("This is a text with a `code block` word", "text")
        expected = [TextNode("This is a text with a ", "text"), TextNode("code block", "code"), TextNode(" word", "text")]
        assert split_nodes_delimiter([node], "`", "code") == expected
        
    
    def test_code_block_end(self):
        node = TextNode("This is a text with a `code block at the end`", "text")
        expected = [TextNode("This is a text with a ", "text"), TextNode("code block at the end", "code")]
        assert split_nodes_delimiter([node], "`", "code") == expected
        
        
    def test_code_block_middle_and_end(self):
        node = TextNode("This is a text with a `code block` and then another `code block at the end`", "text")
        expected = [TextNode("This is a text with a ", "text"), TextNode("code block", "code"), TextNode(" and then another ", "text"), TextNode("code block at the end", "code")]
        assert split_nodes_delimiter([node], "`", "code") == expected
        
        
    def test_code_block_beginning(self):
        node = TextNode("`Code in the beginning` and then text", "text")
        expected = [TextNode("Code in the beginning", "code"), TextNode(" and then text", "text")]
        assert split_nodes_delimiter([node], "`", "code") == expected
        
        
    def test_inside_code_block(self):
        node = TextNode("`This is a text entirely inside a code block`", "text")
        expected = [TextNode("This is a text entirely inside a code block", "code")]
        assert split_nodes_delimiter([node], "`", "code") == expected
        
        
    def test_no_code_blocks(self):
        node = TextNode("This is a text with no code blocks", "text")
        expected = [TextNode("This is a text with no code blocks", "text")]
        assert split_nodes_delimiter([node], "`", "code") == expected
        
        
    def test_unmatched_delimiter(self):
        node = TextNode("This is text with an unmatched `code block", "text")
        expected = [TextNode("This is text with an unmatched `code block", "text")]
        assert split_nodes_delimiter([node], "`", "code") == expected
            
            
class TestExtractMarkdownLinksImages(unittest.TestCase):
    def test_single_image_link(self):
        assert extract_markdown_images("![sample](https://sample.com/image.jpg)") == [("sample", "https://sample.com/image.jpg")]
        assert extract_markdown_links("[boot.dev](https://www.boot.dev)") == [("boot.dev", "https://www.boot.dev")]
        
        
    def test_multiple_images_links(self):
        assert extract_markdown_images("![img1](https://img1.com) and ![img2](https://img2.com)") == [("img1", "https://img1.com"), ("img2", "https://img2.com")]
        assert extract_markdown_links("[link1](https://link1.com) and [link2](https://link2.com)") == [("link1", "https://link1.com"), ("link2", "https://link2.com")]
        
        
    def test_no_matches(self):
        assert extract_markdown_images("No images here!") == []
        assert extract_markdown_links("No links here!") == []
        
        
    def test_mixed_content(self):
        text = "This is a ![image](https://img.com) and a [link](https://link.com)"
        assert extract_markdown_images(text) == [("image", "https://img.com")]
        assert extract_markdown_links(text) == [("link", "https://link.com")]
        
        
    def test_edge_cases(self):
        assert extract_markdown_images("![img](invalid)") == [("img", "invalid")]
        assert extract_markdown_links("[text](more_invalid)") == [("text", "more_invalid")]

        text = "![ ](https://emptyalt.com)"
        assert extract_markdown_images(text) == [(" ", "https://emptyalt.com")]

        text = "[ ](https://emptyanchor.com)"
        assert extract_markdown_links(text) == [(" ", "https://emptyanchor.com")]
        
        text = "![empty](https://emptyimage.com)"
        assert extract_markdown_images(text) == [("empty", "https://emptyimage.com")]

        text = "[empty anchor text](https://emptyanchor.com)"
        assert extract_markdown_links(text) == [("empty anchor text", "https://emptyanchor.com")]
        
        
class TestSplitNodesLinksImages(unittest.TestCase):
    def test_link_nodes(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", "text")
        expected = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode("to youtube", "link", "https://www.youtube.com/@bootdotdev")
        ]
        result = split_nodes_link([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_multiple_links_no_text(self):
        node = TextNode("[first link](https://example1.com)[second link](https://example2.com)", "text")
        expected = [
            TextNode("first link", "link", "https://example1.com"),
            TextNode("second link", "link", "https://example2.com")
        ]
        result = split_nodes_link([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_text_no_links(self):
        node = TextNode("This is a simple text without any links.", "text")
        expected = [TextNode("This is a simple text without any links.", "text")]
        result = split_nodes_link([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_text_empty_link(self):
        node = TextNode("This text has an empty link []()", "text")
        expected = [
            TextNode("This text has an empty link ", "text") 
        ]
        result = split_nodes_link([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_mixed_text_and_links(self):
        node = TextNode("Some text [first link](https://example1.com) more text [second link](https://example2.com) end text.", "text")
        expected = [
            TextNode("Some text ", "text"),
            TextNode("first link", "link", "https://example1.com"),
            TextNode(" more text ", "text"),
            TextNode("second link", "link", "https://example2.com"),
            TextNode(" end text.", "text")
        ]
        result = split_nodes_link([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_link_beginning(self):
        node = TextNode("[intro link](https://intro.com) starts the text.", "text")
        expected = [
            TextNode("intro link", "link", "https://intro.com"),
            TextNode(" starts the text.", "text")
        ]
        result = split_nodes_link([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_link_end(self):
        node = TextNode("Text ends with a [final link](https://final.com)", "text")
        expected = [
            TextNode("Text ends with a ", "text"),
            TextNode("final link", "link", "https://final.com")
        ]
        result = split_nodes_link([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_consecutive_links(self):
        node = TextNode("[link1](https://link1.com)[link2](https://link2.com)[link3](https://link3.com)", "text")
        expected = [
            TextNode("link1", "link", "https://link1.com"),
            TextNode("link2", "link", "https://link2.com"),
            TextNode("link3", "link", "https://link3.com")
        ]
        result = split_nodes_link([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
    def test_image_nodes(self):
        node = TextNode("This is text with an image ![alt text](https://www.example.com/image.jpg) and another one ![second image](https://www.example.com/image2.jpg)", "text")
        expected = [
            TextNode("This is text with an image ", "text"),
            TextNode("alt text", "image", "https://www.example.com/image.jpg"),
            TextNode(" and another one ", "text"),
            TextNode("second image", "image", "https://www.example.com/image2.jpg")
        ]
        result = split_nodes_image([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_multiple_images_no_text(self):
        node = TextNode("![first image](https://www.example1.com/image1.jpg)![second image](https://www.example2.com/image2.jpg)", "text")
        expected = [
            TextNode("first image", "image", "https://www.example1.com/image1.jpg"),
            TextNode("second image", "image", "https://www.example2.com/image2.jpg")
        ]
        result = split_nodes_image([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_text_no_images(self):
        node = TextNode("This is simple text without any images.", "text")
        expected = [TextNode("This is simple text without any images.", "text")]
        result = split_nodes_image([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_image_beginning(self):
        node = TextNode("![intro image](https://intro.com/image.jpg) starts the text.", "text")
        expected = [
            TextNode("intro image", "image", "https://intro.com/image.jpg"),
            TextNode(" starts the text.", "text")
        ]
        result = split_nodes_image([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_image_end(self):
        node = TextNode("Text ends with an image ![final image](https://final.com/image.jpg)", "text")
        expected = [
            TextNode("Text ends with an image ", "text"),
            TextNode("final image", "image", "https://final.com/image.jpg")
        ]
        result = split_nodes_image([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_consecutive_images(self):
        node = TextNode("![image1](https://link1.com/image1.jpg)![image2](https://link2.com/image2.jpg)![image3](https://link3.com/image3.jpg)", "text")
        expected = [
            TextNode("image1", "image", "https://link1.com/image1.jpg"),
            TextNode("image2", "image", "https://link2.com/image2.jpg"),
            TextNode("image3", "image", "https://link3.com/image3.jpg")
        ]
        result = split_nodes_image([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_empty_image_alt_text(self):
        node = TextNode("This text has an image without alt text ![](https://www.example.com/image.jpg)", "text")
        expected = [
            TextNode("This text has an image without alt text ", "text"),
            TextNode("", "image", "https://www.example.com/image.jpg")
        ]
        result = split_nodes_image([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
    def test_nested_images_links(self):
        node = TextNode("Text with mixed content ![image](https://example.com/image.jpg) and a [link](https://example.com)", "text")
        expected = [
            TextNode("Text with mixed content ", "text"),
            TextNode("image", "image", "https://example.com/image.jpg"),
            TextNode(" and a [link](https://example.com)", "text")  
        ]
        result = split_nodes_image([node])
        assert result == expected, f"Expected {expected}, but got {result}"
        
        
class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        input_text = "This is **bold** and *italic* and `code`"
        expected_output = [
        TextNode("This is ", "text"),
        TextNode("bold", "bold"),
        TextNode(" and ", "text"),
        TextNode("italic", "italic"),
        TextNode(" and ", "text"),
        TextNode("code", "code")
    ]
        
        output = text_to_textnodes(input_text)
        assert output == expected_output, f"Expected {expected_output} but got {output}"
        
        
    def test_image_link_nodes(self):
        input_text = "An ![image](image_url) and a [link](link_url)"
        expected_output = [
            TextNode("An ", "text"),
            TextNode("image", "image", "image_url"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "link_url")
        ]
        
        output = text_to_textnodes(input_text)
        assert output == expected_output, f"Expected {expected_output} but got {output}"
        
        
    def test_empty_string(self):
        input_text = ""
        expected_output = []
        
        output = text_to_textnodes(input_text)
        assert output == expected_output, f"Expected {expected_output} but got {output}"
        
        
    def test_no_formatting(self):
        input_text = "plain text with no formatting"
        expected_output = [
            TextNode("plain text with no formatting", "text")
        ]
        
        output = text_to_textnodes(input_text)
        assert output == expected_output, f"Expected {expected_output} but got {output}"
        
        
    def test_sequential_formatting(self):
        input_text = "**bold**`code`*italic*"
        expected_output = [
            TextNode("bold", "bold"),
            TextNode("code", "code"),
            TextNode("italic", "italic")
        ]
        
        output = text_to_textnodes(input_text)
        assert output == expected_output, f"Expected {expected_output} but got {output}"


class TestMarkDownToBlocks(unittest.TestCase):
    def test_markdown_text(self):
        input_text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        output = markdown_to_blocks(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_multiple_blank_lines(self):
        input_text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.




* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        output = markdown_to_blocks(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_single_block(self):
        input_text = """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = ['* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        output = markdown_to_blocks(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_whitespace_handling(self):
        input_text = """# This is a heading          

This is a paragraph of text. It has some **bold** and *italic* words inside of it.       

        * This is the first list item in a list block
* This is a list item
* This is another list item          """
        expected = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        output = markdown_to_blocks(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_empty_input(self):
        input_text = ""
        expected = []
        output = markdown_to_blocks(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_header_single(self):
        input_text = """# This is a heading"""
        expected = "heading"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
    
    def test_block_to_header_multiple(self):
        input_text = """### This is a heading"""
        expected = "heading"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_block_to_header_max(self):
        input_text = """###### This is a heading"""
        expected = "heading"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
    def test_block_to_code(self):
        input_text = """```This is a code block.

        This is a line in the code block
        This is another line in the code block
        ```"""
        expected = "code"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_block_to_quote(self):
        input_text = """> This is a quote block.
        > This is a line in the quote block
        > This is another line in the quote block.
        > 
        > This is another line in the quote block. """
        expected = "quote"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_block_to_unordered_list_star(self):
        input_text = """* This is a unordered list block.
        * This is a line in the unordered list block
        * This is another line in the unordered list block.
        * 
        * This is another line in the unordered list block. """
        expected = "unordered_list"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_block_to_unordered_list_dash(self):
        input_text = """- This is a unordered list block.
        - This is a line in the unordered list block
        - This is another line in the unordered list block.
        - 
        - This is another line in the unordered list block. """
        expected = "unordered_list"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_block_to_unordered_list_mixed(self):
        input_text = """- This is a unordered list block.
        - This is a line in the unordered list block
        * This is another line in the unordered list block.
        - 
        - This is another line in the unordered list block. """
        expected = "paragraph"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_block_to_ordered_list(self):
        input_text = """1. This is a ordered list block.
        2. This is a line in the ordered list block
        3. This is another line in the ordered list block.
        4.  
        5. This is another line in the ordered list block. """
        expected = "ordered_list"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_block_to_paragraph(self):
        input_text = """This is a paragraph block.
        This is a line in the paragraph block
        This is another line in the paragraph block.
        
        This is another line in the paragraph block. """
        expected = "paragraph"
        output = block_to_block_type(input_text)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
class TestMarkdowntoHTMLNode(unittest.TestCase):
    def test_markdown(self):
        markdown_text = """### This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

> This is the first quote item
> This is a second quote item
> This is another quote item

```This is a block of code
This is a code line

This is another code line```

1. This is a list item
2. This is another list item
3. This is another list item

* This is an unordered list item
* This is an unordered list item
* This is an unordered list item"""
        
        root_node = markdown_to_html_node(markdown_text)
        
        self.assertIsInstance(root_node, ParentNode)
        self.assertEqual(root_node.tag, "div")
        
        heading_node = root_node.children[0]
        self.assertEqual(heading_node.tag, "h3")
        
        paragraph_node = root_node.children[1]
        self.assertEqual(paragraph_node.tag, "p")
        
        quote_node = root_node.children[2]
        self.assertEqual(quote_node.tag, "blockquote")
        
        pre_node = root_node.children[3]
        self.assertEqual(pre_node.tag, "pre")
        code_node = root_node.children[3].children[0]
        self.assertEqual(code_node.tag, "code")
        
        ol_node = root_node.children[4]
        self.assertEqual(ol_node.tag, "ol")
        li_node = root_node.children[4].children[0]
        self.assertEqual(li_node.tag, "li")
        
        ul_node = root_node.children[5]
        self.assertEqual(ul_node.tag, "ul")
        li_node = root_node.children[5].children[0]
        self.assertEqual(li_node.tag, "li")
        
        
    def test_heading_levels(self):
        markdown_text = """# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6"""

        root_node = markdown_to_html_node(markdown_text)
        
        self.assertIsInstance(root_node, ParentNode)
        self.assertEqual(root_node.tag, "div")
        
        heading_node1 = root_node.children[0]
        self.assertEqual(heading_node1.tag, "h1")
        
        heading_node2 = root_node.children[1]
        self.assertEqual(heading_node2.tag, "h2")
        
        heading_node3 = root_node.children[2]
        self.assertEqual(heading_node3.tag, "h3")
        
        heading_node4 = root_node.children[3]
        self.assertEqual(heading_node4.tag, "h4")
        
        heading_node5 = root_node.children[4]
        self.assertEqual(heading_node5.tag, "h5")
        
        heading_node6 = root_node.children[5]
        self.assertEqual(heading_node6.tag, "h6")
        
        
    def test_combined_inline_styles(self):
        markdown_text = "This is *italic* and **bold** and `inline code` text."
        
        root_node = markdown_to_html_node(markdown_text)
        
        self.assertIsInstance(root_node, ParentNode)
        self.assertEqual(root_node.tag, "div")
        
        paragraph_node = root_node.children[0]
        self.assertEqual(paragraph_node.tag, "p")     
        
        
        
    def test_combined_block_quotes(self):
        markdown_text = """> ## Quoted Heading
> 
> This is a quoted paragraph.
> 
> * Quoted list item"""

        root_node = markdown_to_html_node(markdown_text)   
        
        self.assertIsInstance(root_node, ParentNode)
        self.assertEqual(root_node.tag, "div")       
        
        blockquote_node = root_node.children[0]
        self.assertEqual(blockquote_node.tag, "blockquote")
        
        blank_node = root_node.children[0].children[0]
        self.assertEqual(blank_node.tag, "")
        
        header_node = root_node.children[0].children[0].children[0]
        self.assertEqual(header_node.tag, "h2")
        
        p_node = root_node.children[0].children[0].children[1]
        self.assertEqual(p_node.tag, "p")
        
        ul_node = root_node.children[0].children[0].children[2]
        self.assertEqual(ul_node.tag, "ul")
        
        li_node = root_node.children[0].children[0].children[2].children[0]
        self.assertEqual(li_node.tag, "li")
        
        
    def test_content_in_code_blocks(self):
        markdown_text = """```
def example():
    # Sample code
    return "hello"
```"""  
        root_node = markdown_to_html_node(markdown_text)  

        self.assertIsInstance(root_node, ParentNode)
        self.assertEqual(root_node.tag, "div")       
        
        pre_node = root_node.children[0]
        self.assertEqual(pre_node.tag, "pre")
        
        code_node = root_node.children[0].children[0]
        self.assertEqual(code_node.tag, "code")
        
        
    def test_consecutive_blocks(self):
        markdown_text = """### Heading
Paragraph following a heading.

> A quote follows with no extra blank line."""

        root_node = markdown_to_html_node(markdown_text)  

        self.assertIsInstance(root_node, ParentNode)
        self.assertEqual(root_node.tag, "div")  
        
        h3_node = root_node.children[0]
        self.assertEqual(h3_node.tag, "h3")
        
        p_node = root_node.children[1]
        self.assertEqual(p_node.tag, "p")
        
        blockquote_node = root_node.children[2]
        self.assertEqual(blockquote_node.tag, "blockquote")
        
        
class TestExtractTitle(unittest.TestCase):
    def test_multiple_headers(self):
        markdown = """# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6"""
        expected = "Heading 1"
        output = extract_title(markdown)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_no_h1_header(self):
        markdown = """## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6"""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
        
    def test_multiple_block_types(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        expected = "This is a heading"
        output = extract_title(markdown)
        assert output == expected, f"Expected {expected} but got {output}"
        
        
    def test_multiple_h1_blocks(self):
        markdown = """# This is an h1 heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

# This is a second h1 heading

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        expected = "This is an h1 heading"
        output = extract_title(markdown)
        assert output == expected, f"Expected {expected} but got {output}"
        
    def test_h1_lower(self):
        markdown = """This is a paragraph of text. It has some **bold** and *italic* words inside of it.

# This is a lower h1 heading

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        expected = "This is a lower h1 heading"
        output = extract_title(markdown)
        assert output == expected, f"Expected {expected} but got {output}"
        
    
    def test_no_h1_no_space(self):
        markdown = """#Heading 1
### Heading 2
#### Heading 3
##### Heading 4
###### Heading 5"""
        with self.assertRaises(Exception):
            extract_title(markdown)
        
if __name__ == "__main__":
    unittest.main()     