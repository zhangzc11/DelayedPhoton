from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TH2F
import os, sys
from Aux import *
from config_noBDT import fileNameData, fileNameSig, fileNameGJets, fileNameQCD, cut, cut_noDisc, cut_noSigmaIetaIeta, cut_GJets_noSigmaIetaIeta, splots, lumi, outputDir, xsecSig, xsecGJets, xsecQCD, cut_noSminor, cut_GJets_noSminor, cut_blindMET, cut_blindTime, cut_MET_filter
from config_noBDT import fractionGJets, fractionQCD, useFraction, kFactor, cut_GJets, xbins_MET, xbins_time, sigLegend, weight_cut
from config_noBDT import fileNameTTJets, fileNameWJets, xsecTTJets, xsecWJets, cut_EWKCR, fileNameEWKG, xsecEWKG
import numpy as np
import array

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir+"/METCorrPlots")
os.system("mkdir -p "+outputDir+"/METCorrPlots")
os.system("cp config_noBDT.py "+outputDir+"/METCorrPlots/")
os.system("cp METCorrPlot.py "+outputDir+"/METCorrPlots/")
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


def properScale(hist, norm):
        #norm = 1.0/hist.Integral()
        for i in range(0, hist.GetNbinsX()+1):
                v0 = hist.GetBinContent(i)
                hist.SetBinContent(i, norm*v0)
                if v0 > 0.0000001:
                        hist.SetBinError(i, norm*v0/np.sqrt(v0))
                else:
                        hist.SetBinError(i, 0.0)

