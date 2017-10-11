from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

import json
import re

BRIEF = 'Ementa'
AUTHORS = 'Autores'
TEXT = 'Texto'
DATE = 'Data'
ARTICLES = 'Artigos'
JUSTIFICATION = 'Justificativa'

amendment_pattern = re.compile(r'(Texto\s*da\s*Emenda.*\nJUSTIFICATIVA\n)', flags=re.DOTALL)
project_pattern = re.compile(r'(PROJETO\s*DE\s*LEI\s*Nº\s.*\nJUSTIFICATIVA\n)', flags=re.DOTALL)
signature_pattern = re.compile(r'(Plenário\s*Teotônio\s*Villela.*(?=\nJUSTIFICATIVA\n))', flags=re.DOTALL)

brief_pattern = re.compile(r'(EMENTA:.*?(?=Autor))', flags=re.DOTALL)
authors_pattern = re.compile(r'(Autor.*?:.*?(?=A\sCÂMARA\sMUNICIPAL\sDO\sRIO\sDE\sJANEIRO))')
date_pattern = re.compile(r'(Plenário\s*Teotônio\s*Villela.*?[0-9]+\s*de\s*\w*\s*de\s*[0-9]{4})')
justification_pattern = re.compile(r'(JUSTIFICATIVA.*?(?=Legislação\s*Citada))')

trash_pattern = re.compile(r'(Atalho\s*para\s*outros\s*documentos.*Informações\s*Básicas)', flags=re.DOTALL)
# supporters_pattern = re.compile(r'(Com\s*o\s*apoio\s*dos\s*Senhores)')

class Project:
    def __init__(self, name, url):
        self.data = {'name': name, 'url': url}
        browser = RoboBrowser()
        browser.open(url)
        soup = BeautifulSoup(str(browser.parsed()))
        self.full_text = soup.get_text()
        # throw garbage off
        self.full_text = trash_pattern.split(self.full_text)[0]

    @property
    def name(self):
        '''Nome do Projeto'''
        return self.data['name']

    @property
    def url(self):
        return self.data['url']

    @property
    def brief(self):
        '''Ementa'''
        if self.data.get(BRIEF):
            return self.data.get(BRIEF)
        match = brief_pattern.search(self.full_text)
        self.data[BRIEF] = match.group(0)
        return self.data[BRIEF]

    @property
    def authors(self):
        '''Autores'''
        if self.data.get(AUTHORS):
            return self.data.get(AUTHORS)
        match = authors_pattern.search(self.full_text)
        self.data[AUTHORS] = match.group(0)
        return self.data[AUTHORS]

    @property
    def date(self):
        '''Data'''
        if self.data.get(DATE):
            return self.data.get(DATE)
        match = date_pattern.search(self.full_text)
        place_date = match.group(0)
        match = re.search(r'([0-9]+\s*de\s*\w*\s*de\s*[0-9]{4})', place_date)
        self.data[DATE] = match.group(0)
        return self.data[DATE]

    @property
    def text(self):
        '''Texto do projeto'''
        if self.data.get(TEXT):
            return self.data.get(TEXT)
        parts = project_pattern.split(self.full_text)
        project_text = [text for text in parts if project_pattern.match(text)][0]
        parts = signature_pattern.split(project_text)
        self.data[TEXT] = parts[0]
        return self.data[TEXT]

    @property
    def justification(self):
        '''Justificativa'''
        if self.data.get(JUSTIFICATION):
            return self.data.get(JUSTIFICATION)
        match = justification_pattern.search(self.full_text)
        self.data[JUSTIFICATION] = match.group(0)
        return self.data[JUSTIFICATION]

    @property
    def legislation_quoted():
        pass

    def articles(self):
        '''Artigos presentes no projeto'''
        if self.data.get(ARTICLES):
            return self.data.get(ARTICLES)
        if has_chapters():
            pass
        article_pattern = re.compile(r'(Art.\s[1-9])')
        parts = article_pattern.split(self.full_text)
        self.data[ARTICLES] = [(parts[i] + parts[i+1]).strip() for i in range(1, len(parts), 2)]
        return self.data[ARTICLES]

    def __str__(self):
        self.brief
        self.authors
        self.date
        self.articles
        self.text
        self.justification
        return str(self.data)


class Amendment(Project):
    @property
    def supporters():
        pass

    def project():
        pass

    def kind():
        pass
