import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Text(
            spans=[
                ft.TextSpan(
                    "print",
                    ft.TextStyle(italic=True, size=20, color=ft.colors.GREEN)
                )
            ],
        ),
    )



ft.app(main)