import googleapiclient.discovery
import google.auth
from tenis_date_register.logger import MyLogger
from tenis_date_register.data.register_date import RegisterDateData
from tenis_date_register.services.util_service import UtilService

logger = MyLogger.setup(__name__)
conf = UtilService.create_conf()

class CalendarRegisterService:
    def register_calender(self, release_dates:list[RegisterDateData]):
        try:
            logger.info('カレンダー登録 開始')
            if len(release_dates) == 0:
                logger.info('カレンダー登録データなし')

            else:
                service = self._create_calendar_service()
                events = self._create_events(release_dates)
                for event in events:
                    registered_event = self._fetch_registered_event(service, event)
                    if (self._is_event_registered(event['summary'], registered_event)):
                        logger.debug('event[summary]=%s は登録済みのためスキップします', event['summary'])
                        continue
                    
                    else:
                        service.events().insert(calendarId=conf.get('google', 'calendar_id'), body=event).execute()
                        logger.debug('event=%s', event)

        except Exception as e:
             logger.exception('exception:%s', e)
             raise
        
        else:    
            logger.info('カレンダー登録 終了')


    def _create_calendar_service(self):
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            creds = google.auth.load_credentials_from_file('tenis_date_register/config/credentials.json', SCOPES)[0]
            service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
            return service


    def _create_events(self, release_dates:list[RegisterDateData]):
        events = []
        for release_data in release_dates:
            event = {
                'summary': release_data.title,
                'start': {
                    'dateTime': release_data.start_datetime.isoformat() + '+09:00',
                },
                'end': {
                   'dateTime': release_data.end_datetime.isoformat() + '+09:00',
                },
            }
            events.append(event)
        return events
    
    def _fetch_registered_event(self, service, event)->dict:
        return service.events().list(
        calendarId=conf.get('google', 'calendar_id'), 
        timeMin=event['start']['dateTime'],
        timeMax=event['end']['dateTime'],
        maxResults=10
        ).execute()

    def _is_event_registered(self, summary:str, registered_event:dict)->bool:
        if not registered_event:
            logger.debug('registered_eventが存在しません')
            return True

        for item in registered_event['items']:
            if summary == item['summary']:
                return True

        return False
    
 