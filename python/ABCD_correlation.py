from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TH2F
import os, sys
from Aux import *
from config_noBDT import fileNameData, fileNameSig, fileNameGJets, fileNameQCD, cut, cut_GJets, cut_QCD_CR, cut_EWKCR, cut_noDisc, cut_noSigmaIetaIeta, cut_GJets_noSigmaIetaIeta, splots, lumi, outputDir, xsecSig, xsecGJets, xsecQCD, cut_noSminor, cut_GJets_noSminor, cut_blindMET, cut_blindTime, cut_MET_filter
from config_noBDT import fractionGJets, fractionQCD, useFraction, kFactor, cut_GJets, xbins_MET, xbins_time, sigLegend, weight_cut
from config_noBDT import fileNameTTJets, fileNameWJets, xsecTTJets, xsecWJets, fileNameEWKG, xsecEWKG
import numpy as np
import array

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir+"/METCorrPlots")
os.system("mkdir -p "+outputDir+"/METCorrPlots")
os.system("cp config_noBDT.py "+outputDir+"/METCorrPlots/")
os.system("cp METCorrPlot.py "+outputDir+"/METCorrPlots/")
#################plot settings###########################
axisTitleSize = 0.06
axisTitleOffset = .8
axisTitleSizeRatioX   = 0.18
axisLabelSizeRatioX   = 0.12
axisTitleOffsetRatioX = 0.94
axisTitleSizeRatioY   = 0.15
axisLabelSizeRatioY   = 0.108
axisTitleOffsetRatioY = 0.32

leftMargin   = 0.12
rightMargin  = 0.05
topMargin    = 0.07
bottomMargin = 0.12


def getXsecBR(Lambda, Ctau):
        fxsecBR = 0.0
        efxsecBR = 0.0
        Ctau_this=str(Ctau)
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
def properScale(hist, norm):
        #norm = 1.0/hist.Integral()
        for i in range(0, hist.GetNbinsX()+1):
                v0 = hist.GetBinContent(i)
                hist.SetBinContent(i, norm*v0)
                if v0 > 0.0000001:
                        hist.SetBinError(i, norm*v0/np.sqrt(v0))
                else:
                        hist.SetBinError(i, 0.0)


