from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors, TMultiGraph
import os, sys
from Aux import *
import numpy as np
import array
import math

from config_noBDT import weight_cut, cut_GJets, cut_QCD_CR
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


pho1passSigmaIetaIetaTight = "pho1passSigmaIetaIetaTight"
pho1passSigmaIetaIetaLoose = "pho1passSigmaIetaIetaLoose"

pho1passSmajorTight = "pho1passSmajorTight"
pho1passSmajorLoose = "pho1passSmajorLoose"

ph1passHoverETight = "pho1passHoverETight"
ph1passHoverELoose = "pho1passHoverELoose"


cut_tight_3J_2G = 'n_Jets > 2 && (HLTDecision[81] == 1) && n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 30.0 && pho2sumNeutralHadronEt < 30.0 && pho2trkSumPtHollowConeDR03 < 30.0'
cut_tight_3J_2G_g2tight = "n_Jets > 2 &&n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 6.0 && pho2hcalPFClusterIso < 6.0 && (pho2sumNeutralHadronEt*(1.0-pho2isStandardPhoton) < 30.0) && (pho2trkSumPtHollowConeDR03 < 6.0 )&& abs(pho2Eta) <2.0 && pho2R9 > 0.8 &&(HLTDecision[81] == 1)"
cut_tight_3J_2G_g2trigger = "n_Jets > 2 &&n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight && pho2SigmaIetaIeta < 0.03 && pho2HoverE < 0.1 && pho2ecalPFClusterIso < 8.0 && pho2hcalPFClusterIso < 8.0 && (pho2sumNeutralHadronEt*(1.0-pho2isStandardPhoton) < 30.0) && (pho2trkSumPtHollowConeDR03 < 8.0 )&& abs(pho2Eta) <2.0 && pho2R9 > 0.65 &&(HLTDecision[81] == 1)"

inputDir = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/"

tableFileName = "./effTable.txt"

def print_eff_table(cut, label="test"):
	list_ctau = ["10","50", "100", "200","400","600","800","1000","1200","10000"]
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
	
				eff_this = 0.0
				if N_total > 0:
					eff_this = 100.0*N_pass/N_total
				Eeff_this = 0.0
				if N_pass > 0  and N_total > 0:
					Eeff_this = eff_this*np.sqrt(1.0/N_pass+1.0/N_total)
				
				list_eff.append(eff_this/100.0)
				list_eff_err.append(Eeff_this/100.0)

				Eeff_thisint = int(pow(10,-1*int(math.log10(Eeff_this))+1)*Eeff_this)
				Eeff_thisP = Eeff_thisint *1.0/pow(10,-1*int(math.log10(Eeff_this))+1)
				eff_thisP = int(eff_this*pow(10,-1*int(math.log10(Eeff_this))+1))*1.0/pow(10,-1*int(math.log10(Eeff_this))+1)
				if Eeff_thisint < 5:
					Eeff_thisP = int(pow(10,-1*int(math.log10(Eeff_this))+2)*Eeff_this)*1.0/pow(10,-1*int(math.log10(Eeff_this))+2)
					eff_thisP = int(eff_this*pow(10,-1*int(math.log10(Eeff_this))+2))*1.0/pow(10,-1*int(math.log10(Eeff_this))+2)
				'''
				if float(ctau_value) > 10.0:
					Eeff_this = 0.01*np.ceil(100.0*Eeff_this)
					print >> f1, "&"+"$ %.2f" % eff_this + " \pm %.2f " % Eeff_this + "$",
				else:
					Eeff_this = 0.1*np.ceil(10.0*Eeff_this)
					print >> f1, "&"+"$ %.1f" % eff_this + " \pm %.1f " % Eeff_this + "$",
				'''

				print >> f1, "& $"+str(eff_thisP)+" \\pm "+str(Eeff_thisP)+"$",
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
	mg_eff_vs_lambda.GetYaxis().SetRangeUser(0.0005, 1.5)
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
	

def print_2ndPhoton_triggerEff(fileName):
	fileThis = TFile(fileName, "READ")			
	treeThis = fileThis.Get("DelayedPhoton")
	
	cut_without_trigger_1stPhoton = "n_Jets > 2&& n_Photons == 2   && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1  && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0 && pho1Pt > 70 && pho1R9 > 0.9 && abs(pho1Eta)<1.4442 && pho1passIsoTight_comboIso && pho1passEleVeto && pho1Sminor<0.4 && pho1passSigmaIetaIetaTight && pho1passHoverETight && pho1passSmajorTight"

	print "HoverE, Sieie, Isolation, N_withoutTriggerCut, N_withTriggerCut, eff"	
	HoverE_cuts = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1]
	Sieie_cuts = [0.01, 0.015, 0.02, 0.025, 0.03]
	Isolation_cuts = [1.0, 3.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]
	for HoverE_this in HoverE_cuts:
		for Sieie_this in Sieie_cuts:
			for Isolation_this in Isolation_cuts:
				cut_without_trigger_this = cut_without_trigger_1stPhoton + " && pho2ecalPFClusterIso<"+str(Isolation_this)+" && pho2sumNeutralHadronEt < "+str(Isolation_this) + " && pho2trkSumPtHollowConeDR03 < "+str(Isolation_this) + " && pho2SigmaIetaIeta<"+str(Sieie_this) + " && pho2HoverE < "+str(HoverE_this)	
				cut_with_trigger_this = cut_without_trigger_this + " && (HLTDecision[81] == 1)"
				N_without_trigger = treeThis.GetEntries(cut_without_trigger_this)
				N_with_trigger = treeThis.GetEntries(cut_with_trigger_this)
				print str(HoverE_this)+", "+str(Sieie_this)+", "+str(Isolation_this)+", "+str(N_without_trigger)+", "+str(N_with_trigger)+", "+str(N_with_trigger*1.0/N_without_trigger)
	



f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_3J_2G"
print >> f2, "------------------------------------------------"
print cut_tight_3J_2G
#print_eff_table(cut_tight_3J_2G, "3J2G")

'''
f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_3J_2G_g2tight"
print >> f2, "------------------------------------------------"
print cut_tight_3J_2G_g2tight
print_eff_table(cut_tight_3J_2G_g2tight, "3J2G_g2tight")

f2=open(tableFileName, 'a') 
print >> f2, "------------------------------------------------"
print >> f2, "cut_tight_3J_2G_g2trigger"
print >> f2, "------------------------------------------------"
print cut_tight_3J_2G_g2trigger
print_eff_table(cut_tight_3J_2G_g2trigger, "3J2G_g2trigger")
'''



#print cut_GJets
#print_eff_table(cut_GJets, "GJetsCR")

#print cut_QCD_CR
#print_eff_table(cut_QCD_CR, "QCDCR")



