import wave
import matplotlib.pyplot as plt
import numpy as np
import time
import math
class audioFFT:
    def getFFTMsg(self,filePath):
        #1. read audio file by wave
        audioFile=wave.open(filePath,'rb')

         #2.get audio msg from file
        channels,sampwidth,framerate,nframes,comptype,compname=audioParams=audioFile.getparams()
        #audio second
        second=nframes/framerate
        print("channels:{0},sampwidth:{1},framerate;{2},nframes:{3},comptype:{4},compname:{5}".format(channels,sampwidth,framerate,nframes,comptype,compname))
        print("audio second:"+str(second))
        timeInterval=0.1
        invertvalCount=1/timeInterval
        #每一次刷新帧的个数
        framePerInterval=int(framerate/invertvalCount)


        print("framePerInterval:"+str(framePerInterval))

        orignframeData=audioFile.readframes(nframes)
        frameData=np.fromstring(orignframeData,dtype=np.int16)

        frameData = np.reshape(frameData,[nframes,channels]).T

        leftChannelData=frameData[0]


        plt.ion() #开启interactive mode 成功的关键函数
        plt.figure(1)
        plt.xlabel(u"Freq(Hz)")
        plt.subplots_adjust(hspace=0.4)


        tag=True
        x_data=[]
        i=0
        while tag:
            if i*framePerInterval>nframes:
                tag=False
                continue
            x_data.append(i*framePerInterval)
            i+=1
        time1=time.time()
        for i in x_data:
            i=math.ceil(i)
            print(i)
            plt.clf()
            plt.ylim(-60,100)
            if i+framePerInterval>nframes:
                break
            xs = leftChannelData[i:i+framePerInterval]
            xf = np.fft.rfft(xs)/framePerInterval

            freqs = np.linspace(0, framerate/2, framePerInterval/2+1)
            xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))

            # for data in xf:
            #     print(data)
            plt.plot(freqs, xfp)
            plt.pause(timeInterval-0.08)
        print("use times:")
        print(time.time()-time1)




    def Spectrogram(self,filePath):
        #1. read audio file by wave
        audioFile=wave.open(filePath,'rb')

        #2.get audio msg from file
        channels,sampwidth,framerate,nframes,comptype,compname=audioParams=audioFile.getparams()
        print("channels:{0},sampwidth:{1},framerate;{2},nframes:{3},comptype:{4},compname:{5}".format(channels,sampwidth,framerate,nframes,comptype,compname))

        orignframeData=audioFile.readframes(nframes)
        frameData=np.fromstring(orignframeData,dtype=np.int16)

        frameData=frameData*1.0/max(abs(frameData))

        frameData = np.reshape(frameData,[nframes,channels]).T
        audioFile.close()
        print("绘制语谱图....")
        plt.specgram(frameData[0],Fs=framerate,scale_by_freq=True,sides='default')
        plt.ylabel('Frequency')
        plt.xlabel('Time(s)')
        plt.show()



if __name__=="__main__":
    filePath="毛不易-东北民谣.wav"
    audiofft=audioFFT()
    # audiofft.Spectrogram(filePath)
    audiofft.getFFTMsg(filePath)


