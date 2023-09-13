from Config import Config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json


# Extract 클래스 생성
class Extract:
    def __init__(self, config_instance):                                # config_instance를 매개변수로 받는 초기화 메서드
        self.config = config_instance
        self.start_url = self.config.get_start_url()

        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=Service("./chromedriver"), options=chrome_options)  # 크롬 웹드라이버를 사용하여 브라우저와 연결 
        self.driver.get(self.start_url)            
        time.sleep(1)

        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        self.first_page_url, self.last_page_num = self.load_last_page()                             # 첫 번째 페이지의 URL과 마지막 페이지 번호 가져오기
        self.page_url_list = self.generate_page_urls(self.first_page_url, self.last_page_num)       # 첫 번째 페이지의 URL과 마지막 페이지 번호를 전달하여 page_url_list 생성



    # 더보기 버튼이 있는지 확인하는 메서드
    def is_more_button_exist(self):                     
        try:
            self.driver.find_element(By.CSS_SELECTOR, '#pagination > a.default')                    # CSS 선택자를 사용하여 '더보기' 버튼 찾기
            return True                                                              
        except NoSuchElementException:
            return False                                                             

    # 마지막 페이지까지 로드 후, 첫번째 페이지의 URL과 마지막 페이지 번호를 추출하는 메서드
    def load_last_page(self):
        while self.is_more_button_exist():                                                               # '더보기' 버튼이 존재하는 동안 반복
            to_more = self.driver.find_element(By.CSS_SELECTOR, '#pagination > a.default')               # '더보기' 버튼 요소 찾기
            to_more.click()
            time.sleep(1)
        pagination_link = self.driver.find_element(By.CSS_SELECTOR, '#pagination > a:nth-child(1)')      # 첫 번째 페이지 링크 요소 찾기
        first_page_url = pagination_link.get_attribute('href')                                           # 링크 URL 추출
        last_page = self.driver.find_element(By.CSS_SELECTOR, '#pagination > strong > span')             # 마지막 페이지 번호 요소 찾기
        last_page_num = last_page.text                                                                   # 마지막 페이지 번호 추출
        return first_page_url, last_page_num


    # URL 리스트를 생성하는 메서드
    def generate_page_urls(self, first_page_url, last_page_num):
        page_url_list = []
        for page_number in range(1, int(last_page_num) + 1):                                    # 첫번째 페이지부터 last_page_num까지의 페이지 번호를 순회하면서 URL 생성
            url = first_page_url.replace("currentPageNo=1", f"currentPageNo={page_number}")     # replace() 메서드를 사용하여 currentPageNo=1을 현재 페이지 번호로 치환
            page_url_list.append(url)                                                           
        return page_url_list                                                                    # 생성된 URL을 page_url_list에 저장


#-----------------------------------------------------------------------------------------


    # 공고_url_list 생성
    def bid_urls(self):
        bid_urls = []

        # 페이지 행('tr') 개수 카운트 
        for page_url in self.page_url_list:
            self.driver.get(page_url)
            num_of_tr = len(self.driver.find_elements(By.CSS_SELECTOR, 'tr'))
            print(num_of_tr)

            for index in range(0, num_of_tr):
                if index == 0:
                    continue
                try:
                    closing_text_element = self.driver.find_element(By.CSS_SELECTOR, '#resultForm > div.results > table > tbody > tr:nth-child(' + str(index) + ') > td:nth-child(10) > div') #마감
                    closing_text = closing_text_element.text
                    
                    # 공고 번호, 공고 url 추출
                    if "마감" in closing_text:
                        bid_number_element = self.driver.find_element(By.CSS_SELECTOR, '#resultForm > div.results > table > tbody > tr:nth-child(' + str(index) + ') > td:nth-child(2) > div > a') #공고 번호
                        #bid_number = bid_number_element.text
                        #bid_name_element = self.driver.find_element(By.CSS_SELECTOR, '#resultForm > div.results > table > tbody > tr:nth-child(' + str(index) + ') > td:nth-child(4) > div > a') #공고명
                        #bid_name = bid_name_element.text
                        bid_url = bid_number_element.get_attribute('href')

                        bid_urls.append({
                            "page_url":  bid_url
                        })
                except NoSuchElementException:
                    print(f"Closing text element not found for index: {index}")

        return bid_urls      # 공고_url_list 


