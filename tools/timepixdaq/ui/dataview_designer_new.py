# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dataviewer_new.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1166, 801)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toa_view = PlotWidget(self.groupBox)
        self.toa_view.setObjectName("toa_view")
        self.verticalLayout.addWidget(self.toa_view)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sexposure = QtWidgets.QLineEdit(self.groupBox)
        self.sexposure.setObjectName("sexposure")
        self.horizontalLayout.addWidget(self.sexposure)
        self.exposure = QtWidgets.QLineEdit(self.groupBox)
        self.exposure.setObjectName("exposure")
        self.horizontalLayout.addWidget(self.exposure)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.bins = QtWidgets.QLineEdit(self.groupBox)
        self.bins.setObjectName("bins")
        self.horizontalLayout_2.addWidget(self.bins)
        self.reset_toa = QtWidgets.QPushButton(self.groupBox)
        self.reset_toa.setObjectName("reset_toa")
        self.horizontalLayout_2.addWidget(self.reset_toa)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.tot_view = ImageView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tot_view.sizePolicy().hasHeightForWidth())
        self.tot_view.setSizePolicy(sizePolicy)
        self.tot_view.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tot_view.setObjectName("tot_view")
        self.verticalLayout_3.addWidget(self.tot_view)
        self.verticalLayout_6.addLayout(self.verticalLayout_3)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.path_name = QtWidgets.QLineEdit(self.groupBox_3)
        self.path_name.setObjectName("path_name")
        self.horizontalLayout_4.addWidget(self.path_name)
        self.openpath = QtWidgets.QPushButton(self.groupBox_3)
        self.openpath.setObjectName("openpath")
        self.horizontalLayout_4.addWidget(self.openpath)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.file_prefix = QtWidgets.QLineEdit(self.groupBox_3)
        self.file_prefix.setObjectName("file_prefix")
        self.horizontalLayout_5.addWidget(self.file_prefix)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.startAcq = QtWidgets.QCheckBox(self.groupBox_3)
        self.startAcq.setObjectName("startAcq")
        self.verticalLayout_5.addWidget(self.startAcq)
        self.verticalLayout_6.addWidget(self.groupBox_3)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.viewer = ImageView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewer.sizePolicy().hasHeightForWidth())
        self.viewer.setSizePolicy(sizePolicy)
        self.viewer.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.viewer.setObjectName("viewer")
        self.verticalLayout_4.addWidget(self.viewer)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.live_viewer = ImageView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.live_viewer.sizePolicy().hasHeightForWidth())
        self.live_viewer.setSizePolicy(sizePolicy)
        self.live_viewer.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.live_viewer.setObjectName("live_viewer")
        self.verticalLayout_4.addWidget(self.live_viewer)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Time of Flight"))
        self.label.setText(_translate("Form", "Exposure"))
        self.label_2.setText(_translate("Form", "us"))
        self.label_3.setText(_translate("Form", "Bins"))
        self.reset_toa.setText(_translate("Form", "Reset"))
        self.groupBox_2.setTitle(_translate("Form", "Time over Threshold"))
        self.groupBox_3.setTitle(_translate("Form", "Acquisition"))
        self.label_6.setText(_translate("Form", "Path"))
        self.openpath.setText(_translate("Form", "Open"))
        self.label_7.setText(_translate("Form", "Prefix:"))
        self.file_prefix.setText(_translate("Form", "test_"))
        self.startAcq.setText(_translate("Form", "Store to File (Immediate)"))
        self.label_5.setText(_translate("Form", "Integrated"))
        self.label_4.setText(_translate("Form", "Live"))

from pyqtgraph import ImageView, PlotWidget