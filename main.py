import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import uuid
import platform

# 한글 폰트 설정 (Windows와 Mac/Linux 호환)
if platform.system() == "Windows":
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == "Darwin":
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# Streamlit 앱 제목
st.title("맞춤형 이탈률 분석 도구")

# 세션 상태 초기화 (퍼널 단계 및 이름)
if 'stages' not in st.session_state:
    st.session_state['stages'] = ["방문자", "회원가입"]
if 'values' not in st.session_state:
    st.session_state['values'] = {stage: 0 for stage in st.session_state['stages']}

# 퍼널 단계 이름 수정 기능
st.subheader("퍼널 단계 이름 수정")
updated_stages = []
for stage in st.session_state['stages']:
    new_name = st.text_input(f"{stage}의 새로운 이름", value=stage, key=f"edit-{stage}")
    updated_stages.append(new_name)

# 버튼을 가로(row)로 배치 (10px 간격 조정)
col1, col2 = st.columns([0.48, 0.48])

# 버튼 HTML을 직접 삽입하여 개별 스타일 적용
with col1:
    st.markdown("""
        <style>
        .update-btn {
            background-color: #007BFF; color: white; padding: 10px 20px; 
            border: none; border-radius: 5px; font-size: 16px;
        }
        .update-btn:hover { background-color: #0056b3; }
        </style>
        <button class="update-btn" onclick="window.location.reload();">단계 이름 업데이트</button>
    """, unsafe_allow_html=True)
    if st.session_state.get('update_clicked'):
        st.session_state['stages'] = updated_stages
        st.session_state['values'] = {stage: st.session_state['values'].get(stage, 0) for stage in updated_stages}

with col2:
    st.markdown("""
        <style>
        .add-btn {
            background-color: #28A745; color: white; padding: 10px 20px; 
            border: none; border-radius: 5px; font-size: 16px;
        }
        .add-btn:hover { background-color: #1e7e34; }
        </style>
        <button class="add-btn" onclick="window.location.reload();">퍼널 단계 추가</button>
    """, unsafe_allow_html=True)
    if st.session_state.get('add_clicked'):
        new_stage = f"단계 {len(st.session_state['stages']) + 1}"
        st.session_state['stages'].append(new_stage)
        st.session_state['values'][new_stage] = 0

# 퍼널 데이터 입력 UI
st.subheader("퍼널 단계별 인원 입력")
for stage in st.session_state['stages']:
    st.session_state['values'][stage] = st.number_input(
        f"{stage} 단계 인원 수", min_value=0, step=1, key=f"{stage}"
    )

# 퍼널 차트 시각화 함수 (세로 차트, 비율 기준, 색상 변경)
def visualize_funnel():
    if len(st.session_state['stages']) < 2:
        st.warning("최소 2개 이상의 퍼널 단계를 추가해주세요.")
        return
    
    fig, ax = plt.subplots(figsize=(8, 6))
    stages = st.session_state['stages']
    values = list(st.session_state['values'].values())
    
    # 비율(%) 계산
    max_value = max(values) if max(values) > 0 else 1
    percentages = [(v / max_value) * 100 for v in values]
    
    x_labels = [f"STEP {i+1} [{stage}]\n{values[i]}명" for i, stage in enumerate(stages)]
    
    ax.bar(x_labels, percentages, color='#FF5733')  # 색상 변경
    ax.set_ylabel("비율 (%)")
    ax.set_xlabel("퍼널 단계")
    ax.set_title("퍼널 분석 차트", color='#333399')
    
    for i, v in enumerate(percentages):
        ax.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=12, color='black')
    
    st.pyplot(fig)

# 퍼널 차트 시각화 버튼 (노란색으로 변경)
st.markdown("""
    <style>
    .visualize-btn {
        background-color: #FFC107; color: black; padding: 10px 20px; 
        border: none; border-radius: 5px; font-size: 16px;
    }
    .visualize-btn:hover { background-color: #e0a800; }
    </style>
    <button class="visualize-btn" onclick="window.location.reload();">퍼널 차트 시각화</button>
""", unsafe_allow_html=True)

if st.session_state.get('visualize_clicked'):
    visualize_funnel()