def drawTimeAndMETShapes(fileName, label, cutsig, Timesplit, METsplit):
	##draw time shapes for different MET:
	fileThis = TFile(fileName)
        tree = fileThis.Get("DelayedPhoton")
	
	colors = [632, 800, 400, 416, 600, 880, 54, 13, 18, 80, 57, 60, 64, 67, 8, 80, 91, 93, 97,  2, 18, 16, 13]

	histTime = []
	arrayTime = []
	histMET = []
	arrayMET = []
	
	myC = TCanvas( "myC", "myC", 200, 10, 800, 800 )
        myC.SetHighLightColor(2)
        myC.SetFillColor(0)
        myC.SetBorderMode(0)
        myC.SetBorderSize(2)
        myC.SetLeftMargin( leftMargin )
        myC.SetRightMargin( rightMargin )
        myC.SetTopMargin( topMargin )
        myC.SetBottomMargin( bottomMargin )
        myC.SetFrameBorderMode(0)
        myC.SetFrameBorderMode(0)
	myC.SetLogy(1)
	
	legTime = TLegend(0.18, 0.75, 0.93, 0.92)
        legTime.SetNColumns(2)
        legTime.SetBorderSize(0)
        legTime.SetTextSize(0.02)
        legTime.SetLineColor(1)
        legTime.SetLineStyle(1)
        legTime.SetLineWidth(1)
        legTime.SetFillColor(0)
        legTime.SetFillStyle(1001)
	maxYTime = 0.0
	minYTime = 999
	
	for idx in range(1,len(METsplit)):	
		MET_low = METsplit[idx-1]
		MET_high = METsplit[idx]
		cutThis = cutsig + " && t1MET < "+ str(MET_high)+ " && t1MET > "+ str(MET_low)
		histThis = TH1F("histTime_idx"+str(idx), "; #gamma cluster time (ns); Events", 20, -2, 8)
		tree.Draw("pho1ClusterTime_SmearToData>>histTime_idx"+str(idx), cutThis)
		if histThis.Integral() > 0.0:
			properScale(histThis, 1.0/histThis.Integral())
		if(histThis.GetMaximum() > maxYTime):
			maxYTime = histThis.GetMaximum()
		if(histThis.GetMinimum() < minYTime):
			minYTime = histThis.GetMinimum()
		histThis.SetLineWidth(2)
		histThis.SetLineColor(colors[idx-1]-4)
		histThis.SetMarkerColor(colors[idx-1]-4)

		histArray = np.zeros(histThis.GetSize()-2)
		for idh in range(1, histThis.GetSize()-1):
			histArray[idh-1] = histThis.GetBinContent(idh)
		arrayTime.append(histArray)
	
		if idx == 1:
			histThis.GetXaxis().SetTitleSize( axisTitleSize )
			histThis.GetXaxis().SetTitleOffset( axisTitleOffset )
			histThis.GetYaxis().SetTitleSize( axisTitleSize )
			histThis.GetYaxis().SetTitleOffset( axisTitleOffset )
			histThis.Draw("hist")
			legTime.AddEntry(histThis, str(MET_low)+" < #slash{E}_{T} < "+str(MET_high))#+", cos = 1.00000", "lep")
	
		else:
			histThis.Draw("samehist")	
			cosThis = 0.0
                        if np.dot(histArray,histArray) > 0.0 and  np.dot(arrayTime[0],arrayTime[0]) > 0.0:
				cosThis = np.dot(arrayTime[0],histArray) / (np.sqrt(np.dot(histArray,histArray)) * np.sqrt(np.dot(arrayTime[0],arrayTime[0])))

			legTime.AddEntry(histThis, str(MET_low)+" < #slash{E}_{T} < "+str(MET_high))#+", cos = %.5f"%cosThis, "lep")
		histTime.append(histThis)
	if minYTime < 1e-5:
		minYTime = 1e-5
	histTime[0].GetYaxis().SetRangeUser(0.1*minYTime, 500*maxYTime)
	histTime[0].Draw("E")
	for idx in range(1, len(histTime)):
		histTime[idx].Draw("sameE")
	legTime.Draw()
	myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_in_METbins_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_in_METbins_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_in_METbins_"+label+".C")
	
	legMET = TLegend(0.18, 0.75, 0.93, 0.92)
        legMET.SetNColumns(2)
        legMET.SetBorderSize(0)
        legMET.SetTextSize(0.02)
        legMET.SetLineColor(1)
        legMET.SetLineStyle(1)
        legMET.SetLineWidth(1)
        legMET.SetFillColor(0)
        legMET.SetFillStyle(1001)
	maxYMET = 0.0
	minYMET = 999
	
	for idx in range(1,len(Timesplit)):	
		Time_low = Timesplit[idx-1]
		Time_high = Timesplit[idx]
		cutThis = cutsig + " && pho1ClusterTime_SmearToData < "+ str(Time_high)+ " && pho1ClusterTime_SmearToData > "+ str(Time_low)
		histThis = TH1F("histMET_idx"+str(idx), "; #slash{E}_{T} (GeV); Events", 20, 0, 800)
		tree.Draw("t1MET>>histMET_idx"+str(idx), cutThis)
		if histThis.Integral() > 0.0:
			properScale(histThis, 1.0/histThis.Integral())
		if(histThis.GetMaximum() > maxYMET):
			maxYMET = histThis.GetMaximum()
		if(histThis.GetMinimum() < minYMET):
			minYMET = histThis.GetMinimum()
		histThis.SetLineWidth(2)
		histThis.SetLineColor(colors[idx-1]-4)
		histThis.SetMarkerColor(colors[idx-1]-4)

		histArray = np.zeros(histThis.GetSize()-2)
		for idh in range(1, histThis.GetSize()-1):
			histArray[idh-1] = histThis.GetBinContent(idh)
		arrayMET.append(histArray)
	
		if idx == 1:
			histThis.GetXaxis().SetTitleSize( axisTitleSize )
			histThis.GetXaxis().SetTitleOffset( axisTitleOffset )
			histThis.GetYaxis().SetTitleSize( axisTitleSize )
			histThis.GetYaxis().SetTitleOffset( axisTitleOffset )
			histThis.Draw("hist")
			legMET.AddEntry(histThis, str(Time_low)+" < T < "+str(Time_high))#+", cos = 1.00000", "lep")
	
		else:
			histThis.Draw("samehist")	
			cosThis = 0.0
			if np.dot(histArray,histArray) > 0.0 and  np.dot(arrayMET[0],arrayMET[0]) > 0.0:
				cosThis = np.dot(arrayMET[0],histArray) / (np.sqrt(np.dot(histArray,histArray)) * np.sqrt(np.dot(arrayMET[0],arrayMET[0])))

			legMET.AddEntry(histThis, str(Time_low)+" < T < "+str(Time_high))#+", cos = %.5f"%cosThis, "lep")
		histMET.append(histThis)
	if minYMET < 1e-5:
		minYMET = 1e-5
	histMET[0].GetYaxis().SetRangeUser(0.1*minYMET, 500*maxYMET)
	histMET[0].Draw("E")
	for idx in range(1, len(histMET)):
		histMET[idx].Draw("sameE")
	legMET.Draw()
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_in_Timebins_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_in_Timebins_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_in_Timebins_"+label+".C")

