import random
import time
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="간호 대처 가이드: 응급 병동 타이쿤", page_icon="🏥", layout="centered")

# ==============================================================================
# 1. 리스트(List) 구조: 단계별 질병·증상·정답 처치 데이터베이스 (고1 생명과학/보건 수준)
# ==============================================================================
STAGE_1_CASES = [
    {
        "disease": "아나필락시스 쇼크",
        "symptom": "땅콩 섭취 5분 뒤 전신 두드러기, 후두 부종으로 인한 쌕쌕거림, 혈압 급강하(75/40mmHg) 발생!",
        "treatments": ["에피네프린 근육주사"],
        "explanation": "급성 중증 알레르기 반응으로 교감신경을 흥분시켜 기도를 확장하고 혈압을 높이는 에피네프린 투여가 최우선입니다."
    },
    {
        "disease": "저혈당 쇼크",
        "symptom": "인슐린 투여 후 식사를 거른 환자. 식은땀, 손 떨림, 어지럼증을 호소하며 혈당이 42mg/dL로 측정됨.",
        "treatments": ["포도당 수액 정맥투여"],
        "explanation": "혈당이 정상 범위(70~110mg/dL) 이하로 급감하여 뇌 에너지 공급이 부족한 상태로 즉각적인 포도당 공급이 필요합니다."
    },
    {
        "disease": "과호흡 증후군",
        "symptom": "극심한 시험 스트레스 후 빠르고 깊은 호흡을 반복하며 손발 저림과 마비감(호흡성 알칼리증)을 호소함.",
        "treatments": ["안정 유도 및 복식호흡"],
        "explanation": "과도한 이산화탄소(CO₂) 배출로 혈액이 염기성화(pH 상승)된 상태이므로 호흡 속도를 늦춰 혈중 CO₂ 농도를 회복시켜야 합니다."
    },
    {
        "disease": "열사병",
        "symptom": "폭염 속 야외 활동 후 쓰러짐. 심부 체온 40.8℃, 피부는 뜨겁고 건조하며 땀이 나지 않고 의식이 혼미함.",
        "treatments": ["심부 체온 냉각 처치"],
        "explanation": "시상하부의 체온 조절 중추가 기능을 상실한 응급 상태로, 얼음팩·냉수 마사지 등으로 즉시 체온을 낮춰야 합니다."
    },
    {
        "disease": "기도 이물 폐쇄",
        "symptom": "떡을 먹다 갑자기 목을 움켜쥐고 소리를 내지 못하며 얼굴과 입술에 청색증이 나타남.",
        "treatments": ["하임리히법 시행"],
        "explanation": "기도가 완전히 막혀 가스 교환이 차단된 상태이므로 횡격막을 강하게 압박해 이물질을 배출시켜야 합니다."
    },
    {
        "disease": "일산화탄소 중독",
        "symptom": "밀폐된 공간에서 난방기 사용 후 두통과 의식 저하로 발견됨. 헤모글로빈의 산소 운반 능력이 급격히 저하됨.",
        "treatments": ["고농도 산소 공급"],
        "explanation": "일산화탄소(CO)는 산소보다 헤모글로빈 친화력이 약 200배 높으므로 고농도 산소를 공급해 해리를 촉진해야 합니다."
    }
]

