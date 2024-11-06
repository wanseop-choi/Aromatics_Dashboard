
import streamlit as st
import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import requests
import json
import pickle
from datetime import datetime, timedelta, time


class Constant:
    PROCESS_TAGS =  {
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
            }
    
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

def app(dashboard_title):

    # 시뮬레이션 설정값 저장을 위한 session_state 생성
    if 'df_sim_params' not in st.session_state:
        df_sim_params_temp = pd.DataFrame(columns=Constant.PROCESS_TAGS.values(), dtype='float')
        df_sim_params_temp.loc[0, :] = 0
        st.session_state['df_sim_params'] = df_sim_params_temp

    # 시뮬레이션 결과 저장을 위한 session_state 생성
    if 'df_result' not in st.session_state:
        st.session_state.df_result = pd.DataFrame(columns=['예상 No.2 PAREX PX Purity'] + list(Constant.PROCESS_TAGS.values()))

    # Side bar
    st.sidebar.markdown('---')
    st.sidebar.subheader('Simulation 일시 설정')

    # # RTDB Data 불러오기 (Text_input 직접 입력)
    # with st.sidebar:
    #     with st.form('RTDB 데이터 불러오기'):
    #         current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    #         datetime_input = st.text_input('입력 기준 이전 1시간 평균 Data Load', placeholder=current_time)
    #         # datetime_input = st.text_input('일시 (ex.2024-01-01 08:00)')
    #         button_set_sim_params = st.form_submit_button('RTDB 데이터 불러오기')

    # if button_set_sim_params:
    #     if datetime_input == '':
    #         st.sidebar.warning('날짜를 입력해주세요.')
    #     else:
    #         # 설정 날짜에 따라 RTDB 데이터 불러오기 (설정 일시의 1시간 평균 Data_Pumparound 2cycle 고려)
    #         dt = datetime.strptime(datetime_input, '%Y-%m-%d %H:%M')
    #         start_time = (dt - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M')
    #         # start_time = datetime_input
    #         end_time = datetime_input
    #         frequency = 3601
    #         sample_type = '1'
    #         df = get_rtdb_data(Constant.PROCESS_TAGS.keys(), start_time, end_time, sample_type, frequency)
    #         df = df.rename(dict(zip(Constant.PROCESS_TAGS.keys(), Constant.PROCESS_TAGS.values())), axis=1)

    # # RTDB Data 불러오기 (st.date_input과 st.slider (time slider) 조합-10분 단위)
    with st.sidebar:
        with st.form('RTDB 데이터 불러오기'):
            # 현재 날짜를 기본값으로 설정
            current_date = datetime.now().date()
            # 날짜 선택 (date picker)
            selected_date = st.date_input('날짜 선택', value=current_date)
            
            # 현재 시간을 기본값으로 설정
            current_time = datetime.now().time()
            # 시간 범위 선택 (time slider)
            selected_time_range = st.slider(
                "시간 선택",
                min_value=time(0, 0),
                max_value=time(23, 59),
                value=time(current_time.hour, (current_time.minute // 10) * 10),  # 10분 단위로 반올림
                step=timedelta(minutes=10),  # 10분 간격으로 설정
                format="HH:mm"  # 시간 형식 지정
            )
    
            button_set_sim_params = st.form_submit_button('RTDB 데이터 불러오기')
            st.caption("_선택시간의 이전 1시간 평균 Data 불러옴_")

    if button_set_sim_params:
        # 선택된 날짜와 시간을 결합하여 datetime 객체 생성
        datetime_input = datetime.combine(selected_date, selected_time_range)
        formatted_datetime = datetime_input.strftime('%Y-%m-%d %H:%M')
        
        # 설정 날짜에 따라 RTDB 데이터 불러오기 (설정 일시의 1시간 평균 Data_Pumparound 2cycle 고려)
        start_time = (datetime_input - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M')
        end_time = formatted_datetime
        frequency = 3601
        sample_type = '1'
        df = get_rtdb_data(Constant.PROCESS_TAGS.keys(), start_time, end_time, sample_type, frequency)
        df = df.rename(dict(zip(Constant.PROCESS_TAGS.keys(), Constant.PROCESS_TAGS.values())), axis=1)

        # session_state에 저장
        st.session_state['df_sim_params'] = df
            
    # Main Page
    st.subheader('No.2 PAREX Purity Simulation')

    with st.form('시뮬레이션 변수 입력'):
        # session_state 값 불러오기
        df = st.session_state['df_sim_params']
        st.markdown(f"#### 운전 변수 설정")

        # st.columns 사이즈 설정
        row_length = 4
        col_length = int(len(Constant.PROCESS_TAGS) / row_length)
        cols = st.columns(col_length)

        # 시뮬레이션 input box 생성
        for i, tag in enumerate(Constant.PROCESS_TAGS.values()):
            with cols[i % col_length]:
                df.loc[0, tag] = float(st.text_input(f'{tag}', key="simulation_input_" + tag, value=df.loc[0, tag]))

        button_run_simulation = st.form_submit_button('Simulation 실행')

    if button_run_simulation:
        # 입력값 저장
        st.session_state['df_sim_params'] = df

        # 모델 불러오기
        # 현재 파일의 디렉토리 경로를 가져옴
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 모델 파일 경로 생성
        model_path = os.path.join(current_dir, 'best_rf_model.pkl')
        
        # 모델 파일 열기
        with open(model_path, 'rb') as file:
            loaded_model = pickle.load(file)
 
        required_features = loaded_model.feature_names_in_
        test_features = df[required_features]
      
        purity_pred = loaded_model.predict(test_features)
        df.loc[0, '예상 No.2 PAREX PX Purity'] = purity_pred

        # 시뮬레이션 결과 저장
        st.session_state.df_result = pd.concat([st.session_state.df_result, df], ignore_index=True)
        # st.session_state.df_result = st.session_state.df_result.drop('DateTime', axis=1)
        st.session_state.df_result.index += 1

    if not st.session_state.df_result.empty:
        st.markdown(f'#### 예측 결과')
        # 역순으로 출력
        st.write(st.session_state.df_result.iloc[::-1])
