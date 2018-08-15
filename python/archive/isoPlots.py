from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array

from config import lumi
from config import outputDir

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/isolation")
os.system("cp isoPlots.py "+outputDir+"/isolation")
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
rightMargin  = 0.15
topMargin    = 0.07
bottomMargin = 0.12
##############load delayed photon input tree#############

inputFiles = [
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L250TeV_Ctau200cm_13TeV-pythia8.root', 'L250TeV_Ctau200cm'],
		#['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L400TeV_Ctau800cm_13TeV-pythia8.root', 'L400TeV_Ctau800cm'],
		#['../GMSB_L250TeV_Ctau10cm_13TeV-pythia8.root', 'L250TeV_Ctau10cm']	
	 	]

os.system("mkdir -p "+outputDir+"/isolation/")

#cut = "(weight*pileupWeight)* (pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3&& (HLTDecision[81] == 1) )"
cut = "(weight*pileupWeight)* (pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3&& (HLTDecision[81] == 1) ) "
cut_inTime = "(weight*pileupWeight)* (pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3&& (HLTDecision[81] == 1)  && pho1isStandardPhoton && pho1isDelayedPhoton) "
cut_OOT = "(weight*pileupWeight)* (pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3&& (HLTDecision[81] == 1)  && (!pho1isStandardPhoton) && pho1isDelayedPhoton) "


plots = [
		["pho1sumPhotonEt","PF Iso - photon (GeV)"],
		["pho1sumChargedHadronPt","PF Iso - charged hadron (GeV)"],
		["pho1sumNeutralHadronEt","PF Iso - neutral hadron (GeV)"],
		["pho1ecalPFClusterIso","PF Cluster Iso - ECAL (GeV)"],
		["pho1hcalPFClusterIso","PF Cluster Iso - HCAL (GeV)"],
		["pho1trkSumPtHollowConeDR03","tracker iso (GeV)"]
	]