def getBinCSys(fileName, label, timeSplits, metSplits, cut_this):
	fileThis = TFile(fileName)
        tree = fileThis.Get("DelayedPhoton")
	All = tree.GetEntries(cut_this)
	for timeSplit in timeSplits:
		for metSplit in metSplits:
			print "calculating systematics due to correlation.... "+label+" ... timeSplit = "+str(timeSplit)+", metSplit = "+str(metSplit)
			A = tree.GetEntries(cut_this+" && t1MET<"+str(metSplit)+" && pho1ClusterTime_SmearToData < "+str(timeSplit))
			B = tree.GetEntries(cut_this+" && t1MET>"+str(metSplit)+" && pho1ClusterTime_SmearToData < "+str(timeSplit))
			C = tree.GetEntries(cut_this+" && t1MET>"+str(metSplit)+" && pho1ClusterTime_SmearToData > "+str(timeSplit))
			D = tree.GetEntries(cut_this+" && t1MET<"+str(metSplit)+" && pho1ClusterTime_SmearToData > "+str(timeSplit))
			C_predict =B*D/A
			
			print "All, A, B, C, D, C_predict, deltaC/C"	
			if C > 0:
				print str(All)+", "+str(A)+", "+str(B)+", "+str(C)+", "+str(D)+", "+str(C_predict)+", "+str((C_predict-C)/C)
			else:
				print str(All)+", "+str(A)+", "+str(B)+", "+str(C)+", "+str(D)+", "+str(C_predict)+", - "
	

