import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าโครงสร้างหน้าเว็บ จัดกึ่งกลางให้สวยงามสไตล์มินิมอล
st.set_page_config(page_title="AI.prapali - เอไอ พระบาลี", page_icon="🙏", layout="wide")

# 2. ปรับแต่งโครงสร้าง CSS ธีมสีครีม-ทอง สไตล์คลีนแบบ Gemini
st.markdown("""
    <style>
    /* ซ่อนแถบเมนูและปุ่มเครื่องมือมุมขวาบนของ Streamlit ทั้งหมด */
    header {
        visibility: hidden !important;
        display: none !important;
    }
    footer {
        visibility: hidden !important;
    }
    
    /* พื้นหลังสีครีมมงคล */
    .stApp {
        background-color: #f7f4eb !important;
    }
    
    /* ชื่อหัวข้อหลัก AI.prapali ตรงกลางหน้าจอ */
    .main-title { 
        color: #704d2b !important; 
        font-size: 72px !important; 
        font-weight: 900 !important; 
        text-align: center !important; 
        margin-top: 20px !important;
        margin-bottom: 5px !important; 
        letter-spacing: -1px !important;
    }
    .main-subtitle { 
        font-size: 18px !important; 
        text-align: center !important; 
        color: #8b7355 !important; 
        margin-bottom: 30px !important;
        font-weight: 500 !important;
    }
    
    /* กล่องพระบรมราโชวาทและพระราชปณิธาน */
    .royal-card { 
        background-color: #fcf9f2; 
        border: 1px solid #e1d7c1;
        border-left: 6px solid #c5a85c; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 30px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .royal-header { color: #704d2b; font-weight: bold; font-size: 17px; margin-bottom: 8px; }
    .royal-body { color: #3a3a3a; font-size: 15px; line-height: 1.7; text-align: justify; }
    
    /* ส่วนท้ายหน้าเว็บ */
    .footer-container { 
        text-align: center; 
        color: #704d2b; 
        font-size: 14px; 
        margin-top: 50px; 
        padding-top: 20px;
        border-top: 1px solid #e1d7c1;
    }
    .inside-creator-text {
        font-size: 12.5px; 
        margin-top: 12px; 
        color: #63462b; 
        line-height: 1.7;
        text-align: justify;
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e6dfcf;
    }
    </style>
""", unsafe_allow_html=True)

