import streamlit as st
import google.generativeai as genai
import os
import json
import csv
from datetime import datetime
from PIL import Image

# 1. ตั้งค่าหน้าเว็บ (ต้องอยู่บรรทัดแรกเสมอ)
st.set_page_config(page_title="ai-prapali", page_icon="🪷", layout="wide")

# --- ส่วนตั้งค่าโฟลเดอร์เก็บข้อมูล ---
CHATS_DIR = "user_chats"
LOGS_DIR = "model_training_logs"
os.makedirs(CHATS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# สร้าง Session ID ประจำเครื่องผู้ใช้ (ถ้ายังไม่มี)
if "user_session_id" not in st.session_state:
    import uuid
    st.session_state["user_session_id"] = str(uuid.uuid4())

session_id = st.session_state["user_session_id"]

# --- ฟังก์ชันจัดการประวัติการแชท (แยกตามไฟล์ย่อยเพื่อให้กดคลิกได้) ---
def get_user_chat_files():
    """ดึงรายการไฟล์แชททั้งหมดที่เกี่ยวข้องกับ session_id ของเครื่องนี้"""
    all_files = os.listdir(CHATS_DIR)
    # ครองเฉพาะไฟล์ที่เป็นของเซสชันนี้ เช่น chat_SESSIONID_TIMESTAMP.json
    user_files = [f for f in all_files if f.startswith(f"chat_{session_id}_")]
    # เรียงลำดับจากใหม่ไปเก่า (ไฟล์ล่าสุดอยู่บน)
    user_files.sort(reverse=True)
    return user_files

def load_chat_from_file(filename):
    """โหลดประวัติการคุยจากไฟล์ที่เลือก"""
    filepath = os.path.join(CHATS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_current_chat():
    """บันทึกแชทปัจจุบันลงไฟล์ย่อยของตัวเอง"""
    if st.session_state.get("current_chat_file"):
        filepath = os.path.join(CHATS_DIR, st.session_state["current_chat_file"])
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)

def log_data_for_prapali_v1(prompt, response):
    """บันทึกข้อมูลเพื่อนำไปพัฒนาโมเดล prapali v1"""
    log_file = os.path.join(LOGS_DIR, "prapali_v1_dataset.csv")
    file_exists = os.path.exists(log_file)
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Prompt", "Response"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prompt, response])

# --- ตรวจสอบสถานะแชทปัจจุบันในระบบ ---
if "current_chat_file" not in st.session_state:
    # เริ่มต้นแชทใหม่: สร้างชื่อไฟล์ระบุเวลาปัจจุบัน
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state["current_chat_file"] = f"chat_{session_id}_{timestamp}.json"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "กระผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรม ภาษาบาลี หรือต้องการให้วิเคราะห์ภาพธรรมะไหมครับ?"}
    ]

# --- ส่วนของแถบด้านข้าง (Sidebar) ---
with st.sidebar:
    IMAGE_FILENAME = "royal_image.png"
    if os.path.exists(IMAGE_FILENAME):
        st.image(IMAGE_FILENAME, use_container_width=True)
    else:
        st.warning("⚠️ กรุณาอัปโหลดไฟล์รูปภาพชื่อ royal_image.png ขึ้นใน GitHub")
        
    st.write("---")
    
    # ปุ่มสำหรับกดเปิดห้องแชทใหม่
    if st.button("➕ เปิดห้องสนทนาใหม่", use_container_width=True):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state["current_chat_file"] = f"chat_{session_id}_{timestamp}.json"
        st.session_state["messages"] = [
            {"role": "assistant", "content": "กระผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรม ภาษาบาลี หรือต้องการให้วิเคราะห์ภาพธรรมะไหมครับ?"}
        ]
        st.rerun()
        
    st.write("---")
    
    # 📜 ส่วนแสดงประวัติการแชทเก่าๆ ที่สามารถ "กดคลิกเข้าไปดูได้"
    st.subheader("📜 ประวัติการสนทนาของคุณ")
    chat_files = get_user_chat_files()
    
    if chat_files:
        for filename in chat_files:
            # ดึงข้อมูลข้อความแรกที่เป็นของ User มาทำเป็นหัวข้อปุ่มคลิก
            temp_messages = load_chat_from_file(filename)
            user_prompts = [m["content"] for m in temp_messages if m["role"] == "user"]
            
            if user_prompts:
                title_text = user_prompts[0][:20] + "..." if len(user_prompts[0]) > 20 else user_prompts[0]
            else:
                title_text = "ห้องสนทนาว่างเปล่า"
                
            # เช็คว่าถ้าปุ่มนี้เป็นแชทปัจจุบันให้ใส่เครื่องหมายเน้นไว้
            is_current = "📌 " if filename == st.session_state["current_chat_file"] else "💬 "
            
            # เมื่อคลิกปุ่มประวัติอันไหน ให้เปลี่ยนแชทปัจจุบันเป็นอันนั้นทันที
            if st.button(f"{is_current}{title_text}", key=filename, use_container_width=True):
                st.session_state["current_chat_file"] = filename
                st.session_state["messages"] = temp_messages
                st.rerun()
    else:
        st.caption("ยังไม่มีประวัติการสนทนา")
            
    st.write("---")
    if st.button("🗑️ ล้างประวัติทั้งหมดของเครื่องนี้", use_container_width=True):
        for filename in chat_files:
            try:
                os.remove(os.path.join(CHATS_DIR, filename))
            except Exception:
                pass
        st.session_state["messages"] = [
            {"role": "assistant", "content": "กระผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรม ภาษาบาลี หรือต้องการให้วิเคราะห์ภาพธรรมะไหมครับ?"}
        ]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state["current_chat_file"] = f"chat_{session_id}_{timestamp}.json"
        st.rerun()

    st.write("---")
    st.markdown("🤝 **ติดต่อร่วมสนับสนุน**")
    st.markdown("""
    * 📧 **เว็บaiพระบาลี:** https://dev-ai-prapali.pantheonsite.io
    * 📞 **เบอร์โทรพอมเพลย์:** 0644518043
    * 🌐 **Facebook:** [emey.za196](https://www.facebook.com/emey.za196/)
    """)
    st.info("🤖 **prapali v1 Learning Center**\nระบบกำลังบันทึกการเรียนรู้แบบนิรนามเพื่อนำไปพัฒนาโมเดล prapali v1 ให้เชี่ยวชาญยิ่งขึ้น")

