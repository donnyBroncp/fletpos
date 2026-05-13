# ============================================================
# SALES REPORT SCREEN
# ============================================================

import flet as ft
import data


def sales_report_screen(page: ft.Page):
    report_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh():
        report_list.controls.clear()
        transactions = data.get_transactions()

        if not transactions:
            report_list.controls.append(ft.Text("No transactions yet.", color="grey"))
            page.update()
            return

        total_sales = sum(t["total"] for t in transactions)

        for t in reversed(transactions):
            items_text = ", ".join(f"{i['name']} x{i['qty']}" for i in t["items"])
            report_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            f"Transaction #{t['id']}",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(t["date"], color="grey", size=12),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Text(items_text, color="grey", size=12),
                                ft.Text(
                                    f"Total: ₱{t['total']:.2f}",
                                    color="green",
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                        padding=12,
                    )
                )
            )

        report_list.controls.append(ft.Divider())
        report_list.controls.append(
            ft.Text(
                f"Overall Sales: ₱{total_sales:.2f}",
                size=18,
                weight=ft.FontWeight.BOLD,
                color="indigo",
            )
        )
        page.update()

    refresh()

    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Sales Report", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.Icons.REFRESH, on_click=lambda e: refresh()),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            report_list,
        ],
        expand=True,
    )
