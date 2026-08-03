"""Isolated demo application for the accounting project.

This module intentionally has no Supabase, HTTP, socket, environment-variable,
or production database integration. Every run creates a fresh in-memory SQLite
store populated with fictional records.
"""

from __future__ import annotations

import sqlite3
import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk


@dataclass(frozen=True)
class DemoSummary:
    receivable: float
    payable: float
    overdue: float


class DemoStore:
    """Ephemeral, fictional data store that disappears when the app closes."""

    def __init__(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self._create_schema()
        self._seed_fictional_data()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE accounts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                account_type TEXT NOT NULL CHECK(account_type IN ('customer', 'supplier')),
                balance REAL NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                sku TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                stock INTEGER NOT NULL,
                sale_price REAL NOT NULL
            );
            """
        )

    def _seed_fictional_data(self) -> None:
        self.connection.executemany(
            """
            INSERT INTO accounts(name, account_type, balance, due_date, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                ("Demo Müşteri A", "customer", 18_750.00, "2026-08-08", "Yaklaşıyor"),
                ("Demo Müşteri B", "customer", 7_420.50, "2026-07-28", "Gecikmiş"),
                ("Örnek Tedarikçi A", "supplier", -12_300.00, "2026-08-12", "Yaklaşıyor"),
                ("Örnek Tedarikçi B", "supplier", -4_950.00, "2026-07-30", "Gecikmiş"),
            ],
        )
        self.connection.executemany(
            """
            INSERT INTO products(sku, name, stock, sale_price)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("DEMO-001", "Demo Fren Balatası", 18, 425.00),
                ("DEMO-002", "Demo Hava Filtresi", 9, 310.00),
                ("DEMO-003", "Demo Siperlik Camı", 4, 1_250.00),
            ],
        )
        self.connection.commit()

    def summary(self) -> DemoSummary:
        row = self.connection.execute(
            """
            SELECT
                COALESCE(SUM(CASE WHEN balance > 0 THEN balance ELSE 0 END), 0) AS receivable,
                ABS(COALESCE(SUM(CASE WHEN balance < 0 THEN balance ELSE 0 END), 0)) AS payable,
                COALESCE(SUM(CASE WHEN status = 'Gecikmiş' THEN ABS(balance) ELSE 0 END), 0) AS overdue
            FROM accounts
            """
        ).fetchone()
        return DemoSummary(row["receivable"], row["payable"], row["overdue"])

    def accounts(self) -> list[sqlite3.Row]:
        return self.connection.execute(
            """
            SELECT name, account_type, balance, due_date, status
            FROM accounts
            ORDER BY account_type, name
            """
        ).fetchall()

    def products(self) -> list[sqlite3.Row]:
        return self.connection.execute(
            """
            SELECT sku, name, stock, sale_price
            FROM products
            ORDER BY name
            """
        ).fetchall()

    def close(self) -> None:
        self.connection.close()


def format_try(value: float) -> str:
    formatted = f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{formatted} TL"


class DemoApplication(tk.Tk):
    def __init__(self, store: DemoStore | None = None) -> None:
        super().__init__()
        self.store = store or DemoStore()
        self.title("Türkmopet Muhasebe — İzole Demo")
        self.geometry("1080x680")
        self.minsize(900, 560)
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._build_ui()

    def _build_ui(self) -> None:
        header = ttk.Frame(self, padding=16)
        header.pack(fill="x")
        ttk.Label(header, text="İZOLE DEMO MODU", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="Bu ekran yalnız kurgusal veriler kullanır. Bulut, Supabase ve gerçek şirket veritabanı bağlantısı yoktur.",
        ).pack(anchor="w", pady=(4, 0))

        summary = self.store.summary()
        cards = ttk.Frame(self, padding=(16, 0, 16, 12))
        cards.pack(fill="x")
        for title, value in (
            ("Toplam Alacak", format_try(summary.receivable)),
            ("Toplam Borç", format_try(summary.payable)),
            ("Gecikmiş Risk", format_try(summary.overdue)),
        ):
            card = ttk.LabelFrame(cards, text=title, padding=14)
            card.pack(side="left", fill="x", expand=True, padx=(0, 10))
            ttk.Label(card, text=value, font=("Segoe UI", 16, "bold")).pack(anchor="w")

        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        tabs.add(self._accounts_tab(tabs), text="Cariler")
        tabs.add(self._products_tab(tabs), text="Ürünler")

    def _accounts_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=12)
        columns = ("name", "type", "balance", "due", "status")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        headings = {
            "name": "Cari",
            "type": "Tür",
            "balance": "Bakiye",
            "due": "Vade",
            "status": "Durum",
        }
        for column, heading in headings.items():
            tree.heading(column, text=heading)
        for row in self.store.accounts():
            account_type = "Müşteri" if row["account_type"] == "customer" else "Tedarikçi"
            tree.insert("", "end", values=(row["name"], account_type, format_try(row["balance"]), row["due_date"], row["status"]))
        tree.pack(fill="both", expand=True)
        return frame

    def _products_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent, padding=12)
        columns = ("sku", "name", "stock", "price")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for column, heading in {
            "sku": "Kod",
            "name": "Ürün",
            "stock": "Stok",
            "price": "Satış Fiyatı",
        }.items():
            tree.heading(column, text=heading)
        for row in self.store.products():
            tree.insert("", "end", values=(row["sku"], row["name"], row["stock"], format_try(row["sale_price"])))
        tree.pack(fill="both", expand=True)
        return frame

    def _close(self) -> None:
        self.store.close()
        self.destroy()


def main() -> None:
    DemoApplication().mainloop()


if __name__ == "__main__":
    main()
