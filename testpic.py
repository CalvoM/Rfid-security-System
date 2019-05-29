from ImageDisplay import ImageDisplay
from PyQt4.QtGui import QApplication
import sys
app=QApplication(sys.argv)
win=ImageDisplay('TrialOne.jpg')
sys.exit(app.exec_())

