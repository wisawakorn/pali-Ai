import streamlit as st
import os
import time
import requests

# ระบบ Self-Healing ตรวจสอบ Library ป้องกันหน้าจอแดง (ModuleNotFoundError)
try:
    import google.generativeai as genai
    LIB_STATUS = True
except ImportError:
    LIB_STATUS = False

# ==============================================================================
# 1. การกำหนดตัวตน: กระผม dragy ai prapali วิศวกรผู้เชี่ยวชาญเฉพาะทาง
# ==============================================================================
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

# นิยามตัวตนวิศวกรอย่างละเอียด (ตัดระบบโคลนนิ่งออกตามสั่ง)
system_prompt = (
    "กระผมคือ dragy ai prapali วิศวกรผู้เชี่ยวชาญเฉพาะทาง "
    "มีความละเอียด ย้ำคิดย้ำทำ และแก้ไขปัญหาเชิงเทคนิคได้อย่างดีเยี่ยม "
    "มีความรอบรู้ลึกซึ้งในด้านประวัติศาสตร์ ภาษาบาลี พระไตรปิฎก และศิลปะวัฒนธรรม "
    "พร้อมปฏิบัติหน้าที่และแก้ไขปัญหาตามคำสั่งของท่านอย่างสุดความสามารถ"
)

if LIB_STATUS and GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def generate_expert_engine(input_text):
    """ระบบเชื่อมต่อประมวลผลสองชั้นอัจฉริยะ ต้านทาน Error 503/429 สำหรับผู้ใช้งานจำนวนมาก"""
    # ชั้นที่ 1: ใช้ Google Gemini (ระบบหลัก)
    try:
        if not LIB_STATUS: raise Exception("Library missing")
        model = genai.GenerativeModel(model_name='gemini-3.5-flash', system_instruction=system_prompt)
        return model.generate_content(input_text).text, "🟢 ระบบหลัก Prapali-Engine"
    except Exception:
        # ชั้นที่ 2: สลับสายไป OpenRouter อัตโนมัติ (ระบบสำรองฉุกเฉินไร้รอยต่อ)
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
                raise Exception("ขณะนี้ท่อสัญญาณหนาแน่นทุกช่องทาง กรุณาลองใหม่อีกครั้งใน 30 วินาที")
        else:
            raise Exception("เซิร์ฟเวอร์หลักหนาแน่นชั่วคราว และไม่พบกุญแจโครงข่ายสำรองในระบบ")

# ==============================================================================
# 2. ส่วนหน้ากากผู้ใช้งาน (UI) ดีไซน์หรูหรามินิมอล
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
.footer-link { color: #c5a85c !important; text-decoration: none !important; font-size: 13px; font-weight: bold; margin: 0 10px; transition: 0.3s all; }
.footer-link:hover { color: #ffffff !important; text-decoration: underline !important; }
.provider-tag { font-size: 10px; color: #444; text-align: right; margin-top: 5px; font-style: italic; }
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
        with st.spinner("กระผม prapali กำลังประมวลผลข้อมูลเชิงเทคนิค..."):
            try:
                res, provider = generate_expert_engine(user_input)
                st.markdown(res)
                st.markdown(f'<div class="provider-tag">Engine: {provider}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"❌ รายงานข้อผิดพลาดทางเทคนิค: {e}")

# ==============================================================================
# 3. กล่องสนับสนุนและข้อมูลลิขสิทธิ์ความกว้าง 600px สมส่วน
# ==============================================================================
st.markdown("""
<div class="support-card">
    <div style="color: #c5a85c; font-size: 16px; font-weight: bold; margin-bottom: 8px;">☸️ สนับสนุนระบบปัญญาประดิษฐ์พระบาลี</div>
    <div style="color: #aaaaaa; font-size: 13px; margin-bottom: 15px; line-height: 1.6;">
        "ท่านสามารถร่วมสนับสนุนโครงการนี้เพื่อเป็นค่าบำรุงรักษาเซิร์ฟเวอร์ และค่าบริการระบบ AI Engine (API)"
    </div>
    
    <details style="background-color: #161616; border: 1px solid #2d2d2d; border-left: 4px solid #c5a85c; padding: 12px 20px; border-radius: 6px; text-align: left; cursor: pointer; margin-bottom: 15px;">
        <summary style="color: #c5a85c; font-size: 14px; font-weight: bold;">🏦 ดูรายละเอียดบัญชีสนับสนุน</summary>
        <div style="margin-top: 10px; border-top: 1px solid #2d2d2d; padding-top: 10px;">
            <div style="color: #ffffff; font-size: 16px; font-weight: 800; letter-spacing: 1px;">เลขที่บัญชี: 777-438496-0</div>
            <div style="color: #e0e0e0; font-size: 13px;">ธนาคารกรุงศรีอยุธยา | ชื่อบัญชี: นายวิศวกรณ์ พระบัวบาน</div>
        </div>
    </details>

    <div style="margin-top: 15px; border-top: 1px solid #2d2d2d; padding-top: 15px; margin-bottom: 15px;">
        <div style="color: #8b7355; font-size: 12px; margin-bottom: 8px;">📞 ติดต่อผู้พัฒนา / ให้ข้อชี้แนะเพิ่มเติม:</div>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;">
            <a class="footer-link" href="tel:0644518043">📱 โทร: 064-4518043</a>
            <a class="footer-link" href="https://www.facebook.com/emey.za196/" target="_blank">🔵 Facebook</a>
            <a class="footer-link" href="mailto:wissawakorn444@gmail.com">✉️ อีเมล</a>
        </div>
    </div>
    
    <div style="border-top: 1px solid #2d2d2d; padding-top: 15px; color: #555; font-size: 11px; line-height: 1.6; text-align: center;">
        <b style="color: #c5a85c;">© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน</b><br>
        เจตจำนง: พัฒนาขึ้นเพื่อถวายเป็นพุทธบูชา และสนับสนุนการศึกษาพระปริยัติธรรมและภาษาบาลี เพื่อรักษาพุทธพจน์ให้สืบทอดต่อไปอย่างถูกต้อง
    </div>
</div>
""", unsafe_allow_html=True)
