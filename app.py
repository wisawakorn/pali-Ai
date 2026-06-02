import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าโครงสร้างหน้าเว็บ จัดกึ่งกลางให้สวยงาม
st.set_page_config(page_title="AI.prapali - เอไอ พระบาลี", page_icon="🙏", layout="centered")

# 2. ปรับแต่งโครงสร้าง CSS ธีมสีครีม-ทอง สไตล์มินิมอล สะอาดตา
st.markdown("""
    <style>
    /* ซ่อนแถบเมนูและปุ่มเครื่องมือมุมขวาบนทั้งหมด */
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
    
    /* คัดลอกส่วนนี้ไปวางทับในกล่อง <style> ตัวเดิมได้เลยครับ */
.main-title { 
    color: #704d2b !important; 
    font-size: 72px !important; /* ปรับเพิ่มขนาดจากเดิมให้ใหญ่เต็มตา */
    font-weight: 900 !important; /* เพิ่มความหนาขั้นสุด */
    text-align: center !important; 
    margin-top: 25px !important;
    margin-bottom: 5px !important; 
    letter-spacing: 1px !important; /* เว้นระยะตัวอักษรให้ดูหรูหรา */
    }
    .main-subtitle { 
        font-size: 17px; 
        text-align: center; 
        color: #5a5a5a; 
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    /* กล่องพระบรมราโชวาทและพระราชปณิธาน */
    .royal-card { 
        background-color: #fcf9f2; 
        border: 1px solid #e1d7c1;
        border-left: 6px solid #c5a85c; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 30px;
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

# ─── ส่วนหัวข้อระบบ ───
st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">นวัตกรรมปัญญาประดิษฐ์เพื่อการวิเคราะห์แปลไวยากรณ์บาลีและสืบค้นพระธรรมคัมภีร์</p>', unsafe_allow_html=True)

# ─── กล่องพระบรมราโชวาทและพระราชปณิธาน ───
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

# ─── ระบบสืบค้นและช่องยิงคำถาม AI ───
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    user_input = st.text_input(
        "💬 สอบถามระบบถาม-ตอบพระบาลีและพระไตรปิฎกอรรถกถาได้ที่นี่:", 
        placeholder="พิมพ์คำศัพท์บาลีเพื่อแปล หรือพิมพ์ข้อธรรมที่ต้องการสืบค้น..."
    )
    
    if user_input:
        with st.spinner("กำลังสืบค้นและประมวลผล..."):
            try:
                response = model.generate_content(
                    f"คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญด้านภาษาบาลีและคัมภีร์พระไตรปิฎก "
                    f"จงตอบคำถามนี้ด้วยความถูกต้องและใช้สรรพนามที่เหมาะสม: {user_input}"
                )
                st.markdown("### 📝 ผลการประมวลผลระบบ AI:")
                st.info(response.text)
            except Exception as e:
                st.error("เกิดข้อผิดพลาดในการเชื่อมต่อระบบ AI")
else:
    st.warning("⚠️ โปรดตรวจสอบการตั้งค่า GEMINI_API_KEY ในระบบ Streamlit Secrets")

# ─── ส่วนท้ายหน้าเว็บ (รวมข้อความลิขสิทธิ์และข้อความปรารภย้ายมาต่อท้ายเรียบร้อยครับ) ───
st.markdown("""
    <div class="footer-container">
        <b>© 2026 AI.prapali - All Rights Reserved |นาย วิศวกรณ์ พระบัวบาน ถวายเป็นพุทธบูชา 🙏</b>
        <div class="inside-creator-text">
            <b>ข้อความปรารภจากผู้จัดทำนวัตกรรม:</b> นาย วิศวกรณ์ พระบัวบาน <br>
            จัดทำขึ้นเพื่อถวายเป็นพุทธบูชาแด่องค์พระสัมมาสัมพุทธเจ้า เพื่อระลึกถึงคุณพระรัตนตรัยเนื่องในวันวิสาขบูชาโลก 
            โดยมีวัตถุประสงค์เพื่อให้พระภิกษุสามเณร และผู้ที่กำลังศึกษาเล่าเรียนพระปริยัติธรรมแผนกบาลี 
            ได้ใช้เป็นเครื่องมือในการศึกษา ค้นคว้า และหาความรู้ในพระศาสนาได้อย่างถูกต้องและสะดวกรวดเร็วยิ่งขึ้น
        </div>
    </div>
""", unsafe_allow_html=True)
# วางโค้ดชุดนี้ไว้ในไฟล์ app.py เพื่อสร้างเมนูด้านข้างแบบมืออาชีพ
import streamlit as st

with st.sidebar:
    # 1. โลโก้และชื่อระบบด้านบนเมนู
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="font-size: 50px;">🙏</span> <!-- หรือเปลี่ยนเป็น URL รูปภาพโลโก้ธรรมจักรของผู้กองได้ครับ -->
            <h3 style="color: #704d2b; margin-top: 10px; font-weight: bold;">AI.prapali</h3>
            <p style="font-size: 13px; color: #666;">ระบบปัญญาประดิษฐ์เพื่อพระพุทธศาสนา</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 2. รายการเมนูสไตล์มินิมอล ถอดแบบจากต้นฉบับ
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

    # เมนู: ดาวน์โหลดแอป (ไฮไลต์เด็ดแบบของเขา)
    with st.expander("📲 ดาวน์โหลดแอปพลิเคชัน", expanded=True):
        st.markdown("""
            <div style="padding: 5px;">
                <!-- ปุ่ม iOS -->
                <a href="#" style="text-decoration: none;">
                    <div style="background-color: #111111; color: white; padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 8px; font-size: 13px; font-weight: 500;">
                        🍏 สำหรับ iOS (iPhone)
                    </div>
                </a>
                <!-- ปุ่ม Android -->
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
    
    # 3. ส่วนท้ายแถบเมนู
    st.markdown("""
        <div style="text-align: center; color: #888; font-size: 11px;">
            © 2026 AI.prapali<br>All Rights Reserved.
        </div>
    """, unsafe_allow_html=True)
