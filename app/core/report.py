from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from io import BytesIO
import calendar

import matplotlib.pyplot as plt
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from app.core import USERS_DIRECTORY
from app.core.data_storage import load_user_data

from app.cryptography import auth_encry


def decrypt_item_fields(item: dict, key: bytes, aad: bytes) -> dict:
    # item values are base64 strings -> decrypt -> bytes -> decode to text
    out = {}
    for k, v in item.items():
        out[k] = auth_encry.decrypt_data(key, v, aad).decode("utf-8")
    return out


def get_years_for_user(username: str, encryption_key: bytes) -> dict[int, int]:
        data = load_user_data(username)["data"]
        expenses = data.get("expenses", [])
        incomes = data.get("incomes", [])

        #  auth_encry.decrypt_data(encryption_key, data.get("expenses", []), (username + "expense").encode('utf-8'))
        # auth_encry.decrypt_data(encryption_key, data.get("incomes", []), (username + "incomes").encode('utf-8')) 

        years = {}

        expense_aad = (username + "expense").encode("utf-8")
        income_aad  = (username + "income").encode("utf-8")

        for item in expenses:
            dec = decrypt_item_fields(item, encryption_key, expense_aad)
            year = int(dec["date"][:4])
            years[year] = years.get(year, 0) + 1

        for item in incomes:
            dec = decrypt_item_fields(item, encryption_key, income_aad)
            year = int(dec["date"][:4])
            years[year] = years.get(year, 0) + 1


        return dict(sorted(years.items(), reverse=True))


