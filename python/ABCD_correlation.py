from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TH2F
import os, sys
from Aux import *
from config_noBDT import cut, cut_GJets, cut_QCD_CR, cut_EWKCR, cut_noDisc, cut_noSigmaIetaIeta, cut_GJets_noSigmaIetaIeta, splots, lumi, outputDir, cut_noSminor, cut_GJets_noSminor, cut_blindMET, cut_blindTime, cut_MET_filter
from config_noBDT import fractionGJets, fractionQCD, useFraction, kFactor, sigLegend, weight_cut
import numpy as np
import array

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir+"/METCorrPlots")
os.system("mkdir -p "+outputDir+"/METCorrPlots")
os.system("cp config_noBDT.py "+outputDir+"/METCorrPlots/")
os.system("cp METCorrPlot.py "+outputDir+"/METCorrPlots/")
#################plot settings###########################
axisTitleSize = 0.035
axisTitleOffset = 1.1
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
                ev0 = hist.GetBinError(i)
                hist.SetBinContent(i, norm*v0)
                if v0 > 0.0000001:
                        hist.SetBinError(i, norm*ev0)
                else:
                        hist.SetBinError(i, 0.0)
def widthScale(hist):
        for i in range(0, hist.GetNbinsX()+1):
		norm = 1.0/hist.GetBinWidth(i)
                v0 = hist.GetBinContent(i)
                ev0 = hist.GetBinError(i)
                hist.SetBinContent(i, norm*v0)
                if v0 > 0.0000001:
                        hist.SetBinError(i, norm*ev0)
                else:
                        hist.SetBinError(i, 0.0)


