from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors, TEfficiency, gPad, TH2F, TF1
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import outputDir

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

inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/"

def drawIDeff_ptetatime_OOTGED(cut_deno, cut_nume, filename, label):
	fileThis = TFile(inputDir+filename, "READ")
	treeThis = fileThis.Get("DelayedPhoton")
	
	pt_binning = np.array([25.0, 35.0, 45.0, 60.0, 80.0, 100.0, 125.0, 150.0, 180.0, 210.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 700.0, 800.0, 1000.0])
	eta_binning = np.array([-1.5, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.5, 0.8, 1.0, 1.2, 1.5])
	time_binning = np.array([-2.0, -1.0, -0.5, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.1, 2.4, 2.8, 3.2, 4.0, 5.0, 6.0, 7.0])
	
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
	
	##efficiency vs pt:
	hist_OOT_deno_vs_pt = TH1F("hist_OOT_deno_vs_pt", "; p_{T}^{#gamma} (GeV); eff", len(pt_binning)-1, pt_binning)
	hist_GED_deno_vs_pt = TH1F("hist_GED_deno_vs_pt", "; p_{T}^{#gamma} (GeV); eff", len(pt_binning)-1, pt_binning)
	hist_OOT_nume_vs_pt = TH1F("hist_OOT_nume_vs_pt", "; p_{T}^{#gamma} (GeV); eff", len(pt_binning)-1, pt_binning)
	hist_GED_nume_vs_pt = TH1F("hist_GED_nume_vs_pt", "; p_{T}^{#gamma} (GeV); eff", len(pt_binning)-1, pt_binning)
	treeThis.Draw("pho1Pt>>hist_OOT_deno_vs_pt", cut_deno+" && !pho1isStandardPhoton")
	treeThis.Draw("pho1Pt>>hist_GED_deno_vs_pt", cut_deno+" && pho1isStandardPhoton")
	treeThis.Draw("pho1Pt>>hist_OOT_nume_vs_pt", cut_nume+" && !pho1isStandardPhoton")
	treeThis.Draw("pho1Pt>>hist_GED_nume_vs_pt", cut_nume+" && pho1isStandardPhoton")
	eff_OOT_vs_pt = TEfficiency(hist_OOT_nume_vs_pt, hist_OOT_deno_vs_pt)
	eff_GED_vs_pt = TEfficiency(hist_GED_nume_vs_pt, hist_GED_deno_vs_pt)
	eff_OOT_vs_pt.SetMarkerStyle(20)
	eff_GED_vs_pt.SetMarkerStyle(22)
	eff_OOT_vs_pt.SetLineWidth(2)
	eff_GED_vs_pt.SetLineWidth(2)
	eff_OOT_vs_pt.SetLineColor(2)
	eff_OOT_vs_pt.SetMarkerColor(2)
	eff_GED_vs_pt.SetLineColor(1)
	eff_GED_vs_pt.SetMarkerColor(1)
	eff_OOT_vs_pt.Draw("AP")
        gPad.Update()	
	graph_vs_pt = eff_OOT_vs_pt.GetPaintedGraph()
        graph_vs_pt.SetMinimum(0.0)
        graph_vs_pt.SetMaximum(1.0)
        gPad.Update()	
	eff_GED_vs_pt.Draw("same")
	leg_vs_pt = TLegend(0.65, 0.75, 0.93, 0.92)
        leg_vs_pt.SetBorderSize(0)
        leg_vs_pt.SetTextSize(0.035)
        leg_vs_pt.SetLineColor(1)
        leg_vs_pt.SetLineStyle(1)
        leg_vs_pt.SetLineWidth(1)
        leg_vs_pt.SetFillColor(0)
        leg_vs_pt.SetFillStyle(1001)
	leg_vs_pt.AddEntry(eff_GED_vs_pt, "GED photon", "lep")
	leg_vs_pt.AddEntry(eff_OOT_vs_pt, "OOT photon", "lep")
	leg_vs_pt.Draw()
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_pt_OOTGED.pdf")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_pt_OOTGED.png")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_pt_OOTGED.C")

	##efficiency vs eta:
	hist_OOT_deno_vs_eta = TH1F("hist_OOT_deno_vs_eta", "; #eta; eff", len(eta_binning)-1, eta_binning)
	hist_GED_deno_vs_eta = TH1F("hist_GED_deno_vs_eta", "; #eta; eff", len(eta_binning)-1, eta_binning)
	hist_OOT_nume_vs_eta = TH1F("hist_OOT_nume_vs_eta", "; #eta; eff", len(eta_binning)-1, eta_binning)
	hist_GED_nume_vs_eta = TH1F("hist_GED_nume_vs_eta", "; #eta; eff", len(eta_binning)-1, eta_binning)
	treeThis.Draw("pho1Eta>>hist_OOT_deno_vs_eta", cut_deno+" && !pho1isStandardPhoton")
	treeThis.Draw("pho1Eta>>hist_GED_deno_vs_eta", cut_deno+" && pho1isStandardPhoton")
	treeThis.Draw("pho1Eta>>hist_OOT_nume_vs_eta", cut_nume+" && !pho1isStandardPhoton")
	treeThis.Draw("pho1Eta>>hist_GED_nume_vs_eta", cut_nume+" && pho1isStandardPhoton")
	eff_OOT_vs_eta = TEfficiency(hist_OOT_nume_vs_eta, hist_OOT_deno_vs_eta)
	eff_GED_vs_eta = TEfficiency(hist_GED_nume_vs_eta, hist_GED_deno_vs_eta)
	eff_OOT_vs_eta.SetMarkerStyle(20)
	eff_GED_vs_eta.SetMarkerStyle(22)
	eff_OOT_vs_eta.SetLineWidth(2)
	eff_GED_vs_eta.SetLineWidth(2)
	eff_OOT_vs_eta.SetLineColor(2)
	eff_OOT_vs_eta.SetMarkerColor(2)
	eff_GED_vs_eta.SetLineColor(1)
	eff_GED_vs_eta.SetMarkerColor(1)
	eff_OOT_vs_eta.Draw("AP")
        gPad.Update()	
	graph_vs_eta = eff_OOT_vs_eta.GetPaintedGraph()
        graph_vs_eta.SetMinimum(0.0)
        graph_vs_eta.SetMaximum(1.0)
        gPad.Update()	
	eff_GED_vs_eta.Draw("same")
	leg_vs_eta = TLegend(0.65, 0.75, 0.93, 0.92)
        leg_vs_eta.SetBorderSize(0)
        leg_vs_eta.SetTextSize(0.035)
        leg_vs_eta.SetLineColor(1)
        leg_vs_eta.SetLineStyle(1)
        leg_vs_eta.SetLineWidth(1)
        leg_vs_eta.SetFillColor(0)
        leg_vs_eta.SetFillStyle(1001)
	leg_vs_eta.AddEntry(eff_GED_vs_eta, "GED photon", "lep")
	leg_vs_eta.AddEntry(eff_OOT_vs_eta, "OOT photon", "lep")
	leg_vs_eta.Draw()
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_eta_OOTGED.pdf")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_eta_OOTGED.png")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_eta_OOTGED.C")


	##efficiency vs time:
	hist_OOT_deno_vs_time = TH1F("hist_OOT_deno_vs_time", "; #gamma time (ns); eff", len(time_binning)-1, time_binning)
	hist_GED_deno_vs_time = TH1F("hist_GED_deno_vs_time", "; #gamma time (ns); eff", len(time_binning)-1, time_binning)
	hist_OOT_nume_vs_time = TH1F("hist_OOT_nume_vs_time", "; #gamma time (ns); eff", len(time_binning)-1, time_binning)
	hist_GED_nume_vs_time = TH1F("hist_GED_nume_vs_time", "; #gamma time (ns); eff", len(time_binning)-1, time_binning)
	treeThis.Draw("pho1ClusterTime_SmearToData>>hist_OOT_deno_vs_time", cut_deno+" && !pho1isStandardPhoton")
	treeThis.Draw("pho1ClusterTime_SmearToData>>hist_GED_deno_vs_time", cut_deno+" && pho1isStandardPhoton")
	treeThis.Draw("pho1ClusterTime_SmearToData>>hist_OOT_nume_vs_time", cut_nume+" && !pho1isStandardPhoton")
	treeThis.Draw("pho1ClusterTime_SmearToData>>hist_GED_nume_vs_time", cut_nume+" && pho1isStandardPhoton")
	eff_OOT_vs_time = TEfficiency(hist_OOT_nume_vs_time, hist_OOT_deno_vs_time)
	eff_GED_vs_time = TEfficiency(hist_GED_nume_vs_time, hist_GED_deno_vs_time)
	eff_OOT_vs_time.SetMarkerStyle(20)
	eff_GED_vs_time.SetMarkerStyle(22)
	eff_OOT_vs_time.SetLineWidth(2)
	eff_GED_vs_time.SetLineWidth(2)
	eff_OOT_vs_time.SetLineColor(2)
	eff_OOT_vs_time.SetMarkerColor(2)
	eff_GED_vs_time.SetLineColor(1)
	eff_GED_vs_time.SetMarkerColor(1)
	eff_OOT_vs_time.Draw("AP")
        gPad.Update()	
	graph_vs_time = eff_OOT_vs_time.GetPaintedGraph()
        graph_vs_time.SetMinimum(0.0)
        graph_vs_time.SetMaximum(1.0)
        gPad.Update()	
	eff_GED_vs_time.Draw("same")
	leg_vs_time = TLegend(0.65, 0.75, 0.93, 0.92)
        leg_vs_time.SetBorderSize(0)
        leg_vs_time.SetTextSize(0.035)
        leg_vs_time.SetLineColor(1)
        leg_vs_time.SetLineStyle(1)
        leg_vs_time.SetLineWidth(1)
        leg_vs_time.SetFillColor(0)
        leg_vs_time.SetFillStyle(1001)
	leg_vs_time.AddEntry(eff_GED_vs_time, "GED photon", "lep")
	leg_vs_time.AddEntry(eff_OOT_vs_time, "OOT photon", "lep")
	leg_vs_time.Draw()
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_time_OOTGED.pdf")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_time_OOTGED.png")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_time_OOTGED.C")



