import flet as ft

# Simple navigation model for the new desktop UI
NAV_ITEMS = [
    # Use string icon names for maximum Flet version compatibility
    ("ai_video", "AI 视频", "movie"),
    ("mix_merge", "混剪/合成", "video_library"),
    ("settings", "设置", "settings"),
]


def build_topbar(on_generate):
    """Top search/intention bar for the main workspace."""
    intent = ft.TextField(
        label="我想做一个...",
        hint_text="例如：30 秒的城市 vlog，风格轻松，中文配音",
        expand=True,
        filled=True,
        border_radius=12,
    )
    action = ft.Button(
        "生成/继续",
        icon="play_arrow",  # string icon for broader compatibility
        on_click=lambda _: on_generate(intent.value),
    )
    return ft.Row([intent, action], spacing=12)


def build_workspace(tab_key: str):
    """Central workspace content varies by tab; currently placeholder blocks."""
    title_map = {
        "ai_video": "AI 视频工作区",
        "mix_merge": "混剪 / 合成工作区",
        "settings": "设置",
    }
    subtitle_map = {
        "ai_video": "输入意图 → 脚本/预览 → 生成视频",
        "mix_merge": "导入音视频素材，快速混剪/合成",
        "settings": "配置 API Key、模型与资源提供方",
    }
    return ft.Column(
        [
            ft.Text(title_map.get(tab_key, ""), size=24, weight=ft.FontWeight.BOLD),
            ft.Text(subtitle_map.get(tab_key, ""), size=14, color="#9ca3af"),
            ft.Container(
                bgcolor="#161920",
                border_radius=12,
                padding=16,
                content=ft.Text("内容区域：预览、脚本编辑、日志/进度等", color="#d1d5db"),
                expand=True,
            ),
        ],
        spacing=12,
        expand=True,
    )


def build_side_panel(tab_key: str):
    """Right-side panel for parameters; currently placeholder fields."""
    if tab_key == "ai_video":
        sections = [
            ft.Text("参数", size=16, weight=ft.FontWeight.BOLD),
            ft.Dropdown(
                label="语言",
                options=[ft.dropdown.Option("zh"), ft.dropdown.Option("en")],
                value="zh",
                filled=True,
            ),
            ft.Dropdown(
                label="视频时长",
                options=[ft.dropdown.Option("30s"), ft.dropdown.Option("60s"), ft.dropdown.Option("90s")],
                value="60s",
                filled=True,
            ),
            ft.Dropdown(
                label="配音人选",
                options=[ft.dropdown.Option("默认"), ft.dropdown.Option("女声 A"), ft.dropdown.Option("男声 B")],
                value="默认",
                filled=True,
            ),
        ]
    elif tab_key == "mix_merge":
        sections = [
            ft.Text("混剪参数", size=16, weight=ft.FontWeight.BOLD),
            ft.Switch(label="自动字幕", value=True),
            ft.Switch(label="自动配乐", value=False),
        ]
    else:
        sections = [
            ft.Text("设置", size=16, weight=ft.FontWeight.BOLD),
            ft.TextField(label="LLM Provider", value="Tongyi Qianwen", filled=True),
            ft.TextField(label="API Key", password=True, can_reveal_password=True, filled=True),
            ft.TextField(label="资源提供方", value="Pexels / Pixabay / SD", filled=True),
        ]

    return ft.Column(
        sections,
        spacing=12,
        scroll="auto",  # string fallback for older Flet versions
    )


def main(page: ft.Page):
    page.title = "MoneyPrinterPlus"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = "#0f1116"
    page.snack_bar = ft.SnackBar(ft.Text("生成流程将在后端接入时启用"))

    state = {"tab": NAV_ITEMS[0][0]}

    workspace_container = ft.Container(
        bgcolor="#0f1116",
        padding=16,
        expand=True,
        content=ft.Column(
            [
                build_topbar(on_generate=lambda intent: page.snack_bar.open()),  # placeholder callback
                build_workspace(state["tab"]),
            ],
            spacing=16,
            expand=True,
        ),
    )

    side_panel = ft.Container(
        width=320,
        bgcolor="#11141c",
        padding=16,
        content=build_side_panel(state["tab"]),
    )

    def handle_nav_change(e: ft.ControlEvent):
        state["tab"] = NAV_ITEMS[e.control.selected_index][0]
        workspace_container.content.controls[1] = build_workspace(state["tab"])
        side_panel.content = build_side_panel(state["tab"])
        page.update()

    nav = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(icon=icon, label=label) for _, label, icon in NAV_ITEMS
        ],
        on_change=handle_nav_change,
        bgcolor="#11141c",
        extended=False,
    )

    layout = ft.Row(
        controls=[
            ft.Container(nav, width=88, bgcolor="#11141c"),
            ft.VerticalDivider(width=1, color="#1f2228"),
            workspace_container,
            ft.VerticalDivider(width=1, color="#1f2228"),
            side_panel,
        ],
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
    )

    page.add(layout)


if __name__ == "__main__":
    # Use run() for newer Flet versions; app() remains for backward compatibility if needed.
    try:
        ft.run(target=main)
    except AttributeError:
        ft.app(target=main)
