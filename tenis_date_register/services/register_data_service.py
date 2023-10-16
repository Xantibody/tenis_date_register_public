from typing import Any
from tenis_date_register.data.register_date import RegisterDateData
from bs4 import BeautifulSoup
import datetime
import re
from tenis_date_register.logger import MyLogger


logger = MyLogger.setup(__name__)

class RegisterDataService:
    def create_register_datas(self, html: str)->list[RegisterDateData]:
        try:
            logger.info('登録リスト作成 開始')
            soup = BeautifulSoup(html, 'html.parser')
            elems = soup.select('[summary=予約一覧] tbody tr')
            register_Dates = []

            for elem in elems:
                if self._is_cancel_court(elem):
                    logger.debug('title=%s：ステータスがキャンセルのため取り込み対象外', self._parse_title(elem))
                    continue
                
                title = self._parse_title(elem)
                logger.debug('title=%s',title)

                date = self._parse_date(elem)
                logger.debug('date=%s',date)

                times = self._pase_times(elem)
                logger.debug('times=%s',times)

                start_datetime = self._create_register_datetime(date, times[0])
                logger.debug('start_datetime=%s', start_datetime)

                end_datetime = self._create_register_datetime(date, times[1])
                logger.debug('end_datetime=%s', end_datetime)

                register_Dates.append(self._create_register_data(title, start_datetime, end_datetime))
            logger.info('登録リスト作成 終了')
            return register_Dates

        except Exception as e:
            logger.exception('exception:%s', e)
            raise

    def _is_cancel_court(self, elem)->bool:
        raw_status = elem.select('.status')[0].get_text(strip=True)
        status = re.sub('\n', '', raw_status)
        return status == 'キャンセル'

    def _parse_title(self,elem)->str:
        raw_facility = elem.select('th')[0].get_text(strip=True)
        facility = re.sub('\n', '', raw_facility)
        raw_court = elem.select('td')[0].get_text(strip=True)
        court = re.sub('\n', '', raw_court).replace('テニスコート','')
        return f'テニス：{facility}（{court}）'

    def _parse_date(self, elem)->datetime:
        str = elem.select('td')[1].get_text(strip=True)
        str_sub = re.sub('\（\S\）','',str)
        date = datetime.datetime.strptime(str_sub ,'%Y年%m月%d日')
        return date

    def _pase_times(self, elem) -> list:
        raw_times = elem.select('td')[2].get_text(strip=True)
        times = re.sub('\n', '', raw_times)
        return times.split('～')
        
        
    def _create_register_data(self, title: str, start_datetime:datetime, end_datetime:datetime)-> RegisterDateData: 
        return RegisterDateData(
            title=title,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )
    
    def _create_register_datetime(self, date:datetime, time:str)->datetime:
        split_time = time.split(':')
        hour = int(split_time[0])
        minute = int(split_time[1])
        return date.replace(hour=hour, minute=minute)