import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

mpl.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'gulim'


# 1. 데이터 전처리
df = pd.read_csv('./서울시 지하철 호선별 역별 시간대별 승하차 인원 정보.csv', encoding='cp949')
print(df.head())
print(df.tail())
print(df.shape)

# 결측치 확인
print(df.isnull().sum())

# 컬럽별 데이터 확인
# 사용월
df['사용월'].unique()

# 호선명
df['호선명'].unique()

# 데이터 타입 확인
df['사용월'] = df['사용월'].astype('str')
print(df.dtypes)

# 불필요한 컬럼 삭제
df.drop(columns=['작업일자'], inplace=True)

# 승차/하차 테이블 분리
# 승차 테이블 만들기
print(df)

# 공통 컬럼
df1 = df.iloc[:, :3]

# 승차 컬럼만 가져오기
df2 = df.iloc[:,3::2]
df2.columns = df2.columns.str.split(' ').str[0]
print(df2.columns)

# 공통컬럼과 승차컬럼 연결하기
df_in = pd.concat([df1,df2], axis=1)
print(df_in)


# 하차 테이블 만들기
# 공통 컬럼
df3 = df.iloc[:, :3]

# 하차 컬럼만 가져오기
df4 = df.iloc[:,4::2]
df4.columns = df4.columns.str.split(' ').str[0]

# 공통컬럼과 하차컬럼 연결하기
df_out = pd.concat([df3,df4], axis=1)
print(df_out)


# -----------------------------------------------------------------

# 2. 출퇴근시간 역별 승하차 인원 분석
# 최근 월을 기준으로 승하차 데이터프레임 생성

df_in_202108 = df_in[df_in['사용월']=='202108']
df_out_202108 = df_out[df_out['사용월']=='202108']

# 질문1. 출근 시간에 가장 많은 사람이 승차하는 역은 어디일까? (08시-09시)
print(df_in_202108)
print(df_in_202108.nlargest(10, '08시-09시')[['지하철역', '08시-09시']])
# 결과 : 1.신림역 2. 구로디지털단지역 3. 서울대입구역


# 질문2. 출근 시간에 가장 많은 사람이 하차하는 역은 어디일까? (09시-10시)
print(df_out_202108.nlargest(10, '09시-10시')[['지하철역', '09시-10시']])
# 결과 : 1.강남역 2. 역삼역 3. 가산디지털단지역


# 질문3. 퇴근 시간에 가장 많은 사람이 승차하는 역은 어디일까? (18시-19시)
print(df_in_202108.nlargest(10, '18시-19시')[['지하철역', '18시-19시']])
# 결과 : 1.강남역 2. 가산디지털단지역 3. 선릉역


# 질문4. 퇴근 시간에 가장 많은 사람이 하차하는 역은 어디일까? (18시-19시)
print(df_out_202108.nlargest(10, '18시-19시')[['지하철역', '18시-19시']])
# 결과 : 1.신림역 2. 잠실(송파구청)역 3. 서울대입구역


# --------------------------------------------------------------------------
# 3. 강남역의 최근 시간대별 승하차정보 분석
# 강남역의 최근 승차정보 분석
df_gangnam_in = df_in_202108[df_in_202108['지하철역']=='강남'].iloc[:,3:]
print(df_gangnam_in)

# melt
df_gangnam_in = df_gangnam_in.melt()

# 컬럼명 변경
df_gangnam_in.columns=['시간대', '승차건수']
print(df_gangnam_in.sort_values('승차건수'))

# 시간대별 승차인원 시각화하기
plt.barh(df_gangnam_in['시간대'], df_gangnam_in['승차건수'])
plt.show()


# ----------------------------------------------------------------
# 4. 지하철 시간대별, 역별 이용현황 분석
# 시간대별 승차 현황
# 승차정보 집계 데이터 만들기
df_in_202108_agg = df_in_202108.copy()
print(df_in_202108_agg)

# 인덱스 변경('지하철역')
df_in_202108_agg.index = df_in_202108_agg['지하철역']
print(df_in_202108_agg)

# 컬럼 삭제 ('사용월', '호선명', '지하철역')
df_in_202108_agg.drop(columns=['사용월', '호선명', '지하철역'], inplace=True)

# 행,열 합계
df_in_202108_agg.loc['sum'] = df_in_202108_agg.apply('sum', axis=0)
print(df_in_202108_agg)

df_in_202108_agg['sum'] = df_in_202108_agg.apply('sum', axis=1)


# 시간대별 승차 건수
s_in = df_in_202108_agg.loc['sum'][:-1].sort_values()
s_in = s_in.sort_index()
x = s_in.index
y = s_in.values
plt.bar(x,y)
plt.xticks(rotation=90)
plt.show()

