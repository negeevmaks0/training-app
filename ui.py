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

        self.page.navigation_bar = ft.NavigationBar(
            selected_index=2,
            bgcolor=ft.Colors.BLUE_GREY_900,
            indicator_color=ft.Colors.BLUE_400,
            indicator_shape=ft.CircleBorder(),
            overlay_color=ft.Colors.TRANSPARENT,
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, label="Профиль"),
                ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS_OUTLINED, label="Статистика"),
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                ft.NavigationBarDestination(icon=ft.Icons.FITNESS_CENTER, label="Зал"),
                ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Настройки"),
            ],
            on_change=self.on_nav_change,
        )

        self.main_content.content = self.get_home_view()

        self.page.add(self.main_content)


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
