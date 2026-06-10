import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ai-prapali", page_icon="🪷")

# --- ข้อมูลระบบที่แถบด้านข้าง (Sidebar) ---
with st.sidebar:
    st.markdown("### 🪷 ข้อมูลระบบ")
    st.caption("**ai-prapali**\nนักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา")
    st.write("---")
    st.markdown("📝 **ลิขสิทธิ์และการจัดทำ**")
    st.info("จัดทำโดย นายวิศวกรณ์ พระบัวบาน\n\nสร้างเพื่อถวายเป็นพุทธบูชา เนื่องในวันวิสาขบูชาโลก")
    st.write("---")
    st.markdown("🤝 **ติดต่อร่วมสนับสนุน**")
    st.markdown("""
    * 📧 **Email:** wissawakorn444@gmail.com
    * 📞 **โทร:** 0644518043
    * 🌐 **Facebook:** [emey.za196](https://www.facebook.com/emey.za196/)
    """)

# --- ส่วนหลักของหน้าเว็บ ---
st.title("ai-prapali 🪷")
st.subheader("ผู้เชี่ยวชาญปัญญาประดิษฐ์ทางพระพุทธศาสนา")
st.write("---")

# 🔑 ใส่ API Key ของคุณตรงนี้ได้เลย (คนใช้งานจะไม่เห็นช่องกรอกแล้ว)
GEMINI_API_KEY = "วาง_API_Key_ของคุณตรงนี้" 

SYSTEM_PROMPT = (
    "คุณคือ 'ai-prapali' นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา "
    "มีหน้าที่ให้ความรู้ ตอบคำถาม และอธิบายหลักธรรมคำสอนทางพระพุทธศาสนา รวมถึงภาษาบาลี "
    "ด้วยความถูกต้อง สุภาพ และใช้ภาษาที่เข้าใจง่ายในเชิงวิชาการ"
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "เจริญพร ผมคือ ai-prapali นักวิชาการปัญญาประดิษฐ์ทางพระพุทธศาสนา มีสิ่งใดให้ร่วมสนทนาหรือให้ข้อมูลเกี่ยวกับหลักธรรมและภาษาบาลีไหมครับ?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("พิมพ์ข้อความคำถามธรรมะหรือบาลีที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        # เชื่อมต่อด้วยคีย์ที่ซ่อนไว้
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-3.1-flash",
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(prompt)
        msg = response.text
        
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
