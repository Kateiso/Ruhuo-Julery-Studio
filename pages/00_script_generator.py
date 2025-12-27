"""
如获珠宝·智能视频工坊 - 拍摄脚本生成器
RuHuo Jewelry Video Studio - Script Generator
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


def load_prompt_template():
    """加载 Prompt 模板"""
    prompt_file = os.path.join(ROOT_DIR, "prompts", "jewelry_script.txt")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read()
    return None


def generate_script(jewelry_name, jewelry_type, style, platforms, duration):
    """调用 LLM 生成拍摄脚本"""
    from langchain_core.prompts import PromptTemplate
    from services.llm.tongyi_service import MyTongyiService
    
    # 构建 Prompt
    platforms_str = "、".join(platforms)
    
    prompt_text = f"""你是一位专业的珠宝短视频拍摄顾问和脚本编剧。请根据以下珠宝信息，生成一份专业的拍摄脚本。

## 输入信息
- 珠宝名称：{jewelry_name}
- 珠宝类型：{jewelry_type}
- 风格定位：{style}
- 目标平台：{platforms_str}
- 视频时长：{duration}秒

## 输出要求

请生成以下内容：

### 1. 拍摄脚本（分镜头描述）
按照时间顺序，详细描述每个镜头：
- 镜头编号和时间范围
- 画面内容描述
- 拍摄角度建议
- 灯光建议

### 2. 文案脚本
为视频生成适合短视频平台的配音文案，要求：
- 语言优雅、有质感
- 突出珠宝的独特卖点
- 符合{style}的调性
- 使用"璀璨"、"永恒"、"匠心"、"臻选"等高端词汇
- 避免使用"便宜"、"打折"、"低价"等词汇

### 3. 配乐建议
推荐适合的背景音乐风格

### 4. 拍摄小贴士
给出2-3条实用的拍摄建议

## 输出格式
请使用清晰的markdown格式输出，便于阅读和复制。

{{topic}}
"""
    
    try:
        # 创建 PromptTemplate
        prompt_template = PromptTemplate(
            input_variables=["topic"],
            template=prompt_text
        )
        
        # 调用通义千问生成脚本
        tongyi_service = MyTongyiService()
        result = tongyi_service.generate_content(
            topic="请开始生成",
            prompt_template=prompt_template
        )
        return result
    except Exception as e:
        return f"❌ 生成失败：{str(e)}\n\n请检查：\n1. 是否已配置通义千问 API Key\n2. 网络连接是否正常"


# 页面标题
st.markdown(
    """
    <h1 style='text-align: center; color: #e85e02; font-weight: bold;'>
        📝 拍摄脚本生成器
    </h1>
    <p style='text-align: center; color: #A0A0A0;'>
        输入珠宝信息，AI 为您生成专业的拍摄脚本
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 输入区域
col1, col2 = st.columns(2)

with col1:
    jewelry_name = st.text_input(
        "💎 珠宝名称",
        placeholder="例如：18K金钻石项链",
        key="jewelry_name"
    )
    
    jewelry_type = st.selectbox(
        "📦 珠宝类型",
        options=JEWELRY_TYPES,
        key="jewelry_type"
    )
    
    style = st.selectbox(
        "🎨 风格定位",
        options=STYLE_OPTIONS,
        key="style"
    )

with col2:
    selected_platforms = st.multiselect(
        "📱 目标平台",
        options=list(PLATFORM_OPTIONS.values()),
        default=["抖音", "小红书"],
        key="platforms"
    )
    
    duration = st.selectbox(
        "⏱️ 视频时长（秒）",
        options=DURATION_OPTIONS,
        index=1,  # 默认 30 秒
        key="duration"
    )

st.markdown("---")

# 生成按钮
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    generate_btn = st.button(
        "✨ 生成拍摄脚本",
        use_container_width=True,
        type="primary"
    )

# 结果区域
if generate_btn:
    if not jewelry_name:
        st.error("⚠️ 请输入珠宝名称")
    elif not selected_platforms:
        st.error("⚠️ 请至少选择一个目标平台")
    else:
        with st.spinner("🔮 AI 正在为您生成拍摄脚本..."):
            result = generate_script(
                jewelry_name=jewelry_name,
                jewelry_type=jewelry_type,
                style=style,
                platforms=selected_platforms,
                duration=duration
            )
        
        st.markdown("---")
        st.markdown("### 📜 生成结果")
        
        # 显示结果
        st.markdown(result)
        
        # 操作按钮
        col_action1, col_action2, col_action3 = st.columns([1, 1, 1])
        
        with col_action1:
            # 复制按钮（使用 Streamlit 的下载功能模拟）
            st.download_button(
                label="📋 下载脚本",
                data=result,
                file_name=f"{jewelry_name}_拍摄脚本.md",
                mime="text/markdown"
            )
        
        with col_action2:
            if st.button("➡️ 开始制作视频", type="secondary"):
                # 保存脚本到 session_state 供视频生成页面使用
                st.session_state['generated_script'] = result
                st.session_state['script_jewelry_name'] = jewelry_name
                st.switch_page("pages/01_auto_video.py")

# 保存会话状态
save_session_state_to_yaml()

# 底部提示
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.85rem;'>
        💡 提示：生成的脚本可以作为拍摄参考，您可以根据实际情况进行调整
    </div>
    """,
    unsafe_allow_html=True
)
