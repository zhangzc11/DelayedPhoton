from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors, TMultiGraph
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import weight_cut, cut
from config_noBDT import outputDir

		
os.system("mkdir -p "+outputDir+"/stack/")
	

gROOT.SetBatch(True)


gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

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

def properScale(hist, norm):
        #norm = 1.0/hist.Integral()
        for i in range(0, hist.GetNbinsX()+1):
                v0 = hist.GetBinContent(i)
                hist.SetBinContent(i, norm*v0)
                if v0 > 0.0000001:
                        hist.SetBinError(i, norm*v0/np.sqrt(v0))
                else:
                        hist.SetBinError(i, 0.0)


print "cut ====> "+cut

cut_noHLT = "pho1Pt > 70 && pho1R9 > 0.9 &&  abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && pho1passSmajorTight && n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0"

weightedcut =  weight_cut + "("+cut_noHLT+")"

inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/"

tableFileName = "./effTable.txt"

samples = ["L200TeV_Ctau200cm", "L200TeV_Ctau10cm", "L100TeV_Ctau200cm", "L300TeV_Ctau200cm"]


colors = [632, 416, 600, 880, 54, 13, 18, 80, 50, 34, 32, 67, 8, 80, 91, 93, 97,  2, 18, 16, 13]	
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

hist_mass = []

idx_sample = 0

mg_mass = TMultiGraph()
mg_mass_zoom = TMultiGraph()
gr_mass = []

for sample in samples:
	print "plotting sample: "+sample
	fileName = inputDir+"GMSB_"+sample+"_13TeV-pythia8.root"
	fileThis = TFile(fileName, "READ")			
	treeThis = fileThis.Get("DelayedPhoton")
	hist_this = TH1F("hist_mass_"+sample, "hist_mass_"+sample, 200, 0, 1000)
	treeThis.Draw("sqrt(2*pho1Pt*pho2Pt*(cosh(pho1Eta-pho2Eta)-cos(pho1Phi-pho2Phi)))>>hist_mass_"+sample, weightedcut)
	properScale(hist_this, 1.0/hist_this.Integral())
	
	gr_this_zoom = TGraphErrors(hist_this)
	gr_this_zoom.SetLineColor(colors[idx_sample])
	gr_this_zoom.SetLineWidth(2)
	mg_mass_zoom.Add(gr_this_zoom)
	gr_mass.append(gr_this_zoom)
	
	hist_this_rebin = hist_this.Rebin(2)
	gr_this = TGraphErrors(hist_this_rebin)
	gr_this.SetLineColor(colors[idx_sample])
	gr_this.SetLineWidth(2)
	mg_mass.Add(gr_this)

	idx_sample = idx_sample + 1
	
myC.SetLogy(1)

mg_mass_zoom.Draw("AP")
mg_mass_zoom.GetYaxis().SetRangeUser(1e-5, 0.5)
mg_mass_zoom.GetXaxis().SetRangeUser(0.0, 100)
mg_mass_zoom.GetXaxis().SetTitle( "M_{#gamma#gamma} [GeV]" )
mg_mass_zoom.GetXaxis().SetTitleSize( axisTitleSize )
mg_mass_zoom.GetXaxis().SetTitleOffset( axisTitleOffset )
mg_mass_zoom.GetYaxis().SetTitleSize( axisTitleSize )
mg_mass_zoom.GetYaxis().SetTitleOffset( axisTitleOffset )
mg_mass_zoom.GetYaxis().SetTitle("events")
mg_mass_zoom.SetTitle("")

leg = TLegend(0.18, 0.75, 0.93, 0.92)
leg.SetNColumns(2)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(0)
leg.SetFillStyle(1001)

for idx in range(len(gr_mass)):
	leg.AddEntry(gr_mass[idx], samples[idx],"lep")

leg.Draw()

myC.SaveAs(outputDir+"/stack/diphoton_mass_signals_zoom.pdf")
myC.SaveAs(outputDir+"/stack/diphoton_mass_signals_zoom.png")
myC.SaveAs(outputDir+"/stack/diphoton_mass_signals_zoom.C")

mg_mass.Draw("AP")
mg_mass.GetYaxis().SetRangeUser(1e-5, 0.5)
mg_mass.GetXaxis().SetRangeUser(0.0, 1000)
mg_mass.GetXaxis().SetTitle( "M_{#gamma#gamma} [GeV]" )
mg_mass.GetXaxis().SetTitleSize( axisTitleSize )
mg_mass.GetXaxis().SetTitleOffset( axisTitleOffset )
mg_mass.GetYaxis().SetTitleSize( axisTitleSize )
mg_mass.GetYaxis().SetTitleOffset( axisTitleOffset )
mg_mass.GetYaxis().SetTitle("events")
mg_mass.SetTitle("")

leg.Draw()

myC.SaveAs(outputDir+"/stack/diphoton_mass_signals.pdf")
myC.SaveAs(outputDir+"/stack/diphoton_mass_signals.png")
myC.SaveAs(outputDir+"/stack/diphoton_mass_signals.C")
