from docx import Document
import requests
import re
from copy import copy
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm
from pathlib import Path
from PIL import Image
import io

def image_to_jpg(image_path):
    Image.open(image_path).convert('RGB').save(image_path)
    return image_path
    
 
doc = Document()
doc.add_picture(image_to_jpg('picture2.jpg')   )
doc.save('dfghjk.docx')