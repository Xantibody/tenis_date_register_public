from tenis_date_register.services.register_data_service import RegisterDataService

def test_create_register_datas():
    html = ''
    with open('tests/test_data/test.html', 'r',  encoding='utf-8') as f:
        html = f.read()
    registerDataService = RegisterDataService()
    registerDataService.create_register_datas(html)