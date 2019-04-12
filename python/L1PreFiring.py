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



def draw_var_twoCuts(filename, label, cut1, cut2, cut1label, cut2label, varName, varTitle, titleY, varBinning, logY = True):
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
	pad1 = TPad("pad1","pad1", 0.05, 0.3,0.95, 0.97)
        pad1.SetBottomMargin(0)
        pad1.SetRightMargin( rightMargin )
        pad1.SetLeftMargin( leftMargin )
        pad1.SetLogy(logY)
        pad1.Draw()

        pad2 = TPad("pad2","pad2", 0.05, 0.02, 0.95, 0.29)
        pad2.SetTopMargin(0.04)
        pad2.SetTopMargin(0.008)
        pad2.SetBottomMargin(0.4)
        pad2.SetRightMargin( rightMargin )
        pad2.SetLeftMargin( leftMargin )
        pad2.SetGridy()
        pad2.Draw()
	
	pad1.cd()

	hist1 = TH1F("hist1","; "+varTitle+"; "+titleY, len(varBinning)-1, varBinning)
	hist2 = TH1F("hist2","; "+varTitle+"; "+titleY, len(varBinning)-1, varBinning)
	
	treeThis.Draw(varName+">>hist1", cut1, "")
	treeThis.Draw(varName+">>hist2", cut2, "")
	
	properScale(hist1, 1.0/hist1.Integral())	
	properScale(hist2, 1.0/hist2.Integral())	

	hist1.SetLineColor(kBlue)
	hist1.SetMarkerColor(kBlue)
	hist1.SetMarkerStyle(20)
	
	hist2.SetLineColor(kRed)
	hist2.SetMarkerColor(kRed)
	hist2.SetMarkerStyle(21)

	hist1.SetTitle("")
        hist1.Draw("E")
        hist1.GetXaxis().SetTitleSize( axisTitleSize )
        hist1.GetXaxis().SetTitleOffset( axisTitleOffset )
        hist1.GetYaxis().SetTitleSize( axisTitleSize )
        hist1.GetYaxis().SetTitleOffset( axisTitleOffset )
        #hist1.GetYaxis().SetTitle("events")		
	hist2.Draw("sameE")	
	
	leg = TLegend(0.6, 0.7, 0.93, 0.89)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.045)
        leg.SetLineColor(1)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)
        leg.AddEntry(hist1, cut1label,"lep")
        leg.AddEntry(hist2, cut2label,"lep")
	leg.Draw()

	
	pad2.cd()
	ratio = TH1F("ratio","; "+varTitle+"; ratio", len(varBinning)-1, varBinning)

	ratio.Add(hist1)
	ratio.Divide(hist2)
	
	ratio.SetMarkerStyle( 20 )
        ratio.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
        ratio.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
        ratio.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
        ratio.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
        ratio.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
        ratio.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
        ratio.SetMarkerColor( kBlack )
        ratio.SetLineColor( kBlack )
        ratio.GetYaxis().SetRangeUser( 0.9, 1.1 )
        ratio.SetTitle("")
        ratio.GetYaxis().SetTitle("ratio")
        ratio.GetYaxis().CenterTitle( True )
        ratio.GetYaxis().SetNdivisions( 504, False )
        ratio.SetStats( 0 )
        ratio.Draw("E")
        ratio.GetXaxis().SetTitle(varTitle)
        pad1.Update()
        pad2.Update()
	
	drawCMS(myC, 13, lumi)

	myC.SaveAs(outputDir+"/stack/checkL1PreFiring_"+varName+"_"+label+".pdf")
	myC.SaveAs(outputDir+"/stack/checkL1PreFiring_"+varName+"_"+label+".png")
	myC.SaveAs(outputDir+"/stack/checkL1PreFiring_"+varName+"_"+label+".C")

