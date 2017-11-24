#!/usr/bin/python 
from ROOT import TFile, TTree, TChain, TH1F, TLegend, gROOT, gStyle, TCanvas
import os, sys
from Aux import drawCMS, drawCMS2
import numpy as np
import array

from config import lumi
from config import outputDir
from config import fileNameData

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/nJets")
os.system("cp nJetsPlots.py "+outputDir+"/nJets")
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
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L100TeV_Ctau10cm_13TeV-pythia8.root', 'L100TeV_Ctau10cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L150TeV_Ctau10cm_13TeV-pythia8.root', 'L150TeV_Ctau10cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L250TeV_Ctau10cm_13TeV-pythia8.root', 'L250TeV_Ctau10cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L400TeV_Ctau10cm_13TeV-pythia8.root', 'L400TeV_Ctau10cm'],
		#['../GMSB_L250TeV_Ctau10cm_13TeV-pythia8.root', 'L250TeV_Ctau10cm']	
		#['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L150TeV_Ctau10cm_13TeV-pythia8.root', 'L150TeV_Ctau10cm'],
                #['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L150TeV_Ctau800cm_13TeV-pythia8.root', 'L150TeV_Ctau800cm'],
                #['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L400TeV_Ctau10cm_13TeV-pythia8.root', 'L400TeV_Ctau10cm'],
                #['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/GMSB_L400TeV_Ctau800cm_13TeV-pythia8.root', 'L400TeV_Ctau800cm'],

	 	]


os.system("mkdir -p "+outputDir+"/nJets/")

cut = "(weight*pileupWeight)* (pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2)"
cut_data = "(pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2)"

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



leg = TLegend(0.6, 0.65, 0.8, 0.85)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(0)
leg.SetFillStyle(1001)

file_data = TFile(fileNameData.replace("private_REMINIAOD/skim","private_REMINIAOD/withcut"))
file_input0 = TFile(inputFiles[0][0])
file_input1 = TFile(inputFiles[1][0])
file_input2 = TFile(inputFiles[2][0])
file_input3 = TFile(inputFiles[3][0])

tree_data = file_data.Get("DelayedPhoton")
tree_in0 = file_input0.Get("DelayedPhoton")
tree_in1 = file_input1.Get("DelayedPhoton")
tree_in2 = file_input2.Get("DelayedPhoton")
tree_in3 = file_input3.Get("DelayedPhoton")

print "fraction of nJets < 3: "

print "data -  "+str(tree_data.GetEntries(cut_data +" && n_Jets<3")*1.0/tree_data.GetEntries(cut_data))
print inputFiles[0][1]+" -  "+str(tree_in0.GetEntries(cut +" && n_Jets<3")*1.0/tree_in0.GetEntries(cut))
print inputFiles[1][1]+" -  "+str(tree_in1.GetEntries(cut + " && n_Jets<3")*1.0/tree_in1.GetEntries(cut))
print inputFiles[2][1]+" -  "+str(tree_in2.GetEntries(cut + " && n_Jets<3")*1.0/tree_in2.GetEntries(cut))
print inputFiles[3][1]+" -  "+str(tree_in3.GetEntries(cut + " && n_Jets<3")*1.0/tree_in3.GetEntries(cut))


histthis_data = TH1F("hist_nJets_data","; number of jets; Events", 15, -0.5, 14.5)
histthis0 = TH1F("hist_nJets_"+inputFiles[0][1],"; number of jets; Events", 15, -0.5, 14.5)
histthis1 = TH1F("hist_nJets_"+inputFiles[1][1],"; number of jets; Events", 15, -0.5, 14.5)
histthis2 = TH1F("hist_nJets_"+inputFiles[2][1],"; number of jets; Events", 15, -0.5, 14.5)
histthis3 = TH1F("hist_nJets_"+inputFiles[3][1],"; number of jets; Events", 15, -0.5, 14.5)

tree_data.Draw("n_Jets>>hist_nJets_data",cut_data)
tree_in0.Draw("n_Jets>>hist_nJets_"+inputFiles[0][1],cut)
tree_in1.Draw("n_Jets>>hist_nJets_"+inputFiles[1][1],cut)
tree_in2.Draw("n_Jets>>hist_nJets_"+inputFiles[2][1],cut)
tree_in3.Draw("n_Jets>>hist_nJets_"+inputFiles[3][1],cut)

histthis_data.SetLineWidth( 3 )
histthis0.SetLineWidth( 3 )
histthis1.SetLineWidth( 3 )
histthis2.SetLineWidth( 3 )
histthis3.SetLineWidth( 3 )
histthis_data.SetLineColor( 1 )
histthis0.SetLineColor( 2 )
histthis1.SetLineColor( 3 )
histthis2.SetLineColor( 4 )
histthis3.SetLineColor( 5 )

histthis_data.Scale(0.5/histthis_data.Integral())
histthis0.Scale(1.0/histthis0.Integral())
histthis1.Scale(1.0/histthis1.Integral())
histthis2.Scale(1.0/histthis2.Integral())
histthis3.Scale(1.0/histthis3.Integral())

leg.AddEntry(histthis_data, "data*0.5","l")
leg.AddEntry(histthis0, inputFiles[0][1],"l")
leg.AddEntry(histthis1, inputFiles[1][1],"l")
leg.AddEntry(histthis2, inputFiles[2][1],"l")
leg.AddEntry(histthis3, inputFiles[3][1],"l")

histthis0.GetYaxis().SetRangeUser(0.0, 1.3*max(histthis_data.GetMaximum(), histthis0.GetMaximum(), histthis1.GetMaximum(), histthis2.GetMaximum(), histthis3.GetMaximum()))

histthis0.GetXaxis().SetTitleSize( axisTitleSize )
histthis0.GetXaxis().SetTitleOffset( axisTitleOffset )
histthis0.GetYaxis().SetTitleSize( axisTitleSize )
histthis0.GetYaxis().SetTitleOffset( axisTitleOffset )

histthis0.Draw("hist")
histthis_data.Draw("Esame")
histthis1.Draw("histsame")
histthis2.Draw("histsame")
histthis3.Draw("histsame")
	
leg.Draw()
myC.SaveAs(outputDir+"nJets/nJets.pdf")
myC.SaveAs(outputDir+"nJets/nJets.png")
myC.SaveAs(outputDir+"nJets/nJets.C")
