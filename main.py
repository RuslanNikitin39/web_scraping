import requests
import bs4
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'azure', 'DevOps', 'админ', 'Герман', 'Frontend', 'wallet', 'Процесс',
            'люди']


def run_request(current_url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_ym_uid=1589784582931479475; _ga=GA1.2.726331468.1628762646; hl=ru; fl=ru; __gads=ID=8aa3b2ce66c2fb17:T=1628762646:S=ALNI_MbDgnoPNOIVvXmweewgMTl16JMTmw; feature_streaming_comments=true; _gid=GA1.2.1782263930.1644849993; _ym_d=1644849993; _ym_isad=2; cto_bundle=HIu2ql9yUWZ4MjlOVktHTWRPYko4RUJQdGVMdGpRMlpvazZiV2p2TTFUQnhzRHQlMkZ5aWtBOFNEJTJCa1cyNU9ucW8yaUs5SFhJU3lOem9sWmtsOVRxWmxQJTJCVWY5TyUyRjgwMWlBaGdNRiUyQjUwaVVCc3BDYUk3YTdwd2toVjIyVkhlSFQwM09Od0RKbkVwSVhFazZsekZVZ1M3UVNOZyUyRlElM0QlM0Q; _gat=1',
        'Host': 'habr.com',
        'Referer': 'https://www.google.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
    }

    response = requests.get(current_url, headers=headers)
    response.raise_for_status()

    return response.text


def get_links(current_url, txt_fnd=''):
    keywords = [word.lower() for word in KEYWORDS]
    text = run_request(current_url)

    soup = bs4.BeautifulSoup(text, features='html.parser')

    articles = soup.find_all('article')
    i = 0
    for article in articles:
        i += 1
        href = article.find(class_='tm-article-snippet__readmore').attrs['href']
        link = base_url + href
        title = article.find('h2').find('span').text
        date = article.find('time').attrs['title']

        current_text = article.find_all(class_='article-formatted-body article-formatted-body_version-2')
        words = []
        print(i, link)
        result = date + '  ' + title + '  ' + link
        if not len(current_text) == 0:
            words = [word.lower() for word in (re.findall(r'\b(\w+)\b', current_text[0].text.strip()))]
        if not len(set(words)) + len(set(keywords)) == len(set(words + keywords)):
            print(result)
        else:
            if check_link(link, keywords):
                print(result)


def check_link(link, keywords):
    text = run_request(link)
    soup = bs4.BeautifulSoup(text, features='html.parser')
    current_text = soup.find_all(class_='article-formatted-body article-formatted-body_version-1')
    if len(current_text) == 0:
        current_text = soup.find_all(class_='article-formatted-body article-formatted-body_version-2')
    words = []
    if not len(current_text) == 0:
        words = [word.lower() for word in (re.findall(r'\b(\w+)\b', current_text[0].text.strip()))]
    if not len(set(words)) + len(set(keywords)) == len(set(words + keywords)):
        return True


if __name__ == '__main__':
    base_url = 'https://habr.com'
    url = base_url + '/ru/all/'
    get_links(url)
