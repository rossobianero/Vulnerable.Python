# tests/test_weather.py
import os
import sys

# Ensure the project root (where app.py lives) is importable,
# regardless of where pytest is invoked from.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from app import app, get_db
import sqlite3
import json

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Run the app in testing mode
    app.config['TESTING'] = True

    # Force the working directory to the temp path so the sqlite file is created there
    monkeypatch.chdir(tmp_path)

    with app.test_client() as client:
        yield client

def test_weather_stores_and_returns_md5(client):
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
