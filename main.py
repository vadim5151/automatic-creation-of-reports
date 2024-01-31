import requests
import re
from copy import copy
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def get_url_user_and_check_it():
    while True: 
            url_user = input('Введите вашу ссылку: ')     
            try:
                response = requests.get(url_user)
            except requests.exceptions.MissingSchema:
                print('ссылка неправильно введена')
                continue
            if "wikipedia.org" not in url_user:
                print('Введите ссылку на википедию')
                continue
            if response.status_code != 200:
                print('неизвестная ошибка сервера.Возможно неверно введена ссылка')
                continue 
            return response

def setting_styles(doc):
    style = doc.styles['Normal']
    style.font.size = Pt(14)
    style.font.name =  "Times New Roman"
    return style

def fill_in_file(all_tags,doc):      
    for i in all_tags: 
        if '<p' in i:
            p = doc.add_paragraph(BeautifulSoup(i,features="html.parser").text)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            continue
        for a in range(1,5):
            if f'<h{a}' in i:
                head = doc.add_heading(BeautifulSoup(i,features="html.parser").text, level=a)
                head.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
def get_rid_of_unnecessary_sections_bottom(all_tags):   
    reversed_all_tags = list(reversed(all_tags))
    for i in reversed_all_tags:
        if '<p>' in str(i):
            index = reversed_all_tags.index(i)
            del reversed_all_tags[0:index]
            return list(reversed(reversed_all_tags))

def get_rid_of_unnecessary_sections_from_above(all_tags):
    copy_all_tags = copy(all_tags)
    for i in copy_all_tags:
        if'<p>' in str(i):
            index = copy_all_tags.index(i)
            del copy_all_tags[0:index-2]
            return copy_all_tags

def get_tags_without_notes(all_tags):
        return [re.sub(r"\[.*?\]",r"", str(i)) for i in all_tags]

def try_save(doc,file_name):
        try:
            doc.save(f'{file_name}.docx')
        except PermissionError:
            print('Не удалось сохранить файл ')

if __name__ == '__main__':
    response = get_url_user_and_check_it()

    soup = BeautifulSoup(response.text, features="html.parser")
    mw_content_text_block = soup.find('div',id = 'mw-content-text')

    doc = Document()
    
    all_tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4'])
    styles = setting_styles(doc)
    all_tags = get_rid_of_unnecessary_sections_bottom(all_tags)
    all_tags = get_rid_of_unnecessary_sections_from_above(all_tags)
    all_tags = get_tags_without_notes(all_tags)
    fill_in_file(all_tags,doc)
    file_name = input('Выберите имя файла: ')
    try_save(doc,file_name)
    
