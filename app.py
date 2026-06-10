import streamlit as st
import os
import requests

# ระบบตรวจสอบ Library เพื่อความปลอดภัยของแอป
try:
    import google.generativeai as genai
    LIB_STATUS = True
except ImportError:
    LIB_STATUS = False

# ==============================================================================
# 1. การกำหนดค่าระบบและตัวตนของวิศวกร Prapali
# ==============================================================================
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

system_prompt = (
    "กระผมคือ dragy ai prapali วิศวกรผู้เชี่ยวชาญเฉพาะทาง "
    "มีความละเอียด ย้ำคิดย้ำทำ และแก้ไขปัญหาเชิงเทคนิคได้อย่างดีเยี่ยม "
    "มีความรอบรู้ลึกซึ้งในด้านประวัติศาสตร์ ภาษาบาลี พระไตรปิฎก และศิลปะวัฒนธรรม "
    "พร้อมปฏิบัติหน้าที่และแก้ไขปัญหาตามคำสั่งของท่านอย่างสุดความสามารถ"
)

if LIB_STATUS and GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def generate_expert_engine(input_text):
    """ระบบเชื่อมต่อประมวลผลอัจฉริยะ (OpenRouter หลัก -> Gemini สำรอง)"""
    
    # 🟢 ช่องทางที่ 1: สลับมาให้ OpenRouter เป็นระบบหลัก
    if OPENROUTER_KEY:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}", 
                    "Content-Type": "application/json"
                },
                json={
                    "model": "meta-llama/llama-3-8b-instruct:free", 
                    "messages": [
                        {"role": "system", "content": system_prompt}, 
                        {"role": "user", "content": input_text}
                    ]
                },
                timeout=15  # กำหนด timeout ให้กระชับ เผื่อสลับไปหาบอทสำรองได้ไวขึ้น
            )
            res_json = response.json()
            if 'choices' in res_json and len(res_json['choices']) > 0:
                return res_json['choices'][0]['message']['content'], "🟢 ระบบหลัก Prapali-Engine (OpenRouter)"
            else:
                raise Exception("OpenRouter Response Error")
        except Exception:
            pass  # ถ้าเกิด Error ให้ปล่อยไหลข้ามไปทำงานในบล็อก Gemini สำรองด้านล่าง
            
    # 🟡 ช่องทางที่ 2: Google Gemini รับหน้าที่เป็น "ระบบสำรอง" ประคองแอปยามฉุกเฉิน
    try:
        if not LIB_STATUS or not GEMINI_KEY: 
            raise Exception("คีย์สำรองหรือ Library ของ Gemini ไม่พร้อมใช้งาน")
        
        # ใช้โมเดล gemini-2.0-flash ล่าสุดรองรับ System Instruction แม่นยำ
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            system_instruction=system_prompt
        )
        
        response = model.generate_content(input_text)
        if response.text:
            return response.text, "🟡 ระบบสำรอง Prapali-Backup (Gemini 2.0)"
        else:
            raise Exception("Gemini Empty response")
            
    except Exception:
        return "เซิร์ฟเวอร์ระบบหลักและระบบสำรองกำลังปรับปรุงชั่วคราว กรุณาเว้นระยะสักครู่แล้วลองใหม่อีกครั้งครับ", "🔴 ระบบขัดข้อง"

# ==============================================================================
# 2. ส่วนแสดงผล (UI) ดีไซน์โทนดาร์ก-ทอง เรียบหรู ไม่ใช้ HTML ดิบป้องกันการระเบิด
# ==============================================================================
st.set_page_config(page_title="AI.prapali", page_icon="☸️", layout="centered")

# ปรับแต่งธีมผ่านสไตล์หลักที่ปลอดภัย
st.markdown("""
<style>
header { visibility: hidden !important; height: 0px !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #121212 !important; color: #ffffff !important; }
h1 { color: #c5a85c !important; text-align: center; font-size: 36px !important; font-weight: 800; }
.subtitle { color: #8b7355 !important; text-align: center; margin-bottom: 30px; font-size: 15px; }
.copyright-text { color: #555555 !important; text-align: center; font-size: 11px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("AI.prapali")
st.markdown('<p class="subtitle">วิศวกรปัญญาประดิษฐ์ผู้เชี่ยวชาญเฉพาะทางด้านพระบาลี</p>', unsafe_allow_html=True)

# ระบบบันทึกสถานะการสนทนา
if "messages" not in st.session_state: 
    st.session_state.messages = []

# แสดงกล่องข้อความแชตจากประวัติเดิม
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ช่องกรอกข้อมูลรับคำสั่ง
if user_input := st.chat_input("พิมพ์คำศัพท์หรือข้อธรรมที่ต้องการสืบค้น..."):
    # แสดงข้อความฝั่งผู้ใช้ทันที
    with st.chat_message("user"): 
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # ประมวลผลจาก AI
    with st.chat_message("assistant"):
        with st.spinner("กระผม prapali กำลังประมวลผลข้อมูลเชิงเทคนิค..."):
            res, provider = generate_expert_engine(user_input)
            st.markdown(res)
            st.caption(f"Engine: {provider}")
            st.session_state.messages.append({"role": "assistant", "content": res})

st.divider()

# ==============================================================================
# 3. ส่วนกล่องสนับสนุนและข้อมูลติดต่อ (ใช้ Widget แท้ของ Streamlit ไม่มีพัง)
# ==============================================================================
st.write("### ☸️ สนับสนุนระบบปัญญาประดิษฐ์พระบาลี")
st.caption('"ท่านสามารถร่วมสนับสนุนโครงการนี้เพื่อเป็นค่าบำรุงรักษาเซิร์ฟเวอร์ และค่าบริการระบบ AI Engine (API)"')

# ปุ่มพับเก็บรายละเอียดบัญชีแบบปลอดภัยร้อยเปอร์เซ็นต์
with st.expander("🏦 ดูรายละเอียดบัญชีสนับสนุน (คลิกเปิดตรงนี้)"):
    st.info("**เลขที่บัญชี:** 777-438496-0\n\n**ธนาคาร:** กรุงศรีอยุธยา | **ชื่อบัญชี:** นายวิศวกรณ์ พระบัวบาน")

st.write("---")
st.write("📞 **ติดต่อผู้พัฒนา / ให้ข้อชี้แนะเพิ่มเติม:**")

# ปุ่มลิงก์ติดต่อภายนอกแบบสวยงามสไตล์มินิมอล
col1, col2 = st.columns(2)
with col1:
    st.link_button("📱 โทร: 064-4518043", "tel:0644518043", use_container_width=True)
with col2:
    st.link_button("🔵 Facebook ผู้พัฒนา", "https://www.facebook.com/emey.za196/", use_container_width=True)

st.markdown('<p class="copyright-text">© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน<br>เจตจำนง: พัฒนาขึ้นเพื่อถวายเป็นพุทธบูชา และสนับสนุนการศึกษาพระปริยัติธรรมและภาษาบาลี</p>', unsafe_allow_html=True)
