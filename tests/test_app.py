from app import app

def test_index():
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200

def test_tts_no_text():
    tester = app.test_client()
    response = tester.post('/tts', json={})
    assert response.status_code == 400
