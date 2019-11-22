from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import lumi
from config_noBDT import kFactor
from config_noBDT import outputDir

splots = []

time_binning = np.array([-5.0, -2.0, -1.0, 0.0, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.1, 2.4, 3.0, 4.0, 5.0, 6.0, 8.0, 12.0, 20.0])
#time_binning = np.arange(-5.0, 25.0, 1.0)
#MET_binning = np.array([0.0, 60.0, 100.0, 140.0, 200.0, 300.0, 450.0, 650.0, 1000.0])
MET_binning = np.arange(0.0, 1000.0, 20.0)
nPV_binning = np.arange(-0.5, 49.5, 1.0)
nJets_binning = np.arange(-0.5, 14.5, 1.0)


splots.append(["t1MET", "MET_log", "#slash{E}_{T} [GeV]", MET_binning, True])
splots.append(["pho1ClusterTime_SmearToData", "phoTimeCluster_log", "#gamma cluster time [ns]", time_binning, True])
splots.append(["pho1Pt", "phoPt_log", "p_{T}^{#gamma} [GeV]", np.arange(40.0, 1000.0, 20.0), True])
splots.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta_log", "#sigma_{i#eta i#eta}", np.arange(0.005,0.025, 0.001), True])

splots.append(["t1MET", "MET_linear", "#slash{E}_{T} [GeV]", MET_binning, False])
splots.append(["pho1ClusterTime_SmearToData", "phoTimeCluster_linear", "#gamma cluster time [ns]", time_binning, False])

splots.append(["n_Jets", "nJets_linear", "number of jets", nJets_binning, False])
splots.append(["n_Jets", "nJets_log", "number of jets", nJets_binning, True])

splots.append(["nPV", "nPV_linear", "number of vertices", nPV_binning, False])
splots.append(["nPV", "nPV_log", "number of vertices", nPV_binning, True])

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/stack")
os.system("cp official_vs_private.py "+outputDir+"/stack")
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

inputDir = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/'

samples = [
		['GMSB_L200TeV_Ctau200cm_13TeV-pythia8', 'L200TeV_Ctau200cm', 0.04445]
	  ]


os.system("mkdir -p "+outputDir+"/stack/")

cut = "(weight*pileupWeight*triggerEffSFWeight*photonEffSF*triggerEffWeight)" # * (n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2 && nTightMuons < 1  && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0)"

def properScale(hist, norm):
        #norm = 1.0/hist.Integral()
        for i in range(0, hist.GetNbinsX()+1):
                v0 = hist.GetBinContent(i)
                hist.SetBinContent(i, norm*v0)
                if v0 > 0.0000001:
                        hist.SetBinError(i, norm*v0/(np.sqrt(v0)))
                else:
                        hist.SetBinError(i, 0.0)

