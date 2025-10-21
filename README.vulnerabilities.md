# Vulnerabilities in Vulnerable.Python
_(Intentionally insecure for scanner testing. Do not deploy.)_

## 1) Hardcoded API key
- **Where:** `Vulnerable.Python/app.py` — `WEATHER_KEY = '...'`
- **CWE:** CWE-798
- **OWASP:** A02 – Cryptographic Failures

## 2) TLS verification disabled
- **Where:** `app.py` — `requests.get(..., verify=False)`
- **CWE:** CWE-295
- **OWASP:** A02 – Cryptographic Failures
- **Fix:** Remove `verify=False` or provide trusted CA bundle/pinning.

## 3) SQL injection via string formatting
- **Where:** `app.py`, `/weather` — `cur.execute("INSERT ... '%s' '%s'" % (zip, body))`
- **CWE:** CWE-89
- **OWASP:** A03 – Injection
- **Fix:** Use parameterized queries (`?` placeholders).

## 4) Command execution with user input
- **Where:** `app.py` — `subprocess.check_output(f'echo fetched {zip}', shell=True)`
- **CWE:** CWE-78
- **OWASP:** A03 – Injection
- **Fix:** Avoid `shell=True`; use argument lists or remove shell step.

## 5) Weak cryptography (MD5)
- **Where:** `app.py` — `hashlib.md5(zip.encode(...))`
- **CWE:** CWE-327
- **OWASP:** A02 – Cryptographic Failures

## 6) Insecure deserialization
- **Where:** `app.py`, `/deserialize` — `pickle.loads(data)`
- **CWE:** CWE-502
- **OWASP:** A08 – Software and Data Integrity Failures
- **Fix:** Avoid pickle for untrusted data; use JSON and schema validation.

## 7) Outdated/vulnerable dependencies
- **Where:** `requirements.txt`
  - `Flask==1.1.2`
  - `requests==2.20.0`
  - `pysqlite3==0.4.6`
- **CWE:** CWE-1104
- **OWASP:** A06 – Vulnerable and Outdated Components
- **Fix:** Upgrade pinned versions; run SCA.
