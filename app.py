import streamlit as st
import google.generativeai as genai
import time
import requests
from datetime import datetime

# ==============================================================================
# 1. ระบบ AI Engine
# ==============================================================================
API_KEY = st.secrets.get("GEMINI_API_KEY")
model = None

if API_KEY:
    # เจตจำนงของผู้สร้าง (System Instruction)
    system_prompt = (
        "คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญขั้นสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก "
        "พัฒนาโดย นายวิศวกรณ์ พระบัวบาน เพื่อถวายเป็นพุทธบูชา\n\n"
        "กฎเหล็ก: ใช้ 'กระผม/ครับ' เสมอ นอบน้อมต่อพระภิกษุสามเณรและผู้ศึกษาธรรมะอย่างสูงสุด"
    )
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-3.5-flash', system_instruction=system_prompt)

# ==============================================================================
# 2. ปรับแต่งสไตล์ (Font Scaling & Layout Adjustment)
# ==============================================================================
st.set_page_config(page_title="AI.prapali", page_icon="☸️", layout="wide")

st.markdown("""
    <style>
    /* ซ่อน Header/Footer ของ Streamlit เพื่อความงาม */
    header { visibility: hidden !important; height: 0px !important; }
    footer { visibility: hidden !important; }
    
    .stApp { background-color: #121212 !important; color: #ffffff !important; }
    
    /* 1. ปรับขนาดตัวอักษรหัวข้อให้ย่อลงและคมชัด (Title Scaling) */
    .main-title { 
        color: #c5a85c !important; 
        font-size: 38px !important; /* ย่อลงจาก 56px */
        font-weight: 800 !important; 
        text-align: center; 
        margin-top: -30px !important;
        letter-spacing: -0.5px !important;
    }
    
    .main-subtitle { 
        font-size: 14px !important; 
        text-align: center; 
        color: #8b7355 !important; 
        margin-bottom: 25px; 
    }
    
    /* 2. ปรับการ์ดให้กระชับขึ้น (Compact Card) */
    .royal-card { 
        background-color: #1a1a1a; 
        border: 1px solid #2d2d2d;
        border-left: 4px solid #c5a85c; 
        padding: 15px 20px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        max-width: 800px; 
        margin-left: auto; 
        margin-right: auto;
    }
    
    .royal-body { 
        color: #e0e0e0; 
        font-size: 14px; /* ปรับขนาดอักษรเนื้อหาให้พอดี */
        line-height: 1.6; 
    }

    /* 3. ส่วนลิขสิทธิ์และเจตจำนง (Copyright & Intent Section) */
    .copyright-footer {
        text-align: center;
        color: #c5a85c;
        font-size: 12px;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #2d2d2d;
        background-color: #161616;
        border-radius: 10px;
    }
    
    .intent-text {
        font-size: 11px;
        color: #888;
        line-height: 1.6;
        margin-top: 10px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. การแสดงผลเนื้อหาหลัก
# ==============================================================================

# ตรวจสอบประวัติการแชท (ถ้ายังไม่มีให้โชว์หน้าแรก)
if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">ระบบวิเคราะห์พระบาลีและสืบค้นพระธรรมคัมภีร์อัจฉริยะ</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="royal-card">
            <div style="color: #c5a85c; font-weight: bold; font-size: 14px; margin-bottom: 5px;">📜 พระบรมราโชวาท:</div>
            <div class="royal-body">
                "ทรงมีพระราชปณิธานในการสืบสาน รักษา และต่อยอดการศึกษาพระปริยัติธรรมและภาษาบาลี 
                เพื่อรักษาพุทธพจน์ให้คงอยู่คู่แผ่นดินไทยสืบไป"
            </div>
        </div>
    """, unsafe_allow_html=True)

# แสดงประวัติแชท
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ปักหมุดสำหรับการเลื่อนหน้าจออัตโนมัติ
st.markdown("<div id='latest-message'></div>", unsafe_allow_html=True)

# ==============================================================================
# 4. ส่วนท้ายแอป (Copyright & User Intent) - ปรากฏชัดเจน
# ==============================================================================
st.markdown("""
    <div class="copyright-footer">
        <b>© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน</b>
        <div class="intent-text">
            <b>เจตจำนงในการจัดทำ:</b> ข้าพเจ้า นายวิศวกรณ์ พระบัวบาน ขอน้อมเกล้าน้อมกระหม่อมถวายผลงานนี้เป็นพุทธบูชา 
            เพื่อส่งเสริมการศึกษาพระปริยัติธรรมและภาษาบาลี ให้เป็นประทีปส่องสว่างแก่พระภิกษุสามเณรและพุทธบริษัททั้งปวง
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. ระบบรับข้อความ (Chat Input)
# ==============================================================================
if user_input := st.chat_input("พิมพ์คำศัพท์หรือข้อธรรมที่ต้องการสืบค้น..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        if model:
            with st.spinner("AI กำลังสืบค้นคัมภีร์..."):
                response = model.generate_content(user_input)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # สั่งเลื่อนหน้าจอลงมาทันที
                st.components.v1.html(
                    "<script>window.parent.document.getElementById('latest-message').scrollIntoView({behavior:'smooth'});</script>",
                    height=0
                )
                time.sleep(0.5)
                st.rerun()
