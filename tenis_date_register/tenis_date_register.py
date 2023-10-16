from tenis_date_register.services.request_service import RequestService
from tenis_date_register.services.register_data_service import RegisterDataService
from tenis_date_register.services.calendar_register_service import CalendarRegisterService
from tenis_date_register.logger import MyLogger


logger = MyLogger.setup(__name__)

def main():
    try:
        request_service = RequestService()
        html = request_service.fetch_html()
        
        register_data_service = RegisterDataService()
        register_datas = register_data_service.create_register_datas(html)
        
        calendar_register_service = CalendarRegisterService()
        calendar_register_service.register_calender(register_datas)

    except Exception as e:
        logger.exception('exception:%s', e)

##登録済みの予定を登録しないように調整する