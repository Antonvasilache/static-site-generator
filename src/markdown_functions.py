from textnode import TextNode, text_node_to_html_node
from htmlnode import ParentNode
import re
import textwrap


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #converting a markdown string into a list of TextNode objects, of type text, or type bold, italic, code, based on the input list
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != "text":
        #nodes of type other than text are added directly to the next list 
            new_nodes.append(node)
        else:
        #nodes of type text are attempted to be split into TextNode objects, based on the given delimiter
            new_node = node.text.split(delimiter)
            
            if len(new_node) % 2 != 0:
            #if the new node list length is an odd number, the list elements can be transformed into TextNode objects    
                for i in range(0, len(new_node)):
                    if new_node[i]:
                    #we work only on elements which are not empty strings
                        if i % 2 == 0:
                        #even elements will be of type text
                            new_text_node = TextNode(new_node[i], "text")
                            new_nodes.append(new_text_node)
                        else:
                        #odd elements will be of type delimiter (bold, italic etc.)
                            new_delimiter_node = TextNode(new_node[i], text_type)                                  
                            new_nodes.append(new_delimiter_node)
                        
            else:
            #if the new node list is an even number, we don't have a closing delimiter
                new_nodes.append(node)
                        
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_generic(old_nodes, extract_func, regex_pattern, text_type):
    #splitting TextNode objects into TextNode objects of type text and image or link, where appropriate
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
        #skip nodes that are not the primary text type
            new_nodes.append(node)
            continue
        
        results = re.split(regex_pattern, node.text)
        #creating a results list that is splitting the initial text node into multiple text nodes based on the given regex pattern
        extracted_nodes = extract_func(node.text)
        #creating a list of tuples, each with alt text and link, from the same source
        
        index = 0
        while index < len(results):        
        #iterating the results list and checking if any of the items is found within the extracted_nodes list
            special_flag = False
            #flag initialized with False, it will turn True if an item is found within the extracted_nodes
            if index + 1 < len(results):
            #removing unnecessary iterations    
                for ex_node in extracted_nodes:
                    #looping over extracted_nodes and checking if the results item is found in any of the extracted_nodes tuples
                    if results[index] == ex_node[0] and results[index + 1] == ex_node[1]:
                    #if the tuple matches with the current and next item, a new TextNode is created using the current and next item as alt text and url, and added to new_nodes
                        special_flag = True
                        special_text = results[index]
                        special_url = results[index + 1]
                        if special_url:
                            new_nodes.append(TextNode(special_text, text_type, special_url))
                        index += 1
                        break
                        
            if not special_flag and results[index]:
            #if flag is still False and the current item is not an empty string, the current item will be added to new_nodes as a text type TextNode
                new_nodes.append(TextNode(results[index], "text"))
                    
            index += 1
            
    return new_nodes
                            


def split_nodes_image(old_nodes):    
    #variation for split_nodes for images
    return split_nodes_generic(old_nodes, extract_markdown_images, r"!\[(.*?)\]\((.*?)\)", "image")


def split_nodes_link(old_nodes):    
    #variation for split_nodes for links
    return split_nodes_generic(old_nodes, extract_markdown_links, r"(?<!!)\[(.*?)\]\((.*?)\)", "link")


def text_to_textnodes(text):
    #Converting the given text into a list of TextNode objects by successively applying the split functions
    node = TextNode(text, "text")
    
    node_images = split_nodes_image([node])
  
    node_links = split_nodes_link([*node_images])
    
    node_bold = split_nodes_delimiter([*node_links], "**", "bold")   
   
    node_italic = split_nodes_delimiter([*node_bold], "*", "italic")
    
    node_code = split_nodes_delimiter([*node_italic], "`", "code")    
    
    return node_code


def markdown_to_blocks(markdown):
    #taking a full markdown document and converting it to a list of "block" strings
    dedent_mark = textwrap.dedent(markdown)
    
    #we need a different approach for code blocks marked by "```", so we identify and return any blocks that start and end with this separator
    regex = r"^```[\s\S]*?```$"
    matches = re.findall(regex, markdown, re.MULTILINE)
    
    #storing placeholders for each code block
    placeholder_map = {}
    placeholder_counter = 0
    
    #we create placeholders for our matches and replace every match in the markdown string with a placeholder
    for match in matches:
        placeholder = f"CODEBLOCK{placeholder_counter}"
        dedent_mark = dedent_mark.replace(match, placeholder)
        placeholder_map[placeholder] = match
        placeholder_counter += 1
    
    #we split our markdown string into block strings, now that we replaced any potential code blocks
    block_strings = dedent_mark.split("\n\n") 
    
    #isolating headings present in other blocks
    heading_regex = r"^(#{1,6} .+)"
    new_blocks = []
    for block in block_strings:
        parts = re.split(heading_regex, block, flags=re.MULTILINE)
        for part in parts:
            if part:
                new_blocks.append(part.strip())
    
    #reinserting code blocks by replacing the placeholders
    for i, block in enumerate(new_blocks):
        if block.startswith("CODEBLOCK"):
            new_blocks[i] = placeholder_map[block]
    
    #cleaning the blocks of whitespace
    clean_blocks = []      
    for block in new_blocks:
        lines = block.splitlines()
        
        #Defining patterns for ordered and unordered list markers
        ul_pattern = r"^\s*[*-]\s+"
        ol_pattern = r"^\s*\d+\.\s+"
        
        stripped_lines = []
        
        for index, line in enumerate(lines):
            #Strip first line regardless of pattern
            if index == 0:
                stripped_line = line.strip()
            else:
                #General stripping rule for lines that are not starting with list markers
                if not re.match(ul_pattern, line) and not re.match(ol_pattern, line):
                    stripped_line = line.strip()
                else:
                    stripped_line = line
                
            stripped_lines.append(stripped_line)
            
        clean_blocks.append('\n'.join(stripped_lines).strip())            
        
    #adding back only the non empty blocks
    clean_blocks = [block for block in clean_blocks if block]
    
    return clean_blocks     


