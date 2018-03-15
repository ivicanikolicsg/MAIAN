# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

try:
    import PyQt5
except:
    print("\033[91m[-] Python module PyQt5 is missing.\033[0m Please install it (on Ubuntu: sudo apt install python-pyqt5)")
    exit(1)


from PyQt5 import QtCore, QtGui, QtWidgets
from Queue import Queue
import sys
import subprocess
import threading
import platform
import re
import maian
import blockchain


class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

class MyReceiver(QtCore.QObject):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self,queue,*args,**kwargs):
        QtCore.QObject.__init__(self,*args,**kwargs)
        self.queue = queue

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)   




class LongRunningThing(QtCore.QObject):

    def __init__(self, myvar, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.notifyProgress = QtCore.pyqtSignal(int)
        self.l = myvar

    @QtCore.pyqtSlot()
    def run(self):
        for el in self.l:
            maian.main(el)


dfont = "Linux Biolinum O"
if platform.dist()[0] == 'Ubuntu':
    dfont = "Ubuntu Condensed"


class Ui_MAIAN(object):
    def setupUi(self, MAIAN):
        MAIAN.setObjectName("MAIAN")
        MAIAN.resize(950, 821)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MAIAN.sizePolicy().hasHeightForWidth())
        MAIAN.setSizePolicy(sizePolicy)
        MAIAN.setMinimumSize(QtCore.QSize(950, 815))
        MAIAN.setMaximumSize(QtCore.QSize(950, 815))
        font = QtGui.QFont()
        font.setFamily("Liberation Sans")
        font.setPointSize(10)
        MAIAN.setFont(font)
        self.groupBox = QtWidgets.QGroupBox(MAIAN)
        self.groupBox.setGeometry(QtCore.QRect(10, 640, 431, 111))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.lineMaxFuncInv = QtWidgets.QLineEdit(self.groupBox)
        self.lineMaxFuncInv.setGeometry(QtCore.QRect(330, 30, 91, 27))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineMaxFuncInv.setFont(font)
        self.lineMaxFuncInv.setFrame(False)
        self.lineMaxFuncInv.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineMaxFuncInv.setObjectName("lineMaxFuncInv")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 40, 221, 20))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 80, 171, 17))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineSolverTimeout = QtWidgets.QLineEdit(self.groupBox)
        self.lineSolverTimeout.setGeometry(QtCore.QRect(330, 70, 91, 27))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineSolverTimeout.setFont(font)
        self.lineSolverTimeout.setFrame(False)
        self.lineSolverTimeout.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineSolverTimeout.setObjectName("lineSolverTimeout")
        self.lineMaxFuncInv.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.lineSolverTimeout.raise_()
        self.groupBox_2 = QtWidgets.QGroupBox(MAIAN)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 431, 621))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.txtSolidity = QtWidgets.QTextEdit(self.groupBox_2)
        self.txtSolidity.setGeometry(QtCore.QRect(20, 130, 391, 471))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txtSolidity.setFont(font)
        self.txtSolidity.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.txtSolidity.setFrameShadow(QtWidgets.QFrame.Plain)
        self.txtSolidity.setAcceptRichText(False)
        self.txtSolidity.setObjectName("txtSolidity")
        self.radioSolidity = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioSolidity.setGeometry(QtCore.QRect(20, 30, 191, 22))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.radioSolidity.setFont(font)
        self.radioSolidity.setChecked(True)
        self.radioSolidity.setObjectName("radioSolidity")
        self.radioBytecodecompiled = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioBytecodecompiled.setGeometry(QtCore.QRect(20, 90, 171, 22))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.radioBytecodecompiled.setFont(font)
        self.radioBytecodecompiled.setObjectName("radioBytecodecompiled")
        self.radioBytecode = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioBytecode.setGeometry(QtCore.QRect(20, 60, 311, 22))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.radioBytecode.setFont(font)
        self.radioBytecode.setObjectName("radioBytecode")
        self.lineSolidityName = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineSolidityName.setGeometry(QtCore.QRect(300, 30, 113, 21))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineSolidityName.setFont(font)
        self.lineSolidityName.setFrame(False)
        self.lineSolidityName.setObjectName("lineSolidityName")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(210, 30, 91, 20))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.groupBox_3 = QtWidgets.QGroupBox(MAIAN)
        self.groupBox_3.setGeometry(QtCore.QRect(450, 10, 491, 741))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.txtLog = QtWidgets.QTextEdit(self.groupBox_3)
        self.txtLog.setGeometry(QtCore.QRect(20, 420, 451, 301))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txtLog.setFont(font)
        self.txtLog.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.txtLog.setFrameShadow(QtWidgets.QFrame.Plain)
        self.txtLog.setAcceptRichText(False)
        self.txtLog.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.txtLog.setObjectName("txtLog")
        self.pushStart = QtWidgets.QPushButton(self.groupBox_3)
        self.pushStart.setGeometry(QtCore.QRect(240, 30, 231, 91))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushStart.setFont(font)
        self.pushStart.setObjectName("pushStart")
        self.checkGreedy = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkGreedy.setGeometry(QtCore.QRect(20, 90, 151, 22))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkGreedy.setFont(font)
        self.checkGreedy.setChecked(True)
        self.checkGreedy.setObjectName("checkGreedy")
        self.checkSuicidal = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkSuicidal.setGeometry(QtCore.QRect(20, 60, 151, 22))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkSuicidal.setFont(font)
        self.checkSuicidal.setChecked(True)
        self.checkSuicidal.setObjectName("checkSuicidal")
        self.checkProdigal = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkProdigal.setGeometry(QtCore.QRect(20, 30, 171, 22))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.checkProdigal.setFont(font)
        self.checkProdigal.setChecked(True)
        self.checkProdigal.setObjectName("checkProdigal")
        self.txtResults = QtWidgets.QTextEdit(self.groupBox_3)
        self.txtResults.setGeometry(QtCore.QRect(20, 130, 451, 271))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.txtResults.setFont(font)
        self.txtResults.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.txtResults.setFrameShadow(QtWidgets.QFrame.Plain)
        self.txtResults.setAcceptRichText(False)
        self.txtResults.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.txtResults.setObjectName("txtResults")
        self.groupBox_4 = QtWidgets.QGroupBox(MAIAN)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 760, 931, 51))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.lineSolidityName_2 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineSolidityName_2.setGeometry(QtCore.QRect(10, 10, 951, 21))
        font = QtGui.QFont()
        font.setFamily(dfont)
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lineSolidityName_2.setFont(font)
        self.lineSolidityName_2.setAutoFillBackground(False)
        self.lineSolidityName_2.setStyleSheet("background-color:transparent;\n"
"")
        self.lineSolidityName_2.setFrame(False)
        self.lineSolidityName_2.setReadOnly(True)
        self.lineSolidityName_2.setObjectName("lineSolidityName_2")

        self.retranslateUi(MAIAN)
        QtCore.QMetaObject.connectSlotsByName(MAIAN)

        self.pushStart.clicked.connect(self.start_thread)
        self.txtLog.textChanged.connect(self.changed_log)
        self.txtSolidity.textChanged.connect(self.changed_source)

        self.last_pos = 0  
        self.locked_text = False


    @QtCore.pyqtSlot(str)
    def changed_source(self):

        tx = self.txtSolidity.toPlainText()
        pt = '^[0-9A-Fa-fx ]+$'
        remat = re.match(pt,tx)
        if remat is None and tx.find('contract') >= 0:
            self.radioSolidity.setChecked(True)
            ml = re.findall('contract[ |\t|\n]*[a-zA-Z0-9_]*', tx)
            if len(ml) == 0:
                pass
            elif len(ml) == 1:
                cnam = re.sub('contract[ |\t|\n]*','',ml[0])
                self.lineSolidityName.setText(cnam)
            else:
                pass
        elif remat is not None:
            if len(re.findall('60606040', tx)) > 1:
                self.radioBytecode.setChecked(True)
            else:
                self.radioBytecodecompiled.setChecked(True)



    @QtCore.pyqtSlot(str)
    def changed_log(self):

        if self.locked_text:  return


        self.locked_text = True

        tx = self.txtLog.toPlainText()
        trl = ['0','1','91','92','93','94']
        for tz in trl:
            tx = tx.replace('\033['+tz+'m','')
            tx = tx.replace('['+tz+'m','')

        self.txtLog.setText(tx)

        cursor = self.txtLog.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        self.txtLog.setTextCursor(cursor)

        self.locked_text = False


        

        t = ''
        vp = vs = vg = False

        if self.txtLog.toPlainText().find('Check if contract is PRODIGAL') >= 0:
            t += '<strong>Check on PRODIGAL </strong> <br />'
        if self.txtLog.toPlainText().find('The code does not have CALL/SUICIDE,') >= 0:
            t += '<font color="green">Not vulnerable</font><br />'
        if self.txtLog.toPlainText().find('Leak vulnerability found') >= 0:
            t += '<font color="red">Vulnerability found</font><br />'
            vp = True
        if self.txtLog.toPlainText().find('Confirmed ! The contract is prodigal') >= 0:
            t += '<font color="red">Vulnerability confirmed</font><br />'
        if self.txtLog.toPlainText().find('Cannot confirm the leak vulnerability') >= 0:
            t += '<font color="blue">Cannot confirm the vulnerability</font><br />'
        if self.txtLog.toPlainText().find('Cannot confirm the bug because the contract is not deployed on the blockchain') >= 0:
            t += '<font color="blue">Cannot confirm because there is no source code</font><br />'
        if self.txtLog.toPlainText().find('No prodigal vulnerability found') >= 0:
            t += '<font color="green">Not vulnerable</font>'
        if vp:
            t += '(see the log below)<br />'


        if len(t) > 0: 
            t += "<br />"
        if self.txtLog.toPlainText().find('Check if contract is SUICIDAL') >= 0:
            t += '<strong>Check on SUICIDAL  </strong><br /> '
        if self.txtLog.toPlainText().find('Suicidal vulnerability found') >= 0:
            t += '<font color="red">Vulnerability found</font><br />'
            vs = True
        if self.txtLog.toPlainText().find('Confirmed ! The contract is suicidal') >= 0:
            t += '<font color="red">Vulnerability confirmed</font><br />'
        if self.txtLog.toPlainText().find('Cannot confirm the suicide vulnerability') >= 0:
            t += '<font color="blue">Cannot confirm the vulnerability</font><br />'
        if self.txtLog.toPlainText().find('The code does not contain SUICIDE instructions, hence it is not vulnerable') >= 0:
            t += '<font color="green">Not vulnerable</font>'
        if self.txtLog.toPlainText().find('No suicidal vulnerability found') >= 0:
            t += '<font color="green">Not vulnerable</font>'
        if vs:
            t += '(see the log below)<br />'


        if len(t) > 0: 
            t += "<br />"
        if self.txtLog.toPlainText().find('Check if contract is GREEDY') >= 0:
            t += '<strong>Check on GREEDY  </strong><br /> '
        if self.txtLog.toPlainText().find('No lock vulnerability found because the contract cannot receive Ether') >= 0:
            t += '<font color="green">Not vulnerable</font>'
        if self.txtLog.toPlainText().find('No locking vulnerability found') >= 0:
            t += '<font color="green">Not vulnerable</font>'
        if self.txtLog.toPlainText().find('The code does not have CALL/SUICIDE/DELEGATECALL/CALLCODE') >= 0:
            t += '<font color="red">Vulnerability found</font><br />'
            vg = True           
        if self.txtLog.toPlainText().find('Locking vulnerability found') >= 0:
            t += '<font color="red">Vulnerability found</font><br />'
            vg = True     
        

        self.txtResults.setHtml(t)


    @QtCore.pyqtSlot(str)
    def append_text(self,text):
        self.txtLog.insertPlainText( text )


    @QtCore.pyqtSlot()
    def start_thread(self):
        self.txtLog.clear()
        self.txtResults.clear()


        contract = self.txtSolidity.toPlainText()

        with open('out/lastcontract','w') as f:
            f.write(contract.encode('utf-8'))
            f.close()

        if self.radioBytecode.isChecked():
            type_of_contract = ['--bytecode_source','out/lastcontract']
            pt = '^[0-9A-Fa-fx ]+$'
            result = re.match(pt, self.txtSolidity.toPlainText())
            if result is None:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Something went wrong")
                msg.setText("The provided code is not bytecode.")
                msg.exec_()
                return

        elif self.radioBytecodecompiled.isChecked():
            type_of_contract = ['--bytecode','out/lastcontract']
            pt = '^[0-9A-Fa-fx ]+$'
            result = re.match(pt, self.txtSolidity.toPlainText())
            if result is None:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Something went wrong")
                msg.setText("The provided code is not bytecode.")
                msg.exec_()
                return
                
        elif self.radioSolidity.isChecked():
            conname = self.lineSolidityName.text()
            if len(conname) == 0:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Something went wrong")
                msg.setText("If the type of source code is Solidity, then you need to specify the main contract name.")
                msg.exec_()
                return
            if self.txtSolidity.toPlainText().find(conname) < 0:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Something went wrong")
                msg.setText("Contract '"+conname+"' does not exist in the Solidity code.")
                msg.exec_()
                return

            type_of_contract = ['--soliditycode','out/lastcontract',conname]

        max_inv = ['--max_inv',self.lineMaxFuncInv.text()]
        stimout = ['--solve_timeout',self.lineSolverTimeout.text()]
        perform_checks = []
        if self.checkProdigal.isChecked():
            perform_checks.append( type_of_contract + max_inv + stimout + ['--check','1'] )
        if self.checkSuicidal.isChecked():
            perform_checks.append( type_of_contract + max_inv + stimout + ['--check','0'] )
        if self.checkGreedy.isChecked():
            perform_checks.append( type_of_contract + max_inv + stimout + ['--check','2'] )


        self.thread = QtCore.QThread()
        self.long_running_thing = LongRunningThing(perform_checks)
        self.long_running_thing.moveToThread(self.thread)
        self.thread.started.connect(self.long_running_thing.run)
        self.thread.start()       



    def retranslateUi(self, MAIAN):
            _translate = QtCore.QCoreApplication.translate
            MAIAN.setWindowTitle(_translate("MAIAN", "MAIAN v1.0"))
            self.groupBox.setTitle(_translate("MAIAN", "Settings"))
            self.lineMaxFuncInv.setText(_translate("MAIAN", "3"))
            self.label_4.setText(_translate("MAIAN", "Max function invocations"))
            self.label_5.setText(_translate("MAIAN", "Solver timeout (msec)"))
            self.lineSolverTimeout.setText(_translate("MAIAN", "10000"))
            self.groupBox_2.setToolTip(_translate("MAIAN", "The name of the main contract"))
            self.groupBox_2.setTitle(_translate("MAIAN", "Type of contract code"))
            self.txtSolidity.setProperty("placeholderText", _translate("MAIAN", "Put your code here. Usually, the type is recognized automatically."))
            self.radioSolidity.setText(_translate("MAIAN", "Solidity source code"))
            self.radioBytecodecompiled.setText(_translate("MAIAN", "Bytecode compiled"))
            self.radioBytecode.setText(_translate("MAIAN", "Bytecode source"))
            self.lineSolidityName.setPlaceholderText(_translate("MAIAN", "Main contract name"))
            self.label_6.setText(_translate("MAIAN", "Contract name"))
            self.groupBox_3.setTitle(_translate("MAIAN", "Run"))
            self.txtLog.setProperty("placeholderText", _translate("MAIAN", "Log will appear here"))
            self.pushStart.setText(_translate("MAIAN", "START"))
            self.checkGreedy.setText(_translate("MAIAN", "Check on Greedy"))
            self.checkSuicidal.setText(_translate("MAIAN", "Check on Suicidal"))
            self.checkProdigal.setText(_translate("MAIAN", "Check on Prodigal"))
            self.txtResults.setHtml(_translate("MAIAN", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "</style></head><body style=\" font-family:\'Linux Biolinum O\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Geneva\'; font-size:10pt;\"><br /></p></body></html>"))
            self.txtResults.setProperty("placeholderText", _translate("MAIAN", "Main results will appear here"))
            self.lineSolidityName_2.setText(_translate("MAIAN", "To keep MAIAN free and up to date, consider donating Ether to our account: 0xfd03b29b5c20f878836a3b35718351adf24f4a06"))






def cev():
    blockchain.kill_active_blockchain()
    sys.exit(0)


if __name__ == "__main__":


    queue = Queue()
    sys.stdout = WriteStream(queue)


    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(cev)


    MAIAN = QtWidgets.QWidget()
    ui = Ui_MAIAN()
    ui.setupUi(MAIAN)
    MAIAN.show()

    thread = QtCore.QThread()
    my_receiver = MyReceiver(queue)
    my_receiver.mysignal.connect(ui.append_text)
    my_receiver.moveToThread(thread)
    thread.started.connect(my_receiver.run)
    thread.start()    


    sys.exit(app.exec_())