def drawIDeff_ptetatime_Nm1(cut_deno, cuts_nume, filename, label, label_cuts, varBName, varBTitle, varBBinning):
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
	myC.SetGridy(1)

	colors = [632, 416, 600, 880, 54, 13, 18, 80, 57, 60, 64, 67, 8, 80, 91, 93, 97,  2, 18, 16, 13]


	effs_vs_varB = []
	for idx in range(len(cuts_nume)):
		hist_deno_vs_varB = TH1F("hist_deno_vs_varB_cut"+str(idx), "; "+varBTitle+"; eff", len(varBBinning)-1, varBBinning)
		treeThis.Draw(varBName+">>hist_deno_vs_varB_cut"+str(idx), cut_deno)
		hist_nume_vs_varB = TH1F("hist_nume_vs_varB_cut"+str(idx), "; "+varBTitle+"; eff", len(varBBinning)-1, varBBinning)
		treeThis.Draw(varBName+">>hist_nume_vs_varB_cut"+str(idx), cuts_nume[idx])
		eff_vs_varB = TEfficiency(hist_nume_vs_varB, hist_deno_vs_varB)
		eff_vs_varB.SetMarkerStyle(20+idx)
		eff_vs_varB.SetMarkerColor(colors[idx]-4)
		eff_vs_varB.SetLineColor(colors[idx]-4)
		eff_vs_varB.SetLineWidth(2)
		eff_vs_varB.Draw("AP")
		effs_vs_varB.append(eff_vs_varB)
		gPad.Update()	

	#effs_vs_varB[0].Draw("AP")
	graph = effs_vs_varB[0].GetPaintedGraph()
	graph.SetMinimum(0.0)
	graph.SetMaximum(1.0)
	gPad.Update()	
	leg = TLegend(0.3, 0.2, 0.93, 0.4)
        leg.SetNColumns(1)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.035)
        leg.SetLineColor(1)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)
	
	for idx in range(len(cuts_nume)):
		if idx == 0:
			effs_vs_varB[idx].Draw("AP")
		else:
			effs_vs_varB[idx].Draw("same")
		leg.AddEntry(effs_vs_varB[idx], label_cuts[idx], "lep")

	leg.Draw()
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_"+varBName+".pdf")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_"+varBName+".png")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_"+varBName+".C")


