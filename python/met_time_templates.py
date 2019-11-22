from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors, TEfficiency, gPad, TH2F, TF1
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import outputDir, lumi

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir+"/stack")
os.system("mkdir -p "+outputDir+"/stack")
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
########################################################

inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"



def properScale(hist, norm):
        #norm = 1.0/hist.Integral()
        for i in range(0, hist.GetNbinsX()+1):
                v0 = hist.GetBinContent(i)
                hist.SetBinContent(i, norm*v0/hist.GetBinWidth(i))
                if v0 > 0.0000001:
                        hist.SetBinError(i, norm*v0/(np.sqrt(v0)*hist.GetBinWidth(i)))
                else:
                        hist.SetBinError(i, 0.0)



def draw_var_showInt(filename, label, cut, varName, varTitle, titleY, unitX, varBinning, splits, logY = True):
	print "Making plots of "+varName
	fileThis = TFile(inputDir+filename, "READ")
        treeThis = fileThis.Get("DelayedPhoton")
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
	myC.SetLogy(logY)

	hist1 = TH1F("hist1","; "+varTitle+"; "+titleY, len(varBinning)-1, varBinning)
	
	treeThis.Draw(varName+">>hist1", cut, "")

	hist1.SetLineColor(kBlack)
	hist1.SetMarkerColor(kBlack)
	hist1.SetMarkerStyle(20)

	hist1.SetTitle("")
        hist1.Draw("E")
        hist1.GetXaxis().SetTitleSize( axisTitleSize )
        hist1.GetXaxis().SetTitleOffset( axisTitleOffset )
        hist1.GetYaxis().SetTitleSize( axisTitleSize )
        hist1.GetYaxis().SetTitleOffset( axisTitleOffset )
	
	#Ntotal = hist1.Integral()
	Ntotal = treeThis.GetEntries(cut+" && "+varName+">="+str(varBinning[0])+ " && "+varName+"<="+str(varBinning[-1]))

	tlatex = TLatex()
	tlatex.SetNDC()
	tlatex.SetTextAngle(0)
	tlatex.SetTextColor(1)
	tlatex.SetTextFont(63)
	tlatex.SetTextAlign(11)
	tlatex.SetTextSize(25)
	tlatex.SetTextColor(kBlue)
	
	print "Ntotal: "+str(Ntotal)

	for idx in range(len(splits)):
		N_left = treeThis.GetEntries(cut+" && "+varName+">="+str(varBinning[0])+ " && "+varName+"<"+str(splits[idx]))
		N_right = treeThis.GetEntries(cut+" && "+varName+"<="+str(varBinning[-1])+ " && "+varName+">="+str(splits[idx]))
		percent = N_right*1.0/N_left
		percent_err = (N_right*1.0/N_left)*(1.0/N_right + 1.0/N_left)**0.5
		print "split: "+str(splits[idx])
		print "N_left: "+str(N_left)
		print "N_right: "+str(N_right)
		print "percent: "+str(percent)
		print "percent_err: "+str(percent_err)
		
		if percent < 0.0001 or percent_err < 0.0001:	
			tlatex.DrawLatex(0.45, 0.4+idx*0.1, "#frac{N(>"+str(splits[idx])+""+unitX+")}{N(<"+str(splits[idx])+""+unitX+")} =  %8.6f #pm %8.6f"%(percent, percent_err))	
		elif percent < 0.001 or percent_err < 0.001:	
			tlatex.DrawLatex(0.45, 0.4+idx*0.1, "#frac{N(>"+str(splits[idx])+""+unitX+")}{N(<"+str(splits[idx])+""+unitX+")} =  %7.5f #pm %7.5f"%(percent, percent_err))	
		elif percent < 0.01 or percent_err < 0.01:
			tlatex.DrawLatex(0.45, 0.4+idx*0.1, "#frac{N(>"+str(splits[idx])+""+unitX+")}{N(<"+str(splits[idx])+""+unitX+")} =  %6.4f #pm %6.4f"%(percent, percent_err))	
		else:
			tlatex.DrawLatex(0.45, 0.4+idx*0.1, "#frac{N(>"+str(splits[idx])+""+unitX+")}{N(<"+str(splits[idx])+""+unitX+")} =  %5.3f #pm %5.3f"%(percent, percent_err))	
		
	

	drawCMS2(myC, 13, lumi)

	myC.SaveAs(outputDir+"/stack/templates_"+varName+"_"+label+".pdf")
	myC.SaveAs(outputDir+"/stack/templates_"+varName+"_"+label+".png")
	myC.SaveAs(outputDir+"/stack/templates_"+varName+"_"+label+".C")


cut_normal = "n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 &&Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight && pho2SigmaIetaIeta<0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso<30.0 && pho2sumNeutralHadronEt<30.0 && pho2trkSumPtHollowConeDR03 < 30.0 && pho1R9 > 0.9"

cut_time_template = cut_normal + " && t1MET < 100.0"
cut_met_template = cut_normal + "&&  (pho1ClusterTime_SmearToData < 1.0)"

#time_binning = np.array([-2.0, 0.0, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.1, 2.4, 3.0, 20.0])
#MET_binning = np.array([0, 80., 110., 130.0, 150., 170.0, 200.0, 300., 1000.])
time_binning = np.arange(-2.0, 25.0, 0.05)
MET_binning = np.arange(0.0, 3000.0, 10.0)
	
#DelayedPhoton_DoubleEG_2016All_GoodLumi.root
draw_var_showInt("DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "time", cut_time_template, "pho1ClusterTime_SmearToData", "#gamma cluster time [ns]","Events", "ns", time_binning, np.array([0.0, 1.5]), True)
draw_var_showInt("DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "met", cut_met_template, "t1MET", "MET [GeV]","Events", "GeV", MET_binning, np.array([100.0, 150.0, 250.0]), True)
