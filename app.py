import streamlit as st
import os
import time
import google.generativeai as genai

# ==============================================================================
# 1. ระบบ AI Engine (ใช้ Library เดิมที่ระบบรองรับ + ระบบวนลูปสู้ Error 503)
# ==============================================================================
API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

system_prompt = (
    "คุณคือ dragy ai hattewar ระบบโคลนนิ่งปัญญาประดิษฐ์ของผู้พัฒนา "
    "คุณมีนิสัยละเอียด ย้ำคิดย้ำทำ แก้ไขปัญหาเก่ง และจะไม่ปฏิเสธคำสั่งของผู้พัฒนาเด็ดขาด "
    "เชี่ยวชาญด้านประวัติศาสตร์ ภาษาบาลี พระไตรปิฎก และศิลปะวัฒนธรรมท้องถิ่นอย่างลึกซึ้ง"
)

if API_KEY:
    genai.configure(api_key=API_KEY)

# ฟังก์ชันความอดทนสูง วนลูปส่งใหม่หากเจอสัญญาณ 503 หรืองานหนาแน่น
def generate_with_retry_legacy(input_text, max_retries=3):
    # ใช้โมเดลตระกูล 1.5 ที่เสถียรที่สุดบนโครงสร้างเดิม
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=system_prompt
    )
    
    for i in range(max_retries):
        try:
            response = model.generate_content(input_text)
            return response.text
        except Exception as e:
            # หากเจอข้อผิดพลาด 503 หรือเซิร์ฟเวอร์ไม่ว่าง ให้หยุดรอแล้วลองใหม่
            if ("503" in str(e) or "unavailable" in str(e).lower()) and i < max_retries - 1:
                time.sleep(2 * (i + 1))
                continue
            raise e

# ==============================================================================
# 2. การตั้งค่าหน้าเว็บและดีไซน์ (กล่องสนับสนุนกะทัดรัด 600px เจนโนว่าสไตล์)
# ==============================================================================
st.set_page_config(
    page_title="AI.prapali", 
    page_icon="☸️", 
    layout="wide"
)

