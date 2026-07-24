"""
Word export: fill template.docx with project data using cell-by-cell replacement.

The frontend stores data with descriptive keys that may differ from Word placeholder suffixes.
This module handles the mapping to ensure correct replacement.
"""
import copy
import re
import os
from io import BytesIO
from docx import Document
from docx.shared import Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")


# ── Word table index → data key mapping ──
TABLE_MAP = {
    0:  {"section": 1, "key": "table_1-1",  "type": "form"},
    1:  {"section": 1, "key": "table_1-2",  "type": "form"},
    2:  {"section": 1, "key": "table_1-3",  "type": "table"},
    3:  {"section": 1, "key": "table_1-4",  "type": "form"},
    4:  {"section": 1, "key": "table_1-5",  "type": "table"},
    5:  {"section": 1, "key": "table_1-6",  "type": "table"},
    6:  {"section": 1, "key": "table_1-7",  "type": "table"},
    7:  {"section": 1, "key": "table_1-8",  "type": "table"},
    8:  {"section": 1, "key": "table_1-9",  "type": "table"},
    9:  {"section": 1, "key": "table_1-10", "type": "form"},
    10: {"section": 1, "key": "table_1-11", "type": "form"},
    11: {"section": 1, "key": "table_1-12", "type": "table"},
    12: {"section": 1, "key": "table_1-13", "type": "table"},
    13: {"section": 1, "key": "table_1-14", "type": "table"},
    14: {"section": 1, "key": "table_1-15", "type": "table"},
    15: {"section": 1, "key": "table_1-16", "type": "table"},
    16: {"section": 1, "key": "table_1-17", "type": "table"},
    17: {"section": 1, "key": "table_1-18a", "type": "checklist"},
    18: {"section": 1, "key": "table_1-18b", "type": "checklist"},
    19: {"section": 1, "key": "table_1-18c", "type": "checklist"},
    20: {"section": 1, "key": "table_1-18d", "type": "checklist"},
    21: {"section": 1, "key": "table_1-18e", "type": "checklist"},
    22: {"section": 1, "key": "table_1-18f", "type": "checklist"},
    23: {"section": 1, "key": "table_1-19", "type": "table"},
    24: {"section": 1, "key": "table_1-20", "type": "form"},
    25: {"section": 2, "key": "table_2-1",  "type": "form"},
    26: {"section": 2, "key": "table_2-2",  "type": "form"},
    27: {"section": 2, "key": "table_2-3",  "type": "checklist"},
    28: {"section": 3, "key": "table_3-1",  "type": "form"},
    29: {"section": 3, "key": "table_3-2",  "type": "form"},
    30: {"section": 3, "key": "table_3-3",  "type": "table"},
    31: {"section": 3, "key": "table_3-4",  "type": "table"},
    32: {"section": 3, "key": "table_3-5",  "type": "table"},
    33: {"section": 3, "key": "table_3-6",  "type": "table"},
    34: {"section": 3, "key": "table_3-7",  "type": "checklist"},
    35: {"section": 4, "key": "table_4-1",  "type": "form"},
    36: {"section": 4, "key": "table_4-2",  "type": "table"},
    37: {"section": 4, "key": "table_4-3",  "type": "checklist"},
    38: {"section": 5, "key": "table_5-1",  "type": "table"},
    39: {"section": 5, "key": "table_5-2",  "type": "table"},
    40: {"section": 5, "key": "table_5-3",  "type": "table"},
    41: {"section": 5, "key": "table_5-4",  "type": "checklist"},
    42: {"section": 6, "key": "table_6-1",  "type": "table"},
    43: {"section": 6, "key": "table_6-2",  "type": "table"},
    44: {"section": 6, "key": "table_6-3",  "type": "table"},
}


