from ROOT import *
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
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L150TeV_Ctau200cm_13TeV-pythia8.root', 'L150TeV_Ctau200cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root', 'L200TeV_Ctau200cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L250TeV_Ctau200cm_13TeV-pythia8.root', 'L250TeV_Ctau200cm'],
		['/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root', 'L350TeV_Ctau200cm'],
		#['../GMSB_L250TeV_Ctau10cm_13TeV-pythia8.root', 'L250TeV_Ctau10cm']	
	 	]

os.system("mkdir -p "+outputDir+"/nJets/")

cut = "(weight*pileupWeight)* (pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2)"


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

allHist = []
leg = TLegend(0.6, 0.65, 0.8, 0.85)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(0)
leg.SetFillStyle(1001)

index = 0
for finput in inputFiles:
	file_input = TFile(finput[0])
	tree_in = file_input.Get("DelayedPhoton")
	histthis = TH1F("hist_nJets_"+finput[1],"; number of jets; Events", 15, -0.5, 14.5)
	tree_in.Draw("n_Jets>>hist_nJets_"+finput[1],cut)
	histthis.GetXaxis().SetTitleSize( axisTitleSize )
	histthis.GetXaxis().SetTitleOffset( axisTitleOffset )
	histthis.GetYaxis().SetTitleSize( axisTitleSize )
	histthis.GetYaxis().SetTitleOffset( axisTitleOffset )
	histthis.SetLineWidth( 2 )
	histthis.SetLineColor( index+1 )
	if histthis.Integral() > 0.0:
		histthis.Scale(1.0/histthis.Integral())
	allHist.append(histthis)
	leg.AddEntry("hist_nJets_"+finput[1],finput[1],"l")
	if index == 0:
		histthis.Draw("hist")
	else:
		histthis.Draw("histsame")
	index = index +1
	
leg.Draw()
myC.SaveAs("plots/nJets_Ctau200.pdf")
myC.SaveAs("plots/nJets_Ctau200.png")
myC.SaveAs("plots/nJets_Ctau200.C")
