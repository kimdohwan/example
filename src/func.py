import asyncio
import random
import selectors
import threading

import aiohttp
import requests
from aiohttp_proxy import ProxyConnector

from src.my_sqlite import select_all_proxy

lock = threading.Lock()


class AsyncReq:
    def __init__(self):
        self.proxy = []

    def set_proxy_list(self):
        proxy = list(select_all_proxy())
        random.shuffle(proxy)
        self.proxy = proxy
        print(f'set proxy : {len(self.proxy)}')

    def get(self):
        pass

    def post(self):
        pass

    # async def request(self, url, req_kwargs=None, ret_val='', proxy=False):
    #     req_kwargs: dict
    #     proxy: bool
    #
    #     if not isinstance(req_kwargs, dict):
    #         req_kwargs = {}
    #
    #     while True:
    #         if proxy:
    #             while True:
    #                 try:
    #                     ip, port = self.proxy.pop()
    #                     break
    #                 except IndexError:
    #                     self.set_proxy_list()
    #             connector = {'connector': ProxyConnector.from_url(f'http://{ip}:{port}')}
    #         else:
    #             connector = {}
    #
    #         req_kwargs['timeout'] = 120
    #         try:
    #             async with aiohttp.ClientSession(**connector) as sess:
    #                 async with sess.get(url=url, **req_kwargs) as res:
    #                     if ret_val == 'html':
    #                         await res.read()
    #                     elif ret_val == 'json':
    #                         await res.json()
    #                     else:
    #                         await res.read()
    #         except Exception as e:
    #             print(e)
    #             return None
    #         else:
    #             print('success')
    #             return res

    def request(self, url, req_kwargs=None, proxy=False):
        req_kwargs: dict
        proxy: bool

        if not isinstance(req_kwargs, dict):
            req_kwargs = {}

        while True:
            with lock:
                if proxy:
                    while True:
                        try:
                            ip, port = self.proxy.pop()
                            break
                        except IndexError:
                            self.set_proxy_list()
                    proxies = {'http': f'http://{ip}:{port}', 'https': f'https://{ip}:{port}'}
                else:
                    proxies = None

            req_kwargs['timeout'] = 60
            try:
                res = requests.get(url, proxies=proxies, **req_kwargs)
            except Exception as e:
                print(e)
                return None
            else:
                print('success')
                return res