def drawIDeff_ptetatime(cut_deno, cut_nume, filename, label):
	fileThis = TFile(inputDir+filename, "READ")
	treeThis = fileThis.Get("DelayedPhoton")
	
	pt_binning = np.array([25.0, 35.0, 45.0, 60.0, 80.0, 100.0, 125.0, 150.0, 180.0, 210.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 700.0, 800.0, 1000.0])
	eta_binning = np.array([-1.5, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.5, 0.8, 1.0, 1.2, 1.5])
	time_binning = np.array([-2.0, -1.0, -0.5, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.1, 2.4, 2.8, 3.2, 4.0, 5.0, 6.0, 7.0])
	
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
	myC.SetGridy(1)
	
	##efficiency vs pt:
	hist_deno_vs_pt = TH1F("hist_deno_vs_pt", "; p_{T}^{#gamma} (GeV); eff", len(pt_binning)-1, pt_binning)
	hist_nume_vs_pt = TH1F("hist_nume_vs_pt", "; p_{T}^{#gamma} (GeV); eff", len(pt_binning)-1, pt_binning)
	treeThis.Draw("pho1Pt>>hist_deno_vs_pt", cut_deno)
	treeThis.Draw("pho1Pt>>hist_nume_vs_pt", cut_nume)
	eff_vs_pt = TEfficiency(hist_nume_vs_pt, hist_deno_vs_pt)
	eff_vs_pt.SetMarkerStyle(20)
	eff_vs_pt.SetLineWidth(2)
	eff_vs_pt.Draw("AP")
        gPad.Update()	
	graph_vs_pt = eff_vs_pt.GetPaintedGraph()
        graph_vs_pt.SetMinimum(0.0)
        graph_vs_pt.SetMaximum(1.0)
        gPad.Update()	
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_pt.pdf")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_pt.png")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_pt.C")

	##efficiency vs eta:
	hist_deno_vs_eta = TH1F("hist_deno_vs_eta", "; #eta; eff", len(eta_binning)-1, eta_binning)
	hist_nume_vs_eta = TH1F("hist_nume_vs_eta", "; #eta; eff", len(eta_binning)-1, eta_binning)
	treeThis.Draw("pho1Eta>>hist_deno_vs_eta", cut_deno)
	treeThis.Draw("pho1Eta>>hist_nume_vs_eta", cut_nume)
	eff_vs_eta = TEfficiency(hist_nume_vs_eta, hist_deno_vs_eta)
	eff_vs_eta.SetMarkerStyle(20)
	eff_vs_eta.SetLineWidth(2)
	eff_vs_eta.Draw("AP")
        gPad.Update()	
	graph_vs_eta = eff_vs_eta.GetPaintedGraph()
        graph_vs_eta.SetMinimum(0.0)
        graph_vs_eta.SetMaximum(1.0)
        gPad.Update()	
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_eta.pdf")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_eta.png")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_eta.C")


	##efficiency vs time:
	hist_deno_vs_time = TH1F("hist_deno_vs_time", "; #gamma time (ns); eff", len(time_binning)-1, time_binning)
	hist_nume_vs_time = TH1F("hist_nume_vs_time", "; #gamma time (ns); eff", len(time_binning)-1, time_binning)
	treeThis.Draw("pho1ClusterTime_SmearToData>>hist_deno_vs_time", cut_deno)
	treeThis.Draw("pho1ClusterTime_SmearToData>>hist_nume_vs_time", cut_nume)
	eff_vs_time = TEfficiency(hist_nume_vs_time, hist_deno_vs_time)
	eff_vs_time.SetMarkerStyle(20)
	eff_vs_time.SetLineWidth(2)
	eff_vs_time.Draw("AP")
        gPad.Update()	
	graph_vs_time = eff_vs_time.GetPaintedGraph()
        graph_vs_time.SetMinimum(0.0)
        graph_vs_time.SetMaximum(1.0)
        gPad.Update()	
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_time.pdf")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_time.png")
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_vs_time.C")