# ── Key mapping: frontend key → Word placeholder suffix ──
# Only needed for tables where keys differ
KEY_MAP = {
    "table_1-1": {
        "单位全称": "公司名称",
        "简称": "公司简称",
        "邮政编码": "邮编",
        "负责人电话": "电话1",
        "负责人传真": "传真1",
        "负责人所属部门": "所属部门1",
        "负责人电子邮件": "邮件1",
        "联系人电话": "电话2",
        "联系人传真": "传真2",
        "联系人所属部门": "所属部门2",
        "联系人电子邮件": "邮件2",
        # Checkbox options
        "党政机关": "党政机关",
        "国家重要行业、重要领域或重要企事业单位": "国家重要",
        "一般企事业单位": "一般单位",
        "其它类型": "其它类型",
    },
    "table_1-5": {
        "重要程度": "网络区域重要程度",
        "备注": "网络结构情况备注",
    },
}


def export_word(project) -> str:
    template_path = os.path.join(os.path.dirname(__file__), "..", "template.docx")
    output_path = f"/tmp/export_{project.id}.docx"
    doc = Document(template_path)

    for word_ti, table in enumerate(doc.tables):
        if word_ti not in TABLE_MAP:
            continue
        info = TABLE_MAP[word_ti]
        sec_num = info["section"]

        if sec_num >= 2 and not getattr(project, f"section{sec_num}_enabled"):
            continue

        sec_data = project.get_section_data(sec_num)
        table_data = sec_data.get(info["key"], {} if info["type"] == "form" else [])

        if info["type"] == "form":
            _fill_form_table(table, table_data, info["key"])
        elif info["type"] == "table":
            _fill_dynamic_table(table, table_data)
        elif info["type"] == "checklist":
            _fill_checklist_table(table, table_data)

    _replace_paragraphs(doc, project)
    doc.save(output_path)
    return output_path


def _lookup_value(placeholder_suffix, data, table_key):
    """Find a value in data dict matching the placeholder suffix.

    Strategy:
    1. Try exact key match in data
    2. Try key mapping for this table
    3. Try reverse key mapping (Word suffix → frontend key)
    4. Try partial match (data key contains suffix or vice versa)
    5. For checkbox values, search in array-typed fields
    """
    if not isinstance(data, dict):
        return None

    suffix = placeholder_suffix.strip()

    # 1. Exact match
    if suffix in data:
        val = data[suffix]
        if not isinstance(val, (list, dict)):
            return str(val)
        return val  # Return list for checkboxes

    # 2. Key mapping lookup (frontend key → Word key)
    mapping = KEY_MAP.get(table_key, {})
    for frontend_key, word_key in mapping.items():
        if word_key == suffix and frontend_key in data:
            val = data[frontend_key]
            if not isinstance(val, (list, dict)):
                return str(val)
            return val

    # 3. Search all values - try finding a key that matches
    for dk, dv in data.items():
        if isinstance(dv, (list, dict)):
            continue
        # Word suffix is longer and contains data key
        if dk in suffix or suffix in dk:
            return str(dv)

    # 4. For checkbox arrays, search in lists
    for dk, dv in data.items():
        if isinstance(dv, list):
            for item in dv:
                if isinstance(item, str) and (item in suffix or suffix in item):
                    return dv  # Return the list

    return None


def _collect_file_keys(data):
    """Collect keys whose values are file arrays [{url, filename, ...}]."""
    keys = set()
    if not isinstance(data, dict):
        return keys
    for k, v in data.items():
        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict) and 'url' in v[0]:
            keys.add(k)
    return keys