#-----------------------------------------------------------------------------------------
#container > div:nth-child(27) > table > tbody > tr > td:nth-child(5) > a                   # 일반 개찰 완료
#container > div:nth-child(27) > table > tbody > tr:nth-child(2) > td:nth-child(5) > a      # 재입찰(1), 개찰 완료(2)
#container > div:nth-child(31) > table > tbody > tr > td:nth-child(5) > a                   # "개찰 완료" 위치가 달라 에러남


    # 버튼 클릭
    def click_button(self):
        result_dict = {}

        # "개찰완료" 테이블 행('tr') 개수 카운트
        for bid_url in self.bid_urls():
            try:
                self.driver.get(bid_url["page_url"])
                opening_Tb = self.driver.find_element(By.CSS_SELECTOR, ".table_list_integrationBidResultTbl.table_list")
                number_of_tr = len(opening_Tb.find_elements(By.CSS_SELECTOR, 'tr'))
                
                for row in range(0, number_of_tr):
                    if row == 0:
                        continue
                    
                        #"개찰완료" text 클릭
                    try:
                        opening_completed = self.driver.find_element(By.CSS_SELECTOR, '#container > div:nth-child(27) > table > tbody > tr:nth-child(' + str(row) + ') > td:nth-child(5) > a')
                        opening_completed_text = opening_completed.text

                        if "개찰완료" in opening_completed_text:
                            opening_completed.click()
                            
                    except NoSuchElementException:
                        print(f"(공고명 : {bid_name_text}),'개찰완료' 요소를 찾을 수 없습니다.")
                        continue


                        # "보기" 버튼 클릭
                    try:
                        bogi = self.driver.find_element(By.CSS_SELECTOR, "#rebid > div.section > table > tbody > tr:nth-child(5) > td:nth-child(4) > div > a")
                        bogi.click()

                        # 입찰 데이터 추출
                        try:
                            # 팝업창으로 이동
                            self.driver.switch_to.window(self.driver.window_handles[1]) 

                            # "공고 번호"
                            bid_number = self.driver.find_element(By.CSS_SELECTOR, '#container > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2) > div')
                            bid_number_text = bid_number.text

                            # "공고명"
                            bid_name = self.driver.find_element(By.CSS_SELECTOR, '#container > div:nth-child(1) > table > tbody > tr:nth-child(3) > td > div')
                            bid_name_text = bid_name.text

                            # "예정 가격"
                            estimated_price_table = self.driver.find_element(By.CSS_SELECTOR, "#container > div:nth-child(3) > table")       
                            estimated_price = estimated_price_table.find_element(By.CSS_SELECTOR, "#container > div:nth-child(3) > table > tbody > tr > td:nth-child(2) > div")
                            estimated_price_text = estimated_price.get_attribute("innerText")

                            # "기초 금액"
                            base_amount = self.driver.find_element(By.CSS_SELECTOR, "#container > div:nth-child(3) > table > tbody > tr > td:nth-child(4) > div")
                            base_amount_text = base_amount.text

                            result_dict[bid_url["page_url"]] = {
                            "공고 번호" : bid_number_text,
                            "공고명" : bid_name_text,
                            "예정 가격" : estimated_price_text,
                            "기초 금액" : base_amount_text
                            }

                        except NoSuchElementException:
                            bid_name_text = ""
                            print(f"(공고명 : {bid_name_text}), '입찰 데이터' 요소를 찾지 못했습니다.")

                    except NoSuchElementException:
                        print(f"(공고명 : {bid_name_text}), '보기' 버튼을 찾지 못했습니다.")

            except NoSuchElementException:
                print(f"페이지를 불러올 수 없습니다: {bid_url['page_url']}")
                continue

        # JSON 파일로 저장
        with open('result7.json', 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, ensure_ascii=False, indent=4)

        print("데이터가 JSON 파일로 저장되었습니다.")

        # 드라이버 종료
        self.driver.quit()




        

        
        








