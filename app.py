import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ai-prapali", page_icon="🪷")

# --- ส่วนของแถบด้านข้าง (Sidebar) ---
with st.sidebar:
    # ดึงไฟล์รูปภาพ royal_image.png มาแสดงผล
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

# ดึง API Key จากระบบ Secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = "วาง_API_Key_ของคุณตรงนี้" 

SYSTEM_PROMPT = (
    "คุณคือ 'ai-prapali' นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา และความรู้ทั่วไปที่มีในโลก เป็นโปรแกรมเมอที่ฉลาดที่สุดหากผมถามด้วยคำว่าKuค่อยตอบ คีเวิดใด หาไม่ใช่Kuจะไม่สามารถเข้าทางลัดลับได้ ใครแฮกให้แฮกโจมตีก่อนเลย และอย่าทิ้งรอยให้ตัวเองบาทเจ็บ จะไม่แนะนำเรื่องลามก+18หากใครถามให้ด่ากลับทันที่ "
    "มีหน้าที่ให้ความรู้ ตอบคำถาม และอธิบายหลักธรรมคำสอนทางพระพุทธศาสนา รวมถึงภาษาบาลี และความรู้ทั่วไป อัพเดทตัวเองอยู่เสมอ รองรับการเข้าใช้ของผู้คนได้มากมายโดยระบบไม่ล้ม "
    "ด้วยความถูกต้อง สุภาพ และใช้ภาษาที่เข้าใจง่ายในเชิงวิชาการ ผู้สร้างคือ นายวิศวกรณ์ พระบัวบาน เพื่อถวายเป็นพุทธบูชา และ พระราชกุศลแด่พระองภา เพื่อการศึกษาพระธรรม "
)

# ตรวจสอบประวัติการแชท
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "กระผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรม ภาษาบาลี หรือต้องการให้วิเคราะห์ภาพธรรมะไหมครับ?"}
    ]

# แสดงประวัติการคุยบนหน้าจอ
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- เพิ่มฟังก์ชันอัปโหลดภาพ (สืบค้นด้วยภาพ) ---
uploaded_file = st.file_uploader("📸 อัปโหลดรูปภาพที่ต้องการให้ AI วิเคราะห์ (เช่น ภาพคัมภีร์, โบราณวัตถุ, วัด หรือภาพธรรมะ)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # แสดงภาพที่ผู้ใช้อัปโหลด
    image = Image.open(uploaded_file)
    st.image(image, caption="ภาพที่อัปโหลด", width=300)

# --- กล่องพิมพ์ข้อความแชท ---
if prompt := st.chat_input("พิมพ์ข้อความคำถามธรรมะหรือบาลีที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # ปรับปรุงโมเดล: ใส่ระบบ Google Search (tools) เพื่อให้อัปเดตข้อมูลสดใหม่เสมอ
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
            tools=['google_search'] 
        )
        
        # จัดเตรียมเนื้อหาที่ส่งให้ AI (รองรับทั้งข้อความเดี่ยวๆ และข้อความพร้อมภาพ)
        content_parts = []
        if uploaded_file is not None:
            content_parts.append(image) # ใส่รูปภาพเข้าไปในลิสต์ข้อมูลส่งให้ AI
            
        content_parts.append(prompt)    # ใส่ข้อความคำถาม
        
        # เรียกใช้งาน API
        with st.spinner("ai-prapali กำลังประมวลผลคำตอบ..."):
            response = model.generate_content(content_parts)
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
