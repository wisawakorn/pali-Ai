import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime
from PIL import Image

# 1. ตั้งค่าหน้าเว็บ (ต้องอยู่บรรทัดแรกของระบบ Streamlit เสมอ)
st.set_page_config(page_title="ai-prapali", page_icon="🪷", layout="wide")

# --- 📜 [เพิ่มส่วนนี้] ตั้งค่าระบบเก็บไฟล์ประวัติแชทแยกห้อง ---
CHATS_DIR = "user_chats"
os.makedirs(CHATS_DIR, exist_ok=True)

# ดึงหรือสร้าง Session ID ประจำเบราว์เซอร์ของผู้ใช้
if "user_session_id" not in st.session_state:
    import uuid
    st.session_state["user_session_id"] = str(uuid.uuid4())

session_id = st.session_state["user_session_id"]

def get_user_chat_files():
    """ดึงรายการไฟล์แชททั้งหมดของเครื่องนี้"""
    try:
        all_files = os.listdir(CHATS_DIR)
        user_files = [f for f in all_files if f.startswith(f"chat_{session_id}_")]
        user_files.sort(reverse=True)
        return user_files
    except Exception:
        return []

def load_chat_from_file(filename):
    """โหลดประวัติจากไฟล์ที่คลิกเลือก"""
    filepath = os.path.join(CHATS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_current_chat():
    """บันทึกแชทปัจจุบันลงไฟล์ย่อยประจำห้องนั้น"""
    if st.session_state.get("current_chat_file"):
        filepath = os.path.join(CHATS_DIR, st.session_state["current_chat_file"])
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)

# กำหนดชื่อไฟล์สำหรับห้องแชทปัจจุบันใน Session State
if "current_chat_file" not in st.session_state:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state["current_chat_file"] = f"chat_{session_id}_{timestamp}.json"


# --- ส่วนของแถบด้านข้าง (Sidebar) ---
with st.sidebar:
    IMAGE_FILENAME = "royal_image.png"
    
    if os.path.exists(IMAGE_FILENAME):
        st.image(IMAGE_FILENAME, use_container_width=True)
    else:
        st.warning("⚠️ กรุณาอัปโหลดไฟล์รูปภาพชื่อ royal_image.png ขึ้นใน GitHub")
        
    st.write("---")
    
    # ➕ [เพิ่มส่วนนี้] ปุ่มเปิดห้องสนทนาใหม่
    if st.button("➕ เปิดห้องสนทนาใหม่", use_container_width=True):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state["current_chat_file"] = f"chat_{session_id}_{timestamp}.json"
        st.session_state["messages"] = [
            {"role": "assistant", "content": "กระผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรม ภาษาบาลี หรือต้องการให้วิเคราะห์ภาพธรรมะไหมครับ?"}
        ]
        st.rerun()

    st.write("---")

    # 📜 [เพิ่มส่วนนี้] รายการแสดงประวัติแชทเก่าเพื่อให้กดเรียกดูได้
    st.subheader("📜 ประวัติการสนทนาของคุณ")
    chat_files = get_user_chat_files()
    
    if chat_files:
        for filename in chat_files:
            temp_messages = load_chat_from_file(filename)
            user_prompts = [m["content"] for m in temp_messages if m["role"] == "user"]
            
            if user_prompts:
                title_text = user_prompts[0][:20] + "..." if len(user_prompts[0]) > 20 else user_prompts[0]
            else:
                title_text = "ห้องสนทนาว่างเปล่า"
                
            is_current = "📌 " if filename == st.session_state["current_chat_file"] else "💬 "
            
            if st.button(f"{is_current}{title_text}", key=filename, use_container_width=True):
                st.session_state["current_chat_file"] = filename
                st.session_state["messages"] = temp_messages
                st.rerun()
    else:
        st.caption("ยังไม่มีประวัติการสนทนา")

    st.write("---")
    
    # ส่วนข้อมูลติดต่อและสนับสนุน (คงเดิมตามโค้ดคุณ)
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


# --- 📌 จัดกล่องแชทและปุ่มเครื่องหมายบวกให้อยู่ด้านล่างสุดเสมอ ---
input_container = st.container()

uploaded_file = None
image = None

with input_container:
    col_btn, col_chat = st.columns([1, 7], vertical_alignment="bottom")

    with col_btn:
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
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    save_current_chat() # 💾 [เพิ่มส่วนนี้] บันทึกประวัติฝั่งผู้ใช้ลงไฟล์ก่อนส่ง
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # มัดรวมข้อมูลอินพุต (ภาพ + ข้อความคำถาม)
        content_parts = []
        if image is not None:
            content_parts.append(image)
        content_parts.append(prompt)
        
        with st.spinner("ai-prapali กำลังประมวลผลคำตอบ..."):
            # ระบบสลับโหมดอัตโนมัติ (Fallback) ของเดิมของคุณทั้งหมด
            try:
                # แผน A
                model = genai.GenerativeModel(
                    model_name="gemini-3.5-flash",
                    system_instruction=SYSTEM_PROMPT,
                    tools=[{"google_search": {}}]
                )
                response = model.generate_content(content_parts)
            except Exception:
                try:
                    # แผน B
                    model = genai.GenerativeModel(
                        model_name="gemini-3.5-flash",
                        system_instruction=SYSTEM_PROMPT,
                        tools=['google_search_retrieval']
                    )
                    response = model.generate_content(content_parts)
                except Exception:
                    # แผน C
                    model = genai.GenerativeModel(
                        model_name="gemini-3.5-flash",
                        system_instruction=SYSTEM_PROMPT
                    )
                    response = model.generate_content(content_parts)
            
            msg = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
        save_current_chat() # 💾 [เพิ่มส่วนนี้] บันทึกคำตอบของ AI ลงไฟล์ประวัติ
        st.rerun()
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")

# --- ข้อความลิขสิทธิ์ท้ายหน้าเว็บ ---
st.write("") 
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85rem; padding-top: 20px; padding-bottom: 60px;'>"
    "© 2026 AI.prapali | สงวนลิขสิทธิ์โดย นายวิศวกรณ์ พระบัวบาน<br>"
    "พัฒนาขึ้นเพื่อถวายเป็นพุทธบูชา และ เป็นพระราชกุศลแด่พระองค์ภา เพื่อสนับสนุนการศึกษาพระปริยัติธรรมและภาษาบาลี"
    "</div>", 
    unsafe_allow_html=True
)