def drawTimeAndMETShapesSR(fileNameData, fileNameMC, label, cutsig, Timesplit, METsplit, xsecSig, sigModel, doScale, doWidthScale):
	print "reding data tree"
        fileData = TFile(fileNameData)
        treeData = fileData.Get("DelayedPhoton")
	print "reding signal tree"

        fileMC = TFile(fileNameMC)
        treeMC = fileMC.Get("DelayedPhoton")
        hNEventsSig = fileMC.Get("NEvents")
        NEventsSig = hNEventsSig.GetBinContent(1)
	
	unitY_time = "< Events / ns >"
	if not doWidthScale:
		unitY_time = "Events"
	unitY_met = "< Events / GeV >"
	if not doWidthScale:
		unitY_met = "Events"

        timeBins = [-2, -1.5, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 5, 10, 15, 25]
        metBins = [0.0, 20.0, 40.0, 60, 80, 100, 150, 200, 250, 300, 400, 500, 750, 1000, 3000]
	if not doWidthScale:
		metBins = [0.0, 20.0, 40.0, 60, 80, 100, 150, 200, 250, 300, 400, 500, 1000, 3000]
        colors = [633, 600, 400, 416, 600, 880, 54, 13, 18, 80, 57, 60, 64, 67, 8, 80, 91, 93, 97,  2, 18, 16, 13]
        histTime_Data = []
        histTime_MC = []
        histMET_Data = []
        histMET_MC = []

        myC = TCanvas( "myC", "myC",0, 0, 700, 600)
	myC.SetFillColor(0)
	myC.SetBorderMode(0)
	myC.SetBorderSize(2)
	myC.SetLogy()
	myC.SetTickx(1)
	myC.SetTicky(1)
	myC.SetLeftMargin(0.18)
	myC.SetRightMargin(0.15)
	myC.SetTopMargin(0.05)
	myC.SetBottomMargin(0.14)
	myC.SetFrameFillStyle(0)
	myC.SetFrameBorderMode(0)
	myC.SetFrameFillStyle(0)
	myC.SetFrameBorderMode(0)

        legTime = TLegend(0.3, 0.755, 0.82, 0.92)
        legTime.SetBorderSize(0)
        legTime.SetTextFont(42)
        legTime.SetLineColor(1)
        legTime.SetLineStyle(1)
        legTime.SetLineWidth(1)
        legTime.SetFillColor(0)
        legTime.SetFillStyle(1001)
        maxYTime = 0.0
        minYTime = 999

        for idx in range(1,len(METsplit)):
		print "draw Time histogram of METsplit "+str(idx)
                MET_low = METsplit[idx-1]
                MET_high = METsplit[idx]
                cutThis = cutsig + " && t1MET < "+ str(MET_high)+ " && t1MET > "+ str(MET_low)
                histThis_Data = TH1F("histTime_Data_idx"+str(idx), "; t^{#gamma} (ns); "+unitY_time, len(timeBins)-1, np.array(timeBins))
                treeData.Draw("pho1ClusterTime_SmearToData>>histTime_Data_idx"+str(idx), cutThis)
                if doWidthScale:
			#histThis_Data.Scale(1.0, "width")
			widthScale(histThis_Data)
                if(histThis_Data.GetMaximum() > maxYTime):
                        maxYTime = histThis_Data.GetMaximum()
                if(histThis_Data.GetMinimum() < minYTime):
                        minYTime = histThis_Data.GetMinimum()
                histThis_Data.SetMarkerStyle(20)
                histThis_Data.SetLineWidth(2)
                histThis_Data.SetLineColor(colors[idx-1])
                histThis_Data.SetMarkerColor(colors[idx-1])
                histTime_Data.append(histThis_Data)

                cutThis_weighted = weight_cut + "(" + cutThis + ")"
                histThis_MC = TH1F("histTime_MC_idx"+str(idx), "; t^{#gamma} (ns); "+unitY_time, len(timeBins)-1, np.array(timeBins))
                treeMC.Draw("pho1ClusterTime_SmearToData>>histTime_MC_idx"+str(idx), cutThis_weighted)
                properScale(histThis_MC, lumi*xsecSig/NEventsSig)
		if doWidthScale:
			#histThis_MC.Scale(1.0, "width")
			widthScale(histThis_MC)
                if(histThis_MC.GetMaximum() > maxYTime):
                        maxYTime = histThis_MC.GetMaximum()
                if(histThis_MC.GetMinimum() < minYTime):
                        minYTime = histThis_MC.GetMinimum()
                histThis_MC.SetLineStyle(9)
                histThis_MC.SetLineWidth(2)
                histThis_MC.SetLineColor(1)
                histThis_MC.SetMarkerColor(1)
                histTime_MC.append(histThis_MC)
        scaleFactor = histTime_Data[1].Integral()/histTime_Data[0].Integral()
        if doScale:
                properScale(histTime_Data[0], scaleFactor)

	histTime_Data[0].GetXaxis().SetTitleSize( axisTitleSize )
        histTime_Data[0].GetXaxis().SetTitleOffset( axisTitleOffset )
        histTime_Data[0].GetYaxis().SetTitleSize( axisTitleSize )
        histTime_Data[0].GetYaxis().SetTitleOffset( axisTitleOffset )
        histTime_Data[0].GetXaxis().SetTitleFont(42)
        histTime_Data[0].GetXaxis().SetLabelFont(42)
        histTime_Data[0].GetYaxis().SetTitleFont(42)
        histTime_Data[0].GetYaxis().SetLabelFont(42)
        histTime_Data[0].Draw("ep")
        histTime_Data[1].Draw("epsame")
        #histTime_MC[0].Draw("histsame")
        histTime_MC[1].Draw("histsame")

        if doScale:
		legTime.AddEntry(histTime_Data[0], "Data [p_{T}^{miss} < "+str(METsplit[1])+" GeV] (Scaled x %.3f"%scaleFactor+")", "lep")
        else:
		legTime.AddEntry(histTime_Data[0], "Data [p_{T}^{miss} < "+str(METsplit[1])+" GeV]", "lep")
	legTime.AddEntry(histTime_Data[1], "Data [p_{T}^{miss} #geq "+str(METsplit[1])+" GeV]", "lep")
        #legTime.AddEntry(histTime_MC[0], "GMSB "+sigModel+" [p_{T}^{miss} < "+str(METsplit[1])+" GeV]", "l")
        legTime.AddEntry(histTime_MC[1], "GMSB "+sigModel+" [p_{T}^{miss} #geq "+str(METsplit[1])+" GeV]", "l")

        if minYTime < 1e-2:
                minYTime = 1e-2
        #histTime_Data[0].GetYaxis().SetRangeUser(0.1*minYTime, 50*maxYTime)
        histTime_Data[0].GetYaxis().SetRangeUser(1e-3, 1e5)
        legTime.Draw()
	drawCMS3(myC, 13, lumi)
        myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_in_METbins_"+label+".pdf")
        myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_in_METbins_"+label+".png")
        myC.SaveAs(outputDir+"/METCorrPlots/Timeshapes_in_METbins_"+label+".C")
	
	NBinsTime = len(timeBins)-1
	file_Time = open(outputDir+"/METCorrPlots/Timeshapes_in_METbins_"+label+".txt", "w")
	for idx in range(NBinsTime):
		print >> file_Time, "Data_Hist_L Content "+str(idx+1)+" "+str(histTime_Data[0].GetBinContent(idx+1))
	for idx in range(NBinsTime):
		print >> file_Time, "Data_Hist_L Error "+str(idx+1)+" "+str(histTime_Data[0].GetBinError(idx+1))
	print >> file_Time, "Data_Hist_L Entries "+str(histTime_Data[0].GetEntries())
	print >> file_Time, "\n"

	for idx in range(NBinsTime):
		print >> file_Time, "Data_Hist_R Content "+str(idx+1)+" "+str(histTime_Data[1].GetBinContent(idx+1))
	for idx in range(NBinsTime):
		print >> file_Time, "Data_Hist_R Error "+str(idx+1)+" "+str(histTime_Data[1].GetBinError(idx+1))
	print >> file_Time, "Data_Hist_R Entries "+str(histTime_Data[1].GetEntries())
	print >> file_Time, "\n"


	for idx in range(NBinsTime):
		print >> file_Time, "GMSB_Hist Content "+str(idx+1)+" "+str(histTime_MC[1].GetBinContent(idx+1))
	for idx in range(NBinsTime):
		print >> file_Time, "GMSB_Hist Error "+str(idx+1)+" "+str(histTime_MC[1].GetBinError(idx+1))
	print >> file_Time, "GMSB_Hist Entries "+str(histTime_MC[1].GetEntries())



        legMET = TLegend(0.3, 0.755, 0.82, 0.92)
        legMET.SetBorderSize(0)
        legMET.SetTextFont(42)
        legMET.SetLineColor(1)
        legMET.SetLineStyle(1)
        legMET.SetLineWidth(1)
        legMET.SetFillColor(0)
        legMET.SetFillStyle(1001)
        maxYMET = 0.0
        minYMET = 999

        for idx in range(1,len(Timesplit)):
		print "draw MET histogram of Timesplit "+str(idx)
                Time_low = Timesplit[idx-1]
                Time_high = Timesplit[idx]
		cutThis = cutsig + " && pho1ClusterTime_SmearToData < "+ str(Time_high)+ " && pho1ClusterTime_SmearToData > "+ str(Time_low)
		histThis_Data = TH1F("histMET_Data_idx"+str(idx), "; p_{T}^{miss} (GeV); "+unitY_met, len(metBins)-1, np.array(metBins))
                treeData.Draw("t1MET>>histMET_Data_idx"+str(idx), cutThis)
		if doWidthScale:
			#histThis_Data.Scale(1.0, "width")
			widthScale(histThis_Data)
		if not doWidthScale:
			histThis_Data.SetBinContent(len(metBins)-2, histThis_Data.GetBinContent(len(metBins)-2) + histThis_Data.GetBinContent(len(metBins)-1))
                if(histThis_Data.GetMaximum() > maxYMET):
                        maxYMET = histThis_Data.GetMaximum()
                if(histThis_Data.GetMinimum() < minYMET):
                        minYMET = histThis_Data.GetMinimum()
                histThis_Data.SetMarkerStyle(20)
                histThis_Data.SetLineWidth(2)
                histThis_Data.SetLineColor(colors[idx-1])
                histThis_Data.SetMarkerColor(colors[idx-1])
                histMET_Data.append(histThis_Data)

                cutThis_weighted = weight_cut + "(" + cutThis + ")"
		histThis_MC = TH1F("histMET_MC_idx"+str(idx), "; p_{T}^{miss} (GeV); "+unitY_met, len(metBins)-1, np.array(metBins))
                treeMC.Draw("t1MET>>histMET_MC_idx"+str(idx), cutThis_weighted)
                properScale(histThis_MC, lumi*xsecSig/NEventsSig)

		if doWidthScale:
			#histThis_MC.Scale(1.0, "width")
			widthScale(histThis_MC)
		if not doWidthScale:
			histThis_MC.SetBinContent(len(metBins)-2, histThis_MC.GetBinContent(len(metBins)-2) + histThis_MC.GetBinContent(len(metBins)-1))
                if(histThis_MC.GetMaximum() > maxYMET):
                        maxYMET = histThis_MC.GetMaximum()
                if(histThis_MC.GetMinimum() < minYMET):
                        minYMET = histThis_MC.GetMinimum()
                histThis_MC.SetLineStyle(9)
                histThis_MC.SetLineWidth(2)
                histThis_MC.SetLineColor(1)
                histThis_MC.SetMarkerColor(1)
                histMET_MC.append(histThis_MC)
        scaleFactor = histMET_Data[1].Integral()/histMET_Data[0].Integral()
        if doScale:
                properScale(histMET_Data[0], scaleFactor)
	histMET_Data[0].GetXaxis().SetTitleSize( axisTitleSize )
        histMET_Data[0].GetXaxis().SetTitleOffset( axisTitleOffset )
        histMET_Data[0].GetYaxis().SetTitleSize( axisTitleSize )
        histMET_Data[0].GetYaxis().SetTitleOffset( axisTitleOffset )
        histMET_Data[0].GetXaxis().SetTitleFont(42)
        histMET_Data[0].GetXaxis().SetLabelFont(42)
        histMET_Data[0].GetYaxis().SetTitleFont(42)
        histMET_Data[0].GetYaxis().SetLabelFont(42)
        histMET_Data[0].Draw("ep")
        histMET_Data[1].Draw("epsame")
        #histMET_MC[0].Draw("histsame")
        histMET_MC[1].Draw("histsame")

        if doScale:
                #legMET.AddEntry(histMET_Data[1], "Data [T #geq "+str(Timesplit[1])+" ns] (Scaled x %.1f"%scaleFactor+")", "lep")
		legMET.AddEntry(histMET_Data[0], "Data [T < "+str(Timesplit[1])+" ns] (Scaled x %.3f"%scaleFactor+")", "lep")
        else:
		legMET.AddEntry(histMET_Data[0], "Data [T < "+str(Timesplit[1])+" ns]", "lep")
	legMET.AddEntry(histMET_Data[1], "Data [T #geq "+str(Timesplit[1])+" ns]", "lep")
        #legMET.AddEntry(histMET_MC[0], "GMSB "+sigModel+" [T < "+str(Timesplit[1])+" ns]", "l")
        legMET.AddEntry(histMET_MC[1], "GMSB "+sigModel+" [T #geq "+str(Timesplit[1])+" ns]", "l")

        if minYMET < 1e-2:
                minYMET = 1e-2
        histMET_Data[0].GetYaxis().SetRangeUser(0.1*minYMET, 50*maxYMET)
	if not doWidthScale:
		histMET_Data[0].GetXaxis().SetRangeUser(metBins[0], metBins[-2])
        legMET.Draw()
	drawCMS3(myC, 13, lumi)
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_in_Timebins_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_in_Timebins_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/METshapes_in_Timebins_"+label+".C")
	
	NBinsMET = len(metBins)-1
	if not doWidthScale:
		NBinsMET = len(metBins)-2
	file_MET = open(outputDir+"/METCorrPlots/METshapes_in_Timebins_"+label+".txt", "w")
	for idx in range(NBinsMET):
		print >> file_MET, "Data_Hist_L Content "+str(idx+1)+" "+str(histMET_Data[0].GetBinContent(idx+1))
	for idx in range(NBinsMET):
		print >> file_MET, "Data_Hist_L Error "+str(idx+1)+" "+str(histMET_Data[0].GetBinError(idx+1))
	print >> file_MET, "Data_Hist_L Entries "+str(histMET_Data[0].GetEntries())
	print >> file_MET, "\n"

	for idx in range(NBinsMET):
		print >> file_MET, "Data_Hist_R Content "+str(idx+1)+" "+str(histMET_Data[1].GetBinContent(idx+1))
	for idx in range(NBinsMET):
		print >> file_MET, "Data_Hist_R Error "+str(idx+1)+" "+str(histMET_Data[1].GetBinError(idx+1))
	print >> file_MET, "Data_Hist_R Entries "+str(histMET_Data[1].GetEntries())

	print >> file_MET, "\n"

	for idx in range(NBinsMET):
		print >> file_MET, "GMSB_Hist Content "+str(idx+1)+" "+str(histMET_MC[1].GetBinContent(idx+1))
	for idx in range(NBinsMET):
		print >> file_MET, "GMSB_Hist Error "+str(idx+1)+" "+str(histMET_MC[1].GetBinError(idx+1))
	print >> file_MET, "GMSB_Hist Entries "+str(histMET_MC[1].GetEntries())