def make_overlapPlots(fileName, label, cut_this):
	fileThis = TFile(fileName)

	tree = fileThis.Get("DelayedPhoton")
	hNEvents = fileThis.Get("NEvents")
	NEvents = hNEvents.GetBinContent(1)

	print "file ==> "+fileName
	print "cut ==> "+cut_this
	print "Entries ==> "+str(tree.GetEntries(cut_this))
	
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

	#dR(pho1, pho2)
	myC.SetLogy(0)
	hist_dR_pho1_pho2 = TH1F("hist_dR_pho1_pho2","; #DeltaR(#gamma1, #gamma2); Events/0.01", 1000, -0.1, 9.9)
	tree.Draw("sqrt((pho1Eta-pho2Eta)*(pho1Eta-pho2Eta) + (pho1Phi-pho2Phi)*(pho1Phi-pho2Phi))>>hist_dR_pho1_pho2", cut_this)
	if hist_dR_pho1_pho2.Integral() > 0:
		properScale(hist_dR_pho1_pho2, 1.0/hist_dR_pho1_pho2.Integral())
	hist_dR_pho1_pho2.SetLineWidth(3)
	hist_dR_pho1_pho2.SetLineColor( kRed )
	hist_dR_pho1_pho2.Draw("E")
	hist_dR_pho1_pho2.GetXaxis().SetTitleSize( axisTitleSize )
	hist_dR_pho1_pho2.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_dR_pho1_pho2.GetYaxis().SetTitleSize( axisTitleSize )
	hist_dR_pho1_pho2.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_dR_pho1_pho2.GetYaxis().SetRangeUser(0.0, 1.5*hist_dR_pho1_pho2.GetMaximum())
	hist_dR_pho1_pho2.GetXaxis().SetRangeUser(-0.1, 3.0)

	frac_dR0p3 =  100.0*hist_dR_pho1_pho2.Integral(1,41)

	tlatex_2pho = TLatex()
	tlatex_2pho.SetNDC()
	tlatex_2pho.SetTextAlign(11)
	tlatex_2pho.DrawLatex(0.4,0.85, "fraction of #DeltaR < 0.3: "+"%.1f" % frac_dR0p3+"%")

	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_"+label+".C")



	#dR(pho1, pho2), where both pho1 and pho2 are OOT
	myC.SetLogy(0)
	hist_dR_pho1_pho2_OOTOOT = TH1F("hist_dR_pho1_pho2_OOTOOT","; #DeltaR(#gamma1, #gamma2); Events/0.01", 1000, -0.1, 9.9)
	tree.Draw("sqrt((pho1Eta-pho2Eta)*(pho1Eta-pho2Eta) + (pho1Phi-pho2Phi)*(pho1Phi-pho2Phi))>>hist_dR_pho1_pho2_OOTOOT", cut_this+"&& !pho1isStandardPhoton && !pho2isStandardPhoton")
	if hist_dR_pho1_pho2_OOTOOT.Integral() > 0:
		properScale(hist_dR_pho1_pho2_OOTOOT, 1.0/hist_dR_pho1_pho2_OOTOOT.Integral())
	hist_dR_pho1_pho2_OOTOOT.SetLineWidth(3)
	hist_dR_pho1_pho2_OOTOOT.SetLineColor( kRed )
	hist_dR_pho1_pho2_OOTOOT.Draw("E")
	hist_dR_pho1_pho2_OOTOOT.GetXaxis().SetTitleSize( axisTitleSize )
	hist_dR_pho1_pho2_OOTOOT.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_dR_pho1_pho2_OOTOOT.GetYaxis().SetTitleSize( axisTitleSize )
	hist_dR_pho1_pho2_OOTOOT.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_dR_pho1_pho2_OOTOOT.GetYaxis().SetRangeUser(0.0, 1.5*hist_dR_pho1_pho2_OOTOOT.GetMaximum())
	hist_dR_pho1_pho2_OOTOOT.GetXaxis().SetRangeUser(-0.1, 3.0)

	frac_dR0p3 =  100.0*hist_dR_pho1_pho2_OOTOOT.Integral(1,41)

	tlatex_2pho = TLatex()
	tlatex_2pho.SetNDC()
	tlatex_2pho.SetTextAlign(11)
	tlatex_2pho.DrawLatex(0.4,0.85, "fraction of #DeltaR < 0.3: "+"%.1f" % frac_dR0p3+"%")

	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_OOTOOT_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_OOTOOT_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_OOTOOT_"+label+".C")


	#dR(pho1, pho2), inT vs OOT
	myC.SetLogy(0)
	hist_dR_pho1_pho2_inTOOT = TH1F("hist_dR_pho1_pho2_inTOOT","; #DeltaR(#gamma1, #gamma2); Events/0.01", 1000, -0.1, 9.9)
	tree.Draw("sqrt((pho1Eta-pho2Eta)*(pho1Eta-pho2Eta) + (pho1Phi-pho2Phi)*(pho1Phi-pho2Phi))>>hist_dR_pho1_pho2_inTOOT", cut_this+"&& (pho1isStandardPhoton && !pho2isStandardPhoton) || (!pho1isStandardPhoton && pho2isStandardPhoton)")
	if hist_dR_pho1_pho2_inTOOT.Integral() > 0:
		properScale(hist_dR_pho1_pho2_inTOOT, 1.0/hist_dR_pho1_pho2_inTOOT.Integral())
	hist_dR_pho1_pho2_inTOOT.SetLineWidth(3)
	hist_dR_pho1_pho2_inTOOT.SetLineColor( kRed )
	hist_dR_pho1_pho2_inTOOT.Draw("E")
	hist_dR_pho1_pho2_inTOOT.GetXaxis().SetTitleSize( axisTitleSize )
	hist_dR_pho1_pho2_inTOOT.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_dR_pho1_pho2_inTOOT.GetYaxis().SetTitleSize( axisTitleSize )
	hist_dR_pho1_pho2_inTOOT.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_dR_pho1_pho2_inTOOT.GetYaxis().SetRangeUser(0.0, 1.5*hist_dR_pho1_pho2_inTOOT.GetMaximum())
	hist_dR_pho1_pho2_inTOOT.GetXaxis().SetRangeUser(-0.1, 3.0)

	frac_dR0p3 =  100.0*hist_dR_pho1_pho2_inTOOT.Integral(1,41)

	tlatex_2pho = TLatex()
	tlatex_2pho.SetNDC()
	tlatex_2pho.SetTextAlign(11)
	tlatex_2pho.DrawLatex(0.4,0.85, "fraction of #DeltaR < 0.3: "+"%.1f" % frac_dR0p3+"%")

	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_inTOOT_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_inTOOT_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_inTOOT_"+label+".C")


	#dR(pho1, pho2), inT vs inT
	myC.SetLogy(0)
	hist_dR_pho1_pho2_inTinT = TH1F("hist_dR_pho1_pho2_inTinT","; #DeltaR(#gamma1, #gamma2); Events/0.01", 1000, -0.1, 9.9)
	tree.Draw("sqrt((pho1Eta-pho2Eta)*(pho1Eta-pho2Eta) + (pho1Phi-pho2Phi)*(pho1Phi-pho2Phi))>>hist_dR_pho1_pho2_inTinT", cut_this+"&& pho1isStandardPhoton && pho2isStandardPhoton")
	if hist_dR_pho1_pho2_inTinT.Integral() > 0:
		properScale(hist_dR_pho1_pho2_inTinT, 1.0/hist_dR_pho1_pho2_inTinT.Integral())
	hist_dR_pho1_pho2_inTinT.SetLineWidth(3)
	hist_dR_pho1_pho2_inTinT.SetLineColor( kRed )
	hist_dR_pho1_pho2_inTinT.Draw("E")
	hist_dR_pho1_pho2_inTinT.GetXaxis().SetTitleSize( axisTitleSize )
	hist_dR_pho1_pho2_inTinT.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_dR_pho1_pho2_inTinT.GetYaxis().SetTitleSize( axisTitleSize )
	hist_dR_pho1_pho2_inTinT.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_dR_pho1_pho2_inTinT.GetYaxis().SetRangeUser(0.0, 1.5*hist_dR_pho1_pho2_inTinT.GetMaximum())
	hist_dR_pho1_pho2_inTinT.GetXaxis().SetRangeUser(-0.1, 3.0)

	frac_dR0p3 =  100.0*hist_dR_pho1_pho2_inTinT.Integral(1,41)

	tlatex_2pho = TLatex()
	tlatex_2pho.SetNDC()
	tlatex_2pho.SetTextAlign(11)
	tlatex_2pho.DrawLatex(0.4,0.85, "fraction of #DeltaR < 0.3: "+"%.1f" % frac_dR0p3+"%")

	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_inTinT_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_inTinT_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/dR_pho1_pho2_inTinT_"+label+".C")




