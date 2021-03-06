import random
import threading
from queue import Queue

import requests

from src.modules.func_etc import Func, ReqBaseException
from src.modules.my_sqlite import select_all_proxy, bulk_insert_proxy
from src.scrape.site_naver_finance import ItemFrgn

TIMEOUT = 30

lock = threading.Lock()


# def check_alive():
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
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/91.0.4472.106 '
#                       'Safari/537.36',
#         'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
#         'sec-fetch-site': 'same-site',
#         'sec-fetch-mode': 'no-cors',
#         'sec-fetch-user': '?1',
#         'sec-fetch-dest': 'image',
#         'referer': 'https://finance.naver.com/',
#         'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
#         'if-modified-since': 'Mon, 21 Jun 2021 14:59:01 GMT',
#         'Referer': 'https://finance.naver.com/',
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
#     t = AsyncReq()  # sub thread ??????
#     url = 'https://finance.naver.com/'
#     ts = [threading.Thread(name=f'WORKER{i + 1}', target=t.request, args=(url,), kwargs={'req_kwargs': {
#         'cookies': cookies,
#         'headers': headers}, 'proxy': True})
#           for i in range(3)]
#     for t in ts:
#         t.start()
#
#     for t in ts:
#         t.join()
#
#     # res = t.request(, req_kwargs={'cookies': cookies, 'headers': headers}, proxy=True)  # sub thread??? run ???????????? ??????
#
#     print(1)
#
#
# @Func.print_func_name
# def proxy_validation():
#     url = 'https://finance.naver.com/'
#     headers = {
#         'authority': 'finance.naver.com',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/91.0.4472.114 '
#                       'Safari/537.36',
#         'sec-fetch-site': 'same-origin',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-dest': 'document',
#         'referer': 'https://finance.naver.com/sise/',
#         'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
#     }
#     th_list = []
#     for ip, port in select_all_proxy():
#         proxy_validation_exec(ip, port, url, headers=headers)
#
#         th = threading.Thread(
#             target=proxy_validation_exec,
#             args=(ip, port, url,),
#             kwargs={'headers': headers}
#         )
#
#     for th in th_list:
#         th.start()
#
#     for th in th_list:
#         th.join()
#
#
# def proxy_validation_exec(ip, port, url, **kwargs):
#     session = requests.Session()
#     session.proxies = {
#         'http': f'http://{ip}:{port}',
#         'https': f'https://{ip}:{port}',
#     }
#
#     res = requests.get(url, **kwargs)
#     res.raise_for_status()


@Func.print_func_name
def crawl_proxy(proxy_func):
    for tp in proxy_func():
        bulk_insert_proxy(*tp)


class ProxyReq:
    def __init__(self):
        self.proxy_gen = self._proxy_gen()

    @staticmethod
    def _proxy_gen():
        while True:
            all_proxy = select_all_proxy()
            random.shuffle(all_proxy)
            for ip, port in all_proxy:
                print(threading.current_thread().name, ip, port)
                yield ip, port

    def next_proxy(self):
        with lock:
            return next(self.proxy_gen)

    def req(self, req_q, res_q):
        ip, port = '', ''
        default_kwargs = {'timeout': TIMEOUT}
        while True:
            req = req_q.get()
            retry = 0
            while True:
                try:
                    if not ip or not port:
                        raise ProxyReq.NoProxy

                    session = requests.Session()
                    session.proxies = {
                        'http': f'http://{ip}:{port}',
                        'https': f'https://{ip}:{port}',
                    }
                    try:
                        retry += 1
                        with Func.check_time():
                            res = getattr(session, req.method)(
                                req.url,
                                **req.req_kwargs,
                                **default_kwargs
                            )
                        req.is_valid(res)
                    except Exception as e:
                        ip, port = self.next_proxy()
                        if retry % 10 == 0:
                            print(threading.current_thread().name, f'{retry=}, {req.url, req.req_kwargs}')
                        # print(threading.current_thread().name, e)
                        if isinstance(e, ReqBaseException):
                            raise
                        else:
                            continue
                    else:
                        print('success')
                        res_q.put_nowait(req)
                        break
                except ProxyReq.NoProxy:
                    ip, port = self.next_proxy()
                    continue

    class NoProxy(Exception):
        pass


@Func.print_func_name
def exec_crawl():
    # a = check_alive()
    pr = ProxyReq()
    req_if_list = [ItemFrgn('035720', 1) for _ in range(5)]

    req_q = Queue()
    res_q = Queue()
    for req_if in req_if_list:
        req_q.put_nowait(req_if)

    ts = [threading.Thread(name=f'WORKER{i + 1}', target=pr.req, args=(req_q, res_q,)) for i, req_if in
          enumerate(req_if_list)]
    for t in ts:
        t.start()

    while True:
        req_if = res_q.get()
        print(req_if)


# if __name__ == '__main__':
#     from src.scrape.site_proxy import free_proxy_list

    #     '''crawl proxy'''
    #     from src.crawl_proxy import proxyhub, free_proxy_list
    #     crawl_proxy(proxyhub)
    # crawl_proxy(free_proxy_list)
