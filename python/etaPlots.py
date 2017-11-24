#!/usr/bin/python 
from ROOT import TFile, TTree, TChain, TH1F, TLegend, gROOT, gStyle, TCanvas
import os, sys
from Aux import drawCMS, drawCMS2
import numpy as np
import array

from config import lumi
from config import outputDir

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/eta")
os.system("cp etaPlots.py "+outputDir+"/eta")
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
##############load delayed photon input tree#############

inputFiles = [
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L150TeV_Ctau10cm_13TeV-pythia8.root', 'L150TeV_Ctau10cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L150TeV_Ctau800cm_13TeV-pythia8.root', 'L150TeV_Ctau800cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L400TeV_Ctau10cm_13TeV-pythia8.root', 'L400TeV_Ctau10cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L400TeV_Ctau800cm_13TeV-pythia8.root', 'L400TeV_Ctau800cm'],
		#['../GMSB_L250TeV_Ctau10cm_13TeV-pythia8.root', 'L250TeV_Ctau10cm']	
	 	]

os.system("mkdir -p "+outputDir+"/eta/")

cut = "(weight*pileupWeight)* (pho1Pt > 70 && n_Jets > 2 &&pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2)"

print inputFiles[0][1]
print inputFiles[1][1]
print inputFiles[2][1]
print inputFiles[3][1]


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

#myC.SetLogy(1)



leg = TLegend(0.6, 0.70, 0.92, 0.85)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(0)
leg.SetFillStyle(1001)



file_input0 = TFile(inputFiles[0][0])
file_input1 = TFile(inputFiles[1][0])
file_input2 = TFile(inputFiles[2][0])
file_input3 = TFile(inputFiles[3][0])

hNEvents0 = file_input0.Get("NEvents")
hNEvents1 = file_input1.Get("NEvents")
hNEvents2 = file_input2.Get("NEvents")
hNEvents3 = file_input3.Get("NEvents")

NEvents0 = hNEvents0.GetBinContent(1)
NEvents1 = hNEvents1.GetBinContent(1)
NEvents2 = hNEvents2.GetBinContent(1)
NEvents3 = hNEvents3.GetBinContent(1)

tree_in0 = file_input0.Get("DelayedPhoton")
tree_in1 = file_input1.Get("DelayedPhoton")
tree_in2 = file_input2.Get("DelayedPhoton")
tree_in3 = file_input3.Get("DelayedPhoton")


histthis_eff0 = TH1F("hist_eta_eff_"+inputFiles[0][1],"; #eta; efficiency",100,-3.0,3.0)
histthis_eff1 = TH1F("hist_eta_eff_"+inputFiles[1][1],"; #eta; efficiency",100,-3.0,3.0)
histthis_eff2 = TH1F("hist_eta_eff_"+inputFiles[2][1],"; #eta; efficiency",100,-3.0,3.0)
histthis_eff3 = TH1F("hist_eta_eff_"+inputFiles[3][1],"; #eta; efficiency",100,-3.0,3.0)


histthis0 = TH1F("hist_eta_"+inputFiles[0][1],"; #eta; Events",100,-3.0,3.0)
histthis1 = TH1F("hist_eta_"+inputFiles[1][1],"; #eta; Events",100,-3.0,3.0)
histthis2 = TH1F("hist_eta_"+inputFiles[2][1],"; #eta; Events",100,-3.0,3.0)
histthis3 = TH1F("hist_eta_"+inputFiles[3][1],"; #eta; Events",100,-3.0,3.0)

tree_in0.Draw("pho1Eta>>hist_eta_"+inputFiles[0][1],cut)
tree_in1.Draw("pho1Eta>>hist_eta_"+inputFiles[1][1],cut)
tree_in2.Draw("pho1Eta>>hist_eta_"+inputFiles[2][1],cut)
tree_in3.Draw("pho1Eta>>hist_eta_"+inputFiles[3][1],cut)

histthis_eff0.Add(histthis0)
histthis_eff1.Add(histthis1)
histthis_eff2.Add(histthis2)
histthis_eff3.Add(histthis3)

histthis0.SetLineWidth( 2 )
histthis1.SetLineWidth( 2 )
histthis2.SetLineWidth( 2 )
histthis3.SetLineWidth( 2 )
histthis0.SetLineColor( 1 )
histthis1.SetLineColor( 2 )
histthis2.SetLineColor( 3 )
histthis3.SetLineColor( 4 )

histthis0.Scale(1.0/histthis0.Integral())
histthis1.Scale(1.0/histthis1.Integral())
histthis2.Scale(1.0/histthis2.Integral())
histthis3.Scale(1.0/histthis3.Integral())

leg.AddEntry(histthis0, inputFiles[0][1],"l")
leg.AddEntry(histthis1, inputFiles[1][1],"l")
leg.AddEntry(histthis2, inputFiles[2][1],"l")
leg.AddEntry(histthis3, inputFiles[3][1],"l")

histthis0.GetYaxis().SetRangeUser(0.0, 1.4*max(histthis0.GetMaximum(), histthis1.GetMaximum(), histthis2.GetMaximum(), histthis3.GetMaximum()))

