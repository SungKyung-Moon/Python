import json
import urllib.parse

class Config:
    def __init__(self, config_file):                                # config_file 매개변수 설정
        self.config_file = config_file
        self.config = self.load_config()                
        self.start_url = self.get_start_url()                       # start_url 설정

    def load_config(self):
        with open(self.config_file, encoding='utf-8') as f:         #open 함수를 사용하여 JSON 파일을 읽어옴 / 인코딩 명시
            config_data = json.load(f)                              # json.load 함수를 통해 JSON 파일을 읽어와 파이썬 객체로 변환
        return config_data


    def get_base_url(self):
        return self.config["base"]["url"] + str(self.config["base"]["port"]) + self.config["base"]["path"]      # 문자열과 정수를 연결하는 경우 : 정수를 문자열로 변환(형 변환 필요)
        
    def get_make_url(self):
        return self.config["make"]                 

    def get_start_url(self):
        base_url = self.get_base_url()             
        make_url = self.get_make_url()             
      
        encoded_query_params = urllib.parse.urlencode(make_url, encoding='EUC-KR')          # urlencode() : 딕셔너리를 문자열로 인코딩 / URL의 쿼리 파라미터를 인코딩할 때 사용
        # EUC-KR 인코딩 형식 : 대한민국에서 주로 사용되는 한글 문자 집합을 인코딩 
        return f"{base_url}{encoded_query_params}"         
    
    


