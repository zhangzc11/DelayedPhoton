#! /usr/bin/env python
from ROOT import TLatex, TCanvas
import ROOT as rt
import shlex
from array import *
from math import *
import numpy as np
from scipy.interpolate import Rbf, interp1d


def getXsecBR(Lambda, Ctau):
	fxsecBR = 0.0
	efxsecBR = 0.0
	Ctau_this=str(Ctau)
	if Ctau_this == "10.0":
		Ctau_this = "10"
	if Ctau_this == "0.1":
		Ctau_this = "0_1"
	if Ctau_this == "0.01":
		Ctau_this = "0_01"
	if Ctau_this == "0.001":
		Ctau_this = "0_001"

	model_to_find="L"+str(Lambda)+"TeV_Ctau"+Ctau_this+"cm"
	
	with open("../data/XsecBR.dat","r") as xsec_file:
		for this_model in xsec_file:
			this_model_array = shlex.split(this_model)
			if this_model_array[0] == model_to_find:
				#print this_model
				fxsecBR = float(this_model_array[4])
				efxsecBR = float(this_model_array[5])
	#print model_to_find
	return fxsecBR,efxsecBR

def getXsecBR2(Lambda, Ctau):
	fxsecBR = 0.0
	efxsecBR = 0.0
	if Lambda == 100:
		return 2.16, 0.02
	if Lambda == 150:
		return 0.228, 0.002
	if Lambda == 200:
		return 0.0445, 0.0003
	if Lambda == 250:
		return 0.0126, 0.0001
	if Lambda == 300:
		return 0.00445, 0.00003
	if Lambda == 350:
		return 0.00178, 0.00001
	if Lambda == 400:
		return 0.000778, 0.000005


def drawCMS(myC, energy, lumi):

	myC.cd()

        tlatex = TLatex()
        baseSize = 25
        tlatex.SetNDC()
        tlatex.SetTextAngle(0)
        tlatex.SetTextColor(1)
        tlatex.SetTextFont(63)
        tlatex.SetTextAlign(11)
        tlatex.SetTextSize(25)
        tlatex.DrawLatex(0.16, 0.92, "CMS")
        tlatex.SetTextFont(53)
        tlatex.DrawLatex(0.23, 0.92, "Preliminary")
        tlatex.SetTextFont(43)
        tlatex.SetTextSize(23)
	lumiString = "%.2f" % lumi
        Lumi = "" + lumiString + " pb^{-1} ("+str(energy)+" TeV)"
        if lumi > 1000:
		lumiString = "%.2f" % (lumi/1000.0)
                Lumi = "" + lumiString + " fb^{-1} ("+str(energy)+" TeV)"
        tlatex.SetTextAlign(31)
        tlatex.DrawLatex(0.9, 0.92, Lumi)
        tlatex.SetTextAlign(11)

def drawCMS2(myC, energy, lumi):

	myC.cd()

        tlatex = TLatex()
        baseSize = 25
        tlatex.SetNDC()
        tlatex.SetTextAngle(0)
        tlatex.SetTextColor(1)
        tlatex.SetTextFont(63)
        tlatex.SetTextAlign(11)
        tlatex.SetTextSize(25)
        tlatex.DrawLatex(0.16, 0.95, "CMS")
        tlatex.SetTextFont(53)
        tlatex.DrawLatex(0.23, 0.95, "Preliminary")
        tlatex.SetTextFont(43)
        tlatex.SetTextSize(23)
	lumiString = "%.2f" % lumi
        Lumi = "" + lumiString + " pb^{-1} ("+str(energy)+" TeV)"
        if lumi > 1000:
		lumiString = "%.2f" % (lumi/1000.0)
                Lumi = "" + lumiString + " fb^{-1} ("+str(energy)+" TeV)"
        tlatex.SetTextAlign(31)
        tlatex.DrawLatex(0.9, 0.95, Lumi)
        tlatex.SetTextAlign(11)

def drawCMS3(myC, energy, lumi):
        myC.cd()

        tlatex = TLatex()
        baseSize = 25
        tlatex.SetNDC()
        tlatex.SetTextAngle(0)
        tlatex.SetTextColor(1)
        tlatex.SetTextFont(61)
        tlatex.SetTextAlign(11)
        tlatex.SetTextSize(0.0375)
        tlatex.DrawLatex(0.215, 0.89, "CMS")
        tlatex.SetTextFont(52)
        tlatex.SetTextSize(0.0285)
        tlatex.DrawLatex(0.215, 0.852, "Preliminary")
        tlatex.SetTextFont(43)
        tlatex.SetTextSize(23)
        lumiString = "%.1f" % lumi
        Lumi = "" + lumiString + " pb^{-1} ("+str(energy)+" TeV)"
        if lumi > 1000:
                lumiString = "%.1f" % (lumi/1000.0)
                Lumi = "" + lumiString + " fb^{-1} ("+str(energy)+" TeV)"
        tlatex.SetTextAlign(31)
        tlatex.DrawLatex(0.85, 0.96, Lumi)
        tlatex.SetTextAlign(11)

