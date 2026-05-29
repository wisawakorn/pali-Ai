import streamlit as plt
import google.generativeai as genai

# ตั้งค่าหน้าเว็บให้สวยงาม
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

# ดึงรหัส API Key จากระบบ Secrets ของ Streamlit
API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("กรุณาตั้งค่า GEMINI_API_KEY ในระบบ Secrets ของ Streamlit ก่อนใช้งาน")
else:
    # เริ่มต้นตั้งค่าโมเดล AI
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # ช่องรับข้อมูลหลัก (ช่องเดียวสารพัดประโยชน์)
    st.write("### 📝 กรอกประโยคหรือคำศัพท์ที่ต้องการสืบค้น")
    user_input = st.text_input("พิมพ์ข้อความภาษาบาลีที่ต้องการให้แปล หรือพิมพ์ข้อความภาษาไทยเพื่อค้นคว้าธรรมะ", placeholder="ตัวอย่าง: ปุริโส คามํ คจฺฉติ หรือ อริยสัจ 4 คืออะไร")

    if user_input:
        with st.spinner("กำลังประมวลผลสืบค้นจากคัมภีร์และหลักธรรม..."):
            buddha_prompt = f"""
            คุณคือผู้เชี่ยวชาญระดับสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก และพระพุทธศาสนา 
            จงวิเคราะห์ข้อความที่ผู้ใช้พิมพ์เข้ามา ซึ่งจะมี 2 รูปแบบหลักๆ ดังนี้:

            1. หากข้อความที่พิมพ์มาเป็น "ภาษาบาลี": 
               - ให้ทำการแปลยกศัพท์ วิเคราะห์วิภัตติปัจจัย และอธิบายไวยากรณ์ตามหลักสูตรสนามหลวงอย่างละเอียด

            2. หากข้อความที่พิมพ์มาเป็น "คำถามธรรมะ/การค้นคว้าพระศาสนา" (ภาษาไทย):
               - ให้สืบค้นและอธิบายหลักธรรม หลักพุทธศาสนา หรือข้อความจากพระไตรปิฎกอรรถกถาอย่างถูกต้อง สุภาพ และชัดเจน

            ⚠️ ข้อบังคับเด็ดขาด (Security Guard): 
            หากผู้ใช้พิมพ์ถามเรื่องทางโลกที่ไม่เกี่ยวข้องกับพระพุทธศาสนา พระธรรม พระสงฆ์ คัมภีร์ หรือภาษาบาลีเลย (เช่น ข่าวบันเทิง, การเมือง, หวย, ชวนคุยทั่วไป) 
            ให้ปฏิเสธอย่างสุภาพทันทีว่า: "ระบบบาลี AI รองรับเฉพาะการวิเคราะห์ภาษาบาลีและการสืบค้นข้อมูลที่เกี่ยวเนื่องกับพระพุทธศาสนาเพื่อการศึกษาเท่านั้น"

            ข้อความจากผู้ใช้: {user_input}
            """
            
            try:
                response = model.generate_content(buddha_prompt)
                st.info("ผลการประมวลผล:")
                st.write(response.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อโมเดล: {str(e)}")
