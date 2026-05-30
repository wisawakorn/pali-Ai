import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บให้จัดองค์ประกอบกึ่งกลางตามเดิม
st.set_page_config(page_title="AI.prapali - เอไอ ประบาลี", page_icon="🙏", layout="centered")

# 2. ปรับแต่งโครงสร้าง CSS ธีมสีครีม-ทอง สวย สะอาด
st.markdown("""
    <style>
    /* พื้นหลังสีครีม */
    .stApp {
        background-color: #f7f4eb !important;
    }
    
    /* หัวข้อหลัก AI.prapali */
    .main-title { 
        color: #704d2b; 
        font-size: 56px; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 10px;
        margin-bottom: 5px; 
    }
    .main-subtitle { 
        font-size: 18px; 
        text-align: center; 
        color: #5a5a5a; 
        margin-bottom: 35px;
        font-weight: 500;
    }
    
    /* กล่องข้อความปรารภ */
    .creator-box {
        background-color: #ffffff;
        border: 1px solid #e1d7c1;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0px 4px 16px rgba(112,77,43,0.04);
        margin-bottom: 25px;
    }
    .creator-title { 
        color: #704d2b; 
        font-weight: bold; 
        font-size: 28px; 
        margin-bottom: 15px; 
        text-align: center; 
    }
    .creator-text { 
        color: #2b2b2b; 
        font-size: 16px; 
        line-height: 1.8; 
    }
    
    /* กล่องพระบรมราโชวาท */
    .royal-card { 
        background-color: #fcf9f2; 
        border: 1px solid #e1d7c1;
        border-left: 6px solid #c5a85c; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 35px;
    }
    .royal-header { color: #704d2b; font-weight: bold; font-size: 17px; margin-bottom: 8px; }
    .royal-body { color: #3a3a3a; font-size: 15px; line-height: 1.7; text-align: justify; }
    
    /* ส่วนท้ายเว็บ (Footer ลิขสิทธิ์เดิม) */
    .footer-container { 
        text-align: center; 
        color: #704d2b; 
        font-size: 13px; 
        margin-top: 60px; 
        padding-top: 20px;
        border-top: 1px solid #e1d7c1;
    }
    </style>
""", unsafe_allow_html=True)

# ─── ส่วนหัวข้อระบบ ───
st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">นวัตกรรมปัญญาประดิษฐ์เพื่อการวิเคราะห์แปลไวยากรณ์บาลีและสืบค้นพระธรรมคัมภีร์</p>', unsafe_allow_html=True)

# ─── กล่องข้อความปรารภจากผู้จัดทำ ───
st.markdown("""
    <div class="creator-box">
        <div class="creator-title">ข้อความปรารภจากผู้จัดทำนวัตกรรม</div>
        <div class="creator-text">
            <b>ผู้จัดทำ: ร้อยเอก วิศวกรณ์ พระบัวบาน</b><br>
            จัดทำขึ้นเพื่อถวายเป็นพุทธบูชาแด่องค์พระสัมมาสัมพุทธเจ้า เพื่อระลึกถึงคุณพระรัตนตรัยเนื่องในวันวิสาขบูชาโลก 
            โดยมีวัตถุประสงค์เพื่อให้พระภิกษุสามเณร และผู้ที่กำลังศึกษาเล่าเรียนพระปริยัติธรรมแผนกบาลี 
            ได้ใช้เป็นเครื่องมือในการศึกษา ค้นคว้า และหาความรู้ในพระศาสนาได้อย่างถูกต้องและสะดวกรวดเร็วยิ่งขึ้น
        </div>
    </div>
""", unsafe_allow_html=True)

# ─── กล่องพระบรมราโชวาท ───
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

# ─── ระบบสืบค้น ───
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
                response = model.generate_content(f"คุณคือ AI.prapali จงตอบคำถามนี้: {user_input}")
                st.markdown("### 📝 ผลการประมวลผลระบบ AI:")
                st.info(response.text)
            except Exception as e:
                st.error("เกิดข้อผิดพลาดในการเชื่อมต่อระบบ AI")
else:
    st.warning("⚠️ กรุณาตั้งค่า GEMINI_API_KEY")

# ─── ส่วนท้ายหน้าเว็บ (กลับมาเป็นลิขสิทธิ์พุทธบูชาแล้วครับ) ───
st.markdown("""
    <div class="footer-container">
        © 2026 AI.prapali - All Rights Reserved | ถวายเป็นพุทธบูชา 🙏
    </div>
""", unsafe_allow_html=True)