def drawIDeff(cut_deno, cut_nume, filename, label):
	fileThis = TFile(inputDir+filename, "READ")
	treeThis = fileThis.Get("DelayedPhoton")
	
	pt_binning = np.array([25.0, 35.0, 45.0, 60.0, 80.0, 150.0, 200.0, 300.0, 500.0, 800.0])
	eta_binning = np.array([0.0, 0.2, 0.5, 0.8, 1.0, 1.2, 1.5])
	
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

	colors = [632, 800, 400, 416, 600, 880, 54, 13, 18, 80, 57, 60, 64, 67, 8, 80, 91, 93, 97,  2, 18, 16, 13]	
	
	efficiencies = []
	
	for idx_eta in range(len(eta_binning)-1):
		hist_deno = TH1F("hist_deno_ieta"+str(idx_eta), "; p_{T}^{#gamma} (GeV); eff", len(pt_binning)-1, pt_binning)
		hist_nume = TH1F("hist_nume_ieta"+str(idx_eta), "; p_{T}^{#gamma} (GeV); eff", len(pt_binning)-1, pt_binning)
		
		cut_eta = " && pho1Eta > "+str(eta_binning[idx_eta])+" && pho1Eta < "+str(eta_binning[idx_eta+1])

		treeThis.Draw("pho1Pt>>hist_deno_ieta"+str(idx_eta), cut_deno+cut_eta)
		treeThis.Draw("pho1Pt>>hist_nume_ieta"+str(idx_eta), cut_nume+cut_eta)
		
		print "numerator cut: "+cut_nume+cut_eta	
		print "numerator: Int = "+str(hist_nume.Integral())
		print "denominator cut: "+cut_deno+cut_eta	
		print "denominator: Int = "+str(hist_deno.Integral())

		eff_this = TEfficiency(hist_nume, hist_deno)

		eff_this.SetMarkerStyle(20)
		eff_this.SetLineWidth(2)
		eff_this.SetLineColor(colors[idx_eta]-4)
		eff_this.SetMarkerColor(colors[idx_eta]-4)
		
		eff_this.Draw("AP")
		efficiencies.append(eff_this)

		myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_Eta"+str(idx_eta)+".pdf")
		myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_Eta"+str(idx_eta)+".png")
		myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_Eta"+str(idx_eta)+".C")
	
	leg = TLegend(0.18, 0.75, 0.93, 0.92)
        leg.SetNColumns(2)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.035)
        leg.SetLineColor(1)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)
	graph = efficiencies[0].GetPaintedGraph()
        graph.SetMinimum(0.4)
	graph.SetMaximum(1.1) 
	gPad.Update()	
	for idx_eta in range(len(eta_binning)-1):
		if idx_eta == 0:
			efficiencies[idx_eta].Draw("AP")
		else:
			efficiencies[idx_eta].Draw("same")
		leg.AddEntry(efficiencies[idx_eta], str(eta_binning[idx_eta])+" < |#eta| < "+str(eta_binning[idx_eta+1]), "lep")
	leg.Draw()

	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_EtaAll.pdf")	
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_EtaAll.png")	
	myC.SaveAs(outputDir+"/stack/photonID_eff_"+label+"_EtaAll.C")	