def drawRatiosVsSplitTimeAndMET(fileName, label, cutsig, Timesplit, METsplit):
	fileThis = TFile(fileName)
        tree = fileThis.Get("DelayedPhoton")

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
	xbins_MET = np.arange(0,500.0,10.0)
	xbins_time = np.arange(-2.0, 8.0, 0.25)

	#draw ratio of high Time and low Time events in bins of MET
	hist_ratio1_MET = TH1F("hist_ratio1_MET","; p_{T}^{miss} split [GeV]; ratio ( time split ="+str(Timesplit)+"ns )", len(xbins_MET)-1, np.array(xbins_MET)) 	
	hist_ratio2_MET = TH1F("hist_ratio2_MET","; p_{T}^{miss} split [GeV]; ratio ( time split ="+str(Timesplit)+"ns )", len(xbins_MET)-1, np.array(xbins_MET)) 	
	cut_highTime = cutsig + " && pho1ClusterTime_SmearToData > "+ str(Timesplit)+ " && pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"
	cut_lowTime = cutsig + " && pho1ClusterTime_SmearToData < "+ str(Timesplit)+ " && pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"
	hist_highTime_MET = TH1F("hist_highTime_MET","hist_highTime_MET", len(xbins_MET)-1, np.array(xbins_MET)) 	
	hist_lowTime_MET = TH1F("hist_lowTime_MET","hist_lowTime_MET", len(xbins_MET)-1, np.array(xbins_MET)) 	
	tree.Draw("t1MET>>hist_highTime_MET", cut_highTime)
	tree.Draw("t1MET>>hist_lowTime_MET", cut_lowTime)
	Ntotal_highTime = hist_highTime_MET.Integral()
	Ntotal_lowTime = hist_lowTime_MET.Integral()

	for idx in range(len(xbins_MET)-1):
		N1 = hist_highTime_MET.Integral(1, idx+1)
		N2 = hist_lowTime_MET.Integral(1, idx+1)
		N1p = Ntotal_highTime - N1
		N2p = Ntotal_lowTime - N2

		if N2 > 0:
			hist_ratio1_MET.SetBinContent(idx+1, N1*1.0/N2)
			if  N1 > 0:
				hist_ratio1_MET.SetBinError(idx+1, N1*1.0/N2*np.sqrt(1.0/N1 + 1.0/N2))
			else:
				hist_ratio1_MET.SetBinError(idx+1, 0)
		else:
			hist_ratio1_MET.SetBinContent(idx+1, 0)
			hist_ratio1_MET.SetBinError(idx+1, 0)

		if N2p > 0:
			hist_ratio2_MET.SetBinContent(idx+1, N1p*1.0/N2p)
			if  N1p > 0:
				hist_ratio2_MET.SetBinError(idx+1, N1p*1.0/N2p*np.sqrt(1.0/N1p + 1.0/N2p))
			else:
				hist_ratio2_MET.SetBinError(idx+1, 0)
		else:
			hist_ratio2_MET.SetBinContent(idx+1, 0)
			hist_ratio2_MET.SetBinError(idx+1, 0)

	hist_ratio1_MET.SetLineWidth(2)
	hist_ratio1_MET.SetLineColor(kRed)
	hist_ratio1_MET.SetMarkerColor(kRed)
	hist_ratio1_MET.GetXaxis().SetTitleSize( axisTitleSize )
	hist_ratio1_MET.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_ratio1_MET.GetYaxis().SetTitleSize( axisTitleSize - 0.02 )
	hist_ratio1_MET.GetYaxis().SetTitleOffset( axisTitleOffset + 0.7)
	hist_ratio1_MET.GetXaxis().SetRangeUser(0.0, 500.0)
	hist_ratio1_MET.Draw("ep")
	#hist_ratio1_MET.GetYaxis().SetRangeUser(0.5*hist_ratio1_MET.GetBinContent(10), 3.0*hist_ratio1_MET.GetBinContent(10))
	hist_ratio1_MET.GetYaxis().SetRangeUser(0.0*hist_ratio1_MET.GetBinContent(10), 5.0*hist_ratio1_MET.GetBinContent(10))

	hist_ratio2_MET.SetLineWidth(2)
	hist_ratio2_MET.SetLineColor(kBlue)
	hist_ratio2_MET.SetMarkerColor(kBlue)
	hist_ratio2_MET.Draw("epsame")
	
	legMET = TLegend(0.5, 0.7, 0.93, 0.92)
        legMET.SetBorderSize(0)
        legMET.SetTextFont(62)
        legMET.SetLineColor(1)
        legMET.SetLineStyle(1)
        legMET.SetLineWidth(1)
        legMET.SetFillColor(0)
        legMET.SetFillStyle(1001)
	legMET.AddEntry(hist_ratio1_MET, "D(high time)/A(low time)", "lep")
	legMET.AddEntry(hist_ratio2_MET, "C(high time)/B(low time)", "lep")
	legMET.Draw()

	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highTime_vs_lowTime_vs_METsplit_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highTime_vs_lowTime_vs_METsplit_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highTime_vs_lowTime_vs_METsplit_"+label+".C")


	#draw ratio of high MET and low MET events in bins of Time
	hist_ratio1_Time = TH1F("hist_ratio1_Time","; time split [ns]; ratio ( p_{T}^{miss} split = "+str(METsplit)+"GeV )", len(xbins_time)-1, np.array(xbins_time)) 	
	hist_ratio2_Time = TH1F("hist_ratio2_Time","; time split [ns]; ratio ( p_{T}^{miss} split = "+str(METsplit)+"GeV )", len(xbins_time)-1, np.array(xbins_time)) 	
	cut_highMET = cutsig + " && t1MET > "+ str(METsplit)
	cut_lowMET = cutsig + " && t1MET < "+ str(METsplit)
	hist_highMET_Time = TH1F("hist_highMET_Time","hist_highMET_Time", len(xbins_time)-1, np.array(xbins_time)) 	
	hist_lowMET_Time = TH1F("hist_lowMET_Time","hist_lowMET_Time", len(xbins_time)-1, np.array(xbins_time)) 	
	tree.Draw("pho1ClusterTime_SmearToData>>hist_highMET_Time", cut_highMET)
	tree.Draw("pho1ClusterTime_SmearToData>>hist_lowMET_Time", cut_lowMET)
	Ntotal_highMET = hist_highMET_Time.Integral()
	Ntotal_lowMET = hist_lowMET_Time.Integral()

	for idx in range(len(xbins_time)-1):
		N1 = hist_highMET_Time.Integral(1, idx+1)
		N2 = hist_lowMET_Time.Integral(1, idx+1)
		N1p = Ntotal_highMET - N1
		N2p = Ntotal_lowMET - N2
	
		if N2 > 0:
			hist_ratio1_Time.SetBinContent(idx+1, N1*1.0/N2)
			if  N1 > 0:
				hist_ratio1_Time.SetBinError(idx+1, N1*1.0/N2*np.sqrt(1.0/N1 + 1.0/N2))
			else:
				hist_ratio1_Time.SetBinError(idx+1, 0)
		else:
			hist_ratio1_Time.SetBinContent(idx+1, 0)
			hist_ratio1_Time.SetBinError(idx+1, 0)
	
		if N2p > 0:
			hist_ratio2_Time.SetBinContent(idx+1, N1p*1.0/N2p)
			if  N1p > 0:
				hist_ratio2_Time.SetBinError(idx+1, N1p*1.0/N2p*np.sqrt(1.0/N1p + 1.0/N2p))
			else:
				hist_ratio2_Time.SetBinError(idx+1, 0)
		else:
			hist_ratio2_Time.SetBinContent(idx+1, 0)
			hist_ratio2_Time.SetBinError(idx+1, 0)


	hist_ratio1_Time.SetLineWidth(2)
	hist_ratio1_Time.SetLineColor(kRed)
	hist_ratio1_Time.SetMarkerColor(kRed)
	hist_ratio1_Time.GetXaxis().SetTitleSize( axisTitleSize )
	hist_ratio1_Time.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_ratio1_Time.GetYaxis().SetTitleSize( axisTitleSize - 0.02 )
	hist_ratio1_Time.GetYaxis().SetTitleOffset( axisTitleOffset + 0.7)
	hist_ratio1_Time.GetXaxis().SetRangeUser(-2.0, 8.0)
	hist_ratio1_Time.Draw("ep")
	hist_ratio1_Time.GetYaxis().SetRangeUser(0.0*hist_ratio1_Time.GetBinContent(10), 5.0*hist_ratio1_Time.GetBinContent(10))

	hist_ratio2_Time.SetLineWidth(2)
	hist_ratio2_Time.SetLineColor(kBlue)
	hist_ratio2_Time.SetMarkerColor(kBlue)
	hist_ratio2_Time.Draw("epsame")

	legTime = TLegend(0.5, 0.7, 0.93, 0.92)
        legTime.SetBorderSize(0)
        legTime.SetTextFont(62)
        legTime.SetLineColor(1)
        legTime.SetLineStyle(1)
        legTime.SetLineWidth(1)
        legTime.SetFillColor(0)
        legTime.SetFillStyle(1001)
	legTime.AddEntry(hist_ratio1_Time, "B(hith MET)/A(low MET)", "lep")
	legTime.AddEntry(hist_ratio2_Time, "C(high MET)/D(low MET)", "lep")
	legTime.Draw()


	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highMET_vs_lowMET_vs_Timesplit_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highMET_vs_lowMET_vs_Timesplit_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highMET_vs_lowMET_vs_Timesplit_"+label+".C")



