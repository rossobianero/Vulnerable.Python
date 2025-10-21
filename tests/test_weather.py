import pytest
from app import app, get_db
import sqlite3, os, json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_weather_stores_and_returns_md5(client, tmp_path):
    # use temp DB file
    db_path = tmp_path / "vuln_py.db"
    # set working dir so sqlite file is created in tmp
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        resp = client.get('/weather?zip=10001')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['zip'] == '10001'
        assert 'md5' in data and len(data['md5']) > 0
        # verify DB row exists
        conn = sqlite3.connect('vuln_py.db')
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM weather WHERE zip='10001'")
        c = cur.fetchone()[0]
        conn.close()
        assert c >= 1
    finally:
        os.chdir(cwd)
