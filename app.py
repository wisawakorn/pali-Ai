import streamlit as st
import os
import time
import requests

# ระบบ Self-Healing ตรวจสอบ Library เพื่อป้องกันหน้าจอแดง
try:
    import google.generativeai as genai
    LIB_STATUS = True
except ImportError:
    LIB_STATUS = False

# ==============================================================================
# 1. การกำหนดตัวตนใหม่: กระผม dragy ai prapali
# ==============================================================================
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

# นิยามตัวตนวิศวกรผู้เชี่ยวชาญเฉพาะทาง (ตัดคำว่าโคลนนิ่งออกตามสั่ง)
system_prompt = (
    "กระผมคือ dragy ai prapali วิศวกรผู้เชี่ยวชาญเฉพาะทาง "
    "มีความละเอียด ย้ำคิดย้ำทำ และแก้ไขปัญหาเชิงเทคนิคได้อย่างดีเยี่ยม "
    "มีความรอบรู้ลึกซึ้งในด้านประวัติศาสตร์ ภาษาบาลี พระไตรปิฎก และศิลปะวัฒนธรรม "
    "พร้อมปฏิบัติหน้าที่และแก้ไขปัญหาตามคำสั่งของท่านอย่างสุดความสามารถ"
)

if LIB_STATUS and GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def generate_expert_engine(input_text):
    """ระบบประมวลผลสองชั้น: มั่นใจว่าคำตอบจะถูกส่งถึงมือผู้ใช้เสมอ"""
    # ชั้นที่ 1: Google Gemini (วิศวกรหลัก)
    try:
        if not LIB_STATUS: raise Exception("Library missing")
        model = genai.GenerativeModel(model_name='gemini-3.5-flash', system_instruction=system_prompt)
        return model.generate_content(input_text).text, "🟢 ระบบหลัก Prapali-Engine"
    except Exception:
        # ชั้นที่ 2: OpenRouter (วิศวกรสำรองฉุกเฉิน)
        if OPENROUTER_KEY:
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": "meta-llama/llama-3-8b-instruct:free", 
                        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": input_text}]
                    },
                    timeout=20
                )
                return response.json()['choices'][0]['message']['content'], "🟡 ระบบสำรอง Prapali-Backup"
            except:
                raise Exception("ขณะนี้ท่อสัญญาณหนาแน่น กรุณาลองใหม่อีกครั้งใน 30 วินาที")
        else:
            raise Exception("ระบบหลักหนาแน่น และไม่พบกุญแจระบบสำรอง")

# ==============================================================================
# 2. ส่วนหน้ากากผู้ใช้งาน (UI) - เน้นความสมส่วนและเป็นวิศวกร
# ==============================================================================
st.set_page_config(page_title="AI.prapali", page_icon="☸️", layout="wide")

st.markdown("""
<style>
header { visibility: hidden !important; height: 0px !important; }
footer { visibility: hidden !important; }
.stApp { background-color: #121212 !important; color: #ffffff !important; }
.main-title { color: #c5a85c !important; font-size: 34px !important; font-weight: 800 !important; text-align: center; margin-top: -20px !important; }
.main-subtitle { font-size: 14px !important; text-align: center; color: #8b7355 !important; margin-bottom: 25px; }
.support-card { background-color: #1a1a1a; border: 1px solid #2d2d2d; border-top: 3px solid #c5a85c; padding: 20px; border-radius: 12px; text-align: center; max-width: 600px; margin: 30px auto 10px auto; }
.provider-tag { font-size: 10px; color: #555; text-align: right; font-style: italic; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if len(st.session_state.messages) == 0:
    st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">วิศวกรปัญญาประดิษฐ์ผู้เชี่ยวชาญเฉพาะทางด้านพระบาลี</p>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("พิมพ์ข้อความเพื่อสั่งงานวิศวกร prapali..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("กระผม prapali กำลังคำนวณและประมวลผลข้อมูลเชิงเทคนิค..."):
            try:
                res, provider = generate_expert_engine(user_input)
                st.markdown(res)
                st.markdown(f'<div class="provider-tag">Engine: {provider}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"❌ รายงานข้อผิดพลาดทางเทคนิค: {e}")

# ส่วนสนับสนุนระบบ (คงขนาด 600px ตามความต้องการ)
st.markdown("""
<div class="support-card">
<div style="color: #c5a85c; font-size: 16px; font-weight: bold; margin-bottom: 8px;">☸️ สนับสนุนงานวิศวกรรมปัญญาประดิษฐ์</div>
<div style="color: #ffffff; font-size: 15px; font-weight: 800;">เลขที่บัญชี: 777-438496-0</div>
<div style="color: #e0e0e0; font-size: 12px; margin-bottom: 10px;">ธนาคารกรุงศรีอยุธยา | นายวิศวกรณ์ พระบัวบาน</div>
<div style="border-top: 1px solid #2d2d2d; padding-top: 10px;">
    <a style="color: #c5a85c; text-decoration: none; font-size: 12px;" href="tel:0644518043">📞 ติดต่อวิศวกร: 064-4518043</a>
</div>
</div>
""", unsafe_allow_html=True)