def drawRatiosVsTimeAndMET(fileName, label, cutsig, Timesplit, METsplit):
	fileThis = TFile(fileName)
        tree = fileThis.Get("DelayedPhoton")

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
	xbins_MET = [0.0, 10.0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 250.0, 500.0, 1000.0, 3000.0]
	xbins_time = [-5.0, -3, -2, -1.5, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 1.5, 2.0, 8.0, 25.0]

	#draw ratio of high Time and low Time events in bins of MET
	hist_ratio_MET = TH1F("hist_ratio_MET","; p_{T}^{miss} [GeV]; N(t > "+str(Timesplit)+"ns)/N(t < "+str(Timesplit)+"ns)", len(xbins_MET)-1, np.array(xbins_MET)) 	
	cut_highTime = cutsig + " && pho1ClusterTime_SmearToData > "+ str(Timesplit)+ " && pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"
	cut_lowTime = cutsig + " && pho1ClusterTime_SmearToData < "+ str(Timesplit)+ " && pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"
	hist_highTime_MET = TH1F("hist_highTime_MET","hist_highTime_MET", len(xbins_MET)-1, np.array(xbins_MET)) 	
	hist_lowTime_MET = TH1F("hist_lowTime_MET","hist_lowTime_MET", len(xbins_MET)-1, np.array(xbins_MET)) 	
	tree.Draw("t1MET>>hist_highTime_MET", cut_highTime)
	tree.Draw("t1MET>>hist_lowTime_MET", cut_lowTime)
	for idx in range(len(xbins_MET)-1):
		N1 = hist_highTime_MET.GetBinContent(idx+1)
		N2 = hist_lowTime_MET.GetBinContent(idx+1)
		if N2 > 0:
			hist_ratio_MET.SetBinContent(idx+1, N1*1.0/N2)
			if  N1 > 0:
				hist_ratio_MET.SetBinError(idx+1, N1*1.0/N2*np.sqrt(1.0/N1 + 1.0/N2))
			else:
				hist_ratio_MET.SetBinError(idx+1, 0)
		else:
			hist_ratio_MET.SetBinContent(idx+1, 0)
			hist_ratio_MET.SetBinError(idx+1, 0)
	hist_ratio_MET.SetLineWidth(2)
	hist_ratio_MET.SetLineColor(kBlack)
	hist_ratio_MET.SetMarkerColor(kBlack)
	hist_ratio_MET.GetXaxis().SetTitleSize( axisTitleSize )
	hist_ratio_MET.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_ratio_MET.GetYaxis().SetTitleSize( axisTitleSize - 0.02 )
	hist_ratio_MET.GetYaxis().SetTitleOffset( axisTitleOffset + 0.7)
	hist_ratio_MET.GetXaxis().SetRangeUser(0.0, 500.0)
	hist_ratio_MET.Fit("pol1")
	hist_ratio_MET.Draw("ep")
	hist_ratio_MET.GetYaxis().SetRangeUser(0.0, 3.0*hist_ratio_MET.GetBinContent(3))
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highTime_vs_lowTime_in_METbins_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highTime_vs_lowTime_in_METbins_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highTime_vs_lowTime_in_METbins_"+label+".C")


	#draw ratio of high MET and low MET events in bins of Time
	hist_ratio_Time = TH1F("hist_ratio_Time","; #gamma cluster time [ns]; N(p_{T}^{miss} > "+str(METsplit)+"GeV)/N(p_{T}^{miss} < "+str(METsplit)+"GeV)", len(xbins_time)-1, np.array(xbins_time)) 	
	cut_highMET = cutsig + " && t1MET > "+ str(METsplit)
	cut_lowMET = cutsig + " && t1MET < "+ str(METsplit)
	hist_highMET_Time = TH1F("hist_highMET_Time","hist_highMET_Time", len(xbins_time)-1, np.array(xbins_time)) 	
	hist_lowMET_Time = TH1F("hist_lowMET_Time","hist_lowMET_Time", len(xbins_time)-1, np.array(xbins_time)) 	
	tree.Draw("pho1ClusterTime_SmearToData>>hist_highMET_Time", cut_highMET)
	tree.Draw("pho1ClusterTime_SmearToData>>hist_lowMET_Time", cut_lowMET)
	for idx in range(len(xbins_time)-1):
		N1 = hist_highMET_Time.GetBinContent(idx+1)
		N2 = hist_lowMET_Time.GetBinContent(idx+1)
		if N2 > 0:
			hist_ratio_Time.SetBinContent(idx+1, N1*1.0/N2)
			if  N1 > 0:
				hist_ratio_Time.SetBinError(idx+1, N1*1.0/N2*np.sqrt(1.0/N1 + 1.0/N2))
			else:
				hist_ratio_Time.SetBinError(idx+1, 0)
		else:
			hist_ratio_Time.SetBinContent(idx+1, 0)
			hist_ratio_Time.SetBinError(idx+1, 0)
	print hist_ratio_Time.Integral()
	hist_ratio_Time.SetLineWidth(2)
	hist_ratio_Time.SetLineColor(kBlack)
	hist_ratio_Time.SetMarkerColor(kBlack)
	hist_ratio_Time.GetXaxis().SetTitleSize( axisTitleSize )
	hist_ratio_Time.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_ratio_Time.GetYaxis().SetTitleSize( axisTitleSize - 0.02 )
	hist_ratio_Time.GetYaxis().SetTitleOffset( axisTitleOffset + 0.7)
	hist_ratio_Time.GetXaxis().SetRangeUser(-2.0, 8.0)
	hist_ratio_Time.Fit("pol1")
	hist_ratio_Time.Draw("ep")
	#hist_ratio_Time.GetYaxis().SetRangeUser(0.0, 5.0*hist_ratio_Time.GetBinContent(8))
	hist_ratio_Time.GetYaxis().SetRangeUser(0.0, 0.25)
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highMET_vs_lowMET_in_Timebins_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highMET_vs_lowMET_in_Timebins_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/ratio_highMET_vs_lowMET_in_Timebins_"+label+".C")



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
	
	legTime = TLegend(0.18, 0.7, 0.93, 0.92)
        legTime.SetNColumns(2)
        legTime.SetBorderSize(0)
        legTime.SetTextSize(0.025)
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
		histThis = TH1F("histTime_idx"+str(idx), "; #gamma cluster time (ns); Events", 100, -25., 25.)
		#histThis = TH1F("histTime_idx"+str(idx), "; #gamma cluster time (ns); Events", 20, -2., 8.)
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
	if minYTime < 1e-6:
		minYTime = 1e-6
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
		histThis = TH1F("histTime_idx"+str(idx), "; #gamma cluster time (ns); Events", 20, -2., 8.)
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



