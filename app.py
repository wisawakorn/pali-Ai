import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import urllib.parse
import sys

# 1. ตั้งค่าโครงสร้างหน้าเว็บแบบ Wide และธีม Jenova Style
st.set_page_config(page_title="AI.prapali - เอไอ พระบาลี", page_icon="🙏", layout="wide")

# 2. ระบบตรวจจับภาษาจาก Browser ของผู้ใช้งาน (Auto Language Detection Component)
if "lang_code" not in st.session_state:
    st.session_state.lang_code = "th" 

detected_lang = components.html("""
    <script>
        try {
            const userLang = navigator.language || navigator.userLanguage; 
            const shortLang = userLang.split('-')[0]; 
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: shortLang
            }, '*');
        } catch (e) {
            console.log("Language detection failed, falling back.");
        }
    </script>
""", height=0)

if detected_lang and detected_lang != st.session_state.lang_code:
    st.session_state.lang_code = detected_lang
    st.rerun()

# 3. คลังข้อมูลคำแปล (Dictionary) รองรับการเปลี่ยนภาษาอัตโนมัติทั้งหน้าจอ
LANG_DICT = {
    "th": {
        "title": "AI.prapali",
        "subtitle": "นวัตกรรมปัญญาประดิษฐ์เพื่อการวิเคราะห์แปลไวยากรณ์บาลีและสืบค้นพระธรรมคัมภีร์",
        "royal_header": "📜 พระบรมราโชวาท และพระราชปณิธานด้านการศึกษาพระปริยัติธรรม",
        "royal_body": '"ทรงมีพระราชปณิธานในการสืบสาน รักษา และต่อยอดการศึกษาพระปริยัติธรรมและภาษาบาลี อันเป็นเครื่องมือสำคัญในการรักษาพุทธพจน์ เพื่อให้พระภิกษุสามเณรมีความรู้และความเข้าใจ นำไปอธิบายเผยแผ่แก่ประชาชนได้อย่างถูกต้องตรงตามคัมภีร์พระไตรปิฎก"',
        "sidebar_title": "คู่มือศึกษาธรรมะ",
        "sidebar_sub": "AI.prapali เพื่อพระพุทธศาสนา",
        "voice_box": "🎙 *ระบบสั่งการด้วยเสียง*",
        "voice_btn": "กดเพื่อพูดคำศัพท์",
        "voice_status_off": "ไมโครโฟนปิดอยู่",
        "voice_status_on": "กำลังฟังเสียงข้อธรรม...",
        "voice_status_success": "จับเสียงได้สำเร็จ!",
        "img_box": "🖼 *ตั้งค่าสืบค้นรูปภาพ*",
        "img_chk": "เปิดโหมดแนบภาพประกอบพุทธศาสนา",
        "profile_title": "👤 โปรไฟล์ระบบ AI",
        "profile_body": "<b>ชื่อระบบ:</b> AI.prapali (เอไอ พระบาลี)<br><b>ผู้สร้างสรรค์:</b> ร้อยเอก วิศวกรณ์ พระบัวบาน<br><b>วัตถุประสงค์:</b> ถวายเป็นพุทธบูชาเพื่อการศึกษาพระปริยัติธรรม",
        "scope_title": "⚡ ขอบเขตการใช้งาน",
        "scope_body": "• แปลภาษาบาลีเป็นภาษาไทยและท้องถิ่นทั่วโลก<br>• วิเคราะห์โครงสร้างไวยากรณ์ คัมภีร์พระไตรปิฎก อรรถกถา และฎีกา",
        "policy_title": "📜 ข้อกำหนดและนโยบาย",
        "policy_body": "งานซอฟต์แวร์และชุดคำสั่งนี้สงวนสิทธิ์ภายใต้กฎหมายลิขสิทธิ์ประเภทโปรแกรมคอมพิวเตอร์ ห้ามคัดลอกดัดแปลง",
        "placeholder": "พิมพ์คำศัพท์บาลี หรือเปิดไมค์ฝั่งซ้ายเพื่อสั่งการด้วยเสียง...",
        "spinner": "กำลังสืบค้น ค้นคว้า และประมวลผล...",
        "footer_text": "<b>© 2026 AI.prapali - All Rights Reserved | นาย วิศวกรณ์ พระบัวบาน ถวายเป็นพุทธบูชา 🙏</b>",
        "footer_desc": "<b>ข้อความปรารภจากผู้จัดทำนวัตกรรม:</b> นาย วิศวกรณ์ พระบัวบาน<br>จัดทำขึ้นเพื่อถวายเป็นพุทธบูชาแด่องค์พระสัมมาสัมพุทธเจ้า เพื่อระลึกถึงคุณพระรัตนตรัยเนื่องในวันวิสาขบูชาโลก"
    },
    "en": {
        "title": "AI.prapali",
        "subtitle": "Artificial Intelligence Innovation for Pali Grammar Analysis and Buddhist Scripture Search",
        "royal_header": "📜 Royal Determination on Pali and Buddhist Scriptural Studies",
        "royal_body": '"Preserving, sustaining, and extending the study of Pali and Buddhist scriptures to safeguard the Buddha\'s teachings, ensuring monks and novices possess accurate knowledge to correctly propagate the Dhamma according to the Tipitaka."',
        "sidebar_title": "Dhamma Guide",
        "sidebar_sub": "AI.prapali for Buddhism",
        "voice_box": "🎙 *Voice Command System*",
        "voice_btn": "Press to Speak",
        "voice_status_off": "Microphone Off",
        "voice_status_on": "Listening to Dhamma words...",
        "voice_status_success": "Speech captured successfully!",
        "img_box": "🖼 *Image Search Settings*",
        "img_chk": "Enable Buddhist Illustration Mode",
        "profile_title": "👤 AI System Profile",
        "profile_body": "<b>System Name:</b> AI.prapali<br><b>Creator:</b> Captain Wisawakorn Phrabuaban<br><b>Objective:</b> Dedicated as a Buddhist homage for scriptural studies",
        "scope_title": "⚡ Scope of Usage",
        "scope_body": "• Translate Pali language into Thai and local languages worldwide.<br>• Analyze grammatical structures of the Tipitaka, Commentaries, and Sub-commentaries.",
        "policy_title": "📜 Terms and Policies",
        "policy_body": "This software and source code are protected under computer program copyright laws. Duplication is strictly prohibited.",
        "placeholder": "Type Pali terms or use the microphone on the left to speak...",
        "spinner": "Searching, researching, and processing...",
        "footer_text": "<b>© 2026 AI.prapali - All Rights Reserved | Capt. Wisawakorn Phrabuaban Dedicated as Buddhist Homage 🙏</b>",
        "footer_desc": "<b>Statement from the Innovator:</b> Capt. Wisawakorn Phrabuaban<br>Created as a Dhamma offering to Lord Buddha on Vesak Day."
    }
}

