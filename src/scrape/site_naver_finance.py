__all__ = [
    'ReqBase',
    'ItemSiseDay',
    'ItemFrgn',
]


class ReqBase:
    method: str = None
    url: str = None

    class ReqBaseException:
        pass

    def __init__(self):
        self._res = None

    @property
    def req_kwargs(self):
        raise Exception('req_kwargs() is not defined')

    def is_valid(self, res):
        raise Exception('is_valid() is not defined')

    def set_res(self, res):
        self._res = res


class ItemSiseDay(ReqBase):
    method = 'get'
    url = f'https://finance.naver.com/item/sise_day.nhn'

    def __init__(self, company_code, page_num):
        company_code: int or str
        page_num: int or str

        super().__init__()

        self.company_code = company_code
        self.page_num = page_num

    @property
    def req_kwargs(self):
        return {
            'headers': {
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
            },
            'params': (
                ('code', str(self.company_code)),
                ('page', str(self.page_num)),
            ),
        }


class ItemFrgn(ReqBase):
    method = 'get'
    url = f'https://finance.naver.com/item/frgn.nhn'

    def __init__(self, company_code, page_num):
        company_code: int or str
        page_num: int or str

        super().__init__()

        self.company_code = company_code
        self.page_num = page_num

    @property
    def req_kwargs(self):
        return {
            'headers': {
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
            },
            'params': (
                ('code', str(self.company_code)),
                ('page', str(self.page_num)),
            ),
        }

    def is_valid(self, res):
        res.raise_for_status()
        self.set_res(res)
        return True


if __name__ == '__main__':
    # req_info = ItemSiseDay('035720', 1)  # 카카오
    req_info = ItemFrgn('035720', 1)

    pass
