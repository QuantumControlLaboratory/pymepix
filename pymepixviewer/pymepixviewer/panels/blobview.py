
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from .ui.blobviewui import Ui_Form
from ..core.datatypes import ViewerMode
import threading
import numpy as np
from collections import deque
class BlobView(QtGui.QWidget,Ui_Form):

    def __init__(self,parent=None,start=None,end=None,current_mode=ViewerMode.TOA):
        super(BlobView, self).__init__(parent)

        # Set up the user interface from Designer.
        self.setupUi(self)  

        self._start_tof = start
        self._end_tof = end

        self._int_blob_count = 0


        self._current_mode = current_mode

        self._matrix = np.ndarray(shape=(256,256),dtype=np.float)
        self._matrix[...]=0.0

        self._blob_trend = deque(maxlen=100)#np.ndarray(shape=(400,),dtype=np.float)
        #self._blob_trend[...]=0.0
        #self._blob_trend_trigger = np.ndarray(shape=(400,),dtype=np.int)
        #self._blob_trend_trigger[...]=0
        self._blob_trend_trigger = deque(maxlen=100)
        self._blob_trend_data = pg.PlotDataItem()
        self.blob_trend.addItem(self._blob_trend_data)
        self.blob_trend.setLabel('left',text='Blob Count')
        self.blob_trend.setLabel('bottom',text='Trigger Number')
        self._last_trigger = 0

        self._histogram_mode = False
        self._histogram_bins=256
        self.checkBox.stateChanged.connect(self.onHistogramCheck)
        self.blob_trend_check.stateChanged.connect(self.onTrendCheck)
        self.histo_binning.valueChanged[int].connect(self.onHistBinChange)

        self._histogram = None


    def modeChange(self,mode):
        self._current_mode = mode
        self.clearData()

    def getFilter(self,tof):
        

        if self._start_tof is not None:
            return (tof >= self._start_tof) & (tof < self._end_tof)
        else:
            return (tof>=0.0)

    def onHistBinChange(self,value):
        self._histogram_bins = value
        if self._histogram_mode:
            self.clearData()



    def onHistogramCheck(self,status):
        if status == 2:
            self._histogram_mode = True
            self.clearData()
        else:
            self._histogram_mode = False
            self.clearData()

    def onTrendCheck(self,status):
        if status == 2:
            self.blob_trend.show()
        else:
            self.blob_trend.hide()

    def updateMatrix(self,x,y,tof,tot):
        tof_filter = self.getFilter(tof)

        self._matrix[x[tof_filter],y[tof_filter]] += 1.0


    def onRegionChange(self,start,end):
        self._start_tof = start
        self._end_tof = end
        self.clearData()

    def computeDirectionCosine(self,x,y,tof):
        x_cm = np.average(x)
        y_cm = np.average(y)


    def updateHistogram(self,x,y):
        h = np.histogram2d(x,y,bins=self._histogram_bins,range=[[0,256],[0,256]])
        if self._histogram is None:
            self._histogram = h[0]
        else:
            self._histogram += h[0]



    def updateBlobData(self,cluster_shot,cluster_x,cluster_y,cluster_tof):
        tof_filter = self.getFilter(cluster_tof)
        

        total_triggers = (cluster_shot.max()-cluster_shot.min())+1

        x = cluster_x[tof_filter]
        y = cluster_y[tof_filter]
        tof = cluster_tof[tof_filter]
        shots = cluster_shot[tof_filter]
        if x.size == 0:
            self._last_trigger=cluster_shot.max()
            #self.updateTrend(self._last_trigger,0)
            self.rec_blobs.setText(str(int(0)))
            return

        uniq_shot,counts = np.unique(shots,return_counts=True)



        self._int_blob_count += np.sum(counts)

        avg_blobs = np.sum(counts)/total_triggers

        self.rec_blobs.setText(str(int(avg_blobs)))
        
        self.int_blobs.setText(str(self._int_blob_count))

        self.computeDirectionCosine(x,y,tof)
        self._last_trigger = shots.max()
        #self.updateTrend(self._last_trigger,avg_blobs)

        if self._histogram_mode:
            self.updateHistogram(x,y)


    def onCentroid(self,event):
        if self._current_mode in (ViewerMode.Centroid,):   
            cluster_shot,cluster_x,cluster_y,cluster_tof,cluster_tot = event
            self.updateBlobData(cluster_shot,cluster_x,cluster_y,cluster_tof )
    
    def onEvent(self,event):
        if self._current_mode in (ViewerMode.TOF, ViewerMode.Centroid,):    
            
            if not self._histogram_mode:
                counter,x,y,tof,tot = event
                self.updateMatrix(x,y,tof,tot)

    def onToA(self,event):
        if self._current_mode in (ViewerMode.TOA,):
            x,y,toa,tot = event
            self.updateMatrix(x,y,toa,tot)
    
    def updateTrend(self,trigger,avg_blobs):

        self._blob_trend.append(avg_blobs)
        self._blob_trend_trigger.append(trigger)
        #self._blob_trend_trigger[-1]= trigger




        

    def plotData(self):
        if not self._histogram_mode:
            self.image_view.setImage(self._matrix/self._matrix.max(),autoLevels=False,autoRange=False,autoHistogramRange=False)
        else:
            if self._histogram is not None:
                
                self.image_view.setImage(self._histogram/self._histogram.max(),autoLevels=False,autoRange=False,autoHistogramRange=False)
        try:
            self._blob_trend_data.setData(x=np.array(self._blob_trend_trigger),y=np.array(self._blob_trend))
        except:
            pass
    
    def clearData(self):
        self._matrix[...]=0.0
        self._int_blob_count = 0
        self._histogram = None
        #self.plotData()


def main():
    import sys
    app = QtGui.QApplication([])
    config = BlobView()
    config.show()

    app.exec_()
if __name__=="__main__":
    main()