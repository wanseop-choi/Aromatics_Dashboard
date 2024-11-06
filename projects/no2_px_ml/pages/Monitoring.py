
import streamlit as st
import datetime
import json
import requests
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu


# RTDB Data 불러오기
def get_rtdb_data(TagNames: list, StartTime: str, EndTime: str, SampleType: str = '1', Frequency: int = 3600) -> pd.DataFrame:
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

# 2개 태그에 대한 그래프 생성
def create_plot(rtdb_data: pd.DataFrame, tags: list):
    margin_percent = 0.1  # 고정된 마진 값
    min_values = rtdb_data[tags].min()
    max_values = rtdb_data[tags].max()

    adjusted_min_values = {
        tag: min_val - (max_values[tag] - min_val) * margin_percent 
        for tag, min_val in min_values.items()
    }

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=rtdb_data['DateTime'], y=rtdb_data[tags[0]], name=tags[0]),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=rtdb_data['DateTime'], y=rtdb_data[tags[1]], name=tags[1]),
        secondary_y=True,
    )

    fig.update_layout(
        title='RTDB Tag Data',
        xaxis_title='DateTime',
        height=600
    )

    fig.update_yaxes(
        title_text=tags[0],
        secondary_y=False,
        range=[adjusted_min_values[tags[0]], max_values[tags[0]]]
    )
    fig.update_yaxes(
        title_text=tags[1],
        secondary_y=True,
        range=[adjusted_min_values[tags[1]], max_values[tags[1]]]
    )

    return fig

# def visualize_rtdb_data(tags: list):
#     days = 7  # 고정된 일수
#     now = datetime.datetime.now()
#     start_time = (now - datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
#     end_time = now.strftime('%Y-%m-%d %H:%M:%S')

#     rtdb_data = get_rtdb_data(tags, start_time, end_time)
#     fig = create_plot(rtdb_data, tags)

#     st.plotly_chart(fig, use_container_width=True)

# 단일 태그에 대한 그래프 생성
def create_single_tag_plot(tag: str, title: str, days: int):
    now = datetime.datetime.now()
    start_time = (now - datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    end_time = now.strftime('%Y-%m-%d %H:%M:%S')

    rtdb_data = get_rtdb_data([tag], start_time, end_time)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rtdb_data['DateTime'], 
        y=rtdb_data[tag], 
        name="",
        hovertemplate='시간: %{x|%H:%M}<br>' + '값 : %{y:.2f}<extra></extra>'

    ))
    
    fig.update_layout(
        title=title,
        height=300,
        hovermode='x unified', 
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        griddash='dot'
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        griddash='dot',
        tickformat='%Y-%m-%d'
    )
    return fig


def app(dashboard_title):
    # Side bar
    st.sidebar.markdown('---')
    st.sidebar.subheader('Trend 조회 기간(일) 설정')
    with st.sidebar:
        days_slider = st.slider("현재로부터 최근 몇일 Data", 1, 30, 7)

    
    # Main 페이지 설정
    st.title(f"No.2 PX Process Trend - {days_slider} Days")  
    
    tab1, tab2, tab3 = st.tabs([":gray-background[No.2 PAREX]", ":gray-background[No.2 ISOMAR]", ":gray-background[No.2 Xylene]"])
    
    with tab1:
        
        tag_dict_PAREX = {
            'No.2 PAREX Load (%)': 'N10FRATE.PV',
            'PX 생산량 (kl/hr)': 'N1FI136.PV',
            'PX Purity (wt%)': 'LAB_210_FINISH_BTM_P_XYL',
            'PAREX Unit Recovery (%)': '(Lab_210_Finish_BTM_P_Xyl*(Lab_205_Parex_Feed_P_Xyl-Lab_210_Raffi_SC_P_Xyl))/(Lab_205_Parex_Feed_P_Xyl*(LAb_210_Finish_BTM_P_Xyl-Lab_210_Raffi_SC_P_Xyl))*100',
            'Chamber 운전변수 - L2/A': 'N10L2A_I.PV',
            'Chamber 운전변수 - A/Fa': 'N10AF_I.PV',
            'EB Content in Feed (wt%) ': 'LAB_205_PAREX_FEED_ETHYL_BENZ',
            'Trace Xylene - Raffinate Column BTM (wtppm)': 'LAB_210_RAFFI_SC_TRACE_PDEB'
        }
    
    
        # 2x4 그리드 생성
        for i in range(0, len(tag_dict_PAREX), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(tag_dict_PAREX):
                    title, tag = list(tag_dict_PAREX.items())[i + j]
                    with cols[j]:
                        fig = create_single_tag_plot(tag, title, days_slider)
                        st.plotly_chart(fig, use_container_width=True)
    with tab2:
        
        tag_dict_ISOMAR = {
            'Feed Rate (kl/hr)': 'N9FC101.PV',
            'EB Conversion (%)': 'C_29EBC',
            'PX Conversion (%)': 'C_29PXC',     
            'Reactor Inlet Temperature (℃)': 'N9TC101.PV',
            'Reactor DT (℃)': 'N9TI103.PV-N9TC101.PV',
            'H2 Consumpsion (Nm3/hr) - CCR H2': 'N9FC107A.PV',
            'Recycle Gas H2 Purity (mol%)': 'LAB_209_RC_GAS_H2_PU',
            'H2/HC Ratio': '(N9FI103A.PV*(LAB_209_RC_GAS_H2_PU)/22.4*10)/((N9FC101.PV)*0.8720/106.2*1000000)',
            'Recycle Gas Moisture (wtppm) - Analyzer' : 'N9AI107.PV'
        }
    
        # 2x4 그리드 생성
        for i in range(0, len(tag_dict_ISOMAR), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(tag_dict_ISOMAR):
                    title, tag = list(tag_dict_ISOMAR.items())[i + j]
                    with cols[j]:
                        fig = create_single_tag_plot(tag, title, days_slider)
                        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        
        tag_dict_Xylene = {
            'Reformate Splitter Total Feed (kl/hr)': '23FC106.PV+N5FC147.PV+N5FC148.PV',
            'Xylene Column Total Feed (kl/hr)': 'N5FC103.PV+N9FC109.PV+N5FC160.PV',
            'Reformate Splitter Column DP (kg/cm2)': 'N5PI303.PV-N5PC211.PV',
            'Clay Tower Inlet Temperature (℃)': 'N5TC210.PV',
            'Light Reformate R/D Flow-SPL OVHD (kl/hr)': 'N5FC107.PV',
            'MX R/D Flow (kl/hr)': 'N5FC157.PV',
            'Splitter OVHD A-C8 Content (wt%)': 'LAB_205_SPLIT_OVHD_ETHYL_BENZ+LAB_205_SPLIT_OVHD_P_XYL+LAB_205_SPLIT_OVHD_M_XYL+LAB_205_SPLIT_OVHD_O_XYL',
            'Xylene OVHD A-C9 Content (wtppm)': 'LAB_205_PAREX_FEED_C9*10000',
            'Xylene BTM OX Content (wt%)' : 'LAB_205_XYLENE_BTM_O_XYL_NIR'
        }
    
        # 2x4 그리드 생성
        for i in range(0, len(tag_dict_Xylene), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(tag_dict_Xylene):
                    title, tag = list(tag_dict_Xylene.items())[i + j]
                    with cols[j]:
                        fig = create_single_tag_plot(tag, title, days_slider)
                        st.plotly_chart(fig, use_container_width=True)
