import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="บาลี AI", page_icon="🙏", layout="wide")

st.markdown("""
    <style>
    .title { color: #8B5A2B; font-size: 40px; font-weight: bold; text-align: center; }
    .subtitle { font-size: 18px; text-align: center; color: #555555; margin-bottom: 20px; }
    .royal-box { 
        background-color: #FFF8DC; 
        border-left: 5px solid #FFD700; 
        padding: 15px; 
        border-radius: 5px; 
        margin-bottom: 25px;
    }
    .royal-title { color: #8B6508; font-weight: bold; font-size: 16px; margin-bottom: 5px; }
    .royal-text { color: #4A3C31; font-size: 15px; line-height: 1.6; }
    .footer { 
        text-align: center; 
        color: #8B5A2B; 
        font-size: 14px; 
        margin-top: 50px; 
        padding: 20px;
        border-top: 1px solid #eeeeee;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">AI.prapaliระบบวิเคราะห์และแปลบาลีไวยากรณ์</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">เพื่อการศึกษาพระปริยัติธรรม ถวายเป็นพุทธบูชาเนื่องในวันวิสาขบูชา</p>', unsafe_allow_html=True)

# พระราชปณิธาน
st.markdown("""
    <div class="royal-box">
        <div class="royal-title">📜 พระราชปณิธานและแนวพระบรมราโชวาทด้านการศึกษาพระปริยัติธรรม</div>
        <div class="royal-text">
            "การศึกษาพระปริยัติธรรมและภาษาบาลี เป็นเครื่องมือสำคัญในการรักษาพุทธพจน์ 
            ทรงมีพระราชปณิธานในการสืบสาน รักษา และต่อยอด เพื่อให้พระภิกษุสามเณรมีความรู้ความเข้าใจ 
            ในหลักธรรมคำสอนของพระพุทธเจ้าอย่างถูกต้อง แตกฉาน และนำความรู้นั้นมาอธิบายเผยแผ่ 
            ให้แก่ประชาชนได้อย่างถูกต้องตรงตามคัมภีร์พระไตรปิฎก"
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# ดึงรหัส API Key
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("กรุณาตั้งค่า GEMINI_API_KEY ในระบบ Secrets ของ Streamlit")
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

    st.write("### 📝 กรอกประโยคหรือคำศัพท์ที่ต้องการสืบค้น")
    user_input = st.text_input("พิมพ์บาลีเพื่อแปล หรือพิมพ์ไทยเพื่อค้นธรรมะ", placeholder="ตัวอย่าง: ปุริโส คามํ คจฺฉติ หรือ อริยสัจ 4 คืออะไร")

    if user_input:
        with st.spinner("กำลังประมวลผล..."):
            buddha_prompt = f"""
            คุณคือผู้เชี่ยวชาญด้านภาษาบาลีและพระพุทธศาสนา 
            1. หากเป็นภาษาบาลี: ให้แปลยกศัพท์และวิเคราะห์ไวยากรณ์บาลีสนามหลวงอย่างละเอียด
            2. หากเป็นคำถามธรรมะ: ให้สืบค้นและอธิบายตามหลักพระไตรปิฎกอรรถกถาอย่างถูกต้องและสุภาพ
            ⚠️ ห้ามตอบเรื่องที่ไม่เกี่ยวข้องกับพระพุทธศาสนาเด็ดขาด
            ข้อความจากผู้ใช้: {user_input}
            """
            try:
                response = model.generate_content(buddha_prompt)
                st.info("ผลการประมวลผล:")
                st.write(response.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")

# ส่วนท้ายแสดงผู้จัดทำ (Footer)
st.markdown("""
    <div class="footer">
        <p><b>ผู้จัดทำ:</b> วิศวกรณ์ พระบัวบาน</p>
        <p>สร้าง <b>Pali AI</b> เป็นพุทธบูชาแด่พระสัมมาพุทธเจ้า</p>
        <p style="font-style: italic; color: #999;">"ธรรมะที่รักษาไว้อย่างถูกต้อง คือรากแก้วของพระศาสนา"</p>
    </div>
""", unsafe_allow_html=True)
