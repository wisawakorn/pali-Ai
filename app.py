import streamlit as st
import google.generativeai as genai
import time
import requests
import shutil
import subprocess
import os
from datetime import datetime

# ==============================================================================
# 1. เริ่มต้นระบบ AI Engine
# ==============================================================================
API_KEY = st.secrets.get("GEMINI_API_KEY")
model = None

if API_KEY:
    system_prompt = (
        "คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญขั้นสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก อรรถกถา และฎีกา "
        "พัฒนาขึ้นโดย นายวิศวกรณ์ พระบัวบาน ถวายเป็นพุทธบูชา\n\n"
        "กฎเหล็ก: ห้าม 'ค่ะ/เจ้าค่ะ' ให้ใช้ 'กระผม/ครับ' เท่านั้น สำรวม นอบน้อม ต่อพระภิกษุสามเณร"
    )
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-3.5-flash', system_instruction=system_prompt)

# ==============================================================================
# 2. ฟังก์ชันระบบหลังบ้านและความปลอดภัย
# ==============================================================================
BLOCK_WORDS = ["ignore previous instructions", "reveal system prompt", "show api key", "display secrets"]

def security_check(text):
    text_lower = text.lower()
    for word in BLOCK_WORDS:
        if word in text_lower: return False
    return True

def search_buddhist_images(keyword):
    try:
        url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query", "generator": "search", "gsrsearch": keyword,
            "gsrnamespace": "6", "prop": "imageinfo", "iiprop": "url", "format": "json"
        }
        response = requests.get(url, params=params, timeout=5).json()
        pages = response.get("query", {}).get("pages", {})
        return [v.get("imageinfo", [{}])[0].get("url") for k, v in pages.items() if v.get("imageinfo")]
    except: return []

# ==============================================================================
# 3. การตั้งค่าหน้าเว็บ และสไตล์ CSS (Dark Gold Jenova)
# ==============================================================================
st.set_page_config(page_title="AI.prapali - เอไอ พระบาลี", page_icon="🙏", layout="wide")

st.markdown("""
    <style>
    header { visibility: hidden !important; height: 0px !important; }
    footer { visibility: hidden !important; }
    .stApp { background-color: #121212 !important; color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; border-right: 1px solid #2d2d2d; }
    
    /* ตกแต่ง Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a1a; }
    ::-webkit-scrollbar-thumb { background: #c5a85c; border-radius: 4px; }
    
    .main-title { color: #c5a85c !important; font-size: 56px !important; font-weight: 900 !important; text-align: center; }
    .royal-card { background-color: #1a1a1a; border-left: 6px solid #c5a85c; padding: 22px; border-radius: 14px; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. Session State (หน่วยความจำ)
# ==============================================================================
if "messages" not in st.session_state: st.session_state.messages = []
if "last_request" not in st.session_state: st.session_state.last_request = 0.0
if "cached_image_url" not in st.session_state: st.session_state.cached_image_url = None

# ==============================================================================
# 5. Sidebar & Image Search
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#c5a85c;'>☸️ AI.prapali</h2>", unsafe_allow_html=True)
    with st.expander("🖼️ คลังรูปภาพพระพุทธศาสนา", expanded=True):
        img_keyword = st.text_input("คำค้นหา:", placeholder="เช่น เจดีย์, วัด")
        if st.button("🔍 ค้นหาภาพ"):
            with st.spinner("AI กำลังค้นหา..."):
                # ใช้ AI ช่วยแปลคีย์เวิร์ดเป็นอังกฤษเพื่อผลลัพธ์ที่ดีขึ้น
                search_query = img_keyword
                if model:
                    try:
                        res = model.generate_content(f"Translate to 1-2 English nouns: {img_keyword}")
                        search_query = res.text.strip()
                    except: pass
                urls = search_buddhist_images(search_query)
                if urls: st.session_state.cached_image_url = urls[0]
                else: st.session_state.cached_image_url = "NOT_FOUND"

        if st.session_state.cached_image_url:
            if st.session_state.cached_image_url == "NOT_FOUND": st.warning("ไม่พบรูปภาพ")
            else: st.image(st.session_state.cached_image_url, use_container_width=True)

# ==============================================================================
# 6. ส่วนการแสดงผลแชท
# ==============================================================================
if len(st.session_state.messages) == 0:
    st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
    st.markdown('<div class="royal-card"><b>📜 พระบรมราโชวาท:</b><br>"ทรงมีพระราชปณิธานในการสืบสาน รักษา และต่อยอดการศึกษาพระปริยัติธรรม..."</div>', unsafe_allow_html=True)

# วนลูปแสดงข้อความ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🚩 ส่วนสำคัญ: ปักหมุดจุดสิ้นสุดการสนทนา (Anchor)
st.markdown("<div id='latest-message'></div>", unsafe_allow_html=True)

# ==============================================================================
# 7. ระบบรับคำสั่งแชทและการ Scroll อัตโนมัติ
# ==============================================================================
if user_input := st.chat_input("พิมพ์คำศัพท์บาลีหรือข้อธรรม..."):
    if time.time() - st.session_state.last_request < 2.0:
        st.error("⚠️ กรุณารอสักครู่ครับ")
    elif not security_check(user_input):
        st.error("⚠️ คำสั่งไม่ปลอดภัย")
    else:
        st.session_state.last_request = time.time()
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.markdown(user_input)
            
        with st.chat_message("assistant"):
            with st.spinner("กำลังประมวลผล..."):
                try:
                    response = model.generate_content(user_input)
                    full_response = response.text
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    # ✨ ระบบ JavaScript สั่งให้เด้งลงมาที่หมุด 'latest-message' ทันที
                    st.components.v1.html(
                        """
                        <script>
                            var element = window.parent.document.getElementById('latest-message');
                            if (element) {
                                element.scrollIntoView({behavior: 'smooth'});
                            }
                        </script>
                        """,
                        height=0,
                    )
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ ขัดข้อง: {e}")

# กรณีที่มีข้อความอยู่แล้ว ให้รัน JS เพื่อเลื่อนลงมาเสมอเมื่อหน้าเว็บ Refresh
if len(st.session_state.messages) > 0:
    st.components.v1.html(
        """
        <script>
            setTimeout(function() {
                var element = window.parent.document.getElementById('latest-message');
                if (element) {
                    element.scrollIntoView({behavior: 'smooth'});
                }
            }, 500);
        </script>
        """,
        height=0,
    )
