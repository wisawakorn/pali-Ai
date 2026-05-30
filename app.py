import streamlit as st
import google.generativeai as genai

# 1. ตั้งค่าหน้าเว็บให้สะอาดและกว้างขวางแบบมินิมอล
st.set_page_config(page_title="AI.prapali - เอไอ ประบาลี", page_icon="🙏", layout="centered")

# 2. ปรับแต่งสไตล์ (CSS) ขยายหัวข้อและปรับแต่งองค์ประกอบให้สมภาคภูมิ
st.markdown("""
    <style>
    /* ตั้งค่าฟอนต์และพื้นหลัง */
    body { background-color: #faf8f5; }
    
    /* ขยายขนาดหัวข้อหลักตามความประสงค์ */
    .main-title { 
        color: #8B5A2B; 
        font-size: 52px; /* ขยายขนาดตัวอักษรให้ใหญ่เด่นชัด */
        font-weight: bold; 
        text-align: center; 
        margin-top: 10px;
        margin-bottom: 5px; 
        letter-spacing: 1px;
    }
    .main-subtitle { font-size: 16px; text-align: center; color: #666666; margin-bottom: 25px; }
    
    /* กล่องพระราชปณิธานด้านการศึกษาปริยัติธรรม */
    .royal-card { 
        background-color: #FFFBF0; 
        border: 1px solid #E6D5B8;
        border-left: 5px solid #D4AF37; 
        padding: 15px; 
        border-radius: 8px; 
        margin-bottom: 25px;
    }
    .royal-header { color: #8B6508; font-weight: bold; font-size: 14px; margin-bottom: 4px; }
    .royal-body { color: #555555; font-size: 14px; line-height: 1.5; }
    
    /* กล่องข้อความผู้จัดทำและวัตถุประสงค์ใต้ช่องค้นหา */
    .creator-box {
        background-color: #fcfcfc;
        border: 1px dashed #D4AF37;
        padding: 20px;
        border-radius: 8px;
        margin-top: 25px;
        text-align: center;
    }
    .creator-title { color: #8B5A2B; font-weight: bold; font-size: 15px; margin-bottom: 8px; }
    .creator-text { color: #444444; font-size: 14px; line-height: 1.6; text-align: justify; text-justify: inter-word; }
    
    /* ส่วนท้ายเว็บ */
    .footer-container { 
        text-align: center; 
        color: #8B5A2B; 
        font-size: 12px; 
        margin-top: 40px; 
        padding-top: 15px;
        border-top: 1px solid #EAEAEA;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ประดิษฐานรูปพระพุทธปฏิมากรโทนสีขาวสไตล์ศิลปะร่วมสมัยด้านบนสุดเพื่อเป็นสัญลักษณ์
# ใช้ภาพพระพุทธรูปสีขาวลายเส้นวิจิตรสวยงามและจัดตำแหน่งไว้ตรงกลาง
st.image(
    "https://images.unsplash.com/photo-1609137144813-7d72110c7324?q=80&w=300", 
    width=180, 
    use_container_width=False
)

# แสดงหัวข้อระบบขนาดใหญ่ขึ้นตามต้องการ
st.markdown('<p class="main-title">AI.prapali</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">นวัตกรรมปัญญาประดิษฐ์เพื่อการวิเคราะห์แปลไวยากรณ์บาลีและสืบค้นพระธรรมคัมภีร์</p>', unsafe_allow_html=True)

# แสดงกล่องพระราชปณิธานสนองพระบรมราโชวาท
st.markdown("""
    <div class="royal-card">
        <div class="royal-header">📜 พระราชปณิธานด้านการศึกษาพระปริยัติธรรม</div>
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
    # เริ่มต้นเชื่อมต่อโมเดลล่าสุด (Gemini 1.5 Flash)
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # ช่องพิมพ์รับข้อมูลแบบเด่นชัดตรงกลางหน้าเว็บ (Clean & Simple Input)
    user_input = st.text_input(
        "💬 สอบถามระบบถาม-ตอบพระบาลีและพระไตรปิฎกอรรถกถาได้ที่นี่:", 
        placeholder="พิมพ์ภาษาบาลีเพื่อแปลแยกธาตุปัจจัย หรือพิมพ์ภาษาไทยเพื่อค้นคว้าหลักธรรม..."
    )

    # เมื่อมีการกดค้นหาหรือพิมพ์ข้อความ
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

# 4. แทรกกล่องข้อความผู้จัดทำและวัตถุประสงค์พุทธบูชาไว้ใต้ช่องตารางค้นหาทันทีตามที่ระบุ
st.markdown("""
    <div class="creator-box">
        <div class="creator-title">🙏 ข้อความปรารภจากผู้จัดทำนวัตกรรม</div>
        <div class="creator-text">
            <b>ผู้จัดทำ: ร้อยเอก วิศวกรณ์ พระบัวบาน</b><br>
            จัดทำขึ้นเพื่อถวายเป็นพุทธบูชาแด่องค์พระสัมมาสัมพุทธเจ้า เพื่อระลึกถึงคุณพระรัตนตรัยเนื่องในวันวิสาขบูชาโลก 
            โดยมีวัตถุประสงค์เพื่อให้พระภิกษุสามเณร และผู้ที่กำลังศึกษาเล่าเรียนพระปริยัติธรรมแผนกบาลี 
            ได้ใช้เป็นเครื่องมือในการศึกษา ค้นคว้า และหาความรู้ในพระศาสนาได้อย่างถูกต้องและสะดวกรวดเร็วยิ่งขึ้น
        </div>
    </div>
""", unsafe_allow_html=True)

# ส่วนท้ายหน้าเว็บ (Footer)
st.markdown("""
    <div class="footer-container">
        <p>© 2026 AI.prapali - All Rights Reserved | ถวายเป็นพุทธบูชา</p>
    </div>
""", unsafe_allow_html=True)
