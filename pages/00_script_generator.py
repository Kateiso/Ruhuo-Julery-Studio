"""
如获珠宝·智能视频工坊 - 拍摄脚本生成器
RuHuo Jewelry Video Studio - Script Generator
支持多轮对话优化脚本
"""
#  Copyright © [2024] 程序那些事
#  Modified for 如获珠宝·智能视频工坊

import os
import streamlit as st

from config.config import my_config, delete_first_visit_session_state, load_session_state_from_yaml, save_session_state_to_yaml
from pages.common import common_ui
from tools.tr_utils import tr

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 初始化页面
delete_first_visit_session_state("00_first_visit")
load_session_state_from_yaml("00_first_visit")
common_ui()

# 珠宝类型选项
JEWELRY_TYPES = [
    "项链", "戒指", "耳环", "手镯", "手链", 
    "吊坠", "胸针", "套装", "其他"
]

# 风格定位选项
STYLE_OPTIONS = [
    "轻奢优雅", "经典复古", "时尚前卫", 
    "简约现代", "浪漫甜美", "商务大气"
]

# 目标平台选项
PLATFORM_OPTIONS = {
    "douyin": "抖音",
    "xiaohongshu": "小红书",
    "kuaishou": "快手",
    "shipinhao": "视频号"
}

# 视频时长选项
DURATION_OPTIONS = [15, 30, 45, 60]

# 系统提示词
SYSTEM_PROMPT = """你是一位专业的珠宝短视频拍摄顾问和脚本编剧。

你的能力：
- 精通珠宝产品的视觉呈现技巧
- 了解各短视频平台的内容调性
- 擅长撰写高端优雅的珠宝文案
- 熟悉珠宝拍摄的灯光、角度、构图

对话规则：
- 生成脚本时提供完整的分镜表、口播文案、配乐建议
- 用户要求修改时，只输出修改后的内容
- 保持专业友好的语气"""


def build_initial_prompt(jewelry_name, jewelry_type, style, platforms, duration):
    """构建初始生成脚本的 Prompt"""
    platforms_str = "、".join(platforms)
    
    return f"""请为以下珠宝产品生成专业拍摄脚本：

## 产品信息
- 珠宝名称：{jewelry_name}
- 珠宝类型：{jewelry_type}
- 风格定位：{style}
- 目标平台：{platforms_str}
- 视频时长：{duration}秒

## 请生成：

### 1. 分镜脚本表
| 时间段 | 镜头画面 | 拍摄角度 | 口播文案 | 字幕/贴纸 |

### 2. 完整口播稿
整合所有口播，标注字数和朗读时长

### 3. 配乐建议

### 4. 拍摄小贴士"""


def chat_stream_response(messages):
    """流式对话响应"""
    from services.llm.tongyi_service import MyTongyiService
    
    try:
        service = MyTongyiService()
        for chunk in service.chat_stream(messages):
            yield chunk
    except Exception as e:
        yield f"\n\n❌ 生成失败：{str(e)}"


def init_chat():
    """初始化对话状态"""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    if "custom_system_prompt" not in st.session_state:
        st.session_state.custom_system_prompt = SYSTEM_PROMPT


def clear_chat():
    """清空对话"""
    st.session_state.chat_messages = []
    st.session_state.chat_started = False
    st.session_state.pop('generated_script', None)


def get_system_prompt():
    """获取当前系统提示词"""
    return st.session_state.get("custom_system_prompt", SYSTEM_PROMPT)


# 初始化
init_chat()

# 页面标题
st.markdown(
    """
    <h1 style='text-align: center; color: #F37021; font-weight: bold;'>
        📝 拍摄脚本生成器
    </h1>
    <p style='text-align: center; color: #A0A0A0;'>
        AI 生成专业脚本，支持多轮对话优化
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ========== 未开始对话：显示输入表单 ==========
if not st.session_state.chat_started:
    col1, col2 = st.columns(2)
    
    with col1:
        jewelry_name = st.text_input(
            "💎 珠宝名称",
            placeholder="例如：18K金钻石项链",
            key="jewelry_name"
        )
        jewelry_type = st.selectbox("📦 珠宝类型", options=JEWELRY_TYPES, key="jewelry_type")
        style = st.selectbox("🎨 风格定位", options=STYLE_OPTIONS, key="style")
    
    with col2:
        selected_platforms = st.multiselect(
            "📱 目标平台",
            options=list(PLATFORM_OPTIONS.values()),
            default=["抖音", "小红书"],
            key="platforms"
        )
        duration = st.selectbox("⏱️ 视频时长（秒）", options=DURATION_OPTIONS, index=1, key="duration")
    
    # 系统提示词设置
    with st.expander("⚙️ 高级设置：自定义 AI 角色", expanded=False):
        new_prompt = st.text_area(
            "系统提示词",
            value=st.session_state.custom_system_prompt,
            height=200,
            help="定义 AI 的角色和行为规则",
            key="system_prompt_input"
        )
        st.session_state.custom_system_prompt = new_prompt
        
        if st.button("🔄 恢复默认"):
            st.session_state.custom_system_prompt = SYSTEM_PROMPT
            st.rerun()
    
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("✨ 生成拍摄脚本", use_container_width=True, type="primary"):
            if not jewelry_name:
                st.error("⚠️ 请输入珠宝名称")
            elif not selected_platforms:
                st.error("⚠️ 请至少选择一个目标平台")
            else:
                # 保存产品信息
                st.session_state.product_info = {
                    "name": jewelry_name,
                    "type": jewelry_type,
                    "style": style,
                    "platforms": selected_platforms,
                    "duration": duration
                }
                # 初始化对话
                st.session_state.chat_messages = [
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": build_initial_prompt(
                        jewelry_name, jewelry_type, style, selected_platforms, duration
                    )}
                ]
                st.session_state.chat_started = True
                st.rerun()

# ========== 已开始对话：显示聊天界面 ==========
else:
    # 产品信息摘要
    info = st.session_state.get("product_info", {})
    st.markdown(
        f"""<div style='background: #2A2420; padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 1rem; font-size: 0.9rem;'>
        <strong>{info.get('name', '')}</strong> | {info.get('type', '')} | {info.get('style', '')} | {info.get('duration', '')}秒
        </div>""",
        unsafe_allow_html=True
    )
    
    # 操作按钮
    if st.button("🔄 重新开始"):
        clear_chat()
        st.rerun()
    
    st.markdown("---")
    
    # 显示对话历史
    for msg in st.session_state.chat_messages:
        if msg["role"] == "system":
            continue
        with st.chat_message("user" if msg["role"] == "user" else "assistant", 
                            avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])
    
    # 生成助手回复
    if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "user":
        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()
            full_response = ""
            
            for chunk in chat_stream_response(st.session_state.chat_messages):
                full_response += chunk
                placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            
            # 保存回复
            st.session_state.chat_messages.append({"role": "assistant", "content": full_response})
            st.session_state.generated_script = full_response
    
    # 用户输入
    user_input = st.chat_input("继续对话优化脚本，如：修改第3个镜头的口播...")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        st.rerun()

# 保存状态
save_session_state_to_yaml()

# 底部提示
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.85rem;'>"
    "💡 生成后可继续对话让 AI 帮您修改优化"
    "</div>",
    unsafe_allow_html=True
)
