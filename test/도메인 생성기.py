import base64
import hashlib  # 해시 라이브러리 import
import secrets  # 랜덤 솔트 생성을 위한 모듈

def generate_short_code(input_string: str, salt: str) -> str:
    """
    입력 문자열과 솔트(salt)를 결합하여 SHA-256 해시로 뒤섞은 다음,
    그 해시 결과를 Base64로 인코딩하여 6자리를 반환합니다.
    """
    
    # 1. 솔트와 입력 문자열을 결합
    combined_string = salt + input_string
    
    # 2. 결합된 문자열을 SHA-256 해시로 완전히 뒤섞습니다.
    hasher = hashlib.sha256()
    hasher.update(combined_string.encode('utf-8'))
    
    # 3. 뒤섞인 결과(해시)를 바이트(bytes)로 가져옵니다.
    hashed_bytes = hasher.digest()
    
    # 4. '해시 결과'를 Base64로 인코딩합니다.
    encoded_bytes = base64.urlsafe_b64encode(hashed_bytes)
    
    # 5. 바이트를 문자열로 변환합니다.
    encoded_string = encoded_bytes.decode('utf-8')
    
    # 6. Base64 문자열의 앞 6자리를 반환합니다.
    return encoded_string[:6]

my_salt = secrets.token_hex(16) # 32자리 랜덤 솔트 생성

# --- 메인 코드 실행 ---

# 1. 사용자에게 'test'와 같은 서브도메인 부분을 입력받습니다.
subdomain_part = input("코드로 만들 서브도메인 (예: test)을 입력하세요: ")

# 2. 사용자에게 'itforest.net'과 같은 메인 도메인 부분을 입력받습니다.
main_domain_part = input("연결할 메인 도메인 (예: itforest.net)을 입력하세요: ")

# 3. 함수를 호출하여 코드를 생성합니다.
short_code = generate_short_code(subdomain_part, my_salt)

# 4. 두 문자열을 합쳐 최종 결과물을 만듭니다.
final_domain = f"{short_code}.{main_domain_part}"

# 5. 결과를 출력합니다.
print("---" * 10)
print(f"입력된 서브도메인: {subdomain_part}")
print(f"입력된 메인 도메인: {main_domain_part}")
print(f"적용된 *랜덤* 솔트: {my_salt}")
print(f"생성된 6자리 코드: {short_code}")
print(f"최종 생성된 도메인: {final_domain}")