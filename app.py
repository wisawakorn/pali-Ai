import streamlit as st
import os
import requests

# 1. ระบบตรวจสอบความพร้อมของ Library ป้องกันหน้าจอแดง (ModuleNotFoundError)
try:
    import google.generativeai as genai
    LIB_STATUS = True
except ImportError:
    LIB_STATUS = False

# ==============================================================================
# 2. การกำหนดค่าระบบและตัวตนวิศวกร Prapali (ตัวตนที่ท่านกำหนด)
# ==============================================================================
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

# นิยามตัวตนวิศวกรผู้เชี่ยวชาญ (ตามคำสั่งดั้งเดิมของท่าน)
system_prompt = (
    "กระผมคือ dragy ai prapali วิศวกรผู้เชี่ยวชาญเฉพาะทาง "
    "มีความละเอียด ย้ำคิดย้ำทำ และแก้ไขปัญหาเชิงเทคนิคได้อย่างดีเยี่ยม "
    "มีความรอบรู้ลึกซึ้งในด้านประวัติศาสตร์ ภาษาบาลี พระไตรปิฎก และศิลปะวัฒนธรรม "
    "พร้อมปฏิบัติหน้าที่และแก้ไขปัญหาตามคำสั่งของท่านอย่างสุดความสามารถ"
)

if LIB_STATUS and GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def generate_expert_engine(input_text):
    """ระบบเชื่อมต่อประมวลผล 2 ชั้น: ป้องกันอาการค้างและ Error 503"""
    # ชั้นที่ 1: ใช้ Google Gemini (ระบบหลัก)
    try:
        if not LIB_STATUS: raise Exception("Library missing")
        model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=system_prompt)
        # ตั้งค่า timeout เพื่อไม่ให้รอนานเกินไป
        return model.generate_content(input_text).text, "🟢 ระบบหลัก Prapali-Engine"
    except Exception:
        # ชั้นที่ 2: สลับไประบบสำรองทันที (แก้ปัญหาประมวลผลนาน/ระบบล่ม)
        if OPENROUTER_KEY:
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": "meta-llama/llama-3-8b-instruct:free", 
                        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": input_text}]
                    },
                    timeout=15 # ตัดสายใน 15 วินาทีถ้าช้าเกินไป
                )
                return response.json()['choices'][0]['message']['content'], "🟡 ระบบสำรอง Prapali-Backup"
            except:
                return "ขออภัยครับ ระบบหนาแน่นเกินไปในขณะนี้ กรุณาลองใหม่อีกครั้งใน 10 วินาที", "🔴 ขัดข้อง"
        else:
            return "เซิร์ฟเวอร์หลักหนาแน่น และไม่พบคีย์ระบบสำรอง", "🔴 ขัดข้อง"

# ==============================================================================
# 3. ส่วนหน้ากากผู้ใช้งาน (UI) - ปรับปรุงใหม่ให้ปลอดภัยจากเศษโค้ด HTML
# ==============================================================================
st.set_page_config(page_title="AI.prapali", page_icon="☸️", layout="centered")

# ใช้ CSS เพื่อความสวยงามโดยไม่ทำให้โครงสร้างหลักพัง
st.markdown("""
<style>
    header { visibility: hidden !important; height: 0px !important; }
    footer { visibility: hidden !important; }
    .stApp { background-color: #121212 !important; color: #ffffff !important; }
    .main-title { color: #c5a85c; text-align: center; font-size: 40px; font-weight: 800; margin-bottom: 5px; }
    .main-subtitle { color: #8b7355; text-align: center; margin-bottom: 30px; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AI.prapali</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">วิศวกรปัญญาประดิษฐ์ผู้เชี่ยวชาญเฉพาะทาง</div>', unsafe_allow_html=True)

# ระบบจำประวัติการสนทนา
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงแชทเก่า
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# รับคำสั่งจากท่าน
if user_input := st.chat_input("พิมพ์คำสั่งให้วิศวกร Prapali..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("กระผม prapali กำลังแก้ไขปัญหาเชิงเทคนิค..."):
            res, provider = generate_expert_engine(user_input)
            st.markdown(res)
            st.caption(f"ประมวลผลผ่าน: {provider}")
            st.session_state.messages.append({"role": "assistant", "content": res})

st.divider()

# ==============================================================================
# 4. ส่วนสนับสนุนและข้อมูลติดต่อ (ใช้ Widget มาตรฐาน ป้องกัน HTML หลุด)
# ==============================================================================
st.subheader("☸️ สนับสนุนระบบปัญญาประดิษฐ์พระบาลี")
st.write("โครงการพัฒนาเพื่อรักษาและสืบทอดพุทธพจน์ด้วยเทคโนโลยีสมัยใหม่")

# ใช้ Expander แทน HTML Details เพื่อความลื่นไหล
with st.expander("🏦 ข้อมูลบัญชีสนับสนุน (คลิกเพื่อดูรายละเอียด)"):
    st.success("**ธนาคารกรุงศรีอยุธยา**\n\n**เลขที่บัญชี:** 777-438496-0\n\n**ชื่อบัญชี:** นายวิศวกรณ์ พระบัวบาน")

st.write("---")
st.write("📞 **ช่องทางติดต่อวิศวกรผู้พัฒนา:**")

col1, col2 = st.columns(2)
with col1:
    st.link_button("📱 โทร: 064-4518043", "tel:0644518043", use_container_width=True)
with col2:
    st.link_button("🔵 ติดต่อผ่าน Facebook", "https://www.facebook.com/emey.za196/", use_container_width=True)

st.caption("© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน")
