import os
from datetime import datetime
from functools import reduce
from urllib.parse import urlencode
from xml.etree.ElementTree import parse

import pandas as pd

from src.modules.func_etc import ReqBase, Func

abspath, dn, jn = os.path.abspath, os.path.dirname, os.path.join


class DartAPI:
    PATH_DATA_ROOT = jn(dn(dn(dn(abspath(__file__)))), 'data')

    try:
        path_api_key = jn(jn(dn(dn(dn(abspath(__file__)))), 'ignore'), 'dart_api_key')
        with open(path_api_key, 'r') as f:
            API_KEY = f.read().strip()
    except Exception as e:
        print(e)
        exit()

    @property
    def dir_path(self):
        dir_path = jn(self.PATH_DATA_ROOT, self.__class__.__name__)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path


class CorpCode(ReqBase, DartAPI):
    """
    https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018

    공시정보

    기본 정보
    메서드	요청URL	인코딩	출력포멧
    GET	https://opendart.fss.or.kr/api/corpCode.xml	UTF-8	Zip FILE (binary)

    요청 인자
    키	명칭	타입	필수여부	값설명
    crtfc_key	API 인증키	STRING(40)	Y	발급받은 인증키(40자리)

    응답 결과
    키	명칭	List 여부	출력설명
    status	에러 및 정보 코드		(※메시지 설명 참조)
    message	에러 및 정보 메시지		(※메시지 설명 참조)
    corp_code	고유번호	Y	공시대상회사의 고유번호(8자리)
    ※ ZIP File 안에 있는 XML파일 정보
    corp_name	정식명칭	Y	정식회사명칭
    ※ ZIP File 안에 있는 XML파일 정보
    stock_code	종목코드	Y	상장회사인 경우 주식의 종목코드(6자리)
    ※ ZIP File 안에 있는 XML파일 정보
    modify_date	최종변경일자	Y	기업개황정보 최종변경일자(YYYYMMDD)
    ※ ZIP File 안에 있는 XML파일 정보

    OpenAPI 테스트
    출력포멧이 Zip FILE (binary)인 경우 브라우저 테스트를 제공하지 않습니다.
    출력포멧Zip FILE (binary)
    요청인자API 인증키*xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    메시지 설명
    - 000 :정상
    - 010 :등록되지 않은 키입니다.
    - 011 :사용할 수 없는 키입니다. 오픈API에 등록되었으나, 일시적으로 사용 중지된 키를 통하여 검색하는 경우 발생합니다.
    - 020 :요청 제한을 초과하였습니다.
    일반적으로는 10,000건 이상의 요청에 대하여 이 에러 메시지가 발생되나, 요청 제한이 다르게 설정된 경우에는 이에 준하여 발생됩니다.
    - 100 :필드의 부적절한 값입니다. 필드 설명에 없는 값을 사용한 경우에 발생하는 메시지입니다.
    - 800 :원활한 공시서비스를 위하여 오픈API 서비스가 중지 중입니다.
    - 900 :정의되지 않은 오류가 발생하였습니다.
    """
    method = 'get'
    url = 'https://opendart.fss.or.kr/api/corpCode.xml'

    _res_code_msg = {
        '000': '정상',
        '010': '등록되지 않은 키입니다.',
        '011': '사용할 수 없는 키입니다. 오픈API에 등록되었으나, '
               '일시적으로 사용 중지된 키를 통하여 검색하는 경우 발생합니다.',
        '020': '요청 제한을 초과하였습니다. '
               '일반적으로는 10,000건 이상의 요청에 대하여 이 에러 메시지가 발생되나, '
               '요청 제한이 다르게 설정된 경우에는 이에 준하여 발생됩니다.',
        '100': '필드의 부적절한 값입니다. 필드 설명에 없는 값을 사용한 경우에 발생하는 메시지입니다.',
        '800': '원활한 공시서비스를 위하여 오픈API 서비스가 중지 중입니다.',
        '900': '정의되지 않은 오류가 발생하였습니다.',
    }
    _error_code = '99999'
    _res_code_msg.update({
        _error_code: 'Request Error - not api response code'  # my error
    })

    def __init__(self):
        super().__init__()
        self.filename = None

    @property
    def req_kwargs(self):
        return {
            'params': (
                ('crtfc_key', str(self.API_KEY)),
            ),
            'stream': True,
        }

    def is_valid(self, res, save=True):
        res.raise_for_status()

        res_code = getattr(res, 'status_code', False) or getattr(res, 'status', False)  # requests or aiohttp
        if not res_code:
            res_code = self._error_code

        try:
            msg = self._res_code_msg[str(res_code)]
            print(msg)
            return False
        except KeyError:
            self.set_res(res)
            if save:
                self.filename = f'{datetime.now().strftime("%y%d%m%H%M%S")}.{urlencode(self.req_kwargs)}'
                Func.save_zip(res.content, self.dir_path, self.filename)
            return True

    @classmethod
    def get_data_path(cls):
        # find recent date(dir name)

        path_data_dir = jn(DartAPI.PATH_DATA_ROOT, cls.__name__)
        data_dir_name = reduce(
            lambda a, b: a if int(a.split('.')[0]) > int(b.split('.')[0]) else b,
            os.listdir(path_data_dir)
        )  # latest data crawled
        file_path = jn(jn(path_data_dir, data_dir_name), 'CORPCODE.XML')

        return file_path

    @classmethod
    def gen_data(cls, xml=False, has_stock_code=True):
        file_path = cls.get_data_path()
        if file_path:
            # xml parsing
            tree = parse(file_path)
            for li in tree.getroot().findall('list'):
                try:
                    if has_stock_code and not li.find("stock_code").text.strip():
                        continue

                    if xml:
                        yield li
                    else:
                        yield (
                            li.find("corp_code").text.strip(),
                            li.find("corp_name").text.strip(),
                            li.find("stock_code").text.strip(),
                            li.find("modify_date").text.strip(),
                        )
                except Exception as e:
                    print(f'{e}')

    @classmethod
    def data_frame(cls, has_stock_code=True):
        columns = [
            "corp_code",
            "corp_name",
            "stock_code",
            "modify_date",
        ]
        return pd.DataFrame([i for i in cls.gen_data(has_stock_code=has_stock_code)], columns=columns)


