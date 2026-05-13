# ============================================================
# INVENTORY SCREEN
# ============================================================

import flet as ft
import data


def inventory_screen(page: ft.Page):
    name = ft.TextField(label="Product Name", expand=True)
    price = ft.TextField(label="Price", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    stock = ft.TextField(label="Stock", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    error = ft.Text(color="red", size=12)
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh():
        product_list.controls.clear()
        for p in data.get_products():
            product_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(p["name"], weight=ft.FontWeight.BOLD),
                                        ft.Text(
                                            f"₱{p['price']} | Stock: {p['stock']}",
                                            color="grey",
                                            size=12,
                                        ),
                                    ],
                                    expand=True,
                                ),
                                ft.IconButton(
                                    ft.Icons.EDIT,
                                    on_click=lambda e, p=p: open_edit(p),
                                    icon_color="blue",
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE,
                                    on_click=lambda e, p=p: handle_delete(p["id"]),
                                    icon_color="red",
                                ),
                            ],
                        ),
                        padding=10,
                    )
                )
            )
        page.update()

    def handle_add(e):
        if not name.value or not price.value or not stock.value:
            error.value = "Fill all fields"
            page.update()
            return
        products = data.get_products()
        if any(p["name"].lower() == name.value.lower() for p in products):
            error.value = "Product already exists"
            page.update()
            return
        data.add_product(name.value, float(price.value), int(stock.value))
        name.value = price.value = stock.value = error.value = ""
        refresh()

    def handle_delete(id):
        data.delete_product(id)
        refresh()

    def open_edit(p):
        edit_name = ft.TextField(label="Name", value=p["name"])
        edit_price = ft.TextField(label="Price", value=str(p["price"]))
        edit_stock = ft.TextField(label="Stock", value=str(p["stock"]))

        def save_edit(e):
            data.update_product(
                p["id"], edit_name.value, float(edit_price.value), int(edit_stock.value)
            )
            page.close(dlg)
            refresh()

        dlg = ft.AlertDialog(
            title=ft.Text("Edit Product"),
            content=ft.Column(controls=[edit_name, edit_price, edit_stock], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: page.close(dlg)),
                ft.ElevatedButton("Save", on_click=save_edit),
            ],
        )
        page.open(dlg)

    refresh()

    return ft.Column(
        controls=[
            ft.Text("Inventory", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[name, price, stock]),
            error,
            ft.ElevatedButton("Add Product", on_click=handle_add, icon=ft.Icons.ADD),
            ft.Divider(),
            product_list,
        ],
        expand=True,
    )