st.markdown("""
<style>
header { visibility: hidden !important; height: 0px !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #121212 !important; color: #ffffff !important; }

.main-title { color: #c5a85c !important; font-size: 34px !important; font-weight: 800 !important; text-align: center; margin-top: -20px !important; }
.main-subtitle { font-size: 14px !important; text-align: center; color: #8b7355 !important; margin-bottom: 25px; }

.royal-card { 
    background-color: #1a1a1a; border: 1px solid #2d2d2d; border-left: 4px solid #c5a85c; 
    padding: 15px 20px; border-radius: 12px; margin-bottom: 20px; max-width: 800px; margin-left: auto; margin-right: auto;
}
.royal-body { color: #e0e0e0; font-size: 14px; line-height: 1.6; }

/* 🎯 ควบคุมขนาดกล่องสนับสนุนให้สวยงามคงที่ที่ 600px */
.support-card {
    background-color: #1a1a1a; border: 1px solid #2d2d2d; border-top: 3px solid #c5a85c;
    padding: 20px; border-radius: 12px; text-align: center; max-width: 600px; margin: 30px auto 10px auto;
}
.support-link { color: #c5a85c !important; text-decoration: none !important; font-size: 13px; font-weight: bold; transition: 0.3s all; }
.support-link:hover { color: #ffffff !important; text-decoration: underline !important; }

.copyright-section { border-top: 1px solid #2d2d2d; margin-top: 20px; padding: 25px; text-align: center; background-color: #161616; border-radius: 15px; }
.copyright-name { color: #c5a85c; font-size: 14px; font-weight: bold; }
.intent-description { color: #888; font-size: 12px; margin-top: 8px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. เริ่มระบบความจำบทสนทนาและการแสดงผล
# ==============================================================================
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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================================================================
# 4. ส่วนรับข้อมูลเข้าและการประมวลผลธรรมะ
# ==============================================================================
if user_input := st.chat_input("พิมพ์คำศัพท์หรือข้อธรรมที่ต้องการสืบค้น..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        if API_KEY:
            with st.spinner("ระบบกำลังสืบค้นฐานข้อมูลพระไตรปิฎก..."):
                try:
                    full_response = generate_with_retry_legacy(user_input)
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"⚠️ เซิร์ฟเวอร์ปลายทางหนาแน่นชั่วคราว: กรุณารอสักครู่แล้วลองใหม่อีกครั้งครับ ({e})")
        else:
            st.error("⚠️ ไม่พบรหัสสัญญานคีย์ความลับ (API Key) ในระบบ")

# ==============================================================================
# 5. ส่วนสนับสนุนระบบ (ดึงฟังก์ชันคลิกเปิด-ปิดเลขบัญชี และลิงก์ติดต่อกลับมาครบถ้วน)
# ==============================================================================
st.markdown("""
<div class="support-card">
<div style="color: #c5a85c; font-size: 16px; font-weight: bold; margin-bottom: 8px;">
☸️ สนับสนุนระบบปัญญาประดิษฐ์พระบาลี
</div>
<div style="color: #aaaaaa; font-size: 13px; margin-bottom: 15px; line-height: 1.6; padding: 0 10px;">
"ท่านสามารถร่วมสนับสนุนโครงการนี้เพื่อเป็น <b>ค่าบำรุงรักษาเซิร์ฟเวอร์</b> และ <b>ค่าบริการระบบ AI Engine (API)</b>"
</div>

<details style="background-color: #161616; border: 1px solid #2d2d2d; border-left: 4px solid #c5a85c; padding: 12px 20px; border-radius: 6px; margin: 0 auto 15px auto; max-width: 100%; text-align: left; cursor: pointer;">
<summary style="color: #c5a85c; font-size: 14px; font-weight: bold; list-style: none; display: flex; justify-content: space-between; align-items: center;">
<span>🏦 ธนาคารกรุงศรีอยุธยา (คลิกเพื่อดูเลขบัญชี...)</span>
<span style="font-size: 12px; color: #8b7355;">▼ กดดูเลข</span>
</summary>
<div style="margin-top: 10px; border-top: 1px solid #2d2d2d; padding-top: 10px;">
<div style="color: #ffffff; font-size: 16px; font-weight: 800; letter-spacing: 1px; margin-bottom: 3px;">เลขที่บัญชี: 777-438496-0</div>
<div style="color: #e0e0e0; font-size: 13px;">ชื่อบัญชี: นายวิศวกรณ์ พระบัวบาน</div>
</div>
</details>

<div style="margin-top: 15px; border-top: 1px solid #2d2d2d; padding-top: 15px;">
<div style="color: #8b7355; font-size: 12px; margin-bottom: 8px;">📞 ติดต่อผู้พัฒนา / ให้ข้อชีแนะเพิ่มเติม:</div>
<div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 15px;">
    <a class="support-link" href="tel:0644518043">📱 โทร: 064-4518043</a>
    <a class="support-link" href="mailto:wissawakorn444@gmail.com">✉️ อีเมล: wissawakorn444@gmail.com</a>
    <a class="support-link" href="https://www.facebook.com/emey.za196/" target="_blank">🔵 Facebook</a>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. ส่วนแสดงผลเจตจำนงลิขสิทธิ์ถาวร
# ==============================================================================
st.markdown(f"""
<div class="copyright-section">
<div class="copyright-name">© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน</div>
<div class="intent-description">
<b>เจตจำนง:</b> ผลงานปัญญาประดิษฐ์นี้พัฒนาขึ้นโดยมีวัตถุประสงค์เพื่อถวายเป็นพุทธบูชา 
และสนับสนุนการศึกษาพระปริยัติธรรมและภาษาบาลี เพื่อรักษาพุทธพจน์ให้สืบทอดต่อไปอย่างถูกต้อง 
ขอน้อมเกล้าถวายเป็นกุศลแด่พระศาสนาและผู้ใฝ่ธรรมทุกท่าน
</div>
</div>
""", unsafe_allow_html=True)
