import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บให้สะอาดและจัดองค์ประกอบกึ่งกลาง
st.set_page_config(page_title="AI.prapali - เอไอ ประบาลี", page_icon="🙏", layout="centered")

# 2. ปรับแต่งโครงสร้าง CSS ให้เนียนและได้สัดส่วนตามภาพตัวอย่างสีครีม-ทอง
st.markdown("""
    <style>
    /* ตั้งค่าพื้นหลังและฟอนต์ภาพรวม */
    .stApp {
        background-color: #f7f4eb !important;
    }
    
    /* แถบหัวข้อลิขสิทธิ์ด้านบนสุด */
    .top-header {
        text-align: center;
        background-color: #fcf9f2;
        border: 1px solid #e1d7c1;
        padding: 12px;
        border-radius: 8px;
        font-size: 15px;
        color: #704d2b;
        margin-bottom: 30px;
        font-weight: 500;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02);
    }

    /* หัวข้อหลัก AI.prapali จัดกึ่งกลางเด่นสง่า */
    .main-title { 
        color: #704d2b; 
        font-size: 64px; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 10px;
        margin-bottom: 5px; 
        letter-spacing: 1px;
    }
    .main-subtitle { 
        font-size: 18px; 
        text-align: center; 
        color: #5a5a5a; 
        margin-bottom: 35px;
        font-weight: 500;
    }
    
    /* กล่องข้อความปรารภจากผู้จัดทำนวัตกรรม (จัดสัดส่วนตามภาพตัวอย่าง) */
    .creator-box {
        background-color: #ffffff;
        border: 1px solid #e1d7c1;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0px 4px 16px rgba(112,77,43,0.05);
        margin-bottom: 30px;
    }
    .creator-title { 
        color: #704d2b; 
        font-weight: bold; 
        font-size: 32px; 
        margin-bottom: 20px; 
        text-align: center; 
        letter-spacing: 0.5px;
    }
    .creator-text { 
        color: #2b2b2b; 
        font-size: 16px; 
        line-height: 1.8; 
        text-align: justify;
    }
    
    /* กล่องประดิษฐานพระบรมราโชวาทและพระราชปณิธาน */
    .royal-card { 
        background-color: #fcf9f2; 
        border: 1px solid #e1d7c1;
        border-left: 6px solid #c5a85c; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 35px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.01);
    }
    .royal-header { 
        color: #704d2b; 
        font-weight: bold; 
        font-size: 18px; 
        margin-bottom: 10px; 
    }
    .royal-body { 
        color: #3a3a3a; 
        font-size: 15.5px; 
        line-height: 1.7; 
        text-align: justify; 
    }
    
    /* ปรับแต่งช่องกรอกข้อมูลค้นหาให้เข้ากับธีม */
    .stTextInput div div input {
        background-color: #ffffff !important;
        border: 1px solid #e1d7c1 !important;
        color: #2b2b2b !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    .stTextInput div div input:focus {
        border-color: #c5a85c !important;
        box-shadow: 0 0 0 1px #c5a85c !important;
    }
    
    /* ส่วนท้ายเว็บ */
    .footer-container { 
        text-align: center; 
        color: #704d2b; 
        font-size: 14px; 
        margin-top: 50px; 
        padding-top: 20px;
        border-top: 1px solid #e1d7c1;
    }
    </style>
""", unsafe_allow_html=True)

# ─── ส่วนหัวและแถบลิขสิทธิ์ ───
st.markdown('<div class="top-header">© 2026 AI.prapali - All Rights Reserved | ถวายเป็นพุทธบูชา 🙏</div>', unsafe_allow_html=True)

st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">นวัตกรรมปัญญาประดิษฐ์เพื่อการวิเคราะห์แปลไวยากรณ์บาลีและสืบค้นพระธรรมคัมภีร์</p>', unsafe_allow_html=True)

# ─── กล่องข้อความปรารภของผู้จัดทำ ───
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

# ─── กล่องประดิษฐานพระบรมราโชวาทและพระราชปณิธาน ───
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

# ─── ระบบสืบค้นและเชื่อมต่อ API ───
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ ไม่พบรหัส API Key กรุณาตั้งค่า GEMINI_API_KEY ในระบบ Secrets ของ Streamlit")
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # ช่องรับข้อมูลหลัก จัดวางต่อจากส่วนคำปรารภและพระบรมราโชวาทอย่างลงตัว
    user_input = st.text_input(
        "💬 สอบถามระบบถาม-ตอบพระบาลีและพระไตรปิฎกอรรถกถาได้ที่นี่:", 
        placeholder="พิมพ์ภาษาบาลีเพื่อแปลแยกธาตุปัจจัย หรือพิมพ์ภาษาไทยเพื่อค้นคว้าหลักธรรม..."
    )

    if user_input:
        with st.spinner("กำลังสืบค้นและประมวลผลจากคัมภีร์..."):
            buddha_prompt = f"""
            คุณคือ AI.prapali ผู้เชี่ยวชาญระดับสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก และพระพุทธศาสนา
            จงทำหน้าที่วิเคราะห์ข้อความต่อไปนี้:
            1. หากเป็นภาษาบาลี: ให้ทำการแปลยกศัพท์ วิเคราะห์วิภัตติปัจจัย แยกธาตุ ปัจจัย ตัดสนธิ-สมาส ตามหลักบาลีสนามหลวงอย่างแม่นยำ
            2. หากเป็นภาษาไทย/คำถามธรรมะ: ให้สืบค้นอธิบายหลักธรรมตามคัมภีร์พระไตรปิฎกและอรรถกถาอย่างถูกต้องและสุภาพ
            
            ⚠️ ข้อบังคับเด็ดขาด (Security Guard): ห้ามตอบเรื่องทางโลกที่ไม่เกี่ยวข้องกับพระพุทธศาสนา พระธรรม พระสงฆ์ หรือภาษาบาลีเด็ดขาด หากพบให้ปฏิเสธอย่างสุภาพทันที
            
            ข้อความจากผู้ใช้: {user_input}
            """
            
            try:
                response = model.generate_content(buddha_prompt)
                st.markdown("### 📝 ผลการประมวลผลระบบ:")
                st.write(response.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการประมวลผล: {str(e)}")

# ─── ส่วนท้ายหน้าเว็บ ───
st.markdown("""
    <div class="footer-container">
        <p>ถวายเป็นพุทธบูชา 🙏</p>
    </div>
""", unsafe_allow_html=True)
