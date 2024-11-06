
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import requests
import datetime
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

### Data Load
# rtdb_data Load 함수 정의
def get_rtdb_data(TagNames: list, StartTime: str, EndTime: str, SampleType: str , Frequency: int = 43200 ) -> pd.DataFrame:
    url = "http://s2appsvr/rtdbservice/PHDService.svc/getdata"
    headers = {"Content-type": "application/json", "Accept": "application/json"}
    result_df = pd.DataFrame()
    
    for TagName in TagNames:
        data = {
            "TagName": TagName,
            "StartTime": StartTime,
            "EndTime": EndTime,
            "SampleType": SampleType,
            "MaxRows": 100000000,
            "Frequency": Frequency
        }
        
        while True:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            df = pd.DataFrame.from_dict(json.loads(response.text))
            if not pd.isnull(df.loc[0, 'TagName']):
                break
        
        df = df.loc[:, ['TimeStamp', 'TagValue']].rename(columns={'TagValue': TagName, 'TimeStamp': 'DateTime'})
        df = df.astype({TagName: 'float', 'DateTime': 'datetime64[ns]'})
        
        if result_df.empty:
            result_df = df
        else:
            result_df = result_df.merge(df, on='DateTime')
    
    return result_df

# rtdb_data Load 전 조건 정의 (시간, Tag 등)
# tag_x_lab = ['PAREX Feed_Moisture', 'PAREX Feed_NA', 'PAREX Feed_Tol', 'PAREX Feed_EB', 'PAREX Feed_PX', 'PAREX Feed_MX', 'RSC_PX']
tag_x_lab = [
    'LAB_205_PAREX_FEED_MOIST',
    'LAB_205_PAREX_FEED_NON_ARO',
    'LAB_205_PAREX_FEED_TOLU',
    'LAB_205_PAREX_FEED_ETHYL_BENZ',
    'LAB_205_PAREX_FEED_P_XYL',
    'LAB_205_PAREX_FEED_M_XYL',
    'LAB_210_RAFFI_SC_P_XYL',
]

tag_x_valiables = [
    'N10L2A_I.PV',
    'N1FI136.PV',
    'N10FI109.PV',
    'N1TI168.PV',
    'N10FI113.PV',
    'N10RVCYCLE.PV',
    'N10FI111.PV',
    'N10AF_I.PV',
    'N1FC138.PV',
    'N1TI122.PV',
    'N10FI121.PV',
    'N1FC134.PV',
    'N1FC129.PV',
    'N1TDC149.PV',
    'N1TI165.PV',
    'N10FI114.PV',
]

tag_y_lab = ['LAB_210_FINISH_BTM_P_XYL'] 
days = 7 # 설정일수
now = datetime.datetime.now()
# end_time 설정
current_hour = now.hour
if 8 <= current_hour < 20:
    # 현재 시간이 08:00~19:59 사이면 당일 08:00으로 설정
    end_time = now.replace(hour=8, minute=0, second=0)
else:
    # 현재 시간이 20:00~다음날 07:59 사이면 20:00으로 설정
    if current_hour >= 20:
        end_time = now.replace(hour=20, minute=0, second=0)
    else:  # current_hour < 8
        # 전날 20:00으로 설정
        end_time = (now - datetime.timedelta(days=1)).replace(hour=20, minute=0, second=0)

# start_time 설정 (end_time 기준 으로 설정일수 전)
start_time = end_time - datetime.timedelta(days=days)

# datetime을 문자열로 변환
start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

#rtdb_data Load
rtdb_data1 = get_rtdb_data(tag_x_valiables, start_time, end_time, SampleType = '1') # process tag이므로 SampleType = '1' 줘서 average 설정
rtdb_data2 = get_rtdb_data(tag_x_lab, start_time, end_time, SampleType = '0') # lab tag이므로 SampleType = '0' 줘서 snapshot 설정
rtdb_data3 = get_rtdb_data(tag_y_lab, start_time, end_time, SampleType = '0')

#y값 전처리 (운전에 대한 결과이므로 shift 시켜 다음 분석갑을 가져옴)
rtdb_data3['LAB_210_FINISH_BTM_P_XYL'] = rtdb_data3['LAB_210_FINISH_BTM_P_XYL'].shift(-1)
rtdb_data3['LAB_210_FINISH_BTM_P_XYL'].fillna(method='ffill', inplace=True)

#data 병합 
merged_rtdb_data = rtdb_data1.merge(rtdb_data2, on='DateTime', how='outer').merge(rtdb_data3, on='DateTime', how='outer')

# Column명 변경
new_col_dict = {
    'N10L2A_I.PV': 'L2/A',
    'N1FI136.PV': 'Fin BTM RD Flow',
    'N10FI109.PV': 'Ext Flow_Turbine',
    'N1TI168.PV': 'F.Col BTM Temp',
    'N10FI113.PV': 'Line Flush Flow_Turbine',
    'N10RVCYCLE.PV': 'RV Cycle Time',
    'N10FI111.PV': '2nd Flush Flow_Turbine',
    'N10AF_I.PV': 'A/Fa',
    'N1FC138.PV': 'F.Col Net OVHD  Flow',
    'N1TI122.PV': 'R.Col Tray 3 Temp',
    'N10FI121.PV': 'Pumparound Flow, Turbine Meter',
    'N1FC134.PV': 'E.Col Net OVHD  Flow',
    'N1FC129.PV': 'RSC Flow',
    'N1TDC149.PV': 'E.Col TDC',
    'N1TI165.PV': 'F.Col OVHD Temp',
    'N10FI114.PV': 'RV Sealant Flow_Out',
    'LAB_205_PAREX_FEED_MOIST': 'PAREX Feed_Moisture',
    'LAB_205_PAREX_FEED_NON_ARO': 'PAREX Feed_NA',
    'LAB_205_PAREX_FEED_TOLU': 'PAREX Feed_Tol',
    'LAB_205_PAREX_FEED_ETHYL_BENZ': 'PAREX Feed_EB',
    'LAB_205_PAREX_FEED_P_XYL': 'PAREX Feed_PX',
    'LAB_205_PAREX_FEED_M_XYL': 'PAREX Feed_MX',
    'LAB_210_RAFFI_SC_P_XYL': 'RSC_PX',
    'LAB_210_FINISH_BTM_P_XYL': 'PX Purity_Lab'
}
merged_rtdb_data= merged_rtdb_data.rename(columns=new_col_dict)