def runClosureTests(fileName, label, cutsig, timeSplit, metSplit):
	print "closure tests in "+label
	print "cut ==== "
	print cutsig
	fileThis = TFile(fileName)
        tree = fileThis.Get("DelayedPhoton")

	for idx in range(len(timeSplit)):
		boundaryTime = timeSplit[idx]
		boundaryMET = metSplit[idx]
		ARegion = " && pho1ClusterTime_SmearToData < "+str(boundaryTime) + " && t1MET < "+ str(boundaryMET)
		BRegion = " && pho1ClusterTime_SmearToData < "+str(boundaryTime) + " && t1MET > "+ str(boundaryMET)
		CRegion = " && pho1ClusterTime_SmearToData > "+str(boundaryTime) + " && t1MET > "+ str(boundaryMET)
		DRegion = " && pho1ClusterTime_SmearToData > "+str(boundaryTime) + " && t1MET < "+ str(boundaryMET)
		cutA = cutsig + ARegion + "&& pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"
		cutB = cutsig + BRegion + "&& pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"
		cutC = cutsig + CRegion + "&& pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"
		cutD = cutsig + DRegion + "&& pho1ClusterTime_SmearToData > -2.0 && pho1ClusterTime_SmearToData < 25.0"
		
		
		NA = tree.GetEntries(cutA)
		NB = tree.GetEntries(cutB)
		NC = tree.GetEntries(cutC)
		ND = tree.GetEntries(cutD)
		NCP = NB*ND*1.0/NA
		eNCP = NCP*np.sqrt(1.0/NB+1.0/ND+1.0/NA)
		dCoverC = 999
		edCoverC = 999
		if NC > 0:
			dCoverC = (NCP-NC)/NC
			edCoverC = (NCP/NC)*np.sqrt(1.0/NCP + 1.0/NC)
		print "%.1f"%boundaryTime+" & "+str(boundaryMET)+" & "+str(NA) +" & "+str(NB) + " & "+str(NC)+" & "+str(ND)+" & %.2f"%NCP + " $\\pm$ %.2f"%eNCP + " & %.1f"%(100.0*dCoverC)+" $\\pm$ %.1f"%(100.0*edCoverC)+" \\\\"



