from helpers import copy_contents, generate_pages_recursive

    
def main():
    copy_contents("./static", "./public")
    
    generate_pages_recursive("content", "template.html", "public")    
    
main()