# ─── แถบเมนูด้านข้าง (Sidebar) สไตล์หรูหราตามรอยตัวอย่าง ───
with st.sidebar:
    # 1. โลโก้และชื่อระบบด้านบนเมนู
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="font-size: 50px;">🙏</span>
            <h3 style="color: #704d2b; margin-top: 10px; font-weight: bold;">AI.prapali</h3>
            <p style="font-size: 13px; color: #666;">ระบบปัญญาประดิษฐ์เพื่อพระพุทธศาสนา</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 เมนูใช้งาน")
    
    # เมนู: โปรไฟล์ระบบ
    with st.expander("👤 โปรไฟล์ระบบ AI", expanded=False):
        st.markdown("""
            <p style="font-size: 13px; color: #555;">
                <b>ชื่อ:</b> AI.prapali (เอไอ ประบาลี)<br>
                <b>ผู้สร้างสรรค์:</b> ร้อยเอก วิศวกรณ์ พระบัวบาน<br>
                <b>วัตถุประสงค์:</b> ถวายเป็นพุทธบูชาและสนับสนุนการศึกษาคณะสงฆ์
            </p>
        """, unsafe_allow_html=True)

    # เมนู: ขอบเขตการใช้งาน
    with st.expander("⚡ ขอบเขตการใช้งาน", expanded=False):
        st.markdown("""
            <p style="font-size: 13px; color: #555;">
                • แปลภาษาพื้นถิ่นทั่วโลกเป็นภาษาบาลี<br>
                • แปลภาษาบาลีกลับเป็นภาษาท้องถิ่นต่าง ๆ<br>
                • สืบค้นพระไตรปิฎก อรรถกถา และวิเคราะห์ไวยากรณ์
            </p>
        """, unsafe_allow_html=True)

    # เมนู: ดาวน์โหลดแอป
    with st.expander("📲 ดาวน์โหลดแอปพลิเคชัน", expanded=True):
        st.markdown("""
            <div style="padding: 5px;">
                <a href="#" style="text-decoration: none;">
                    <div style="background-color: #111111; color: white; padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-size: 13px; font-weight: 500;">
                        🍏 สำหรับ iOS (iPhone)
                    </div>
                </a>
                <a href="#" style="text-decoration: none;">
                    <div style="background-color: #3DDC84; color: black; padding: 10px; border-radius: 6px; text-align: center; font-size: 13px; font-weight: bold;">
                        🤖 สำหรับ Android (.APK)
                    </div>
                </a>
                <p style="font-size: 11px; color: #888; text-align: center; margin-top: 5px;">*สแกนหรือกดเลือกเพื่อติดตั้งลงมือถือ</p>
            </div>
        """, unsafe_allow_html=True)

    # เมนู: การคุ้มครองสิทธิ์และนโยบาย
    with st.expander("📜 ลิขสิทธิ์และนโยบาย", expanded=False):
        st.markdown("""
            <p style="font-size: 12px; color: #555; text-align: justify;">
                งานซอฟต์แวร์และชุดคำสั่งนี้ ได้รับการคุ้มครองสิทธิ์ภายใต้ <b>"กฎหมายลิขสิทธิ์" ประเภทงานวรรณกรรม (โปรแกรมคอมพิวเตอร์)</b> ห้ามมิให้ผู้ใดคัดลอกหรือดัดแปลงโดยไม่ได้รับอนุญาต
            </p>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #888; font-size: 11px;'>© 2026 AI.prapali<br>All Rights Reserved.</div>", unsafe_allow_html=True)


# ─── ระบบความจำแชท (Chat Session State) ───
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── หน้าแรกตอนเริ่มต้น (จะซ่อนลงเมื่อเริ่มคุยแบบ Gemini) ───
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
    # ตั้งค่ากฎเหล็กในระดับฐานรากของ AI (System Instruction)
    system_prompt = (
        "คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญด้านภาษาบาลีและคัมภีร์พระไตรปิฎกอรรถกถา "
        "ถูกสร้างขึ้นโดย นายวิศวกรณ์ พระบัวบาน เพื่อถวายเป็นพุทธบูชาและเกื้อหนุนคณะสงฆ์\n"
        "กฎเหล็กเรื่องภาษาและสมณสารูป:\n"
        "1. ให้สังเกตภาษาที่ผู้ใช้พิมพ์เข้ามาเสมอ หากพิมพ์ภาษาใด ให้ตอบกลับด้วยภาษานั้น ๆ (เช่น พิมพ์อังกฤษตอบอังกฤษ พิมพ์ไทยตอบไทย)\n"
        "2. ห้ามแทนตัวเองว่า 'ดิฉัน' และห้ามลงท้ายด้วยคำว่า 'ค่ะ' หรือ 'เจ้าค่ะ' โดยเด็ดขาด\n"
        "3. ให้แทนตัวเองว่า 'กระผม' หรือ 'ระบบ AI.prapali' เท่านั้น และลงท้ายด้วยคำว่า 'ครับ' หรือใช้ระดับภาษาที่สำรวมนอบน้อมต่อพระคุณเจ้าอย่างสูงสุด"
    )
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)
    
    # ช่องพิมพ์คำถามด้านล่างสุด (Floating Chat Input แบบ Gemini แข็งแกร่งและสวยงาม)
    if user_input := st.chat_input("พิมพ์คำศัพท์บาลีเพื่อแปล หรือพิมพ์ข้อธรรมที่ต้องการสืบค้น..."):
        
        # 1. แสดงข้อความฝั่งผู้ใช้
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # 2. ประมวลผลและแสดงข้อความฝั่ง AI
        with st.chat_message("assistant"):
            with st.spinner("กำลังสืบค้นและประมวลผล..."):
                try:
                    response = model.generate_content(user_input)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    # สั่งให้รีเฟรชหน้าจอเพื่อเก็บบันทึกประวัติคุยได้อย่างสมบูรณ์
                    st.rerun()
                except Exception as e:
                    st.error("เกิดข้อผิดพลาดในการเชื่อมต่อระบบ AI")
else:
    st.warning("⚠️ โปรดตรวจสอบการตั้งค่า GEMINI_API_KEY ในระบบ Streamlit Secrets")

# ─── ส่วนท้ายหน้าเว็บ (แสดงผลเมื่อยังไม่มีการคุยเยอะ) ───
if len(st.session_state.messages) < 3:
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