def draw_varA_vs_varB(filename, label, cut, cut_invert_match, varAName, varBName, varATitle, varBTitle, varALow, varAHigh, varBBinning, quantile, fitOption):
	print "Making plots of "+varAName+" vs. "+varBName
	fileThis = TFile(inputDir+filename, "READ")
        treeThis = fileThis.Get("DelayedPhoton")
	varABinning = np.arange(varALow, varAHigh, (varAHigh-varALow)/400.0)
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
	h2 = TH2F("h2","; "+varBTitle+"; "+varATitle+"; Events", len(varBBinning)-1, varBBinning, len(varABinning)-1, varABinning)
	treeThis.Draw(varAName+":"+varBName+">>h2", cut, "")
	h2.SetMarkerStyle(7)
	myC.SaveAs(outputDir+"/stack/photon_"+varAName+"_vs_"+varBName+"_"+label+"_2D.pdf")
	myC.SaveAs(outputDir+"/stack/photon_"+varAName+"_vs_"+varBName+"_"+label+"_2D.png")
	myC.SaveAs(outputDir+"/stack/photon_"+varAName+"_vs_"+varBName+"_"+label+"_2D.C")
	pf = h2.QuantilesX(quantile)
	maxErrorOverValue = 0.0
	
	for idx in range(1, pf.GetNbinsX() +1):
		if pf.GetBinContent(idx) > 0.0:
			if pf.GetBinError(idx)/pf.GetBinContent(idx) > maxErrorOverValue:
				maxErrorOverValue = pf.GetBinError(idx)/pf.GetBinContent(idx)
	
	if maxErrorOverValue > 0.1:
		for idx in range(1, pf.GetNbinsX() +1):
			pf.SetBinError(idx, pf.GetBinError(idx)*0.1/maxErrorOverValue)

	pf.Draw()
	pf.GetXaxis().SetTitle(varBTitle)
	pf.GetYaxis().SetTitle(varATitle)
	pf.SetMarkerStyle(20)
	pf.SetLineWidth(3)
	pf.GetYaxis().SetRangeUser(0.8*pf.GetMinimum(), 1.5*pf.GetMaximum())
	pf.GetYaxis().SetNdivisions( 5, False )
	pf.GetYaxis().SetLabelSize(0.025)
	##perform the fit
	fitRangeL = 3
	fitRangeR = 3
	if varBName == "pho1Eta":
		fitRangeL = 1
		fitRangeR = 1
	if varBName == "pho1ClusterTime_SmearToData":
		fitRangeL = 1
		fitRangeR = 1
	if varBName == "pho1Pt" and varAName == "pho1Smajor":
		fitRangeL = 0
		fitRangeR = 7
	tf1_fit = None
	if fitOption == 1:
		tf1_fit = TF1("tf1_fit","[0]+[1]*x", varBBinning[fitRangeL],varBBinning[-1-fitRangeR])
		tf1_fit.SetParameters(varALow, (varAHigh-varALow)/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]))
	if fitOption == 2:
		tf1_fit = TF1("tf1_fit","[0]+[1]*x+[2]*x*x", varBBinning[fitRangeL],varBBinning[-1-fitRangeR])
		tf1_fit.SetParameters(varALow, (varAHigh-varALow)/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]))
	if fitOption == 3:
		tf1_fit = TF1("tf1_fit","[0]+[1]*x+[2]*x*x+[3]*x*x*x", varBBinning[fitRangeL],varBBinning[-1-fitRangeR])
		tf1_fit.SetParameters(varALow, (varAHigh-varALow)/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.0001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]))
	if fitOption == 4:
		tf1_fit = TF1("tf1_fit","[0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x", varBBinning[fitRangeL],varBBinning[-1-fitRangeR])
		tf1_fit.SetParameters(varALow, (varAHigh-varALow)/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.0001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.00001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]))
	if fitOption == 5:
		tf1_fit = TF1("tf1_fit","[0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x+[5]*x*x*x*x*x", varBBinning[fitRangeL],varBBinning[-1-fitRangeR])
		tf1_fit.SetParameters(varALow, (varAHigh-varALow)/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.0001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.00001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]), (varAHigh-varALow)*0.000001/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]))
	if fitOption == 6:
		tf1_fit = TF1("tf1_fit","[0]+[1]*exp([2]*x)", varBBinning[fitRangeL],varBBinning[-1-fitRangeR])
		tf1_fit.SetParameters(pf.GetMinimum(), pf.GetMaximum()-pf.GetMinimum(), -2.0/(varBBinning[-1-fitRangeR] - varBBinning[fitRangeL]))

	pf.Fit("tf1_fit", "", "", varBBinning[fitRangeL],varBBinning[-1-fitRangeR])
	myC.SaveAs(outputDir+"/stack/photon_"+varAName+"_vs_"+varBName+"_"+label+"_qualtile.pdf")
	myC.SaveAs(outputDir+"/stack/photon_"+varAName+"_vs_"+varBName+"_"+label+"_qualtile.png")
	myC.SaveAs(outputDir+"/stack/photon_"+varAName+"_vs_"+varBName+"_"+label+"_qualtile.C")


