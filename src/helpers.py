import os
import shutil
from markdown_functions import markdown_to_html_node, extract_title
from pathlib import Path

def copy_contents(from_path, dest_path):
    #copy contents from one dir to another, deleting the destination dir, if it exists
    try:
        if os.path.exists(from_path):   
            src_list = os.listdir(from_path)        
            
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
            os.mkdir(dest_path)
        else:
            os.mkdir(dest_path)
        
        for item in src_list:
            item_path = os.path.join(from_path, item)
            
            if os.path.isfile(item_path):
                shutil.copy(item_path, dest_path)
                
            elif os.path.isdir(item_path):
                new_src_path = os.path.join(from_path, item)
                new_dest_path = os.path.join(dest_path, item)
                
                os.mkdir(new_dest_path)
                copy_contents(new_src_path, new_dest_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
        
def generate_page(from_path, template_path, dest_path):
    #reading contents from a file, and creating an html page using a given template, to the destination dir
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as file:
        content = file.read()
        
    with open(template_path, 'r') as file:
        template = file.read()
        
    title = extract_title(content)
        
    html_node = markdown_to_html_node(content)
    html_content = html_node.to_html()    
    
    html = template.replace("{{ Title }}", title) 
    html = html.replace("{{ Content }}", html_content)
    
    with open(dest_path, 'w') as file:
        file.write(html)
        
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    try:
        if os.path.exists(dir_path_content):
            content_list = os.listdir(dir_path_content)        
        
        #iterating over directory entries.    
        for entry in content_list:
            entry_path = os.path.join(dir_path_content, entry)
            entry_path_object = Path(entry_path)    
            
            #If the entry is a an md file, we generate an html page
            if entry_path_object.is_file():
                filename = entry_path_object.name
                
                if filename.endswith(".md"):                    
                    new_dest_path = os.path.join(dest_dir_path, entry)
                    new_dest_path = new_dest_path.replace(".md", ".html")                   
                    generate_page(entry_path, "./template.html", new_dest_path)
             
            #If the entry is a directory, create the directory path, the directories, and recursively call the function using the current entry path as a content path argument 
            elif entry_path_object.is_dir():
                new_dest_path = os.path.join(dest_dir_path, entry)                
                os.makedirs(new_dest_path, exist_ok=True)           
                generate_pages_recursive(entry_path, template_path, new_dest_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")



        
   