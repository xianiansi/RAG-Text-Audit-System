import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
from PyQt5.QtGui import QPalette, QColor
from docx import Document
from paragraph_classification import doc_classification

class Window1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('审计文件模板要求上传')
        self.setGeometry(600, 250, 800, 400)  # x, y 横、竖

        # 主布局、第1行、第2行、第3行
        mainLy = QVBoxLayout()
        L1Layout = QHBoxLayout()
        L2Layout = QHBoxLayout()
        L3Layout = QHBoxLayout()

        # 第一行左边：上传文件按钮
        self.uploadButton = QPushButton('请上传文件模板', self)
        self.uploadButton.setFixedSize(300, 300)
        self.uploadButton.clicked.connect(self.uploadFile)
        L1Layout.addWidget(self.uploadButton)

        # 第一行右边是上下俩布局：多行文本编辑器和标签
        L1RLayout = QVBoxLayout()
        self.label = QLabel('其他审计要求', self)
        self.textEdit = QTextEdit(self)
        L1RLayout.addWidget(self.label)
        L1RLayout.addWidget(self.textEdit)
        L1Layout.addLayout(L1RLayout)

        # 第2行
        L2Layout.addStretch()
        self.uploadPendingButton = QPushButton('确定', self)
        self.uploadPendingButton.setFixedSize(300, 50)
        self.uploadPendingButton.clicked.connect(self.confirmUpload)
        L2Layout.addWidget(self.uploadPendingButton)
        L2Layout.addStretch()

        # 提示标签
        self.statusLabel = QLabel('', self)
        palette = self.statusLabel.palette()
        palette.setColor(QPalette.WindowText, QColor('red'))
        self.statusLabel.setPalette(palette)
        self.statusLabel.hide()  # 初始状态隐藏
        L2Layout.addWidget(self.statusLabel)

        # 第3行
        L3Layout.addStretch()
        self.nextButton = QPushButton('下一步', self)
        self.nextButton.setFixedSize(300, 50)
        self.nextButton.clicked.connect(self.openNextWindow)
        L3Layout.addWidget(self.nextButton)
        L3Layout.addStretch()

        # 添加到主布局，设置主布局
        mainLy.addLayout(L1Layout)
        mainLy.addLayout(L2Layout)
        mainLy.addLayout(L3Layout)
        self.setLayout(mainLy)

    def uploadFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, '上传Word模板', '', 'Word Files (*.docx)', options=options)
        if fileName:
            self.uploadButton.setText(fileName)
            self.fileName = fileName  # 保存文件路径
            self.processTemplate(fileName)  # 调用模板处理函数
            self.fileUploaded = True  # 记录文件已上传

    def confirmUpload(self):
        if hasattr(self, 'fileUploaded') and self.fileUploaded:
            self.readWordFile(self.fileName)
            self.statusLabel.setText('文件模板、其他审计要求已上传！')
            self.statusLabel.show()
        else:
            self.statusLabel.setText('请先上传文件模板和其他审计要求！')
            self.statusLabel.show()

    def processTemplate(self, filePath):
        # 识别模板每个段落的类别
        tpr = doc_classification(filePath)
        tpr.classified()

    def readWordFile(self, filePath):
        doc = Document(filePath)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        self.textEdit.setPlainText('\n'.join(fullText))  # 显示在文本编辑器里

    def openNextWindow(self):
        self.hide()  # 自己隐藏
        self.newWindow = Window2(self)  # 把上一级的窗口传进去
        self.newWindow.show()  # 显示窗口2

class Window2(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window  # 上一步窗口继承一下
        self.initUI()

    def initUI(self):
        self.setWindowTitle('审计文件')
        self.setGeometry(600, 250, 800, 400)  # x, y 横、竖

        # 主布局、第1行、第2行、第3行
        mainLy = QVBoxLayout()
        L1Layout = QHBoxLayout()
        L2Layout = QHBoxLayout()
        L3Layout = QHBoxLayout()

        # 第一行：上传文件按钮
        self.uploadButton = QPushButton('请上传待审计文件', self)
        self.uploadButton.setFixedSize(300, 300)
        self.uploadButton.clicked.connect(self.uploadFile)
        L1Layout.addWidget(self.uploadButton)

        # 第2行
        L2Layout.addStretch()
        self.generateReportButton = QPushButton('生成审计报告', self)
        self.generateReportButton.setFixedSize(300, 50)
        self.generateReportButton.clicked.connect(self.generateReport)
        L2Layout.addWidget(self.generateReportButton)
        L2Layout.addStretch()

        # 第3行
        L3Layout.addStretch()
        self.backButton = QPushButton('上一步', self)
        self.backButton.setFixedSize(300, 50)
        self.backButton.clicked.connect(self.backToParent)
        L3Layout.addWidget(self.backButton)
        L3Layout.addStretch()

        # 添加到主布局，设置主布局
        mainLy.addLayout(L1Layout)
        mainLy.addLayout(L2Layout)
        mainLy.addLayout(L3Layout)
        self.setLayout(mainLy)

    def uploadFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, '上传待审计文件', '', 'Word Files (*.docx)', options=options)
        if fileName:
            self.uploadButton.setText(fileName)
            self.fileName = fileName  # 保存文件路径
            self.fileUploaded = True  # 记录文件已上传

    def backToParent(self):
        self.close()    # 自己关掉
        self.parent_window.show() # 显示上一级

    def generateReport(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window1()
    ex.show()
    sys.exit(app.exec())
