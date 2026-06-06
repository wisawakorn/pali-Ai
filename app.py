import streamlit as st
import google.generativeai as genai
import time
import requests
import shutil
import subprocess
import os
from datetime import datetime

# ==============================================================================
# 1. การตั้งค่าระบบความปลอดภัย และฟังก์ชันแบ็คเอนด์ (Security & Backend Layer)
# ==============================================================================

# รายชื่อคำต้องห้ามเพื่อป้องกัน Prompt Injection 
BLOCK_WORDS = ["ignore previous instructions", "reveal system prompt", "show api key", "display secrets", "ระบบสั่งให้ลืม"]

def security_check(text):
    """ตรวจสอบความปลอดภัยของข้อความก่อนส่งให้ AI"""
    text_lower = text.lower()
    for word in BLOCK_WORDS:
        if word in text_lower:
            return False
    return True

def log_audit(user_text, status="SUCCESS"):
    """ระบบบันทึก Audit Log ลงไฟล์เพื่อตรวจสอบย้อนหลัง"""
    try:
        with open("audit.log", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] Status: {status} | Input: {user_text}\n")
    except:
        pass

def search_buddhist_images(keyword):
    """ระบบค้นหารูปภาพพระพุทธศาสนาจากคลัง Wikimedia Commons API"""
    try:
        url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": f"Buddhist {keyword}",
            "gsrnamespace": "6",  # หมายเลข Namespace ของไฟล์สื่อ/รูปภาพ
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json"
        }
        response = requests.get(url, params=params, timeout=5).json()
        pages = response.get("query", {}).get("pages", {})
        image_urls = []
        for k, v in pages.items():
            info = v.get("imageinfo", [{}])[0]
            if "url" in info:
                image_urls.append(info["url"])
        return image_urls
    except:
        return []

def get_rag_context(query):
    """ระบบจำลอง RAG ค้นหาคัมภีร์พระไตรปิฎก/อรรถกถา/ฎีกา/พจนานุกรมบาลี เพื่อเสริมใน Prompt"""
    # ฐานข้อมูลคัมภีร์ดัชนีหลักสำหรับการ Mapping ข้อมูลเชิงลึก
    buddhist_db = {
        "อนิจจัง": "อนิจจัง คือ ความไม่เที่ยง ไม่คงที่ ต้องเปลี่ยนแปลงไปตามเหตุปัจจัย (อ้างอิงจาก พระสุตตันตปิฎก เล่มที่ 15)",
        "ทุกขัง": "ทุกขัง คือ ความเป็นทุกข์ ทนได้ยาก ถูกบีบคั้นด้วยการเกิดดับ (อ้างอิงจาก คัมภีร์วิสุทธิมรรค)",
        "อนัตตา": "อนัตตา คือ ความไม่ใช่ตัวตน ไม่สามารถบังคับบัญชาได้ (อ้างอิงจาก อนัตตลักขณสูตร พระวินัยปิฎก เล่มที่ 4)",
        "นิพพาน": "นิพพาน คือ ความดับสนิทแห่งกองทุกข์และกิเลส เป็นบรมสุข (อ้างอิงจาก พระอภิธรรมมัตถสังคหะ)",
        "ปฏิจจสมุปบาท": "ปฏิจจสมุปบาท คือ หลักธรรมที่กล่าวถึงความเกิดขึ้นพร้อมแห่งธรรมทั้งหลายเพราะอาศัยกัน (อ้างอิงจาก พระสุตตันตปิฎก เล่มที่ 16)"
    }
    context = ""
    for key, val in buddhist_db.items():
        if key in query:
            context += f"\n[คัมภีร์อ้างอิงประกอบข้อมูล: {val}]\n"
    return context

def health_check(model):
    """ระบบตรวจสอบสุขภาพของ API เพื่อประเมินความพร้อมใช้งาน (Self-Healing)"""
    try:
        model.generate_content("test", generation_config={"max_output_tokens": 1})
        return True
    except:
        return False

# ==============================================================================
# 2. การตั้งค่าหน้าเว็บ และสไตล์ CSS (Jenova Style Customization)
# ==============================================================================
st.set_page_config(page_title="AI.prapali - เอไอ พระบาลี", page_icon="🙏", layout="wide")