cut_normal = "(weight*pileupWeight*triggerEffSFWeight*photonEffSF) * ((HLTDecision[81] == 1)&&pho1Pt > 70 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto  && pho1passSmajorTight && pho1Sminor<0.4 && pho1R9 > 0.9&& pho1passSigmaIetaIetaTight&& pho1passHoverETight&&n_Jets > 2&&nTightMuons == 0&& n_Photons == 2&&Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho2SigmaIetaIeta<0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso<30.0 && pho2sumNeutralHadronEt<30.0 && pho2trkSumPtHollowConeDR03 < 30.0) "	
cut_L1PreFiring = cut_normal + " * (!hasJetL1PreFiring)"

time_binning = np.array([-2.0, 0.0, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.1, 2.4, 3.0, 20.0])
MET_binning = np.array([0, 80., 110., 130.0, 150., 170.0, 200.0, 300., 1000.])
	
draw_var_twoCuts("GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "GMSB_L200TeV_Ctau200cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "pho1ClusterTime_SmearToData", "#gamma cluster time [ns]","arbitary unit", time_binning, True)
draw_var_twoCuts("GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root", "GMSB_L200TeV_Ctau200cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "t1MET", "MET [GeV]","arbitary unit", MET_binning, True)

draw_var_twoCuts("GMSB_L300TeV_Ctau200cm_13TeV-pythia8.root", "GMSB_L300TeV_Ctau200cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "pho1ClusterTime_SmearToData", "#gamma cluster time [ns]","arbitary unit", time_binning, True)
draw_var_twoCuts("GMSB_L300TeV_Ctau200cm_13TeV-pythia8.root", "GMSB_L300TeV_Ctau200cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "t1MET", "MET [GeV]","arbitary unit", MET_binning, True)


time_binning = np.array([-2.0, -1.0, -0.5, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 2.0, 5.0])
MET_binning = np.array([0, 50., 80., 110., 130.0, 150., 170.0, 200.0, 300., 500.0, 1000.])

draw_var_twoCuts("GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root", "GMSB_L200TeV_Ctau0_1cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "pho1ClusterTime_SmearToData", "#gamma cluster time [ns]","arbitary unit", time_binning, True)
draw_var_twoCuts("GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root", "GMSB_L200TeV_Ctau0_1cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "t1MET", "MET [GeV]","arbitary unit", MET_binning, True)

draw_var_twoCuts("GMSB_L300TeV_Ctau0_1cm_13TeV-pythia8.root", "GMSB_L300TeV_Ctau0_1cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "pho1ClusterTime_SmearToData", "#gamma cluster time [ns]","arbitary unit", time_binning, True)
draw_var_twoCuts("GMSB_L300TeV_Ctau0_1cm_13TeV-pythia8.root", "GMSB_L300TeV_Ctau0_1cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "t1MET", "MET [GeV]","arbitary unit", MET_binning, True)

time_binning = np.array([-2.0, 0.0, 1.0, 2.0, 20.0])
MET_binning = np.array([0, 80., 110., 150., 200.0, 300., 1000.])
draw_var_twoCuts("GMSB_L200TeV_Ctau1000cm_13TeV-pythia8.root", "GMSB_L200TeV_Ctau1000cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "pho1ClusterTime_SmearToData", "#gamma cluster time [ns]","arbitary unit", time_binning, True)
draw_var_twoCuts("GMSB_L200TeV_Ctau1000cm_13TeV-pythia8.root", "GMSB_L200TeV_Ctau1000cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "t1MET", "MET [GeV]","arbitary unit", MET_binning, True)

draw_var_twoCuts("GMSB_L300TeV_Ctau1000cm_13TeV-pythia8.root", "GMSB_L300TeV_Ctau1000cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "pho1ClusterTime_SmearToData", "#gamma cluster time [ns]","arbitary unit", time_binning, True)
draw_var_twoCuts("GMSB_L300TeV_Ctau1000cm_13TeV-pythia8.root", "GMSB_L300TeV_Ctau1000cm", cut_normal, cut_L1PreFiring, "normal selection", "Prefire test", "t1MET", "MET [GeV]","arbitary unit", MET_binning, True)