class FnlttMultiAcnt(ReqBase, DartAPI):
    """상장기업 재무정보
        홈개발가이드상장기업 재무정보다중회사 주요계정
        다중회사 주요계정 개발가이드

        기본 정보
        메서드	요청URL	인코딩	출력포멧
        GET	https://opendart.fss.or.kr/api/fnlttMultiAcnt.json	UTF-8	JSON
        GET	https://opendart.fss.or.kr/api/fnlttMultiAcnt.xml	UTF-8	XML
        요청 인자
        키	명칭	타입	필수여부	값설명
        crtfc_key	API 인증키	STRING(40)	Y	발급받은 인증키(40자리)
        corp_code	고유번호	STRING(8)	Y	공시대상회사의 고유번호(8자리)
        ※ 개발가이드 > 공시정보 > 고유번호 API조회 가능
        bsns_year	사업연도	STRING(4)	Y	사업연도(4자리)
        ※ 2015년 이후 부터 정보제공
        reprt_code	보고서 코드	STRING(5)	Y	1분기보고서 : 11013
        반기보고서 : 11012
        3분기보고서 : 11014
        사업보고서 : 11011
        응답 결과
        키	명칭	List 여부	출력설명
        status	에러 및 정보 코드		(※메시지 설명 참조)
        message	에러 및 정보 메시지		(※메시지 설명 참조)
        rcept_no	접수번호	Y	접수번호(14자리)

        ※ 공시뷰어 연결에 이용예시
        - PC용 : http://dart.fss.or.kr/dsaf001/main.do?rcpNo=접수번호
        - 모바일용 : http://m.dart.fss.or.kr/html_mdart/MD1007.html?rcpNo=접수번호
        bsns_year	사업 연도	Y	사업연도(4자리)
        stock_code	종목 코드	Y	상장회사의 종목코드(6자리)
        reprt_code	보고서 코드	Y	1분기보고서 : 11013
        반기보고서 : 11012
        3분기보고서 : 11014
        사업보고서 : 11011
        account_nm	계정명	Y	ex) 자본총계
        fs_div	개별/연결구분	Y	CFS:연결재무제표, OFS:재무제표
        fs_nm	개별/연결명	Y	ex) 연결재무제표 또는 재무제표 출력
        sj_div	재무제표구분	Y	BS:재무상태표, IS:손익계산서
        sj_nm	재무제표명	Y	ex) 재무상태표 또는 손익계산서 출력
        thstrm_nm	당기명	Y	ex) 제 13 기 3분기말
        thstrm_dt	당기일자	Y	ex) 2018.09.30 현재
        thstrm_amount	당기금액	Y	9,999,999,999
        thstrm_add_amount	당기누적금액	Y	9,999,999,999
        frmtrm_nm	전기명	Y	ex) 제 12 기말
        frmtrm_dt	전기일자	Y	ex) 2017.01.01 ~ 2017.12.31
        frmtrm_amount	전기금액	Y	9,999,999,999
        frmtrm_add_amount	전기누적금액	Y	9,999,999,999
        bfefrmtrm_nm	전전기명	Y	ex) 제 11 기말(※ 사업보고서의 경우에만 출력)
        bfefrmtrm_dt	전전기일자	Y	ex) 2016.12.31 현재(※ 사업보고서의 경우에만 출력)
        bfefrmtrm_amount	전전기금액	Y	9,999,999,999(※ 사업보고서의 경우에만 출력)
        ord	계정과목 정렬순서	Y	계정과목 정렬순서
    """
    method = 'get'
    url = 'https://opendart.fss.or.kr/api/fnlttMultiAcnt.json'

    _res_code_msg = {
        '000': '정상',
        '010': '등록되지 않은 키입니다.',
        '011': '사용할 수 없는 키입니다. '
               '오픈API에 등록되었으나, 일시적으로 사용 중지된 키를 통하여 검색하는 경우 발생합니다.',
        '020': '요청 제한을 초과하였습니다. '
               '일반적으로는 10,000건 이상의 요청에 대하여 이 에러 메시지가 발생되나, '
               '요청 제한이 다르게 설정된 경우에는 이에 준하여 발생됩니다.',
        '100': '필드의 부적절한 값입니다. 필드 설명에 없는 값을 사용한 경우에 발생하는 메시지입니다.',
        '800': '원활한 공시서비스를 위하여 오픈API 서비스가 중지 중입니다.',
        '900': '정의되지 않은 오류가 발생하였습니다.',
    }
    _error_code = '99999'
    _res_code_msg.update({
        _error_code: 'Request Error - not api response code'  # my error
    })
    _reprt_code_tu = (
        11013,  # 1분기보고서
        11012,  # 반기보고서
        11014,  # 3분기보고서
        11011,  # 사업보고서
    )

    def __init__(self, bsns_year, reprt_code_idx, *corp_code):
        super().__init__()
        self.filename = None

        self.bsns_year = bsns_year  # min 2015 max now
        self.reprt_code = self._reprt_code_tu[reprt_code_idx]  # 0 ~ 3
        self.corp_code_list = corp_code  # max 500

    @property
    def req_kwargs(self):
        return {
            'params': (
                ('crtfc_key', str(self.API_KEY)),
                ('corp_code', str(','.join(self.corp_code_list))),
                ('bsns_year', str(self.bsns_year)),
                ('reprt_code', str(self.reprt_code)),
            ),
        }

    # def is_valid(self, res, save=True):
    #     res.raise_for_status()
    #
    #     res_code = getattr(res, 'status_code', False) or getattr(res, 'status', False)  # requests or aiohttp
    #     if not res_code:
    #         res_code = self._error_code
    #
    #     try:
    #         msg = self._res_code_msg[str(res_code)]
    #         print(msg)
    #         return False
    #     except KeyError:
    #         self.set_res(res)
    #         if save:
    #             self.filename = f'{datetime.now().strftime("%y%d%m%H%M%S")}.{urlencode(self.req_kwargs)}'
    #             Func.save_zip(res.content, self.dir_path, self.filename)
    #         return True