def drawCMS3_supp(myC, energy, lumi):
        myC.cd()

        tlatex = TLatex()
        baseSize = 25
        tlatex.SetNDC()
        tlatex.SetTextAngle(0)
        tlatex.SetTextColor(1)
        tlatex.SetTextFont(61)
        tlatex.SetTextAlign(11)
        tlatex.SetTextSize(0.0375)
        tlatex.DrawLatex(0.18, 0.96, "CMS")
        tlatex.SetTextFont(52)
        tlatex.SetTextSize(0.0285)
        tlatex.DrawLatex(0.26, 0.96, "Supplementary")
        tlatex.SetTextFont(43)
        tlatex.SetTextSize(23)
        lumiString = "%.1f" % lumi
        Lumi = "" + lumiString + " pb^{-1} ("+str(energy)+" TeV)"
        if lumi > 1000:
                lumiString = "%.1f" % (lumi/1000.0)
                Lumi = "" + lumiString + " fb^{-1} ("+str(energy)+" TeV)"
        tlatex.SetTextAlign(31)
        tlatex.DrawLatex(0.85, 0.96, Lumi)
        tlatex.SetTextAlign(11)


def interpolate2D(hist,epsilon=1,smooth=0,multiplyNbinsX=3,multiplyNbinsY=30,diagonalOffset=0,fixLSP0=False,refHist=None):
    x = array('d',[])
    y = array('d',[])
    z = array('d',[])
    
    binWidth = float(hist.GetXaxis().GetBinWidth(1))
    
    for i in range(1, hist.GetNbinsX()+1):
        for j in range(1, hist.GetNbinsY()+1):
            if hist.GetBinContent(i,j)>0.:
                if refHist!=None and refHist.GetBinContent(i,j) > 0.:
                        x.append(hist.GetXaxis().GetBinCenter(i))
                        y.append(hist.GetYaxis().GetBinCenter(j))
                        z.append(rt.TMath.Log(hist.GetBinContent(i,j)/refHist.GetBinContent(i,j)))
                else:
                    x.append(hist.GetXaxis().GetBinCenter(i))
                    y.append(hist.GetYaxis().GetBinCenter(j))
                    z.append(rt.TMath.Log(hist.GetBinContent(i,j)))

    mgMin = hist.GetXaxis().GetBinCenter(1) - 0.5*hist.GetXaxis().GetBinWidth(1)
    mgMax = hist.GetXaxis().GetBinCenter(hist.GetNbinsX()) + 0.5*hist.GetXaxis().GetBinWidth(hist.GetNbinsX())
    mchiMin = hist.GetYaxis().GetBinCenter(1) - 0.5*hist.GetYaxis().GetBinWidth(1)
    mchiMax = hist.GetYaxis().GetBinCenter(hist.GetNbinsY()-1) + 0.5*hist.GetYaxis().GetBinWidth(hist.GetNbinsY()-1)
    
    myX = np.linspace(mgMin, mgMax, multiplyNbinsX*hist.GetNbinsX())
    #myY = np.linspace(mchiMin, mchiMax, multiplyNbinsY*hist.GetNbinsY())
    myY = np.zeros(multiplyNbinsY*(hist.GetNbinsY()-1))
    for j in range(1, hist.GetNbinsY()):
	for rep in range(multiplyNbinsY):
		jj = (j-1)*multiplyNbinsY + rep
		myY[jj] = hist.GetYaxis().GetBinCenter(j) + hist.GetYaxis().GetBinWidth(j)*(rep*1.0/multiplyNbinsY -  0.5)

    #print "myX:===="
    #print myX
    #print "myY:===="
    #print myY


    #myY = np.zeros(
    myXI, myYI = np.meshgrid(myX,myY)

    rbf = Rbf(x, y, z,function='multiquadric', epsilon=epsilon,smooth=smooth)
    myZI = rbf(myXI, myYI)
    rbf_nosmooth = Rbf(x, y, z, function='multiquadric',epsilon=epsilon,smooth=10)
    otherY = array('d',[mchiMin])
    lineXI, lineYI = np.meshgrid(myX,otherY)
    lineZI = rbf_nosmooth(lineXI, lineYI)
	

    xbins_th2 = []
    ybins_th2 = []
    xbins_th2.append(hist.GetXaxis().GetBinCenter(1)-0.5*hist.GetXaxis().GetBinWidth(1))
    ybins_th2.append(hist.GetYaxis().GetBinCenter(1)-0.5*hist.GetYaxis().GetBinWidth(1))
    for idx in range(len(myXI[0,:])-1):
	#xbins_th2.append(0.5*(myXI[0][idx]+myXI[0][idx+1]))
	xbins_th2.append(myXI[0][idx+1])
    xbins_th2.append(hist.GetXaxis().GetBinCenter(hist.GetNbinsX())+0.5*hist.GetXaxis().GetBinWidth(hist.GetNbinsX()))
	
    for idx in range(len(myYI[:,0])-1):
	#ybins_th2.append(0.5*(myYI[idx][0]+myYI[idx+1][0]))
	ybins_th2.append(myYI[idx+1][0])
    ybins_th2.append(hist.GetYaxis().GetBinCenter(hist.GetNbinsY())+0.5*hist.GetYaxis().GetBinWidth(hist.GetNbinsY()))
 
    #print "xbins_th2: ==="
    #print xbins_th2 
    #print "ybins_th2: ==="
    #print ybins_th2 

    hist2 = rt.TH2F("hist2","hist2", len(xbins_th2)-1, np.array(xbins_th2), len(ybins_th2)-1, np.array(ybins_th2))

    for ix in range(len(xbins_th2)-1):
        for iy in range(len(ybins_th2)-2):
            hist2.SetBinContent(ix+1, iy+1, np.exp(myZI[iy][ix]))
	hist2.SetBinContent(ix+1, len(ybins_th2)-1, 1.0e-6)

    return hist2

