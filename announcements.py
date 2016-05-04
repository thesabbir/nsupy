import requests
from bs4 import BeautifulSoup


def get_many(from_n=0, upto=None):
    notices = []
    url = "http://www.northsouth.edu/nsu-announcements/?anaunc_start={0}".format(from_n)
    r = requests.get(url)
    if r.status_code / 100 == 2:
        soup = BeautifulSoup(r.text, "lxml")
        for notice in [notice_h3.find('a') for notice_h3 in soup.find('div', {'id': 'nsuannouncement'}).find_all('h3')]:
            notices.append({
                'id': from_n + len(notice) - 1,
                'title': notice.text.strip(),
                'url': notice.get('href') if notice.get('href')[:7] == "http://" else "http://www.northsouth.edu/" +
                                                                                      notice.get('href')
            })

    return notices


def get(n=0):
    return get_many(from_n=n, upto=n)[0]


def read(url=None):
    if url and url[:44] == 'http://www.northsouth.edu/nsu-announcements/':
        r = requests.get(url)
        if r.status_code / 100 == 2:
            soup = BeautifulSoup(r.text, "lxml")
            link = soup.find('div', {'id': 'research-align'}).find('a')
            try:
                url = link.get('href') if link.get('href')[:7] == "http://" else "http://www.northsouth.edu/" +\
                                                                                 link.get('href')
            except AttributeError:
                url = None
            return {
                'title': soup.find('div', {'id': 'breadcrumbs'}).find('span', {'class': 'B_currentCrumb'}).text,
                'url': url,
                'body': ("".join([p.text.strip() + " " for p in soup.find('div', {'id': 'research-align'}).find_all('p')
                                  if not len(p.text.strip())== 0])).strip()
            }