from ROOT import gStyle, gROOT, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TF1, TGraphErrors
import os, sys
from Aux import *
import numpy as np
import array
from config_noBDT import outputDir
from config_noBDT import lumi, weight_cut

gROOT.SetBatch(True)

gStyle.SetOptStat(0)

os.system("mkdir -p "+outputDir+"/ZeeTiming")
os.system("cp Timing*.py "+outputDir+"/ZeeTiming/")
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
topMargin    = 0.09
bottomMargin = 0.12

def properScale(hist):
	norm = 1.0/hist.Integral()
	for i in range(0, hist.GetNbinsX()+1):
		v0 = hist.GetBinContent(i)
		hist.SetBinContent(i, norm*v0)
		if v0 > 1:
			hist.SetBinError(i, norm*v0/np.sqrt(v0))
		else:
			hist.SetBinError(i, 0.0)

def singGausFit(hist, x_min, x_max):
	tf1_singGaus = TF1("tf1_singGaus","gaus(0)", x_min,x_max)
	tf1_singGaus.SetParameters(hist.Integral(),0.5*(x_min+x_max),0.3*(x_max-x_min))
	hist.Fit("tf1_singGaus","","",x_min,x_max)
	sigEff = 1000.0*np.abs(tf1_singGaus.GetParameter(2))
	esigEff = 1000.0*tf1_singGaus.GetParError(2)
	meanEff = 1000.0*tf1_singGaus.GetParameter(1)
	emeanEff = 1000.0*tf1_singGaus.GetParError(1)
	result = np.array([meanEff,emeanEff,sigEff,esigEff])
	return result

def doubGausFit(hist, x_min, x_max, sig_small, sig_big):
	tf1_doubGaus = TF1("tf1_doubGaus","gaus(0)+gaus(3)", x_min,x_max)
	#tf1_doubGaus.SetParameters(0.5*hist.Integral(),0.5*(x_min+x_max),0.2*(x_max-x_min), 0.5*hist.Integral(),0.5*(x_min+x_max),0.1*(x_max-x_min))
	tf1_doubGaus.SetParameters(0.5*hist.Integral(),0.5*(x_min+x_max),sig_small, 0.5*hist.Integral(),0.5*(x_min+x_max),sig_big)
	tf1_doubGaus.SetParLimits(2,0.0800,1.000)
	tf1_doubGaus.SetParLimits(5,0.0800,1.000)
	hist.Fit("tf1_doubGaus","B","",x_min,x_max)
	N1 = tf1_doubGaus.GetParameter(0)
	u1 = tf1_doubGaus.GetParameter(1)
	eu1 = tf1_doubGaus.GetParError(1)
	s1 = np.abs(tf1_doubGaus.GetParameter(2))
	es1 = tf1_doubGaus.GetParError(2)
	N2 = tf1_doubGaus.GetParameter(3)
	u2 = tf1_doubGaus.GetParameter(4)
	eu2 = tf1_doubGaus.GetParError(4)
	s2 = np.abs(tf1_doubGaus.GetParameter(5))
	es2 = tf1_doubGaus.GetParError(5)

	sigEff = 1000.0*(N1*s1 + N2*s2) / (N1+N2) 
	esigEff = 1000.0* np.sqrt(N1*N1*es1*es1 + N2*N2*es2*es2)/(N1+N2)
	meanEff = 1000.0*(N1*u1 + N2*u2) / (N1+N2) 
	emeanEff = 1000.0* np.sqrt(N1*N1*eu1*eu1 + N2*N2*eu2*eu2)/(N1+N2)
	
	result = np.array([meanEff,emeanEff,sigEff,esigEff])
	return result


	
####load data
cut = "abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && pho1SigmaIetaIeta < 0.00994"

file_data = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi_noreweight.root")
tree_data = file_data.Get("DelayedPhoton")


file_GJets = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HTAll_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
tree_GJets = file_GJets.Get("DelayedPhoton")


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

########correction vs. E##########
N_E_points = 19
E_divide = [40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 78.0, 84.0, 91.0, 100.0, 115.0, 140.0, 190.0, 1000.0]