def make_METCorrPlots(fileName, label, cut_this):
##############load delayed photon input tree#############
	fileThis = TFile(fileName)

	tree = fileThis.Get("DelayedPhoton")
	hNEvents = fileThis.Get("NEvents")
	NEvents = hNEvents.GetBinContent(1)

	print "file ==> "+fileName
	print "cut ==> "+cut_this
	print "Entries ==> "+str(tree.GetEntries(cut_this))

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

	#number of overlap photons
	myC.SetLogy(1)
	hist_nPhotons_overlap = TH1F("hist_nPhotons_overlap","; Num of Cleaned Photons; Events", 10, -0.5, 9.5)
	tree.Draw("nPhotons_overlap>>hist_nPhotons_overlap", cut_this)
	properScale(hist_nPhotons_overlap, 1.0/hist_nPhotons_overlap.Integral())
	hist_nPhotons_overlap.SetLineWidth(3)
	hist_nPhotons_overlap.SetLineColor( kRed )
	hist_nPhotons_overlap.Draw("E")
	hist_nPhotons_overlap.GetXaxis().SetTitleSize( axisTitleSize )
	hist_nPhotons_overlap.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_nPhotons_overlap.GetYaxis().SetTitleSize( axisTitleSize )
	hist_nPhotons_overlap.GetYaxis().SetTitleOffset( axisTitleOffset )

	frac_overlap =  100.0*hist_nPhotons_overlap.Integral(2,10)

	tlatex = TLatex()
	tlatex.SetNDC()
	tlatex.SetTextAlign(11)
	tlatex.DrawLatex(0.4,0.85, "fraction of N > 0: "+"%.1f" % frac_overlap+"%")

	myC.SaveAs(outputDir+"/METCorrPlots/nPhotons_overlap_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/nPhotons_overlap_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/nPhotons_overlap_"+label+".C")

	gStyle.SetOptStat(1)
	#delta_pho1_Pt(reco, gen)
	myC.SetLogy(0)
	hist_pho1_deltaPt = TH1F("hist_pho1_deltaPt","; #Delta p_{T}(RECO, GEN) (GeV), #gamma1; Events", 100, -200, 200)
	tree.Draw("pho1Pt - pho1GenPt >>hist_pho1_deltaPt", cut_this)
	properScale(hist_pho1_deltaPt, 1.0/hist_pho1_deltaPt.Integral())
	hist_pho1_deltaPt.SetLineWidth(3)
	hist_pho1_deltaPt.SetLineColor( kRed )
	hist_pho1_deltaPt.Draw("E")
	hist_pho1_deltaPt.GetXaxis().SetTitleSize( axisTitleSize )
	hist_pho1_deltaPt.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_pho1_deltaPt.GetYaxis().SetTitleSize( axisTitleSize )
	hist_pho1_deltaPt.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_pho1_deltaPt.GetYaxis().SetRangeUser(0.0, 1.5*hist_pho1_deltaPt.GetMaximum())

	myC.SaveAs(outputDir+"/METCorrPlots/pho1_deltaPt_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/pho1_deltaPt_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/pho1_deltaPt_"+label+".C")

	#delta_pho1_R(reco, gen)
	myC.SetLogy(0)
	hist_pho1_deltaR = TH1F("hist_pho1_deltaR","; #DeltaR(RECO, GEN), #gamma1; Events", 100, 0, 1.0)
	tree.Draw("sqrt((pho1Eta-pho1GenEta)*(pho1Eta-pho1GenEta) + (pho1Phi-pho1GenPhi)*(pho1Phi-pho1GenPhi)) >>hist_pho1_deltaR", cut_this)
	properScale(hist_pho1_deltaR, 1.0/hist_pho1_deltaR.Integral())
	hist_pho1_deltaR.SetLineWidth(3)
	hist_pho1_deltaR.SetLineColor( kRed )
	hist_pho1_deltaR.Draw("E")
	hist_pho1_deltaR.GetXaxis().SetTitleSize( axisTitleSize )
	hist_pho1_deltaR.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_pho1_deltaR.GetYaxis().SetTitleSize( axisTitleSize )
	hist_pho1_deltaR.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_pho1_deltaR.GetYaxis().SetRangeUser(0.0, 1.5*hist_pho1_deltaR.GetMaximum())

	myC.SaveAs(outputDir+"/METCorrPlots/pho1_deltaR_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/pho1_deltaR_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/pho1_deltaR_"+label+".C")

	#delta_pho2_Pt(reco, gen)
	myC.SetLogy(0)
	hist_pho2_deltaPt = TH1F("hist_pho2_deltaPt","; #Delta p_{T}(RECO, GEN), #gamma2 (GeV); Events", 100, -200, 200)
	tree.Draw("pho2Pt - pho2GenPt >>hist_pho2_deltaPt", cut_this)
	properScale(hist_pho2_deltaPt, 1.0/hist_pho2_deltaPt.Integral())
	hist_pho2_deltaPt.SetLineWidth(3)
	hist_pho2_deltaPt.SetLineColor( kRed )
	hist_pho2_deltaPt.Draw("E")
	hist_pho2_deltaPt.GetXaxis().SetTitleSize( axisTitleSize )
	hist_pho2_deltaPt.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_pho2_deltaPt.GetYaxis().SetTitleSize( axisTitleSize )
	hist_pho2_deltaPt.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_pho2_deltaPt.GetYaxis().SetRangeUser(0.0, 1.5*hist_pho2_deltaPt.GetMaximum())

	myC.SaveAs(outputDir+"/METCorrPlots/pho2_deltaPt_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/pho2_deltaPt_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/pho2_deltaPt_"+label+".C")

	#delta_pho2_R(reco, gen)
	myC.SetLogy(0)
	hist_pho2_deltaR = TH1F("hist_pho2_deltaR","; #DeltaR(RECO, GEN), #gamma2; Events", 100, 0, 1.0)
	tree.Draw("sqrt((pho2Eta-pho2GenEta)*(pho2Eta-pho2GenEta) + (pho2Phi-pho2GenPhi)*(pho2Phi-pho2GenPhi)) >>hist_pho2_deltaR", cut_this)
	properScale(hist_pho2_deltaR, 1.0/hist_pho2_deltaR.Integral())
	hist_pho2_deltaR.SetLineWidth(3)
	hist_pho2_deltaR.SetLineColor( kRed )
	hist_pho2_deltaR.Draw("E")
	hist_pho2_deltaR.GetXaxis().SetTitleSize( axisTitleSize )
	hist_pho2_deltaR.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_pho2_deltaR.GetYaxis().SetTitleSize( axisTitleSize )
	hist_pho2_deltaR.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_pho2_deltaR.GetYaxis().SetRangeUser(0.0, 1.5*hist_pho2_deltaR.GetMaximum())

	myC.SaveAs(outputDir+"/METCorrPlots/pho2_deltaR_"+label+".pdf")
	myC.SaveAs(outputDir+"/METCorrPlots/pho2_deltaR_"+label+".png")
	myC.SaveAs(outputDir+"/METCorrPlots/pho2_deltaR_"+label+".C")



	gStyle.SetOptStat(0)
	#MET vs time 2D plot

	myC2 = TCanvas( "myC2", "myC2", 200, 10, 800, 800 )
	myC2.SetHighLightColor(2)
	myC2.SetFillColor(0)
	myC2.SetBorderMode(0)
	myC2.SetBorderSize(2)
	myC2.SetLeftMargin( leftMargin )
	myC2.SetRightMargin( rightMargin*2 )
	myC2.SetTopMargin( topMargin )
	myC2.SetBottomMargin( bottomMargin )
	myC2.SetFrameBorderMode(0)
	myC2.SetFrameBorderMode(0)
	myC2.SetLogy(0)
	myC2.SetGridx()
	myC2.SetGridy()

	h2_MET_vs_time_raw = TH2F("h2_MET_vs_time_raw", "; photon time (ns);  uncorrected #slash{E}_{T} (GeV)", 100, -5, 15, 100, 0, 2000)
	tree.Draw("t1MET_raw:pho1ClusterTime_SmearToData>>h2_MET_vs_time_raw", cut_this)
	h2_MET_vs_time_raw.Draw("colz")
		
	h2_MET_vs_time_raw.GetXaxis().SetTitleSize( axisTitleSize )
	h2_MET_vs_time_raw.GetXaxis().SetTitleOffset( axisTitleOffset )
	h2_MET_vs_time_raw.GetYaxis().SetTitleSize( axisTitleSize )
	h2_MET_vs_time_raw.GetYaxis().SetTitleOffset( axisTitleOffset*1.2 )
	myC2.SaveAs(outputDir+"/METCorrPlots/MET_vs_time_raw_"+label+".pdf")
	myC2.SaveAs(outputDir+"/METCorrPlots/MET_vs_time_raw_"+label+".png")
	myC2.SaveAs(outputDir+"/METCorrPlots/MET_vs_time_raw_"+label+".C")


	h2_MET_vs_time_corr = TH2F("h2_MET_vs_time_corr", "; photon time (ns);  corrected #slash{E}_{T} (GeV)", 100, -5, 15, 100, 0, 2000)
	tree.Draw("t1MET:pho1ClusterTime_SmearToData>>h2_MET_vs_time_corr", cut_this)
	h2_MET_vs_time_corr.Draw("colz")
		
	h2_MET_vs_time_corr.GetXaxis().SetTitleSize( axisTitleSize )
	h2_MET_vs_time_corr.GetXaxis().SetTitleOffset( axisTitleOffset )
	h2_MET_vs_time_corr.GetYaxis().SetTitleSize( axisTitleSize )
	h2_MET_vs_time_corr.GetYaxis().SetTitleOffset( axisTitleOffset*1.2 )
	myC2.SaveAs(outputDir+"/METCorrPlots/MET_vs_time_corr_"+label+".pdf")
	myC2.SaveAs(outputDir+"/METCorrPlots/MET_vs_time_corr_"+label+".png")
	myC2.SaveAs(outputDir+"/METCorrPlots/MET_vs_time_corr_"+label+".C")


	#MET of raw vs corr with ratios
	hist_MET_raw = TH1F("hist_MET_raw","; #slash{E}_{T} (GeV); Events", 100, 0.0,2000)
	hist_MET_corr = TH1F("hist_MET_corr","; #slash{E}_{T} (GeV); Events", 100, 0.0, 2000)
	hist_MET_ratio = TH1F("hist_MET_ratio","; #slash{E}_{T} (GeV); raw/cor", 100, 0.0, 2000)
	tree.Draw("t1MET_raw>>hist_MET_raw", cut_this)
	tree.Draw("t1MET>>hist_MET_corr", cut_this)
	properScale(hist_MET_raw, 1.0/hist_MET_raw.Integral())
	properScale(hist_MET_corr, 1.0/hist_MET_corr.Integral())
	hist_MET_raw.SetLineWidth(3)
	hist_MET_corr.SetLineWidth(3)
	hist_MET_raw.SetLineColor( kRed )
	hist_MET_corr.SetLineColor( kBlue )
	hist_MET_raw.GetXaxis().SetTitleSize( axisTitleSize )
	hist_MET_raw.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_MET_raw.GetYaxis().SetTitleSize( axisTitleSize )
	hist_MET_raw.GetYaxis().SetTitleOffset( axisTitleOffset )

	
	mean_MET_raw = hist_MET_raw.GetMean()
	mean_MET_corr = hist_MET_corr.GetMean()

	leg_MET = TLegend(0.5, 0.7, 0.93, 0.89)
        leg_MET.SetBorderSize(0)
        leg_MET.SetTextSize(0.04)
        leg_MET.SetLineColor(1)
        leg_MET.SetLineStyle(1)
        leg_MET.SetLineWidth(1)
        leg_MET.SetFillColor(0)
        leg_MET.SetFillStyle(1001)
        leg_MET.AddEntry(hist_MET_raw, "uncorrected (mean = "+"%.1f" % mean_MET_raw+")","lep")
        leg_MET.AddEntry(hist_MET_corr, "corrected (mean = "+"%.1f" % mean_MET_corr+")","lep")
	
	myC3 = TCanvas( "myC3", "myC3", 200, 10, 800, 800 )
        myC3.SetHighLightColor(2)
        myC3.SetFillColor(0)
        myC3.SetBorderMode(0)
        myC3.SetBorderSize(2)
        myC3.SetLeftMargin( leftMargin )
        myC3.SetRightMargin( rightMargin )
        myC3.SetTopMargin( topMargin )
        myC3.SetBottomMargin( bottomMargin )
        myC3.SetFrameBorderMode(0)
        myC3.SetFrameBorderMode(0)

        pad1 = TPad("pad1","pad1", 0.05, 0.3,0.95, 0.97)
        pad1.SetBottomMargin(0)
        pad1.SetRightMargin( rightMargin )
        pad1.SetLeftMargin( leftMargin )
        pad1.SetLogy(1)
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
	hist_MET_raw.Draw("E")
	hist_MET_corr.Draw("Esame")
	leg_MET.Draw()
	pad1.Update()

	pad2.cd()
	hist_MET_ratio.Add(hist_MET_raw)	
	hist_MET_ratio.Divide(hist_MET_corr)	
	
	hist_MET_ratio.SetMarkerStyle( 20 )
        hist_MET_ratio.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
        hist_MET_ratio.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
        hist_MET_ratio.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
        hist_MET_ratio.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
        hist_MET_ratio.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
        hist_MET_ratio.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
        hist_MET_ratio.SetMarkerColor( kBlue )
        hist_MET_ratio.SetLineColor( kBlue )
        hist_MET_ratio.GetYaxis().SetRangeUser( 0.0, 2.5 )
        hist_MET_ratio.SetTitle("")
        hist_MET_ratio.GetYaxis().CenterTitle( True )
        hist_MET_ratio.GetYaxis().SetNdivisions( 5, False )
        hist_MET_ratio.SetStats( 0 )
        hist_MET_ratio.Draw("E")
        pad1.Update()
        pad2.Update()

	myC3.SaveAs(outputDir+"/METCorrPlots/MET_raw_vs_corr_"+label+".pdf")
	myC3.SaveAs(outputDir+"/METCorrPlots/MET_raw_vs_corr_"+label+".png")
	myC3.SaveAs(outputDir+"/METCorrPlots/MET_raw_vs_corr_"+label+".C")
	
	#MET residualPt of raw vs corr
	hist_MET_residualPt_raw = TH1F("hist_MET_residualPt_raw","; #slash{E}_{T}^{GEN} - #slash{E}_{T}^{RECO} (GeV); Events", 40, -1000.0,1000)
	hist_MET_residualPt_corr = TH1F("hist_MET_residualPt_corr","; #slash{E}_{T}^{GEN} - #slash{E}_{T}^{RECO} (GeV); Events", 40, -1000.0, 1000)
	tree.Draw("genMetPt - t1MET_raw>>hist_MET_residualPt_raw", cut_this)
	tree.Draw("genMetPt - t1MET>>hist_MET_residualPt_corr", cut_this)
	properScale(hist_MET_residualPt_raw, 1.0/hist_MET_residualPt_raw.Integral())
	properScale(hist_MET_residualPt_corr, 1.0/hist_MET_residualPt_corr.Integral())
	hist_MET_residualPt_raw.SetLineWidth(3)
	hist_MET_residualPt_corr.SetLineWidth(3)
	hist_MET_residualPt_raw.SetLineColor( kRed )
	hist_MET_residualPt_corr.SetLineColor( kBlue )
	hist_MET_residualPt_raw.GetXaxis().SetTitleSize( axisTitleSize )
	hist_MET_residualPt_raw.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_MET_residualPt_raw.GetYaxis().SetTitleSize( axisTitleSize )
	hist_MET_residualPt_raw.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_MET_residualPt_raw.GetYaxis().SetRangeUser(0.0, 1.5*max(hist_MET_residualPt_raw.GetMaximum(), hist_MET_residualPt_corr.GetMaximum()))
	
	mean_MET_residualPt_raw = hist_MET_residualPt_raw.GetMean()
	stddev_MET_residualPt_raw = hist_MET_residualPt_raw.GetStdDev()
	mean_MET_residualPt_corr = hist_MET_residualPt_corr.GetMean()
	stddev_MET_residualPt_corr = hist_MET_residualPt_corr.GetStdDev()

	leg_MET_residualPt = TLegend(0.2, 0.75, 0.93, 0.89)
        leg_MET_residualPt.SetBorderSize(0)
        leg_MET_residualPt.SetTextSize(0.03)
        leg_MET_residualPt.SetLineColor(1)
        leg_MET_residualPt.SetLineStyle(1)
        leg_MET_residualPt.SetLineWidth(1)
        leg_MET_residualPt.SetFillColor(0)
        leg_MET_residualPt.SetFillStyle(1001)
        leg_MET_residualPt.AddEntry(hist_MET_residualPt_raw, "uncorrected (mean = "+"%.1f" % mean_MET_residualPt_raw+", StdDev = "+"%.1f" % stddev_MET_residualPt_raw+")","lep")
        leg_MET_residualPt.AddEntry(hist_MET_residualPt_corr, "corrected (mean = "+"%.1f" % mean_MET_residualPt_corr+", StdDev = "+"%.1f" % stddev_MET_residualPt_corr+")","lep")
	
	myC4 = TCanvas( "myC4", "myC4", 200, 10, 800, 800 )
        myC4.SetHighLightColor(2)
        myC4.SetFillColor(0)
        myC4.SetBorderMode(0)
        myC4.SetBorderSize(2)
        myC4.SetLeftMargin( leftMargin )
        myC4.SetRightMargin( rightMargin )
        myC4.SetTopMargin( topMargin )
        myC4.SetBottomMargin( bottomMargin )
        myC4.SetFrameBorderMode(0)
        myC4.SetFrameBorderMode(0)

	hist_MET_residualPt_raw.Draw("E")
	hist_MET_residualPt_corr.Draw("Esame")
	leg_MET_residualPt.Draw()
	
	myC4.SaveAs(outputDir+"/METCorrPlots/MET_residualPt_raw_vs_corr_"+label+".pdf")
	myC4.SaveAs(outputDir+"/METCorrPlots/MET_residualPt_raw_vs_corr_"+label+".png")
	myC4.SaveAs(outputDir+"/METCorrPlots/MET_residualPt_raw_vs_corr_"+label+".C")
	
	#MET residualPhi of raw vs corr
	hist_MET_residualPhi_raw = TH1F("hist_MET_residualPhi_raw","; #phi_{MET}^{GEN} - #phi_{MET}^{RECO}; Events", 40, -3.0,3.0)
	hist_MET_residualPhi_corr = TH1F("hist_MET_residualPhi_corr","; #phi_{MET}^{GEN} - #phi_{MET}^{RECO}; Events", 40, -3.0, 3.0)
	tree.Draw("genMetPhi - t1METPhi_raw>>hist_MET_residualPhi_raw", cut_this)
	tree.Draw("genMetPhi - t1METPhi>>hist_MET_residualPhi_corr", cut_this)
	properScale(hist_MET_residualPhi_raw, 1.0/hist_MET_residualPhi_raw.Integral())
	properScale(hist_MET_residualPhi_corr, 1.0/hist_MET_residualPhi_corr.Integral())
	hist_MET_residualPhi_raw.SetLineWidth(3)
	hist_MET_residualPhi_corr.SetLineWidth(3)
	hist_MET_residualPhi_raw.SetLineColor( kRed )
	hist_MET_residualPhi_corr.SetLineColor( kBlue )
	hist_MET_residualPhi_raw.GetXaxis().SetTitleSize( axisTitleSize )
	hist_MET_residualPhi_raw.GetXaxis().SetTitleOffset( axisTitleOffset )
	hist_MET_residualPhi_raw.GetYaxis().SetTitleSize( axisTitleSize )
	hist_MET_residualPhi_raw.GetYaxis().SetTitleOffset( axisTitleOffset )
	hist_MET_residualPhi_raw.GetYaxis().SetRangeUser(0.0, 1.5*max(hist_MET_residualPhi_raw.GetMaximum(), hist_MET_residualPhi_corr.GetMaximum()))
	
	mean_MET_residualPhi_raw = hist_MET_residualPhi_raw.GetMean()
	stddev_MET_residualPhi_raw = hist_MET_residualPhi_raw.GetStdDev()
	mean_MET_residualPhi_corr = hist_MET_residualPhi_corr.GetMean()
	stddev_MET_residualPhi_corr = hist_MET_residualPhi_corr.GetStdDev()

	leg_MET_residualPhi = TLegend(0.2, 0.75, 0.93, 0.89)
        leg_MET_residualPhi.SetBorderSize(0)
        leg_MET_residualPhi.SetTextSize(0.03)
        leg_MET_residualPhi.SetLineColor(1)
        leg_MET_residualPhi.SetLineStyle(1)
        leg_MET_residualPhi.SetLineWidth(1)
        leg_MET_residualPhi.SetFillColor(0)
        leg_MET_residualPhi.SetFillStyle(1001)
        leg_MET_residualPhi.AddEntry(hist_MET_residualPhi_raw, "uncorrected (mean = "+"%.3f" % mean_MET_residualPhi_raw+", StdDev = "+"%.2f" % stddev_MET_residualPhi_raw+")","lep")
        leg_MET_residualPhi.AddEntry(hist_MET_residualPhi_corr, "corrected (mean = "+"%.3f" % mean_MET_residualPhi_corr+", StdDev = "+"%.2f" % stddev_MET_residualPhi_corr+")","lep")
	
	myC4 = TCanvas( "myC4", "myC4", 200, 10, 800, 800 )
        myC4.SetHighLightColor(2)
        myC4.SetFillColor(0)
        myC4.SetBorderMode(0)
        myC4.SetBorderSize(2)
        myC4.SetLeftMargin( leftMargin )
        myC4.SetRightMargin( rightMargin )
        myC4.SetTopMargin( topMargin )
        myC4.SetBottomMargin( bottomMargin )
        myC4.SetFrameBorderMode(0)
        myC4.SetFrameBorderMode(0)

	hist_MET_residualPhi_raw.Draw("E")
	hist_MET_residualPhi_corr.Draw("Esame")
	leg_MET_residualPhi.Draw()
	
	myC4.SaveAs(outputDir+"/METCorrPlots/MET_residualPhi_raw_vs_corr_"+label+".pdf")
	myC4.SaveAs(outputDir+"/METCorrPlots/MET_residualPhi_raw_vs_corr_"+label+".png")
	myC4.SaveAs(outputDir+"/METCorrPlots/MET_residualPhi_raw_vs_corr_"+label+".C")



