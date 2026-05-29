import streamlit as st
import google.generativeai as genai

# --- การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="pali-AIระบบวิเคราะห์บาลีไวยากรณ์ AI", page_icon="🙏", layout="centered")

# --- ส่วนจัดการ API Key ปลอดภัย ---

if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("ระบุ Gemini API Key ของคุณ", type="password", help="รับ API Key ฟรีได้ที่ Google AI Studio")

# --- ส่วนหน้าตาเว็บ (UI) ---
st.markdown("<h1 style='text-align: center; color: #b45309;'>ระบบpali-AIวิเคราะห์และแปลบาลีไวยากรณ์</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>เพื่อการศึกษาพระปริยัติธรรมตามพระราชดำริ ถวายเป็นพุทธบูชาเนื่องในวันวิสาขบูชา</p>", unsafe_allow_html=True)
st.divider()

st.subheader("📝 กรอกประโยคหรือศัพท์บาลี")
user_input = st.text_area("พิมพ์ข้อความภาษาบาลีที่ต้องการให้ AI ช่วยตรวจชำระหรือแปล", placeholder="ตัวอย่าง: ปุริโส คามํ คจฺฉติ", height=120)

if st.button("ส่งให้ AI วิเคราะห์ไวยากรณ์", use_container_width=True):
    if not API_KEY:
        st.error("⚠️ ระบบยังไม่ได้ตั้งค่า API Key กรุณาระบุที่แถบด้านข้างก่อนครับ")
    elif user_input:
        with st.spinner('กำลังประมวลผลไวยากรณ์ตามหลักบาลีหลวง...'):
            # สมมติว่านี่คือจุดที่ท่านส่งข้อความไปหา Gemini ในโค้ดเดิม
buddha_prompt = f"""
คุณคือผู้เชี่ยวชาญระดับสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก และพระพุทธศาสนา 
จงวิเคราะห์ข้อความที่ผู้ใช้พิมพ์เข้ามา ซึ่งจะมี 2 รูปแบบหลักๆ ดังนี้:

1. หากข้อความที่พิมพ์มาเป็น "ภาษาบาลี": 
   - ให้ทำการแปลยกศัพท์ วิเคราะห์วิภัตติปัจจัย และอธิบายไวยากรณ์ตามหลักหลักสูตรสนามหลวงอย่างละเอียด

2. หากข้อความที่พิมพ์มาเป็น "คำถามธรรมะ/การค้นคว้าพระศาสนา" (ภาษาไทย):
   - ให้สืบค้นและอธิบายหลักธรรม หลักพุทธศาสนา หรือข้อความจากพระไตรปิฎกอรรถกถาอย่างถูกต้อง สุภาพ และชัดเจน

⚠️ ข้อบังคับเด็ดขาด (Security Guard): 
หากผู้ใช้พิมพ์ถามเรื่องทางโลกที่ไม่เกี่ยวข้องกับพระพุทธศาสนา พระธรรม พระสงฆ์ คัมภีร์ หรือภาษาบาลีเลย (เช่น ข่าวบันเทิง, การเมือง, หวย, ชวนคุยทั่วไป) 
ให้ปฏิเสธอย่างสุภาพทันทีว่า: "ระบบบาลี AI รองรับเฉพาะการวิเคราะห์ภาษาบาลีและการสืบค้นข้อมูลที่เกี่ยวเนื่องกับพระพุทธศาสนาเพื่อการศึกษาเท่านั้น"

ข้อความจากผู้ใช้: {user_input}
"""
            try:
                genai.configure(api_key=API_KEY)
                # ปรับเป็นรุ่นล่าสุดที่โควต้าเยอะและประมวลผลเร็ว
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                
                st.success("วิเคราะห์และแปลเสร็จสิ้น!")
                st.markdown("### 📜 ผลการตรวจชำระและวิเคราะห์ไวยากรณ์")
                st.info(response.text)
                
                # ข้อความที่จะใส่ในไฟล์ ดาวน์โหลดขยับหัวข้อให้เว้นบรรทัดสวยงามขึ้น
                download_text = f"ผลการวิเคราะห์บาลีไวยากรณ์ด้วย AI\n"
                download_text += f"โจทย์ที่ตั้ง: {user_input}\n"
                download_text += f"=========================================\n\n"
                download_text += response.text

                # ปุ่มดาวน์โหลดที่แปลงเป็นไฟล์รูปแบบ Word (.doc) ให้เปิดในโปรแกรม Word ได้ทันที
                st.download_button(
                    label="📥 ดาวน์โหลดผลการแปลเก็บไว้ (ไฟล์ Word .doc)",
                    data=download_text,
                    file_name=f"pali_analysis.doc",
                    mime="application/msword"
                )
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ AI: {e}")
    else:
        st.warning("กรุณากรอกข้อความบาลีก่อนกดปุ่มครับ")

st.divider()
st.caption("จัดทำเพื่อถวายเป็นพุทธบูชาและส่งเสริมการศึกษาพระบาลี | วิศวกรณ์ พระบัวบาน พัฒนาด้วย Streamlit และ Gemini AI")
