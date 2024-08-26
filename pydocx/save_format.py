from docx import Document
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING
import json

# 加载模板文档，读取格式信息
doc_path = r'./file)save/Appendix2 muban.docx'
doc = Document(doc_path)


doc_format = {
    "main_text": {},  # 报告正文:“1.5倍行距”，中文“宋体 小四”，数字“Times New Roman 小四”，标点符号均为“中文输入法全角”，首行空两格；
    "appendix_table": {},  # 报告附表“1倍行距”，中文“楷体 五号”，数字“Times New Roman 五号”，标点符号均为“中文输入法全角”，数字保留2位或4位小数;
    "title": {},  # 报告标题“宋体二号 加粗 居中”；
    "doc_number": {},  # 报告文号“黑体 小四 居中”
    "sub_title": {},  # 报告小标题“黑体 三号 居中”；
    "report_subject": {},  # 报告对象“宋体 四号”；
    "level1_heading": {},  # 一级标题“黑体 小四”
    "level2_heading": {},  # 二级标题“宋体 小四 加粗”
    "level3_heading": {},  # 三级标题“宋体 小四”
}

# 函数：提取段落格式信息
def extract_format(para):
    format_info = {}
    # 字体名称
    if para.runs:
        run = para.runs[0]
        if run.font.name:
            format_info['font_name'] = run.font.name
        elif run.font.element.rPr.rFonts is not None:
            rFonts = run.font.element.rPr.rFonts
            if qn('w:eastAsia') in rFonts.attrib:
                format_info['font_name'] = rFonts.attrib[qn('w:eastAsia')]
            elif qn('w:ascii') in rFonts.attrib:
                format_info['font_name'] = rFonts.attrib[qn('w:ascii')]
            elif qn('w:hAnsi') in rFonts.attrib:
                format_info['font_name'] = rFonts.attrib[qn('w:hAnsi')]
        # 字体大小
        if run.font.size:
            format_info['font_size'] = run.font.size.pt
    # 行间距
    if para.paragraph_format.line_spacing:
        if para.paragraph_format.line_spacing_rule == WD_LINE_SPACING.AT_LEAST:
            format_info['line_spacing'] = para.paragraph_format.line_spacing.pt
        elif para.paragraph_format.line_spacing_rule == WD_LINE_SPACING.EXACTLY:
            format_info['line_spacing'] = para.paragraph_format.line_spacing.pt
        elif para.paragraph_format.line_spacing_rule == WD_LINE_SPACING.MULTIPLE:
            format_info['line_spacing'] = para.paragraph_format.line_spacing
    # 对齐方式
    if para.alignment:
        if para.alignment == WD_PARAGRAPH_ALIGNMENT.LEFT:
            format_info['alignment'] = 'left'
        elif para.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            format_info['alignment'] = 'center'
        elif para.alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT:
            format_info['alignment'] = 'right'
        elif para.alignment == WD_PARAGRAPH_ALIGNMENT.JUSTIFY:
            format_info['alignment'] = 'justify'
    return format_info

# 提取文档中的格式信息
for para in doc.paragraphs:
    # 标题
    if para.style.name == 'Title':
        doc_format['title'] = extract_format(para)
    # 一级标题
    elif para.style.name == 'Heading 1':
        doc_format['level1_heading'] = extract_format(para)
    # 二级标题
    elif para.style.name == 'Heading 2':
        doc_format['level2_heading'] = extract_format(para)
    # 段落
    elif para.style.name == 'Normal':
        doc_format['paragraph'] = extract_format(para)

# 保存格式信息到本地文件
output_path = 'document_format.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(doc_format, f, ensure_ascii=False, indent=4)

print(f"文档格式信息已保存到 {output_path}")
