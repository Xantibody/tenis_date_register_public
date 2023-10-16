import requests
from bs4 import BeautifulSoup
from tenis_date_register.logger import MyLogger
from tenis_date_register.services.util_service import UtilService


logger = MyLogger.setup(__name__)
conf = UtilService.create_conf()

class RequestService:
    def fetch_html(self):
        logger.info('コート一覧html取得 開始')
        try:
            url = conf.get('request','URL')
            csrf_req = requests.get(url)
            soup = BeautifulSoup(csrf_req.text, 'html.parser')
            csrf = soup.find(attrs={'name':'csrf'}).get('value')
            data = {
                'no':conf.get('hachioji', 'no'),
                'password':conf.get('hachioji', 'password'),
                'location':'%2Freserve%2F',
                'csrf':csrf
                }
            cookie = csrf_req.cookies

            login_ses = requests.session()
            html = login_ses.post(url, data=data, cookies=cookie)
            if not html.status_code == requests.codes.ok:
                raise Exception('ログイン失敗')
            
            logger.info('コート一覧html取得 終了')
            return html.text

        except Exception as e:
            logger.exception('exception:%s', e)
            raise