#make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm", cut)
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_noCut_nOOTgt0", "nPhotons_overlap > 0")
#make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_nOOTgt0", cut+"&& nPhotons_overlap > 0")

#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "data_SR", cut)
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "data_CR_EWK", cut_EWKCR)
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "data_CR_GJets", cut_GJets)
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root", "data_CR_QCD", cut_loose + " && !( " + cut +")")

#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/withcut/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", "Sig_L400CTau0_1cm_noCorrnoCut", "n_Photons == 2")
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/withcut/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", "Sig_L400CTau0_1cm_noCorrWithCut", cut)
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_noCorrnoCut", "n_Photons == 2")
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_noCorrWithCut", cut)
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/withcut/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "Sig_L400CTauAll_noCorrnoCut", "n_Photons ==2")
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/v1_before18Jan2019/withcut/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "Sig_L400CTauAll_noCorrWithCut",cut)
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", "Sig_L400CTau0_1cm_noCut", "n_Photons == 2")
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_noCut", "n_Photons == 2")
#make_overlapPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "Sig_L400CTauAll_noCut", "n_Photons ==2")

'''
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", "Sig_L400CTau0_1cm_noCut", "")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", "Sig_L400CTau0_1cm_1PCut", cut)
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", "Sig_L400CTau0_1cm_2PCut", cut+"&& pho2passIsoLoose_PFClusterIso && pho2passEleVeto")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_noCut", "")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_1PCut", cut)
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_2PCut", cut+"&& pho2passIsoLoose_PFClusterIso && pho2passEleVeto")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_noCut_nOOTeq0", "nPhotons_overlap == 0")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_noCut_nOOTgt0", "nPhotons_overlap > 0")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "Sig_L400CTauAll_noCut_nOOTgt0", "nPhotons_overlap > 0")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_CtauAll_13TeV-pythia8.root", "Sig_L400CTauAll_noCut_nOOTeq0", "nPhotons_overlap == 0")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root", "Sig_L400CTau200cm_nOOTgt0", cut+"&& nPhotons_overlap > 0")
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root", "Sig_L400CTau0_1cm", cut)
make_METCorrPlots("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau0_001cm_13TeV-pythia8.root", "Sig_L400CTau0_001cm", cut)
'''