def drawTimeAndMETShapesRandN(fileName, label, cutsig, randN):
	##draw time shapes for different MET:
	fileThis = TFile(fileName)
        tree = fileThis.Get("DelayedPhoton")
	
	colors = [632, 800, 400, 416, 600, 880, 54, 13, 18, 80, 57, 60, 64, 67, 8, 80, 91, 93, 97,  2, 18, 16, 13]

	histTime = []
	arrayTime = []
	histMET = []
	arrayMET = []
	
	myC = TCanvas( "myC", "myC", 200, 10, 800, 800 )
        myC.SetHighLightColor(2)
        myC.SetFillColor(0)
        myC.SetBorderMode(0)
        myC.SetBorderSize(2)
        myC.SetLeftMargin( leftMargin )
        myC.SetRightMargin( rightMargin )
        myC.SetTopMargin( topMargin )
        myC.SetBottomMargin( bottomMargin )
        myC.SetFrameBorderMode(0)
        myC.SetFrameBorderMode(0)
	myC.SetLogy(1)
	
	legTime = TLegend(0.18, 0.75, 0.93, 0.92)
        legTime.SetNColumns(2)
        legTime.SetBorderSize(0)
        legTime.SetTextSize(0.02)
        legTime.SetLineColor(1)
        legTime.SetLineStyle(1)
        legTime.SetLineWidth(1)
        legTime.SetFillColor(0)
        legTime.SetFillStyle(1001)
	maxYTime = 0.0
	minYTime = 999
	
	for idx in range(randN):	
		cutThis = cutsig + " && Entry$%"+str(randN)+" == "+str(idx)
		histThis = TH1F("histTime_idx"+str(idx), "; #gamma cluster time (ns); Events", 20, -2, 8)
		tree.Draw("pho1ClusterTime_SmearToData>>histTime_idx"+str(idx), cutThis)
		if histThis.Integral() > 0.0:
			properScale(histThis, 1.0/histThis.Integral())
		if(histThis.GetMaximum() > maxYTime):
			maxYTime = histThis.GetMaximum()
		if(histThis.GetMinimum() < minYTime):
			minYTime = histThis.GetMinimum()
		histThis.SetLineWidth(2)
		histThis.SetLineColor(colors[idx-1]-4)
		histThis.SetMarkerColor(colors[idx-1]-4)

		histArray = np.zeros(histThis.GetSize()-2)
		for idh in range(1, histThis.GetSize()-1):
			histArray[idh-1] = histThis.GetBinContent(idh)
		arrayTime.append(histArray)
	
		if idx == 0:
			histThis.GetXaxis().SetTitleSize( axisTitleSize )
			histThis.GetXaxis().SetTitleOffset( axisTitleOffset )
			histThis.GetYaxis().SetTitleSize( axisTitleSize )
			histThis.GetYaxis().SetTitleOffset( axisTitleOffset )
			histThis.Draw("hist")
			legTime.AddEntry(histThis, "random sample "+str(idx))#+", cos = 1.00000", "lep")
	
		else:
			histThis.Draw("samehist")	
			cosThis = 0.0
                        if np.dot(histArray,histArray) > 0.0 and  np.dot(arrayTime[0],arrayTime[0]) > 0.0:
				cosThis = np.dot(arrayTime[0],histArray) / (np.sqrt(np.dot(histArray,histArray)) * np.sqrt(np.dot(arrayTime[0],arrayTime[0])))

			legTime.AddEntry(histThis, "random sample "+str(idx))#+", cos = %.5f"%cosThis, "lep")
		histTime.append(histThis)
	if minYTime < 1e-5:
		minYTime = 1e-5
	histTime[0].GetYaxis().SetRangeUser(0.1*minYTime, 500*maxYTime)
	histTime[0].Draw("E")
	for idx in range(1, len(histTime)):
		histTime[idx].Draw("sameE")
	legTime.Draw()
	myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_randN_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_randN_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_randN_"+label+".C")


	
	legMET = TLegend(0.18, 0.75, 0.93, 0.92)
        legMET.SetNColumns(2)
        legMET.SetBorderSize(0)
        legMET.SetTextSize(0.02)
        legMET.SetLineColor(1)
        legMET.SetLineStyle(1)
        legMET.SetLineWidth(1)
        legMET.SetFillColor(0)
        legMET.SetFillStyle(1001)
	maxYMET = 0.0
	minYMET = 999
	
	for idx in range(randN):	
		cutThis = cutsig + " && Entry$%"+str(randN)+" == "+str(idx)
		histThis = TH1F("histMET_idx"+str(idx), "; #slash{E}_{T} (GeV); Events", 20, 0, 800)
		tree.Draw("t1MET>>histMET_idx"+str(idx), cutThis)
		if histThis.Integral() > 0.0:
			properScale(histThis, 1.0/histThis.Integral())
		if(histThis.GetMaximum() > maxYMET):
			maxYMET = histThis.GetMaximum()
		if(histThis.GetMinimum() < minYMET):
			minYMET = histThis.GetMinimum()
		histThis.SetLineWidth(2)
		histThis.SetLineColor(colors[idx-1]-4)
		histThis.SetMarkerColor(colors[idx-1]-4)

		histArray = np.zeros(histThis.GetSize()-2)
		for idh in range(1, histThis.GetSize()-1):
			histArray[idh-1] = histThis.GetBinContent(idh)
		arrayMET.append(histArray)
	
		if idx == 0:
			histThis.GetXaxis().SetTitleSize( axisTitleSize )
			histThis.GetXaxis().SetTitleOffset( axisTitleOffset )
			histThis.GetYaxis().SetTitleSize( axisTitleSize )
			histThis.GetYaxis().SetTitleOffset( axisTitleOffset )
			histThis.Draw("hist")
			legMET.AddEntry(histThis, "random sample "+str(idx))#+", cos = 1.00000", "lep")
	
		else:
			histThis.Draw("samehist")	
			cosThis = 0.0
                        if np.dot(histArray,histArray) > 0.0 and  np.dot(arrayMET[0],arrayMET[0]) > 0.0:
				cosThis = np.dot(arrayMET[0],histArray) / (np.sqrt(np.dot(histArray,histArray)) * np.sqrt(np.dot(arrayMET[0],arrayMET[0])))

			legMET.AddEntry(histThis, "random sample "+str(idx))#+", cos = %.5f"%cosThis, "lep")
		histMET.append(histThis)
	if minYMET < 1e-5:
		minYMET = 1e-5
	histMET[0].GetYaxis().SetRangeUser(0.1*minYMET, 500*maxYMET)
	histMET[0].Draw("E")
	for idx in range(1, len(histMET)):
		histMET[idx].Draw("sameE")
	legMET.Draw()
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_randN_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_randN_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_randN_"+label+".C")