weights = "(weight*pileupWeight*triggerEffSFWeight*triggerEffWeight) * "
	
cut_match = "abs(deltaR_pho1)<0.3  && deltaPt_pho1/pho1GenPt < 0.3 && abs(pho1Eta)<1.4442"
cut_invert_match = "!(abs(deltaR_pho1)<0.3  && deltaPt_pho1/pho1GenPt < 0.3) && abs(pho1Eta)<1.4442"

#pho1passSigmaIetaIetaTight = "pho1SigmaIetaIeta < (0.011 - 2.4e-6*pho1ClusterTime_SmearToData + 1.0e-4*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 3.4e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 6.7e-6*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +5.2e-5*pho1Eta + 2.5e-4*pho1Eta*pho1Eta -3.3e-5*pho1Eta*pho1Eta*pho1Eta -2.7e-4*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"
pho1passSigmaIetaIetaTight = "pho1SigmaIetaIeta < (0.015 - 4.0e-5*pho1ClusterTime_SmearToData + 4.2e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 1.3e-4*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 4.0e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 3.1e-6*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +5.2e-5*pho1Eta + 2.5e-4*pho1Eta*pho1Eta -3.3e-5*pho1Eta*pho1Eta*pho1Eta -2.7e-4*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"
pho1passSigmaIetaIetaLoose = "pho1SigmaIetaIeta < (0.020 - 4.0e-5*pho1ClusterTime_SmearToData + 4.2e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 1.3e-4*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 4.0e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 3.1e-6*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +5.2e-5*pho1Eta + 2.5e-4*pho1Eta*pho1Eta -3.3e-5*pho1Eta*pho1Eta*pho1Eta -2.7e-4*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"

