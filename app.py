import streamlit as st
import google.generativeai as genai

# 1. 設定網頁標題與圖示
st.set_page_config(page_title="小小辯論家 AI 版", page_icon="🗣️")

st.title("🗣️ 小小辯論家 (AI 教練版)")
st.caption("由 Streamlit 與 Google Gemini 強力驅動")

# 2. 側邊欄：使用者設定
with st.sidebar:
    st.header("📝 設定區")
    user_name = st.text_input("請輸入你的名字", "同學A")
    topic = st.text_input("辯論主題", "小學生是否應擁有手機？")
    
    # 重置按鈕
    if st.button("重新開始討論"):
        st.session_state.messages = []
        st.rerun()

# 3. 初始化聊天記錄 (若不存在則建立空清單)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 顯示歷史訊息
for msg in st.session_state.messages:
    # 根據角色決定顯示樣式 (user=人類, assistant=AI)
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. 處理輸入與 AI 回應
# 當使用者輸入內容並按下 Enter
if prompt := st.chat_input("請輸入你的觀點、證據或反駁..."):
    
    # A. 顯示使用者輸入
    st.session_state.messages.append({"role": "user", "content": f"{user_name}: {prompt}"})
    with st.chat_message("user"):
        st.write(f"{user_name}: {prompt}")

    # B. 呼叫 AI
    try:
        # 設定 API Key (從 Secrets 讀取)
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 修正點：將 'gemini-pro' 改為更新的 'gemini-1.5-flash'
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 組合提示詞 (Prompt Engineering)
        full_prompt = f"""
        你是一個國小辯論社的溫柔教練。
        目前的辯論主題是：「{topic}」。
        學生({user_name})剛說：「{prompt}」。
        
        請依照以下規則回應：
        1. 先肯定學生的發言。
        2. 指出這個論點的類型(觀點/證據/反駁)。
        3. 提出一個引導式問題，鼓勵他想得更深(例如問有無證據、或反過來想)。
        4. 語氣要活潑、友善，字數不要太多(100字以內)。
        """
        
        with st.chat_message("assistant"):
            with st.spinner("AI 教練正在思考中..."):
                response = model.generate_content(full_prompt)
                ai_reply = response.text
                st.write(ai_reply)
        
        # 儲存 AI 回應
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        st.error(f"連線錯誤，請檢查 API Key 設定。錯誤訊息: {e}")
