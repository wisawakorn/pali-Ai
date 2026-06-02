import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าโครงสร้างหน้าเว็บแบบ Wide และเปลี่ยนธีมให้เป็นแบบ Jenova Style (Dark Gold)
st.set_page_config(page_title="AI.prapali - เอไอ พระบาลี", page_icon="🙏", layout="wide")

# 2. ปรับแต่ง CSS เปลี่ยนโลกให้เป็นสีดาร์กโมดหรูหรา ตัดด้วยทองและส้มอิฐแบบหน้า Jenova
st.markdown("""
    <style>
    /* ซ่อนแถบเมนูของ Streamlit */
    header { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; }
    
    /* พื้นหลังมืดสนิทแบบ Jenova */
    .stApp {
        background-color: #121212 !important;
        color: #ffffff !important;
    }
    
    /* เมนูด้านข้างดาร์กโทน */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 1px solid #2d2d2d;
    }
    
    /* หัวข้อหลักตรงกลางหน้าจอ */
    .main-title { 
        color: #c5a85c !important; 
        font-size: 56px !important; 
        font-weight: 900 !important; 
        text-align: center !important; 
        margin-top: 10px !important;
        margin-bottom: 5px !important; 
        letter-spacing: -1px !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
    }
    .main-subtitle { 
        font-size: 16px !important; 
        text-align: center !important; 
        color: #8b7355 !important; 
        margin-bottom: 30px !important;
        font-weight: 500 !important;
    }
    
    /* กล่องพระบรมราโชวาทดีไซน์ดาร์กโกลด์ */
    .royal-card { 
        background-color: #1a1a1a; 
        border: 1px solid #2d2d2d;
        border-left: 6px solid #c5a85c; 
        padding: 22px; 
        border-radius: 14px; 
        margin-bottom: 30px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .royal-header { color: #c5a85c; font-weight: bold; font-size: 16px; margin-bottom: 8px; }
    .royal-body { color: #e0e0e0; font-size: 14.5px; line-height: 1.7; text-align: justify; }
    
    /* ปรับแต่งสีของฟอนต์ใน Expander (เมนูข้าง) ให้ชัดเจนบนพื้นหลังดำ */
    .stMarkdown, p, span { color: #ffffff !important; }
    .sidebar-subtext { color: #aaaaaa !important; font-size: 13px; }
    
    /* ส่วนท้ายหน้าเว็บ */
    .footer-container { 
        text-align: center; 
        color: #8b7355; 
        font-size: 13px; 
        margin-top: 60px; 
        padding-top: 20px;
        border-top: 1px solid #2d2d2d;
    }
    .inside-creator-text {
        font-size: 12px; 
        margin-top: 12px; 
        color: #bbbbbb; 
        line-height: 1.7;
        text-align: justify;
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2d2d2d;
    }
    </style>
""", unsafe_allow_html=True)

# ─── แถบเมนูด้านข้าง (Sidebar) ถอดแบบปุ่มจาก Jenova เป๊ะๆ ───
with st.sidebar:
    # โลโก้กงล้อธรรมจักรสีทอง/แดงเพลิง แบบ Jenova
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
    
    # รายการเมนูเรียงตามแบบหน้า Jenova เป๊ะๆ
    with st.expander("👤 โปรไฟล์ระบบ AI", expanded=False):
        st.markdown("""
            <p class="sidebar-subtext">
                <b>ชื่อระบบ:</b> AI.prapali (เอไอ พระบาลี)<br>
                <b>ผู้สร้างสรรค์:</b> ร้อยเอก วิศวกรณ์ พระบัวบาน<br>
                <b>วัตถุประสงค์:</b> ถวายเป็นพุทธบูชาเพื่อการศึกษาพระปริยัติธรรม
            </p>
        """, unsafe_allow_html=True)

    with st.expander("⚡ ขอบเขตการใช้งาน", expanded=False):
        st.markdown("""
            <p class="sidebar-subtext">
                • แปลภาษาบาลีเป็นภาษาไทยและท้องถิ่นทั่วโลก<br>
                • วิเคราะห์โครงสร้างไวยากรณ์ คัมภีร์พระไตรปิฎก อรรถกถา และฎีกา
            </p>
        """, unsafe_allow_html=True)

    with st.expander("💳 การสมัครสมาชิก", expanded=False):
        st.markdown("<p class="sidebar-subtext">เปิดใช้งานฟรีทุกฟังก์ชันเพื่อสนับสนุนกิจการคณะสงฆ์</p>", unsafe_allow_html=True)

    with st.expander("🤝 เชิญเพื่อน", expanded=False):
        st.markdown("<p class="sidebar-subtext">แชร์ลิงก์แอปพลิเคชันนี้เพื่อร่วมเผยแผ่เป็นธรรมทาน</p>", unsafe_allow_html=True)

    with st.expander("📲 ดาวน์โหลดแอปพลิเคชัน", expanded=True):
        st.markdown("""
            <div style="padding: 3px;">
                <a href="#" style="text-decoration: none;">
                    <div style="background-color: #ffffff; color: #000000 !important; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; font-size: 13px; font-weight: bold;">
                        🍏 สำหรับ iOS (iPhone)
                    </div>
                </a>
                <a href="#" style="text-decoration: none;">
                    <div style="background-color: #e57373; color: #ffffff !important; padding: 10px; border-radius: 8px; text-align: center; font-size: 13px; font-weight: bold;">
                        🤖 สำหรับ Android (.APK)
                    </div>
                </a>
            </div>
        """, unsafe_allow_html=True)

    with st.expander("📜 ข้อกำหนดและนโยบาย", expanded=False):
        st.markdown("<p class="sidebar-subtext">งานซอฟต์แวร์และชุดคำสั่งนี้สงวนสิทธิ์ภายใต้กฎหมายลิขสิทธิ์ประเภทโปรแกรมคอมพิวเตอร์ ห้ามคัดลอกดัดแปลง</p>", unsafe_allow_html=True)

    st.markdown("<br><div style='text-align: center; color: #555; font-size: 11px;'>© 2026 AI.prapali | All Rights Reserved.</div>", unsafe_allow_html=True)