class ApiList(ReqBase, DartAPI):
    method = 'get'
    url = 'https://opendart.fss.or.kr/api/list.json'

    _res_code_msg = {
    }
    _error_code = '99999'
    _res_code_msg.update({
        _error_code: 'Request Error - not api response code'  # my error
    })

    def __init__(self):
        super().__init__()
        self.filename = None
        self.corp_code = '00126380'
        self.page_no = '1'


    @property
    def req_kwargs(self):
        return {
            'params': (
                ('crtfc_key', str(self.API_KEY)),
                # ('corp_code', str(self.corp_code)),
                ('bgn_de', str(20210101)),
                ('end_de', str(20210401)),
                ('last_reprt_at', str('Y')),
                ('pblntf_ty', str('A')),
                # ('pblntf_detail_ty', str('')),
                ('corp_cls', str('Y')),
                # ('sortsort', str('')),
                # ('sort_mth', str()),
                ('page_no', str(self.page_no)),
                ('page_count', str(100)),
            ),
        }

    def is_valid(self, res):
        pass



if __name__ == '__main__':
    import requests

    '''상장회사 정보'''
    # cc = CorpCode()
    # res = requests.get(cc.url, **cc.req_kwargs)
    # cc_is_valid = cc.is_valid(res)

    # cc_gen = CorpCode.gen_data()
    # for data in cc_gen:
    #     print(data)

    # df_has_sc = CorpCode.data_frame(has_stock_code=True)
    # df_all = CorpCode.data_frame(has_stock_code=False)

    '''재무재표(복수 기업 가능)'''
    # x = 1
    # df_cc = CorpCode.data_frame(has_stock_code=True)
    # li_corpcode = [_ for _ in zip(df_cc['corp_name'], df_cc['corp_code'], df_cc['modify_date'], df_cc['stock_code'])]
    # for i in range((len(li_corpcode) // x) + 1):
    #     b = li_corpcode[i * x: (i + 1) * x]
    #     fma = FnlttMultiAcnt(2020, 0, *b)
    #     res = requests.get(fma.url, **fma.req_kwargs)
    #     fma_is_valid = fma.is_valid(res)
    #     print(1)

    '''공시 검색'''
    al = ApiList()
    res = requests.get(al.url, **al.req_kwargs)
    cc_is_valid = al.is_valid(res)

    print(1)