def _fill_form_table(table, data, table_key):
    """Fill a single-row form table by replacing all placeholders and inserting images.

    Handles both simple forms (flat data dict) and dynamic forms (data with formBlocks array).
    """
    if not isinstance(data, dict):
        data = {}

    # For dynamic forms, flatten formBlocks into a single merged dict for placeholder matching
    # (each block's file arrays are merged so images from all blocks get inserted)
    merged_data = dict(data)
    blocks = data.get('formBlocks')
    if isinstance(blocks, list) and len(blocks) > 0:
        merged_data = dict(data)
        # Merge all blocks - for non-file keys, last block wins; for file keys, merge all
        for k in merged_data.keys():
            if k == 'formBlocks':
                continue
        for block in blocks:
            if isinstance(block, dict):
                for bk, bv in block.items():
                    if bk in merged_data and isinstance(merged_data[bk], list) and isinstance(bv, list):
                        merged_data[bk] = merged_data[bk] + bv
                    else:
                        merged_data[bk] = bv

    # Identify file keys
    file_keys = _collect_file_keys(merged_data)

    # Insert images FIRST (before text replacement clears the placeholders)
    for file_key in file_keys:
        _insert_images_for_key(table, merged_data[file_key], file_key, table_key)

    # Then replace text placeholders (skipping file keys since images are already inserted)
    for row in table.rows:
        for cell in row.cells:
            _replace_cell_text(cell, merged_data, table_key, skip_keys=file_keys)


def _fill_dynamic_table(table, rows, table_key=""):
    """Fill a multi-row dynamic table using existing template rows first.

    Word template has N pre-built empty rows (header + N data rows with placeholders).
    Strategy: fill existing rows first, append new rows only when data exceeds template,
    and remove leftover template rows when data is fewer than template rows.
    """
    if not isinstance(rows, list):
        return
    if len(table.rows) < 2:
        return

    template_row = table.rows[1]  # First data row (index 0 is header)
    total_data_rows = len(rows)

    # Remove extra template rows if data has fewer rows
    existing_rows = len(table.rows) - 1  # Excluding header
    while existing_rows > total_data_rows:
        last_row_elem = table.rows[-1]._element
        table._tbl.remove(last_row_elem)
        existing_rows -= 1

    for i, row_data in enumerate(rows):
        if not isinstance(row_data, dict):
            continue
        if i < existing_rows:
            # Fill existing template row
            row = table.rows[i + 1]
        else:
            # Append new row from template
            new_row_elem = copy.deepcopy(template_row._element)
            table._tbl.append(new_row_elem)
            row = table.rows[-1]
        for cell in row.cells:
            _replace_cell_text(cell, row_data, table_key)


def _fill_checklist_table(table, rows, table_key=""):
    """Fill a checklist table using existing template rows first, append if needed."""
    if not isinstance(rows, list):
        return
    if len(table.rows) < 2:
        return

    template_row = table.rows[1]
    total_data_rows = len(rows)

    # Remove extra template rows if data has fewer rows
    existing_rows = len(table.rows) - 1
    while existing_rows > total_data_rows:
        last_row_elem = table.rows[-1]._element
        table._tbl.remove(last_row_elem)
        existing_rows -= 1

    for i, row_data in enumerate(rows):
        if not isinstance(row_data, dict):
            continue
        if i < existing_rows:
            row = table.rows[i + 1]
        else:
            new_row_elem = copy.deepcopy(template_row._element)
            table._tbl.append(new_row_elem)
            row = table.rows[-1]
        for cell in row.cells:
            _replace_cell_text(cell, row_data, table_key)


