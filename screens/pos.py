# ============================================================
# POS SCREEN — with error trapping
# ============================================================

import flet as ft
import data


def pos_screen(page: ft.Page):
    cart = []
    cart_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("Total: ₱0.00", size=18, weight=ft.FontWeight.BOLD)
    error = ft.Text(color="red", size=12)
    search = ft.TextField(
        label="Search product", expand=True, on_change=lambda e: refresh_products()
    )
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def show_error(msg):
        error.value = msg
        page.update()

    def refresh_products():
        try:
            product_list.controls.clear()
            query = search.value.lower()
            for p in data.get_products():
                if query in p["name"].lower():
                    out_of_stock = p["stock"] <= 0
                    product_list.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    p["name"],
                                                    weight=ft.FontWeight.BOLD,
                                                    color=(
                                                        "grey" if out_of_stock else None
                                                    ),
                                                ),
                                                ft.Text(
                                                    f"₱{p['price']} | Stock: {p['stock']}",
                                                    color=(
                                                        "red"
                                                        if out_of_stock
                                                        else "grey"
                                                    ),
                                                    size=12,
                                                ),
                                            ],
                                            expand=True,
                                        ),
                                        ft.ElevatedButton(
                                            "Add",
                                            on_click=lambda e, p=p: add_to_cart(p),
                                            disabled=out_of_stock,
                                            style=ft.ButtonStyle(
                                                bgcolor=(
                                                    "grey" if out_of_stock else "indigo"
                                                ),
                                                color="white",
                                            ),
                                        ),
                                    ],
                                ),
                                padding=10,
                            )
                        )
                    )
            page.update()
        except Exception as ex:
            show_error(f"Failed to load products: {ex}")

    def refresh_cart():
        try:
            cart_list.controls.clear()
            for item in cart:
                cart_list.controls.append(
                    ft.Row(
                        controls=[
                            ft.Text(item["name"], expand=True),
                            ft.Text(f"x{item['qty']}"),
                            ft.Text(f"₱{item['price'] * item['qty']:.2f}", width=80),
                            ft.IconButton(
                                ft.Icons.REMOVE_CIRCLE,
                                on_click=lambda e, item=item: remove_from_cart(item),
                                icon_color="red",
                            ),
                        ]
                    )
                )
            total = sum(i["price"] * i["qty"] for i in cart)
            total_text.value = f"Total: ₱{total:.2f}"
            page.update()
        except Exception as ex:
            show_error(f"Failed to refresh cart: {ex}")

    def add_to_cart(p):
        try:
            if p["stock"] <= 0:
                show_error(f"{p['name']} is out of stock")
                return
            for item in cart:
                if item["id"] == p["id"]:
                    if item["qty"] >= p["stock"]:
                        show_error(f"Not enough stock for {p['name']}")
                        return
                    item["qty"] += 1
                    error.value = ""
                    refresh_cart()
                    return
            cart.append(
                {"id": p["id"], "name": p["name"], "price": p["price"], "qty": 1}
            )
            error.value = ""
            refresh_cart()
        except Exception as ex:
            show_error(f"Failed to add to cart: {ex}")

    def remove_from_cart(item):
        try:
            cart.remove(item)
            refresh_cart()
        except Exception as ex:
            show_error(f"Failed to remove from cart: {ex}")

    def checkout(e):
        try:
            if not cart:
                show_error("Cart is empty")
                return
            for item in cart:
                data.deduct_stock(item["id"], item["qty"])
            total = sum(i["price"] * i["qty"] for i in cart)
            data.add_transaction(
                items=[
                    {"name": i["name"], "qty": i["qty"], "price": i["price"]}
                    for i in cart
                ],
                total=total,
            )
            cart.clear()
            error.value = ""
            refresh_cart()
            refresh_products()

            dlg = ft.AlertDialog(
                title=ft.Text("Checkout Success!"),
                content=ft.Text(f"Total: ₱{total:.2f}"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: close_dlg(dlg)),
                ],
            )
            page.overlay.append(dlg)
            dlg.open = True
            page.update()

        except Exception as ex:
            show_error(f"Checkout failed: {ex}")

    def close_dlg(dlg):
        dlg.open = False
        page.update()

    refresh_products()

    return ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Products", size=20, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    ft.Icons.REFRESH,
                                    on_click=lambda e: refresh_products(),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        search,
                        error,
                        product_list,
                    ],
                    expand=True,
                ),
                expand=True,
                padding=10,
            ),
            ft.VerticalDivider(),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Cart", size=20, weight=ft.FontWeight.BOLD),
                        cart_list,
                        ft.Divider(),
                        total_text,
                        ft.ElevatedButton(
                            "Checkout",
                            on_click=checkout,
                            width=200,
                            style=ft.ButtonStyle(bgcolor="green", color="white"),
                        ),
                    ],
                    expand=True,
                ),
                width=300,
                padding=10,
            ),
        ],
        expand=True,
    )
