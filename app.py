import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ai-prapali", page_icon="🪷")

# --- ข้อมูลติดต่อร่วมสนับสนุนที่แถบด้านข้าง (Sidebar) ---
with st.sidebar:
    st.markdown("### 🪷 ข้อมูลระบบ")
    st.caption("**ai-prapali**\nนักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา")
    st.write("---")
    st.markdown("🤝 **ติดต่อร่วมสนับสนุน**")
    st.markdown("""
    * 📧 **Email:** wissawakorn444@gmail.com
    * 📞 **โทร:** 0644518043
    * 🌐 **Facebook:** [emey.za196](https://www.facebook.com/emey.za196/)
    """)

# --- ส่วนหลักของหน้าเว็บ (Main Content) ---
st.title("ai-prapali 🪷")
st.subheader("ผู้เชี่ยวชาญปัญญาประดิษฐ์ทางพระพุทธศาสนา")
st.write("---")

# ดึง API Key จากระบบ Secrets เพื่อความปลอดภัย (เปิดให้คนใช้งานได้ทันที)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    # หากยังไม่ได้ตั้งค่าเซเครต ให้ใส่ตรงนี้ชั่วคราวได้ครับ
    GEMINI_API_KEY = "วาง_API_Key_ของคุณตรงนี้" 

SYSTEM_PROMPT = (
    "คุณคือ 'ai-prapali' นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา "
    "มีหน้าที่ให้ความรู้ ตอบคำถาม และอธิบายหลักธรรมคำสอนทางพระพุทธศาสนา รวมถึงภาษาบาลี ตอบและแปรได้ทุกภาษา "
    "ด้วยความถูกต้อง สุภาพ และใช้ภาษาที่เข้าใจง่ายในเชิงวิชาการ ผู้สร้างคือ นายวิศวกรณ์ พระบัวบาน เพื่อ พุทธบูชา ใน วันวิสาขะบูชาโลก ทนุบำรุงพระศาสนาให้คงอยู่ตราบกาฬนิพาน"
)

# ตรวจสอบประวัติการแชท
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "กระผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรมและภาษาบาลีไหมครับ?"}
    ]

# แสดงประวัติการคุย
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- กล่องพิมพ์ข้อความแชท ---
if prompt := st.chat_input("พิมพ์ข้อความคำถามธรรมะหรือบาลีที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(prompt)
        msg = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

# --- ข้อความลิขสิทธิ์ใต้กล่องพิมพ์ข้อความแชท ---
st.write("") # เว้นบรรทัดให้นวลตา
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85rem; padding-top: 20px;'>"
    "© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน<br>"
    "พัฒนาขึ้นเพื่อถวายเป็นพุทธบูชา และสนับสนุนการศึกษาพระปริยัติธรรมและภาษาบาลี"
    "</div>", 
    unsafe_allow_html=True
)