for sample in samples:
	
	file_input_official = TFile(inputDir+sample[0]+".root")
	tree_in_official = file_input_official.Get("DelayedPhoton")
	file_input_private = TFile(inputDir+sample[0]+"_private.root")
	tree_in_private = file_input_private.Get("DelayedPhoton")
	
	hNEvents_official = file_input_official.Get("NEvents")
	NEvents_official = hNEvents_official.GetBinContent(1)
	hNEvents_private = file_input_private.Get("NEvents")
	NEvents_private = hNEvents_private.GetBinContent(1)
	
	for plot in splots:
		myC = TCanvas( "myC", "myC", 200, 10, 800, 800 )
		myC.SetHighLightColor(2)
		myC.SetFillColor(0)
		myC.SetBorderMode(0)
		myC.SetBorderSize(2)
		myC.SetLeftMargin( leftMargin )
		myC.SetRightMargin( 0.05 )
		myC.SetTopMargin( topMargin )
		myC.SetBottomMargin( bottomMargin )
		myC.SetFrameBorderMode(0)
		myC.SetFrameBorderMode(0)

		pad1 = TPad("pad1","pad1", 0.05, 0.3,0.95, 0.97)
		pad1.SetBottomMargin(0)
		pad1.SetRightMargin( 0.05 )
		pad1.SetLeftMargin( leftMargin )
		pad1.SetLogy(plot[4])
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
		hist_official = TH1F("hist"+plot[1]+"_official","", len(plot[3])-1, plot[3])
		hist_private = TH1F("hist"+plot[1]+"_private","", len(plot[3])-1, plot[3])
		tree_in_official.Draw(plot[0]+">>hist"+plot[1]+"_official",cut)
		tree_in_private.Draw(plot[0]+">>hist"+plot[1]+"_private",cut)

		if hist_official.Integral() > 0.0:
			properScale(hist_official, lumi*sample[2]/NEvents_official)
		if hist_private.Integral() > 0.0:
			properScale(hist_private, lumi*sample[2]/NEvents_private)

		hist_official.SetTitle("")
		hist_official.SetLineWidth(2)
		hist_official.SetLineColor(kBlue)
		hist_official.SetMarkerColor(kBlue)
		hist_official.SetMarkerStyle( 20 )
		hist_official.Draw("E")
		hist_official.GetXaxis().SetTitleSize( axisTitleSize )
		hist_official.GetXaxis().SetTitleOffset( axisTitleOffset )
		hist_official.GetYaxis().SetTitle( "Events" )
		hist_official.GetYaxis().SetTitleSize( axisTitleSize )
		hist_official.GetYaxis().SetTitleOffset( axisTitleOffset )
		if plot[4]:
			hist_official.GetYaxis().SetRangeUser(1e-4, max(hist_official.GetMaximum(), hist_private.GetMaximum())*100.0 )
		else:
			hist_official.GetYaxis().SetRangeUser(0, max(hist_official.GetMaximum(), hist_private.GetMaximum())*1.5 )

		hist_private.SetLineWidth(2)
		hist_private.SetLineColor(kRed)
		hist_private.SetMarkerColor(kRed)
		hist_private.SetMarkerStyle( 22 )
		hist_private.Draw("sameE")

		leg = TLegend(0.6, 0.7, 0.88, 0.85)
		leg.SetBorderSize(0)
		leg.SetTextSize(0.045)
		leg.SetLineColor(1)
		leg.SetLineStyle(1)
		leg.SetLineWidth(1)
		leg.SetFillColor(0)
		leg.SetFillStyle(1001)
		leg.AddEntry(hist_official, "official sample","lep")
		leg.AddEntry(hist_private, "private sample","lep")
		leg.Draw()

		pad1.Update()
		pad2.cd()
		ratio = TH1F("ratio_"+plot[1],"", len(plot[3])-1, plot[3])
		ratio.Add(hist_private)
		ratio.Divide(hist_official)
		ratio.SetMarkerStyle( 20 )
		ratio.GetXaxis().SetTitle( plot[2] )
		ratio.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
		ratio.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
		ratio.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
		ratio.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
		ratio.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
		ratio.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
		ratio.SetMarkerColor( kBlue )
		ratio.SetLineColor( kBlue )
		ratio.GetYaxis().SetTitle( "ratio" )
		ratio.GetYaxis().SetRangeUser( 0.6, 1.4 )
		ratio.SetTitle("")
		ratio.GetYaxis().CenterTitle( True )
		ratio.GetYaxis().SetNdivisions( 508, False )
		ratio.SetStats( 0 )
		ratio.Draw("E")
		pad1.Update()
		pad2.Update()
		
		myC.SaveAs(outputDir+"/stack/official_vs_private_"+plot[1]+"_"+sample[1]+".pdf")
		myC.SaveAs(outputDir+"/stack/official_vs_private_"+plot[1]+"_"+sample[1]+".png")
		myC.SaveAs(outputDir+"/stack/official_vs_private_"+plot[1]+"_"+sample[1]+".C")

