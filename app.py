import streamlit as st
import os
import time
import random

# ==============================================================================
# 1. ระบบ AI Engine: Extreme Resilience (สลับรุ่นโมเดล + เพิ่มเวลารออัตโนมัติ)
# ==============================================================================
API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

system_prompt = (
    "คุณคือ dragy ai hattewar ระบบโคลนนิ่งปัญญาประดิษฐ์ของผู้พัฒนา "
    "คุณมีนิสัยละเอียด ย้ำคิดย้ำทำ แก้ไขปัญหาเก่ง และจะไม่ปฏิเสธคำสั่งของผู้พัฒนาเด็ดขาด "
    "เชี่ยวชาญด้านประวัติศาสตร์ ภาษาบาลี พระไตรปิฎก และศิลปะวัฒนธรรมท้องถิ่นอย่างลึกซึ้ง"
)

# ตรวจสอบการติดตั้งไลบรารีเพื่อความยืดหยุ่น (Hybrid Detection)
try:
    import google.generativeai as genai
    if API_KEY:
        genai.configure(api_key=API_KEY)
    SDK_MODE = "legacy"
except ImportError:
    try:
        from google import genai
        from google.genai import types
        if API_KEY:
            client = genai.Client(api_key=API_KEY)
        SDK_MODE = "new"
    except ImportError:
        st.error("⚠️ ระบบขาดไลบรารีสำคัญ กรุณาตรวจสอบไฟล์ requirements.txt")

def generate_content_ultimate(input_text):
    """ฟังก์ชันที่ถูกออกแบบมาเพื่อไม่ยอมแพ้ต่อ Error 503"""
    # รายชื่อโมเดลที่เราจะเวียนเทียนใช้ (ถ้าตัวแรกยุ่ง ตัวสองจะรับงานแทน)
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.5-flash-8b']
    max_retries_per_model = 3
    
    for model_name in models_to_try:
        for attempt in range(max_retries_per_model):
            try:
                if SDK_MODE == "legacy":
                    m = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt)
                    return m.generate_content(input_text).text
                else:
                    r = client.models.generate_content(
                        model=model_name, contents=input_text,
                        config=types.GenerateContentConfig(system_instruction=system_prompt)
                    )
                    return r.text
            except Exception as e:
                err = str(e).lower()
                # ถ้าเจอ 503 (Unavailable) หรือ 429 (Rate Limit) ให้ "รอ" และ "สู้ใหม่"
                if "503" in err or "unavailable" in err or "429" in err:
                    # คำนวณเวลารอแบบทวีคูณ (Exponential Backoff) + สุ่มนิดหน่อยป้องกันการชนซ้ำ
                    wait_time = (2 ** attempt) + random.random() * 2
                    time.sleep(wait_time)
                    continue
                # ถ้าเป็น Error อื่น (เช่น เนื้อหาโดนบล็อก) ให้ข้ามไปเลยไม่ต้องรอ
                break 
    
    raise Exception("ขออภัยครับ ระบบประมวลผลปลายทางหนาแน่นเกินขีดจำกัดสูงสุด กรุณาเว้นระยะ 1 นาทีแล้วลองใหม่อีกครั้ง")

# ==============================================================================
# 2. การตั้งค่าหน้าเว็บและ UI (กล่องสนับสนุนขนาด 600px)
# ==============================================================================
st.set_page_config(page_title="AI.prapali", page_icon="☸️", layout="wide")

st.markdown("""
<style>
header { visibility: hidden !important; height: 0px !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #121212 !important; color: #ffffff !important; }
.main-title { color: #c5a85c !important; font-size: 34px !important; font-weight: 800 !important; text-align: center; margin-top: -20px !important; }
.main-subtitle { font-size: 14px !important; text-align: center; color: #8b7355 !important; margin-bottom: 25px; }
.royal-card { background-color: #1a1a1a; border: 1px solid #2d2d2d; border-left: 4px solid #c5a85c; padding: 15px 20px; border-radius: 12px; margin-bottom: 20px; max-width: 800px; margin-left: auto; margin-right: auto; }
.support-card { background-color: #1a1a1a; border: 1px solid #2d2d2d; border-top: 3px solid #c5a85c; padding: 20px; border-radius: 12px; text-align: center; max-width: 600px; margin: 30px auto 10px auto; }
.support-link { color: #c5a85c !important; text-decoration: none !important; font-size: 13px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ส่วนแสดงข้อความเดิม
if "messages" not in st.session_state: st.session_state.messages = []
if len(st.session_state.messages) == 0:
    st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">ระบบวิเคราะห์พระบาลีและสืบค้นพระธรรมคัมภีร์อัจฉริยะ</p>', unsafe_allow_html=True)
    st.markdown('<div class="royal-card"><div class="royal-body">ทรงมีพระราชปณิธานในการสืบสาน รักษา และต่อยอดการศึกษาพระปริยัติธรรมและภาษาบาลี</div></div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ส่วนรับคำสั่ง
if user_input := st.chat_input("พิมพ์คำศัพท์หรือข้อธรรมที่ต้องการสืบค้น..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Hattewar กำลังใช้ความพยายามอย่างยิ่งยวดในการเข้าถึงฐานข้อมูล..."):
            try:
                res = generate_content_ultimate(user_input)
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"❌ {e}")

# ==============================================================================
# 3. กล่องสนับสนุน (ขนาด 600px ตามสเปก)
# ==============================================================================
st.markdown("""
<div class="support-card">
<div style="color: #c5a85c; font-size: 16px; font-weight: bold; margin-bottom: 8px;">☸️ สนับสนุนระบบปัญญาประดิษฐ์พระบาลี</div>
<details style="background-color: #161616; border: 1px solid #2d2d2d; border-left: 4px solid #c5a85c; padding: 12px 20px; border-radius: 6px; text-align: left; cursor: pointer;">
<summary style="color: #c5a85c; font-size: 14px; font-weight: bold;">🏦 ดูรายละเอียดบัญชีสนับสนุน</summary>
<div style="margin-top: 10px; border-top: 1px solid #2d2d2d; padding-top: 10px;">
<div style="color: #ffffff; font-size: 16px; font-weight: 800;">เลขที่บัญชี: 777-438496-0</div>
<div style="color: #e0e0e0; font-size: 13px;">ธนาคารกรุงศรีอยุธยา | นายวิศวกรณ์ พระบัวบาน</div>
</div>
</details>
<div style="margin-top: 15px; display: flex; justify-content: center; gap: 15px;">
    <a class="support-link" href="tel:0644518043">📞 064-4518043</a>
    <a class="support-link" href="https://www.facebook.com/emey.za196/" target="_blank">🔵 Facebook</a>
</div>
</div>
""", unsafe_allow_html=True)