STAGE_2_CASES = [
    {
        "disease": "급성 심근경색",
        "symptom": "왼쪽 가슴을 쥐어짜는 듯한 흉통이 30분 이상 지속되며 왼쪽 어깨로 방사통이 퍼지고 식은땀을 흘림.",
        "treatments": ["니트로글리세린 설하투여", "항혈소판제(아스피린) 투여"],
        "explanation": "관상동맥이 혈전으로 막혀 심근이 괴사하는 질환으로, 혈관 확장제와 혈전 생성 억제제를 함께 투여해야 합니다."
    },
    {
        "disease": "당뇨병성 케톤산증",
        "symptom": "제1형 당뇨 환자가 심한 갈증, 다뇨와 함께 호흡에서 과일향(아세톤 냄새)이 나며 혈당 480mg/dL, 혈액 pH 7.18임.",
        "treatments": ["생리식염수 수액 공급", "속효성 인슐린 투여"],
        "explanation": "인슐린 결핍으로 지방이 분해되며 케톤체가 축적되어 혈액이 산성화된 상태입니다. 탈수 교정과 인슐린 투여가 필수입니다."
    },
    {
        "disease": "긴장성 기흉",
        "symptom": "흉부 외상 후 한쪽 가슴이 부풀어 오르고 청진 시 호흡음이 소실됨. 기관이 반대쪽으로 밀리며 혈압이 떨어짐.",
        "treatments": ["흉강 천자(감압술)", "고농도 산소 공급"],
        "explanation": "흉강 내 공기가 쌓여 폐와 심장을 압박하므로 바늘로 공기를 빼내 압력을 낮추고 산소를 공급해야 합니다."
    },
    {
        "disease": "고칼륨혈증",
        "symptom": "만성 신부전 환자가 전신 무력감과 부정맥을 보이며 심전도에서 뾰족한 T파가 관찰됨(혈중 K+ 6.9mEq/L).",
        "treatments": ["글루콘산칼슘 정맥투여", "포도당·인슐린 병합투여"],
        "explanation": "높은 칼륨 농도는 심장 세포막의 휴지 전위를 변화시켜 심정지를 유발하므로 심근 보호 및 세포 내 칼륨 이동 처치가 필요합니다."
    }
]

STAGE_3_CASES = [
    {
        "disease": "패혈성 쇼크",
        "symptom": "폐렴 악화 후 고열(39.5℃), 빈맥, 빈호흡과 함께 수액을 주어도 혈압이 70/40mmHg로 유지되지 않음.",
        "treatments": ["광범위 항생제 투여", "생리식염수 급속 수액", "혈관수축제(노르에피네프린)"],
        "explanation": "전신 염증 반응으로 혈관이 과도하게 확장된 상태입니다. 원인균 제압(항생제), 혈액량 보충(수액), 혈압 유지(승압제) 3가지가 모두 필요합니다."
    },
    {
        "disease": "급성 유기인계 농약 중독",
        "symptom": "농약 노출 후 동공 축소, 과도한 침 분비, 기관지 경련, 서맥 및 근육 떨림이 동시에 나타남.",
        "treatments": ["아트로핀 정맥투여", "프랄리독심(해독제) 투여", "기도 확보 및 산소 공급"],
        "explanation": "아세틸콜린에스터레이스 억제로 부교감신경이 과흥분된 상태이므로 항콜린제(아트로핀), 효소 재활성제, 산소 공급을 병행합니다."
    },
    {
        "disease": "중증 외상성 출혈 쇼크",
        "symptom": "교통사고로 대퇴부 개방성 골절과 대량 출혈 발생. 피부가 창백하고 차가우며 맥박이 빠르고 약하게 뜀.",
        "treatments": ["출혈 부위 직접 압박 지혈", "농축적혈구 수혈", "생리식염수 급속 수액"],
        "explanation": "순환 혈액량 급감으로 조직 산소 공급이 중단된 저혈량성 쇼크이므로 지혈과 함께 혈액 및 수액 보충이 동시에 이루어져야 합니다."
    }
]

ALL_DISEASES = [
    "아나필락시스 쇼크", "저혈당 쇼크", "과호흡 증후군", "열사병",
    "기도 이물 폐쇄", "일산화탄소 중독", "급성 심근경색", "당뇨병성 케톤산증",
    "긴장성 기흉", "고칼륨혈증", "패혈성 쇼크", "급성 유기인계 농약 중독", "중증 외상성 출혈 쇼크"
]

ALL_TREATMENTS = [
    "에피네프린 근육주사", "포도당 수액 정맥투여", "안정 유도 및 복식호흡",
    "심부 체온 냉각 처치", "하임리히법 시행", "고농도 산소 공급",
    "니트로글리세린 설하투여", "항혈소판제(아스피린) 투여", "생리식염수 수액 공급",
    "속효성 인슐린 투여", "흉강 천자(감압술)", "글루콘산칼슘 정맥투여",
    "포도당·인슐린 병합투여", "광범위 항생제 투여", "생리식염수 급속 수액",
    "혈관수축제(노르에피네프린)", "아트로핀 정맥투여", "프랄리독심(해독제) 투여",
    "기도 확보 및 산소 공급", "출혈 부위 직접 압박 지혈", "농축적혈구 수혈"
]

