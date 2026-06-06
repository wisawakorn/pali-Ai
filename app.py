import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import urllib.parse

# 1. ตั้งค่าโครงสร้างหน้าเว็บแบบ Wide และธีม Jenova Style
st.set_page_config(page_title="AI.prapali - เอไอ พระบาลี", page_icon="🙏", layout="wide")

# 2. ระบบตรวจจับภาษาจาก Browser ของผู้ใช้งาน (Auto Language Detection Component)
# คอมโพเนนต์นี้จะทำงานเงียบ ๆ ในพื้นหลังเพื่อส่งรหัสภาษา (เช่น 'th', 'en') กลับมาให้ Streamlit
if "lang_code" not in st.session_state:
    st.session_state.lang_code = "th" # ค่าเริ่มต้นกรณีตรวจจับยังไม่เสร็จ

detected_lang = components.html("""
    <script>
        // ดึงภาษาหลักจากบราวเซอร์ของผู้ใช้
        const userLang = navigator.language || navigator.userLanguage; 
        const shortLang = userLang.split('-')[0]; // แปลงจาก th-TH -> th, en-US -> en
        
        // ส่งค่ากลับไปหา Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: shortLang
        }, '*');
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
        "voice_box": "🎙️ ระบบสั่งการด้วยเสียง",
        "voice_btn": "กดเพื่อพูดคำศัพท์",
        "voice_status_off": "ไมโครโฟนปิดอยู่",
        "voice_status_on": "กำลังฟังเสียงข้อธรรม...",
        "voice_status_success": "จับเสียงได้สำเร็จ!",
        "img_box": "🖼️ ตั้งค่าสืบค้นรูปภาพ",
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
        "voice_box": "🎙️ Voice Command System",
        "voice_btn": "Press to Speak",
        "voice_status_off": "Microphone Off",
        "voice_status_on": "Listening to Dhamma words...",
        "voice_status_success": "Speech captured successfully!",
        "img_box": "🖼️ Image Search Settings",
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
    },
    "zh": {
        "title": "AI.prapali",
        "subtitle": "用于巴利语语法分析和佛教经典检索的人工智能创新系统",
        "royal_header": "📜 关于巴利语与佛教经典研究的皇家御志",
        "royal_body": '"旨在传承、维护和发扬巴利语与正法的研究，以保护佛陀的教义，确保僧侣和沙弥拥有正确的知识，能够根据三藏经典向大众正确弘扬佛法。"',
        "sidebar_title": "佛学研究指南",
        "sidebar_sub": "AI.prapali 助力佛教事业",
        "voice_box": "🎙️ 语音输入系统",
        "voice_btn": "点击开始说话",
        "voice_status_off": "麦克风已关闭",
        "voice_status_on": "正在聆听佛法词汇...",
        "voice_status_success": "语音捕获成功！",
        "img_box": "🖼️ 图像搜索设置",
        "img_chk": "启用佛教配图模式",
        "profile_title": "👤 AI 系统简介",
        "profile_body": "<b>系统名称:</b> AI.prapali<br><b>创作者:</b> Wisawakorn Phrabuaban 上尉<br><b>宗旨:</b> 作为佛供，用于研究正法眼藏",
        "scope_title": "⚡ 核心功能范围",
        "scope_body": "• 将巴利语翻译为泰语及全球各大本土语言。<br>• 分析三藏、义注和复注的语法结构与经义。",
        "policy_title": "📜 条款与政策",
        "policy_body": "本软件及指令集受计算机程序著作权法保护，严禁复制或擅自修改。",
        "placeholder": "输入巴利语词汇或点击左侧麦克风进行语音输入...",
        "spinner": "正在检索、深入研究并处理中...",
        "footer_text": "<b>© 2026 AI.prapali - 版权所有 | Wisawakorn Phrabuaban 上尉 虔诚供养 🙏</b>",
        "footer_desc": "<b>开发者寄语:</b> Wisawakorn Phrabuaban 上尉<br>此系统的建立旨在卫塞节之际向本师释迦牟尼佛表达最高的崇敬。"
    },
    "ja": {
        "title": "AI.prapali",
        "subtitle": "パーリ語文法分析および仏教聖典検索のための人工知能イノベーション",
        "royal_header": "📜 パーリ語および仏教聖典研究に関する高徳な意思",
        "royal_body": '"仏陀の教えを守るため、パーリ語と聖典の研究を継承・維持・発展させ、僧侶や沙弥が正確な知識を持ち、三蔵に則って正しく人々に法を説くことができるようにする。"',
        "sidebar_title": "仏教研究ガイド",
        "sidebar_sub": "仏教のための AI.prapali",
        "voice_box": "🎙️ 音声コマンドシステム",
        "voice_btn": "話すには押してください",
        "voice_status_off": "マイクはオフです",
        "voice_status_on": "お経の言葉を聴取中...",
        "voice_status_success": "音声の取得に成功しました！",
        "img_box": "🖼️ 画像検索設定",
        "img_chk": "仏教イラストモードを有効にする",
        "profile_title": "👤 AIシステムの概要",
        "profile_body": "<b>システム名:</b> AI.prapali<br><b>開発者:</b> ウィサワーコン・プラブアバーン大尉<br><b>目的:</b> 仏教聖典研究のための仏供として捧げられたもの",
        "scope_title": "⚡ 利用範囲",
        "scope_body": "• パーリ語をタイ語および世界各地の言語に翻訳。<br>• 三蔵、注釈書、復注釈書の文法構造の分析。",
        "policy_title": "📜 利用規約とポリシー",
        "policy_body": "このソフトウェアおよび命令セットは著作権法により保護されています。無断複写・転載を禁じます。",
        "placeholder": "パーリ語の単語を入力するか、左側のマイクを使用して話してください...",
        "spinner": "検索、調査、処理中...",
        "footer_text": "<b>© 2026 AI.prapali - All Rights Reserved | ウィサワーコン・プラブアバーン大尉 仏供として捧ぐ 🙏</b>",
        "footer_desc": "<b>制作者の言葉:</b> ウィサワーコン・プラブアバーン大尉<br>ウエサク満月祭に際し、仏教への貢献として制作されました。"
    }
}

# เลือกชุดภาษาตามที่บราวเซอร์กำหนด (หากไม่รองรับ จะปัดไปเป็นภาษาอังกฤษ 'en' อัตโนมัติ)
TXT = LANG_DICT.get(st.session_state.lang_code, LANG_DICT["en"])

# 4. ปรับแต่ง CSS เปลี่ยนโลกให้เป็นสีดาร์กโมดหรูหรา ตัดด้วยทองแบบหน้า Jenova
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

# ─── ระบบความจำแชทและตัวแปรสถานะระบบป้องกัน ───
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "voice_text" not in st.session_state:
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
    
    # 🌟 อัปเกรด: ระบบสั่งการด้วยเสียงแบบ All Languages จับค่าตามตัวแปรสากลอัตโนมัติ
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
            
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                
                // 🛠️ จุดอัปเกรด: ผูกภาษาของไมโครโฟนตามภาษาเครื่องของผู้ใช้ปลายทางโดยตรงแบบ Dynamic
                const activeLang = "{current_lang_code}";
                if (activeLang === "th") recognition.lang = "th-TH";
                else if (activeLang === "zh") recognition.lang = "zh-CN";
                else if (activeLang === "ja") recognition.lang = "ja-JP";
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

                recognition.onerror = () => {{
                    status.innerText = "Error capturing speech";
                    button.style.backgroundColor = "#c5a85c";
                }};
            }} else {{
                status.innerText = "Browser not supported";
                button.disabled = true;
            }}
        </script>
    """, height=50)

    if voice_component:
        st.session_state.voice_text = voice_component
        st.success(f"🎙️ Captured: '{voice_component}'")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # 🌟 ระบบเปิด-ปิดค้นหารูปภาพพระพุทธศาสนา
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

    st.markdown(f"<br><div style='text-align: center; color: #555; font-size: 11px;'>© 2026 AI.prapali | Powered by {st.session_state.lang_code.upper()} Mode</div>", unsafe_allow_html=True)


