import asyncio

import aiohttp
import pandas as pd
import requests


class ItemSiseDay:
    def __init__(self, company_code, page_num):
        self.method = 'get'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.101 '
                          'Safari/537.36',
            'accept': 'text/html,'
                      'application/xhtml+xml,'
                      'application/xml;q=0.9,'
                      'image/avif,'
                      'image/webp,'
                      'image/apng,'
                      '*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.params = (
            ('code', str(company_code)),
            ('page', str(page_num)),
        )
        self.url = f'https://finance.naver.com/item/sise_day.nhn'
        self.content_type = 'text/html'


class ItemFrgn:
    def __init__(self, company_code, page_num):
        self.method = 'get'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.101 '
                          'Safari/537.36',
            'accept': 'text/html,'
                      'application/xhtml+xml,'
                      'application/xml;q=0.9,'
                      'image/avif,'
                      'image/webp,'
                      'image/apng,'
                      '*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.params = (
            ('code', str(company_code)),
            ('page', str(page_num)),
        )
        self.url = f'https://finance.naver.com/item/frgn.nhn'
        self.content_type = 'text/html'


async def async_req(method, url, proxy_on=True, my_session=None, content_type='', **request_kwargs):
    my_session = my_session if my_session else aiohttp.ClientSession

    retry = 0
    while True:
        try:
            if 0 < retry:
                # proxy_on = True  # proxy 사용하지 않고 크롤링 중, 재시도 요청이 들어가면 프록시를 사용하도록 전환
                if retry % 10 == 0:  # 100번의 재시도마다 로그 찍기
                    # logger.info(f""
                    #             f"retry num is {retry} "
                    #             f"\n\tmethod: {method}"
                    #             f"\n\turl: {url}"
                    #             f"\n\trequest_kwargs: {request_kwargs}"
                    #             f"")
                    if 50 <= retry:  # 1000번 넘는 재시도일때는 예외처리 되지 않은 응답을 받은 것으로 판단하고 중지
                        return None

            if proxy_on:
                proxy_url = self.https_proxy_url()
                connector = {'connector': ProxyConnector.from_url(proxy_url)}
            else:
                proxy_url = ''
                connector = {}
            logger.info('{} {}'.format(proxy_url, url))

            connector = {}

            retry += 1
            async with my_session(**connector) as session:
                request_kwargs['timeout'] = 60
                async with getattr(session, method)(url=url, **request_kwargs) as res:
                    if content_type == 'text/html':
                        content = await res.text()
                    elif content_type == 'json':
                        content = await res.json()
                    else:
                        content = await res.read()
            return res, content

        except Exception as e:
            return e
            # _continue = self._handle_exception(e)
            # if _continue:  # retry with another proxy(invalid proxy)
            #     self._set_proxy()
            #     continue
            #
            # return None  # fail to got response

        # else:  # got response
        #     _continue = self._handle_response(res)
        #     if _continue:
        #         self._set_proxy()
        #         continue  # retry with another proxy(invalid proxy)
        #
        #     return res  # success, good job!


if __name__ == '__main__':
    # req_info = ItemSiseDay('035720', 1)  # 카카오
    req_info = ItemFrgn('035720', 1)
    res, content = asyncio.run(
        async_req(
            req_info.method,
            req_info.url,
            content_type=req_info.content_type,
            headers=req_info.headers,
            params=req_info.params,
        )
    )
    df = pd.read_html(content)
    pass