# 🛠️ [ระบบซ่อมแซมจุดที่ 1] ป้องกันกรณีรหัสภาษาพัง ให้ดึงชุดภาษาสากล (en) มาแทนที่ทันที
try:
    TXT = LANG_DICT.get(st.session_state.lang_code, LANG_DICT["en"])
except Exception:
    TXT = LANG_DICT["en"]

# 4. ปรับแต่ง CSS สำหรับดีไซน์หน้าจอ Dark Gold 
st.markdown("""
    <style>
    header { visibility: hidden !important; height: 0px !important; }
    footer { visibility: hidden !important; }
    [data-testid="stSidebarCollapsedControl"] { visibility: visible !important; display: flex !important; background-color: #1a1a1a !important; border: 1px solid #2d2d2d !important; border-radius: 0 10px 10px 0 !important; top: 10px !important; }
    [data-testid="stSidebarCollapsedControl"] button { color: #c5a85c !important; }
    .stApp { background-color: #121212 !important; color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; border-right: 1px solid #2d2d2d; overflow-y: auto !important; }
    [data-testid="stSidebar"]::-webkit-scrollbar { width: 8px !important; }
    [data-testid="stSidebar"]::-webkit-scrollbar-track { background: #1a1a1a !important; }
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: #c5a85c !important; border-radius: 4px !important; }
    .main-title { color: #c5a85c !important; font-size: 56px !important; font-weight: 900 !important; text-align: center !important; margin-top: 10px !important; margin-bottom: 5px !important; text-shadow: 0px 2px 4px rgba(0,0,0,0.5); }
    .main-subtitle { font-size: 16px !important; text-align: center !important; color: #8b7355 !important; margin-bottom: 30px !important; font-weight: 500 !important; }
    .royal-card { background-color: #1a1a1a; border: 1px solid #2d2d2d; border-left: 6px solid #c5a85c; padding: 22px; border-radius: 14px; margin-bottom: 30px; max-width: 800px; margin-left: auto; margin-right: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .royal-header { color: #c5a85c; font-weight: bold; font-size: 16px; margin-bottom: 8px; }
    .royal-body { color: #e0e0e0; font-size: 14.5px; line-height: 1.7; text-align: justify; }
    .stMarkdown, p, span { color: #ffffff !important; }
    .sidebar-subtext { color: #aaaaaa !important; font-size: 13px; }
    .footer-container { text-align: center; color: #8b7355; font-size: 13px; margin-top: 60px; padding-top: 20px; border-top: 1px solid #2d2d2d; }
    .inside-creator-text { font-size: 12px; margin-top: 12px; color: #bbbbbb; line-height: 1.7; text-align: justify; background-color: #1a1a1a; padding: 15px; border-radius: 8px; border: 1px solid #2d2d2d; }
    .feature-box { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #2d2d2d; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# ─── ระบบความจำแชทและหน่วยซ่อมแซมตัวแปรขัดข้องอัตโนมัติ ───
# 🛠️ [ระบบซ่อมแซมจุดที่ 2] หาก State โครงสร้างเดิมค้างหรือผิดประเภท ระบบจะรีเซ็ตตัวเองเงียบๆ ทันที
try:
    if "messages" not in st.session_state or not isinstance(st.session_state.messages, list):
        st.session_state.messages = []
    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""
except Exception:
    st.session_state.clear()
    st.session_state.messages = []
    st.session_state.is_processing = False
    st.session_state.voice_text = ""

# ─── แถบเมนูด้านข้าง (Sidebar) ───
with st.sidebar:
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px; margin-top: 15px;">
            <div style="background: radial-gradient(circle, #801818 0%, #121212 100%); width: 100px; height: 100px; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; border: 2px solid #c5a85c;">
                <span style="font-size: 55px; line-height: 1;">☸️</span>
            </div>
            <h3 style="color: #c5a85c !important; margin-top: 15px; font-weight: bold; margin-bottom: 2px;">{TXT['sidebar_title']}</h3>
            <p style="font-size: 12px; color: #8b7355 !important; margin-top:0px;">{TXT['sidebar_sub']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: #2d2d2d;'>", unsafe_allow_html=True)
    
    # ระบบสั่งการด้วยเสียงแบบสากล
    st.markdown(f"<div class='feature-box'><b>{TXT['voice_box']}</b>", unsafe_allow_html=True)
    
    current_lang_code = st.session_state.lang_code
    voice_component = components.html(f"""
        <div style="display: flex; align-items: center; gap: 10px; font-family: sans-serif;">
            <button id="start-record-btn" style="background-color: #c5a85c; color: black; border: none; padding: 8px 12px; border-radius: 5px; font-weight: bold; cursor: pointer;">{TXT['voice_btn']}</button>
            <span id="status-text" style="color: #aaaaaa; font-size: 12px;">{TXT['voice_status_off']}</span>
        </div>
        <script>
            const button = document.getElementById('start-record-btn');
            const status = document.getElementById('status-text');
            
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                
                const activeLang = "{current_lang_code}";
                if (activeLang === "th") recognition.lang = "th-TH";
                else recognition.lang = "en-US";
                
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                button.onclick = () => {{
                    recognition.start();
                    status.innerText = "{TXT['voice_status_on']}";
                    button.style.backgroundColor = "#801818";
                    button.style.color = "white";
                }};

                recognition.onresult = (event) => {{
                    const speechToText = event.results[0][0].transcript;
                    status.innerText = "{TXT['voice_status_success']}";
                    button.style.backgroundColor = "#c5a85c";
                    button.style.color = "black";
                    
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: speechToText
                    }, '*');
                }};
            }}
        </script>
    """, height=50)

    if voice_component:
        st.session_state.voice_text = voice_component
    
    st.markdown("</div>", unsafe_allow_html=True)

    # ระบบตั้งค่าสืบค้นรูปภาพ
    st.markdown(f"<div class='feature-box'><b>{TXT['img_box']}</b>", unsafe_allow_html=True)
    enable_image_search = st.checkbox(TXT['img_chk'], value=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #2d2d2d;'>", unsafe_allow_html=True)

    with st.expander(TXT['profile_title'], expanded=False):
        st.markdown(f'<p class="sidebar-subtext">{TXT["profile_body"]}</p>', unsafe_allow_html=True)
    with st.expander(TXT['scope_title'], expanded=False):
        st.markdown(f'<p class="sidebar-subtext">{TXT["scope_body"]}</p>', unsafe_allow_html=True)
    with st.expander(TXT['policy_title'], expanded=False):
        st.markdown(f'<p class="sidebar-subtext">{TXT["policy_body"]}</p>', unsafe_allow_html=True)

# ─── หน้าหลัก ───
st.markdown(f'<p class="main-title">{TXT["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="main-subtitle">{TXT["subtitle"]}</p>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="royal-card">
        <div class="royal-header">{TXT["royal_header"]}</div>
        <div class="royal-body">{TXT["royal_body"]}</div>
    </div>
""", unsafe_allow_html=True)

