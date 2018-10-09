from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import weight_cut

gROOT.SetBatch(True)

cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"

cut_tight_3J_2G_looseG2 = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 && pho2passIsoLoose_PFClusterIso && pho2passEleVeto' + cut_MET_filter


cut_tight_3J_2G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2'+ cut_MET_filter

cut_loose_3J_2G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 '+ cut_MET_filter

cut_tight_3J_1G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1)'+ cut_MET_filter

cut_loose_3J_1G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1)'+ cut_MET_filter

cut_tight_2J_2G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 1 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 '+ cut_MET_filter

cut_tight_e2J_2G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets == 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 '+ cut_MET_filter

cut_loose_2J_2G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && n_Jets > 1 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 '+ cut_MET_filter

cut_tight_2J_1G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 1 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1)'+ cut_MET_filter

cut_loose_2J_1G = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && n_Jets > 1 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1)'+ cut_MET_filter

inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"

tableFileName = "./effTable.txt"

def print_eff_table(cut):
	list_ctau = ["0p01","0p1","5","10","50","100","200","400","600","800","1000","1200","4000","20000"]
	list_Lambda  = ["100","150","200","250","300","350","400"]

	weightedcut =  weight_cut + cut

	print weightedcut

	f1=open(tableFileName, 'a') 

	for this_ctau in list_ctau:
		ctau_value = this_ctau
		if this_ctau == "0p01":
			ctau_value = "0.01"
		if this_ctau == "0p1":
			ctau_value = "0.1"
		#print >> f1, "$c\\tau ="+ctau_value+" \\mathrm{cm} $ ",
		print >> f1, ctau_value,

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
				effThis_err = 0.1*np.ceil(10.0*effThis_err)

				print >> f1, "&"+"$ %.1f" % effThis + " \pm %.1f " % effThis_err + "$",
			else:
				print >> f1, "& -- ",
		print >> f1, "\\\\"
		#f1.close()

f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_3J_2G"
print >> f2, "------------------------------------------------"
print_eff_table(cut_tight_3J_2G)


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