def getTimeAndMETCorrFactor(fileName, label, cutsig):
	fileThis = TFile(fileName)
        tree = fileThis.Get("DelayedPhoton")

	print tree.GetEntries(cutsig)
		
	myC = TCanvas( "myC", "myC", 200, 10, 900, 800 )
        myC.SetHighLightColor(2)
        myC.SetFillColor(0)
        myC.SetBorderMode(0)
        myC.SetBorderSize(2)
        myC.SetLeftMargin( leftMargin )
        myC.SetRightMargin( 0.15 )
        myC.SetTopMargin( topMargin )
        myC.SetBottomMargin( bottomMargin )
        myC.SetFrameBorderMode(0)
        myC.SetFrameBorderMode(0)

	h2_rate = TH2F("h2_rate","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, -2, 25, 100, 0, 1000)
	h2_rate_1ns = TH2F("h2_rate_1ns","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, 1.0, 25, 100, 0, 1000)
	h2_rate_1p5ns = TH2F("h2_rate_1p5ns","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, 1.5, 25, 100, 0, 1000)
	h2_rate_1p5to5ns = TH2F("h2_rate_1p5to5ns","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 100, 1.5, 3.0, 100, 0, 1000)
	h2_rate_m10to25ns = TH2F("h2_rate_m10to25ns","; #gamma cluster time (ns); #slash{E}_{T} (GeV); Events", 200, -10, 25.0, 100, 0, 1000)
	tree.Draw("t1MET:pho1ClusterTime_SmearToData>>h2_rate", cutsig, "COLZ")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_m2to25ns.pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_m2to25ns.png")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_m2to25ns.C")
	tree.Draw("t1MET:pho1ClusterTime_SmearToData>>h2_rate_1ns", cutsig,"COLZ")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1to25ns.pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1to25ns.png")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1to25ns.C")
	tree.Draw("t1MET:pho1ClusterTime_SmearToData>>h2_rate_1p5ns", cutsig,"COLZ")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1p5to25ns.pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1p5to25ns.png")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1p5to25ns.C")
	tree.Draw("t1MET:pho1ClusterTime_SmearToData>>h2_rate_1p5to5ns", cutsig,"COLZ")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1p5to5ns.pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1p5to5ns.png")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_1p5to5ns.C")
	tree.Draw("t1MET:pho1ClusterTime_SmearToData>>h2_rate_m10to25ns", cutsig,"COLZ")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_m10to25ns.pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_m10to25ns.png")
	myC.SaveAs(outputDir+"/METCorrPlots/time_met_2d_"+label+"_m10to25ns.C")
	print "#events of "+label+" (-10, 25)ns:  "+str(h2_rate_m10to25ns.Integral())
	print "correlation factor of "+label+" (-10, 25)ns:  "+str(h2_rate_m10to25ns.GetCorrelationFactor())
	print "#events of "+label+" (-2, 25)ns:  "+str(h2_rate.Integral())
	print "correlation factor of "+label+" (-2, 25)ns:  "+str(h2_rate.GetCorrelationFactor())
	print "#events of "+label+" (1.0, 25)ns:  "+str(h2_rate_1ns.Integral())
	print "correlation factor of "+label+" (1.0, 25)ns:  "+str(h2_rate_1ns.GetCorrelationFactor())
	print "#events of "+label+" (1.5, 25)ns:  "+str(h2_rate_1p5ns.Integral())
	print "correlation factor of "+label+" (1.5, 25)ns:  "+str(h2_rate_1p5ns.GetCorrelationFactor())
	print "#events of "+label+" (1.5, 5)ns:  "+str(h2_rate_1p5to5ns.Integral())
	print "correlation factor of "+label+" (1.5, 5)ns:  "+str(h2_rate_1p5to5ns.GetCorrelationFactor())