for finput in inputFiles:
	
	file_input = TFile(finput[0])
	tree_in = file_input.Get("DelayedPhoton")
	
	for plot in plots:
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

		hist_iso_vs_Time = TH2F("hist_"+plot[0]+"_vs_Time","; #gamma cluster time (ns); "+plot[1]+"; Events", 100, -15, 15, 100, -1.0, 50.0)
		tree_in.Draw(plot[0]+":pho1ClusterTime>>hist_"+plot[0]+"_vs_Time",cut)
		hist_iso_vs_Time.SetTitle("")
		hist_iso_vs_Time.SetLineWidth(2)
		hist_iso_vs_Time.Draw("COLZ")
		hist_iso_vs_Time.GetXaxis().SetTitleSize( axisTitleSize )
		hist_iso_vs_Time.GetXaxis().SetTitleOffset( axisTitleOffset )
		hist_iso_vs_Time.GetYaxis().SetTitleSize( axisTitleSize )
		hist_iso_vs_Time.GetYaxis().SetTitleOffset( axisTitleOffset )
		#drawCMS2(myC, 13, lumi)	

		myC.SaveAs(outputDir+"/isolation/"+plot[0]+"_vs_Time_"+finput[1]+".pdf")
		myC.SaveAs(outputDir+"/isolation/"+plot[0]+"_vs_Time_"+finput[1]+".png")
		myC.SaveAs(outputDir+"/isolation/"+plot[0]+"_vs_Time_"+finput[1]+".C")

		##1D distribution

		myC2 = TCanvas( "myC2", "myC2", 200, 10, 800, 800 )
		myC2.SetHighLightColor(2)
		myC2.SetFillColor(0)
		myC2.SetBorderMode(0)
		myC2.SetBorderSize(2)
		myC2.SetLeftMargin( leftMargin )
		myC2.SetRightMargin( 0.05 )
		myC2.SetTopMargin( topMargin )
		myC2.SetBottomMargin( bottomMargin )
		myC2.SetFrameBorderMode(0)
		myC2.SetFrameBorderMode(0)

		pad1 = TPad("pad1","pad1", 0.05, 0.3,0.95, 0.97)
		pad1.SetBottomMargin(0)
		pad1.SetRightMargin( 0.05 )
		pad1.SetLeftMargin( leftMargin )
		pad1.SetLogy(1)
		pad1.Draw()

		pad2 = TPad("pad2","pad2", 0.05, 0.02, 0.95, 0.29)
		pad2.SetTopMargin(0.04)
		pad2.SetTopMargin(0.008)
		pad2.SetBottomMargin(0.4)
		pad2.SetRightMargin( 0.05 )
		pad2.SetLeftMargin( leftMargin )
		pad2.SetGridy()
		pad2.Draw()

		pad1.cd()
		histiso_inTime = TH1F("hist"+plot[0]+"_inTime","; "+plot[1]+"; Events", 100, -1.0, 50.0)
		histiso_OOT = TH1F("hist"+plot[0]+"_OOT","; "+plot[1]+"; Events", 100, -1.0, 50.0)
		tree_in.Draw(plot[0]+">>hist"+plot[0]+"_inTime",cut_inTime)
		tree_in.Draw(plot[0]+">>hist"+plot[0]+"_OOT",cut_OOT)

		if histiso_inTime.Integral() > 0.0:
			histiso_inTime.Scale(1.0/histiso_inTime.Integral())
		if histiso_OOT.Integral() > 0.0:
			histiso_OOT.Scale(1.0/histiso_OOT.Integral())

		histiso_inTime.SetTitle("")
		histiso_inTime.SetLineWidth(2)
		histiso_inTime.SetLineColor(kBlue)
		histiso_inTime.Draw("hist")
		histiso_inTime.GetXaxis().SetTitleSize( axisTitleSize )
		histiso_inTime.GetXaxis().SetTitleOffset( axisTitleOffset )
		histiso_inTime.GetYaxis().SetTitleSize( axisTitleSize )
		histiso_inTime.GetYaxis().SetTitleOffset( axisTitleOffset )
		histiso_inTime.GetYaxis().SetRangeUser(1e-4, max(histiso_inTime.GetMaximum(), histiso_OOT.GetMaximum())*100.0 )

		histiso_OOT.SetLineWidth(2)
		histiso_OOT.SetLineColor(kRed)
		histiso_OOT.Draw("histsame")

		leg = TLegend(0.65, 0.7, 0.82, 0.85)
		leg.SetBorderSize(0)
		leg.SetTextSize(0.03)
		leg.SetLineColor(1)
		leg.SetLineStyle(1)
		leg.SetLineWidth(1)
		leg.SetFillColor(0)
		leg.SetFillStyle(1001)
		leg.AddEntry(histiso_inTime, "GED","l")
		leg.AddEntry(histiso_OOT, "OOT","l")
		leg.Draw()

		pad1.Update()
		pad2.cd()
		ratio_iso = TH1F("ratio_"+plot[0],"; "+plot[1]+"; OOT/GED ", 100, -1.0, 50.0)
		ratio_iso.Add(histiso_OOT)
		ratio_iso.Divide(histiso_inTime)
		ratio_iso.SetMarkerStyle( 20 )
		ratio_iso.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
		ratio_iso.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
		ratio_iso.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
		ratio_iso.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
		ratio_iso.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
		ratio_iso.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
		ratio_iso.SetMarkerColor( kBlue )
		ratio_iso.SetLineColor( kBlue )
		ratio_iso.GetYaxis().SetRangeUser( 0.0, 2.5 )
		ratio_iso.SetTitle("")
		ratio_iso.GetYaxis().CenterTitle( True )
		ratio_iso.GetYaxis().SetNdivisions( 5, False )
		ratio_iso.SetStats( 0 )
		ratio_iso.Draw("E")
		pad1.Update()
		pad2.Update()
		
		#drawCMS2(myC2, 13, lumi)	

		myC2.SaveAs(outputDir+"/isolation/"+plot[0]+"_"+finput[1]+".pdf")
		myC2.SaveAs(outputDir+"/isolation/"+plot[0]+"_"+finput[1]+".png")
		myC2.SaveAs(outputDir+"/isolation/"+plot[0]+"_"+finput[1]+".C")