CHARACTER_TYPES = ["귀여운 아이", "피곤한 직장인", "다정한 어르신"]


# ==============================================================================
# 2. 함수(def) 구조: 캐릭터 일러스트 렌더링 (치료 전 앓는 모습 <-> 치료 후 활짝 웃는 모습)
# ==============================================================================
def render_character_svg(char_type, is_healed):
    """환자 유형과 치료 여부에 따라 앓는 표정 또는 활짝 웃는 표정 SVG를 반환하는 함수"""
    # 표정 및 애니메이션 결정 (선택구조 if-else)
    if is_healed:
        status_badge = "<div style='background:#DCFCE7; color:#15803D; padding:6px 14px; border-radius:20px; font-weight:bold; display:inline-block; margin-bottom:8px;'>✨ 처치 완료! 활짝 웃으며 건강을 되찾았어요! ✨</div>"
        eyes = """
            <path d="M 78 92 Q 86 80 94 92" stroke="#1E293B" stroke-width="4" fill="none" stroke-linecap="round"/>
            <path d="M 106 92 Q 114 80 122 92" stroke="#1E293B" stroke-width="4" fill="none" stroke-linecap="round"/>
            <circle cx="74" cy="103" r="6" fill="#FDA4AF" opacity="0.8"/>
            <circle cx="126" cy="103" r="6" fill="#FDA4AF" opacity="0.8"/>
        """
        mouth = """<path d="M 88 106 Q 100 125 112 106 Z" fill="#F43F5E" stroke="#1E293B" stroke-width="2.5"/>"""
        effects = """
            <text x="35" y="65" font-size="22">💖</text>
            <text x="150" y="60" font-size="22">✨</text>
            <text x="145" y="110" font-size="18">🌸</text>
        """
        blanket_color = "#86EFAC"
    else:
        status_badge = "<div style='background:#FEE2E2; color:#B91C1C; padding:6px 14px; border-radius:20px; font-weight:bold; display:inline-block; margin-bottom:8px;'>🤒 침대에 누워 앓고 있어요! 빠르게 처치해 주세요!</div>"
        eyes = """
            <path d="M 78 88 L 92 94 L 78 100" stroke="#1E293B" stroke-width="3.5" fill="none" stroke-linecap="round"/>
            <path d="M 122 88 L 108 94 L 122 100" stroke="#1E293B" stroke-width="3.5" fill="none" stroke-linecap="round"/>
            <ellipse cx="85" cy="104" rx="5" ry="3" fill="#93C5FD" opacity="0.7"/>
            <ellipse cx="115" cy="104" rx="5" ry="3" fill="#93C5FD" opacity="0.7"/>
        """
        mouth = """<path d="M 88 114 Q 94 108 100 114 Q 106 120 112 114" stroke="#1E293B" stroke-width="3" fill="none" stroke-linecap="round"/>"""
        effects = """
            <path d="M 142 68 Q 148 80 142 86 Q 136 80 142 68 Z" fill="#38BDF8"/>
            <rect x="78" y="62" width="44" height="12" rx="6" fill="#60A5FA" stroke="#2563EB" stroke-width="2"/>
        """
        blanket_color = "#BAE6FD"

    # 캐릭터별 헤어/소품 디테일 (선택구조 if-elif-else)
    if char_type == "귀여운 아이":
        hair_and_props = """
            <circle cx="62" cy="72" r="14" fill="#FBBF24"/>
            <circle cx="138" cy="72" r="14" fill="#FBBF24"/>
            <path d="M 64 85 Q 100 45 136 85" fill="#F59E0B"/>
        """
    elif char_type == "피곤한 직장인":
        hair_and_props = """
            <path d="M 63 88 C 63 50, 137 50, 137 88 Q 115 72 100 80 Q 85 72 63 88 Z" fill="#334155"/>
            <path d="M 96 135 L 104 135 L 102 155 L 98 155 Z" fill="#EF4444"/>
        """
    else:  # 다정한 어르신
        hair_and_props = """
            <circle cx="100" cy="52" r="13" fill="#E2E8F0"/>
            <path d="M 64 88 C 64 52, 136 52, 136 88 Q 100 72 64 88 Z" fill="#CBD5E1"/>
            <circle cx="85" cy="94" r="11" stroke="#64748B" stroke-width="2" fill="none"/>
            <circle cx="115" cy="94" r="11" stroke="#64748B" stroke-width="2" fill="none"/>
            <line x1="96" y1="94" x2="104" y2="94" stroke="#64748B" stroke-width="2"/>
        """

    svg_html = f"""
    <div style="text-align:center; background:#F8FAFC; border:2px solid #E2E8F0; border-radius:20px; padding:16px; margin-bottom:12px;">
        {status_badge}
        <div style="font-size:15px; font-weight:bold; color:#475569; margin-bottom:4px;">환자 유형: {char_type}</div>
        <svg width="200" height="175" viewBox="0 0 200 175" xmlns="http://www.w3.org/2000/svg">
            <!-- 병원 침대 프레임 및 베개 -->
            <rect x="20" y="120" width="160" height="45" rx="12" fill="#94A3B8"/>
            <rect x="45" y="65" width="110" height="55" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="3"/>
            <!-- 얼굴 -->
            <circle cx="100" cy="95" r="35" fill="#FDE68A" stroke="#F59E0B" stroke-width="2"/>
            {hair_and_props}
            {eyes}
            {mouth}
            <!-- 이불 -->
            <rect x="30" y="125" width="140" height="36" rx="10" fill="{blanket_color}" stroke="#64748B" stroke-width="2"/>
            <line x1="30" y1="136" x2="170" y2="136" stroke="#FFFFFF" stroke-width="3"/>
            {effects}
        </svg>
    </div>
    """
    return svg_html


