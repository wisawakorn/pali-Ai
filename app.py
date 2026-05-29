import streamlit as st
import google.generativeai as genai

# --- การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="pali-AIระบบวิเคราะห์บาลีไวยากรณ์ AI", page_icon="🙏", layout="centered")

# --- ส่วนจัดการ API Key ปลอดภัย ---
st.sidebar.header("")
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = st.sidebar.text_input("ระบุ Gemini API Key ของคุณ", type="password", help="รับ API Key ฟรีได้ที่ Google AI Studio")

# --- ส่วนหน้าตาเว็บ (UI) ---
st.markdown("<h1 style='text-align: center; color: #b45309;'>ระบบวิเคราะห์และแปลบาลีไวยากรณ์</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>เพื่อการศึกษาพระปริยัติธรรม ถวายเป็นพุทธบูชาเนื่องในวันวิสาขบูชา</p>", unsafe_allow_html=True)
st.divider()

st.subheader("📝 กรอกประโยคหรือศัพท์บาลี")
user_input = st.text_area("พิมพ์ข้อความภาษาบาลีที่ต้องการให้ AI ช่วยตรวจชำระหรือแปล", placeholder="ตัวอย่าง: ปุริโส คามํ คจฺฉติ", height=120)

if st.button("ส่งให้ AI วิเคราะห์ไวยากรณ์", use_container_width=True):
    if not API_KEY:
        st.error("⚠️ ระบบยังไม่ได้ตั้งค่า API Key กรุณาระบุที่แถบด้านข้างก่อนครับ")
    elif user_input:
        with st.spinner('กำลังประมวลผลไวยากรณ์ตามหลักแม่กองบาลีสนามหลวง...'):
            prompt = f"""
            ในฐานะผู้เชี่ยวชาญด้านบาลีไวยากรณ์ (ธัมมปทัฏฐกถา) 
            จงวิเคราะห์ประโยคหรือศัพท์บาลีต่อไปนี้: "{user_input}"
            โดยให้ข้อมูลดังนี้:
            1. แปลโดยพยัญชนะ (แบบยกศัพท์)
            2. แปลโดยอรรถ (ใจความสำคัญ)
            3. วิเคราะห์ไวยากรณ์ทีละศัพท์ (แยกธาตุ, ปัจจัย, วิภัตติ, ลิงค์, พจน์)
            4. ข้อควรระวังหรือสัมพันธ์ที่น่าสนใจในประโยคนี้
            ตอบเป็นภาษาไทยที่สุภาพและเข้าใจง่ายสำหรับนักเรียนบาลี
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
