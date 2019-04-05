from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors, TMultiGraph
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import weight_cut
from config_noBDT import outputDir


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


pho1passSigmaIetaIetaTight = "pho1SigmaIetaIeta < (0.015 - 4.0e-5*pho1ClusterTime_SmearToData + 4.2e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 1.3e-4*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 4.0e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 3.1e-6*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +5.2e-5*pho1Eta + 2.5e-4*pho1Eta*pho1Eta -3.3e-5*pho1Eta*pho1Eta*pho1Eta -2.7e-4*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"
pho1passSigmaIetaIetaLoose = "pho1SigmaIetaIeta < (0.020 - 4.0e-5*pho1ClusterTime_SmearToData + 4.2e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 1.3e-4*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 4.0e-5*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 3.1e-6*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +5.2e-5*pho1Eta + 2.5e-4*pho1Eta*pho1Eta -3.3e-5*pho1Eta*pho1Eta*pho1Eta -2.7e-4*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"

pho1passSmajorTight = "pho1Smajor < (0.8 + 0.3755*exp(-0.01203*pho1Pt)-0.01468*pho1ClusterTime_SmearToData + 0.042*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 0.033*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 0.015*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 0.0015*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +0.0064*pho1Eta - 0.039*pho1Eta*pho1Eta - 0.0087*pho1Eta*pho1Eta*pho1Eta + 0.071*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"
pho1passSmajorLoose = "pho1Smajor < (1.3 + 0.3755*exp(-0.01203*pho1Pt)-0.01468*pho1ClusterTime_SmearToData + 0.042*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 0.033*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData - 0.015*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData + 0.0015*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData*pho1ClusterTime_SmearToData +0.0064*pho1Eta - 0.039*pho1Eta*pho1Eta - 0.0087*pho1Eta*pho1Eta*pho1Eta + 0.071*pho1Eta*pho1Eta*pho1Eta*pho1Eta)"

cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"

cut_lepVeto = " & nTightMuons == 0"

cut_tight_3J_2G_looseG2 = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && (HLTDecision[81] == 1) && n_Photons == 2  && pho2passIsoLoose_comboIso && pho2passEleVeto' + cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_tight_3J_2G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && (HLTDecision[81] == 1) && n_Photons == 2 '+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_loose_3J_2G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoLoose_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && (HLTDecision[81] == 1) && n_Photons == 2  '+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_tight_3J_1G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && (HLTDecision[81] == 1)'+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_loose_3J_1G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoLoose_comboIso && pho1passEleVeto && n_Jets > 2  && pho1Sminor<0.4 && (HLTDecision[81] == 1)'+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_tight_2J_2G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 1  && pho1Sminor<0.4 && (HLTDecision[81] == 1) && n_Photons == 2  '+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_tight_e2J_2G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets == 2  && pho1Sminor<0.4 && (HLTDecision[81] == 1) && n_Photons == 2  '+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_loose_2J_2G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoLoose_comboIso && pho1passEleVeto && n_Jets > 1  && pho1Sminor<0.4 && (HLTDecision[81] == 1) && n_Photons == 2  '+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_tight_2J_1G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && n_Jets > 1  && pho1Sminor<0.4 && (HLTDecision[81] == 1)'+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

cut_loose_2J_1G = 'pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoLoose_comboIso && pho1passEleVeto && n_Jets > 1  && pho1Sminor<0.4 && (HLTDecision[81] == 1)'+ cut_MET_filter + '&& '+pho1passSigmaIetaIetaTight+" && "+ pho1passSmajorTight + cut_lepVeto

inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"

tableFileName = "./effTable.txt"