#runClosureTests("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJets CR", cut_GJets, [0.0, 0.0, 1.0, 0.0, 1.5, 1.5], [50, 100, 100, 250, 100, 150])
#runClosureTests("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCD CR", cut_QCD_CR, [0.0, 0.0, 1.0, 0.0, 1.5, 1.5], [50, 100, 100, 250, 100, 150])

#drawRatiosVsTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR", cut_GJets, 0.7, 70)
#drawRatiosVsTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCDCR", cut_QCD_CR, 0.7, 70)

cut_GJets0  = "1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets == 0  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_GJets1  = "1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets == 1  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_GJets2  = "1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets == 2  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"
cut_GJets3  = "1.0*(pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets == 3  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"

#drawRatiosVsTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR_nj0", cut_GJets0, 0.7, 70)
#drawRatiosVsTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR_nj1", cut_GJets1, 0.7, 70)
#drawRatiosVsTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR_nj2", cut_GJets2, 0.7, 70)
drawRatiosVsTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR_nj3", cut_GJets3, 0.7, 70)

#drawRatiosVsSplitTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR_nj0", cut_GJets0, 0.7, 70)
#drawRatiosVsSplitTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR_nj1", cut_GJets1, 0.7, 70)
#drawRatiosVsSplitTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR_nj2", cut_GJets2, 0.7, 70)
#drawRatiosVsSplitTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR", cut_GJets, 0.7, 70)
#drawRatiosVsSplitTimeAndMET("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCDCR", cut_QCD_CR, 0.7, 70)