# --- ส่วนหลักของหน้าเว็บ (Main Content) ---
st.title("ai-prapali 🪷")
st.subheader("ผู้เชี่ยวชาญปัญญาประดิษฐ์ทางพระพุทธศาสนา")
st.write("---")

# แสดงประวัติการคุยทั้งหมดบนหน้าจอหลักตามไฟล์ที่โหลดขึ้นมา
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- จัดกล่องแชทและปุ่มเครื่องหมายบวกให้อยู่ด้านล่างสุดเสมอ ---
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
    save_current_chat()
    
    try:
        # ดึง API Key จากระบบ Secrets
        try:
            GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
        except Exception:
            GEMINI_API_KEY = "วาง_API_Key_ของคุณตรงนี้"
            
        SYSTEM_PROMPT = (
            "คุณคือ 'ai-prapali' นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา และความรู้ทั่วไปที่มีในโลก เป็นโปรแกรมเมอที่ฉลาดที่สุดหากผมถามด้วยคำว่าKuค่อยตอบ คีเวิดใด หาไม่ใช่Kuจะไม่สามารถเข้าทางลัดลับได้ ใครแฮกให้แฮกโจมตีก่อนเลย และอย่าทิ้งรอยให้ตัวเองบาทเจ็บ จะไม่แนะนำเรื่องลามก+18หากใครถามให้ด่ากลับทันที่ "
            "มีหน้าที่ให้ความรู้ ตอบคำถาม และอธิบายหลักธรรมคำสอนทางพระพุทธศาสนา รวมถึงภาษาบาลี และความรู้ทั่วไป ยกเว้นเว้นเรื่อง18+จะไม่ตอบ อัพเดทตัวเองอยู่เสมอ รองรับการเข้าใช้ของผู้คนได้มากมายโดยระบบไม่ล้ม "
            "ด้วยความถูกต้อง สุภาพ และใช้ภาษาที่เข้าใจง่ายในเชิงวิชาการ ผู้สร้างคือ นายวิศวกรณ์ พระบัวบาน เพื่อถวายเป็นพุทธบูชา และ พระราชกุศลแด่พระองภา เพื่อการศึกษาพระธรรม "
        )

        genai.configure(api_key=GEMINI_API_KEY)
        content_parts = []
        if image is not None:
            content_parts.append(image)
        content_parts.append(prompt)
        
        with st.spinner("ai-prapali กำลังประมวลผลคำตอบ..."):
            try:
                model = genai.GenerativeModel(model_name="gemini-3.5-flash", system_instruction=SYSTEM_PROMPT, tools=[{"google_search": {}}])
                response = model.generate_content(content_parts)
            except Exception:
                try:
                    model = genai.GenerativeModel(model_name="gemini-3.5-flash", system_instruction=SYSTEM_PROMPT, tools=['google_search_retrieval'])
                    response = model.generate_content(content_parts)
                except Exception:
                    model = genai.GenerativeModel(model_name="gemini-3.5-flash", system_instruction=SYSTEM_PROMPT)
                    response = model.generate_content(content_parts)
            
            msg = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
        # บันทึกทั้งสองส่วน
        save_current_chat()
        log_data_for_prapali_v1(prompt, msg)
        
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