#pho1passSmajorTight = "pho1Smajor < (0.5 +0.0043*pho1ClusterTime_SmearToData + 0.061*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 0.0089*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 1.6e-4*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +0.0064*pho1Eta - 0.039*pho1Eta*pho1Eta - 0.0087*pho1Eta*pho1Eta*pho1Eta + 0.071*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"
pho1passSmajorTight = "pho1Smajor < (0.8 + 0.3755*exp(-0.01203*pho1Pt)-0.01468*pho1ClusterTime_SmearToData + 0.042*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 0.033*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 0.015*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 0.0015*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +0.0064*pho1Eta - 0.039*pho1Eta*pho1Eta - 0.0087*pho1Eta*pho1Eta*pho1Eta + 0.071*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"
pho1passSmajorLoose = "pho1Smajor < (1.3 + 0.3755*exp(-0.01203*pho1Pt)-0.01468*pho1ClusterTime_SmearToData + 0.042*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 0.033*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 0.015*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 0.0015*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +0.0064*pho1Eta - 0.039*pho1Eta*pho1Eta - 0.0087*pho1Eta*pho1Eta*pho1Eta + 0.071*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"

'''
photonID_cuts_OOT_Tight = ["pho1passIsoTight_PFClusterIso", "pho1passSigmaIetaIetaTight", "pho1passSmajorTight"]	
photonID_cuts_OOT_Tight_all = "pho1passIsoTight_PFClusterIso && pho1passSigmaIetaIetaTight && pho1passSmajorTight"
photonID_cuts_OOT_Loose = ["pho1passIsoLoose_PFClusterIso", "pho1passSigmaIetaIetaLoose", "pho1passSmajorLoose"]	
photonID_cuts_OOT_Loose_all = "pho1passIsoLoose_PFClusterIso && pho1passSigmaIetaIetaLoose && pho1passSmajorLoose"

'''
photonID_cuts_OOT_Tight = ["pho1passIsoTight_PFClusterIso", pho1passSigmaIetaIetaTight, pho1passSmajorTight]	
photonID_cuts_OOT_Tight_all = "pho1passIsoTight_PFClusterIso &&"+ pho1passSigmaIetaIetaTight +"&&" + pho1passSmajorTight
photonID_cuts_OOT_Loose = ["pho1passIsoLoose_PFClusterIso", pho1passSigmaIetaIetaLoose, pho1passSmajorLoose]	
photonID_cuts_OOT_Loose_all = "pho1passIsoLoose_PFClusterIso &&"+ pho1passSigmaIetaIetaLoose +"&&" + pho1passSmajorLoose
photonID_cuts_label = ["Isolation", "SigmaIetaIeta", "Smajor"]
photonID_cuts_label_Nm1 = ["Isolation", "Isolation + #sigma_{i#eta i#eta}", "Isolation + #sigma_{i#eta i#eta} + Smajor"]

cut_deno = weights + cut_match 
cut_nume_OOT_Tight = weights + cut_match + " && "+photonID_cuts_OOT_Tight_all
cut_nume_OOT_Loose = weights + cut_match + " && "+photonID_cuts_OOT_Loose_all

cuts_nume_OOT_Tight = []
cuts_nume_OOT_Loose = []
for idx in range(len(photonID_cuts_OOT_Tight)):
	cut_this_Tight = weights + cut_match
	cut_this_Loose = weights + cut_match
	for idx2 in range(idx+1):
		cut_this_Tight = cut_this_Tight + "&& " + photonID_cuts_OOT_Tight[idx2]
		cut_this_Loose = cut_this_Loose + "&& "+ photonID_cuts_OOT_Loose[idx2]
	cuts_nume_OOT_Tight.append(cut_this_Tight)
	cuts_nume_OOT_Loose.append(cut_this_Loose)
	

pt_binning = np.array([25.0, 35.0, 45.0, 65.0, 80.0, 100.0, 125.0, 150.0, 180.0, 210.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 700.0, 800.0, 1000.0])
eta_binning = np.array([-1.5, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.5, 0.8, 1.0, 1.2, 1.5])
time_binning = np.array([-2.0, -1.0, -0.5, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.1, 2.4, 2.8, 3.2, 4.0, 5.0, 6.0, 7.0])
rho_binning = np.array([0.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 35.0, 40.0, 50.0, 60.0])

print len(pt_binning)
print len(eta_binning)
print len(time_binning)
print len(rho_binning)

draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1SigmaIetaIeta", "pho1ClusterTime_SmearToData", "SigmaIetaIeta", " #gamma cluster time (ns)", 0.0, 0.02, time_binning, 0.7, 5)

