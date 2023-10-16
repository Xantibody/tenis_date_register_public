import pytest
from release_date_crawler.data.release_date import ReleaseDateData
from release_date_crawler.services.calendar_register_service import CalendarRegisterService
import datetime

def test_register():
    today = datetime.date.today()
    tomorrow =  datetime.datetime.now() + datetime.timedelta(days = 1)
    tomorrow = tomorrow.date()
    release_datas = [ReleaseDateData(title="テスト1", release_date=today), ReleaseDateData(title="テスト2", release_date=tomorrow)]
    CalendarRegisterService.register_calender(CalendarRegisterService, release_datas)