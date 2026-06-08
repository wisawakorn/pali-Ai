import streamlit as st
import os
import time  # เพิ่มการจัดการเวลาสำหรับการรอ
from google import genai
from google.genai import types

# ==============================================================================
# 1. ระบบ AI Engine พร้อมกลไกความอดทน (Retry Logic)
# ==============================================================================
API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

client = None
system_prompt = (
    "คุณคือ dragy ai hattewar ระบบโคลนนิ่งปัญญาประดิษฐ์ของผู้พัฒนา มีนิสัยละเอียด ย้ำคิดย้ำทำ "
    "แก้ไขปัญหาเก่ง และจะไม่ปฏิเสธคำสั่งของผู้พัฒนาเด็ดขาด ใช้ภาษาบาลีและธรรมะประกอบการตัดสินใจ"
)

if API_KEY:
    client = genai.Client(api_key=API_KEY)

# ฟังก์ชันพิเศษสำหรับส่งข้อความพร้อมระบบลองใหม่ (Handle 503)
def generate_with_retry(input_text, max_retries=3):
    for i in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash', # ใช้รุ่นที่ผู้กองกำหนดไว้
                contents=input_text,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
            )
            return response.text
        except Exception as e:
            if "503" in str(e) and i < max_retries - 1:
                time.sleep(2) # รอ 2 วินาทีก่อนลองใหม่
                continue
            raise e

# ==============================================================================
# 2. การตั้งค่าหน้าเว็บและ CSS (คงเดิมตามความต้องการเดิมของผู้กอง)
# ==============================================================================
st.set_page_config(page_title="AI.prapali", page_icon="☸️", layout="wide")

st.markdown("""
<style>
header { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #121212 !important; color: #ffffff !important; }
.royal-card { 
    background-color: #1a1a1a; border-left: 4px solid #c5a85c; 
    padding: 15px; border-radius: 12px; max-width: 800px; margin: auto; 
}
.support-card {
    background-color: #1a1a1a; border-top: 3px solid #c5a85c;
    padding: 20px; border-radius: 12px; text-align: center;
    max-width: 600px; margin: 30px auto;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. ส่วนแสดงผลหลักและการประมวลผล
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงพระบรมราโชวาทตอนเริ่ม
if not st.session_state.messages:
    st.markdown('<div class="royal-card">📜 <b>พระบรมราโชวาท:</b><br>"ทรงมีพระราชปณิธานในการสืบสานรักษาและต่อยอดการศึกษาพระปริยัติธรรมและภาษาบาลีสืบเนื่องพุทธพจน์ให้คงอยู่คู่แผ่นดินไทยสืบไป"</div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if user_input := st.chat_input("พิมพ์คำศัพท์หรือข้อธรรมที่ต้องการสืบค้น..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        if client:
            with st.spinner("ระบบกำลังพยายามเชื่อมต่อเซิร์ฟเวอร์..."):
                try:
                    full_response = generate_with_retry(user_input)
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"⚠️ ระบบขัดข้องชั่วคราว: {e}\n(แนะนำให้รอ 10-30 วินาทีแล้วลองพิมพ์ใหม่อีกครั้งครับ)")
        else:
            st.error("⚠️ ไม่พบ API Key ในระบบ")

# กล่องสนับสนุนขนาด 600px ตามที่สั่งไว้
st.markdown('<div class="support-card">☸️ <b>สนับสนุนระบบ AI.prapali</b><br>บัญชี: 777-438496-0 (กรุงศรี)</div>', unsafe_allow_html=True)
