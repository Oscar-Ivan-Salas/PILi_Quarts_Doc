
import logging
from bs4 import BeautifulSoup
from openpyxl import Workbook
import sys
import os

# Setup path
sys.path.append(os.path.abspath("e:/PILi_Quarts/PILi_Quarts_V3.0/backend"))

from modules.N04_Binary_Factory.excel_converter import TeslaExcelConverter

# Mock logger
logging.basicConfig(level=logging.INFO)

def test_color_parsing():
    html = """
    <div style="font-family: 'Roboto'; color: rgb(255, 0, 0); font-size: 14pt;">
        Test Wrapper
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')
    converter = TeslaExcelConverter()
    
    # Test _parse_style indirect access or logic simulation
    body_div = soup.find('div')
    color, size = converter._parse_style(body_div)
    
    print(f"Parsed Color: {color} (Expected: FF0000)")
    print(f"Parsed Size: {size}")
    
    # Verify openpyxl side
    from openpyxl.styles import Side
    
    try:
        side = Side(border_style='medium', color=color)
        print("✅ OpenPyXL Side created successfully with parsed color.")
    except Exception as e:
        print(f"❌ OpenPyXL Failed: {e}")

if __name__ == "__main__":
    test_color_parsing()
