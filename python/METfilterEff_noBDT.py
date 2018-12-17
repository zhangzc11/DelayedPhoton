from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors
import os, sys
from Aux import *
import numpy as np
import array

from config_noBDT import weight_cut

gROOT.SetBatch(True)


cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"
cut_MET_filter_new = " && Flag_HBHENoiseFilter == 1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"

cut_with_METfilter = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2'+ cut_MET_filter + '&& pho1SigmaIetaIeta < 0.00994'
cut_with_METfilter_new = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2'+ cut_MET_filter_new + '&& pho1SigmaIetaIeta < 0.00994'
cut_no_METfilter = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 && pho1SigmaIetaIeta < 0.00994'

inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"

tableFileName = "./effTable.txt"

def print_eff_table(cut_before, cut_after):
	list_ctau = ["0_1","10","200","400","600","800","1000","1200"]
	list_Lambda  = ["100","150","200","250","300","350","400"]

	weightedcut_before =  weight_cut + "("+cut_before+")"
	weightedcut_after =  weight_cut + "("+cut_after+")"

	print weightedcut_before
	print weightedcut_after

	f1=open(tableFileName, 'a') 

	for this_ctau in list_ctau:
		ctau_value = this_ctau
		if this_ctau == "0_1":
			ctau_value = "0.1"
		#print >> f1, "$c\\tau ="+ctau_value+" \\mathrm{cm} $ ",
		print >> f1, ctau_value,

		for this_lambda in list_Lambda:
			fileName = inputDir+"GMSB_L"+this_lambda+"TeV_Ctau"+this_ctau+"cm_13TeV-pythia8.root"
			fileThis = TFile(fileName, "READ")			
			if fileThis.IsOpen():

				treeThis = fileThis.Get("DelayedPhoton")
				histThis_before = TH1F("histThis_before","",100,0,100)
				histThis_after = TH1F("histThis_after","",100,0,100)
			
				treeThis.Draw("NPU>>histThis_before",weightedcut_before)
				treeThis.Draw("NPU>>histThis_after",weightedcut_after)

				N_total = histThis_before.Integral()
				N_pass = histThis_after.Integral()
	
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
print >> f2, "MET filter efficiency"
print >> f2, "------------------------------------------------"
print_eff_table(cut_no_METfilter, cut_with_METfilter)


f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "MET filter efficiency new"
print >> f2, "------------------------------------------------"
print_eff_table(cut_no_METfilter, cut_with_METfilter_new)

