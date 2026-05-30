import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บให้สะอาดและจัดองค์ประกอบกึ่งกลาง
st.set_page_config(page_title="AI.prapali - เอไอ ประบาลี", page_icon="🙏", layout="centered")

# 2. ปรับแต่งโครงสร้าง CSS ให้เนียนตามธีมสีครีม-ทอง
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f4eb !important;
    }
    
    /* หัวข้อหลัก AI.prapali */
    .main-title { 
        color: #704d2b; 
        font-size: 64px; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 20px;
        margin-bottom: 5px; 
        letter-spacing: 1px;
    }
    .main-subtitle { 
        font-size: 18px; 
        text-align: center; 
        color: #5a5a5a; 
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    /* กล่องพระบรมราโชวาท */
    .royal-card { 
        background-color: #fcf9f2; 
        border: 1px solid #e1d7c1;
        border-left: 6px solid #c5a85c; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 30px;
    }
    .royal-header { color: #704d2b; font-weight: bold; font-size: 18px; margin-bottom: 10px; }
    .royal-body { color: #3a3a3a; font-size: 15.5px; line-height: 1.7; text-align: justify; }

    /* ปรับแต่งช่องกรอกข้อมูลค้นหา */
    .stTextInput div div input {
        background-color: #ffffff !important;
        border: 1px solid #e1d7c1 !important;
        color: #2b2b2b !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }

    /* กล่องข้อความรวมด้านล่างสุด (ลิขสิทธิ์ + ข้อความปรารภ ตัวอักษรเท่ากันทั้งหมด) */
    .footer-combined-box { 
        text-align: center; 
        color: #704d2b; 
        font-size: 14.5px; 
        line-height: 1.8;
        margin-top: 50px; 
        padding: 25px;
        background-color: #fcf9f2;
        border: 1px solid #e1d7c1;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.02);
    }
    .footer-copyright {
        font-weight: bold;
        margin-bottom: 12px;
        font-size: 15px;
    }
    .footer-paragraph {
        text-align: justify;
        text-justify: inter-word;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ─── ส่วนหัวข้อระบบ ───
st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">นวัตกรรมปัญญาประดิษฐ์เพื่อการวิเคราะห์แปลไวยากรณ์บาลีและสืบค้นพระธรรมคัมภีร์</p>', unsafe_allow_html=True)

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
        placeholder="พิมพ์ภาษาบาลีเพื่อแปล หรือพิมพ์ภาษาไทยเพื่อค้นคว้าหลักธรรม..."
    )
    if user_input:
        with st.spinner("กำลังประมวลผล..."):
            try:
                buddha_prompt = f"""
                คุณคือ AI.prapali ผู้เชี่ยวชาญระดับสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก และพระพุทธศาสนา
                จงทำหน้าที่วิเคราะห์ข้อความต่อไปนี้ตามหลักการทางพระพุทธศาสนา: {user_input}
                ⚠️ ข้อบังคับเด็ดขาด: ห้ามตอบเรื่องทางโลกที่ไม่เกี่ยวข้องกับพระพุทธศาสนาเด็ดขาด
                """
                response = model.generate_content(buddha_prompt)
                st.markdown("### 📝 ผลการประมวลผล:")
                st.write(response.text)
            except Exception as e:
                st.error("เกิดข้อผิดพลาดในการเชื่อมต่อ")
else:
    st.error("⚠️ กรุณาตั้งค่า API Key")

# ─── กล่องด้านล่างสุด: รวมลิขสิทธิ์และข้อความปรารภต่อท้องกัน ขนาดตัวอักษรเท่ากันตามสั่ง ───
st.markdown("""
    <div class="footer-combined-box">
        <div class="footer-copyright">
            © 2026 AI.prapali - All Rights Reserved | ถวายเป็นพุทธบูชา 🙏
        </div>
        <div class="footer-paragraph">
            <b>ข้อความปรารภจากผู้จัดทำนวัตกรรม (ผู้จัดทำ: ร้อยเอก วิศวกรณ์ พระบัวบาน):</b> 
            จัดทำขึ้นเพื่อถวายเป็นพุทธบูชาแด่องค์พระสัมมาสัมพุทธเจ้า เพื่อระลึกถึงคุณพระรัตนตรัยเนื่องในวันวิสาขบูชาโลก 
            โดยมีวัตถุประสงค์เพื่อให้พระภิกษุสามเณร และผู้ที่กำลังศึกษาเล่าเรียนพระปริยัติธรรมแผนกบาลี 
            ได้ใช้เป็นเครื่องมือในการศึกษา ค้นคว้า และหาความรู้ในพระศาสนาได้อย่างถูกต้องและสะดวกรวดเร็วยิ่งขึ้น
        </div>
    </div>
""", unsafe_allow_html=True)