#cut_sig_looseNj = "pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 1  && pho1Sminor<0.4 && pho1passSmajorTight && (HLTDecision[81] == 1) && n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0"
#drawTimeAndMETShapesSR("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "SR_looseNj", cut_sig_looseNj, [-2.0, 1,25.0], [0.0, 100, 3000.0], 0.04445, "#Lambda: 200 TeV, c#tau: 200 cm", False)
#drawTimeAndMETShapesSR("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "SR", cut, [-2.0, 1,25.0], [0.0, 100, 3000.0], 0.04445, "#Lambda: 200 TeV, c#tau: 200 cm", False)
#drawTimeAndMETShapesSR("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "SR_scaled", cut, [-2.0, 1,25.0], [0.0, 100, 3000.0], 0.04445, "#Lambda: 200 TeV, c#tau: 200 cm", True, True)
#drawTimeAndMETShapesSR("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "SR", cut, [-2.0, 1,25.0], [0.0, 100, 3000.0], 0.04445, "#Lambda: 200 TeV, c#tau: 200 cm", True, False)

#cut_noHLT = "pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0"

#drawTimeAndMETShapesSR("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "SR_scaled_10000cm_noHLT", cut_noHLT, [-2.0, 1,25.0], [0.0, 100, 3000.0], 0.04445, "#Lambda: 200 TeV, c#tau: 10000 cm", True, True)
#drawTimeAndMETShapesSR("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "SR_10000cm_noHLT", cut_noHLT, [-2.0, 1,25.0], [0.0, 100, 3000.0], 0.04445, "#Lambda: 200 TeV, c#tau: 10000 cm", True, False)

#drawTimeAndMETShapesSR("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "SR_scaled_10000cm", cut, [-2.0, 1,25.0], [0.0, 100, 3000.0], 0.04445, "#Lambda: 200 TeV, c#tau: 10000 cm", True, True)
#drawTimeAndMETShapesSR("~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau10000cm_13TeV-pythia8.root", "SR_10000cm", cut, [-2.0, 1,25.0], [0.0, 100, 3000.0], 0.04445, "#Lambda: 200 TeV, c#tau: 10000 cm", True, False)

#getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR", cut_GJets)
#getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCDCR", cut_QCD_CR)
#getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "SR", cut)

#getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "EWKCR", cut_EWKCR)
#getTimeAndMETCorrFactor("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "Data", cut)

#Timesplit = [-2, 0, 0.5, 1.0, 1.5, 3.0, 25]
#METsplit = [0, 50, 100, 200, 300, 500, 3000]
#drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR", cut_GJets, Timesplit, METsplit)
#drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCDCR", cut_QCD_CR, Timesplit, METsplit)

#drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "GJetsCR_full", cut_GJets, Timesplit, METsplit)
#drawTimeAndMETShapes("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "QCDCR_full", cut_QCD_CR, Timesplit, METsplit)

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

