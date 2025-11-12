import requests
import json
import datetime

# CISA가 공식적으로 제공하는 KEV JSON 데이터 주소
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# 저장할 HTML 파일 이름
SAVE_FILENAME = "kev_report.html"

def fetch_and_save_as_html():
    try:
        # 1. CISA 서버에서 최신 KEV JSON 데이터를 가져옵니다.
        print(f"'{KEV_URL}'에서 최신 KEV 데이터를 다운로드합니다...")
        response = requests.get(KEV_URL)
        response.raise_for_status()  # 오류가 있으면 예외 발생
        
        data = response.json()
        vulnerabilities = data.get('vulnerabilities', [])
        
        # 2. '목록에 추가된 날짜(dateAdded)'를 기준으로 최신순 정렬 (내림차순)
        print("데이터를 최신순으로 정렬합니다...")
        vulnerabilities_sorted = sorted(
            vulnerabilities, 
            key=lambda x: x['dateAdded'], 
            reverse=True
        )
        
        # 3. 저장할 HTML 내용 (문자열) 생성 시작
        print("HTML 리포트를 생성합니다...")
        
        # 현재 시간 타임스탬프
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # HTML 헤더 및 스타일
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>CISA KEV 최신 보고서</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 20px; }}
        h1 {{ color: #b91c1c; }}
        p {{ font-size: 1.1em; background-color: #f4f4f4; padding: 10px; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #333; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>CISA 알려진 악용 취약점(KEV) 보고서</h1>
    <p>
        <strong>보고서 생성 시각:</strong> {now}<br>
        <strong>총 취약점 개수:</strong> {data['count']}
    </p>
    
    <table id="kev-table">
        <thead>
            <tr>
                <th>추가일 (최신순)</th>
                <th>CVE ID</th>
                <th>취약점 이름</th>
                <th>제품</th>
                <th>제조사</th>
                <th>조치 기한</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # 4. 정렬된 데이터를 HTML 테이블 행(row)으로 추가
        for vuln in vulnerabilities_sorted:
            tr = f"""
            <tr>
                <td>{vuln.get('dateAdded', 'N/A')}</td>
                <td><strong>{vuln.get('cveID', 'N/A')}</strong></td>
                <td>{vuln.get('vulnerabilityName', 'N/A')}</td>
                <td>{vuln.get('product', 'N/A')}</td>
                <td>{vuln.get('vendorProject', 'N/A')}</td>
                <td>{vuln.get('dueDate', 'N/A')}</td>
            </tr>
"""
            html_content += tr
            
        # 5. HTML 태그 닫기
        html_content += """
        </tbody>
    </table>
</body>
</html>
"""
        
        # 6. 완성된 HTML 문자열을 파일로 저장
        with open(SAVE_FILENAME, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"\n✅ 성공! 전체 {data['count']}개의 취약점 목록을 '{SAVE_FILENAME}' 파일로 저장했습니다.")
        print(f"'{SAVE_FILENAME}' 파일을 브라우저로 열어 확인하세요.")

    except Exception as e:
        print(f"❌ 작업 실패: {e}")

# --- 스크립트 실행 ---
fetch_and_save_as_html()