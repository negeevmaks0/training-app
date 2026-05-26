import flet as ft

import asyncio
import httpx



class UITrainingApp:
    def __init__(self, settings):
        self.settings = {
            **settings,
            'theme_mode': ft.ThemeMode.DARK,
            'vertical_alignment': ft.MainAxisAlignment.START,
        }

        self.main_content = ft.Container(expand=True)

        self.server_url = 'https://geranium-unsavory-fiscally.ngrok-free.dev'
        self.http_client = httpx.AsyncClient(timeout=4.0)
        self.categories_cache = None



    def on_nav_change(self, e):
        views = {
            0: self.get_exercises_view,
            2: self.get_home_view
        }

        idx = e.control.selected_index
        view_func = views.get(idx, lambda: ft.Text(f'Stranica {idx + 1}', size=30))

        self.main_content.content = view_func()
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
            height=60,
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
            height=100 if self.page.platform == ft.PagePlatform.ANDROID else 85,
            border_radius=ft.BorderRadius(top_left=30, top_right=30, bottom_left=0, bottom_right=0),
            # alignment=ft.Alignment(0, 0),
            padding=ft.Padding(top=5, left=15, right=15, bottom=25 if self.page.platform == ft.PagePlatform.ANDROID else 0),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),

            ),
            # clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        self.main_content.content = self.get_home_view()

        safe_main_content = ft.SafeArea(
            content=ft.Container(
                content=self.main_content,
                padding=ft.Padding(top=10, left=10, right=10)
            ),
            expand=True
        )

        self.page.add(
            ft.Column(
                controls=[
                    safe_main_content,
                    nav_container
                ],
                expand=True,
                spacing=0
            )
        )

        asyncio.create_task(self.pre_warm_server())
        self.page.update()


    def open_add_category_sheet(self, e):
        self.category_input = ft.TextField(
            label="Название категории",
            hint_text="Категория...",
            border_color=ft.Colors.BLUE_400,
            border_radius=10,
            autofocus=True
        )

        self.island_dialog = ft.AlertDialog(
            modal=False,
            bgcolor=ft.Colors.TRANSPARENT,
            content_padding=ft.Padding(0, 0, 0, 0),
            content=ft.Container(
                width=340,
                bgcolor=ft.Colors.BLUE_GREY_900,
                border_radius=20, 
                padding=20,
                content=ft.Column([
                    ft.Text("Новая категория", size=20, weight="bold"),
                    self.category_input,
                    ft.Row([
                        ft.TextButton(
                            "Отмена", 
                            on_click=lambda _: self.close_sheet()
                        ),
                        ft.ElevatedButton(
                            "Добавить",
                            bgcolor=ft.Colors.BLUE_400,
                            color=ft.Colors.WHITE,
                            on_click=self.validate_and_submit 
                        )
                    ], alignment=ft.MainAxisAlignment.END, spacing=10)
                ], tight=True, spacing=20)
            )
        )

        self.page.show_dialog(self.island_dialog)


    def validate_and_submit(self, e):
        text_value = self.category_input.value.strip()
        
        if not text_value or len(text_value) < 2:
            return
            
        print(f"Отправляем в БД: {text_value}")
        
        asyncio.create_task(self.send_category_to_server(text_value))


    async def send_category_to_server(self, category_name):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.server_url}/add_category",
                    json={"name": category_name},
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    self.close_sheet()
                    
                    self.main_content.content = self.get_exercises_view()
                    self.page.update()

                self.categories_cache = None
                    
            except Exception as ex:
                self.category_input.error_text = "Ошибка сети. Сервер недоступен."
                self.category_input.update()


    def close_sheet(self):
        if hasattr(self, 'island_dialog') and self.island_dialog:
            self.page.pop_dialog()


    async def load_exercises_data_from_server(self):
        if self.categories_cache:
            self.render_categories(self.categories_cache)
            
        categories = []

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.server_url}/get_categorys")

                if response.status_code == 200:
                    categories = response.json()
                    self.categories_cache = categories 

        except Exception as e:
            if not self.categories_cache:
                self.categories_area.content = ft.Text("Ошибка сети: Сервер недоступен", color="red")
                self.page.update()

            return

        self.render_categories(categories)


    def render_categories(self, categories):
        if not categories:
            self.categories_area.content = ft.Text("Библиотека пуста. Нажмите на плюс чтобы добавить.", italic=True)
            self.page.update()

            return

        list_view = ft.ListView(
            expand=True,
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.FITNESS_CENTER, color=ft.Colors.BLUE_400),
                        ft.Text(cat["name"], size=18),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE_30),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.Colors.BLUE_GREY_800,
                    padding=15,
                    border_radius=10,
                    on_click=lambda e, c=cat["name"]: print(f"Открываем категорию: {c}")
                ) for cat in categories
            ]
        )

        self.categories_area.content = list_view
        self.page.update()


    async def pre_warm_server(self):
        try:
            response = await self.http_client.get(f"{self.server_url}/get_categorys")

            if response.status_code == 200:
                self.categories_cache = response.json()

        except:
            self.categories_cache = None


    def get_exercises_view(self):
        self.categories_area = ft.Container(
            content=ft.Row([
                ft.ProgressRing(width=30, height=30, color=ft.Colors.BLUE_400),
                ft.Text("Загрузка категорий...", italic=True, size=16)
            ], alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.Alignment(0, 0),
            expand=True
        )

        asyncio.create_task(self.load_exercises_data_from_server())

        return ft.Column([
            ft.Text("Библиотека упражнений", size=25, weight="bold"),
            
            ft.Row([
                ft.TextField(hint_text="Поиск упражнения...", expand=True, border_radius=10),
                ft.IconButton(
                    icon=ft.Icons.ADD_CIRCLE,
                    icon_color=ft.Colors.BLUE_400,
                    on_click=self.open_add_category_sheet
                )
            ]),
            
            self.categories_area
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
        ft.app(target=self.main, port=0)
