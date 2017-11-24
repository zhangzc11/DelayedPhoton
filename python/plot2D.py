#!/usr/bin/python
from ROOT import TFile, TTree, TChain, TH1F, TLegend, gROOT, gStyle, TCanvas, TGraph, TH2F, TLine
import os, sys
from Aux import drawCMS, drawCMS2
import numpy as np
import array

from config import lumi
from config import fractionGJets, fractionQCD
from config import cut, cut_loose, cut_GJets
from config import fileNameData, fileNameSig, fileNameSigSkim
from config import outputDir

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)
gStyle.SetPalette(1)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/2D")
#os.system("mkdir -p ../data")
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

###draw binning
xbins_MET_lowT = [0.0, 70.0, 130.0, 225.0, 295.0, 320.0, 1000.0]
xbins_MET_highT = [0.0, 55.0, 85.0, 185.0, 500.0, 1000.0]
xbins_time_lowT = [-15.0, -0.7, 0.3, 0.8, 1.4, 15.0]
xbins_time_highT = [-15.0, -0.7, 0.0, 0.9, 1.6, 2.1, 10.0, 15.0]

line_time_lowT_1 = TLine(xbins_time_lowT[1], 0.0, xbins_time_lowT[1], 600.0)
line_time_lowT_1.SetLineWidth(2)
line_time_lowT_1.SetLineColor(880)
line_time_lowT_2 = TLine(xbins_time_lowT[2], 0.0, xbins_time_lowT[2], 600.0)
line_time_lowT_2.SetLineWidth(2)
line_time_lowT_2.SetLineColor(880)
line_time_lowT_3 = TLine(xbins_time_lowT[3], 0.0, xbins_time_lowT[3], 600.0)
line_time_lowT_3.SetLineWidth(2)
line_time_lowT_3.SetLineColor(880)
line_time_lowT_4 = TLine(xbins_time_lowT[4], 0.0, xbins_time_lowT[4], 600.0)
line_time_lowT_4.SetLineWidth(2)
line_time_lowT_4.SetLineColor(880)


line_time_highT_1 = TLine(xbins_time_highT[1], 0.0, xbins_time_highT[1], 600.0)
line_time_highT_1.SetLineWidth(2)
line_time_highT_1.SetLineColor(880)
line_time_highT_2 = TLine(xbins_time_highT[2], 0.0, xbins_time_highT[2], 600.0)
line_time_highT_2.SetLineWidth(2)
line_time_highT_2.SetLineColor(880)
line_time_highT_3 = TLine(xbins_time_highT[3], 0.0, xbins_time_highT[3], 600.0)
line_time_highT_3.SetLineWidth(2)
line_time_highT_3.SetLineColor(880)
line_time_highT_4 = TLine(xbins_time_highT[4], 0.0, xbins_time_highT[4], 600.0)
line_time_highT_4.SetLineWidth(2)
line_time_highT_4.SetLineColor(880)
line_time_highT_5 = TLine(xbins_time_highT[5], 0.0, xbins_time_highT[5], 600.0)
line_time_highT_5.SetLineWidth(2)
line_time_highT_5.SetLineColor(880)
line_time_highT_6 = TLine(xbins_time_highT[6], 0.0, xbins_time_highT[6], 600.0)
line_time_highT_6.SetLineWidth(2)
line_time_highT_6.SetLineColor(880)


line_MET_lowT_1 = TLine(-10.0, xbins_MET_lowT[1], 15.0, xbins_MET_lowT[1])
line_MET_lowT_1.SetLineWidth(2)
line_MET_lowT_1.SetLineColor(880)
line_MET_lowT_2 = TLine(-10.0, xbins_MET_lowT[2], 15.0, xbins_MET_lowT[2])
line_MET_lowT_2.SetLineWidth(2)
line_MET_lowT_2.SetLineColor(880)
line_MET_lowT_3 = TLine(-10.0, xbins_MET_lowT[3], 15.0, xbins_MET_lowT[3])
line_MET_lowT_3.SetLineWidth(2)
line_MET_lowT_3.SetLineColor(880)
line_MET_lowT_4 = TLine(-10.0, xbins_MET_lowT[4], 15.0, xbins_MET_lowT[4])
line_MET_lowT_4.SetLineWidth(2)
line_MET_lowT_4.SetLineColor(880)
line_MET_lowT_5 = TLine(-10.0, xbins_MET_lowT[5], 15.0, xbins_MET_lowT[5])
line_MET_lowT_5.SetLineWidth(2)
line_MET_lowT_5.SetLineColor(880)

