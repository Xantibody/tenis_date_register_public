from tenis_date_register.services.request_service import RequestService

def test_fetch_html():
    requestService = RequestService()
    html = requestService.fetch_html()
    with open('tests/test_data/test.html', mode='w',  encoding='utf-8') as f:
        f.write(html)
    assert html, 'successful'