def getTimeAndMETCorrFactor(fileName, label, cutsig, Timesplit, METsplit):
	fileThis = TFile(fileName)
        tree = fileThis.Get("DelayedPhoton")

	print tree.GetEntries(cutsig)
	
	h2_rate = TH2F("h2_rate","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, -15, 15, 100, 0, 1000)
	tree.Draw("t1MET:pho1ClusterTime_SmearToData>>h2_rate", cutsig)
	print "correlation factor of "+label+":  "+str(h2_rate.GetCorrelationFactor())



Timesplit = [-2, 0, 0.5, 1.0, 1.5, 3.0, 25]
METsplit = [0, 50, 100, 200, 300, 500, 3000]

'''
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR", cut_GJets, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCDCR", cut_QCD_CR, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "EWKCR", cut_EWKCR, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "Data", cut, Timesplit, METsplit)
'''

drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR", cut_GJets, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCDCR", cut_QCD_CR, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "EWKCR", cut_EWKCR, Timesplit, METsplit)
#drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "Data", cut, Timesplit, METsplit)

'''
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR", cut_GJets, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCDCR", cut_QCD_CR, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "EWKCR", cut_EWKCR, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "Data", cut, 6)

'''

'''
#timeSplits =  np.array([0.0, 1.5])
#metSplits  = np.array([100.0, 150.0, 200.0, 300.0])
timeSplits =  np.array([0.0, 0.5])
metSplits  = np.array([50.0, 100.0])
getBinCSys("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJets", timeSplits, metSplits, cut_GJets)
getBinCSys("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCD", timeSplits, metSplits, cut_QCD_CR)
getBinCSys("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "EWK", timeSplits, metSplits, cut_EWKCR)
'''