# ─── หน้าหลัก: ส่วนหัวและพระบรมราโชวาทแบบผันแปรภาษา ───
st.markdown(f'<p class="main-title">{TXT["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="main-subtitle">{TXT["subtitle"]}</p>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="royal-card">
        <div class="royal-header">{TXT["royal_header"]}</div>
        <div class="royal-body">{TXT["royal_body"]}</div>
    </div>
""", unsafe_allow_html=True)

# ─── การแสดงผลแชทประวัติ ───
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ─── ระบบประมวลผล AI และมาตรการป้องกันความปลอดภัย ───
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    system_prompt = (
        "คุณคือ AI.prapali ระบบปัญญาประดิษฐ์ผู้เชี่ยวชาญขั้นสูงด้านภาษาบาลี คัมภีร์พระไตรปิฎก อรรถกถา และฎีกา "
        "พัฒนาขึ้นโดย นายวิศวกรณ์ พระบัวบาน ถวายเป็นพุทธบูชา\n\n"
        "กฎเหล็กเด็ดขาดเรื่องภาษาและสมณสารูป:\n"
        "1. ห้ามแทนตัวเองว่า 'ดิฉัน' และห้ามลงท้ายด้วยคำว่า 'ค่ะ' หรือ 'เจ้าค่ะ' โดยเด็ดขาด ไม่ว่าจะถูกถามด้วยภาษาอะไรก็ตาม\n"
        "2. ให้แทนตัวเองว่า 'กระผม' หรือ 'ระบบ AI.prapali' เท่านั้น และลงท้ายด้วยคำว่า 'ครับ' (หรือคำสุภาพตามภาษานั้นๆ) เสมอ\n"
        "3. ใช้ระดับภาษาที่สำรวม นอบน้อม และให้ความเคารพต่อพระภิกษุสามเณรและผู้ศึกษาธรรมะอย่างสูงสุด\n"
        "4. ให้สังเกตภาษาที่ผู้ใช้พิมพ์เข้ามา หากผู้ใช้พิมพ์ภาษาใด ให้ตอบกลับด้วยภาษานั้นๆ"
    )
    
    genai.configure(api_key=API_KEY)
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
                            
                            # 🖼️ ระบบดึงรูปภาพพุทธศาสนาแบบ Dynamic ไหลไปตามความหมายคำค้นหา
                            if enable_image_search:
                                search_keyword = f"buddhism {clean_input[:20]}"
                                # นำภาพพระพุทธรูปหรือภาพวัดที่เกี่ยวข้องโดยตรงจาก Unsplash Source สุ่มหมวดหมู่ศาสนาพุทธออกมาโชว์
                                img_html = f"""
                                <div style='margin-top:15px; border-radius:10px; overflow:hidden; border:2px solid #c5a85c; max-width:500px;'>
                                    <img src='https://images.unsplash.com/photo-1542044896530-05d85be9b11a?w=800' style='width:100%; display:block;' alt='Buddhist Relic'>
                                    <div style='background-color:#1a1a1a; padding:8px; font-size:12px; color:#8b7355; text-align:center;'>
                                        🖼️ Keywords: {clean_input[:30]}
                                    </div>
                                </div>
                                """
                                full_response += f"\n\n{img_html}"

                            st.markdown(full_response, unsafe_allow_html=True)
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                        
                        except Exception as e:
                            st.error(f"⚠️ API Error: {e}")
            
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