histthis0.GetXaxis().SetTitleSize( axisTitleSize )
histthis0.GetXaxis().SetTitleOffset( axisTitleOffset )
histthis0.GetYaxis().SetTitleSize( axisTitleSize )
histthis0.GetYaxis().SetTitleOffset( axisTitleOffset )

histthis0.Draw("hist")
histthis1.Draw("histsame")
histthis2.Draw("histsame")
histthis3.Draw("histsame")
	
leg.Draw()
myC.SaveAs(outputDir+"eta/eta.pdf")
myC.SaveAs(outputDir+"eta/eta.png")
myC.SaveAs(outputDir+"eta/eta.C")



histthis_nocut0 = TH1F("hist_eta_nocut_"+inputFiles[0][1],"; #eta; Events",100,-3.0,3.0)
histthis_nocut1 = TH1F("hist_eta_nocut_"+inputFiles[1][1],"; #eta; Events",100,-3.0,3.0)
histthis_nocut2 = TH1F("hist_eta_nocut_"+inputFiles[2][1],"; #eta; Events",100,-3.0,3.0)
histthis_nocut3 = TH1F("hist_eta_nocut_"+inputFiles[3][1],"; #eta; Events",100,-3.0,3.0)

tree_in0.Draw("pho1Eta>>hist_eta_nocut_"+inputFiles[0][1])
tree_in1.Draw("pho1Eta>>hist_eta_nocut_"+inputFiles[1][1])
tree_in2.Draw("pho1Eta>>hist_eta_nocut_"+inputFiles[2][1])
tree_in3.Draw("pho1Eta>>hist_eta_nocut_"+inputFiles[3][1])



histthis_nocut0.Scale((1.0*NEvents0)/histthis_nocut0.Integral())
histthis_nocut1.Scale((1.0*NEvents1)/histthis_nocut1.Integral())
histthis_nocut2.Scale((1.0*NEvents2)/histthis_nocut2.Integral())
histthis_nocut3.Scale((1.0*NEvents3)/histthis_nocut3.Integral())


histthis_eff0.Divide(histthis_nocut0)
histthis_eff1.Divide(histthis_nocut1)
histthis_eff2.Divide(histthis_nocut2)
histthis_eff3.Divide(histthis_nocut3)

histthis_nocut0.SetLineWidth( 2 )
histthis_nocut1.SetLineWidth( 2 )
histthis_nocut2.SetLineWidth( 2 )
histthis_nocut3.SetLineWidth( 2 )
histthis_nocut0.SetLineColor( 1 )
histthis_nocut1.SetLineColor( 2 )
histthis_nocut2.SetLineColor( 3 )
histthis_nocut3.SetLineColor( 4 )

histthis_nocut0.Scale(1.0/histthis_nocut0.Integral())
histthis_nocut1.Scale(1.0/histthis_nocut1.Integral())
histthis_nocut2.Scale(1.0/histthis_nocut2.Integral())
histthis_nocut3.Scale(1.0/histthis_nocut3.Integral())

histthis_nocut0.GetYaxis().SetRangeUser(0.0, 1.4*max(histthis_nocut0.GetMaximum(), histthis_nocut1.GetMaximum(), histthis_nocut2.GetMaximum(), histthis_nocut3.GetMaximum()))

histthis_nocut0.GetXaxis().SetTitleSize( axisTitleSize )
histthis_nocut0.GetXaxis().SetTitleOffset( axisTitleOffset )
histthis_nocut0.GetYaxis().SetTitleSize( axisTitleSize )
histthis_nocut0.GetYaxis().SetTitleOffset( axisTitleOffset )

histthis_nocut0.Draw("hist")
histthis_nocut1.Draw("histsame")
histthis_nocut2.Draw("histsame")
histthis_nocut3.Draw("histsame")
	
leg.Draw()
myC.SaveAs(outputDir+"eta/eta_nocut.pdf")
myC.SaveAs(outputDir+"eta/eta_nocut.png")
myC.SaveAs(outputDir+"eta/eta_nocut.C")




histthis_eff0.SetLineWidth( 2 )
histthis_eff1.SetLineWidth( 2 )
histthis_eff2.SetLineWidth( 2 )
histthis_eff3.SetLineWidth( 2 )
histthis_eff0.SetLineColor( 1 )
histthis_eff1.SetLineColor( 2 )
histthis_eff2.SetLineColor( 3 )
histthis_eff3.SetLineColor( 4 )

histthis_eff0.GetYaxis().SetRangeUser(0.0, 1.4*max(histthis_eff0.GetMaximum(), histthis_eff1.GetMaximum(), histthis_eff2.GetMaximum(), histthis_eff3.GetMaximum()))

histthis_eff0.GetXaxis().SetTitleSize( axisTitleSize )
histthis_eff0.GetXaxis().SetTitleOffset( axisTitleOffset )
histthis_eff0.GetYaxis().SetTitleSize( axisTitleSize )
histthis_eff0.GetYaxis().SetTitleOffset( axisTitleOffset )

histthis_eff0.Draw("hist")
histthis_eff1.Draw("histsame")
histthis_eff2.Draw("histsame")
histthis_eff3.Draw("histsame")
	
leg.Draw()
myC.SaveAs(outputDir+"eta/eta_eff.pdf")
myC.SaveAs(outputDir+"eta/eta_eff.png")
myC.SaveAs(outputDir+"eta/eta_eff.C")
