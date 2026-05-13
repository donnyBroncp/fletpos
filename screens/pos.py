# ============================================================
# POS SCREEN
# ============================================================

import flet as ft
import data


def pos_screen(page: ft.Page):
    cart = []
    cart_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("Total: ₱0.00", size=18, weight=ft.FontWeight.BOLD)
    search = ft.TextField(
        label="Search product", expand=True, on_change=lambda e: refresh_products()
    )
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh_products():
        product_list.controls.clear()
        query = search.value.lower()
        for p in data.get_products():
            if query in p["name"].lower() and p["stock"] > 0:
                product_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                p["name"], weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Text(
                                                f"₱{p['price']} | Stock: {p['stock']}",
                                                color="grey",
                                                size=12,
                                            ),
                                        ],
                                        expand=True,
                                    ),
                                    ft.ElevatedButton(
                                        "Add",
                                        on_click=lambda e, p=p: add_to_cart(p),
                                        style=ft.ButtonStyle(
                                            bgcolor="indigo", color="white"
                                        ),
                                    ),
                                ],
                            ),
                            padding=10,
                        )
                    )
                )
        page.update()

    def refresh_cart():
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

    def add_to_cart(p):
        for item in cart:
            if item["id"] == p["id"]:
                item["qty"] += 1
                refresh_cart()
                return
        cart.append({"id": p["id"], "name": p["name"], "price": p["price"], "qty": 1})
        refresh_cart()

    def remove_from_cart(item):
        cart.remove(item)
        refresh_cart()

    def checkout(e):
        if not cart:
            return
        for item in cart:
            data.deduct_stock(item["id"], item["qty"])
        total = sum(i["price"] * i["qty"] for i in cart)
        data.add_transaction(
            items=[
                {"name": i["name"], "qty": i["qty"], "price": i["price"]} for i in cart
            ],
            total=total,
        )
        cart.clear()
        refresh_cart()
        refresh_products()

        page.open(
            ft.AlertDialog(
                title=ft.Text("Checkout Success!"),
                content=ft.Text(f"Total: ₱{total:.2f}"),
            )
        )

    refresh_products()

    return ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Products", size=20, weight=ft.FontWeight.BOLD),
                        search,
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
