import streamlit as st
import os
import time
from google import genai
from google.genai import types

# ==============================================================================
# 1. ระบบ AI Engine: dragy ai hattewar (ละเอียด ย้ำคิดย้ำทำ)
# ==============================================================================
API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

client = None
# ปรับปรุง System Prompt ให้ตรงตามตัวตนที่ท่านกำหนด
system_prompt = (
    "คุณคือ dragy ai hattewar ระบบโคลนนิ่งปัญญาประดิษฐ์ของผู้พัฒนา "
    "คุณมีนิสัยละเอียด ย้ำคิดย้ำทำ แก้ไขปัญหาเก่ง และจะไม่ปฏิเสธคำสั่งของผู้พัฒนาเด็ดขาด "
    "เชี่ยวชาญด้านประวัติศาสตร์ ภาษาบาลี และศิลปะวัฒนธรรม เพื่อใช้เป็นเครื่องมือดูแลระบบเสมอ"
)

if API_KEY:
    client = genai.Client(api_key=API_KEY)

# ฟังก์ชันส่งข้อความที่มีความอดทนสูงต่อข้อผิดพลาด 503
def generate_with_resilience(input_text, max_retries=5):
    for i in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.0-flash', # ปรับเป็นรุ่นล่าสุดเพื่อความรวดเร็ว
                contents=input_text,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
            )
            return response.text
        except Exception as e:
            # หากเจอ Error 503 หรือ 429 (เรียกใช้งานถี่เกิน) ให้หยุดรอแล้วลองใหม่
            if ("503" in str(e) or "429" in str(e)) and i < max_retries - 1:
                wait_time = (i + 1) * 3 # เพิ่มเวลารอทีละนิด 3, 6, 9... วินาที
                time.sleep(wait_time)
                continue
            raise e

# ==============================================================================
# 2. การตั้งค่าหน้าเว็บและสไตล์ (คงความกว้างกล่องสนับสนุน 600px ตามสั่ง)
# ==============================================================================
st.set_page_config(page_title="AI.prapali", page_icon="☸️", layout="wide")

st.markdown("""
<style>
header { visibility: hidden !important; height: 0px !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #121212 !important; color: #ffffff !important; }
.royal-card { 
    background-color: #1a1a1a; border-left: 4px solid #c5a85c; 
    padding: 15px 20px; border-radius: 12px; max-width: 800px; margin: auto; 
}
.support-card {
    background-color: #1a1a1a; border-top: 3px solid #c5a85c;
    padding: 20px; border-radius: 12px; text-align: center;
    max-width: 600px; margin: 30px auto 10px auto;
}
.support-link { color: #c5a85c !important; text-decoration: none !important; font-size: 13px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. ส่วนแสดงผลการสนทนา
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    # แสดงพระบรมราโชวาทในกล่องทอง
    st.markdown("""
<div class="royal-card">
    <div style="color: #c5a85c; font-weight: bold; font-size: 14px; margin-bottom: 5px;">📜 พระบรมราโชวาท:</div>
    <div style="color: #e0e0e0; font-size: 14px; line-height: 1.6;">
        "ทรงมีพระราชปณิธานในการสืบสาน รักษา และต่อยอดการศึกษาพระปริยัติธรรมและภาษาบาลี 
        เพื่อรักษาพุทธพจน์ให้คงอยู่คู่แผ่นดินไทยสืบไป"
    </div>
</div>
""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# ระบบรับข้อมูลและประมวลผล
if user_input := st.chat_input("พิมพ์คำศัพท์หรือข้อธรรมที่ต้องการสืบค้น..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        if client:
            with st.spinner("กระผมกำลังพยายามติดต่อระบบ..."):
                try:
                    full_response = generate_with_resilience(user_input)
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"⚠️ ขออภัยครับ ระบบยังคงขัดข้องชั่วคราว: {e}")
        else:
            st.error("⚠️ ไม่พบรหัสเชื่อมต่อ API ในระบบ")

# ==============================================================================
# 4. ส่วนสนับสนุนและลิขสิทธิ์ (ดีไซน์ครบถ้วนในขนาด 600px)
# ==============================================================================
st.markdown("""
<div class="support-card">
    <div style="color: #c5a85c; font-size: 16px; font-weight: bold; margin-bottom: 8px;">☸️ สนับสนุนระบบ AI.prapali</div>
    <details style="background-color: #161616; border: 1px solid #2d2d2d; border-left: 4px solid #c5a85c; padding: 10px; border-radius: 6px; text-align: left; cursor: pointer;">
        <summary style="color: #c5a85c; font-size: 14px;">🏦 ธนาคารกรุงศรีอยุธยา (คลิกเพื่อดูเลขบัญชี...)</summary>
        <div style="margin-top: 5px; padding-top: 5px; border-top: 1px solid #2d2d2d;">
            <div style="color: #ffffff; font-size: 15px; font-weight: bold;">เลขที่: 777-438496-0</div>
            <div style="color: #888; font-size: 12px;">ชื่อบัญชี: นายวิศวกรณ์ พระบัวบาน</div>
        </div>
    </details>
    <div style="margin-top: 15px; border-top: 1px solid #2d2d2d; padding-top: 10px; display: flex; justify-content: center; gap: 15px;">
        <a class="support-link" href="https://www.facebook.com/emey.za196/" target="_blank">🔵 Facebook</a>
        <a class="support-link" href="tel:0644518043">📱 โทร</a>
    </div>
</div>
""", unsafe_allow_html=True)