### 실시간 Data로 모델 평가
# 모델 불러오기
# 현재 파일의 디렉토리 경로를 가져옴
current_dir = os.path.dirname(os.path.abspath(__file__))

# 모델 파일 경로 생성
model_path = os.path.join(current_dir, 'best_rf_model.pkl')

# 모델 파일 열기
with open(model_path, 'rb') as file:
    loaded_model = pickle.load(file)

# 모델이 요구하는 특성 확인
# print("모델이 요구하는 특성:")
# print(loaded_model.feature_names_in_)

# 현재 데이터의 컬럼 확인
# print("\n현재 데이터의 컬럼:")
# print(merged_rtdb_data.columns)

# 테스트 데이터의 특성이 올바른지 확인
required_features = loaded_model.feature_names_in_
test_features = merged_rtdb_data[required_features]

# 이제 이 test_features로 예측
predictions = loaded_model.predict(test_features)

# 예측 결과를 데이터프레임에 추가
merged_rtdb_data['Predicted_PX_Purity'] = predictions

### 시각화

def app(dashboard_title):

    # Streamlit 페이지 설정
    st.title("머신러닝을 통한 No.2 PAREX Purity 예측 결과")

    # 그래프와 표를 위한 컨테이너 생성
    graph_container = st.container()
    table_container = st.container()
   
    with graph_container:
        st.subheader(":chart_with_upwards_trend: 실제값 vs 머신러닝 예측값")
        
        # Plotly 그래프 생성
        fig = go.Figure()
    
        # 실제 분석값 추가
        fig.add_trace(
            go.Scatter(
                x=merged_rtdb_data['DateTime'],
                y=merged_rtdb_data['PX Purity_Lab'],
                name='실제 분석값',
                mode='lines+markers',
                line=dict(color='blue'),
                hovertemplate='실제 분석값: %{y:.3f}<br><extra></extra>'
            )
        )
    
        # 머신러닝 예측값 추가
        fig.add_trace(
            go.Scatter(
                x=merged_rtdb_data['DateTime'],
                y=merged_rtdb_data['Predicted_PX_Purity'],
                name='머신러닝 예측값',
                mode='lines+markers',
                line=dict(color='red'),
                hovertemplate='예측값: %{y:.3f}<br><extra></extra>'
            )
        )
        tickvals = pd.date_range(start=merged_rtdb_data['DateTime'].min(), 
                         end=merged_rtdb_data['DateTime'].max(), 
                         freq='D') + pd.Timedelta(hours=12)
        
        # 그래프 레이아웃 설정
        fig.update_layout(
        yaxis_title='No.2 PAREX PX Purity, wt%',
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=1.2,
            xanchor="right",
            x=0.99
        ),
        xaxis=dict(
            tickformat='%Y-%m-%d %H시',
            tickvals=tickvals,            
         
        )
    )

        
        # Streamlit에 플로틀리 그래프 표시
        st.plotly_chart(fig, use_container_width=True)
    
    with table_container:
        st.subheader(":clipboard: 예측 결과 상세 데이터")
        
        # 시간 형식 변경 함수
        def format_datetime(dt):
            return dt.strftime('%Y-%m-%d %H시')
    
        # 차이(오차) 계산
        merged_rtdb_data['차이(오차)'] = merged_rtdb_data['PX Purity_Lab'] - merged_rtdb_data['Predicted_PX_Purity']
    
        # 표시할 데이터 준비
        display_df = merged_rtdb_data[['DateTime', 'PX Purity_Lab', 'Predicted_PX_Purity', '차이(오차)']].copy()
    
        # 시간 형식 변경
        display_df['DateTime'] = display_df['DateTime'].apply(format_datetime)
    
        # 컬럼명 변경
        display_df.columns = ['시간', '실제 분석값', '머신러닝 예측값', '차이(오차)']
    
        # 평균 계산
        means = display_df.mean(numeric_only=True)
        means_df = pd.DataFrame(means).T
        means_df.index = ['평균']
    
        # 시간 컬럼에 대한 처리
        means_df.insert(0, '시간', '')
    
        # 데이터프레임 결합
        final_df = pd.concat([display_df, means_df])
    
        # 인덱스 이름 설정
        final_df.index.name = 'No.'

         
        # 각 컬럼의 값을 가운데 정렬하는 스타일 적용
        # styled_df = final_df.style.set_properties(**{'text-align': 'center'})
        # html = styled_df.to_html()

        # st.markdown(html, unsafe_allow_html=True)
        # Streamlit에 표 표시
        st.dataframe(
            final_df.style.format({
                '실제 분석값': '{:.3f}',
                '머신러닝 예측값': '{:.3f}',
                '차이(오차)': '{:.3f}'
            }).set_properties(**{
                'text-align': 'center',
                'font-size': '11pt'
            }),
            use_container_width=False,
            height=400  # 표의 높이 조정
        )
 


