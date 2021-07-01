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