x_E = np.zeros(N_E_points)
ex_E = np.zeros(N_E_points)
y_E_mean_data = np.zeros(N_E_points)
y_E_mean_GJets = np.zeros(N_E_points)
y_E_mean_GJets_corr = np.zeros(N_E_points)
y_E_mean_diff_GJets = np.zeros(N_E_points)
y_E_mean_diff_GJets_corr = np.zeros(N_E_points)
ey_E_mean_data = np.zeros(N_E_points)
ey_E_mean_GJets = np.zeros(N_E_points)
ey_E_mean_GJets_corr = np.zeros(N_E_points)
ey_E_mean_diff_GJets = np.zeros(N_E_points)
ey_E_mean_diff_GJets_corr = np.zeros(N_E_points)


for i in range(0, N_E_points):
	x_E[i] = 0.5*(E_divide[i+1]+E_divide[i])
	ex_E[i] = 0.5*(E_divide[i+1]-E_divide[i])
	E_low_this = E_divide[i]
	E_high_this = E_divide[i+1]
	cut_1g_this = cut+" && pho1Pt > "+str(E_low_this)+" && pho1Pt < "+str(E_high_this)

	hist_1g_this_data = TH1F("hist_1g_this_data_"+str(i),"hist_1g_this_data_"+str(i), 60, -1.5, 1.5)
	tree_data.Draw("pho1ClusterTime>>hist_1g_this_data_"+str(i),  weight_cut + cut_1g_this)
	result_1g_this_data = singGausFit(hist_1g_this_data, -0.6, 0.6) 
	myC.SaveAs(outputDir+"/ZeeTiming/iEFit_photon_"+str(i)+"_dt_data.png")
	y_E_mean_data[i] = result_1g_this_data[0]
	ey_E_mean_data[i] = result_1g_this_data[1]



	hist_1g_this_GJets = TH1F("hist_1g_this_GJets_"+str(i),"hist_1g_this_GJets_"+str(i), 60, -1.5, 1.5)
	tree_GJets.Draw("pho1ClusterTime>>hist_1g_this_GJets_"+str(i),  weight_cut + cut_1g_this)
	result_1g_this_GJets = singGausFit(hist_1g_this_GJets, -0.6, 0.6) 
	myC.SaveAs(outputDir+"/ZeeTiming/iEFit_photon_"+str(i)+"_dt_GJets.png")
	y_E_mean_GJets[i] = result_1g_this_GJets[0]
	ey_E_mean_GJets[i] = result_1g_this_GJets[1]

	y_E_mean_diff_GJets[i] = y_E_mean_data[i] -  y_E_mean_GJets[i]
	ey_E_mean_diff_GJets[i] = np.sqrt(ey_E_mean_data[i]*ey_E_mean_data[i] + ey_E_mean_GJets[i]*ey_E_mean_GJets[i])




	hist_1g_this_GJets_corr = TH1F("hist_1g_this_GJets_corr_"+str(i),"hist_1g_this_GJets_corr_"+str(i), 60, -1.5, 1.5)
	tree_GJets.Draw("pho1ClusterTime_SmearToData>>hist_1g_this_GJets_corr_"+str(i),  weight_cut + cut_1g_this)
	result_1g_this_GJets_corr = singGausFit(hist_1g_this_GJets_corr, -0.6, 0.6) 
	myC.SaveAs(outputDir+"/ZeeTiming/iEFit_photon_"+str(i)+"_dt_GJets_corr.png")
	y_E_mean_GJets_corr[i] = result_1g_this_GJets_corr[0]
	ey_E_mean_GJets_corr[i] = result_1g_this_GJets_corr[1]

	y_E_mean_diff_GJets_corr[i] = y_E_mean_data[i] -  y_E_mean_GJets_corr[i]
	ey_E_mean_diff_GJets_corr[i] = np.sqrt(ey_E_mean_data[i]*ey_E_mean_data[i] + ey_E_mean_GJets_corr[i]*ey_E_mean_GJets_corr[i])



print "y_E_mean_data:"
print y_E_mean_data
print "ey_E_mean_data:"
print ey_E_mean_data




print "y_E_mean_GJets:"
print y_E_mean_GJets
print "ey_E_mean_GJets:"
print ey_E_mean_GJets

print "y_E_mean_diff_GJets:"
print y_E_mean_diff_GJets
print "ey_E_mean_diff_GJets:"
print ey_E_mean_diff_GJets




print "y_E_mean_GJets_corr:"
print y_E_mean_GJets_corr
print "ey_E_mean_GJets_corr:"
print ey_E_mean_GJets_corr