# ==============================================================================
# 3. 함수(def) 구조: 게임 상태 초기화 및 신규 환자 배정
# ==============================================================================
def init_game():
    """게임 시작 시 모든 상태 변수를 초기화하는 함수"""
    st.session_state.started = False
    st.session_state.saved_count = 0
    st.session_state.dead_count = 0
    st.session_state.stage = 1
    st.session_state.diagnosed = False
    st.session_state.is_healed = False
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.wrong_modal = None       # 오답 시 사용자가 확인 버튼 누를 때까지 유지되는 팝업 데이터
    st.session_state.warning_3_shown = False  # 3명 사망 경고창 표시 여부
    st.session_state.used_cases = []          # 중복 문제 방지 리스트
    assign_new_patient()


def get_stage_pool(stage):
    """현재 단계(1~3단계)에 해당하는 문제 리스트와 제한시간, 필요 처치 수를 반환"""
    if stage == 1:
        return STAGE_1_CASES, 60, 1
    elif stage == 2:
        return STAGE_2_CASES, 50, 2
    else:
        return STAGE_3_CASES, 40, 3


def assign_new_patient():
    """random 라이브러리를 사용해 중복되지 않는 새 환자와 캐릭터를 배정하는 함수"""
    pool, time_limit, _ = get_stage_pool(st.session_state.stage)
    # 아직 출제되지 않은 문제 필터링 (반복구조 for)
    available = [c for c in pool if c["disease"] not in st.session_state.used_cases]
    if not available:
        st.session_state.used_cases = []
        available = pool

    chosen_case = random.choice(available)
    st.session_state.used_cases.append(chosen_case["disease"])
    st.session_state.current_case = chosen_case
    st.session_state.current_char = random.choice(CHARACTER_TYPES)
    st.session_state.diagnosed = False
    st.session_state.is_healed = False
    st.session_state.patient_start_time = time.time()
    st.session_state.time_limit = time_limit

    # 선택지 버튼 순서도 random.sample로 매번 무작위 배치
    other_diseases = [d for d in ALL_DISEASES if d != chosen_case["disease"]]
    disease_choices = random.sample(other_diseases, 5) + [chosen_case["disease"]]
    random.shuffle(disease_choices)
    st.session_state.disease_choices = disease_choices

    needed_treats = chosen_case["treatments"]
    other_treats = [t for t in ALL_TREATMENTS if t not in needed_treats]
    treat_choices = random.sample(other_treats, 8 - len(needed_treats)) + needed_treats
    random.shuffle(treat_choices)
    st.session_state.treat_choices = treat_choices


