
import cv2
import urllib.request
import numpy
import peakutils
import matplotlib.pyplot as plt
import scipy.signal

class SpectrometerCameraSensor:
    
    def __init__(self):        
        req = urllib.request.urlopen('file:///home/nidwe/development/resources/testSpectrum.png')
        arr = numpy.asarray(bytearray(req.read()), dtype=numpy.uint8)
        frame = cv2.imdecode(arr, -1) # 'Load it as it is'        
        bwimage = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        rows,cols = bwimage.shape
        
        print (rows)
        print (cols)
        
        halfway =int(rows*0.5) #halfway point to select a row of pixels from
        intensity=[]
        print (halfway)
        
        intensity = [0] * cols

        for i in range(cols):
            data = bwimage[halfway,i]        
            intensity[i] = data
            
#            if data>20:
#                print (i)
#                print (intensity[i])
            
        thresh=20       
        mindist=50
        
        thresh = int(thresh) #make sure the data is int.
        thresh=thresh/max(intensity)
        
        MSFy = numpy.array(intensity)
        print(MSFy)
        
        #indexes = peakutils.indexes(MSFy, thres=thresh, min_dist=mindist)
        
        x = numpy.linspace(0, 100, 1000)
        centers = (20, 40, 70)
        y = (peakutils.gaussian(x, 1, centers[0], 3) +
             peakutils.gaussian(x, 2, centers[1], 5) +
             peakutils.gaussian(x, 3, centers[2], 1) +
             numpy.random.random(x.size) * 0.2)

        #filtered = scipy.signal.savgol_filter(y, 51, 3)
        filtered = scipy.signal.savgol_filter(MSFy, 3, 2)
        idx = peakutils.indexes(filtered, thres=thresh, min_dist=mindist)        
        
        
        
        #print(y)
        print(idx)
        print (type(idx))
        
        print (type(intensity))
        
        ax = plt.axes()
        
        #plt.plot(numpy.linspace(0, 1920, 1),MSFy , idx)
        ax.plot(intensity)
        
        peakValues=intensity = [0] * len(idx)
        index=0
        for x in numpy.nditer(idx):
            print (x)
            peakValues[index]=MSFy[x]            
            
            index=index+1
        ax.plot(idx.tolist(), peakValues, 'ro')            
        
        #plt.plot(filtered)
        plt.ylabel('some numbers')
        plt.show()
        
        #pyplot.figure(figsize=(10, 6))
        #pplot(MSFxr, MSFy)
        
        #print (indexes)
        
        
        
        
        
        
        
        