line_MET_highT_1 = TLine(-10.0, xbins_MET_highT[1], 15.0, xbins_MET_highT[1])
line_MET_highT_1.SetLineWidth(2)
line_MET_highT_1.SetLineColor(880)
line_MET_highT_2 = TLine(-10.0, xbins_MET_highT[2], 15.0, xbins_MET_highT[2])
line_MET_highT_2.SetLineWidth(2)
line_MET_highT_2.SetLineColor(880)
line_MET_highT_3 = TLine(-10.0, xbins_MET_highT[3], 15.0, xbins_MET_highT[3])
line_MET_highT_3.SetLineWidth(2)
line_MET_highT_3.SetLineColor(880)
line_MET_highT_4 = TLine(-10.0, xbins_MET_highT[4], 15.0, xbins_MET_highT[4])
line_MET_highT_4.SetLineWidth(2)
line_MET_highT_4.SetLineColor(880)

##############load delayed photon input tree#############
	
file_data = TFile(fileNameData)
tree_data = file_data.Get("DelayedPhoton")

histData = TH2F("hdata","hdata",100,-10,15, 100, 0, 600)
histGJets = TH2F("hGJets","hGJets",100,-10,15, 100, 0, 600)
histQCD = TH2F("hQCD","hQCD",100,-10,15, 100, 0, 600)
histBkg = TH2F("hBkg","hBkg",100,-10,15, 100, 0, 600)

tree_data.Draw("MET:pho1ClusterTime>>hdata",cut)
tree_data.Draw("MET:pho1ClusterTime>>hGJets",cut_GJets)
tree_data.Draw("MET:pho1ClusterTime>>hQCD",cut_loose + " && ! ("+cut+")")

histGJets.Scale(fractionGJets*histData.Integral()/histGJets.Integral())
histQCD.Scale(fractionQCD*histData.Integral()/histQCD.Integral())
histBkg.Add(histGJets)
histBkg.Add(histQCD)
	
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

N_blind = 5
x_blind = [1.0,15.0,15.0,1.0,1.0]
y_blind = [100.0,100.0,600.0,600.0,100.0]
graph_blind = TGraph(N_blind, np.array(x_blind), np.array(y_blind))
graph_blind.SetFillColor(800+3)


histData.SetTitle("")
histData.Draw("COLZ")
graph_blind.Draw("Fsame")

histData.GetXaxis().SetTitleSize( axisTitleSize )
histData.GetXaxis().SetTitleOffset( axisTitleOffset )
histData.GetYaxis().SetTitleSize( axisTitleSize )
histData.GetYaxis().SetTitleOffset( axisTitleOffset )
histData.GetXaxis().SetTitle("#gamma cluster time [ns]")
histData.GetYaxis().SetTitle("#slash{E}_{T} [GeV]")


drawCMS2(myC, 13, lumi)	

myC.Modified()
myC.Update()

myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_blinded.pdf")
myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_blinded.png")
myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_blinded.C")

#####background and signal distribution of 2D
histBkg.SetTitle("")
histBkg.SetMarkerColorAlpha(2, 1.0)
histBkg.SetMarkerStyle(7)

histBkg.Draw("")

histBkg.GetXaxis().SetTitleSize( axisTitleSize )
histBkg.GetXaxis().SetTitleOffset( axisTitleOffset )
histBkg.GetYaxis().SetTitleSize( axisTitleSize )
histBkg.GetYaxis().SetTitleOffset( axisTitleOffset )
histBkg.GetXaxis().SetTitle("#gamma cluster time [ns]")
histBkg.GetYaxis().SetTitle("#slash{E}_{T} [GeV]")

drawCMS2(myC, 13, lumi)	

myC.Modified()
myC.Update()

myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkg.pdf")
myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkg.png")
myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkg.C")


myC.SetRightMargin( 0.1 )
myC.SetLogz(1)
histBkg.Draw("COLZ")

line_time_lowT_1.Draw()
line_time_lowT_2.Draw()
line_time_lowT_3.Draw()
line_time_lowT_4.Draw()
line_MET_lowT_1.Draw()
line_MET_lowT_2.Draw()
line_MET_lowT_3.Draw()
line_MET_lowT_4.Draw()
line_MET_lowT_5.Draw()


drawCMS2(myC, 13, lumi)	

myC.Modified()
myC.Update()

myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkg_colz.pdf")
myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkg_colz.png")
myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkg_colz.C")

myC.SetRightMargin( rightMargin )
myC.SetLogz(0)

