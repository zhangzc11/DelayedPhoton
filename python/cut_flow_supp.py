from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors
import os, sys
import numpy as np
import array
import math
from config_noBDT import weight_cut
from Aux import getXsecBR

#ctau_data = ['10', '50', '100', '200', '400', '600', '800', '1000', '1200', '10000']
#lambda_data = ['100', '150', '200', '250', '300', '350', '400']
#ctau_data = ['10', '100', '1000', '10000']
ctau_data = ['200']
lambda_data = ['100', '200', '300', '400']



cuts = ["(HLTDecision[81] == 1)", "pho1Pt > 70", "abs(pho1Eta)<1.4442", "pho1passIsoTight_comboIso && pho1passSmajorTight && pho1Sminor<0.4 && pho1R9 > 0.9 && pho1passSigmaIetaIetaTight && pho1passHoverETight ", "pho1passEleVeto", "n_Jets > 2", "Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0", "n_Photons == 2", " n_Photons == 2", "pho2SigmaIetaIeta<0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso<30.0 && pho2sumNeutralHadronEt<30.0 && pho2trkSumPtHollowConeDR03 < 30.0"]
cuts_name = ["+ Signal Trigger", "+ 1st Photon $\\pt>70\GeV$", "+ 1st Photon $\\abs{\\eta} < 1.4442$", "+ 1st Photon Tight ID", "+ 1st Photon Electron Veto", "+ nJets$\\geq3$", "+ Anomalous \\ptmiss filters", "+ 2nd Photon $\\pt>40\\GeV$", "+ 2nd Photon $1.566 < \\abs{\\eta} < 2.5$", "+ 2nd Photon Very Loose ID"]

gROOT.SetBatch(True)

tableFileName = "./cut_flow_Table_supp.txt"
f1=open(tableFileName, 'a')

for Ctau in ctau_data:
	eff_flow = np.zeros((len(lambda_data), len(cuts)))
	Eeff_flow = np.zeros((len(lambda_data), len(cuts)))

	
	for idx_lambda in range(len(lambda_data)):
		Lambda = lambda_data[idx_lambda]

		fileNameSig = "~/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L"+Lambda+"TeV_Ctau"+Ctau+"cm_13TeV-pythia8.root"
		fileSig = TFile(fileNameSig, "READ")
		hNEventsThis_Sig = fileSig.Get("NEvents")
		treeSig = fileSig.Get("DelayedPhoton")

		xsec_Sig, exsec_Sig =  getXsecBR(Lambda, Ctau)

		N_total_Sig = hNEventsThis_Sig.GetBinContent(1)
		lumi_xs_Sig = xsec_Sig*35922.0
		N_beforePreselection_Sig =  lumi_xs_Sig
		
		final_cut = weight_cut + "("
		for idx in range(len(cuts)):
			if idx == 0:
				final_cut = final_cut + ""+ cuts[idx]
			else:
				final_cut = final_cut + "&& "+ cuts[idx]
			this_cut = final_cut + ")"
			print this_cut
			hist_this = TH1F("hist_"+str(idx)+Ctau+Lambda, "hist_"+str(idx), 100,0,100)
			treeSig.Draw("NPU>>hist_"+str(idx)+Ctau+Lambda, this_cut)
		
			N_this = lumi_xs_Sig*hist_this.Integral()/N_total_Sig
			print hist_this.Integral()
			
			#print str(N_this)+", "+str(N_beforePreselection_Sig)
			eff_this = 100.0*(N_this/N_beforePreselection_Sig)	
			Eeff_this  = 100.0*(N_this/N_beforePreselection_Sig*np.sqrt(1.0/hist_this.Integral() + 1.0/N_total_Sig))
			
			'''
			Eeff_thisint = int(pow(10,-1*int(math.log10(Eeff_this))+1)*Eeff_this)
			Eeff_thisP = Eeff_thisint *1.0/pow(10,-1*int(math.log10(Eeff_this))+1)
			eff_thisP = int(eff_this*pow(10,-1*int(math.log10(Eeff_this))+1))*1.0/pow(10,-1*int(math.log10(Eeff_this))+1)
			if Eeff_thisint < 5:
				Eeff_thisP = int(pow(10,-1*int(math.log10(Eeff_this))+2)*Eeff_this)*1.0/pow(10,-1*int(math.log10(Eeff_this))+2)
				eff_thisP = int(eff_this*pow(10,-1*int(math.log10(Eeff_this))+2))*1.0/pow(10,-1*int(math.log10(Eeff_this))+2)
			'''
			eff_flow[idx_lambda][idx] = eff_this
			Eeff_flow[idx_lambda][idx] = Eeff_this
		
		final_cut = final_cut + ")"
		
		#print "final cut ===> "+final_cut
		print Ctau
		print Lambda
		print eff_flow[idx_lambda]
		print Eeff_flow[idx_lambda]
	print "\\begin{table}[!htb]"
	print "\\footnotesize"
	print "\\begin{center}"
	print "\\caption{(2016) Event selection cut-flow efficiency for GMSB SPS8 $\\ctau = "+Ctau+"\\cm$ and varying $\\Lambda$ (unit of efficiency$: \\%$; unit of $\\Lambda: \\TeV$) using the 2016 event selection.}"
	print "\\label{tab:cut_flow_ctau"+Ctau+"_2016}"
	print "\\begin{tabular}{c|",
	for idx_lambda in range(len(lambda_data)):
		print " c ",
	print "}"
	print "\\hline"
	for idx_lambda in range(len(lambda_data)):
		print " & $\\Lambda="+lambda_data[idx_lambda]+"$ ",
	print "\\\\"
	print "\\hline"
	print " - ",
	for idx_lambda in range(len(lambda_data)):
		print " & $100.00 \\pm 0.00$ ",
	print "\\\\"
	for idx in range(len(cuts)):
		print cuts_name[idx],
		for idx_lambda in range(len(lambda_data)):
			print " & $"+str(eff_flow[idx_lambda][idx])+" \\pm "+str(Eeff_flow[idx_lambda][idx])+"$",
		print "\\\\"
        print "\\hline"
        print "\\end{tabular}"
        print "\\end{center}"
        print "\\end{table}"
	print "\n"
		
	
	
	

