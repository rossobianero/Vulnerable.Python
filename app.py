from flask import Flask, request, jsonify
import sqlite3, requests, hashlib, pickle, subprocess
app=Flask(__name__)
KEY='OWM_PY_KEY'
def get_db(): conn=sqlite3.connect('vuln_py.db'); conn.execute('CREATE TABLE IF NOT EXISTS weather (id INTEGER PRIMARY KEY, zip TEXT, payload TEXT)'); return conn
@app.route('/weather') def weather(): zip=request.args.get('zip',''); url=f'https://api.openweathermap.org/data/2.5/weather?zip={zip}&appid={KEY}'; 
    try: resp=requests.get(url,verify=False,timeout=5); body=resp.text
    except: body='{"error":"fetch failed"}'
    conn=get_db(); cur=conn.cursor(); cur.execute("INSERT INTO weather (zip,payload) VALUES ('%s','%s')" % (zip, body.replace("'","''"))); conn.commit(); conn.close()
    try: subprocess.check_output(f'echo fetched {zip}', shell=True)
    except: pass
    md5=hashlib.md5(zip.encode('utf-8')).hexdigest(); return jsonify({'zip':zip,'md5':md5,'stored':True})
@app.route('/deserialize', methods=['POST']) def deserial(): data=request.get_data(); try: obj=pickle.loads(data); return jsonify({'type':type(obj).__name__}); except Exception as e: return jsonify({'error':str(e)}),400
if __name__=='__main__': app.run(host='0.0.0.0',port=5001)
