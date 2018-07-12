# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 21:29:58 2018

@author: Irfan Javed
"""

import numpy as np
import matplotlib.pyplot as plt
import cmath

def makeMirror(mirrorLen, inside = False):
    fig = plt.figure(figsize = (10, 10))
    ax = fig.gca()
    ax.set_xlim(-mirrorLen/10, mirrorLen+mirrorLen/10)
    ax.set_xlabel("$x/m$", fontsize = 12)
    ax.set_ylabel("$y/m$", fontsize = 12)
    ax.set_title("$Fig. 1$", fontsize = 20)
    ax.plot([0, mirrorLen], [0, 0], "-")
    ax.plot([0], [0], "ok")
    if inside==False:
        midMirror = (-mirrorLen/10+mirrorLen+mirrorLen/10)/2
        ax.set_ylim(-2, 10)
        ax.arrow(midMirror, -1, 0, 1, width = mirrorLen/100, color = "k",
                  length_includes_head = True, head_length = 12/50)
        ax.arrow(0, -1, 0, 1, width = mirrorLen/100, color = "k",
                  length_includes_head = True, head_length = 12/50)
        ax.text(midMirror-mirrorLen/32, -1.2, "$Mirror$")
        ax.text(-mirrorLen/32, -1.2, "$Origin$")
    return fig

def divideMirror(mirrorLen, numPiece, inside = False, sourceX = None,
                 sourceY = None, photoX = None, photoY = None):
    if numPiece>1000:
        raise ValueError("numPiece cannot be greater than 1000.")
    if numPiece<=0:
        raise ValueError("numPiece must be a positive integer.")
    if type(numPiece)!=int:
        raise TypeError("numPiece must be a positive integer.")
    pieceLen = mirrorLen/numPiece
    valX = np.zeros([1, numPiece+1])
    varX1 = 0
    varX2 = pieceLen/2
    font = 200/numPiece
    fig = makeMirror(mirrorLen, inside = True)
    ax = fig.gca()
    ax.set_title("$Fig. 2$", fontsize = 20)
    if inside==False:
        ax.set_ylim(-2, 10)
        for i in range(numPiece+1):
            if font>20 and i<numPiece:
                ax.text(varX2-pieceLen/5, -0.3, "$x_{"+str(i)+"}$",
                                                     fontsize = 20)
            elif 2.5<=font<=20 and i<numPiece:
                ax.text(varX2-pieceLen/5, -0.3, "$x_{"+str(i)+"}$",
                                                     fontsize = font)
            valX[0][i] = varX1
            varX1 += pieceLen
            if i<numPiece:
                varX2 += pieceLen
    else:
        valX = np.lib.pad(valX, ((0, 0), (0, 2)), "constant",
                          constant_values = (0))
        valX[0][numPiece+1] = sourceX
        valX[0][numPiece+2] = photoX
        for i in range(numPiece+1):
            valX[0][i] = varX1
            varX1 += pieceLen
        varX1 = 0
        font = 200/(numPiece*((valX.max()-valX.min())/mirrorLen))
        ax.set_ylim(-max([sourceY, photoY])/5, max([sourceY, photoY])
        +max([sourceY, photoY])/5)
        for i in range(numPiece+1):
            if font>20 and i<numPiece:
                ax.text(varX2-pieceLen/5, -0.025*(max([sourceY, photoY])+(2/5)
                *(max([sourceY, photoY]))), "$x_{"+str(i)+"}$", fontsize = 20)
            elif 2.5<=font<=20 and i<numPiece:
                ax.text(varX2-pieceLen/5, -0.025*(max([sourceY, photoY])+(2/5)
                *(max([sourceY, photoY]))), "$x_{"+str(i)+"}$", fontsize = font)
            valX[0][i] = varX1
            varX1 += pieceLen
            if i<numPiece:
                varX2 += pieceLen
    if inside==True:
        ax.set_xlim(valX.min()-((valX.max()-valX.min())/10), valX.max()
        +((valX.max()-valX.min())/10))
        zeros = np.zeros([1, numPiece+1])
        ax.plot(valX[0][:-2], zeros[0], "|k")
    else:
        zeros = np.zeros([1, numPiece+1])
        ax.plot(valX[0], zeros[0], "|k")
    return fig, valX

def placeSAndP(mirrorLen, numPiece, sourceX, sourceY, photoX, photoY):
    if sourceY<=0 or photoY<=0:
        raise ValueError(
                "sourceY and photoY should both be greater than zero.")
    fig, valX = divideMirror(mirrorLen, numPiece, inside = True, sourceX =
                             sourceX, sourceY = sourceY, photoX = photoX,
                             photoY = photoY)
    ax = fig.gca()
    ax.set_title("$Fig. 3$", fontsize = 20)
    ax.plot([sourceX], [sourceY], "*r", markersize = 15)
    ax.plot([photoX], [photoY], "hg", markersize = 15)
    ax.text(sourceX-(1/90)*(valX.max()-valX.min()+(1/5)
    *(valX.max()-valX.min())), sourceY+(1/40)*(max([sourceY, photoY])
    +(2/5)*max([sourceY, photoY])), "$A$", fontsize = 20)
    ax.text(photoX-(1/90)*(valX.max()-valX.min()+(1/5)
    *(valX.max()-valX.min())), photoY+(1/40)*(max([sourceY, photoY])
    +(2/5)*max([sourceY, photoY])), "$B$", fontsize = 20)
    return fig

def classicalPath(mirrorLen, numPiece, sourceX, sourceY, photoX, photoY):
    refPointX = (photoY*abs(sourceX-photoX))/(sourceY+photoY)
    fig = placeSAndP(mirrorLen, numPiece, sourceX, sourceY, photoX, photoY)
    ax = fig.gca()
    ax.set_title("$Fig. 4$", fontsize = 20)
    if (sourceX<photoX and 0<=photoX-refPointX<=mirrorLen):
        midPointX1 = (sourceX+photoX-refPointX)/2
        midPointX2 = (photoX+photoX-refPointX)/2
        ax.plot([sourceX, sourceX+(abs(sourceX-photoX)-refPointX)],
                  [sourceY, 0], "-r")
        ax.plot([sourceX+(abs(sourceX-photoX)-refPointX), photoX],
                  [0, photoY], "-r")
        ax.annotate("", xy = (midPointX1, sourceY/2), xytext =
                    (sourceX, sourceY),
                    arrowprops = {"arrowstyle": "->", "ec": "r"}, size = 15,
                    ha = "center", va = "center")
        ax.annotate("", xy = (midPointX2, photoY/2), xytext =
                    (photoX-refPointX, 0),
                    arrowprops = {"arrowstyle": "->", "ec": "r"}, size = 15,
                    ha = "center", va = "center")
    elif (sourceX>=photoX and 0<=photoX+refPointX<=mirrorLen):
        midPointX1 = (sourceX+photoX+refPointX)/2
        midPointX2 = (photoX+photoX+refPointX)/2
        ax.plot([sourceX, sourceX-(abs(sourceX-photoX)-refPointX)],
                  [sourceY, 0], "-r")
        ax.plot([sourceX-(abs(sourceX-photoX)-refPointX), photoX],
                  [0, photoY], "-r")
        ax.annotate("", xy = (midPointX1, sourceY/2), xytext =
                    (sourceX, sourceY),
                    arrowprops = {"arrowstyle": "->", "ec": "r"}, size = 15,
                    ha = "center", va = "center")
        ax.annotate("", xy = (midPointX2, photoY/2), xytext =
                    (photoX+refPointX, 0),
                    arrowprops = {"arrowstyle": "->", "ec": "r"}, size = 15,
                    ha = "center", va = "center")
    else:
        print("Classically, no photon reflected by the mirror would reach the"
              "photomultiplier.")
    return fig

def QEDPath(mirrorLen, numPiece, sourceX, sourceY, photoX, photoY):
    pieceLen = mirrorLen/numPiece
    fig = classicalPath(mirrorLen, numPiece, sourceX, sourceY, photoX, photoY)
    ax = fig.gca()
    ax.set_title("$Fig. 5$", fontsize = 20)
    for i in range(numPiece):
        ax.plot([sourceX, pieceLen/2+i*pieceLen], [sourceY, 0], "-k")
        ax.plot([pieceLen/2+i*pieceLen, photoX], [0, photoY], "-k")
        if numPiece<=80:
            midPointX1 = (sourceX+pieceLen/2+i*pieceLen)/2
            midPointX2 = (pieceLen/2+i*pieceLen+photoX)/2
            ax.annotate("", xy = (midPointX1, sourceY/2), xytext =
                        (sourceX, sourceY),
                        arrowprops = {"arrowstyle": "->", "ec": "k"}, size = 15,
                        ha = "center", va = "center")
            ax.annotate("", xy = (midPointX2, photoY/2), xytext =
                        (pieceLen/2+i*pieceLen, 0),
                        arrowprops = {"arrowstyle": "->", "ec": "k"}, size = 15,
                        ha = "center", va = "center")

def createTimes(mirrorLen, numPiece, sourceX, sourceY, photoX, photoY, speed):
    pieceLen = mirrorLen/numPiece
    times = np.zeros([1, numPiece])
    for i in range(numPiece):
        times[0][i] = (np.sqrt((pieceLen/2+i*pieceLen-sourceX)**2+(sourceY**2))
        +np.sqrt((pieceLen/2+i*pieceLen-photoX)**2+(photoY**2)))/speed
    return times

def plotTimes(mirrorLen, numPiece, times):
    pieceLen = mirrorLen/numPiece
    length = np.zeros([1, numPiece])
    xTicksOld = np.zeros([1, numPiece+1])
    xTicksNew = []
    for i in range(numPiece):
        length[0][i] = pieceLen/2+i*pieceLen
    fig = plt.figure(figsize = (10, 10))
    ax = fig.gca()
    ax.set_xlabel("$Length/m$", fontsize = 12)
    ax.set_ylabel("$Time/s$", fontsize = 12)
    ax.set_title("$Fig. 6$", fontsize = 20)
    ax.plot(length[0], times[0], "ok-")
    for i in range(numPiece+1):
        xTicksOld[0][i] = i*pieceLen
        xTicksNew.append(round(i*pieceLen, 1))
    ax.set_xticks(xTicksOld[0])
    if numPiece<=25:
        ax.set_xticklabels(xTicksNew)
    else:
        ax.set_xticklabels([])

def phasor(amp, phase):
    if amp<0:
        raise ValueError("amp cannot be negative.")
    x = np.array([[0]])
    y = np.array([[0]])
    u = np.array([[amp*np.cos(phase*(np.pi/180))]])
    v = np.array([[amp*np.sin(phase*(np.pi/180))]])
    fig = plt.figure(figsize = (10, 10))
    ax = fig.gca()
    ax.set_xlim(-amp-amp/2, amp+amp/2)
    ax.set_ylim(-amp-amp/2, amp+amp/2)
    ax.set_xlabel("$x/unit$", fontsize = 12)
    ax.set_ylabel("$y/unit$", fontsize = 12)
    ax.set_title("$Fig. 7$", fontsize = 20)
    ax.plot([0], [0], marker = "o", color = u"#1f77b4", markersize = 10)
    ax.plot([-amp-amp/2, amp+amp/2], [0, 0], color = u"#1f77b4",
            linestyle = "-")
    ax.plot([0, 0], [-amp-amp/2, amp+amp/2], color = u"#1f77b4",
            linestyle = "-")
    ax.quiver(x, y, u, v, angles = "xy", scale_units = "xy", scale = 1)

def timePhasor(amp, freq):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize = (10, 6))
    ax1 = plt.subplot2grid((3, 5), (1, 0), colspan = 2, rowspan = 1)
    ax1.set_xticks([])
    ax1.set_xticklabels([])
    ax1.set_yticks([])
    ax1.set_yticklabels([])
    ax1.set_title("$Fig. 7$", fontsize = 20)
    ax2 = plt.subplot2grid((3, 5), (0, 2), colspan = 3, rowspan = 3)
    ax2.set_xlim(-amp-1, amp+1)
    ax2.set_ylim(-amp-1, amp+1)
    ax2.set_xlabel("$x/unit$", fontsize = 12)
    ax2.set_ylabel("$y/unit$", fontsize = 12)
    ax2.set_title("$Fig. 8$", fontsize = 20)
    ax2.set_aspect('equal', 'box')
    ax2.plot([-amp-1, amp+1], [0, 0], color = u"#1f77b4", linestyle = "-")
    ax2.plot([0, 0], [-amp-1, amp+1])
    ax2.plot([0], [0], marker = "o", color = u"#1f77b4", markersize = 10)
    text1 = ax1.text(0.5, 0.5, str(0).zfill(2), fontsize = 60, ha = "center",
                     va = "center")
    text2 = ax1.text(0.68, 0.35, str(0).zfill(2), fontsize = 20)
    ax1.text(0.5, 0.1, "fs", fontsize = 20, ha = "center", va = "center")
    phasor = ax2.quiver([[0]], [[0]], [[amp]], [[0]], angles = "xy",
                        scale_units = "xy", scale = 1)
    fig.tight_layout()
    def updatePhasor(i, phasor, text1, text2 , amp, freq, frames, interval):
        t = np.linspace(0, 1, frames)
        u = [[amp*np.cos(2*np.pi*freq*t[i])]]
        v = [[amp*np.sin(2*np.pi*freq*t[i])]]
        if i%10!=0:
            text2.set_text(str(((i)%10)*10).zfill(2))
        else:
            text2.set_text(str(0).zfill(2))
            text1.set_text(str((i)//10).zfill(2))
        if i==149:
            text1.set_text("15")
            text2.set_text("00")
        phasor.set_UVC(u, v)
        return phasor, text1, text2
    frames = 150
    interval = 33+(1/3)
    freq = freq
    mpl.rcParams["animation.embed_limit"] = 500
    return fig, updatePhasor, (phasor, text1, text2, amp, freq, frames,
                                   interval), frames, interval, True

def phasorsOnMirror(mirrorLen, numPiece, times):
    pieceLen = mirrorLen/numPiece
    lightFreq = None
    minInt = None
    for i in range(1, numPiece):
        if minInt==None or minInt>times[0][i]-times[0][i-1]:
            minInt = times[0][i]-times[0][i-1]
    lightFreq = (7.5/360)/minInt
    comp = np.zeros([1, numPiece], dtype = complex)
    x = np.zeros([1, numPiece])
    y = np.zeros([1, numPiece])
    reals = np.zeros([1, numPiece])
    imags = np.zeros([1, numPiece])
    z = 0
    fig = plt.figure(figsize = (10, 10))
    ax = fig.gca()
    ax.set_title("$Fig. 9$", fontsize = 20)
    for i in range(numPiece):
        comp[0][i] = -((mirrorLen/10)*cmath.exp(2*np.pi*lightFreq*times[0][i]
        *1j))
        reals[0][i] = -(((mirrorLen/10)*(cmath.exp(2*np.pi*lightFreq
             *times[0][i]*1j))).real)
        imags[0][i] = -(((mirrorLen/10)*(cmath.exp(2*np.pi*lightFreq
             *times[0][i]*1j))).imag)
        x[0][i] = pieceLen/2+i*pieceLen
        z += -((mirrorLen/10)*cmath.exp(2*np.pi*lightFreq*times[0][i]*1j))
    ax.set_xlim(-mirrorLen/10, mirrorLen+mirrorLen/10)
    ax.set_ylim(-mirrorLen/2-mirrorLen/10, mirrorLen/2+mirrorLen/10)
    ax.set_xlabel("$x/m$", fontsize = 12)
    ax.set_ylabel("$y/m$", fontsize = 12)
    ax.set_title("$Fig. 10$", fontsize = 20)
    ax.plot([0, mirrorLen], [0, 0], "-")
    ax.plot([0], [0], "ok")
    ax.quiver(x, y, reals, imags, angles = "xy", scale_units = "xy", scale = 1)
    return reals, imags, z

def addPhasors(numPiece, reals, imags, z, startInd, endInd):
    if startInd<0 or startInd>numPiece-1:
        raise ValueError("startInd must be between 0 and numPiece-1 inclusive.")
    if endInd<0 or endInd>numPiece-1:
        raise ValueError("endInd must be between 0 and numPiece-1 inclusive.")
    if startInd>=endInd:
        raise ValueError("startInd must be less than endInd.")
    if type(startInd)!=int:
        raise TypeError("startEnd must be a nonnegative integer.")
    if type(endInd)!=int:
        raise TypeError("endInd must be a nonnegative integer.")
    diff = endInd-startInd
    reals = reals[0][startInd: endInd+1]
    imags = imags[0][startInd: endInd+1]
    x = np.zeros([1, diff+1])
    y = np.zeros([1, diff+1])
    u = np.zeros([1, diff+1])
    v = np.zeros([1, diff+1])
    xRes = np.zeros([1, diff+2])
    yRes = np.zeros([1, diff+2])
    xResVar = 0
    yResVar = 0
    fig = plt.figure(figsize = [10, 10])
    ax = fig.gca()
    for i in range(diff+1):
        xResVar += reals[i]
        yResVar += imags[i]
        u[0][i] = reals[i]
        v[0][i] = imags[i]
        xRes[0][i+1] = xResVar
        yRes[0][i+1] = yResVar
    for i in range(diff):
        x[0][i+1] = xRes[0][i+1]
        y[0][i+1] = yRes[0][i+1]
    ax.set_xlim(xRes.min()-(xRes.max()-xRes.min())/10, xRes.max()
    +(xRes.max()-xRes.min())/10)
    ax.set_ylim(yRes.min()-(yRes.max()-yRes.min())/10, yRes.max()
    +(yRes.max()-yRes.min())/10)
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_title("$Fig. 11$", fontsize = 20)
    ax.plot([0], [0], "ok")
    ax.plot(xRes[0][-1], yRes[0][-1], "ok")
    ax.quiver(x, y, u, v, angles = "xy", scale_units = "xy", scale = 1)
    ax.quiver([0], [0], xRes[0][-1], yRes[0][-1], color = ["r"],
               angles = "xy", scale_units = "xy", scale = 1)