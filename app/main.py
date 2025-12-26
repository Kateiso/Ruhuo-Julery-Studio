import asyncio
import flet as ft

NAV_ITEMS = [
    ("studio", "创作台", "auto_awesome"),
    ("mix", "混剪/合成", "movie_edit"),
    ("settings", "设置", "settings"),
]

COLORS = {
    "bg": "#0b0f14",
    "panel": "#111823",
    "panel_alt": "#0f151f",
    "card": "#151e2a",
    "card_alt": "#0f1621",
    "border": "#1f2a3a",
    "text": "#e2e8f0",
    "muted": "#94a3b8",
    "accent": "#38bdf8",
    "accent_2": "#f59e0b",
}

def _alignment(x: float, y: float):
    alignment_cls = getattr(ft, "Alignment", None) or getattr(ft.alignment, "Alignment", None)
    if alignment_cls:
        return alignment_cls(x, y)
    return None


ALIGN_CENTER = getattr(ft.alignment, "center", _alignment(0, 0))
ALIGN_TOP_LEFT = getattr(ft.alignment, "top_left", _alignment(-1, -1))
ALIGN_BOTTOM_RIGHT = getattr(ft.alignment, "bottom_right", _alignment(1, 1))

def resolve_icon(name: str):
    icon_pack = getattr(ft, "icons", None)
    if icon_pack:
        icon_value = getattr(icon_pack, name.upper(), None)
        if icon_value:
            return icon_value
    return name


def icon_control(name: str, size: int | None = None, color: str | None = None) -> ft.Icon:
    icon_value = resolve_icon(name)
    try:
        return ft.Icon(icon_value, size=size, color=color)
    except TypeError:
        try:
            return ft.Icon(icon=icon_value, size=size, color=color)
        except TypeError:
            return ft.Icon(name=icon_value, size=size, color=color)


def badge(text: str, color: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(text, size=12, color=COLORS["text"]),
        bgcolor=color,
        padding=ft.Padding(6, 2, 6, 2),
        border_radius=999,
    )


def section_title(text: str) -> ft.Text:
    return ft.Text(text, size=15, weight=ft.FontWeight.BOLD, color=COLORS["text"])


def build_card(title: str, subtitle: str, content: ft.Control, height: int | None = None) -> ft.Container:
    return ft.Container(
        bgcolor=COLORS["card"],
        border=ft.border.all(1, COLORS["border"]),
        border_radius=16,
        padding=16,
        height=height,
        content=ft.Column(
            [
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                ft.Text(subtitle, size=12, color=COLORS["muted"]),
                content,
            ],
            spacing=10,
        ),
    )