for fileSig in fileNameSigSkim:
	fileThis = fileSig.replace("private_REMINIAOD/withcut","private_REMINIAOD/skim")
	modelThis_temp = fileSig.replace("/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_","")
	modelThis = modelThis_temp.replace("_13TeV-pythia8.root","")

	useLowTBinning = False
	if modelThis.find("0p") != -1:
		useLowTBinning = True
	if modelThis.find("10cm") != -1:
		useLowTBinning = True
	print "model name: "+str(modelThis)
	print "using lowT binning?"
	print useLowTBinning
	
	file_Sig = TFile(fileThis)
	tree_Sig = file_Sig.Get("DelayedPhoton")
	histSig = TH2F("hSig","hSig",100,-10,15, 100, 0, 600)
	tree_Sig.Draw("MET:pho1ClusterTime>>hSig",cut)
	histSig.Scale(0.5*histData.Integral()/histSig.Integral())

	###
	myC.SetRightMargin( 0.1 )
	#myC.SetLogz(1)

	histSig.SetTitle("")
	histSig.SetMarkerColorAlpha(3, 0.5)
	histSig.SetMarkerStyle(26)
	histSig.SetMarkerSize(0.6)

	histSig.Draw("COLZ")

	histSig.GetXaxis().SetTitleSize( axisTitleSize )
	histSig.GetXaxis().SetTitleOffset( axisTitleOffset )
	histSig.GetYaxis().SetTitleSize( axisTitleSize )
	histSig.GetYaxis().SetTitleOffset( axisTitleOffset )
	histSig.GetXaxis().SetTitle("#gamma cluster time [ns]")
	histSig.GetYaxis().SetTitle("#slash{E}_{T} [GeV]")

	drawCMS2(myC, 13, lumi)	
	if useLowTBinning:
		line_time_lowT_1.Draw()
		line_time_lowT_2.Draw()
		line_time_lowT_3.Draw()
		line_time_lowT_4.Draw()
		line_MET_lowT_1.Draw()
		line_MET_lowT_2.Draw()
		line_MET_lowT_3.Draw()
		line_MET_lowT_4.Draw()
		line_MET_lowT_5.Draw()
	else:
		line_time_highT_1.Draw()
		line_time_highT_2.Draw()
		line_time_highT_3.Draw()
		line_time_highT_4.Draw()
		line_time_highT_5.Draw()
		line_time_highT_6.Draw()
		line_MET_highT_1.Draw()
		line_MET_highT_2.Draw()
		line_MET_highT_3.Draw()
		line_MET_highT_4.Draw()


	myC.Modified()
	myC.Update()

	myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_sig_"+modelThis+".pdf")
	myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_sig_"+modelThis+".png")
	myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_sig_"+modelThis+".C")
	myC.SetRightMargin( rightMargin )
	#myC.SetLogz(0)


	###together

	histBkg.Draw()
	histSig.Draw("same")

	if useLowTBinning:
		line_time_lowT_1.Draw()
		line_time_lowT_2.Draw()
		line_time_lowT_3.Draw()
		line_time_lowT_4.Draw()
		line_MET_lowT_1.Draw()
		line_MET_lowT_2.Draw()
		line_MET_lowT_3.Draw()
		line_MET_lowT_4.Draw()
		line_MET_lowT_5.Draw()
	else:
		line_time_highT_1.Draw()
		line_time_highT_2.Draw()
		line_time_highT_3.Draw()
		line_time_highT_4.Draw()
		line_time_highT_5.Draw()
		line_time_highT_6.Draw()
		line_MET_highT_1.Draw()
		line_MET_highT_2.Draw()
		line_MET_highT_3.Draw()
		line_MET_highT_4.Draw()

	drawCMS2(myC, 13, lumi)	

	leg = TLegend(0.5,0.732,0.9498747,0.932)
	leg.SetHeader("                S/B = 0.5")
	leg.SetBorderSize(1)
	leg.SetTextSize(0.03)
	leg.SetLineColor(1)
	leg.SetLineStyle(1)
	leg.SetLineWidth(1)
	leg.SetFillColor(0)
	leg.SetFillStyle(1001)

	leg.AddEntry(histBkg, "background","p")
	leg.AddEntry(histSig, modelThis,"p")

	leg.Draw()
	myC.Modified()
	myC.Update()

	myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkgsig_"+modelThis+".pdf")
	myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkgsig_"+modelThis+".png")
	myC.SaveAs(outputDir+"/2D"+"/MET_Time_2D_bkgsig_"+modelThis+".C")