# ─── ระบบความจำแชท (Chat Session State) ───
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── หน้าแรกตอนเริ่มต้น (จะซ่อนตัวเมื่อเริ่มคุยแบบ Gemini/Jenova) ───
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

# ─── การแสดงผลกล่องข้อความย้อนหลัง (Chat History) ───
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─── ระบบประมวลผลและการตั้งค่า API ───
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    # ตรึงกฎเหล็กดัดนิสัย AI ขั้นสูงสุด ล็อกเพศและระดับภาษาสำหรับสมณสารูป
    system_prompt = (
        "คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญขั้นสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก อรรถกถา และฎีกา "
        "พัฒนาขึ้นโดย นายวิศวกรณ์ พระบัวบาน ถวายเป็นพุทธบูชา\n\n"
        "กฎเหล็กเด็ดขาดเรื่องภาษาและสมณสารูป (สำคัญที่สุด):\n"
        "1. ห้ามแทนตัวเองว่า 'ดิฉัน' และห้ามลงท้ายด้วยคำว่า 'ค่ะ' หรือ 'เจ้าค่ะ' โดยเด็ดขาด ไม่ว่าจะถูกถามด้วยภาษาอะไรก็ตาม\n"
        "2. ให้แทนตัวเองว่า 'กระผม' หรือ 'ระบบ AI.prapali' เท่านั้น และลงท้ายด้วยคำว่า 'ครับ' เสมอ\n"
        "3. ใช้ระดับภาษาที่สำรวม นอบน้อม และให้ความเคารพต่อพระภิกษุสามเณรและผู้ศึกษาธรรมะอย่างสูงสุด\n"
        "4. ให้สังเกตภาษาที่ผู้ใช้พิมพ์เข้ามา หากผู้ใช้พิมพ์ภาษาใด ให้ตอบกลับด้วยภาษานั้นๆ (พิมพ์ไทยตอบไทย พิมพ์อังกฤษตอบอังกฤษ) แต่ต้องอยู่ภายใต้กฎข้อ 1 และ 2 เสมอ"
    )
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)
    
    # ช่องพิมพ์คำถามด้านล่างสุด (Floating Chat Input แบบหน้า Gemini / Jenova)
    if user_input := st.chat_input("พิมพ์คำศัพท์บาลีเพื่อแปล หรือพิมพ์ข้อธรรมที่ต้องการสืบค้น..."):
        
        # แสดงข้อความฝั่งผู้ใช้
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # ประมวลผลและแสดงข้อความฝั่ง AI (แก้ไขบั๊ก Indentation เรียบร้อย)
        with st.chat_message("assistant"):
            with st.spinner("กำลังสืบค้นและประมวลผล..."):
                try:
                    response = model.generate_content(user_input)
                    full_response = response.text
                    
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ ระบบเชื่อมต่อขัดข้องเนื่องจาก: {e}")
else:
    st.warning("⚠️ โปรดตรวจสอบการตั้งค่า GEMINI_API_KEY ในระบบ Streamlit Secrets")

# ─── ส่วนท้ายหน้าเว็บ (แสดงผลเมื่อหน้าเว็บยังคลีนอยู่) ───
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
