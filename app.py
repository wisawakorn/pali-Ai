import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# 1. ตั้งค่าหน้าเว็บ (ต้องอยู่บรรทัดแรกๆ ของระบบ Streamlit เสมอ)
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

# ตรวจสอบประวัติการแชทใน Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "กระผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรม ภาษาบาลี หรือต้องการให้วิเคราะห์ภาพธรรมะไหมครับ?"}
    ]

# แสดงประวัติการคุยทั้งหมดบนหน้าจอ
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# --- สร้างแถวควบคุมด้านล่าง (กล่องแชท + ปุ่มบวกสำหรับสืบค้นด้วยภาพ) ---
# ใช้ st.columns เพื่อดันปุ่ม ➕ ให้ไปอยู่ข้างซ้ายของกล่อง chat_input อย่างสวยงาม
col_btn, col_chat = st.columns([1, 7], vertical_alignment="bottom")

uploaded_file = None
image = None

with col_btn:
    # ปุ่ม popover เป็นเครื่องหมายบวก เมื่อกดแล้วจะมีหน้าต่างเล็กๆ ให้เลือกรูปภาพ
    with st.popover("➕", help="คลิกเพื่ออัปโหลดหรือสืบค้นด้วยภาพ"):
        uploaded_file = st.file_uploader(
            "อัปโหลดรูปภาพที่ต้องการให้ AI วิเคราะห์", 
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="ภาพที่เลือกไว้", use_container_width=True)

with col_chat:
    prompt = st.chat_input("พิมพ์ข้อความคำถามธรรมะหรือบาลีที่นี่...")

# --- ส่วนประมวลผลการทำงานเมื่อกดส่งคำถาม ---
if prompt:
    # 1. บันทึกและแสดงคำถามฝั่งผู้ใช้
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        # 2. ตั้งค่าการเชื่อมต่อ Gemini API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # 3. เรียกใช้งานโมเดลพร้อมเปิดระบบเปิด Google Search (ทำให้ข้อมูลอัปเดตสดใหม่ตลอดเวลา)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
            tools=['google_search'] 
        )
        
        # 4. มัดรวมข้อมูลที่จะส่งให้ AI (ตรวจสอบว่ามีภาพติดไปด้วยหรือไม่)
        content_parts = []
        if image is not None:
            content_parts.append(image)  # ส่งรูปภาพเข้าไป
            
        content_parts.append(prompt)     # ส่งข้อความคำถามตัวหนังสือเข้าไป
        
        # 5. สั่งประมวลผลคำตอบ
        with st.spinner("ai-prapali กำลังประมวลผลคำตอบ..."):
            response = model.generate_content(content_parts)
            msg = response.text
        
        # 6. บันทึกและแสดงคำตอบฝั่ง AI Assistant
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

# --- ข้อความลิขสิทธิ์ท้ายหน้าเว็บ ---
st.write("") 
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85rem; padding-top: 20px;'>"
    "© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน<br>"
    "พัฒนาขึ้นเพื่อถวายเป็นพุทธบูชา และ เป็นพระราชกุศลแด่พระองค์ภา เพื่อสนับสนุนการศึกษาพระปริยัติธรรมและภาษาบาลี"
    "</div>", 
    unsafe_allow_html=True
)
