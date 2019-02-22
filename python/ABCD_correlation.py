from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TH2F
import os, sys
from Aux import *
from config_noBDT import fileNameData, fileNameSig, fileNameGJets, fileNameQCD, cut, cut_noDisc, cut_noSigmaIetaIeta, cut_loose_noSigmaIetaIeta, cut_GJets_noSigmaIetaIeta, splots, lumi, outputDir, xsecSig, xsecGJets, xsecQCD, cut_noSminor, cut_loose_noSminor, cut_GJets_noSminor, cut_blindMET, cut_blindTime, cut_MET_filter
from config_noBDT import fractionGJets, fractionQCD, useFraction, kFactor, cut_GJets, cut_loose, xbins_MET, xbins_time, sigLegend, weight_cut
from config_noBDT import fileNameTTJets, fileNameWJets, xsecTTJets, xsecWJets, cut_EWKCR, fileNameEWKG, xsecEWKG
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


def getABCDData(fileName, cutA, cutB, cutC, cutD):
	fileThis = TFile(fileName)
	tree = fileThis.Get("DelayedPhoton")

	histA_NPU = TH1F("histA_NPU","",100,0,100)
	histB_NPU = TH1F("histB_NPU","",100,0,100)
	histC_NPU = TH1F("histC_NPU","",100,0,100)
	histD_NPU = TH1F("histD_NPU","",100,0,100)
	tree.Draw("NPU>>histA_NPU",cutA)
	tree.Draw("NPU>>histB_NPU",cutB)
	tree.Draw("NPU>>histC_NPU",cutC)
	tree.Draw("NPU>>histD_NPU",cutD)
	
	NA = tree.GetEntries(cutA)
        NB = tree.GetEntries(cutB)
        NC = tree.GetEntries(cutC)
        ND = tree.GetEntries(cutD)

	A = histA_NPU.Integral()
	B = histB_NPU.Integral()
	C = histC_NPU.Integral()
	D = histD_NPU.Integral()
	
	eA = A/np.sqrt(NA*1.0)
        eB = B/np.sqrt(NB*1.0)
        eC = C/np.sqrt(NC*1.0)
        eD = D/np.sqrt(ND*1.0)

	return A, B, C, D, eA, eB, eC, eD

def getABCDMC(fileName, cutA, cutB, cutC, cutD, lumiXsec):
	fileThis = TFile(fileName)
	tree = fileThis.Get("DelayedPhoton")
	hNEvents = fileThis.Get("NEvents")
        NEvents = hNEvents.GetBinContent(1)

	histA_NPU = TH1F("histA_NPU","",100,0,100)
	histB_NPU = TH1F("histB_NPU","",100,0,100)
	histC_NPU = TH1F("histC_NPU","",100,0,100)
	histD_NPU = TH1F("histD_NPU","",100,0,100)
	tree.Draw("NPU>>histA_NPU",cutA)
	tree.Draw("NPU>>histB_NPU",cutB)
	tree.Draw("NPU>>histC_NPU",cutC)
	tree.Draw("NPU>>histD_NPU",cutD)

	if histA_NPU.Integral() > 0:
		properScale(histA_NPU, lumiXsec/NEvents)
	if histB_NPU.Integral() > 0:
		properScale(histB_NPU, lumiXsec/NEvents)
	if histC_NPU.Integral() > 0:
		properScale(histC_NPU, lumiXsec/NEvents)
	if histD_NPU.Integral() > 0:
		properScale(histD_NPU, lumiXsec/NEvents)

	NA = tree.GetEntries(cutA)
	NB = tree.GetEntries(cutB)
	NC = tree.GetEntries(cutC)
	ND = tree.GetEntries(cutD)

	A = histA_NPU.Integral()
	B = histB_NPU.Integral()
	C = histC_NPU.Integral()
	D = histD_NPU.Integral()
	eA = A/np.sqrt(NA*1.0)
	eB = B/np.sqrt(NB*1.0)
	eC = C/np.sqrt(NC*1.0)
	eD = D/np.sqrt(ND*1.0)

	return A, B, C, D, eA, eB, eC, eD



boundaryTime = 1.0
boundaryMET = 150.0

ARegion = " && pho1ClusterTime_SmearToData < "+str(boundaryTime) + " && t1MET < "+ str(boundaryMET)
BRegion = " && pho1ClusterTime_SmearToData < "+str(boundaryTime) + " && t1MET > "+ str(boundaryMET)
CRegion = " && pho1ClusterTime_SmearToData > "+str(boundaryTime) + " && t1MET > "+ str(boundaryMET)
DRegion = " && pho1ClusterTime_SmearToData > "+str(boundaryTime) + " && t1MET < "+ str(boundaryMET)

cutA = cut + ARegion
cutB = cut + BRegion
cutC = cut + CRegion
cutD = cut + DRegion

