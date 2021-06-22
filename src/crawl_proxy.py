import re

import pandas as pd
import requests

from my_sqlite import insert_proxy_row

REGEX_IP_PORT = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}'


def print_func_name(func):
    def a(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)

    return a


@print_func_name
def free_proxy_list():
    url = 'https://free-proxy-list.net/'

    headers = {
        'authority': 'free-proxy-list.net',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '^\\^',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.77 '
                      'Safari/537.36',
        'accept': 'text/html,'
                  'application/xhtml+xml,'
                  'application/xml;q=0.9,'
                  'image/avif,'
                  'image/webp,'
                  'image/apng,'
                  '*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.google.com/',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = requests.get(url, headers=headers)

    li = set()
    for proxy in re.findall(REGEX_IP_PORT, response.text):
        ip, port = proxy.split(':')
        li.add((ip, int(port)))

    yield tuple(li)


@print_func_name
def proxyhub():
    def get_res(_page):
        headers = {
            'authority': 'www.proxyhub.me',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.106 '
                          'Safari/537.36',
            'accept': 'text/html,'
                      'application/xhtml+xml,'
                      'application/xml;q=0.9,'
                      'image/avif,'
                      'image/webp,'
                      'image/apng,'
                      '*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.proxyhub.me/en/all-http-proxy-list.html',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'page={_page}; anonymity=all',
        }

        res = requests.get('https://www.proxyhub.me/en/all-http-proxy-list.html', headers=headers)
        return res.text

    tp = tuple()
    for i in range(1, 2):
        try:
            print(f'page: {i}')
            res_text = get_res(i)
            ip_df = pd.read_html(res_text)[0]
            ip_df.dropna(subset=["IP", "Port"])
            li = []
            for _, row in ip_df.iterrows():
                li.append((row.IP, row.Port))
        except Exception as e:
            print(e)
            break
        else:
            added = tuple(set(li) - set(tp))
            if len(added):
                print(f'+{len(added)}({len(tp)})')
                yield added
                tp += tuple(li)
            else:
                print(f'crawled ip({len(li)}) are existed')
                break


@print_func_name
def crawl(proxy_func):
    for tp in proxy_func():
        insert_proxy_row(*tp)


if __name__ == '__main__':
    crawl(proxyhub)
    crawl(free_proxy_list)