drawIDeff_ptetatime(cut_deno, cut_nume_OOT_Tight, "GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "OOT_Tight_L200TeV_CtauAll_allIDcuts")
drawIDeff_ptetatime_Nm1(cut_deno, cuts_nume_OOT_Tight, "GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "OOT_Tight_L200TeV_CtauAll_Nm1Cuts", photonID_cuts_label_Nm1, "pho1Pt", "#gamma p^{T} (GeV)", pt_binning)
drawIDeff_ptetatime_Nm1(cut_deno, cuts_nume_OOT_Tight, "GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "OOT_Tight_L200TeV_CtauAll_Nm1Cuts", photonID_cuts_label_Nm1, "pho1Eta", "#gamma #eta", eta_binning)
drawIDeff_ptetatime_Nm1(cut_deno, cuts_nume_OOT_Tight, "GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "OOT_Tight_L200TeV_CtauAll_Nm1Cuts", photonID_cuts_label_Nm1, "pho1ClusterTime_SmearToData", "#gamma time (ns)", time_binning)

draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1Smajor", "pho1Pt", "Smajor", " #gamma p^{T} (GeV)", 0.0, 2.0, pt_binning, 0.7, 6)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1Smajor", "pho1ClusterTime_SmearToData", "Smajor", " #gamma cluster time (ns)", 0.0, 2.0, time_binning, 0.7, 5)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1Smajor", "pho1Eta", "Smajor", " #eta", 0.0, 2.0, eta_binning, 0.7, 4)

draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1SigmaIetaIeta", "pho1ClusterTime_SmearToData", "SigmaIetaIeta", " #gamma cluster time (ns)", 0.0, 0.02, time_binning, 0.7, 5)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1SigmaIetaIeta", "pho1Eta", "SigmaIetaIeta", " #eta", 0.0, 0.02, eta_binning, 0.7, 4)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1SigmaIetaIeta", "pho1Pt", "SigmaIetaIeta", " #gamma p^{T} (GeV)", 0.0, 0.02, pt_binning, 0.7, 1)

draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1ecalPFClusterIso", "pho1Pt", "ecalPFClusterIso", " #gamma p^{T} (GeV)", 0.0, 50.0, pt_binning, 0.7, 1)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll_etabin1", cut_match+" && abs(pho1Eta) < 0.8 ", cut_invert_match, "pho1ecalPFClusterIso", "fixedGridRhoFastjetAll", "ecalPFClusterIso", " #rho", 0.0, 50.0, rho_binning, 0.7, 1)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll_etabin2", cut_match+" && abs(pho1Eta) > 0.8 ", cut_invert_match, "pho1ecalPFClusterIso", "fixedGridRhoFastjetAll", "ecalPFClusterIso", " #rho", 0.0, 50.0, rho_binning, 0.7, 1)

draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1sumNeutralHadronEt", "pho1Pt", "sumNeutralHadronEt", " #gamma p^{T} (GeV)", 0.0, 50.0, pt_binning, 0.7, 2)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll_etabin1", cut_match+" && abs(pho1Eta) < 0.8 ", cut_invert_match, "pho1sumNeutralHadronEt", "fixedGridRhoFastjetAll", "sumNeutralHadronEt", " #rho", 0.0, 50.0, rho_binning, 0.7, 1)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll_etabin2", cut_match+" && abs(pho1Eta) > 0.8 ", cut_invert_match, "pho1sumNeutralHadronEt", "fixedGridRhoFastjetAll", "sumNeutralHadronEt", " #rho", 0.0, 50.0, rho_binning, 0.7, 1)

draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll", cut_match, cut_invert_match, "pho1trkSumPtHollowConeDR03", "pho1Pt", "trkSumPtHollowConeDR03", " #gamma p^{T} (GeV)", 0.0, 50.0, pt_binning, 0.7, 1)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll_etabin1", cut_match+" && abs(pho1Eta) < 0.8 ", cut_invert_match, "pho1trkSumPtHollowConeDR03", "fixedGridRhoFastjetAll", "trkSumPtHollowConeDR03", " #rho", 0.0, 50.0, rho_binning, 0.7, 1)
draw_varA_vs_varB("GMSB_L200TeV_CtauAll_13TeV-pythia8.root", "L200TeV_CtauAll_etabin2", cut_match+" && abs(pho1Eta) > 0.8 ", cut_invert_match, "pho1trkSumPtHollowConeDR03", "fixedGridRhoFastjetAll", "trkSumPtHollowConeDR03", " #rho", 0.0, 50.0, rho_binning, 0.7, 1)