print "y_E_mean_diff_GJets_corr:"
print y_E_mean_diff_GJets_corr
print "ey_E_mean_diff_GJets_corr:"
print ey_E_mean_diff_GJets_corr




gStyle.SetOptFit(0)
myC.SetGridy(1)
myC.SetLogx(1)

gr_E_mean_data  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_data), np.array(ex_E), np.array(ey_E_mean_data))
gr_E_mean_data.Draw("AP")
gr_E_mean_data.SetMarkerColor(kBlue)
gr_E_mean_data.SetLineColor(kBlue)
gr_E_mean_data.SetLineWidth(2)
gr_E_mean_data.SetTitle("")
gr_E_mean_data.GetXaxis().SetTitle("E^{#gamma} [GeV]")
gr_E_mean_data.GetYaxis().SetTitle("photon time [ps]")
gr_E_mean_data.GetXaxis().SetTitleSize( axisTitleSize )
gr_E_mean_data.GetXaxis().SetTitleOffset( axisTitleOffset )
gr_E_mean_data.GetYaxis().SetTitleSize( axisTitleSize )
gr_E_mean_data.GetYaxis().SetTitleOffset( axisTitleOffset +0.18 )
gr_E_mean_data.GetYaxis().SetRangeUser(-350,400)


gr_E_mean_GJets  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_GJets), np.array(ex_E), np.array(ey_E_mean_GJets))
gr_E_mean_GJets.SetMarkerColor(kRed)
gr_E_mean_GJets.SetLineColor(kRed)
gr_E_mean_GJets.SetLineWidth(2)
gr_E_mean_GJets.Draw("Psame")

gr_E_mean_diff_GJets  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_diff_GJets), np.array(ex_E), np.array(ey_E_mean_diff_GJets))
gr_E_mean_diff_GJets.SetMarkerColor(kRed+4)
gr_E_mean_diff_GJets.SetLineColor(kRed+4)
gr_E_mean_diff_GJets.SetLineWidth(2)
#gr_E_mean_diff_GJets.Draw("Psame")


gr_E_mean_GJets_corr  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_GJets_corr), np.array(ex_E), np.array(ey_E_mean_GJets_corr))
gr_E_mean_GJets_corr.SetMarkerColor(kViolet)
gr_E_mean_GJets_corr.SetLineColor(kViolet)
gr_E_mean_GJets_corr.SetLineWidth(2)
gr_E_mean_GJets_corr.Draw("Psame")

gr_E_mean_diff_GJets_corr  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_diff_GJets_corr), np.array(ex_E), np.array(ey_E_mean_diff_GJets_corr))
gr_E_mean_diff_GJets_corr.SetMarkerColor(kViolet+4)
gr_E_mean_diff_GJets_corr.SetLineColor(kViolet+4)
gr_E_mean_diff_GJets_corr.SetLineWidth(2)
#gr_E_mean_diff_GJets_corr.Draw("Psame")



leg_mean_GJets = TLegend(0.18,0.75,0.93,0.89)
leg_mean_GJets.SetNColumns(3)
leg_mean_GJets.SetBorderSize(0)
leg_mean_GJets.SetTextSize(0.035)
leg_mean_GJets.SetLineColor(1)
leg_mean_GJets.SetLineStyle(1)
leg_mean_GJets.SetLineWidth(1)
leg_mean_GJets.SetFillColor(0)
leg_mean_GJets.SetFillStyle(1001)
leg_mean_GJets.AddEntry(gr_E_mean_data, "data", "lep")
leg_mean_GJets.AddEntry(gr_E_mean_GJets, "#gamma+jets MC", "lep")
#leg_mean_GJets.AddEntry(gr_E_mean_diff_GJets, "#Delta(data, #gamma+jets)", "lep")
leg_mean_GJets.AddEntry(gr_E_mean_GJets_corr, "#gamma+jets MC corrected", "lep")
#leg_mean_GJets.AddEntry(gr_E_mean_diff_GJets_corr, "#Delta(data, #gamma+jets corrected)", "lep")
leg_mean_GJets.Draw()

drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_photon_vs_E_Data_vs_GJets_2016.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_photon_vs_E_Data_vs_GJets_2016.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_photon_vs_E_Data_vs_GJets_2016.C")

