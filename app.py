import streamlit as str
import google.generativeai as genai

st.title("Gemini Chatbot 🤖")

# 1. ใส่ช่องให้กรอก Gemini API Key ใน Sidebar ด้านข้าง
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[รับ API Key ที่นี่](https://aistudio.google.com/)"

# 2. ตรวจสอบสถานะการเชื่อมต่อระบบแชท
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "สวัสดีครับ มีอะไรให้ผมช่วยไหม?"}]

# แสดงประวัติการคุยบนหน้าจอ
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 3. เมื่อผู้ใช้พิมพ์ข้อความส่งมา
if prompt := st.chat_input():
    if not gemini_api_key:
        st.info("กรุณาใส่ Gemini API Key ในช่องด้านซ้ายก่อนเริ่มคุยครับ")
        st.stop()

    # ตั้งค่าและเรียกใช้โมเดล Gemini
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash") # สามารถเปลี่ยนโมเดลตรงนี้ได้
    
    # บันทึกคำถามฝั่งผู้ใช้
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # ส่งข้อความไปหา Gemini และรอคำตอบ
    try:
        response = model.generate_content(prompt)
        msg = response.text
        
        # บันทึกและแสดงคำตอบจากบอท
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
