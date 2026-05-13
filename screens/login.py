# ============================================================
# LOGIN SCREEN
# ============================================================

import flet as ft
import data


def login_screen(page: ft.Page, on_login):
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=300
    )
    error = ft.Text(color="red", size=12)

    def handle_login(e):
        user = data.find_user(username.value, password.value)
        if not user:
            error.value = "Invalid username or password"
            page.update()
            return
        on_login(user)

    def handle_register(e):
        if not username.value or not password.value:
            error.value = "Fill all fields"
            page.update()
            return
        users = data.get_users()
        if any(u["username"] == username.value for u in users):
            error.value = "Username already taken"
            page.update()
            return
        data.add_user(username.value, password.value)
        error.value = ""
        error.color = "green"
        error.value = "Registered! You can now login."
        page.update()

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.icons.INVENTORY, size=60, color="indigo"),
                ft.Text("FlowStock POS", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Sign in to continue", size=14, color="grey"),
                username,
                password,
                error,
                ft.ElevatedButton(
                    "Login",
                    width=300,
                    on_click=handle_login,
                    style=ft.ButtonStyle(bgcolor="indigo", color="white"),
                ),
                ft.TextButton("Register new account", on_click=handle_register),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        alignment=ft.alignment.center,
        expand=True,
    )