class ReportGenerator:
    GREEN = "#37E15A"
    BLACK = "#211A1D"
    PURPLE = "#6320EE"
    LIGHT_PURPLE = "#8075FF"
    BEIGE = "#F8F0FB"
    GRAY = "#ADA19C"

    FONT_REGULAR = "Courier"
    FONT_BOLD = "Courier-Bold"
    FONT_ITALIC = "Courier-Oblique"

    


    def __init__(self, username: str, year: int, encryption_key: bytes):
        self.username = username
        self.year = year
        self.encryption_key = encryption_key
        self.styles = self._prepare_styles()

        self.USER_REPORT_DIRECTORY = USERS_DIRECTORY / self.username / "reports"
        self.USER_REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        self.PDF_PATH = self.USER_REPORT_DIRECTORY / f"report_year_{self.year}.pdf"

    # ====================== STYLES PREPARATION ======================
    def _prepare_styles(self):
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name="ReportTitle",
            fontName=self.FONT_BOLD,
            fontSize=28,
            leading=30,
            textColor=self.PURPLE,
            spaceAfter=20,
            alignment=TA_CENTER,
        ))

        styles.add(ParagraphStyle(
            name="ReportSubtitle",
            fontName=self.FONT_REGULAR,
            fontSize=18,
            leading=22,
            textColor=self.GRAY,
            spaceAfter=15,
            alignment=TA_CENTER,
        ))

        styles.add(ParagraphStyle(
            name="ReportHeading",
            fontName=self.FONT_BOLD,
            fontSize=16,
            textColor=self.GREEN,
            spaceBefore=12,
            spaceAfter=8,
        ))

        return styles

    def _get_table_styles(self):
        return TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, self.LIGHT_PURPLE),
            ("BACKGROUND", (0, 0), (-1, -1), self.BEIGE),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("FONTNAME", (1, 0), (-1, -1), self.FONT_REGULAR),
            ("FONTNAME", (0, 0), (0, -1), self.FONT_BOLD),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ])

    def _get_table_with_headings_styles(self):
        return TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, self.LIGHT_PURPLE),
            ("BACKGROUND", (0, 0), (-1, 0), self.PURPLE),
            ("BACKGROUND", (0, 1), (-1, -1), self.BEIGE),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("FONTNAME", (1, 1), (-1, -1), self.FONT_REGULAR),
            ("FONTNAME", (0, 0), (-1, 0), self.FONT_BOLD),
            ("FONTNAME", (0, 0), (0, -1), self.FONT_BOLD),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("TEXTCOLOR", (0, 0), (-1, 0), self.BEIGE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ])
    # ====================== DECRYPTION ======================
    def _decrypt_entries(self, entries: list[dict], aad: bytes) -> list[dict]:
        decrypted = []
        for item in entries:
            decrypted.append(
                decrypt_item_fields(item, self.encryption_key, aad)
            )
        return decrypted

    # ====================== DATA HELPERS ======================
    def _parse_date(self, entry_date: str) -> datetime:
        try:
            return datetime.fromisoformat(entry_date)
        except Exception:
            return datetime.strptime(entry_date.split("T")[0], "%Y-%m-%d")

    def _filter_year(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = []
        for e in entries:
            if "date" not in e:
                continue
            try:
                d = self._parse_date(e["date"])
            except Exception:
                continue
            if d.year == self.year:
                result.append(e)
        return result

    def _sum_total(self, entries: List[Dict[str, Any]]) -> float:
        total = 0.0
        for e in entries:
            try:
                total += float(e.get("amount", 0))
            except Exception:
                pass
        return total

    def _monthly_totals(self, entries: List[Dict[str, Any]]) -> List[float]:
        months = [0.0] * 12
        for e in entries:
            try:
                d = self._parse_date(e["date"])
                amt = float(e.get("amount", 0))
                months[d.month - 1] += amt
            except Exception:
                continue
        return months

    def _category_totals(self, entries: List[Dict[str, Any]]) -> Dict[str, float]:
        totals = {}
        for e in entries:
            cat = str(e.get("category", "other"))
            amt = float(e.get("amount", 0))
            totals[cat] = totals.get(cat, 0) + amt
        return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    # ====================== CHARTS ======================
    def _chart_bar(self, categories: Dict[str, float], title: str) -> BytesIO:
        labels = list(categories.keys()) or ["none"]
        values = list(categories.values()) or [0]

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(labels, values, color=self.PURPLE)
        ax.set_title(title)
        ax.set_ylabel("Amount")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        plt.close(fig)
        buf.seek(0)
        return buf

    def _chart_line(self, inc: List[float], exp: List[float], title: str) -> BytesIO:
        months = list(range(1, 12 + 1))
        fig, ax = plt.subplots(figsize=(6, 3))

        ax.plot(months, inc, marker="o", label="Income", color=self.GREEN)
        ax.plot(months, exp, marker="o", label="Expense", color=self.PURPLE)

        ax.set_xticks(months)
        ax.set_xticklabels([calendar.month_abbr[m] for m in months])
        ax.set_title(title)
        ax.set_ylabel("Amount")
        ax.legend()
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        plt.close(fig)
        buf.seek(0)
        return buf

    # ====================== BUILD REPORT STRUCTURE ======================
    def _build_structure(self):
        raw = load_user_data(self.username)["data"]

        expense_aad = (self.username + "expense").encode("utf-8")
        income_aad  = (self.username + "income").encode("utf-8")

        expenses_dec = self._decrypt_entries(raw["expenses"], expense_aad)
        incomes_dec  = self._decrypt_entries(raw["incomes"], income_aad)

        expenses = self._filter_year(expenses_dec)
        incomes  = self._filter_year(incomes_dec)

        total_income = self._sum_total(incomes)
        total_expense = self._sum_total(expenses)
        balance = total_income - total_expense

        monthly_income = self._monthly_totals(incomes)
        monthly_expense = self._monthly_totals(expenses)

        return {
            "header": {
                "username": self.username,
                "year": self.year,
                "generated_at": datetime.now().strftime("%d %b %Y at %H:%M:%S"),
            },
            "overall_summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance,
                "avg_income": sum(monthly_income) / 12,
                "avg_expense": sum(monthly_expense) / 12,
            },
            "category": {
                "incomes": self._category_totals(incomes),
                "expenses": self._category_totals(expenses),
            },
            "monthly": {
                "income": monthly_income,
                "expense": monthly_expense,
            },
            "top_expenses": sorted(
                expenses,
                key=lambda x: float(x.get("amount", 0)),
                reverse=True,
            )[:10]
        }

    # ====================== PDF GENERATION ======================
    def generate_pdf(self) -> Path:
        """Generates the PDF report and returns the path to the file."""

        data = self._build_structure()

        doc = SimpleDocTemplate(str(self.PDF_PATH), pagesize=A4)
        story = []

        # Header
        h = data["header"]
        story.append(Paragraph(
            f"Yearly Report — {h['year']}",
            self.styles["ReportTitle"]
        ))
        story.append(Paragraph(f"Generated: {h['generated_at']} <br/> User: {h['username']}", self.styles["ReportSubtitle"]))
        story.append(Spacer(1, 12))

        # Overall summary
        story.append(Paragraph("Overall Summary", self.styles["ReportHeading"]))
        story.append(Spacer(1, 8))
        s = data["overall_summary"]

        summary_table = Table([
            ["Total income", f"{s['total_income']:.2f} €"],
            ["Total expense", f"{s['total_expense']:.2f} €"],
            ["Balance", f"{s['balance']:.2f} €"],
            ["Average monthly income", f"{s['avg_income']:.2f} €"],
            ["Average monthly expense", f"{s['avg_expense']:.2f} €"],
        ])
        summary_table.setStyle(self._get_table_styles())
        story.append(summary_table)
        story.append(Spacer(1, 12))

        # Categories - incomes
        story.append(Paragraph("Category Breakdown — Incomes", self.styles["ReportHeading"]))
        story.append(Spacer(1, 8))

        inc_cat = data["category"]["incomes"]
        inc_table = Table([["Category", "Total"]] + [[k, f"{v:.2f} €"] for k, v in inc_cat.items()])
        inc_table.setStyle(self._get_table_with_headings_styles())
        story.append(inc_table)
        story.append(Spacer(1, 12))

        # Categories - expenses
        story.append(Paragraph("Category Breakdown — Expenses", self.styles["ReportHeading"]))
        story.append(Spacer(1, 8))

        exp_cat = data["category"]["expenses"]
        exp_table = Table([["Category", "Total"]] + [[k, f"{v:.2f} €"] for k, v in exp_cat.items()])
        exp_table.setStyle(self._get_table_with_headings_styles())
        story.append(exp_table)
        story.append(Spacer(1, 12))

        story.append(PageBreak())

        # Charts
        story.append(Paragraph("Charts", self.styles["ReportHeading"]))
        story.append(Spacer(1, 8))

        chart1 = self._chart_bar(exp_cat, "Expenses by Category")
        story.append(Image(chart1, width=450, height=200))
        story.append(Spacer(1, 8))

        chart2 = self._chart_line(
            data["monthly"]["income"],
            data["monthly"]["expense"],
            "Monthly Income vs Expense"
        )
        story.append(Image(chart2, width=450, height=200))
        story.append(Spacer(1, 18))

        # Monthly breakdown table
        story.append(Paragraph("Monthly Breakdown", self.styles["ReportHeading"]))
        story.append(Spacer(1, 8))

        months1 = [calendar.month_name[i+1] for i in range(6)]
        monthly_table1 = Table([
            [" "] + months1,
            ["Income"] + [f"{data['monthly']['income'][i]:.2f}" for i in range(6)],
            ["Expense"] + [f"{data['monthly']['expense'][i]:.2f}" for i in range(6)],
        ])
        monthly_table1.setStyle(self._get_table_with_headings_styles())
        story.append(monthly_table1)
        story.append(Spacer(1, 8))

        months2 = [calendar.month_name[i+7] for i in range(6)]
        monthly_table2 = Table([
            [" "] + months2,
            ["Income"] + [f"{data['monthly']['income'][i+6]:.2f} €" for i in range(6)],
            ["Expense"] + [f"{data['monthly']['expense'][i+6]:.2f} €" for i in range(6)],
        ])
        monthly_table2.setStyle(self._get_table_with_headings_styles())
        story.append(monthly_table2)
        story.append(Spacer(1, 18))

        story.append(PageBreak())

        # Top expenses
        story.append(Paragraph("Top 10 Largest Expenses", self.styles["ReportHeading"]))
        story.append(Spacer(1, 8))

        top_rows = [
            ["Amount", "Category", "Date"]
        ] + [
            [
                f"{float(e.get('amount',0)):.2f} €",
                e.get("category",""),
                self._parse_date(e.get("date","")).strftime("%d %b %Y"),
            ] for e in data["top_expenses"]
        ]
        top_table = Table(top_rows)
        top_table.setStyle(self._get_table_with_headings_styles())
        story.append(top_table)

        # Footer function
        def add_footer(canvas, doc):
            width, height = A4
            canvas.saveState()

            canvas.setStrokeColorRGB(0.6, 0.3, 0.8)
            canvas.setLineWidth(1)
            canvas.line(30, 30, width - 30, 30)

            footer_text = "Cryptography 2025 - Zofia Rozanska & Selina Zundel"
            canvas.setFont(self.FONT_ITALIC, 8)
            canvas.drawCentredString(width / 2.0, 15, footer_text)

            page_number_text = f"Page {doc.page}"
            canvas.setFont(self.FONT_BOLD, 8)
            canvas.drawRightString(width - 30, 15, page_number_text)

            canvas.restoreState()

        # Build PDF
        doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
        return self.PDF_PATH