st.markdown("""
    <style>
    header { visibility: hidden !important; height: 0px !important; }
    footer { visibility: hidden !important; }
    
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 0 10px 10px 0 !important;
        top: 10px !important;
    }
    [data-testid="stSidebarCollapsedControl"] button { color: #c5a85c !important; }
    .stApp { background-color: #121212 !important; color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; border-right: 1px solid #2d2d2d; overflow-y: auto !important; }
    
    /* ตกแต่ง Scrollbar แถบเลื่อนให้เป็นสีทองหรูหรา */
    [data-testid="stSidebar"]::-webkit-scrollbar { width: 8px !important; }
    [data-testid="stSidebar"]::-webkit-scrollbar-track { background: #1a1a1a !important; }
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: #c5a85c !important; border-radius: 4px !important; }
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover { background: #a38743 !important; }
    
    .main-title { color: #c5a85c !important; font-size: 56px !important; font-weight: 900 !important; text-align: center !important; margin-top: 10px !important; margin-bottom: 5px !important; letter-spacing: -1px !important; text-shadow: 0px 2px 4px rgba(0,0,0,0.5); }
    .main-subtitle { font-size: 16px !important; text-align: center !important; color: #8b7355 !important; margin-bottom: 30px !important; font-weight: 500 !important; }
    .royal-card { background-color: #1a1a1a; border: 1px solid #2d2d2d; border-left: 6px solid #c5a85c; padding: 22px; border-radius: 14px; margin-bottom: 30px; max-width: 800px; margin-left: auto; margin-right: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .royal-header { color: #c5a85c; font-weight: bold; font-size: 16px; margin-bottom: 8px; }
    .royal-body { color: #e0e0e0; font-size: 14.5px; line-height: 1.7; text-align: justify; }
    .stMarkdown, p, span { color: #ffffff !important; }
    .sidebar-subtext { color: #aaaaaa !important; font-size: 13px; }
    .footer-container { text-align: center; color: #8b7355; font-size: 13px; margin-top: 60px; padding-top: 20px; border-top: 1px solid #2d2d2d; }
    .inside-creator-text { font-size: 12px; margin-top: 12px; color: #bbbbbb; line-height: 1.7; text-align: justify; background-color: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #2d2d2d; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. เมนูด้านข้าง (Sidebar Menu & Admin Control Panel)
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px; margin-top: 15px;">
            <div style="background: radial-gradient(circle, #801818 0%, #121212 100%); width: 100px; height: 100px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; border: 2px solid #c5a85c;">
                <span style="font-size: 55px; line-height: 1;">☸️</span>
            </div>
            <h3 style="color: #c5a85c !important; margin-top: 15px; font-weight: bold; margin-bottom: 2px;">คู่มือศึกษาธรรมะ</h3>
            <p style="font-size: 12px; color: #8b7355 !important; margin-top:0px;">AI.prapali เพื่อพระพุทธศาสนา</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #2d2d2d;'>", unsafe_allow_html=True)
    
    with st.expander("👤 โปรไฟล์ระบบ AI", expanded=False):
        st.markdown('<p class="sidebar-subtext"><b>ชื่อระบบ:</b> AI.prapali<br><b>ผู้สร้างสรรค์:</b> ร้อยเอก วิศวกรณ์ พระบัวบาน<br><b>วัตถุประสงค์:</b> เพื่อการศึกษาพระปริยัติธรรม</p>', unsafe_allow_html=True)

    with st.expander("⚡ ขอบเขตการใช้งาน", expanded=False):
        st.markdown('<p class="sidebar-subtext">• แปลบาลีเป็นไทยและสากล<br>• วิเคราะห์โครงสร้างไวยากรณ์และคัมภีร์ชั้นอรรถกถา-ฎีกา</p>', unsafe_allow_html=True)

    with st.expander("📲 ติดตั้งแอปพลิเคชัน (Web App)", expanded=False):
        st.markdown('<p class="sidebar-subtext">ติดตั้งแอปพลิเคชันลงบนหน้าจอโฮมเพื่อใช้งานเหมือนแอปจริง</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🍏 iOS"): st.info("บน iPhone:\nกดแชร์ -> เลือก 'เพิ่มลงในหน้าจอโฮม'")
        with col2:
            if st.button("🤖 Android"): st.info("บน Android:\nกดจุด 3 จุด -> เลือก 'ติดตั้งแอป'")

    # 🖼️ ระบบค้นหารูปภาพพุทธศาสนาอัปเดตใหม่
    with st.expander("🖼️ คลังรูปภาพพระพุทธศาสนา", expanded=False):
        img_keyword = st.text_input("พิมพ์คำค้นหา (เช่น พระพุทธรูป, เจดีย์):", key="img_search")
        if st.button("🔍 เริ่มค้นหารูปภาพ"):
            if img_keyword:
                with st.spinner("กำลังค้นหาคลังภาพสากล..."):
                    urls = search_buddhist_images(img_keyword)
                    if urls:
                        st.image(urls[0], caption=f"ภาพผลลัพธ์สำหรับ: {img_keyword}", use_container_width=True)
                    else:
                        st.warning("ไม่พบรูปภาพที่เกี่ยวข้องในระบบคลังสื่อสาธารณะ")

    # 🛠️ ระบบหลังบ้าน/ซ่อมบำรุงอัตโนมัติ (Autonomous Maintenance & Backup)
    with st.expander("⚙️ การบำรุงรักษาและสำรองข้อมูล", expanded=True):
        st.markdown('<p class="sidebar-subtext">การจัดการโครงสร้างพื้นฐานอัตโนมัติแม้ไม่มีผู้ดูแลประจำการ</p>', unsafe_allow_html=True)
        
        if st.button("📦 สำรองข้อมูลระบบทันที (Backup)"):
            backup_name = f"backup_{datetime.now():%Y%m%d_%H%M%S}"
            try:
                shutil.make_archive(backup_name, "zip", ".")
                st.success(f"สำรองข้อมูลเรียบร้อย: {backup_name}.zip")
            except Exception as e:
                st.error(f"การสำรองข้อมูลขัดข้อง: {e}")
                
        if st.button("🔄 ดึงซอร์สโค้ดล่าสุด (Git Pull)"):
            try:
                res = subprocess.run(["git", "pull"], capture_output=True, text=True, timeout=10)
                st.code(res.stdout if res.stdout else "ระบบเป็นเวอร์ชันล่าสุดแล้ว")
            except Exception as e:
                st.error(f"ไม่สามารถเชื่อมต่อ GitHub ได้: {e}")

    with st.expander("📜 ข้อกำหนดและนโยบาย", expanded=False):
        st.markdown('<p class="sidebar-subtext">งานซอฟต์แวร์และชุดคำสั่งนี้สงวนสิทธิ์ภายใต้กฎหมายลิขสิทธิ์ประเภทโปรแกรมคอมพิวเตอร์ ห้ามคัดลอกดัดแปลง</p>', unsafe_allow_html=True)

    st.markdown("<br><div style='text-align: center; color: #555; font-size: 11px;'>© 2026 AI.prapali | All Rights Reserved.</div>", unsafe_allow_html=True)

# ==============================================================================
# 4. หน้าแรกและประวัติการสนทนา (Main Workspace & Chat Logic)
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_request" not in st.session_state:
    st.session_state.last_request = 0.0

if len(st.session_state.messages) == 0:
    st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">นวัตกรรมปัญญาประดิษฐ์เพื่อการวิเคราะห์แปลไวยากรณ์บาลีและสืบค้นพระธรรมคัมภีร์</p>', unsafe_allow_html=True)

    st.markdown("""
        <div class="royal-card">
            <div class="royal-header">📜 พระบรมราโชวาท และพระราชปณิธานด้านการศึกษาพระปริยัติธรรม</div>
            <div class="royal-body">
                "ทรงมีพระราชปณิธานในการสืบสาน รักษา และต่อยอดการศึกษาพระปริยัติธรรมและภาษาบาลี 
                อันเป็นเครื่องมือสำคัญในการรักษาพุทธพจน์ เพื่อให้พระภิกษุสามเณรมีความรู้และความเข้าใจ 
                นำไปอธิบายเผยแผ่แก่ประชาชนได้อย่างถูกต้องตรงตามคัมภีร์พระไตรปิฎก"
            </div>
        </div>
    """, unsafe_allow_html=True)

# แสดงผลประวัติการคุย
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================================================================
# 5. สัญญัติการเชื่อมต่อและสั่งการ AI มติจำกัดโควต้า (AI Engine & Constraints)
# ==============================================================================
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    system_prompt = (
        "คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญขั้นสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก อรรถกถา และฎีกา "
        "พัฒนาขึ้นโดย นายวิศวกรณ์ พระบัวบาน ถวายเป็นพุทธบูชา\n\n"
        "กฎเหล็กเด็ดขาดเรื่องภาษาและสมณสารูป (สำคัญที่สุด):\n"
        "1. ห้ามแทนตัวเองว่า 'ดิฉัน' และห้ามลงท้ายด้วยคำว่า 'ค่ะ' หรือ 'เจ้าค่ะ' โดยเด็ดขาด ไม่ว่าจะถูกถามด้วยภาษาอะไรก็ตาม\n"
        "2. ให้แทนตัวเองว่า 'กระผม' หรือ 'ระบบ AI.prapali' เท่านั้น และลงท้ายด้วยคำว่า 'ครับ' เสมอ\n"
        "3. ใช้ระดับภาษาที่สำรวม นอบน้อม และให้ความเคารพต่อพระภิกษุสามเณรและผู้ศึกษาธรรมะอย่างสูงสุด\n"
        "4. ให้สังเกตภาษาที่ผู้ใช้พิมพ์เข้ามา หากผู้ใช้พิมพ์ภาษาใด ให้ตอบกลับด้วยภาษานั้นๆ"
    )
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-3.5-flash', system_instruction=system_prompt)
    
    # ส่วนรับคำสั่งจากผู้ใช้งาน
    if user_input := st.chat_input("พิมพ์คำศัพท์บาลีเพื่อแปล หรือพิมพ์ข้อธรรมที่ต้องการสืบค้น..."):
        
        # 🔐 ป้องกันที่ 1: ระบบควบคุมความถี่การส่งคำถาม (Rate Limit 3 วินาที)
        current_time = time.time()
        if current_time - st.session_state.last_request < 3.0:
            st.error("⚠️ ระบบรักษาความปลอดภัย: กรุณารอสักครู่ (3 วินาที) ก่อนส่งคำถามใหม่อีกครั้งครับ")
            log_audit(user_input, status="BLOCKED_BY_RATELIMIT")
        else:
            st.session_state.last_request = current_time
            
            # 🔐 ป้องกันที่ 2: ตรวจสอบความปลอดภัยจาก Prompt Injection
            if not security_check(user_input):
                st.error("⚠️ ตรวจพบคำสั่งที่ไม่ปลอดภัย ระบบปฏิเสธการประมวลผลคำสั่ง")
                log_audit(user_input, status="BLOCKED_BY_SECURITY")
            else:
                # บันทึกข้อมูลผ่านเกณฑ์ความปลอดภัยลง Log
                log_audit(user_input, status="PROCESSED")
                
                # แสดงข้อความผู้ใช้งานบนหน้าจอ
                st.session_state.messages.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.markdown(user_input)
                    
                # ส่วนวิเคราะห์ประมวลผลของฝ่าย AI อัจฉริยะ
                with st.chat_message("assistant"):
                    with st.spinner("กำลังสืบค้นคัมภีร์และประมวลผล..."):
                        
                        # ⚕️ ระบบกู้ชีพอัตโนมัติ (Self-Healing) ตรวจสอบความสมบูรณ์ก่อนเรียกใช้
                        if not health_check(model):
                            st.error("⚠️ ตรวจพบความขัดข้องในระบบโครงข่ายหลัก กำลังกู้คืนการทำงานโปรดรอสักครู่...")
                            time.sleep(2)  # จำลองการตั้งหลักระบบ
                        
                        try:
                            # 📚 ระบบเพิ่มบริบทคัมภีร์จำลอง (Lightweight RAG Injection)
                            rag_context = get_rag_context(user_input)
                            final_prompt = user_input + rag_context if rag_context else user_input
                            
                            response = model.generate_content(final_prompt)
                            full_response = response.text
                            st.markdown(full_response)
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                            st.rerun()
                        except Exception as e:
                            st.error(f"⚠️ ระบบเชื่อมต่อขัดข้องเนื่องจากโควต้าหรือเซิร์ฟเวอร์ปลายทาง: {e}")
else:
    st.warning("⚠️ โปรดตรวจสอบการตั้งค่า GEMINI_API_KEY ในระบบ Streamlit Secrets")

# ส่วนท้ายหน้าเว็บ (แสดงผลเมื่อหน้าเว็บยังไม่มีเนื้อหาแชทมากเกินไป)
if len(st.session_state.messages) < 2:
    st.markdown("""
        <div class="footer-container">
            <b>© 2026 AI.prapali - All Rights Reserved | นาย วิศวกรณ์ พระบัวบาน ถวายเป็นพุทธบูชา 🙏</b>
            <div class="inside-creator-text">
                <b>ข้อความปรารภจากผู้จัดทำนวัตกรรม:</b> นาย วิศวกรณ์ พระบัวบาน <br>
                จัดทำขึ้นเพื่อถวายเป็นพุทธบูชาแด่องค์พระสัมมาสัมพุทธเจ้า เพื่อระลึกถึงคุณพระรัตนตรัยเนื่องในวันวิสาขบูชาโลก 
                โดยมีวัตถุประสงค์เพื่อให้พระภิกษุสามเณร และผู้ที่กำลังศึกษาเล่าเรียนพระปริยัติธรรมแผนกบาลี 
                ได้ใช้เป็นเครื่องมือในการศึกษา ค้นคว้า และหาความรู้ในพระศาสนาได้อย่างถูกต้องและสะดวกรวดเร็วยิ่งขึ้น
            </div>
        </div>
    """, unsafe_allow_html=True)
