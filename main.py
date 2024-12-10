import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_headers():
    """HTTP 요청에 사용할 헤더를 반환합니다."""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

def get_job_urls(url, filters):
    """주어진 URL에서 채용 공고의 URL을 추출합니다."""
    job_urls = []
    page = 1

    while True:
        filters['pageIndex'] = page
        response = requests.post(url, headers=get_headers(), data=filters)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='brd_list_n')
        
        if table is None:
            print("채용공고 테이블을 찾을 수 없습니다.")
            break
        
        rows = table.find_all('tr')[1:]
        if not rows:
            print(f"페이지 {page}에 데이터가 없습니다. 종료합니다.")
            break
        
        for row in rows:
            link_tag = row.find('td').find('a')
            if link_tag and 'href' in link_tag.attrs:
                full_url = requests.compat.urljoin('https://work.mma.go.kr', link_tag['href'])
                job_urls.append(full_url)
        
        if not soup.find('a', string=str(page + 1)):
            print("더 이상 페이지가 없습니다. 종료합니다.")
            break
        
        page += 1

    return job_urls

def get_text(soup, th_text):
    """주어진 th_text에 해당하는 td의 텍스트를 안전하게 반환합니다."""
    th = soup.find('th', string=th_text)
    return th.find_next_sibling('td').get_text(strip=True) if th else '정보 없음'

def extract_job_details(job_urls):
    """채용 공고의 세부 정보를 추출하여 CSV 파일로 저장합니다."""
    csv_headers = [
        "Index", "채용공고", "등록일자", "업체명", "업종", "전화번호", "주소", "홈페이지",
        "요원형태", "고용형태", "자격요원", "급여조건", "최종학력", "전공계열", "담당업무",
        "근무형태", "출퇴근시간", "특근·잔업", "교대근무", "수습기간", "군사훈련교육 소집기간 급여",
        "퇴직금지급", "식사(비)지급", "현역배정인원", "현역편입인원", "보충역배정인원",
        "보충역편입인원", "모집인원", "외국어", "자격증", "복리후생", "접수기간", "접수방법",
        "담당자", "담당자 전화번호", "담당자 팩스번호", "비고"
    ]

    # 현재 시간을 기반으로 CSV 파일 이름 생성
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f'{current_time}.csv'

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)  # 헤더 작성
        
        for idx, job_url in enumerate(job_urls, start=1):
            response = requests.get(job_url, headers=get_headers())
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 세부 정보 추출
            job_details = [idx]  # Index 추가
            job_details.extend(get_text(soup, header) for header in csv_headers[1:])  # 나머지 세부 정보 추가
            
            writer.writerow(job_details)  # 세부 정보 작성

def main():
    url = 'https://work.mma.go.kr/caisBYIS/search/cygonggogeomsaek.do'
    filters = {
        'eopjong_gbcd': '1',
        'eopjong_gbcd_list': '11111,11112',
        'yeokjong_brcd': '002',
    }
    
    job_urls = get_job_urls(url, filters)  # 채용 공고 URL 추출
    extract_job_details(job_urls)  # 세부 정보 추출 및 CSV 저장

if __name__ == "__main__":
    main()