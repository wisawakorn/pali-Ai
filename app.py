import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บให้สะอาดแบบมินิมอลและจัดองค์ประกอบกึ่งกลาง
st.set_page_config(page_title="AI.prapali - เอไอ ประบาลี", page_icon="🙏", layout="centered")

# 2. ปรับแต่งสไตล์ (CSS) ตามธีมรูปภาพของผู้กอง (เน้นโทนสีน้ำตาล-ทอง สง่างาม)
st.markdown("""
    <style>
    body { background-color: #faf8f5; }
    
    /* แถบหัวข้อลิขสิทธิ์ด้านบนสุดตามแบบภาพ */
    .top-header {
        text-align: center;
        background-color: #FFFBF0;
        border: 1px solid #E6D5B8;
        padding: 10px;
        border-radius: 8px;
        font-size: 14px;
        color: #8B5A2B;
        margin-bottom: 25px;
        font-weight: 500;
    }

    /* หัวข้อหลัก AI.prapali ใหญ่เด่นสง่า */
    .main-title { 
        color: #8B5A2B; 
        font-size: 72px; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 10px;
        margin-bottom: 5px; 
        letter-spacing: 2px;
    }
    .main-subtitle { font-size: 18px; text-align: center; color: #666666; margin-bottom: 30px; }
    
    /* กล่องข้อความปรารภจากผู้จัดทำนวัตกรรม (เด่นตรงกลางตามแบบ) */
    .creator-box {
        background-color: #ffffff;
        border: 1px solid #E6D5B8;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 25px;
    }
    .creator-title { color: #5C3A21; font-weight: bold; font-size: 26px; margin-bottom: 15px; text-align: center; }
    .creator-text { color: #333333; font-size: 15px; line-height: 1.8; text-align: justify; }
    
    /* กล่องพระบรมราโชวาทและพระราชปณิธาน */
    .royal-card { 
        background-color: #FFFBF0; 
        border: 1px solid #E6D5B8;
        border-left: 5px solid #D4AF37; 
        padding: 20px; 
        border-radius: 8px; 
        margin-bottom: 25px;
    }
    .royal-header { color: #8B6508; font-weight: bold; font-size: 16px; margin-bottom: 8px; }
    .royal-body { color: #444444; font-size: 14.5px; line-height: 1.6; text-align: justify; }
    
    /* ส่วนท้ายเว็บ */
    .footer-container { 
        text-align: center; 
        color: #8B5A2B; 
        font-size: 14px; 
        margin-top: 40px; 
        padding-top: 15px;
        border-top: 1px solid #EAEAEA;
    }
    </style>
""", unsafe_allow_html=True)

# แสดงแถบลิขสิทธิ์และคำถวายพุทธบูชาด้านบนสุดตามแบบรูปภาพ
st.markdown('<div class="top-header">© 2026 AI.prapali - All Rights Reserved | ถวายเป็นพุทธบูชา 🙏</div>', unsafe_allow_html=True)

# แสดงหัวข้อแบรนด์ใหญ่พิเศษเด่นชัด
st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">นวัตกรรมปัญญาประดิษฐ์เพื่อการวิเคราะห์แปลไวยากรณ์บาลีและสืบค้นพระธรรมคัมภีร์</p>', unsafe_allow_html=True)

# ─── กล่องข้อความปรารภของผู้จัดทำ (ขึ้นก่อนตามแบบรูปภาพ) ───
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

# ดึงรหัส API Key จากระบบ Secrets ของ Streamlit
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ ไม่พบรหัส API Key กรุณาตั้งค่า GEMINI_API_KEY ในระบบ Secrets ของ Streamlit")
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # ช่องพิมพ์รับข้อมูล/ระบบค้นหาหลัก
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

# ส่วนท้ายหน้าเว็บตามที่ปรากฏในรูปภาพ
st.markdown("""
    <div class="footer-container">
        <p>ถวายเป็นพุทธบูชา 🙏</p>
    </div>
""", unsafe_allow_html=True)
