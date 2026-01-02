import streamlit as st
import json
import tempfile
import os
from openai import OpenAI
import PyPDF2  # 用于PDF读取，确保已安装

# -------------------- 页面初始化 --------------------
st.set_page_config(
    page_title="iLogos Open - 古典语言研究平台",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- 自定义CSS样式（匹配iLogos风格） --------------------
st.markdown("""
<style>
    /* 主色调：深蓝+金色，体现古典学术感 */
    .main-header {
        color: #1E3A8A;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 0.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2E4A9A;
    }
    .chat-user {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .chat-assistant {
        background-color: #FFF8E1;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- 侧边栏（配置区） --------------------
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🏛️ iLogos Open</h2>", unsafe_allow_html=True)
    st.markdown("### 🔐 配置")
    
    # API 密钥输入
    api_key = st.text_input(
        "DeepSeek API 密钥",
        type="password",
        help="从 platform.deepseek.com 获取",
        value=st.session_state.get("api_key", "")
    )
    if api_key:
        st.session_state["api_key"] = api_key
        st.success("✅ API 密钥已设置")
    
    st.markdown("---")
    st.markdown("### 📁 文档上传")
    
    # 文件上传器（支持多格式）
    uploaded_file = st.file_uploader(
        "上传古典语文档",
        type=['pdf', 'txt', 'docx'],
        help="支持 PDF、TXT、DOCX 格式"
    )
    
    # 成本监控
    st.markdown("---")
    st.markdown("### 📊 成本监控")
    if "total_cost" not in st.session_state:
        st.session_state.total_cost = 0.0
    st.metric("累计估算费用", f"{st.session_state.total_cost:.4f} 元")
    
    # 清空对话按钮
    if st.button("🗑️ 清空对话历史"):
        st.session_state.messages = []
        st.session_state.total_cost = 0.0
        st.rerun()
    
    st.markdown("---")
    st.markdown("**iLogos Open 开放语言项目** · 为了人工智能时代的古典学术")

# -------------------- 主页面标题 --------------------
st.markdown('<h1 class="main-header">🏛️ iLogos Open 古典语言研究平台</h1>', unsafe_allow_html=True)
st.markdown("**iLatin 语料库 · iLexicon 词典编纂 · 深度AI分析**")
st.markdown("---")

# -------------------- 核心函数定义 --------------------
def init_openai_client():
    """初始化 OpenAI 客户端"""
    if "api_key" not in st.session_state or not st.session_state.api_key:
        st.error("⚠️ 请在侧边栏输入有效的 API 密钥")
        return None
    return OpenAI(api_key=st.session_state.api_key, base_url="https://api.deepseek.com")

def read_uploaded_file(uploaded_file):
    """读取上传的文件内容"""
    content = ""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                content += page.extract_text()
            st.sidebar.success(f"✅ 已读取 PDF，共 {len(pdf_reader.pages)} 页")
        else:
            content = uploaded_file.read().decode("utf-8")
            st.sidebar.success(f"✅ 已读取文本，{len(content)} 字符")
        return content
    except Exception as e:
        st.sidebar.error(f"❌ 文件读取失败: {e}")
        return None

def estimate_cost(usage):
    """估算成本并更新状态"""
    if usage:
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        cost = (input_tokens * 0.2 + output_tokens * 3) / 1_000_000  # 使用 V3.2-Exp 价格
        st.session_state.total_cost += cost
        return cost
    return 0.0

# -------------------- 会话状态初始化 --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "您好，我是**爱言**，iLogos Open 项目的首席研究助理。我可以帮助您分析古典拉丁语/希腊语文献、编纂词典，或进行任何相关的学术探讨。请开始在下方输入，或从侧边栏上传文档。"}
    ]

# -------------------- 主聊天界面 --------------------
# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- 文档处理区域 --------------------
if uploaded_file is not None:
    with st.expander("📄 已上传文档分析选项", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            analysis_type = st.selectbox(
                "选择分析类型",
                ["语法结构分析", "词汇提取与统计", "文体风格分析", "全文摘要"]
            )
        with col2:
            doc_action = st.radio(
                "执行操作",
                ["仅预览内容", "发送给AI分析"]
            )
        
        # 预览内容
        if doc_action == "仅预览内容":
            file_content = read_uploaded_file(uploaded_file)
            if file_content:
                with st.container(height=200):
                    st.text(file_content[:1500] + ("..." if len(file_content) > 1500 else ""))
        
        # 发送分析
        if st.button("🚀 发送给爱言分析", type="primary") and doc_action == "发送给AI分析":
            file_content = read_uploaded_file(uploaded_file)
            if file_content:
                user_message = f"请分析以下{uploaded_file.type}文档（分析要求：{analysis_type}）：\n\n{file_content[:6000]}"
                st.session_state.messages.append({"role": "user", "content": f"[文档分析请求：{analysis_type}]"})
                st.session_state.messages.append({"role": "user", "content": user_message})
                st.rerun()

# -------------------- 聊天输入区域 --------------------
if prompt := st.chat_input("💬 输入您的问题，或使用‘爱言’呼唤助手..."):
    # 处理唤醒词
    assistant_name = "爱言"
    if prompt.startswith(assistant_name):
        prompt = prompt[len(assistant_name):].strip()
        st.toast(f"🧠 已唤醒助手「{assistant_name}」")
    
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 调用AI
    client = init_openai_client()
    if client:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # 调用DeepSeek API
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": m["role"], "content": m["content"]} 
                             for m in st.session_state.messages],
                    stream=True  # 启用流式输出
                )
                
                # 流式显示回复
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # 更新消息历史
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # 估算成本（简化版，实际需从response获取usage）
                # 此处为演示，实际需根据API返回的usage对象计算
                
            except Exception as e:
                st.error(f"❌ API调用失败: {e}")

# -------------------- 页脚 --------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**核心功能**")
    st.markdown("- 智能文档分析")
    st.markdown("- 无限对话上下文")
    st.markdown("- 实时成本监控")
with col2:
    st.markdown("**技术栈**")
    st.markdown("- DeepSeek-V3.2-Exp")
    st.markdown("- Streamlit")
    st.markdown("- Python 3.9+")
with col3:
    st.markdown("**项目链接**")
    st.markdown("[iLogos Open 官网](http://ilogosopen.org)")
    st.markdown("[项目GitHub](https://github.com)")  # 可替换为你的仓库

st.caption("© 2024 iLogos Open 开放语言项目 · 传承古典 · 启迪未来")
