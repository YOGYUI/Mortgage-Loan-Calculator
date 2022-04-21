if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QCoreApplication
    from Include import MortgageLoanCalculatorWindow

    QApplication.setStyle('fusion')
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MortgageLoanCalculatorWindow()
    window.show()
    app.exec_()