def build_studio_workspace(on_preview, on_generate) -> ft.Column:
    intent_field = ft.TextField(
        hint_text="例如：30 秒的城市 vlog，风格轻松，中文配音",
        filled=True,
        bgcolor=COLORS["card_alt"],
        border_radius=12,
        min_lines=2,
        max_lines=4,
        expand=True,
    )

    action_row = ft.Row(
        [
            ft.ElevatedButton(
                "生成脚本/预览",
                icon=resolve_icon("bolt"),
                on_click=on_preview,
                style=ft.ButtonStyle(
                    bgcolor=COLORS["accent"],
                    color=COLORS["bg"],
                    padding=ft.Padding(18, 12, 18, 12),
                ),
            ),
            ft.OutlinedButton(
                "生成视频",
                icon=resolve_icon("movie"),
                on_click=on_generate,
                style=ft.ButtonStyle(color=COLORS["text"], padding=ft.Padding(18, 12, 18, 12)),
            ),
            badge("后端未接入", COLORS["panel_alt"]),
        ],
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        wrap=True,
    )

    hero = ft.Container(
        border_radius=18,
        padding=20,
        bgcolor=COLORS["card"],
        border=ft.border.all(1, COLORS["border"]),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("创作台", size=28, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                                ft.Text(
                                    "输入视频意图，生成脚本/预览，开始生成视频",
                                    size=13,
                                    color=COLORS["muted"],
                                ),
                            ],
                            spacing=4,
                        ),
                        badge("AI Creator", "#0f172a"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=12, color="transparent"),
                intent_field,
                action_row,
            ],
            spacing=12,
        ),
    )

    script_card = build_card(
        "脚本预览",
        "生成脚本后可在此微调段落与节奏",
        ft.Column(
            [
                ft.Text("1. 开场：城市夜景 + 旁白引入", color=COLORS["text"]),
                ft.Text("2. 过渡：咖啡馆/街头镜头切换", color=COLORS["text"]),
                ft.Text("3. 收尾：夜灯与一句总结", color=COLORS["text"]),
            ],
            spacing=6,
        ),
    )

    preview_card = build_card(
        "画面预览",
        "未来接入视频素材/合成预览",
        ft.Container(
            height=170,
            border_radius=14,
            bgcolor=COLORS["card_alt"],
            alignment=ALIGN_CENTER,
            content=ft.Column(
                [
                    icon_control("image", size=32, color=COLORS["muted"]),
                    ft.Text("预览窗口", color=COLORS["muted"]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
        ),
    )

    progress_card = build_card(
        "生成进度",
        "阶段化进度与日志将在此显示",
        ft.Column(
            [
                ft.ProgressBar(value=0.15, color=COLORS["accent"], bgcolor=COLORS["panel_alt"]),
                ft.Text("脚本草稿：准备中", color=COLORS["muted"]),
                ft.Text("素材采集：待接入", color=COLORS["muted"]),
                ft.Text("视频渲染：待接入", color=COLORS["muted"]),
            ],
            spacing=8,
        ),
    )

    assets_card = build_card(
        "素材清单",
        "用于管理引用素材与镜头需求",
        ft.Column(
            [
                ft.Text("• 3 段 B-roll：城市夜景、人群、街灯", color=COLORS["text"]),
                ft.Text("• 1 张封面图：主街道远景", color=COLORS["text"]),
                ft.Text("• 背景音乐：轻快 lo-fi", color=COLORS["text"]),
            ],
            spacing=6,
        ),
    )

    row_top = ft.ResponsiveRow(
        [
            ft.Container(content=script_card, col={"sm": 12, "md": 6}),
            ft.Container(content=preview_card, col={"sm": 12, "md": 6}),
        ],
        spacing=16,
        run_spacing=16,
    )

    row_bottom = ft.ResponsiveRow(
        [
            ft.Container(content=progress_card, col={"sm": 12, "md": 6}),
            ft.Container(content=assets_card, col={"sm": 12, "md": 6}),
        ],
        spacing=16,
        run_spacing=16,
    )

    return ft.Column(
        [hero, row_top, row_bottom],
        spacing=16,
        scroll="auto",
        expand=True,
    )


def build_mix_workspace() -> ft.Column:
    intro = ft.Container(
        border_radius=18,
        padding=20,
        bgcolor=COLORS["card"],
        border=ft.border.all(1, COLORS["border"]),
        content=ft.Column(
            [
                ft.Text("混剪 / 合成", size=24, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                ft.Text("导入素材，设置节奏与字幕，快速输出。", size=13, color=COLORS["muted"]),
            ],
            spacing=6,
        ),
    )

    library_card = build_card(
        "素材库",
        "拖拽或导入本地素材",
        ft.Container(
            height=180,
            border_radius=14,
            bgcolor=COLORS["card_alt"],
            alignment=ALIGN_CENTER,
            content=ft.Text("拖拽素材到此区域", color=COLORS["muted"]),
        ),
    )

    timeline_card = build_card(
        "时间线",
        "镜头排序与音轨控制",
        ft.Container(
            height=140,
            border_radius=14,
            bgcolor=COLORS["card_alt"],
            alignment=ALIGN_CENTER,
            content=ft.Text("时间线占位", color=COLORS["muted"]),
        ),
    )

    return ft.Column(
        [intro, library_card, timeline_card],
        spacing=16,
        scroll="auto",
        expand=True,
    )


def build_settings_workspace(on_save) -> ft.Column:
    return ft.Column(
        [
            ft.Container(
                border_radius=18,
                padding=20,
                bgcolor=COLORS["card"],
                border=ft.border.all(1, COLORS["border"]),
                content=ft.Column(
                    [
                        ft.Text("设置", size=24, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                        ft.Text(
                            "API Key 仅保存在本地配置文件，不在主界面展示。",
                            size=13,
                            color=COLORS["muted"],
                        ),
                    ],
                    spacing=6,
                ),
            ),
            build_card(
                "模型与密钥",
                "选择 LLM 与语音服务",
                ft.Column(
                    [
                        ft.Dropdown(
                            label="LLM Provider",
                            options=[
                                ft.dropdown.Option("Tongyi Qianwen"),
                                ft.dropdown.Option("Qianfan"),
                                ft.dropdown.Option("OpenAI (兼容)"),
                            ],
                            value="Tongyi Qianwen",
                            filled=True,
                        ),
                        ft.TextField(
                            label="LLM API Key",
                            password=True,
                            can_reveal_password=True,
                            filled=True,
                        ),
                        ft.Dropdown(
                            label="语音合成",
                            options=[
                                ft.dropdown.Option("阿里云 TTS"),
                                ft.dropdown.Option("腾讯 TTS"),
                                ft.dropdown.Option("CosyVoice"),
                            ],
                            value="阿里云 TTS",
                            filled=True,
                        ),
                        ft.TextField(
                            label="TTS API Key",
                            password=True,
                            can_reveal_password=True,
                            filled=True,
                        ),
                    ],
                    spacing=12,
                ),
            ),
            build_card(
                "资源与输出",
                "素材来源与默认输出",
                ft.Column(
                    [
                        ft.Dropdown(
                            label="资源提供方",
                            options=[
                                ft.dropdown.Option("Pexels / Pixabay"),
                                ft.dropdown.Option("SD / 本地"),
                            ],
                            value="Pexels / Pixabay",
                            filled=True,
                        ),
                        ft.TextField(label="默认输出路径", value="output/", filled=True),
                        ft.Switch(label="自动保存预览", value=True),
                    ],
                    spacing=12,
                ),
            ),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "保存设置",
                        icon=resolve_icon("save"),
                        on_click=on_save,
                        style=ft.ButtonStyle(bgcolor=COLORS["accent"], color=COLORS["bg"]),
                    ),
                    ft.OutlinedButton("导出配置", icon=resolve_icon("upload_file")),
                ],
                spacing=12,
            ),
        ],
        spacing=16,
        scroll="auto",
        expand=True,
    )


def build_side_panel(tab_key: str, on_action) -> ft.Column:
    if tab_key == "studio":
        content = [
            section_title("生成参数"),
            ft.Dropdown(
                label="语言",
                options=[ft.dropdown.Option("中文"), ft.dropdown.Option("英文")],
                value="中文",
                filled=True,
            ),
            ft.Dropdown(
                label="视频时长",
                options=[ft.dropdown.Option("30s"), ft.dropdown.Option("60s"), ft.dropdown.Option("90s")],
                value="60s",
                filled=True,
            ),
            ft.Dropdown(
                label="画面比例",
                options=[ft.dropdown.Option("9:16"), ft.dropdown.Option("16:9"), ft.dropdown.Option("1:1")],
                value="9:16",
                filled=True,
            ),
            ft.Switch(label="自动字幕", value=True),
            ft.Switch(label="自动配乐", value=False),
            ft.Slider(min=0, max=100, value=60, label="节奏 %"),
        ]
    elif tab_key == "mix":
        content = [
            section_title("混剪参数"),
            ft.Switch(label="智能剪辑", value=True),
            ft.Switch(label="自动节奏对齐", value=True),
            ft.Switch(label="多轨合成", value=False),
            ft.Dropdown(
                label="字幕样式",
                options=[
                    ft.dropdown.Option("简洁"),
                    ft.dropdown.Option("强调"),
                    ft.dropdown.Option("电影感"),
                ],
                value="简洁",
                filled=True,
            ),
        ]
    else:
        content = [
            section_title("环境提示"),
            ft.Text("推荐 Python 3.10/3.11 + FFmpeg 6", size=12, color=COLORS["muted"]),
            ft.Text("Apple Silicon 可设置 ARCHFLAGS=\"-arch arm64\"", size=12, color=COLORS["muted"]),
            ft.Divider(height=12, color="transparent"),
            section_title("操作"),
            ft.ElevatedButton(
                "检查依赖",
                icon=resolve_icon("fact_check"),
                on_click=on_action,
                style=ft.ButtonStyle(bgcolor=COLORS["accent"], color=COLORS["bg"]),
            ),
            ft.OutlinedButton("打开配置目录", icon=resolve_icon("folder_open")),
        ]

    return ft.Column(content, spacing=12, scroll="auto")


def build_workspace(tab_key: str, on_preview, on_generate, on_save) -> ft.Control:
    if tab_key == "studio":
        return build_studio_workspace(on_preview, on_generate)
    if tab_key == "mix":
        return build_mix_workspace()
    return build_settings_workspace(on_save)


def main(page: ft.Page):
    page.title = "MoneyPrinterPlus"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_min_width = 1100
    page.window_min_height = 720
    page.padding = 0
    page.bgcolor = COLORS["bg"]
    page.fonts = {"PingFang": "fonts/PingFang.ttc"}
    page.theme = ft.Theme(font_family="PingFang", color_scheme_seed=COLORS["accent"])
    page.snack_bar = ft.SnackBar(content=ft.Text(""))

    state = {"tab": NAV_ITEMS[0][0]}

    def notify(message: str):
        page.snack_bar.content.value = message
        page.snack_bar.open = True
        page.update()

    def handle_preview(_):
        notify("已提交脚本/预览请求（后端待接入）")

    def handle_generate(_):
        notify("已提交视频生成请求（后端待接入）")

    def handle_save(_):
        notify("设置已保存（占位）")

    def handle_settings_action(_):
        notify("环境检查（占位）")

    workspace_content = build_workspace(state["tab"], handle_preview, handle_generate, handle_save)
    workspace_container = ft.Container(
        expand=True,
        padding=20,
        bgcolor=COLORS["bg"],
        gradient=ft.LinearGradient(
            colors=["#0b0f14", "#0f172a", "#0b0f14"],
            begin=ALIGN_TOP_LEFT,
            end=ALIGN_BOTTOM_RIGHT,
        ),
        animate_opacity=ft.Animation(400, "easeOut"),
        opacity=0,
        content=workspace_content,
    )

    side_panel = ft.Container(
        width=320,
        bgcolor=COLORS["panel"],
        padding=18,
        animate_opacity=ft.Animation(400, "easeOut"),
        opacity=0,
        content=build_side_panel(state["tab"], handle_settings_action),
    )

    def handle_nav_change(e: ft.ControlEvent):
        state["tab"] = NAV_ITEMS[e.control.selected_index][0]
        workspace_container.content = build_workspace(state["tab"], handle_preview, handle_generate, handle_save)
        side_panel.content = build_side_panel(state["tab"], handle_settings_action)
        workspace_container.opacity = 0
        side_panel.opacity = 0
        page.update()
        workspace_container.opacity = 1
        side_panel.opacity = 1
        page.update()

    nav = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=COLORS["panel"],
        extended=False,
        destinations=[
            ft.NavigationRailDestination(icon=resolve_icon(icon), label=label) for _, label, icon in NAV_ITEMS
        ],
        on_change=handle_nav_change,
        leading=ft.Container(
            padding=ft.Padding(8, 16, 8, 8),
            content=ft.Column(
                [
                    icon_control("auto_awesome", color=COLORS["accent"], size=24),
                    ft.Text("M+", size=14, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
                    ft.Text("Creator", size=10, color=COLORS["muted"]),
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ),
    )

    nav_container = ft.Container(
        width=96,
        bgcolor=COLORS["panel"],
        content=nav,
        opacity=0,
        animate_opacity=ft.Animation(400, "easeOut"),
    )

    layout = ft.Row(
        [
            nav_container,
            ft.VerticalDivider(width=1, color=COLORS["border"]),
            workspace_container,
            ft.VerticalDivider(width=1, color=COLORS["border"]),
            side_panel,
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    page.add(layout)

    async def reveal():
        await asyncio.sleep(0.05)
        nav_container.opacity = 1
        page.update()
        await asyncio.sleep(0.08)
        workspace_container.opacity = 1
        page.update()
        await asyncio.sleep(0.08)
        side_panel.opacity = 1
        page.update()

    page.run_task(reveal())


def _launch_app():
    if hasattr(ft, "app"):
        try:
            ft.app(target=main)
            return
        except TypeError:
            ft.app(main)
            return
    try:
        ft.run(target=main)
    except TypeError:
        ft.run(main)


if __name__ == "__main__":
    _launch_app()