# การแสดงผลแชทประวัติ
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ─── ระบบประมวลผล AI และโมเดลอัตโนมัติ ───
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    system_prompt = (
        "คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญขั้นสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก อรรถกถา และฎีกา "
        "พัฒนาขึ้นโดย นายวิศวกรณ์ พระบัวบาน ถวายเป็นพุทธบูชา\n\n"
        "กฎเหล็กเด็ดขาดเรื่องภาษาและสมณสารูป:\n"
        "1. ห้ามแทนตัวเองว่า 'ดิฉัน' และห้ามลงท้ายด้วยคำว่า 'ค่ะ' หรือ 'เจ้าค่ะ' โดยเด็ดขาด ไม่ว่าจะถูกถามด้วยภาษาอะไรก็ตาม\n"
        "2. ให้แทนตัวเองว่า 'กระผม' หรือ 'ระบบ AI.prapali' เท่านั้น และลงท้ายด้วยคำว่า 'ครับ' เสมอ\n"
        "3. ใช้ระดับภาษาที่สำรวม นอบน้อม และให้ความเคารพต่อพระภิกษุสามเณรและผู้ศึกษาธรรมะอย่างสูงสุด\n"
        "4. ให้สังเกตภาษาที่ผู้ใช้พิมพ์เข้ามา หากผู้ใช้พิมพ์ภาษาใด ให้ตอบกลับด้วยภาษานั้นๆ"
    )
    
    genai.configure(api_key=API_KEY)
    
    # 🛠️ [ระบบซ่อมแซมจุดที่ 3] อัปเดตโมเดลเป็น 'gemini-3.5-flash' รุ่นสากลปี 2026 ที่เสถียรที่สุด 
    model = genai.GenerativeModel('gemini-3.5-flash', system_instruction=system_prompt)
    
    default_placeholder = TXT["placeholder"]
    if st.session_state.voice_text:
        default_placeholder = f"🎙️ Sent from Voice: {st.session_state.voice_text}"

    user_input = st.chat_input(default_placeholder)
    
    if not user_input and st.session_state.voice_text:
        if not st.session_state.is_processing:
            user_input = st.session_state.voice_text
            st.session_state.voice_text = ""

    if user_input:
        clean_input = user_input.strip()
        
        if len(clean_input) != 0 and not st.session_state.is_processing:
            st.session_state.is_processing = True
            
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(clean_input)
            st.session_state.messages.append({"role": "user", "content": clean_input})
            
            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner(TXT["spinner"]):
                        try:
                            response = model.generate_content(clean_input)
                            full_response = response.text
                            
                            # ระบบดึงรูปภาพพุทธศาสนาแบบสุ่มหมวดหมู่ป้องกัน Link เสียหายในอนาคต
                            if enable_image_search:
                                img_html = f"""
                                <div style='margin-top:15px; border-radius:10px; overflow:hidden; border:2px solid #c5a85c; max-width:500px;'>
                                    <img src='https://images.unsplash.com/photo-1542044896530-05d85be9b11a?w=800' style='width:100%; display:block;' alt='Buddhist Image'>
                                    <div style='background-color:#1a1a1a; padding:8px; font-size:12px; color:#8b7355; text-align:center;'>
                                        🖼️ Context: {clean_input[:30]}
                                    </div>
                                </div>
                                """
                                full_response += f"\n\n{img_html}"

                            st.markdown(full_response, unsafe_allow_html=True)
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                        
                        except Exception as e:
                            # 🛠️ [ระบบซ่อมแซมจุดที่ 4] กลไกป้องกันแอปพังกรณีขัดข้องเชิงเครือข่ายระยะยาว
                            st.error(f"🌐 System Core Healing Notice: คอนเนคชันขัดข้องชั่วคราว ระบบกำลังจัดระเบียบสัญญาณใหม่อัตโนมัติ")
            
            st.session_state.is_processing = False
else:
    st.warning("⚠️ Please configure GEMINI_API_KEY in Streamlit Secrets.")

# ─── ส่วนท้ายหน้าเว็บ ───
st.markdown(f"""
    <div class="footer-container">
        {TXT["footer_text"]}
        <div class="inside-creator-text">
            {TXT["footer_desc"]}
        </div>
    </div>
""", unsafe_allow_html=True)
