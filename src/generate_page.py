from pathlib import Path

from extract_title import extract_title
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_page_contents = Path(from_path).read_text()
    template_contents = Path(template_path).read_text()
    html_page_contents = markdown_to_html_node(markdown_page_contents).to_html()
    title = extract_title(markdown_page_contents)
    templated_html_file = template_contents.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_page_contents
    )

    with open(dest_path, "r", encoding="utf-8") as f:
        f.write(templated_html_file)
