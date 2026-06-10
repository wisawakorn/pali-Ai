import streamlit as st
import os
from google import genai
from google.genai import types

# ==============================================================================
# 1. ระบบ AI Engine (ดึงค่าจากระบบ Environment Variable ของ Hugging Face)
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
# 3. ปรับแต่งสไตล์ CSS (เน้นความกระชับและซ่อนส่วนเกิน)
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

    .copyright-section {
        border-top: 1px solid #2d2d2d;
        margin-top: 40px;
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
# 4. เริ่มระบบความจำบทสนทนา (Session State)
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
    # 1. แสดงข้อความของฝั่งผู้กองทันทีบนหน้าจอ
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
                        model='gemini-3.1-flash',
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
# 6. ส่วนแสดงผลลิขสิทธิ์และเจตจำนง (ตรึงท้ายกระดาษอย่างถาวร)
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