cutA_GJets = cut_GJets + ARegion
cutB_GJets = cut_GJets + BRegion
cutC_GJets = cut_GJets + CRegion
cutD_GJets = cut_GJets + DRegion

cutA_QCD = cut_loose + " && !( " + cut +")" + ARegion
cutB_QCD = cut_loose + " && !( " + cut +")" + BRegion
cutC_QCD = cut_loose + " && !( " + cut +")" + CRegion
cutD_QCD = cut_loose + " && !( " + cut +")" + DRegion


cutA_EWK = cut_EWKCR + ARegion
cutB_EWK = cut_EWKCR + BRegion
cutC_EWK = cut_EWKCR + CRegion
cutD_EWK = cut_EWKCR + DRegion

weight_cutA = weight_cut + "(" + cutA + ")"
weight_cutB = weight_cut + "(" + cutB + ")"
weight_cutC = weight_cut + "(" + cutC + ")"
weight_cutD = weight_cut + "(" + cutD + ")"


def getABCD_yield():
	print weight_cutA
	print weight_cutB
	print weight_cutC
	print weight_cutD
	#signal, L = 400, CTau = 0.1
	xsec, exsec = getXsecBR(400, 0.1)
	A, B, C, D, eA, eB, eC, eD = getABCDMC("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", weight_cutA, weight_cutB, weight_cutC, weight_cutD, xsec*lumi)
	print "L400CTau0.1 & "+"%.4f"%A +"$\\pm$"+"%.4f"%eA+" & "+"%.4f"%B +"$\\pm$"+"%.4f"%eB+" & "+"%.4f"%C+"$\\pm$"+"%.4f"%eC+" & "+"%.4f"%D+"$\\pm$"+"%.4f"%eD+" & "+"%.4f"%(D*B/A)+"$\\pm$"+"%.4f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#signal, L = 400, CTau = 200
	xsec, exsec = getXsecBR(400, 200)
	A, B, C, D, eA, eB, eC, eD = getABCDMC("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", weight_cutA, weight_cutB, weight_cutC, weight_cutD, xsec*lumi)
	print "L400CTau200 & "+"%.4f"%A +"$\\pm$"+"%.4f"%eA+" & "+"%.4f"%B +"$\\pm$"+"%.4f"%eB+" & "+"%.4f"%C+"$\\pm$"+"%.4f"%eC+" & "+"%.4f"%D+"$\\pm$"+"%.4f"%eD+" & "+"%.4f"%(D*B/A)+"$\\pm$"+"%.4f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#signal, L = 400, CTau = 1200
	xsec, exsec = getXsecBR(400, 1200)
	A, B, C, D, eA, eB, eC, eD = getABCDMC("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau1200cm_13TeV-pythia8.root", weight_cutA, weight_cutB, weight_cutC, weight_cutD, xsec*lumi)
	print "L400CTau1200 & "+"%.4f"%A +"$\\pm$"+"%.4f"%eA+" & "+"%.4f"%B +"$\\pm$"+"%.4f"%eB+" & "+"%.4f"%C+"$\\pm$"+"%.4f"%eC+" & "+"%.4f"%D+"$\\pm$"+"%.4f"%eD+" & "+"%.4f"%(D*B/A)+"$\\pm$"+"%.4f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#data, GJets CR
	A, B, C, D, eA, eB, eC, eD = getABCDData("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", cutA_GJets, cutB_GJets, cutC_GJets, cutD_GJets)
	print "#gamma+Jets CR & "+"%.2f"%A +"$\\pm$"+"%.2f"%eA+" & "+"%.2f"%B +"$\\pm$"+"%.2f"%eB+" & "+"%.2f"%C+"$\\pm$"+"%.2f"%eC+" & "+"%.2f"%D+"$\\pm$"+"%.2f"%eD+" & "+"%.2f"%(D*B/A)+"$\\pm$"+"%.2f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#data, QCD CR
	A, B, C, D, eA, eB, eC, eD = getABCDData("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", cutA_QCD, cutB_QCD, cutC_QCD, cutD_QCD)
	print "QCD CR & "+"%.2f"%A +"$\\pm$"+"%.2f"%eA+" & "+"%.2f"%B +"$\\pm$"+"%.2f"%eB+" & "+"%.2f"%C+"$\\pm$"+"%.2f"%eC+" & "+"%.2f"%D+"$\\pm$"+"%.2f"%eD+" & "+"%.2f"%(D*B/A)+"$\\pm$"+"%.2f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#data, EWK CR
	A, B, C, D, eA, eB, eC, eD = getABCDData("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", cutA_EWK, cutB_EWK, cutC_EWK, cutD_EWK)
	print "EWK CR & "+"%.2f"%A +"$\\pm$"+"%.2f"%eA+" & "+"%.2f"%B +"$\\pm$"+"%.2f"%eB+" & "+"%.2f"%C+"$\\pm$"+"%.2f"%eC+" & "+"%.2f"%D+"$\\pm$"+"%.2f"%eD+" & "+"%.2f"%(D*B/A)+"$\\pm$"+"%.2f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)


	print "without correction......."

	#signal, L = 400, CTau = 0.1
	xsec, exsec = getXsecBR(400, 0.1)
	A, B, C, D, eA, eB, eC, eD = getABCDMC("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", weight_cutA, weight_cutB, weight_cutC, weight_cutD, xsec*lumi)
	print "L400CTau0.1 & "+"%.4f"%A +"$\\pm$"+"%.4f"%eA+" & "+"%.4f"%B +"$\\pm$"+"%.4f"%eB+" & "+"%.4f"%C+"$\\pm$"+"%.4f"%eC+" & "+"%.4f"%D+"$\\pm$"+"%.4f"%eD+" & "+"%.4f"%(D*B/A)+"$\\pm$"+"%.4f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#signal, L = 400, CTau = 200
	xsec, exsec = getXsecBR(400, 200)
	A, B, C, D, eA, eB, eC, eD = getABCDMC("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", weight_cutA, weight_cutB, weight_cutC, weight_cutD, xsec*lumi)
	print "L400CTau200 & "+"%.4f"%A +"$\\pm$"+"%.4f"%eA+" & "+"%.4f"%B +"$\\pm$"+"%.4f"%eB+" & "+"%.4f"%C+"$\\pm$"+"%.4f"%eC+" & "+"%.4f"%D+"$\\pm$"+"%.4f"%eD+" & "+"%.4f"%(D*B/A)+"$\\pm$"+"%.4f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#signal, L = 400, CTau = 1200
	xsec, exsec = getXsecBR(400, 1200)
	A, B, C, D, eA, eB, eC, eD = getABCDMC("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L400TeV_Ctau1200cm_13TeV-pythia8.root", weight_cutA, weight_cutB, weight_cutC, weight_cutD, xsec*lumi)
	print "L400CTau1200 & "+"%.4f"%A +"$\\pm$"+"%.4f"%eA+" & "+"%.4f"%B +"$\\pm$"+"%.4f"%eB+" & "+"%.4f"%C+"$\\pm$"+"%.4f"%eC+" & "+"%.4f"%D+"$\\pm$"+"%.4f"%eD+" & "+"%.4f"%(D*B/A)+"$\\pm$"+"%.4f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#data, GJets CR
	A, B, C, D, eA, eB, eC, eD = getABCDData("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", cutA_GJets, cutB_GJets, cutC_GJets, cutD_GJets)
	print "#gamma+Jets CR & "+"%.2f"%A +"$\\pm$"+"%.2f"%eA+" & "+"%.2f"%B +"$\\pm$"+"%.2f"%eB+" & "+"%.2f"%C+"$\\pm$"+"%.2f"%eC+" & "+"%.2f"%D+"$\\pm$"+"%.2f"%eD+" & "+"%.2f"%(D*B/A)+"$\\pm$"+"%.2f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#data, QCD CR
	A, B, C, D, eA, eB, eC, eD = getABCDData("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", cutA_QCD, cutB_QCD, cutC_QCD, cutD_QCD)
	print "QCD CR & "+"%.2f"%A +"$\\pm$"+"%.2f"%eA+" & "+"%.2f"%B +"$\\pm$"+"%.2f"%eB+" & "+"%.2f"%C+"$\\pm$"+"%.2f"%eC+" & "+"%.2f"%D+"$\\pm$"+"%.2f"%eD+" & "+"%.2f"%(D*B/A)+"$\\pm$"+"%.2f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)

	#data, EWK CR
	A, B, C, D, eA, eB, eC, eD = getABCDData("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", cutA_EWK, cutB_EWK, cutC_EWK, cutD_EWK)
	print "EWK CR & "+"%.2f"%A +"$\\pm$"+"%.2f"%eA+" & "+"%.2f"%B +"$\\pm$"+"%.2f"%eB+" & "+"%.2f"%C+"$\\pm$"+"%.2f"%eC+" & "+"%.2f"%D+"$\\pm$"+"%.2f"%eD+" & "+"%.2f"%(D*B/A)+"$\\pm$"+"%.2f"%np.sqrt((B*eD/A)**2 + (D*eB/A)**2 + (eA*D*B/(A*A))**2)



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
			legTime.AddEntry(histThis, str(MET_low)+" < #slash{E}_{T} < "+str(MET_high)+", cos = 1.00000", "lep")
	
		else:
			histThis.Draw("samehist")	
			cosThis = 0.0
                        if np.dot(histArray,histArray) > 0.0 and  np.dot(arrayTime[0],arrayTime[0]) > 0.0:
				cosThis = np.dot(arrayTime[0],histArray) / (np.sqrt(np.dot(histArray,histArray)) * np.sqrt(np.dot(arrayTime[0],arrayTime[0])))

			legTime.AddEntry(histThis, str(MET_low)+" < #slash{E}_{T} < "+str(MET_high)+", cos = %.5f"%cosThis, "lep")
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
			legMET.AddEntry(histThis, str(Time_low)+" < T < "+str(Time_high)+", cos = 1.00000", "lep")
	
		else:
			histThis.Draw("samehist")	
			cosThis = 0.0
			if np.dot(histArray,histArray) > 0.0 and  np.dot(arrayMET[0],arrayMET[0]) > 0.0:
				cosThis = np.dot(arrayMET[0],histArray) / (np.sqrt(np.dot(histArray,histArray)) * np.sqrt(np.dot(arrayMET[0],arrayMET[0])))

			legMET.AddEntry(histThis, str(Time_low)+" < T < "+str(Time_high)+", cos = %.5f"%cosThis, "lep")
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
			legTime.AddEntry(histThis, "random sample "+str(idx)+", cos = 1.00000", "lep")
	
		else:
			histThis.Draw("samehist")	
			cosThis = 0.0
                        if np.dot(histArray,histArray) > 0.0 and  np.dot(arrayTime[0],arrayTime[0]) > 0.0:
				cosThis = np.dot(arrayTime[0],histArray) / (np.sqrt(np.dot(histArray,histArray)) * np.sqrt(np.dot(arrayTime[0],arrayTime[0])))

			legTime.AddEntry(histThis, "random sample "+str(idx)+", cos = %.5f"%cosThis, "lep")
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
			legMET.AddEntry(histThis, "random sample "+str(idx)+", cos = 1.00000", "lep")
	
		else:
			histThis.Draw("samehist")	
			cosThis = 0.0
                        if np.dot(histArray,histArray) > 0.0 and  np.dot(arrayMET[0],arrayMET[0]) > 0.0:
				cosThis = np.dot(arrayMET[0],histArray) / (np.sqrt(np.dot(histArray,histArray)) * np.sqrt(np.dot(arrayMET[0],arrayMET[0])))

			legMET.AddEntry(histThis, "random sample "+str(idx)+", cos = %.5f"%cosThis, "lep")
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

drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "NoCorr_Data", cut, Timesplit, METsplit)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "NoCorr_Data", cut, 6)

drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "L400TeV_CtauAll", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "L400TeV_CtauAll", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "L400TeV_Ctau200cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "L200TeV_Ctau200cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L100TeV_Ctau200cm_13TeV-pythia8.root", "L100TeV_Ctau200cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root", "L200TeV_Ctau0_1cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10cm_13TeV-pythia8.root", "L200TeV_Ctau10cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "L200TeV_Ctau10000cm", cut, Timesplit, METsplit)

drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "L400TeV_CtauAll", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "L400TeV_CtauAll", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "L400TeV_Ctau200cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "L200TeV_Ctau200cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L100TeV_Ctau200cm_13TeV-pythia8.root", "L100TeV_Ctau200cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root", "L200TeV_Ctau0_1cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10cm_13TeV-pythia8.root", "L200TeV_Ctau10cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "L200TeV_Ctau10000cm", cut, 6)

drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "Data", cut, Timesplit, METsplit)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "Data", cut, 6)


drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L400TeV_Ctau200cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau200cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L100TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L100TeV_Ctau200cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau0_1cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau10cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau10cm", cut, Timesplit, METsplit)
drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau10000cm", cut, Timesplit, METsplit)

drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L400TeV_Ctau200cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau200cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L100TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L100TeV_Ctau200cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau0_1cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau10cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau10cm", cut, 6)
drawTimeAndMETShapesRandN("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau10000cm", cut, 6)


getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "L400TeV_CtauAll", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "L400TeV_CtauAll", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "L400TeV_Ctau200cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "L200TeV_Ctau200cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L100TeV_Ctau200cm_13TeV-pythia8.root", "L100TeV_Ctau200cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root", "L200TeV_Ctau0_1cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10cm_13TeV-pythia8.root", "L200TeV_Ctau10cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "L200TeV_Ctau10000cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "Data", cut, Timesplit, METsplit)

getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L400TeV_Ctau200cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau200cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L100TeV_Ctau200cm_13TeV-pythia8.root", "NoCorr_L100TeV_Ctau200cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau0_1cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau10cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau10cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "NoCorr_L200TeV_Ctau10000cm", cut, Timesplit, METsplit)
getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "NoCorr_Data", cut, Timesplit, METsplit)