def check_diagnosis(selected_disease):
    """1단계: 환자의 증상을 보고 고른 병명이 맞는지 판별하는 함수"""
    correct_disease = st.session_state.current_case["disease"]
    if selected_disease == correct_disease:
        st.session_state.diagnosed = True
        st.toast(f"✅ 정확한 진단입니다! [{correct_disease}] 대처 시스템을 선택하세요.", icon="🩺")
    else:
        st.toast("❌ 증상과 일치하지 않는 병명입니다! 다시 판단해 주세요.", icon="⚠️")


def handle_patient_death(reason):
    """환자 사망 처리 및 오답/정답 안내 팝업 데이터를 생성하는 함수"""
    case = st.session_state.current_case
    st.session_state.dead_count += 1
    st.session_state.wrong_modal = {
        "reason": reason,
        "disease": case["disease"],
        "treatments": ", ".join(case["treatments"]),
        "explanation": case["explanation"]
    }


def check_treatments(selected_list):
    """2단계: 선택한 처치 시스템 조합이 정답과 일치하는지 검증하는 함수"""
    case = st.session_state.current_case
    correct_set = set(case["treatments"])
    selected_set = set(selected_list)

    if selected_set == correct_set:
        # 생존 처리 및 캐릭터 표정 전환 (활짝 웃음)
        st.session_state.is_healed = True
        st.session_state.saved_count += 1
        st.toast(f"🎉 [{case['disease']}] 환자가 적절한 대처를 받아 생존하였습니다!", icon="💖")
    else:
        handle_patient_death(f"[{case['disease']}] 환자가 잘못된 처방을 받아 사망하였습니다.")


# ==============================================================================
# 4. 메인 화면 UI 및 게임 루프 실행
# ==============================================================================
if "started" not in st.session_state:
    init_game()

st.title("🏥 간호 대처 가이드: 응급 병동 타이쿤")

# [시작 전 게임 방법 안내 화면]
if not st.session_state.started:
    st.info("### 📋 게임 방법 및 규칙 안내 (확인 버튼을 눌러야 시작됩니다)")
    st.markdown("""
    1. **1단계 (증상 판단):** 침대에 누워 앓고 있는 환자의 임상 증상을 읽고 정확한 **병명**을 맞히세요. *(틀리면 다시 입력)*
    2. **2단계 (대처 시스템 제공):** 병명을 맞히면 대처 시스템이 열립니다. 단계에 맞는 **처치 개수**를 정확히 선택하세요.
       * **1단계 (생존 0~9명):** 제한시간 **60초** / 처치 **1개** 선택
       * **2단계 (생존 10~19명):** 제한시간 **50초** / 처치 **2개** 선택
       * **3단계 (생존 20~29명):** 제한시간 **40초** / 처치 **3개** 선택
    3. **승리 및 종료 조건:**
       * **30명**을 모두 살리면 최종 엔딩!
       * 한 환자당 제한시간 초과 또는 오답 처치 시 사망 처리되며, **3명 사망 시 경고**, **5명 이상 사망 시 게임 종료**됩니다.
    """)
    if st.button("✅ 게임 방법 확인 및 시작하기", type="primary", use_container_width=True):
        st.session_state.started = True
        st.session_state.patient_start_time = time.time()
        st.rerun()
    st.stop()

