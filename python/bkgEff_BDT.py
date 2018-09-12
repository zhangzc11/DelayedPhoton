from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array
from confit_noBDT import weight_cut

gROOT.SetBatch(True)

cut_BDT_tight = 'disc > 0.10'
cut_BDT_loose = 'disc > 0.0586'

cut_EGM_tight = 'pho1passIsoTight_PFClusterIso && pho1Sminor>0.15 && pho1Sminor<0.3'
cut_EGM_loose = 'pho1passIsoLoose_PFClusterIso && pho1Sminor>0.15 && pho1Sminor<0.7'

inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/skim_withBDT/"

tableFileName = "./effTable_bkg.txt"

def print_effBDT_table(cut_tight, cut_loose):
	list_label = ["QCD_HT200to300", "QCD_HT300to500", "QCD_HT500to700", "QCD_HT700to1000", "QCD_HT1000to1500", "QCD_HT1500to2000", "QCD_HT2000toInf", "GJets_HT-40To100", "GJets_HT-100To200", "GJets_HT-200To400", "GJets_HT-400To600", "GJets_HT-600ToInf"]

	weightedcut_tight =  weight_cut + cut_tight
	weightedcut_loose =  weight_cut + cut_loose

	print weightedcut_tight
	print weightedcut_loose

	f1=open(tableFileName, 'a') 

	for this_label in list_label:
		print >> f1, "&"+this_label,
		fileName = inputDir+"DelayedPhoton_"+this_label+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
		fileThis = TFile(fileName, "READ")			
		if fileThis.IsOpen():
			treeThis = fileThis.Get("DelayedPhoton")
			histThis_tight = TH1F("histThis_tight","",100,0,100)
			histThis_loose = TH1F("histThis_loose","",100,0,100)
			histThis_total = TH1F("histThis_total","",100,0,100)
		
			treeThis.Draw("NPU>>histThis_tight",weightedcut_tight)
			treeThis.Draw("NPU>>histThis_loose",weightedcut_loose)
			treeThis.Draw("NPU>>histThis_total","")

			N_pass_tight = histThis_tight.Integral()
			N_pass_loose = histThis_loose.Integral()
			N_total = histThis_total.Integral()

			effThis_tight = 0.0
			effThis_loose = 0.0
			if N_total > 0:
				effThis_tight = 100.0*N_pass_tight/N_total
				effThis_loose = 100.0*N_pass_loose/N_total
			effThis_tight_err = 0.0
			effThis_loose_err = 0.0
			if N_pass_tight > 0  and N_total > 0:
				effThis_tight_err = effThis_tight*np.sqrt(1.0/N_pass_tight+1.0/N_total)
			if N_pass_loose > 0  and N_total > 0:
				effThis_loose_err = effThis_loose*np.sqrt(1.0/N_pass_loose+1.0/N_total)

			effThis_tight_err = 0.1*np.ceil(10.0*effThis_tight_err)
			effThis_loose_err = 0.1*np.ceil(10.0*effThis_loose_err)

			print >> f1, "&"+"$ (%.1f" % effThis_tight + " \pm %.1f " % effThis_tight_err + ")\\%$"+"&"+"$ (%.1f" % effThis_loose + " \pm %.1f " % effThis_loose_err+")\\%$",
		else:
			print >> f1, "& -- ",
		print >> f1, "\\\\"
		#f1.close()

'''
f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_loose_BDT"
print >> f2, "------------------------------------------------"
print_effBDT_table(cut_BDT_tight, cut_BDT_loose)
'''

f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_loose_EGM"
print >> f2, "------------------------------------------------"
print_effBDT_table(cut_EGM_tight, cut_EGM_loose)


