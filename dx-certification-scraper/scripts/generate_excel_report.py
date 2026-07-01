"""
DX Certification Excel Report Generator
======================================
Generates a highly styled Excel report from extracted company data and
LLM-generated classifications.
"""

import json
import sys
import argparse
from pathlib import Path

# Ensure openpyxl is installed
try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl", "-q"])
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter


def generate_report(data_path: str, classification_path: str, output_path: str):
    # Load raw extracted data
    with open(data_path, "r", encoding="utf-8") as f:
        companies = json.load(f)

    # Load LLM classifications
    with open(classification_path, "r", encoding="utf-8") as f:
        classifications = json.load(f)

    # Merge classifications into company data
    for c in companies:
        pid = c.get("procedure_id")
        clf = classifications.get(pid, {})
        c["tier"] = clf.get("tier", "C")
        c["reason"] = clf.get("reason", "Not classified/Vague mention")
        c["target_detail"] = clf.get("target_detail", "")

    # Create Workbook
    wb = openpyxl.Workbook()

    # Styling definitions
    font_family = "Segoe UI"
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name=font_family, color="FFFFFF", bold=True, size=11)
    
    tier_fills = {
        "A": PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid"), # Light green
        "B": PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"), # Light yellow
        "C": PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")  # Light gray
    }
    
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )
    
    normal_font = Font(name=font_family, size=10)
    bold_font = Font(name=font_family, size=10, bold=True)

    # Build Sheet 1 (A-tier) & Sheet 2 (B-tier)
    tiers = [("A", "A级核心目标"), ("B", "B级潜在目标")]
    for tier_code, sheet_name in tiers:
        ws = wb.create_sheet(title=sheet_name)
        
        headers = [
            "手続き番号", "企業名", "法人番号", "代表者", "住所", 
            "従業員数", "規模", "業種", "認定適用日", 
            "分析結果・分類理由", "ターゲット詳細 / 需要予測"
        ]
        
        for col, h in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=h)
            cell.fill = header_fill
            cell.font = header_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            
        ws.row_dimensions[1].height = 28
        
        # Filter companies
        target_companies = [c for c in companies if c.get("tier") == tier_code]
        
        for row_idx, c in enumerate(target_companies, 2):
            values = [
                c.get("procedure_id", ""),
                c.get("company_name", ""),
                c.get("corp_number", ""),
                c.get("representative", ""),
                c.get("address", ""),
                c.get("employees", ""),
                c.get("scale", ""),
                c.get("industry", ""),
                c.get("cert_start", ""),
                c.get("reason", ""),
                c.get("target_detail", "")
            ]
            for col, val in enumerate(values, 1):
                cell = ws.cell(row=row_idx, column=col, value=val)
                cell.font = normal_font
                cell.border = thin_border
                
                # Alignments
                if col in [10, 11]:
                    cell.alignment = Alignment(vertical="top", wrap_text=True)
                else:
                    cell.alignment = Alignment(vertical="center")
                    
            ws.row_dimensions[row_idx].height = 40 if tier_code == "A" else 30
            
        # Column widths
        for col in range(1, 10):
            ws.column_dimensions[get_column_letter(col)].width = 16
        ws.column_dimensions["J"].width = 45 # Reason
        ws.column_dimensions["K"].width = 45 # Detail

    # Build Sheet 3 (All Companies Summary)
    ws_all = wb.active
    ws_all.title = "全企業一覧"
    
    headers_all = [
        "手続き番号", "企業名", "法人番号", "代表者", "住所", 
        "従業員数", "規模", "業種", "認定適用日", "ターゲット分類"
    ]
    
    for col, h in enumerate(headers_all, 1):
        cell = ws_all.cell(row=1, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    ws_all.row_dimensions[1].height = 28
    
    # Sort all by Tier (A then B then C)
    companies_sorted = sorted(
        companies, 
        key=lambda x: ("A", "B", "C").index(x.get("tier", "C"))
    )
    
    for row_idx, c in enumerate(companies_sorted, 2):
        tier_val = c.get("tier", "C")
        values = [
            c.get("procedure_id", ""),
            c.get("company_name", ""),
            c.get("corp_number", ""),
            c.get("representative", ""),
            c.get("address", ""),
            c.get("employees", ""),
            c.get("scale", ""),
            c.get("industry", ""),
            c.get("cert_start", ""),
            f"{tier_val}级"
        ]
        for col, val in enumerate(values, 1):
            cell = ws_all.cell(row=row_idx, column=col, value=val)
            cell.font = normal_font if col != 10 else bold_font
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center", horizontal="center" if col in [1, 9, 10] else "left")
            
            # Highlight classifications
            if col == 10:
                cell.fill = tier_fills.get(tier_val, tier_fills["C"])
                
        ws_all.row_dimensions[row_idx].height = 22
        
    for col in range(1, 11):
        ws_all.column_dimensions[get_column_letter(col)].width = 16

    wb.save(output_path)
    print(f"Report successfully compiled: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate styled XLSX reports from classifications")
    parser.add_argument("--data", required=True, help="Raw extracted JSON data path")
    parser.add_argument("--classifications", required=True, help="LLM classifications JSON path")
    parser.add_argument("--output", required=True, help="Output XLSX file path")
    
    args = parser.parse_args()
    generate_report(args.data, args.classifications, args.output)
