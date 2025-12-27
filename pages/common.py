"""
如获珠宝·智能视频工坊 - 公共组件
RuHuo Jewelry Video Studio - Common UI Components
"""
#  Copyright © [2024] 程序那些事
#  Modified for 如获珠宝·智能视频工坊

import os
import streamlit as st

from tools.tr_utils import tr

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_custom_css():
    """加载自定义 CSS 样式"""
    css_file = os.path.join(ROOT_DIR, "styles", "custom.css")
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def get_logo_path():
    """获取 Logo 路径"""
    logo_path = os.path.join(ROOT_DIR, "assets", "logo.png")
    if os.path.exists(logo_path):
        return logo_path
    # 兼容旧路径
    old_logo_path = os.path.join(ROOT_DIR, "logo.png")
    if os.path.exists(old_logo_path):
        return old_logo_path
    return None


def render_sidebar_logo():
    """渲染侧边栏 Logo"""
    logo_path = get_logo_path()
    if logo_path:
        st.sidebar.image(logo_path, width=200)
    else:
        st.sidebar.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: #e85e02; margin: 0;">如获珠宝</h2>
                <p style="color: #A0A0A0; font-size: 0.8rem; margin: 0;">智能视频工坊</p>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_theme_toggle():
    """渲染主题切换按钮（预留功能）"""
    # 目前 Streamlit 不支持动态切换主题，此功能预留
    pass


def common_ui():
    """公共 UI 初始化"""
    st.set_page_config(
        page_title="如获珠宝·智能视频工坊",
        page_icon="💎",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'Report a Bug': "https://github.com/ddean2009/MoneyPrinterPlus",
            'About': "如获珠宝·智能视频工坊 - 让每一件珠宝都闪耀在镜头前",
            'Get help': "https://www.flydean.com"
        }
    )
    
    # 加载自定义样式
    load_custom_css()
    
    # 渲染侧边栏 Logo（居中、圆角、更小）
    render_sidebar_logo()
    
    # 隐藏默认导航
    st.sidebar.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # ========== 视频制作分组 ==========
    st.sidebar.markdown(
        '<p class="sidebar-group-title">🎬 视频制作</p>',
        unsafe_allow_html=True
    )
    st.sidebar.page_link("pages/00_script_generator.py", label="拍摄脚本生成")
    st.sidebar.page_link("pages/01_auto_video.py", label="AI 视频生成")
    st.sidebar.page_link("pages/02_mix_video.py", label="批量视频混剪")
    st.sidebar.page_link("pages/02_merge_video.py", label="视频片段合并")
    
    # ========== 视频发布分组 ==========
    st.sidebar.markdown(
        '<p class="sidebar-group-title">📤 视频发布</p>',
        unsafe_allow_html=True
    )
    st.sidebar.page_link("pages/03_auto_publish.py", label="一键发布到平台")
    
    # ========== 系统设置分组 ==========
    st.sidebar.markdown(
        '<p class="sidebar-group-title">⚙️ 系统</p>',
        unsafe_allow_html=True
    )
    st.sidebar.page_link("gui.py", label="系统设置")
    
    # 底部信息
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div class="sidebar-footer">
            如获珠宝 · 专属定制
        </div>
        """,
        unsafe_allow_html=True
    )