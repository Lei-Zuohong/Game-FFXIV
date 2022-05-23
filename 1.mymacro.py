# -*- coding: UTF-8 -*-
# Public package
import os
import re
import sys
import functools
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QPushButton, QLabel, QCheckBox, QTextEdit
# Private package
import headpy.hfile as hfile
# Internal package
import hgame.hnamazu as hnamazu

################################################################################
# 借用鲶鱼精邮差得到自己的宏输入软件
################################################################################
# 读取宏列表
config = hfile.config_read()
macro_folder = config['default']['macro_folder']
language = config['default']['language']
files = sorted(os.listdir(macro_folder))
mnames = []
mcommands = {}
for file in files:
    if(language == 'cn'):
        if(re.match(r'(.*)en(.*)', file)): continue
    if(language == 'en'):
        if(re.match(r'(.*)cn(.*)', file)): continue
    mname = re.match(r'(.*).txt', file).group(1)
    mnames.append(mname)
    mcommands[mname] = hfile.txt_readlines('%s/%s' % (macro_folder, file))
################################################################################
# 生成接口
namazu = hnamazu.NAMAZU()
################################################################################
# 生成窗口


class Example(QWidget):
    def __init__(self):
        super().__init__()
        # 数值初始化
        self.mnames = mnames
        self.mcommands = mcommands
        self.namazu = namazu
        self.runonclick = True
        self.onreview = ''
        # 窗口初始化
        self.setGeometry(1600, 100, 300, 900)
        self.setWindowTitle('Mymacro')
        # 主窗体
        self.vbox = QVBoxLayout()
        self.box_runonclick = QCheckBox(u"Run macro on click", self)
        self.box_runonclick.setChecked(True)
        self.box_runonclick.stateChanged.connect(self.box_runonclick_change)
        self.vbox.addWidget(self.box_runonclick)
        self.bottom_macro = {}
        for mname in self.mnames:
            self.bottom_macro[mname] = QPushButton(mname, self)
            self.bottom_macro[mname].clicked.connect(functools.partial(self.run_macro, mname))
            self.vbox.addWidget(self.bottom_macro[mname])
        self.vbox.addStretch(1)
        self.review = QTextEdit(u"empty", self)
        self.vbox.addWidget(self.review)
        # 展示
        self.setLayout(self.vbox)
        self.show()

    def box_runonclick_change(self):
        self.runonclick = self.box_runonclick.isChecked()

    def run_macro(self, mname):
        temp = ''
        for command in self.mcommands[mname]:
            temp += '%s\n' % (command)
        self.onreview = mname
        self.review.setPlainText(temp)
        if(self.box_runonclick.isChecked()):
            self.namazu.sends(self.mcommands[mname])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.setWindowOpacity(0.7)
    app.exit(app.exec_())
