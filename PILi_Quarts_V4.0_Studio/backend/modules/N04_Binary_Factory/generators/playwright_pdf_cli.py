import sys
import os
from playwright.sync_api import sync_playwright

def generate_pdf(html_content_path, output_path):
    try:
        with open(html_content_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html_content)
            page.pdf(
                path=output_path, 
                format="A4", 
                margin={"top": "2cm", "bottom": "2cm", "left": "2cm", "right": "2cm"}, 
                print_background=True
            )
            browser.close()
        print(f"SUCCESS:{output_path}")
    except Exception as e:
        print(f"ERROR:{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python playwright_pdf_cli.py <html_path> <output_path>")
        sys.exit(1)
    generate_pdf(sys.argv[1], sys.argv[2])