def block_to_block_type(block):
    #function that returns the type of markdown block (6 types supported), based on the starting characters
    lines = block.splitlines()
    #list of lines to be used when checking for lists or quotes
    
    def heading():
        start_string = block[0:7]
        return bool(re.match(r"^#{1,6} ", start_string))
            
        
    def quote():
        quote_flag = True
        for line in lines:
            stripped_line = line.lstrip()
            if not stripped_line.startswith(">") or (len(stripped_line) > 1 and stripped_line[0] == ">" and stripped_line[1] != " "):
                quote_flag = False
                
        return quote_flag
  
    
    def unordered_list(char):
        ul_flag = True
        for line in lines:
            if not line.lstrip().startswith(char):
                ul_flag = False
                
        return ul_flag
    
    
    def ordered_list():
        ol_flag = True
        for i in range(0, len(lines)):
            if not lines[i].lstrip().startswith(f"{i + 1}. "):
                ol_flag = False
                
        return ol_flag
    
    if heading():
        block_type = "heading"
    elif block.startswith("```") and block.endswith("```"):
        block_type = "code"
    elif quote():
        block_type = "quote"
    elif unordered_list("* ") or unordered_list("- "):
        block_type = "unordered_list"
    elif ordered_list():
        block_type = "ordered_list"
    else:
        block_type = "paragraph"
    
    return block_type


def text_to_children(text): 
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    
    return html_nodes


def process_heading(block):
    heading_match = re.match(r"^#{1,6} ", block)
    heading_match = heading_match.group()
    heading_level = heading_match.count("#")
    text_content = block[len(heading_match):]                
    children = text_to_children(text_content)   
    heading_node = ParentNode(f"h{heading_level}", children, [])
    
    return heading_node


def process_code(block):
    code_match = "```"
    text_content = block[len(code_match):-len(code_match)]
    children = text_to_children(text_content)
    code_node = ParentNode("code", children, [])
    pre_node = ParentNode("pre", [code_node], [])
    
    return pre_node


def process_unordered_list(block):
    block_lines = block.splitlines()
    
    ul_pattern = r"^\s*[*-]\s+"
    
    text_lines = [re.sub(ul_pattern, '', line) for line in block_lines]    
    li_nodes = [ParentNode("li", text_to_children(line), []) for line in text_lines]
    ul_node = ParentNode("ul", li_nodes, [])   
    
    return ul_node


def process_ordered_list(block):
    block_lines = block.splitlines()
    
    ol_pattern = r"^\s*\d+\.\s+"
    
    text_lines = [re.sub(ol_pattern, '', line) for line in block_lines]
    li_nodes = [ParentNode("li", text_to_children(line), []) for line in text_lines]
    ol_node = ParentNode("ol", li_nodes, [])
    
    return ol_node               
    

def process_quote(block):
    quote_match = "> "
    block_lines = block.splitlines()
    text_lines = [line[len(quote_match):] for line in block_lines]
    text_content = "\n".join(text_lines)
    
    if (len(text_lines) > 1):    
        sub_quote_node = markdown_to_html_node(text_content, wrap_in_div=False)  
        quote_node = ParentNode("blockquote", [sub_quote_node], [])
    else:
        children = text_to_children(text_content)  
        quote_node = ParentNode("blockquote", children, [])  
    
    return quote_node


def process_paragraph(block):
    children = text_to_children(block)
    p_node = ParentNode("p", children, [])  
    return p_node


def markdown_to_html_node(markdown, wrap_in_div=True):
    markdown_blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
       
        match block_type:
            case "heading":
                heading_node = process_heading(block)
                block_nodes.append(heading_node)
                                
            case "quote":
                quote_node = process_quote(block)                
                block_nodes.append(quote_node)
                
            case "code":
                pre_node = process_code(block)
                block_nodes.append(pre_node)
                
            case "ordered_list":
                ol_node = process_ordered_list(block)            
                block_nodes.append(ol_node)
                
            case "unordered_list":               
                ul_node = process_unordered_list(block)
                block_nodes.append(ul_node)
                
            case "paragraph":
                p_node = process_paragraph(block) 
                block_nodes.append(p_node)
                                
    if wrap_in_div:
        result_node = ParentNode("div", block_nodes, [])   
    else:
        result_node = ParentNode("", block_nodes, [])             
    
    return result_node


def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            if re.match(r"^#\s", block):
                return block.strip("#").strip()
            
    raise Exception("No header was found")    


