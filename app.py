import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="บาลี AI", page_icon="🙏", layout="wide")

st.markdown("""
    <style>
    .title { color: #8B5A2B; font-size: 40px; font-weight: bold; text-align: center; }
    .subtitle { font-size: 18px; text-align: center; color: #555555; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">ระบบวิเคราะห์และแปลบาลีไวยากรณ์</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">เพื่อการศึกษาพระปริยัติธรรม ถวายเป็นพุทธบูชาเนื่องในวันวิสาขบูชา</p>', unsafe_allow_html=True)
st.write("---")

# ดึงรหัส API Key จากระบบ Secrets
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("กรุณาตั้งค่า GEMINI_API_KEY ในระบบ Secrets ของ Streamlit ก่อนใช้งาน")
else:
    genai.configure(api_key=API_KEY)
    # แก้ไขชื่อโมเดลเป็นรุ่นล่าสุดที่รองรับ
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