def check_alive():
    # async def check(_ar):
    #     cookies = {
    #         'NRTK': 'ag#all_gr#1_ma#-2_si#0_en#0_sp#0',
    #         'NNB': 'PKRN4OPQULSV6',
    #         'MM_NEW': '1',
    #         'NFS': '2',
    #         'MM_NOW_COACH': '1',
    #         'NV_WETR_LAST_ACCESS_RGN_M': 'MDkxNDAxMDQ=',
    #         'NV_WETR_LOCATION_RGN_M': 'MDkxNDAxMDQ=',
    #         'ASID': 'd32f6a02000001780792c2b60000004f',
    #         'NDARK': 'N',
    #         '_ga': 'GA1.2.1729505386.1608967456',
    #         '_ga_7VKFYR6RV1': 'GS1.1.1617973386.2.1.1617974025.60',
    #         'nid_inf': '304617709',
    #         'NID_JKL': 'ECMHTZjdUdIma2dxn7WPSxNA8ID449wRuFfcBoSG2RI=',
    #         'BMR': 's=1624278191447&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dtankun25%26logNo%3D221299511268&r2=https%3A%2F%2Fwww.google.com%2F',
    #         'page_uid': 'hLug1lprvxsssUbONAhssssstkG-434656',
    #         'nx_ssl': '2',
    #     }
    #
    #     headers = {
    #         'authority': 'www.naver.com',
    #         'cache-control': 'no-cache',
    #         'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    #         'sec-ch-ua-mobile': '?0',
    #         'upgrade-insecure-requests': '1',
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
    #         'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    #         'sec-fetch-site': 'same-site',
    #         'sec-fetch-mode': 'no-cors',
    #         'sec-fetch-user': '?1',
    #         'sec-fetch-dest': 'image',
    #         'referer': 'https://finance.naver.com/',
    #         'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #         'cookie': 'NM_THEME_EDIT=; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; NNB=PKRN4OPQULSV6; MM_NEW=1; NFS=2; MM_NOW_COACH=1; NV_WETR_LAST_ACCESS_RGN_M="MDkxNDAxMDQ="; NV_WETR_LOCATION_RGN_M="MDkxNDAxMDQ="; ASID=d32f6a02000001780792c2b60000004f; NDARK=N; _ga=GA1.2.1729505386.1608967456; _ga_7VKFYR6RV1=GS1.1.1617973386.2.1.1617974025.60; JSESSIONID=3F1C44F9C7422B472981542884857C01; nid_inf=304617709; NID_JKL=ECMHTZjdUdIma2dxn7WPSxNA8ID449wRuFfcBoSG2RI=; PM_CK_loc=5f3466a68c9d7275c4f27e0d3d01570a8045fdcebe8b451d1f0e1a91ebcc72b5; BMR=s=1624278191447&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dtankun25%26logNo%3D221299511268&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hLug1lprvxsssUbONAhssssstkG-434656; nx_ssl=2',
    #         'if-modified-since': 'Mon, 21 Jun 2021 14:59:01 GMT',
    #         'Referer': 'https://finance.naver.com/',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
    #         'Upgrade-Insecure-Requests': '1',
    #         'Origin': 'https://finance.naver.com',
    #         'content-length': '0',
    #         'charset': 'utf-8',
    #         'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    #         'origin': 'https://finance.naver.com',
    #         'Connection': 'keep-alive',
    #         'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    #         'Sec-Fetch-Site': 'same-site',
    #         'Sec-Fetch-Mode': 'no-cors',
    #         'Sec-Fetch-Dest': 'image',
    #         'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #         'pragma': 'no-cache',
    #     }
    #
    #     return await asyncio.gather(*[_ar.request('https://finance.naver.com/', req_kwargs={'cookies': cookies, 'headers': headers}, ret_val='html', proxy=True) for _ in range(100)])
    #
    # ar = AsyncReq()
    # return asyncio.run(check(ar))

    cookies = {
        'NRTK': 'ag#all_gr#1_ma#-2_si#0_en#0_sp#0',
        'NNB': 'PKRN4OPQULSV6',
        'MM_NEW': '1',
        'NFS': '2',
        'MM_NOW_COACH': '1',
        'NV_WETR_LAST_ACCESS_RGN_M': 'MDkxNDAxMDQ=',
        'NV_WETR_LOCATION_RGN_M': 'MDkxNDAxMDQ=',
        'ASID': 'd32f6a02000001780792c2b60000004f',
        'NDARK': 'N',
        '_ga': 'GA1.2.1729505386.1608967456',
        '_ga_7VKFYR6RV1': 'GS1.1.1617973386.2.1.1617974025.60',
        'nid_inf': '304617709',
        'NID_JKL': 'ECMHTZjdUdIma2dxn7WPSxNA8ID449wRuFfcBoSG2RI=',
        'BMR': 's=1624278191447&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dtankun25%26logNo%3D221299511268&r2=https%3A%2F%2Fwww.google.com%2F',
        'page_uid': 'hLug1lprvxsssUbONAhssssstkG-434656',
        'nx_ssl': '2',
    }

    headers = {
        'authority': 'www.naver.com',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'image',
        'referer': 'https://finance.naver.com/',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'NM_THEME_EDIT=; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; NNB=PKRN4OPQULSV6; MM_NEW=1; NFS=2; MM_NOW_COACH=1; NV_WETR_LAST_ACCESS_RGN_M="MDkxNDAxMDQ="; NV_WETR_LOCATION_RGN_M="MDkxNDAxMDQ="; ASID=d32f6a02000001780792c2b60000004f; NDARK=N; _ga=GA1.2.1729505386.1608967456; _ga_7VKFYR6RV1=GS1.1.1617973386.2.1.1617974025.60; JSESSIONID=3F1C44F9C7422B472981542884857C01; nid_inf=304617709; NID_JKL=ECMHTZjdUdIma2dxn7WPSxNA8ID449wRuFfcBoSG2RI=; PM_CK_loc=5f3466a68c9d7275c4f27e0d3d01570a8045fdcebe8b451d1f0e1a91ebcc72b5; BMR=s=1624278191447&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dtankun25%26logNo%3D221299511268&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hLug1lprvxsssUbONAhssssstkG-434656; nx_ssl=2',
        'if-modified-since': 'Mon, 21 Jun 2021 14:59:01 GMT',
        'Referer': 'https://finance.naver.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://finance.naver.com',
        'content-length': '0',
        'charset': 'utf-8',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'origin': 'https://finance.naver.com',
        'Connection': 'keep-alive',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'image',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'pragma': 'no-cache',
    }

    t = AsyncReq()  # sub thread 생성
    url = 'https://finance.naver.com/'
    ts = [threading.Thread(name=f'WORKER{i + 1}', target=t.request, args=(url,), kwargs={'req_kwargs': {
        'cookies': cookies,
        'headers': headers}, 'proxy': True})
          for i in range(1000)]
    for t in ts:
        t.start()

    for t in ts:
        t.join()


    # res = t.request(, req_kwargs={'cookies': cookies, 'headers': headers}, proxy=True)  # sub thread의 run 메서드를 호출

    print(1)


if __name__ == '__main__':
    a = check_alive()
    pass
