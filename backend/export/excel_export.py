"""
Excel export: generate multi-sheet .xlsx from project data.
Each table becomes a sheet, dynamic tables get rows.
"""
import os
import json
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side


def export_excel(project) -> str:
    output_path = f"/tmp/export_{project.id}.xlsx"
    wb = Workbook()
    wb.remove(wb.active)  # remove default sheet

    sheet_names = {
        1: "单位及系统基本信息",
        2: "云计算应用情况",
        3: "大数据应用情况",
        4: "工业控制系统",
        5: "物联网系统",
        6: "移动互联系统",
    }

    for sec_num in range(1, 7):
        if sec_num >= 2 and not getattr(project, f"section{sec_num}_enabled"):
            continue
        data = project.get_section_data(sec_num)
        if not data:
            continue

        _write_section(wb, sheet_names[sec_num], data)

    wb.save(output_path)
    return output_path


def _write_section(wb, section_name, data):
    """Write a section's data to sheets."""
    if not isinstance(data, dict):
        return

    for table_name, table_data in data.items():
        if isinstance(table_data, list) and len(table_data) > 0 and isinstance(table_data[0], dict):
            # Dynamic table with rows
            ws = wb.create_sheet(title=_safe_name(table_name))
            _write_dynamic_table(ws, table_data)
        elif isinstance(table_data, dict):
            # Key-value data
            ws = wb.create_sheet(title=_safe_name(table_name))
            _write_kv_table(ws, table_data)


def _write_dynamic_table(ws, rows):
    """Write a list of row objects as a table with headers."""
    if not rows:
        return
    headers = list(rows[0].keys())
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
    for row in rows:
        ws.append([row.get(h, "") for h in headers])


def _write_kv_table(ws, data):
    """Write key-value pairs as a two-column table."""
    ws.append(["字段", "内容"])
    ws["A1"].font = Font(bold=True)
    ws["B1"].font = Font(bold=True)
    for key, value in data.items():
        if isinstance(value, list):
            value = "、".join(str(v) for v in value)
        elif isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False)
        ws.append([key, str(value) if value else ""])
    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 60


def _safe_name(name):
    """Sanitize sheet name (max 31 chars, no special chars)."""
    name = str(name)[:31]
    name = name.replace("/", "-").replace("\\", "-")
    return name
