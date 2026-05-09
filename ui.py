import flet as ft

import asyncio



class UITrainingApp:
    def __init__(self, settings):
        self.settings = {
            **settings,
            'theme_mode': ft.ThemeMode.DARK,
            'vertical_alignment': ft.MainAxisAlignment.START,
            'safe_area': True
        }

        self.main_content = ft.Container(expand=True)


    def on_nav_change(self, e):
        views = {
            0: self.get_exercises_view(),
            2: self.get_home_view()
        }

        self.main_content.content = views.get(
            e.control.selected_index,
            ft.Text(f'Stranica {e.control.selected_index + 1}', size=30)
        )

        self.page.update()


    async def main(self, page: ft.Page):
        self.page = page

        if self.page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.MACOS]:
            self.page.window.width, self.page.window.height, self.page.window.resizable = 420, 800, False
        
        for key, value in self.settings.items(): setattr(self.page, key, value)

 
        self.page.theme = ft.Theme(tooltip_theme=ft.TooltipTheme(
            wait_duration=100000, show_duration=0, text_style=ft.TextStyle(color=ft.Colors.TRANSPARENT)
        ))

        nav_bar = ft.NavigationBar(
            selected_index=2,
            bgcolor=ft.Colors.BLUE_GREY_900,
            indicator_color=ft.Colors.BLUE_400,
            indicator_shape=ft.CircleBorder(),
            overlay_color=ft.Colors.TRANSPARENT,
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.LIBRARY_BOOKS_OUTLINED, label="Библиотека"),
                ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS_OUTLINED, label="Статистика"),
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                ft.NavigationBarDestination(icon=ft.Icons.ADD, label="Добавить"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Профиль"),
            ],
            on_change=self.on_nav_change,
        )

        nav_container = ft.Container(
            content=nav_bar,
            bgcolor=ft.Colors.BLUE_GREY_900,
            height=80,
            border_radius=ft.border_radius.only(top_left=30, top_right=30),
            margin=ft.margin.only(bottom=0, left=0, right=0), 
            padding=ft.padding.only(bottom=0), 
            
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            ),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        self.main_content.content = self.get_home_view()

        self.page.add(
            self.main_content,
            nav_container
        )


    def get_exercises_view(self):
        categories = ["Грудь", "Спина", "Ноги", "Плечи", "Руки", "Пресс"]
    
        return ft.Column([
            ft.Text("Библиотека упражнений", size=25, weight="bold"),
            
            ft.Row([
                ft.TextField(hint_text="Поиск упражнения...", expand=True, border_radius=10),
                ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_color=ft.Colors.BLUE_400, on_click=lambda _: print("Добавить новое"))
            ]),
            
            ft.ListView(
                expand=True,
                spacing=10,
                controls=[
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.FITNESS_CENTER, color=ft.Colors.BLUE_400),
                            ft.Text(cat, size=18),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE30),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.Colors.BLUE_GREY_800,
                        padding=15,
                        border_radius=10,
                        on_click=lambda e, c=cat: print(f"Открываем категорию: {c}")
                    ) for cat in categories
                ]
            )
        ], expand=True, spacing=20)


    def get_home_view(self):
        return ft.Column([
            ft.ResponsiveRow([
                ft.Container(
                    ft.Text("Карта мышц"),
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    padding=20,
                    col={"sm": 12},
                ),
                ft.Container(
                    ft.Text("Список упражнений"),
                    bgcolor=ft.Colors.BLUE_GREY_800,
                    padding=20,
                    col={"sm": 12},
                ),
            ])
        ])



    def start_ui(self):
        ft.app(self.main)