def _replace_cell_text(cell, data, table_key="", skip_keys=None):
    """Replace all placeholders in a cell with values from data dict.

    Args:
        skip_keys: set of data keys to skip (file/image fields handled separately)
    """
    if skip_keys is None:
        skip_keys = set()

    full_text = cell.text
    if not full_text or '待' not in full_text:
        return

    # Find all placeholder patterns
    pattern = r'(待输入内容B_\S+|待输入数据B_\S+|待勾选_\S+)'
    matches = list(re.finditer(pattern, full_text))
    if not matches:
        return

    # Determine which placeholders belong to file keys and should be skipped
    skip_placeholders = set()
    if skip_keys:
        mapping = KEY_MAP.get(table_key, {})
        for match in matches:
            placeholder = match.group(0)
            suffix = placeholder[7:] if not placeholder.startswith('待勾选_') else placeholder[4:]
            if suffix in skip_keys:
                skip_placeholders.add(placeholder)
            for fk, wk in mapping.items():
                if wk == suffix and fk in skip_keys:
                    skip_placeholders.add(placeholder)

    # Build replacement by splitting at match positions (forward order)
    parts = []
    last_end = 0
    for match in matches:
        parts.append(full_text[last_end:match.start()])
        placeholder = match.group(0)

        if placeholder in skip_placeholders:
            parts.append('')
        elif placeholder.startswith('待勾选_'):
            suffix = placeholder[4:]
            result = _lookup_value(suffix, data, table_key)
            if isinstance(result, list):
                selected = any(sv in suffix for sv in result)
                mark = '☑' if selected else '☐'
            else:
                mark = '☐'
            parts.append(mark + suffix)
        else:
            suffix = placeholder[7:]  # Remove 待输入内容B_ or 待输入数据B_
            value = _lookup_value(suffix, data, table_key)
            parts.append(str(value) if isinstance(value, str) else '')

        last_end = match.end()
    parts.append(full_text[last_end:])
    new_text = ''.join(parts)

    # Apply the new text to the cell
    if new_text != full_text:
        first_para = cell.paragraphs[0] if cell.paragraphs else None
        if first_para:
            if first_para.runs:
                for run in first_para.runs:
                    run.text = ''
                first_para.runs[0].text = new_text
            else:
                first_para.add_run(new_text)


def _insert_images_for_key(table, files, file_key, table_key=""):
    """Insert uploaded images into cells containing the placeholder for file_key."""
    if not files:
        return

    # Build the Word placeholder suffix to search for
    mapping = KEY_MAP.get(table_key, {})
    word_suffix = file_key
    for frontend_key, word_key in mapping.items():
        if frontend_key == file_key:
            word_suffix = word_key
            break

    pattern = re.compile(r'待输入(内容|数据)B_' + re.escape(word_suffix))

    for row in table.rows:
        for cell in row.cells:
            text = cell.text
            if not pattern.search(text):
                continue

            # Clear the cell
            for para in cell.paragraphs:
                for run in para.runs:
                    run.text = ''

            # Insert each image
            for i, f in enumerate(files):
                url = f.get('url', '')
                filename = f.get('filename', '')
                if not url:
                    continue

                # Determine local file path
                if url.startswith('/api/uploads/'):
                    local_name = url.replace('/api/uploads/', '')
                    local_path = os.path.join(UPLOAD_DIR, local_name)
                elif url.startswith('/uploads/'):
                    local_name = url.replace('/uploads/', '')
                    local_path = os.path.join(UPLOAD_DIR, local_name)
                else:
                    local_path = url

                ext = os.path.splitext(filename or url)[1].lower()
                is_image = ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp')

                para = cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()
                if is_image and os.path.exists(local_path):
                    try:
                        para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        run = para.add_run()
                        run.add_picture(local_path, width=Cm(12))
                        if i < len(files) - 1:
                            para.add_run('\n')
                    except Exception:
                        para.add_run(f'[{filename}]')
                else:
                    para.add_run(f'[{filename or "附件"}]')


def _replace_paragraphs(doc, project):
    """Replace header placeholders in document paragraphs."""
    sec1 = project.get_section_data(1)
    t11 = sec1.get('table_1-1', {}) if isinstance(sec1, dict) else {}
    t12 = sec1.get('table_1-2', {}) if isinstance(sec1, dict) else {}

    def g(d, k, default=''):
        return d.get(k, default) if isinstance(d, dict) else default

    reps = {
        '待输入内容B_公司名称': g(t11, '单位全称', project.company_name),
        '待输入内容B_系统名称': g(t12, '等级保护对象名称', project.system_name),
        '待输入内容B_日期': '',
    }

    for para in doc.paragraphs:
        text = para.text
        for old, new in reps.items():
            if old in text:
                text = text.replace(old, str(new) if new else '')
        if para.runs and text != para.text:
            para.runs[0].text = text
            for run in para.runs[1:]:
                run.text = ''
