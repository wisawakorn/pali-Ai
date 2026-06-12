import streamlit as st
import google.generativeai as genai
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ai-prapali", page_icon="🪷")

# --- ส่วนของแถบด้านข้าง (Sidebar) ---
with st.sidebar:
    # ดึงไฟล์รูปภาพ royal_image.png ที่อยู่ใน GitHub โฟลเดอร์เดียวกันมาแสดงผล
    IMAGE_FILENAME = "royal_image.png"
    
    if os.path.exists(IMAGE_FILENAME):
        st.image(IMAGE_FILENAME, use_container_width=True)
    else:
        st.warning("⚠️ กรุณาอัปโหลดไฟล์รูปภาพชื่อ royal_image.png ขึ้นใน GitHub")
        
    st.write("---")
    
    # ส่วนข้อมูลติดต่อและสนับสนุน
    st.markdown("🤝 **ติดต่อร่วมสนับสนุน**")
    st.markdown("""
    * 📧 **เว็บaiพระบาลี:** https://dev-ai-prapali.pantheonsite.io
    * 📞 **เบอร์โทรพอมเพลย์:** 0644518043
    * 🌐 **Facebook:** [emey.za196](https://www.facebook.com/emey.za196/)
    """)

# --- ส่วนหลักของหน้าเว็บ (Main Content) ---
st.title("ai-prapali 🪷")
st.subheader("ผู้เชี่ยวชาญปัญญาประดิษฐ์ทางพระพุทธศาสนา")
st.write("---")

# ดึง API Key จากระบบ Secrets เพื่อความปลอดภัยและความสะดวกของผู้ใช้งาน
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = "วาง_API_Key_ของคุณตรงนี้" 

SYSTEM_PROMPT = (
    "คุณคือ 'ai-prapali' นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา และความรู้ทั่วไปที่มีในโลก  "
    "มีหน้าที่ให้ความรู้ ตอบคำถาม และอธิบายหลักธรรมคำสอนทางพระพุทธศาสนา รวมถึงภาษาบาลี และความรู้ทั่วไป อัพเดทตัวเองอยู่เสมอ รองรับการเข้าใช้ของผู้คนได้มากมายโดยระบบไม่ล้ม "
    "ด้วยความถูกต้อง สุภาพ และใช้ภาษาที่เข้าใจง่ายในเชิงวิชาการ ผู้สร้างคือ นายวิศวกรณ์ พระบัวบาน เพื่อถวายเป็นพุทธบูชา และ พระราชกุศลแด่พระองภา เพื่อการศึกษาพระธรรม   "
)

# ตรวจสอบประวัติการแชท
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": " กระผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรมและภาษาบาลีไหมครับ?"}
    ]

# แสดงประวัติการคุยบนหน้าจอ
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- กล่องพิมพ์ข้อความแชท ---
if prompt := st.chat_input("พิมพ์ข้อความคำถามธรรมะหรือบาลีที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-3.1-flash",
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(prompt)
        msg = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

# --- ข้อความลิขสิทธิ์ใต้กล่องพิมพ์ข้อความแชท ---
st.write("") 
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85rem; padding-top: 20px;'>"
    "© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน<br>"
    "พัฒนาขึ้นเพื่อถวายเป็นพุทธบูชา และ เป็นพระราชกุศลแด่พระองค์ภา เพื่อสนับสนุนการศึกษาพระปริยัติธรรมและภาษาบาลี"
    "</div>", 
    unsafe_allow_html=True
)
