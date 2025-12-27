"""
如获珠宝·智能视频工坊 - 首页/系统设置
RuHuo Jewelry Video Studio - Home / Settings
"""
#  Copyright © [2024] 程序那些事
#  Modified for 如获珠宝·智能视频工坊

import streamlit as st
from config.config import my_config, save_config, languages, test_config, local_audio_tts_providers, \
    local_audio_recognition_providers, local_audio_recognition_fasterwhisper_module_names, \
    local_audio_recognition_fasterwhisper_device_types, local_audio_recognition_fasterwhisper_compute_types, \
    delete_first_visit_session_state, app_title
from pages.common import common_ui
from tools.tr_utils import tr

delete_first_visit_session_state("all_first_visit")

common_ui()

# ========== 首页欢迎区域 ==========
st.markdown(
    f"""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #e85e02; font-weight: bold; font-size: 2.5rem;'>
            💎 {app_title}
        </h1>
        <p style='color: #A0A0A0; font-size: 1.1rem;'>
            让每一件珠宝都闪耀在镜头前
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ========== 快捷入口卡片 ==========
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style='background: #1A1A1A; border: 1px solid #3D3D3D; border-radius: 12px; padding: 2rem; text-align: center;'>
            <div style='font-size: 3rem;'>📝</div>
            <h3 style='color: #FFFFF0; margin: 1rem 0 0.5rem 0;'>拍摄脚本生成</h3>
            <p style='color: #A0A0A0; font-size: 0.9rem;'>AI 生成专业拍摄脚本</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("开始使用", key="btn_script", use_container_width=True):
        st.switch_page("pages/00_script_generator.py")

with col2:
    st.markdown(
        """
        <div style='background: #1A1A1A; border: 1px solid #3D3D3D; border-radius: 12px; padding: 2rem; text-align: center;'>
            <div style='font-size: 3rem;'>🎬</div>
            <h3 style='color: #FFFFF0; margin: 1rem 0 0.5rem 0;'>AI 视频生成</h3>
            <p style='color: #A0A0A0; font-size: 0.9rem;'>一键生成带配音短视频</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("开始使用", key="btn_video", use_container_width=True):
        st.switch_page("pages/01_auto_video.py")

with col3:
    st.markdown(
        """
        <div style='background: #1A1A1A; border: 1px solid #3D3D3D; border-radius: 12px; padding: 2rem; text-align: center;'>
            <div style='font-size: 3rem;'>📤</div>
            <h3 style='color: #FFFFF0; margin: 1rem 0 0.5rem 0;'>一键发布</h3>
            <p style='color: #A0A0A0; font-size: 0.9rem;'>自动发布到各平台</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("开始使用", key="btn_publish", use_container_width=True):
        st.switch_page("pages/03_auto_publish.py")

# ========== 系统设置区域 ==========
st.markdown("---")
st.markdown(
    """
    <h2 style='text-align: center; color: #e85e02;'>⚙️ 系统设置</h2>
    <p style='text-align: center; color: #A0A0A0;'>配置 AI 服务、语音和资源库</p>
    """,
    unsafe_allow_html=True
)

if 'ui_language' not in st.session_state:
    st.session_state['ui_language'] = 'zh-CN - 简体中文'


def set_ui_language():
    my_config['ui']['language'] = st.session_state['ui_language'].split(" - ")[0].strip()
    save_config()


def save_pexels_api_key():
    my_config['resource']['pexels']['api_key'] = st.session_state['pexels_api_key']
    save_config()


def save_pixabay_api_key():
    my_config['resource']['pixabay']['api_key'] = st.session_state['pixabay_api_key']
    save_config()


def save_stable_diffusion_api_user_name():
    test_config(my_config, "resource", 'stableDiffusion')
    my_config['resource']['stableDiffusion']['user_name'] = st.session_state['stableDiffusion_api_user_name']
    save_config()


def save_stable_diffusion_api_password():
    test_config(my_config, "resource", 'stableDiffusion')
    my_config['resource']['stableDiffusion']['password'] = st.session_state['stableDiffusion_api_password']
    save_config()


def save_stable_diffusion_api_server_address():
    test_config(my_config, "resource", 'stableDiffusion')
    my_config['resource']['stableDiffusion']['server_address'] = st.session_state['stableDiffusion_api_server_address']
    save_config()


def set_llm_provider():
    my_config['llm']['provider'] = st.session_state['llm_provider']
    save_config()


def set_resource_provider():
    my_config['resource']['provider'] = st.session_state['resource_provider']
    save_config()


def set_audio_provider():
    my_config['audio']['provider'] = st.session_state['audio_provider']
    save_config()


def set_local_audio_tts_provider():
    test_config(my_config, "audio", "local_tts", 'provider')
    my_config['audio']['local_tts']['provider'] = st.session_state['local_audio_tts_provider']
    save_config()


def set_local_audio_recognition_provider():
    test_config(my_config, "audio", "local_recognition", 'provider')
    my_config['audio']['local_recognition']['provider'] = st.session_state['local_audio_recognition_provider']
    save_config()


def get_recognition_value(key):
    recognition_provider = st.session_state['local_audio_recognition_provider']
    return my_config['audio'].get('local_recognition', {}).get(recognition_provider, {}).get(key, '')


def set_recognition_value(key, session_key):
    recognition_provider = st.session_state['local_audio_recognition_provider']
    test_config(my_config, "audio", "local_recognition", recognition_provider, key)
    my_config['audio']['local_recognition'][recognition_provider][key] = st.session_state[session_key]
    save_config()


def get_chatTTS_server_location():
    return my_config['audio'].get('local_tts', {}).get('chatTTS', {}).get('server_location', '')


def set_chatTTS_server_location():
    test_config(my_config, "audio", "local_tts", 'chatTTS', 'server_location')
    my_config['audio']['local_tts']['chatTTS']['server_location'] = st.session_state['chatTTS_server_location']
    save_config()


def get_GPTSoVITS_server_location():
    return my_config['audio'].get('local_tts', {}).get('GPTSoVITS', {}).get('server_location', '')


def set_GPTSoVITS_server_location():
    test_config(my_config, "audio", "local_tts", 'GPTSoVITS', 'server_location')
    my_config['audio']['local_tts']['GPTSoVITS']['server_location'] = st.session_state['GPTSoVITS_server_location']
    save_config()


def get_CosyVoice_server_location():
    return my_config['audio'].get('local_tts', {}).get('CosyVoice', {}).get('server_location', '')


def set_CosyVoice_server_location():
    test_config(my_config, "audio", "local_tts", 'CosyVoice', 'server_location')
    my_config['audio']['local_tts']['CosyVoice']['server_location'] = st.session_state['CosyVoice_server_location']
    save_config()


def set_audio_key(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['speech_key'] = st.session_state[key]
    save_config()


def set_audio_access_key_id(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['access_key_id'] = st.session_state[key]
    save_config()


def set_audio_access_key_secret(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['access_key_secret'] = st.session_state[key]
    save_config()


def set_audio_app_key(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['app_key'] = st.session_state[key]
    save_config()


def set_audio_region(provider, key):
    if provider not in my_config['audio']:
        my_config['audio'][provider] = {}
    my_config['audio'][provider]['service_region'] = st.session_state[key]
    save_config()


def set_llm_sk(provider, key):
    my_config['llm'][provider]['secret_key'] = st.session_state[key]
    save_config()


def set_llm_key(provider, key):
    my_config['llm'][provider]['api_key'] = st.session_state[key]
    save_config()


def set_llm_base_url(provider, key):
    my_config['llm'][provider]['base_url'] = st.session_state[key]
    save_config()


def set_llm_model_name(provider, key):
    if provider not in my_config['llm']:
        my_config['llm'][provider] = {}
    my_config['llm'][provider]['model_name'] = st.session_state[key]
    save_config()


# ========== 使用 Tabs 组织设置 ==========
tab_llm, tab_audio, tab_resource = st.tabs(["🤖 AI 大模型", "🔊 语音服务", "🎬 资源库"])

# ========== LLM 大模型设置 ==========
with tab_llm:
    llm_providers = ['OpenAI', 'Moonshot', 'Azure', 'Qianfan', 'Baichuan', 'Tongyi', 'DeepSeek', 'Ollama']
    saved_llm_provider = my_config['llm']['provider']
    saved_llm_provider_index = 0
    for i, provider in enumerate(llm_providers):
        if provider == saved_llm_provider:
            saved_llm_provider_index = i
            break

    llm_provider = st.selectbox(
        tr("LLM Provider"),
        options=llm_providers,
        index=saved_llm_provider_index,
        key='llm_provider',
        on_change=set_llm_provider,
        help="推荐使用 Tongyi (通义千问)"
    )

    with st.expander(f"📝 {llm_provider} 配置", expanded=True):
        if llm_provider != 'Ollama':
            st.text_input(
                tr("API Key"),
                value=my_config['llm'].get(llm_provider, {}).get('api_key', ''),
                type="password",
                key=llm_provider + '_api_key',
                on_change=set_llm_key,
                args=(llm_provider, llm_provider + '_api_key')
            )

        if llm_provider == 'Qianfan':
            st.text_input(
                tr("Secret Key"),
                value=my_config['llm'].get(llm_provider, {}).get('secret_key', ''),
                type="password",
                key=llm_provider + '_secret_key',
                on_change=set_llm_sk,
                args=(llm_provider, llm_provider + '_secret_key')
            )
        elif llm_provider in ['Azure', 'DeepSeek', 'Ollama']:
            st.text_input(
                tr("Base Url"),
                value=my_config['llm'].get(llm_provider, {}).get('base_url', ''),
                type="password",
                key=llm_provider + '_base_url',
                on_change=set_llm_base_url,
                args=(llm_provider, llm_provider + '_base_url')
            )

        st.text_input(
            tr("Model Name"),
            value=my_config['llm'].get(llm_provider, {}).get('model_name', ''),
            key=llm_provider + '_model_name',
            on_change=set_llm_model_name,
            args=(llm_provider, llm_provider + '_model_name'),
            help="例如：qwen-turbo, qwen-plus, qwen-max"
        )

# ========== 语音服务设置 ==========
with tab_audio:
    st.info("💡 语音服务用于生成视频配音和字幕识别")
    
    # 本地 TTS 设置
    with st.expander("🎙️ 本地语音合成 (TTS)", expanded=False):
        selected_local_audio_tts_provider = my_config['audio'].get('local_tts', {}).get('provider', 'chatTTS')
        selected_index = local_audio_tts_providers.index(selected_local_audio_tts_provider) if selected_local_audio_tts_provider in local_audio_tts_providers else 0
        
        local_audio_tts_provider = st.selectbox(
            tr("Local Audio TTS Provider"),
            options=local_audio_tts_providers,
            index=selected_index,
            key='local_audio_tts_provider',
            on_change=set_local_audio_tts_provider
        )
        
        if local_audio_tts_provider == 'chatTTS':
            st.text_input(
                label=tr("ChatTTS http server location"),
                placeholder=tr("Input chatTTS http server address"),
                value=get_chatTTS_server_location(),
                key="chatTTS_server_location",
                on_change=set_chatTTS_server_location
            )
        elif local_audio_tts_provider == 'GPTSoVITS':
            st.text_input(
                label=tr("GPT-SoVITS http server location"),
                placeholder=tr("Input GPT-SoVITS http server address"),
                value=get_GPTSoVITS_server_location(),
                key="GPTSoVITS_server_location",
                on_change=set_GPTSoVITS_server_location
            )
        elif local_audio_tts_provider == 'CosyVoice':
            st.text_input(
                label=tr("CosyVoice http server location"),
                placeholder=tr("Input CosyVoice http server address"),
                value=get_CosyVoice_server_location(),
                key="CosyVoice_server_location",
                on_change=set_CosyVoice_server_location
            )

    # 本地语音识别设置
    with st.expander("👂 本地语音识别", expanded=False):
        selected_local_audio_recognition_provider = my_config['audio'].get('local_recognition', {}).get('provider', 'fasterwhisper')
        selected_index = local_audio_recognition_providers.index(selected_local_audio_recognition_provider) if selected_local_audio_recognition_provider in local_audio_recognition_providers else 0
        
        st.selectbox(
            tr("Local Audio recognition Provider"),
            options=local_audio_recognition_providers,
            index=selected_index,
            key='local_audio_recognition_provider',
            on_change=set_local_audio_recognition_provider
        )
        
        if st.session_state.get('local_audio_recognition_provider') == 'fasterwhisper':
            col1, col2, col3 = st.columns(3)
            with col1:
                st.selectbox(
                    tr("model name"),
                    options=local_audio_recognition_fasterwhisper_module_names,
                    key='recognition_model_name',
                    on_change=set_recognition_value,
                    args=('model_name', 'recognition_model_name')
                )
            with col2:
                st.selectbox(
                    tr("device type"),
                    options=local_audio_recognition_fasterwhisper_device_types,
                    key='recognition_device_type',
                    on_change=set_recognition_value,
                    args=('device_type', 'recognition_device_type')
                )
            with col3:
                st.selectbox(
                    tr("compute type"),
                    options=local_audio_recognition_fasterwhisper_compute_types,
                    key='recognition_compute_type',
                    on_change=set_recognition_value,
                    args=('compute_type', 'recognition_compute_type')
                )

    # 云端语音服务
    with st.expander("☁️ 云端语音服务", expanded=True):
        audio_providers = ['Azure', 'Ali', 'Tencent']
        selected_audio_provider = my_config['audio']['provider']
        selected_index = audio_providers.index(selected_audio_provider) if selected_audio_provider in audio_providers else 0

        audio_provider = st.selectbox(
            tr("Remote Audio Provider"),
            options=audio_providers,
            index=selected_index,
            key='audio_provider',
            on_change=set_audio_provider
        )
        
        if audio_provider == 'Azure':
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(
                    label=tr("Speech Key"),
                    type="password",
                    value=my_config['audio'].get(audio_provider, {}).get('speech_key', ''),
                    on_change=set_audio_key,
                    key=audio_provider + "_speech_key",
                    args=(audio_provider, audio_provider + '_speech_key')
                )
            with col2:
                st.text_input(
                    label=tr("Service Region"),
                    type="password",
                    value=my_config['audio'].get(audio_provider, {}).get('service_region', ''),
                    on_change=set_audio_region,
                    key=audio_provider + "_service_region",
                    args=(audio_provider, audio_provider + '_service_region')
                )
        elif audio_provider in ['Ali', 'Tencent']:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input(
                    label=tr("Access Key ID"),
                    type="password",
                    value=my_config['audio'].get(audio_provider, {}).get('access_key_id', ''),
                    on_change=set_audio_access_key_id,
                    key=audio_provider + "_access_key_id",
                    args=(audio_provider, audio_provider + '_access_key_id')
                )
            with col2:
                st.text_input(
                    label=tr("Access Key Secret"),
                    type="password",
                    value=my_config['audio'].get(audio_provider, {}).get('access_key_secret', ''),
                    on_change=set_audio_access_key_secret,
                    key=audio_provider + "_access_key_secret",
                    args=(audio_provider, audio_provider + '_access_key_secret')
                )
            with col3:
                label = tr("App Key") if audio_provider == 'Ali' else tr("App ID")
                st.text_input(
                    label=label,
                    type="password",
                    value=my_config['audio'].get(audio_provider, {}).get('app_key', ''),
                    on_change=set_audio_app_key,
                    key=audio_provider + "_app_key",
                    args=(audio_provider, audio_provider + '_app_key')
                )

# ========== 资源库设置 ==========
with tab_resource:
    resource_providers = ['pexels', 'pixabay', 'stableDiffusion', 'comfyUI']
    selected_resource_provider = my_config['resource']['provider']
    selected_index = resource_providers.index(selected_resource_provider) if selected_resource_provider in resource_providers else 0

    resource_provider = st.selectbox(
        tr("Resource Provider"),
        options=resource_providers,
        index=selected_index,
        key='resource_provider',
        on_change=set_resource_provider,
        help="推荐使用 pexels 或 pixabay 获取免费素材"
    )
    
    if selected_resource_provider == 'pexels':
        st.text_input(
            tr("Pexels API Key"),
            value=my_config['resource']['pexels']['api_key'],
            type="password",
            key='pexels_api_key',
            on_change=save_pexels_api_key
        )
    elif selected_resource_provider == 'pixabay':
        st.text_input(
            tr("Pixabay API Key"),
            value=my_config['resource']['pixabay']['api_key'],
            type="password",
            key='pixabay_api_key',
            on_change=save_pixabay_api_key
        )
    elif selected_resource_provider == 'stableDiffusion':
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input(
                tr("Stable Diffusion API User Name"),
                value=my_config['resource'].get('stableDiffusion', {}).get('user_name', ''),
                key='stableDiffusion_api_user_name',
                on_change=save_stable_diffusion_api_user_name
            )
        with col2:
            st.text_input(
                tr("Stable Diffusion API Password"),
                type="password",
                value=my_config['resource'].get('stableDiffusion', {}).get('password', ''),
                key='stableDiffusion_api_password',
                on_change=save_stable_diffusion_api_password
            )
        with col3:
            st.text_input(
                tr("Stable Diffusion API Server Address"),
                value=my_config['resource'].get('stableDiffusion', {}).get('server_address', ''),
                key='stableDiffusion_api_server_address',
                on_change=save_stable_diffusion_api_server_address
            )

# ========== 语言设置 ==========
st.markdown("---")
with st.expander("🌐 界面语言", expanded=False):
    display_languages = []
    selected_index = 0
    for i, code in enumerate(languages.keys()):
        display_languages.append(f"{code} - {languages[code]}")
        if f"{code} - {languages[code]}" == st.session_state['ui_language']:
            selected_index = i
    
    st.selectbox(
        tr("Language"),
        options=display_languages,
        index=selected_index,
        key='ui_language',
        on_change=set_ui_language
    )

# ========== 底部信息 ==========
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>如获珠宝·智能视频工坊 | 基于 MoneyPrinterPlus 定制</p>
    </div>
    """,
    unsafe_allow_html=True
)