def print_eff_table(cut, label="test"):
	list_ctau = ["0_001", "0_1","10","200","400","600","800","1000","1200","10000"]
	list_Lambda  = ["100","150","200","250","300","350","400"]
	list_Lambda_value  = [100.0,150.0,200.0,250.0,300.0, 350.0,400.0]
	list_Lambda_value_err  = [25.0,25.0,25.0, 25.0, 25.0, 25.0, 25.0]
	
	
	weightedcut =  weight_cut + "("+cut+")"
	#weightedcut =  weight_cut + cut

	print weightedcut

	f1=open(tableFileName, 'a') 
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
        myC.SetLogy(1)


	gr_eff_vs_lambda = []
	legend_gr = []
	mg_eff_vs_lambda = TMultiGraph()
	idx_ctau = 0
	for this_ctau in list_ctau:
		ctau_value = this_ctau
		if this_ctau == "0_1":
			ctau_value = "0.1"
		if this_ctau == "0_001":
			ctau_value = "0.001"
		
		#print >> f1, "$c\\tau ="+ctau_value+" \\mathrm{cm} $ ",
		print >> f1, ctau_value,
		
		list_eff = []
		list_eff_err = []

		for this_lambda in list_Lambda:
			fileName = inputDir+"GMSB_L"+this_lambda+"TeV_Ctau"+this_ctau+"cm_13TeV-pythia8.root"
			fileThis = TFile(fileName, "READ")			
			if fileThis.IsOpen():
				hNEventsThis = fileThis.Get("NEvents")
				N_total = hNEventsThis.GetBinContent(1)
	
				treeThis = fileThis.Get("DelayedPhoton")
				histThis = TH1F("histThis","",100,0,100)
			
				treeThis.Draw("NPU>>histThis",weightedcut)

				N_pass = histThis.Integral()
				#print >> f1, "& "+str(N_total)+" -> "+str(N_pass),
				#print >> f1, N_pass,
	
				effThis = 0.0
				if N_total > 0:
					effThis = 100.0*N_pass/N_total
				effThis_err = 0.0
				if N_pass > 0  and N_total > 0:
					effThis_err = effThis*np.sqrt(1.0/N_pass+1.0/N_total)
				
				list_eff.append(effThis/100.0)
				list_eff_err.append(effThis_err/100.0)

				if float(ctau_value) > 10.0:
					effThis_err = 0.01*np.ceil(100.0*effThis_err)
					print >> f1, "&"+"$ %.2f" % effThis + " \pm %.2f " % effThis_err + "$",
				else:
					effThis_err = 0.1*np.ceil(10.0*effThis_err)
					print >> f1, "&"+"$ %.1f" % effThis + " \pm %.1f " % effThis_err + "$",
				
			else:
				print >> f1, "& -- ",
		if len(list_eff) == len(list_Lambda_value):
			gr_this = TGraphErrors(len(list_eff), np.array(list_Lambda_value), np.array(list_eff), np.array(list_Lambda_value_err), np.array(list_eff_err))
			gr_this.SetMarkerColor(colors[idx_ctau]-4)
			gr_this.SetLineColor(colors[idx_ctau]-4)
			gr_this.SetLineWidth(2)	
			mg_eff_vs_lambda.Add(gr_this)
			gr_eff_vs_lambda.append(gr_this)
			legend_gr.append(ctau_value)

		idx_ctau = idx_ctau + 1	

		print >> f1, "\\\\"
		#f1.close()
	mg_eff_vs_lambda.Draw("AP")
	mg_eff_vs_lambda.GetYaxis().SetRangeUser(0.001, 1.0)
	mg_eff_vs_lambda.GetYaxis().SetTitle("efficiency")
	mg_eff_vs_lambda.GetXaxis().SetTitle("#Lambda (TeV)")
	leg = TLegend(0.18, 0.75, 0.93, 0.92)
        leg.SetNColumns(2)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.035)
        leg.SetLineColor(1)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)

	for idx in range(len(gr_eff_vs_lambda)):
		leg.AddEntry(gr_eff_vs_lambda[idx], "c#tau="+legend_gr[idx]+"cm", "lep")
	leg.Draw()
	myC.SaveAs(outputDir+"/stack/sigEff_vs_lambda_"+label+".pdf")
	myC.SaveAs(outputDir+"/stack/sigEff_vs_lambda_"+label+".png")
	myC.SaveAs(outputDir+"/stack/sigEff_vs_lambda_"+label+".C")
	

f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_3J_2G"
print >> f2, "------------------------------------------------"
print_eff_table(cut_tight_3J_2G, "3J2G")

'''
f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_3J_2G_looseG2"
print >> f2, "------------------------------------------------"
print_eff_table(cut_tight_3J_2G_looseG2)


f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_3J_1G"
print >> f2, "------------------------------------------------"
print_eff_table(cut_tight_3J_1G)


f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_2J_2G"
print >> f2, "------------------------------------------------"
print_eff_table(cut_tight_2J_2G)


f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_2J_1G"
print >> f2, "------------------------------------------------"
print_eff_table(cut_tight_2J_1G)

f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_e2J_2G"
print >> f2, "------------------------------------------------"
print_eff_table(cut_tight_e2J_2G)
'''
