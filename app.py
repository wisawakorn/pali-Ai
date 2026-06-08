import streamlit as st
import os
from google import genai
from google.genai import types

# ==============================================================================
# 1. ระบบ AI Engine (ดึงค่าจากระบบ Environment Variable หรือ Secrets)
# ==============================================================================
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets.get("GEMINI_API_KEY")
    except:
        API_KEY = None

client = None
system_prompt = (
    "คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญขั้นสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก "
    "พัฒนาโดย นายวิศวกรณ์ พระบัวบาน เพื่อถวายเป็นพุทธบูชา\n\n"
    "กฎเหล็ก: ใช้ 'กระผม/ครับ' เสมอ นอบน้อมต่อพระภิกษุสามเณรและผู้ศึกษาธรรมะอย่างสูงสุด"
)

if API_KEY:
    client = genai.Client(api_key=API_KEY)

# ==============================================================================
# 2. การตั้งค่าหน้าเว็บ
# ==============================================================================
st.set_page_config(
    page_title="AI.prapali", 
    page_icon="☸️", 
    layout="wide"
)

# ==============================================================================
# 3. ปรับแต่งสไตล์ CSS (ธีมดำ-ทอง Jenova Style + ซ่อนส่วนเกิน + กล่องสนับสนุน)
# ==============================================================================
st.markdown("""
<style>
header { visibility: hidden !important; height: 0px !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #121212 !important; color: #ffffff !important; }

.main-title { 
    color: #c5a85c !important; 
    font-size: 34px !important; 
    font-weight: 800 !important; 
    text-align: center; 
    margin-top: -20px !important;
}

.main-subtitle { 
    font-size: 14px !important; 
    text-align: center; 
    color: #8b7355 !important; 
    margin-bottom: 25px; 
}

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
    font-size: 14px; 
    line-height: 1.6; 
}

/* การ์ดสนับสนุนและช่องทางติดต่อ */
.support-card {
    background-color: #1a1a1a;
    border: 1px solid #2d2d2d;
    border-top: 3px solid #c5a85c;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    max-width: 600px;
    margin: 30px auto 10px auto;
}
.support-link {
    color: #c5a85c !important;
    text-decoration: none !important;
    font-size: 14px;
    font-weight: bold;
    transition: 0.3s all;
}
.support-link:hover {
    color: #ffffff !important;
    text-decoration: underline !important;
}

.copyright-section {
    border-top: 1px solid #2d2d2d;
    margin-top: 20px;
    padding: 25px;
    text-align: center;
    background-color: #161616;
    border-radius: 15px;
}
.copyright-name { color: #c5a85c; font-size: 14px; font-weight: bold; }
.intent-description { color: #888; font-size: 12px; margin-top: 8px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. เริ่มระบบความจำบทสนทนา (Session State) และการแสดงผลแชท
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# หน้าแรกพุทธบูชา: จะแสดงผลก็ต่อเมื่อยังไม่มีการคุยกันเท่านั้น
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

# แสดงประวัติการสนทนาทั้งหมดที่มีอยู่ในระบบความจำ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================================================================
# 5. ระบบรับข้อความและการประมวลผลธรรมะ (Official Native Pattern)
# ==============================================================================
if user_input := st.chat_input("พิมพ์คำศัพท์หรือข้อธรรมที่ต้องการสืบค้น..."):
    # 1. แสดงข้อความของฝั่งผู้ใช้ทันทีบนหน้าจอ
    with st.chat_message("user"):
        st.markdown(user_input)
    # บันทึกลงความจำระบบ
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. เรียกสัญญานส่งไปหา Google Gemini Engine เพื่อขอคำตอบ
    with st.chat_message("assistant"):
        if client:
            with st.spinner("AI กำลังสืบค้นคัมภีร์พระไตรปิฎก..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=user_input,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt
                        )
                    )
                    full_response = response.text
                    # แสดงคำตอบของ AI บนหน้าจอทันที
                    st.markdown(full_response)
                    # บันทึกคำตอบลงความจำระบบ
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"⚠️ เกิดข้อผิดพลาดจากระบบ AI Engine: {e}")
        else:
            st.error("⚠️ ไม่พบระบบสัญญาน API: กรุณาตรวจสอบว่าได้ตั้งค่าคีย์ความลับ 'GEMINI_API_KEY' ในหน้า Settings ของ Hugging Face แล้วหรือยังครับ")

# ==============================================================================
# 6. ส่วนสนับสนุนเพื่อความยั่งยืนของระบบ และข้อเสนอแนะ (ปรับกรอบธนาคารแนวยาว+กดดูได้)
# ==============================================================================
st.markdown("""
<div class="support-card">
<div style="color: #c5a85c; font-size: 16px; font-weight: bold; margin-bottom: 8px;">
☸️ สนับสนุนระบบปัญญาประดิษฐ์พระบาลี
</div>
<div style="color: #aaaaaa; font-size: 13px; margin-bottom: 18px; line-height: 1.6; padding: 0 10px;">
"ท่านสามารถร่วมสนับสนุนโครงการนี้เพื่อเป็น <b>ค่าบำรุงรักษาเซิร์ฟเวอร์</b> และ <b>ค่าบริการระบบ AI Engine (API)</b> 
ในการขับเคลื่อนระบบ AI.prapali ให้เปิดสแตนด์บายทำหน้าที่สืบทอดพุทธพจน์ตลอด 24 ชั่วโมงอย่างยั่งยืน"
</div>

<!-- กล่องข้อมูลธนาคารดีไซน์แนวยาวแบบกดคลิกเพื่อเปิดดูเลขบัญชี -->
<details style="background-color: #161616; border: 1px solid #2d2d2d; border-left: 4px solid #c5a85c; padding: 8px 15px; border-radius: 6px; margin: 0 auto 15px auto; max-width: 460px; text-align: left; cursor: pointer;">
<summary style="color: #c5a85c; font-size: 13px; font-weight: bold; list-style: none; display: flex; justify-content: space-between; align-items: center;">
<span>🏦 ธนาคารกรุงศรีอยุธยา (คลิกเพื่อดูเลขบัญชี...)</span>
<span style="font-size: 11px; color: #8b7355;">▼ กดดูเลข</span>
</summary>
<div style="margin-top: 8px; border-top: 1px solid #2d2d2d; padding-top: 8px;">
<div style="color: #ffffff; font-size: 16px; font-weight: 800; letter-spacing: 1px; margin-bottom: 3px;">เลขที่บัญชี: 777-438496-0</div>
<div style="color: #e0e0e0; font-size: 13px;">ชื่อบัญชี: นายวิศวกรณ์ พระบัวบาน</div>
</div>
</details>

<!-- ช่องทางการติดต่อและแนะนำเพิ่มเติม -->
<div style="margin-top: 15px; border-top: 1px solid #2d2d2d; padding-top: 15px;">
<div style="color: #8b7355; font-size: 12px; margin-bottom: 8px;">📞 ติดต่อผู้พัฒนา / ให้ข้อชีแนะเพิ่มเติม:</div>
<a class="support-link" href="tel:0644518043" style="margin: 0 15px;">📱 โทร: 064-4518043</a>
<a class="support-link" href="mailto:wissawakorn444@gmail.com" style="margin: 0 15px;">✉️ อีเมล: wissawakorn444@gmail.com</a>
</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 7. ส่วนแสดงผลลิขสิทธิ์และเจตจำนง (ตรึงท้ายกระดาษอย่างถาวร)
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
