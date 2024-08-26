from docx import Document
import re
import json
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_LINE_SPACING

# 对于模板：先识别段落类型，后把每个段落的格式要求存储到json文件中
# 对于文件：先识别段落类型，后把每个段落的格式与json文件中的格式进行匹配

# 函数：根据段落内容来识别段落类型
def classify_paragraph(doc,para):
    text = para.text.strip()

    # 跳过空段落
    if not text:
        return None

    # 如果已进入附表部分，所有内容都归类为附表
    if doc.is_appendix:
        return "appendix_table"

    # 检查是否为"附表"
    if text == "附件":
        doc.is_appendix = True
        return "appendix_table"

    # 标题部分识别
    if text in doc.title_parts:
        return "title"

    # 文号
    elif re.match(r"稽审任字[^\s]+号", text):
        return "doc_number"

    # 小标题识别
    elif re.match(r"^.{3,15}营业部$", text):
        return "sub_title"
    elif re.match(r"^原负责人.{2,4}同志离任审计报告$", text):
        return "sub_title"
    elif re.match(r"^负责人.{2,4}同志离岗审计报告$", text):
        return "sub_title"

    # 报告对象识别
    elif text == "董事长、总审计师、党委组织部-人力资源部：":
        return "report_subject"

    # 一级标题
    elif re.match(r"^[一二三四五六七八九十]+、", text):
        return "level1_heading"

    # 二级标题
    elif re.match(r"^（[一二三四五六七八九十]+）", text):
        return "level2_heading"

    # 三级标题
    elif re.match(r"^[1-9][0-9]*、", text):
        return "level3_heading"

    # 其他为正文
    else:
        return "main_text"


def extract_format(para, para_type):
    para_format = {}

    # 默认字体信息
    font_name_CN = None
    font_name_num = None

    # 遍历段落的每个 run
    for run in para.runs:
        if run.text.strip():  # 检查 run 中是否有非空白字符
            # 判断字符是否为中文
            if any('\u4e00' <= char <= '\u9fff' for char in run.text):
                font_name_CN = run.font.name
            # 判断字符是否为英文或数字
            elif any('A' <= char <= 'Z' or 'a' <= char <= 'z' or '0' <= char <= '9' for char in run.text):
                font_name_num = run.font.name

    # 如果未找到字体，尝试使用段落样式的字体
    if not font_name_CN:
        font_name_CN = para.style.font.name if para.style.font.name else '宋体'  # 使用段落样式的字体作为备选
    if not font_name_num:
        font_name_num = para.style.font.name if para.style.font.name else 'Times New Roman'

    # 对于所有字符的字体样式进行综合处理
    para_format['font_name_CN'] = font_name_CN
    para_format['font_name_num'] = font_name_num
    para_format['font_size'] = para.runs[0].font.size if para.runs else para.style.font.size
    para_format['line_spacing'] = para.paragraph_format.line_spacing
    para_format['first_line_indent'] = para.paragraph_format.first_line_indent
    para_format['alignment'] = para.alignment

    return para_format



class doc_classification():
    def __init__(self,doc_path):
        # doc_path = r'./file)save/Appendix2 muban.docx'
        self.doc = Document(doc_path)   # 加载模板文档
        self.section_format={}          # 初始化分类字典
        self.title_parts = ["国泰君安证券股份有限公司", "审计报告书"]  # 标题检查列表
        self.is_appendix = False        # 标志位：标识是否进入附表部分


    # 遍历文档中的每个段落，分类并填入记录类别的格式
    def classified(self):
        for para in self.doc.paragraphs:
            para_type = classify_paragraph(self,para)
            print(para.text)
            print(para_type)
            if para_type:  # 跳过空段落
                format = extract_format(para,para_type)
                print(format)
                self.section_format[para_type] = format

        # 打印分类识别结果（可根据需要保存到文件）
        for para_type, format in self.section_format.items():
            print(f"\n{para_type} 格式:")
            for fmt in format:
                print(f"- {fmt}")
        output_path = 'document_sections.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.section_format, f, ensure_ascii=False, indent=4)

        print(f"文档段落格式已保存到 {output_path}")
        # return self.section_format

        # self.doc_sections[para_type].append(para.text)

        # # 打印分类结果（可根据需要保存到文件）
        # for section, paragraphs in self.doc_sections.items():
        #     print(f"\n{section} 段落:")
        #     for p in paragraphs:
        #         print(f"- {p}")

        # # 保存分类信息到文件（可选）
        # output_path = 'document_sections.json'
        # with open(output_path, 'w', encoding='utf-8') as f:
        #     json.dump(self.doc_sections, f, ensure_ascii=False, indent=4)
        #
        # print(f"文档段落信息已保存到 {output_path}")



#
# doc_format = {
#         "main_text": {},  # 报告正文:“1.5倍行距”，中文“宋体 小四”，数字“Times New Roman 小四”，标点符号均为“中文输入法全角”，首行空两格；
#         "appendix_table": {},  # 报告附表“1倍行距”，中文“楷体 五号”，数字“Times New Roman 五号”，标点符号均为“中文输入法全角”，数字保留2位或4位小数;
#         "title": {},  # 报告标题“宋体二号 加粗 居中”；
#         "doc_number": {},  # 报告文号“黑体 小四 居中”
#         "sub_title": {},  # 报告小标题“黑体 三号 居中”；
#         "report_subject": {},  # 报告对象“宋体 四号”；
#         "level1_heading": {},  # 一级标题“黑体 小四”
#         "level2_heading": {},  # 二级标题“宋体 小四 加粗”
#         "level3_heading": {},  # 三级标题“宋体 小四”
#     }


# para_format = {             # 存储该段落的字体，字号、行距等信息
#         "font_name_CN":None,
#         "font_name_num": None,
#         "font_size": None,
#         "line_spacing": None,
#         "head_space": None,
#         "alignment": None,
#         "num_reversed": None,
#     }
#     if para_type == "main_text":
#         formats = {}
#     elif para_type == "appendix_table":
#         formats = {}
#     elif para_type == "title":
#         formats = {}
#     elif para_type == "doc_number":
#         formats = {}
#     elif para_type == "sub_title":
#         formats = {}
#     elif para_type == "report_subject":
#         formats = {}
#     elif para_type == "level1_heading":
#         formats = {}
#     elif para_type == "level2_heading":
#         formats = {}
#     elif para_type == "level3_heading":
#         formats = {}



# self.doc_sections = {
#             "title": [],
#             "doc_number": [],
#             "sub_title": [],
#             "report_subject":[],
#             "level1_heading": [],
#             "level2_heading": [],
#             "level3_heading": [],
#             "main_text": [],
#             "appendix_table": []
#         }