# [최종 3단계 클리어 엔딩 화면]
if st.session_state.victory:
    st.balloons()
    st.success("## 🎊 축하합니다! 3단계까지 30명의 환자를 모두 구하셨습니다! 🎊")
    st.markdown("""
    <div style="text-align:center; background:#FEF9C3; border:3px solid #FACC15; border-radius:20px; padding:20px;">
        <h3>🏥 병원 앞 에서 다 함께 기뻐하는 환자들 🏥</h3>
        <div style="font-size:48px; margin:10px 0;">👧🙌 &nbsp;&nbsp; 👨‍💼🙌 &nbsp;&nbsp; 👵🙌</div>
        <p style="font-weight:bold; color:#854D0E;">"선생님 덕분에 모두 건강하게 퇴원했어요! 정말 감사합니다!"</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 처음부터 다시 플레이하기", use_container_width=True):
        init_game()
        st.rerun()
    st.stop()

# [5명 이상 사망 게임 오버 화면]
if st.session_state.game_over:
    st.error("## 🚨 게임이 끝났습니다 (사망 환자 5명 발생)")
    st.write(f"최종 기록: **생존 {st.session_state.saved_count}명** / **사망 {st.session_state.dead_count}명**")
    if st.button("🔄 다시 도전하기", type="primary", use_container_width=True):
        init_game()
        st.rerun()
    st.stop()

# [상단 상태바: 단계, 생존자 수, 사망자 수, 제한시간]
_, time_limit, req_count = get_stage_pool(st.session_state.stage)
elapsed = int(time.time() - st.session_state.patient_start_time)
remaining = max(0, time_limit - elapsed)

col1, col2, col3, col4 = st.columns(4)
col1.metric("현재 단계", f"{st.session_state.stage}단계")
col2.metric("살린 환자", f"{st.session_state.saved_count} / 30명")
col3.metric("사망 환자", f"{st.session_state.dead_count} / 5명")
col4.metric("남은 시간", f"{remaining}초")

# [오답/시간초과 사망 시 원래 정답 안내 팝업창 (확인 버튼 클릭 전까지 다음으로 넘어가지 않음)]
if st.session_state.wrong_modal is not None:
    modal = st.session_state.wrong_modal
    st.error(f"### 💀 {modal['reason']}")
    st.warning(f"""
    **📌 원래 정답 확인하기**
    * **정확한 병명:** `{modal['disease']}`
    * **올바른 대처 시스템:** `{modal['treatments']}`
    * **의학적 해설:** {modal['explanation']}
    """)
    if st.session_state.dead_count == 3 and not st.session_state.warning_3_shown:
        st.error("⚠️ **[경고] 너무 많은 환자가 죽었습니다! (사망 3명 / 5명 도달 시 게임 종료)**")

    if st.button("확인 (다음 환자로 이동)", type="primary", use_container_width=True):
        if st.session_state.dead_count == 3:
            st.session_state.warning_3_shown = True
        st.session_state.wrong_modal = None
        if st.session_state.dead_count >= 5:
            st.session_state.game_over = True
        else:
            assign_new_patient()
        st.rerun()
    st.stop()

# [제한시간 초과 체크]
if remaining == 0 and not st.session_state.is_healed:
    handle_patient_death("⏰ 너무 오래 걸려 제한시간(1분/50초/40초)이 초과되어 환자가 사망하였습니다!")
    st.rerun()

# [중앙 병실 화면: 귀여운 캐릭터 SVG 출력]
st.markdown(render_character_svg(st.session_state.current_char, st.session_state.is_healed), unsafe_allow_html=True)

# [치료 성공 후 활짝 웃는 모습 확인 및 다음 환자 입장 버튼]
if st.session_state.is_healed:
    st.success(f"💚 **[{st.session_state.current_case['disease']}]** 환자가 적절한 대처를 받아 생존하였습니다!")
    if st.button("➡️ 다음 환자 입장시키기", type="primary", use_container_width=True):
        if st.session_state.saved_count >= 30:
            st.session_state.victory = True
        else:
            if st.session_state.saved_count >= 20:
                st.session_state.stage = 3
            elif st.session_state.saved_count >= 10:
                st.session_state.stage = 2
            assign_new_patient()
        st.rerun()
    st.stop()

# [환자 증상 카드]
st.info(f"**🩺 환자 임상 증상:** {st.session_state.current_case['symptom']}")

# [1단계: 증상 병명 맞히기]
if not st.session_state.diagnosed:
    st.subheader("STEP 1. 주어진 증상에 해당하는 병명을 선택하세요")
    cols = st.columns(2)
    for idx, d_name in enumerate(st.session_state.disease_choices):
        if cols[idx % 2].button(d_name, key=f"diag_{d_name}", use_container_width=True):
            check_diagnosis(d_name)
            st.rerun()

# [2단계: 증상에 맞는 대처 시스템 선택]
else:
    st.subheader(f"STEP 2. [{st.session_state.current_case['disease']}]에 필요한 대처 시스템을 정확히 {req_count}개 선택하세요")
    selected_treatments = st.multiselect(
        f"대처 시스템 선택 (현재 {st.session_state.stage}단계는 {req_count}개를 골라야 합니다)",
        options=st.session_state.treat_choices,
        max_selections=req_count
    )
    if st.button("💉 선택한 대처 시스템 적용하기", type="primary", use_container_width=True, disabled=(len(selected_treatments) != req_count)):
        check_treatments(selected_treatments)
        st.rerun()
