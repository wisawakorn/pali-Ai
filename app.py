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


# --- สร้างส่วนควบคุมอินพุตด้านล่าง (กล่องแชท + ปุ่มบวกสำหรับอัปโหลดภาพ) ---
# ใช้ st.columns แบ่งพื้นที่ด้านล่าง โดยให้ปุ่มเครื่องหมายบวกอยู่ฝั่งซ้าย และกล่องแชทหลักอยู่ฝั่งขวา
col_btn, col_chat = st.columns([1, 7], vertical_alignment="bottom")

uploaded_file = None
image = None

with col_btn:
    # ปุ่ม popover รูปเครื่องหมายบวก เมื่อกดแล้วจะมีหน้าต่างเล็กๆ เด้งขึ้นมาให้อัปโหลดไฟล์ภาพ
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

# --- ส่วนของการประมวลผลเมื่อผู้ใช้งานกดส่งข้อความ ---
if prompt:
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
        if image is not None:
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
