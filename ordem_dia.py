import re
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser



prefix = 'http://mail.camara.rj.gov.br'
today = "10/04/2017"
browser = RoboBrowser()
next_coords = "0,4,82,18"
prev_coords = "85,3,157,18"
expand_coords = "242,0,306,18"

AMENDMENT_ID = "Emenda Nº"

def split_projects(text):
    begin_pattern = re.compile(r'(\n[0-9,]+\s+EM\s)')
    parts = begin_pattern.split(text)
    projects = [(parts[i] + parts[i+1]).strip() for i in range(1, len(parts), 2)]
    return projects

def has_chapters():
    # TODO: implement
    return False
    # chapter_pattern = re.compile(r'(CAPÍTULO.*Art.\s[1-9])', flags=re.DOTALL)
    # chapter_pattern = re.compile(r'(?=(CAPÍTULO.*(?=CAPÍTULO.*Art)))', flags=re.DOTALL)
    # parts = chapter_pattern.split(project_text)
    # take only parts with Capítulo and remove 'Art. [1-9]' (last 6 characters)
    # chapters = [text[:-6] for text in parts if chapter_pattern.match(text)]


def get_project_text(browser):
    soup = BeautifulSoup(str(browser.parsed()))
    full_text = soup.get_text()
    project_pattern = re.compile(r'(PROJETO\sDE\sLEI\sNº\s.*\nJUSTIFICATIVA\n)', flags=re.DOTALL)
    signature_pattern = re.compile(r'(Plenário\sTeotônio\sVillela.*(?=\nJUSTIFICATIVA\n))', flags=re.DOTALL)

    parts = project_pattern.split(full_text)
    project_text = [text for text in parts if project_pattern.match(text)][0]
    parts = signature_pattern.split(project_text)
    # discards JUSTIFICATIVA
    project_text = parts[0]
    signature = parts[1]

    return project_text, signature

def get_chapters(project_text):
    pass

def get_articles(project_text):
    if has_chapters():
        pass
    article_pattern = re.compile(r'(Art.\s[1-9])')
    parts = article_pattern.split(project_text)
    articles = [(parts[i] + parts[i+1]).strip() for i in range(1, len(parts), 2)]
    return articles


def next_page(browser):
    areas = browser.find_all('area')
    next_area = [a for a in areas if a.attrs['coords'] == next_coords][0]
    next_url = next_area.attrs['href']
    return prefix + next_url

def has_next_page(next_url):
    if next_url == browser.url:
        return False
    return True


def find_page_amendments(browser):
    amendments = [e for e in browser.get_links() if AMENDMENT_ID in str(e.text)]
    return amendments


def get_project_info(browser):
    info = {}
    # get amendments
    amendments = find_page_amendments(browser)
    next_url = next_page(browser)
    n = 1
    print(n)
    while has_next_page(next_url):
        browser.open(next_url)
        amendments.extend(find_page_amendments(browser))
        next_url = next_page(browser)
        n = n + 1
        print(n)
        print(next_url)
        print(browser.url)
    info['amendments'] = amendments
    return info

def print_amendments(browser):
    project_info = get_project_info(browser)
    amendments = project_info['amendments']
    # amendments = find_page_amendments(browser)
    for a in amendments:
        print(a)

def print_articles(browser):
    text, signature = get_project_text(browser)
    articles = get_articles(text)
    for art in articles:
        print(art)
        print('XXXXXXXXXXXX')

def daily_projects():
    browser.open('http://www.camara.rj.gov.br/index_principal.php')
    od_link = browser.get_link("Ordem do Dia")
    browser.follow_link(od_link)

    today_links = browser.get_link(today)
    # start with the main Ordem do Dia
    if len(today_links) > 1:
        browser.follow_link(today_links[-1])
    else:
        browser.follow_link(today_links[0])

    body = browser.find('body')
    od_text = str(body.text)
    projects = split_projects(od_text)


if __name__ == '__main__':
    # daily_projects()
    # PME
    browser.open('http://mail.camara.rj.gov.br/APL/Legislativos/scpro1720.nsf/f6d54a9bf09ac233032579de006bfef6/832580830061f31883258060005de906?OpenDocument')
    # print_amendments(browser)
    print_articles(browser)
    print("FEITO")


# coords="335,1,436,17"   href="http://mail.camara.rj.gov.br/APL/Legislativos/scpro1720.nsf/$$Search?openform"
# coords="162,3,232,17"   href="/APL/Legislativos/scpro1720.nsf/0cfaa89fb497093603257735005eb2bc/81c3ac25f843fada8325810600623c7e?OpenDocument&amp;CollapseView"
#
# coords="0,4,82,18"      href="/APL/Legislativos/scpro1720.nsf/0cfaa89fb497093603257735005eb2bc/81c3ac25f843fada8325810600623c7e?OpenDocument&amp;Start=1.1.1.20"
# coords="85,3,157,18"    href="/APL/Legislativos/scpro1720.nsf/0cfaa89fb497093603257735005eb2bc/81c3ac25f843fada8325810600623c7e?OpenDocument&amp;Start=1"
# coords="242,0,306,18"   href="/APL/Legislativos/scpro1720.nsf/0cfaa89fb497093603257735005eb2bc/81c3ac25f843fada8325810600623c7e?OpenDocument&amp;ExpandView"
# http://mail.camara.rj.gov.br/APL/Legislativos/scpro1720.nsf/0/832580830061f31883257f5e0064bd24?OpenDocument&Start=1.1.1.188
# http://mail.camara.rj.gov.br/APL/Legislativos/scpro1720.nsf/0/832580830061f31883257f5e0064bd24?OpenDocument&Start=1.1.1.188
