# ============================================================
# MAIN — entry point
# ============================================================

import flet as ft
from screens.login import login_screen
from screens.pos import pos_screen
from screens.inventory import inventory_screen
from screens.sales_report import sales_report_screen
from screens.users import users_screen


def main(page: ft.Page):
    page.title = "FlowStock POS"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0

    current_user = {"value": None}

    def on_login(user):
        current_user["value"] = user
        show_main()

    def show_main():
        page.controls.clear()

        def change_tab(e):
            content.content = tabs[e.control.selected_index]
            page.update()

        tabs = [
            ft.Container(content=pos_screen(page), padding=20, expand=True),
            ft.Container(content=inventory_screen(page), padding=20, expand=True),
            ft.Container(content=sales_report_screen(page), padding=20, expand=True),
            ft.Container(
                content=users_screen(page, current_user["value"]),
                padding=20,
                expand=True,
            ),
        ]

        content = ft.Container(content=tabs[0], expand=True)

        page.add(
            ft.Row(
                controls=[
                    ft.NavigationRail(
                        selected_index=0,
                        label_type=ft.NavigationRailLabelType.ALL,
                        on_change=change_tab,
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.Icons.POINT_OF_SALE, label="POS"
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.STORE, label="Inventory"
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.BAR_CHART, label="Sales"
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.PEOPLE, label="Users"
                            ),
                        ],
                        trailing=ft.IconButton(
                            ft.Icons.LOGOUT,
                            on_click=lambda e: show_login(),
                            tooltip="Logout",
                        ),
                    ),
                    ft.VerticalDivider(width=1),
                    content,
                ],
                expand=True,
            )
        )
        page.update()

    def show_login():
        page.controls.clear()
        page.add(login_screen(page, on_login))
        page.update()

    show_login()


ft.app(target=main)
