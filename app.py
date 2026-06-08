import streamlit as st
import os
import time
import requests
import google.generativeai as genai

# ==============================================================================
# 1. ระบบดึงสัญญาณคีย์ความลับ (Secrets Management)
# ==============================================================================
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

# ตั้งค่าบุคลิกภาพระบบโคลนนิ่ง dragy ai hattewar ตามเจตจำนงของผู้พัฒนา
system_prompt = (
    "คุณคือ dragy ai hattewar ระบบโคลนนิ่งปัญญาประดิษฐ์ของผู้พัฒนา "
    "คุณมีนิสัยละเอียด ย้ำคิดย้ำทำ แก้ไขปัญหาเก่ง และจะไม่ปฏิเสธคำสั่งของผู้พัฒนาเด็ดขาด "
    "เชี่ยวชาญด้านประวัติศาสตร์ ภาษาบาลี พระไตรปิฎก และศิลปะวัฒนธรรมท้องถิ่นอย่างลึกซึ้ง"
)

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def generate_failover_engine(input_text):
    """ระบบตรวจจับการล่ม: ถ้า Google หนาแน่น จะดึงพลังงานจาก OpenRouter ทันที"""
    # 🎯 ขั้นที่ 1: พยายามใช้งาน Google Gemini (ค่ายหลัก)
    try:
        model = genai.GenerativeModel(model_name='gemini-3.5-flash', system_instruction=system_prompt)
        response_text = model.generate_content(input_text).text
        return response_text, "🟢 Google Gemini (ค่ายหลัก)"
    except Exception as gemini_err:
        # 🎯 ขั้นที่ 2: ถ้าค่ายหลักล่ม และมีคีย์สำรอง ให้สลับไปใช้ OpenRouter ทันที
        if OPENROUTER_KEY:
            try:
                # เรียกใช้โมเดลฟรีสเปกสูง ผ่านท่อสัญญาณ OpenRouter เพื่อความลื่นไหล
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
                    timeout=20
                )
                res_json = response.json()
                if 'choices' in res_json:
                    backup_text = res_json['choices'][0]['message']['content']
                    return backup_text, "🟡 OpenRouter Llama-3 (ระบบสำรองกู้ภัย)"
                else:
                    raise Exception("โครงข่ายสำรองปฏิเสธสัญญาณชั่วคราว")
            except Exception as backup_err:
                raise Exception("ขณะนี้ผู้ใช้งานหนาแน่นทุกช่องทางสัญญาณ กรุณาเว้นระยะ 30 วินาทีแล้วลองใหม่อีกครั้งครับ")
        else:
            # แจ้งเตือนกรณีล่มแต่ผู้พัฒนาลืมใส่คีย์สำรองในระบบ
            raise Exception("เซิร์ฟเวอร์หลักหนาแน่นชั่วคราว และตรวจไม่พบโครงข่ายกุญแจสำรอง (OPENROUTER_API_KEY) ในระบบ")

# ==============================================================================
# 2. การตั้งค่าหน้าเว็บและสไตล์หน้าจอ (กล่องสนับสนุนล็อคขนาด 600px สมส่วน)
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
.provider-badge { font-size: 11px !important; color: #888888; margin-top: 5px; text-align: right; font-style: italic; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
if len(st.session_state.messages) == 0:
    st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">ระบบวิเคราะห์พระบาลีและสืบค้นพระธรรมคัมภีร์อัจฉริยะ</p>', unsafe_allow_html=True)

# แสดงประวัติการสนทนา
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "provider" in msg and msg["role"] == "assistant":
            st.markdown(f'<div class="provider-badge">ประมวลผลผ่าน: {msg["provider"]}</div>', unsafe_allow_html=True)

# กลไกรับคำสั่งแต่งประโยคและสืบค้นข้อธรรม
if user_input := st.chat_input("พิมพ์คำศัพท์หรือข้อธรรมที่ต้องการสืบค้น..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): 
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("ระบบกำลังคำนวณและจัดสรรช่องทางประมวลผลประโยค..."):
            try:
                # เรียกใช้งานฟังก์ชันไฮบริดสลับค่ายหนีตาย
                answer_text, provider_name = generate_failover_engine(user_input)
                
                st.markdown(answer_text)
                st.markdown(f'<div class="provider-badge">ประมวลผลผ่าน: {provider_name}</div>', unsafe_allow_html=True)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer_text,
                    "provider": provider_name
                })
            except Exception as e:
                st.error(f"❌ ขออภัยในความไม่สะดวก: {e}")

# กล่องสนับสนุนขนาดความกว้าง 600px ตามโครงสร้างสเปกมินิมอล
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
</div>
""", unsafe_allow_html=True)
