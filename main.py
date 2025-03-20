import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import uuid
import platform
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 한글 폰트 설정 (Windows, Mac, Linux 자동 감지)
def get_font():
    system_name = platform.system()
    if system_name == "Windows":
        return "Malgun Gothic"
    elif system_name == "Darwin":
        return "AppleGothic"
    else:
        return "NanumGothic"

# 폰트 적용
font_path = fm.findSystemFonts(fontpaths=None, fontext='ttf')  # 시스템 폰트 검색
valid_fonts = [f for f in font_path if "Gothic" in f or "Malgun" in f or "Apple" in f]

if valid_fonts:
    font_prop = fm.FontProperties(fname=valid_fonts[0])  # 가장 첫 번째 찾은 폰트 적용
    plt.rcParams['font.family'] = font_prop.get_name()
else:
    plt.rcParams['font.family'] = get_font()

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
# Streamlit 앱 제목
st.title("맞춤형 이탈률 분석 도구")

# 세션 상태 초기화 (퍼널 단계 및 이름)
if 'stages' not in st.session_state:
    st.session_state['stages'] = ["방문자", "회원가입"]
if 'values' not in st.session_state:
    st.session_state['values'] = {stage: 0 for stage in st.session_state['stages']}
if 'new_stage_count' not in st.session_state:
    st.session_state['new_stage_count'] = len(st.session_state['stages'])

# 퍼널 단계 이름 및 개수 수정 UI
st.subheader("퍼널 단계 설정")
updated_stages = []
col1, col2 = st.columns([0.7, 0.3])

with col1:
    for i, stage in enumerate(st.session_state['stages']):
        new_name = st.text_input(f"{stage}의 새로운 이름", value=stage, key=f"edit-{i}")
        updated_stages.append(new_name)

with col2:
    for i in range(len(st.session_state['stages'])):
        st.session_state['values'][st.session_state['stages'][i]] = st.number_input(
            "인원 수", min_value=0, step=1, key=f"value-{i}")

# 버튼 스타일 변경을 위한 CSS 삽입
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #28A745; color: white; width: 100%; padding: 8px; border-radius: 5px;
    }
    div.stButton > button:nth-child(2) {
        background-color: #DC3545; color: white; width: 100%; padding: 8px; border-radius: 5px;
    }
    div.stButton > button:nth-child(3) {
        background-color: #FFC107; color: black; width: 100%; padding: 8px; border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 버튼을 가로(row)로 정렬
col1, col2 = st.columns(2)

with col1:
    if st.button("퍼널 단계 추가"):
        st.session_state['new_stage_count'] += 1
        new_stage = f"단계 {st.session_state['new_stage_count']}"
        st.session_state['stages'].append(new_stage)
        st.session_state['values'][new_stage] = 0

with col2:
    if st.button("퍼널 단계 삭제"):
        if len(st.session_state['stages']) > 2:
            removed_stage = st.session_state['stages'].pop()
            st.session_state['values'].pop(removed_stage, None)
        else:
            st.warning("최소 2개 이상의 퍼널 단계가 필요합니다.")

# 퍼널 차트 시각화 함수 (실제 인원 기준 바 차트 + 바 위에 전환율 표기)
def visualize_funnel():
    
    if len(st.session_state['stages']) < 2:
        st.warning("최소 2개 이상의 퍼널 단계를 추가해주세요.")
        return
    
    # 단계 이름 업데이트
    st.session_state['stages'] = updated_stages
    st.session_state['values'] = {stage: st.session_state['values'].get(stage, 0) for stage in updated_stages}
    
    fig, ax = plt.subplots(figsize=(8, 6))
    stages = st.session_state['stages']
    values = [st.session_state['values'][stage] for stage in stages]
    
    # 왼쪽 단계 대비 전환율(%) 계산
    conversion_rates = [100] + [((values[i] / values[i-1]) * 100) if values[i-1] > 0 else 0 for i in range(1, len(values))]
    
    ax.bar(stages, values, color='#FF5733')  # 실제 인원 수 기준 바 차트
    ax.set_ylabel("인원 수")
    ax.set_xlabel("퍼널 단계")
    ax.set_title("Funnel Chart", color='#333399')
    
    for i, v in enumerate(values):
        ax.text(i, v + 2, f"{v}명 ({conversion_rates[i]:.1f}%)", ha='center', fontsize=12, color='black')
    
    st.pyplot(fig)

# 퍼널 차트 시각화 버튼 (노란색으로 변경)
if st.button("퍼널 차트 시각화"):
    st.subheader("퍼널 시각화")
    visualize_funnel()
