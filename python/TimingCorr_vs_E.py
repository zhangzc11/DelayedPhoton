from ROOT import gROOT, gStyle, TFile, TTree, TCanvas, TH1F, TH1, TLegend, TLatex, TColor, TF1, TGraphErrors, kBlue, kRed, kViolet, kBlack
import os, sys
from Aux import *
import numpy as np
import array
from config_noBDT import outputDir
from config_noBDT import lumi

gROOT.SetBatch(True)

gStyle.SetOptStat(0)

os.system("mkdir -p "+outputDir+"/ZeeTiming")
os.system("mkdir -p "+outputDir+"/ZeeTiming/fits")
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

def singGausFit(hist):
	x_mean = hist.GetMean()
	x_stddev = hist.GetStdDev()
	x_min = x_mean - 2.0*x_stddev
	x_max = x_mean + 2.0*x_stddev
	tf1_singGaus = TF1("tf1_singGaus","gaus(0)", x_min,x_max)
	tf1_singGaus.SetParameters(hist.Integral(),x_mean, x_stddev)
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

def doubGausFit(hist):
	x_mean = hist.GetMean()
        x_stddev = hist.GetStdDev()
        x_min = x_mean - 4.0*x_stddev
        x_max = x_mean + 4.0*x_stddev
	sig_small = 0.5*x_stddev
	sig_big = 1.0*x_stddev
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
cut = "mass>60 && mass <120 && ele1Pt>30 && ele2Pt>30 && ele1IsEB && ele2IsEB"

file_data = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/All2016.root")
tree_data = file_data.Get("ZeeTiming")

file_MC = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/MC2016_all.root")
tree_MC = file_MC.Get("ZeeTiming")

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
y_E_mean_MC = np.zeros(N_E_points)
y_E_mean_MC_corr = np.zeros(N_E_points)
y_E_mean_diff = np.zeros(N_E_points)
y_E_mean_diff_corr = np.zeros(N_E_points)
y_E_sigma_dt_data = np.zeros(N_E_points)
y_E_sigma_dt_MC = np.zeros(N_E_points)
y_E_sigma_dt_MC_corr= np.zeros(N_E_points)
y_E_sigma_dt_diff = np.zeros(N_E_points)
y_E_sigma_dt_diff_corr = np.zeros(N_E_points)

y_E_sigma_time_data = np.zeros(N_E_points)
y_E_sigma_time_MC = np.zeros(N_E_points)
y_E_sigma_time_MC_corr= np.zeros(N_E_points)
y_E_sigma_time_diff = np.zeros(N_E_points)
y_E_sigma_time_diff_corr = np.zeros(N_E_points)

ey_E_mean_data = np.zeros(N_E_points)
ey_E_mean_MC = np.zeros(N_E_points)
ey_E_mean_MC_corr = np.zeros(N_E_points)
ey_E_mean_diff = np.zeros(N_E_points)
ey_E_mean_diff_corr = np.zeros(N_E_points)

ey_E_sigma_dt_data = np.zeros(N_E_points)
ey_E_sigma_dt_MC = np.zeros(N_E_points)
ey_E_sigma_dt_MC_corr = np.zeros(N_E_points)
ey_E_sigma_dt_diff = np.zeros(N_E_points)
ey_E_sigma_dt_diff_corr = np.zeros(N_E_points)

ey_E_sigma_time_data = np.zeros(N_E_points)
ey_E_sigma_time_MC = np.zeros(N_E_points)
ey_E_sigma_time_MC_corr = np.zeros(N_E_points)
ey_E_sigma_time_diff = np.zeros(N_E_points)
ey_E_sigma_time_diff_corr = np.zeros(N_E_points)


gStyle.SetOptFit(1)

myC.SetLogy(1)

for i in range(0, N_E_points):
	x_E[i] = 0.5*(E_divide[i+1]+E_divide[i])
	ex_E[i] = 0.5*(E_divide[i+1]-E_divide[i])
	E_low_this = E_divide[i]
	E_high_this = E_divide[i+1]
	cut_1e_this = cut+" && ele1E > "+str(E_low_this)+" && ele1E < "+str(E_high_this)
	cut_2e_this = cut+" && ele1E > "+str(E_low_this)+" && ele1E < "+str(E_high_this)+" && ele2E < "+str(E_high_this)

	hist_1e_this_data = TH1F("hist_1e_this_data_"+str(i),"hist_1e_this_data_"+str(i), 120, -3.0, 3.0)
	hist_2e_this_data = TH1F("hist_2e_this_data_"+str(i),"hist_2e_this_data_"+str(i), 120, -3.0, 3.0)
	tree_data.Draw("t1>>hist_1e_this_data_"+str(i), cut_1e_this)
	tree_data.Draw("t1-t2>>hist_2e_this_data_"+str(i), cut_2e_this)
	hist_1e_this_data.Draw()
	result_1e_this_data = doubGausFit(hist_1e_this_data)#, -0.6, 0.6) 
	myC.SaveAs(outputDir+"/ZeeTiming/fits/iEFit_Zee_"+str(i)+"_time_data.png")
	hist_2e_this_data.Draw()
	result_2e_this_data = doubGausFit(hist_2e_this_data)#, -1.5, 1.5, 0.2, 0.4) 
	myC.SaveAs(outputDir+"/ZeeTiming/fits/iEFit_Zee_"+str(i)+"_dt_data.png")
	y_E_mean_data[i] = result_1e_this_data[0]
	ey_E_mean_data[i] = result_1e_this_data[1]
	y_E_sigma_dt_data[i] = result_2e_this_data[2]
	y_E_sigma_time_data[i] = result_1e_this_data[2]
	ey_E_sigma_dt_data[i] = result_2e_this_data[3]
	ey_E_sigma_time_data[i] = result_1e_this_data[3]


	hist_1e_this_MC = TH1F("hist_1e_this_MC_"+str(i),"hist_1e_this_MC_"+str(i), 120, -3.0, 3.0)
	hist_2e_this_MC = TH1F("hist_2e_this_MC_"+str(i),"hist_2e_this_MC_"+str(i), 120, -3.0, 3.0)
	tree_MC.Draw("t1>>hist_1e_this_MC_"+str(i),  "(weight*pileupWeight) * " + cut_1e_this)
	tree_MC.Draw("t1-t2>>hist_2e_this_MC_"+str(i),  "(weight*pileupWeight) * " + cut_2e_this)
	hist_1e_this_MC.Draw()
	result_1e_this_MC = doubGausFit(hist_1e_this_MC)#, -0.6, 0.6) 
	myC.SaveAs(outputDir+"/ZeeTiming/fits/iEFit_Zee_"+str(i)+"_time_MC.png")
	hist_2e_this_MC.Draw()
	result_2e_this_MC = doubGausFit(hist_2e_this_MC)#, -1.0, 1.0, 0.15, 0.30) 
	myC.SaveAs(outputDir+"/ZeeTiming/fits/iEFit_Zee_"+str(i)+"_dt_MC.png")
	y_E_mean_MC[i] = result_1e_this_MC[0]
	ey_E_mean_MC[i] = result_1e_this_MC[1]
	y_E_sigma_dt_MC[i] = result_2e_this_MC[2]
	y_E_sigma_time_MC[i] = result_1e_this_MC[2]
	ey_E_sigma_dt_MC[i] = result_2e_this_MC[3]
	ey_E_sigma_time_MC[i] = result_1e_this_MC[3]

	y_E_mean_diff[i] = y_E_mean_data[i] -  y_E_mean_MC[i]
	ey_E_mean_diff[i] = np.sqrt(ey_E_mean_data[i]*ey_E_mean_data[i] + ey_E_mean_MC[i]*ey_E_mean_MC[i])
	y_E_sigma_dt_diff[i] = np.sqrt(y_E_sigma_dt_data[i]*y_E_sigma_dt_data[i] -  y_E_sigma_dt_MC[i]*y_E_sigma_dt_MC[i])
	y_E_sigma_time_diff[i] = np.sqrt(y_E_sigma_time_data[i]*y_E_sigma_time_data[i] -  y_E_sigma_time_MC[i]*y_E_sigma_time_MC[i])
	ey_E_sigma_dt_diff[i] = np.sqrt(4.0*y_E_sigma_dt_data[i]*y_E_sigma_dt_data[i]*ey_E_sigma_dt_data[i]*ey_E_sigma_dt_data[i]+4.0*y_E_sigma_dt_MC[i]*y_E_sigma_dt_MC[i]*ey_E_sigma_dt_MC[i]*ey_E_sigma_dt_MC[i])/(2.0*y_E_sigma_dt_diff[i])
	ey_E_sigma_time_diff[i] = np.sqrt(4.0*y_E_sigma_time_data[i]*y_E_sigma_time_data[i]*ey_E_sigma_time_data[i]*ey_E_sigma_time_data[i]+4.0*y_E_sigma_time_MC[i]*y_E_sigma_time_MC[i]*ey_E_sigma_time_MC[i]*ey_E_sigma_time_MC[i])/(2.0*y_E_sigma_time_diff[i])



	hist_1e_this_MC_corr = TH1F("hist_1e_this_MC_corr_"+str(i),"hist_1e_this_MC_corr_"+str(i), 120, -3.0, 3.0)
	hist_2e_this_MC_corr = TH1F("hist_2e_this_MC_corr_"+str(i),"hist_2e_this_MC_corr_"+str(i), 120, -3.0, 3.0)
	tree_MC.Draw("t1_SmearToData>>hist_1e_this_MC_corr_"+str(i),  "(weight*pileupWeight) * " + cut_1e_this)
	tree_MC.Draw("t1_SmearToData-t2_SmearToData>>hist_2e_this_MC_corr_"+str(i),  "(weight*pileupWeight) * " + cut_2e_this)
	hist_1e_this_MC_corr.Draw()
	result_1e_this_MC_corr = doubGausFit(hist_1e_this_MC_corr)#, -0.6, 0.6) 
	myC.SaveAs(outputDir+"/ZeeTiming/fits/iEFit_Zee_"+str(i)+"_time_MC_corr.png")
	hist_2e_this_MC_corr.Draw()
	result_2e_this_MC_corr = doubGausFit(hist_2e_this_MC_corr)#, -1.0, 1.0, 0.15, 0.30) 
	myC.SaveAs(outputDir+"/ZeeTiming/fits/iEFit_Zee_"+str(i)+"_dt_MC_corr.png")
	y_E_mean_MC_corr[i] = result_1e_this_MC_corr[0]
	ey_E_mean_MC_corr[i] = result_1e_this_MC_corr[1]
	y_E_sigma_dt_MC_corr[i] = result_2e_this_MC_corr[2]
	y_E_sigma_time_MC_corr[i] = result_1e_this_MC_corr[2]
	ey_E_sigma_dt_MC_corr[i] = result_2e_this_MC_corr[3]
	ey_E_sigma_time_MC_corr[i] = result_1e_this_MC_corr[3]


	y_E_mean_diff_corr[i] = y_E_mean_data[i] -  y_E_mean_MC_corr[i]
	ey_E_mean_diff_corr[i] = np.sqrt(ey_E_mean_data[i]*ey_E_mean_data[i] + ey_E_mean_MC_corr[i]*ey_E_mean_MC_corr[i])
	y_E_sigma_dt_diff_corr[i] = np.sqrt(abs(y_E_sigma_dt_data[i]*y_E_sigma_dt_data[i] -  y_E_sigma_dt_MC_corr[i]*y_E_sigma_dt_MC_corr[i]))
	y_E_sigma_time_diff_corr[i] = np.sqrt(abs(y_E_sigma_time_data[i]*y_E_sigma_time_data[i] -  y_E_sigma_time_MC_corr[i]*y_E_sigma_time_MC_corr[i]))
	ey_E_sigma_dt_diff_corr[i] = np.sqrt(4.0*y_E_sigma_dt_data[i]*y_E_sigma_dt_data[i]*ey_E_sigma_dt_data[i]*ey_E_sigma_dt_data[i]+4.0*y_E_sigma_dt_MC_corr[i]*y_E_sigma_dt_MC_corr[i]*ey_E_sigma_dt_MC_corr[i]*ey_E_sigma_dt_MC_corr[i])/(2.0*y_E_sigma_dt_diff_corr[i])
	ey_E_sigma_time_diff_corr[i] = np.sqrt(4.0*y_E_sigma_time_data[i]*y_E_sigma_time_data[i]*ey_E_sigma_time_data[i]*ey_E_sigma_time_data[i]+4.0*y_E_sigma_time_MC_corr[i]*y_E_sigma_time_MC_corr[i]*ey_E_sigma_time_MC_corr[i]*ey_E_sigma_time_MC_corr[i])/(2.0*y_E_sigma_time_diff_corr[i])


gStyle.SetOptFit(0)
myC.SetLogy(0)

print "y_E_mean_data:"
print y_E_mean_data
print "ey_E_mean_data:"
print ey_E_mean_data

print "y_E_mean_MC:"
print y_E_mean_MC
print "ey_E_mean_MC:"
print ey_E_mean_MC


print "y_E_mean_MC_corr:"
print y_E_mean_MC_corr
print "ey_E_mean_MC_corr:"
print ey_E_mean_MC_corr


print "y_E_mean_diff:"
print y_E_mean_diff
print "ey_E_mean_diff:"
print ey_E_mean_diff

print "y_E_mean_diff_corr:"
print y_E_mean_diff_corr
print "ey_E_mean_diff_corr:"
print ey_E_mean_diff_corr


print "y_E_sigma_dt_data:"
print y_E_sigma_dt_data
print "ey_E_sigma_dt_data:"
print ey_E_sigma_dt_data

print "y_E_sigma_dt_MC:"
print y_E_sigma_dt_MC
print "ey_E_sigma_dt_MC:"
print ey_E_sigma_dt_MC

print "y_E_sigma_dt_MC_corr:"
print y_E_sigma_dt_MC_corr
print "ey_E_sigma_dt_MC_corr:"
print ey_E_sigma_dt_MC_corr


print "y_E_sigma_dt_diff:"
print y_E_sigma_dt_diff
print "ey_E_sigma_dt_diff:"
print ey_E_sigma_dt_diff

print "y_E_sigma_dt_diff_corr:"
print y_E_sigma_dt_diff_corr
print "ey_E_sigma_dt_diff_corr:"
print ey_E_sigma_dt_diff_corr

print "y_E_sigma_time_data:"
print y_E_sigma_time_data
print "ey_E_sigma_time_data:"
print ey_E_sigma_time_data

print "y_E_sigma_time_MC:"
print y_E_sigma_time_MC
print "ey_E_sigma_time_MC:"
print ey_E_sigma_time_MC

print "y_E_sigma_time_MC_corr:"
print y_E_sigma_time_MC_corr
print "ey_E_sigma_time_MC_corr:"
print ey_E_sigma_time_MC_corr


print "y_E_sigma_time_diff:"
print y_E_sigma_time_diff
print "ey_E_sigma_time_diff:"
print ey_E_sigma_time_diff


print "y_E_sigma_time_diff_corr:"
print y_E_sigma_time_diff_corr
print "ey_E_sigma_time_diff_corr:"
print ey_E_sigma_time_diff_corr

gStyle.SetOptFit(0)
myC.SetGridy(1)
myC.SetLogx(1)

gr_E_mean_data  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_data), np.array(ex_E), np.array(ey_E_mean_data))
gr_E_mean_data.Draw("AP")
gr_E_mean_data.SetMarkerColor(kBlue)
gr_E_mean_data.SetLineColor(kBlue)
gr_E_mean_data.SetLineWidth(2)
gr_E_mean_data.SetTitle("")
gr_E_mean_data.GetXaxis().SetTitle("E^{e} [GeV]")
gr_E_mean_data.GetYaxis().SetTitle("electron time [ps]")
gr_E_mean_data.GetXaxis().SetTitleSize( axisTitleSize )
gr_E_mean_data.GetXaxis().SetTitleOffset( axisTitleOffset )
gr_E_mean_data.GetYaxis().SetTitleSize( axisTitleSize )
gr_E_mean_data.GetYaxis().SetTitleOffset( axisTitleOffset +0.18 )
gr_E_mean_data.GetYaxis().SetRangeUser(-350,600)
gr_E_mean_data.GetXaxis().SetRangeUser(70,1000)

gr_E_mean_MC  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_MC), np.array(ex_E), np.array(ey_E_mean_MC))
gr_E_mean_MC.SetMarkerColor(kRed)
gr_E_mean_MC.SetLineColor(kRed)
gr_E_mean_MC.SetLineWidth(2)
gr_E_mean_MC.Draw("Psame")

gr_E_mean_MC_corr  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_MC_corr), np.array(ex_E), np.array(ey_E_mean_MC_corr))
gr_E_mean_MC_corr.SetMarkerColor(kRed)
gr_E_mean_MC_corr.SetLineColor(kRed)
gr_E_mean_MC_corr.SetLineWidth(2)
#gr_E_mean_MC_corr.Draw("Psame")


gr_E_mean_diff  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_diff), np.array(ex_E), np.array(ey_E_mean_diff))
gr_E_mean_diff.SetMarkerColor(kBlack)
gr_E_mean_diff.SetLineColor(kBlack)
gr_E_mean_diff.SetLineWidth(2)
gr_E_mean_diff.Draw("Psame")

gr_E_mean_diff_corr  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_mean_diff_corr), np.array(ex_E), np.array(ey_E_mean_diff_corr))
gr_E_mean_diff_corr.SetMarkerColor(kBlack)
gr_E_mean_diff_corr.SetLineColor(kBlack)
gr_E_mean_diff_corr.SetLineWidth(2)
#gr_E_mean_diff_corr.Draw("Psame")

leg_mean = TLegend(0.18,0.75,0.93,0.89)
leg_mean.SetNColumns(3)
leg_mean.SetBorderSize(0)
leg_mean.SetTextSize(0.03)
leg_mean.SetLineColor(1)
leg_mean.SetLineStyle(1)
leg_mean.SetLineWidth(1)
leg_mean.SetFillColor(0)
leg_mean.SetFillStyle(1001)
leg_mean.AddEntry(gr_E_mean_data, "data", "lep")
leg_mean.AddEntry(gr_E_mean_MC, "MC", "lep")
leg_mean.AddEntry(gr_E_mean_diff, "#Delta(data, MC)", "lep")
#leg_mean.AddEntry(gr_E_mean_MC_corr, "MC corr.", "lep")
leg_mean.Draw()

drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_Zee_vs_E_Data_vs_MC_2016_noCorr.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_Zee_vs_E_Data_vs_MC_2016_noCorr.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_Zee_vs_E_Data_vs_MC_2016_noCorr.C")
gr_E_mean_data.Draw("AP")
gr_E_mean_data.GetYaxis().SetRangeUser(-50,200)
gr_E_mean_MC_corr.Draw("Psame")
gr_E_mean_diff_corr.Draw("Psame")
leg_mean.Draw()
drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_Zee_vs_E_Data_vs_MC_2016_Corr.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_Zee_vs_E_Data_vs_MC_2016_Corr.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_Zee_vs_E_Data_vs_MC_2016_Corr.C")

file_plot_shift = TFile(outputDir+"/ZeeTiming/TimingShift_Zee_vs_E_Data_vs_MC_2016.root","RECREATE")
gr_E_mean_data.Write("gr_data")
gr_E_mean_MC.Write("gr_MC")
gr_E_mean_MC_corr.Write("gr_MC_corr")
gr_E_mean_diff.Write("gr_diff")
file_plot_shift.Close()

gr_E_sigma_dt_data  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_dt_data), np.array(ex_E), np.array(ey_E_sigma_dt_data))
gr_E_sigma_dt_data.Draw("AP")
gr_E_sigma_dt_data.SetMarkerColor(kBlue)
gr_E_sigma_dt_data.SetLineColor(kBlue)
gr_E_sigma_dt_data.SetLineWidth(2)
gr_E_sigma_dt_data.SetTitle("")
gr_E_sigma_dt_data.GetXaxis().SetTitle("E^{e} [GeV]")
gr_E_sigma_dt_data.GetYaxis().SetTitle("#sigma_{t1-t2} [ps]")
gr_E_sigma_dt_data.GetXaxis().SetTitleSize( axisTitleSize )
gr_E_sigma_dt_data.GetXaxis().SetTitleOffset( axisTitleOffset )
gr_E_sigma_dt_data.GetYaxis().SetTitleSize( axisTitleSize )
gr_E_sigma_dt_data.GetYaxis().SetTitleOffset( axisTitleOffset +0.18 )
gr_E_sigma_dt_data.GetYaxis().SetRangeUser(100,700)

tf1_dt_vs_E_data = TF1("tf1_dt_vs_E_data","sqrt([0]/(x*x)+[1])", 59.0, 700.0)
tf1_dt_vs_E_data.SetLineColor(kBlue)
tf1_dt_vs_E_data.SetParameters(200.0, 300.0*300.0)
gr_E_sigma_dt_data.Fit("tf1_dt_vs_E_data","","",59.0, 700.0)
fit_dt_a_data = tf1_dt_vs_E_data.GetParameter(0)
fit_dt_b_data = tf1_dt_vs_E_data.GetParameter(1)

gr_E_sigma_dt_MC  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_dt_MC), np.array(ex_E), np.array(ey_E_sigma_dt_MC))
gr_E_sigma_dt_MC.SetMarkerColor(kRed)
gr_E_sigma_dt_MC.SetLineColor(kRed)
gr_E_sigma_dt_MC.SetLineWidth(2)
gr_E_sigma_dt_MC.Draw("Psame")


gr_E_sigma_dt_MC_corr  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_dt_MC_corr), np.array(ex_E), np.array(ey_E_sigma_dt_MC_corr))
gr_E_sigma_dt_MC_corr.SetMarkerColor(kRed)
gr_E_sigma_dt_MC_corr.SetLineColor(kRed)
gr_E_sigma_dt_MC_corr.SetLineWidth(2)
#gr_E_sigma_dt_MC_corr.Draw("Psame")


tf1_dt_vs_E_MC = TF1("tf1_dt_vs_E_MC","sqrt([0]/(x*x)+[1])", 59.0, 700.0)
tf1_dt_vs_E_MC.SetLineColor(kRed)
tf1_dt_vs_E_MC.SetParameters(200.0, 130.0*130.0)
gr_E_sigma_dt_MC.Fit("tf1_dt_vs_E_MC","","",59.0, 700.0)
fit_dt_a_MC = tf1_dt_vs_E_MC.GetParameter(0)
fit_dt_b_MC = tf1_dt_vs_E_MC.GetParameter(1)


gr_E_sigma_dt_diff  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_dt_diff), np.array(ex_E), np.array(ey_E_sigma_dt_diff))
gr_E_sigma_dt_diff.SetMarkerColor(kBlack)
gr_E_sigma_dt_diff.SetLineColor(kBlack)
gr_E_sigma_dt_diff.SetLineWidth(2)
gr_E_sigma_dt_diff.Draw("Psame")

gr_E_sigma_dt_diff_corr  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_dt_diff_corr), np.array(ex_E), np.array(ey_E_sigma_dt_diff_corr))
gr_E_sigma_dt_diff_corr.SetMarkerColor(kBlack)
gr_E_sigma_dt_diff_corr.SetLineColor(kBlack)
gr_E_sigma_dt_diff_corr.SetLineWidth(2)
#gr_E_sigma_dt_diff_corr.Draw("Psame")

leg_sigma_dt = TLegend(0.18,0.75,0.93,0.89)
leg_sigma_dt.SetNColumns(3)
leg_sigma_dt.SetBorderSize(0)
leg_sigma_dt.SetTextSize(0.03)
leg_sigma_dt.SetLineColor(1)
leg_sigma_dt.SetLineStyle(1)
leg_sigma_dt.SetLineWidth(1)
leg_sigma_dt.SetFillColor(0)
leg_sigma_dt.SetFillStyle(1001)
leg_sigma_dt.AddEntry(gr_E_sigma_dt_data, "data", "lep")
leg_sigma_dt.AddEntry(gr_E_sigma_dt_MC, "MC", "lep")
leg_sigma_dt.AddEntry(gr_E_sigma_dt_diff, "#Delta(data, MC)", "lep")
#leg_sigma_dt.AddEntry(gr_E_sigma_dt_MC_corr, "MC corr.", "lep")
leg_sigma_dt.Draw()


leg_fit_dt_data = TLegend(0.42,0.615,0.93,0.715)
leg_fit_dt_data.SetNColumns(3)
leg_fit_dt_data.SetBorderSize(0)
leg_fit_dt_data.SetTextSize(0.035)
leg_fit_dt_data.SetTextColor(kBlue)
leg_fit_dt_data.SetLineColor(1)
leg_fit_dt_data.SetLineStyle(1)
leg_fit_dt_data.SetLineWidth(1)
#leg_fit_dt_data.SetFillColor(0)
leg_fit_dt_data.SetFillStyle(0)
fit_ab_data = "data:  #sigma = #frac{"+ "%.1f" % np.sqrt(np.abs(fit_dt_a_data))+"}{E^{e}} #oplus #sqrt{2} #times "+"%.1f" % np.sqrt(np.abs(fit_dt_b_data)/2.0)
leg_fit_dt_data.AddEntry(gr_E_sigma_dt_data, fit_ab_data , "")
leg_fit_dt_data.Draw()

leg_fit_dt_MC = TLegend(0.42,0.315,0.93,0.415)
leg_fit_dt_MC.SetNColumns(3)
leg_fit_dt_MC.SetBorderSize(0)
leg_fit_dt_MC.SetTextSize(0.035)
leg_fit_dt_MC.SetTextColor(kRed)
leg_fit_dt_MC.SetLineColor(1)
leg_fit_dt_MC.SetLineStyle(1)
leg_fit_dt_MC.SetLineWidth(1)
#leg_fit_dt_MC.SetFillColor(0)
leg_fit_dt_MC.SetFillStyle(0)
fit_ab_MC = "MC:  #sigma = #frac{"+ "%.1f" % np.sqrt(np.abs(fit_dt_a_MC))+"}{E^{e}} #oplus #sqrt{2} #times "+"%.1f" % np.sqrt(np.abs(fit_dt_b_MC)/2.0)
leg_fit_dt_MC.AddEntry(gr_E_sigma_dt_MC, fit_ab_MC , "")
leg_fit_dt_MC.Draw()

drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_E_Data_vs_MC_2016_noCorr.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_E_Data_vs_MC_2016_noCorr.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_E_Data_vs_MC_2016_noCorr.C")
gr_E_sigma_dt_data.Draw("AP")
gr_E_sigma_dt_MC_corr.Draw("Psame")
gr_E_sigma_dt_diff_corr.Draw("Psame")
leg_sigma_dt.Draw()
drawCMS(myC, 13, lumi)
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_E_Data_vs_MC_2016_Corr.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_E_Data_vs_MC_2016_Corr.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_E_Data_vs_MC_2016_Corr.C")



file_plot_dt = TFile(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_E_Data_vs_MC_2016.root", "RECREATE")
gr_E_sigma_dt_data.Write("gr_data")
gr_E_sigma_dt_MC.Write("gr_MC")
gr_E_sigma_dt_MC_corr.Write("gr_MC_corr")
gr_E_sigma_dt_diff.Write("gr_diff")
gr_E_sigma_dt_diff_corr.Write("gr_diff_corr")
file_plot_dt.Close()


gr_E_sigma_time_data  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_time_data), np.array(ex_E), np.array(ey_E_sigma_time_data))
gr_E_sigma_time_data.Draw("AP")
gr_E_sigma_time_data.SetMarkerColor(kBlue)
gr_E_sigma_time_data.SetLineColor(kBlue)
gr_E_sigma_time_data.SetLineWidth(2)
gr_E_sigma_time_data.SetTitle("")
gr_E_sigma_time_data.GetXaxis().SetTitle("E^{e} [GeV]")
gr_E_sigma_time_data.GetYaxis().SetTitle("#sigma_{t} [ps]")
gr_E_sigma_time_data.GetXaxis().SetTitleSize( axisTitleSize )
gr_E_sigma_time_data.GetXaxis().SetTitleOffset( axisTitleOffset )
gr_E_sigma_time_data.GetYaxis().SetTitleSize( axisTitleSize )
gr_E_sigma_time_data.GetYaxis().SetTitleOffset( axisTitleOffset +0.18 )
gr_E_sigma_time_data.GetYaxis().SetRangeUser(100,500)
gr_E_sigma_time_data.GetXaxis().SetRangeUser(70,1000)

tf1_time_vs_E_data = TF1("tf1_time_vs_E_data","sqrt([0]/(x*x)+[1])", 90.0, 700.0)
tf1_time_vs_E_data.SetLineColor(kBlue)
tf1_time_vs_E_data.SetParameters(200.0, 300.0*300.0)
gr_E_sigma_time_data.Fit("tf1_time_vs_E_data","","",90.0, 700.0)
fit_time_a_data = tf1_time_vs_E_data.GetParameter(0)
fit_time_b_data = tf1_time_vs_E_data.GetParameter(1)

gr_E_sigma_time_MC  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_time_MC), np.array(ex_E), np.array(ey_E_sigma_time_MC))
gr_E_sigma_time_MC.SetMarkerColor(kRed)
gr_E_sigma_time_MC.SetLineColor(kRed)
gr_E_sigma_time_MC.SetLineWidth(2)
gr_E_sigma_time_MC.Draw("Psame")


gr_E_sigma_time_MC_corr  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_time_MC_corr), np.array(ex_E), np.array(ey_E_sigma_time_MC_corr))
gr_E_sigma_time_MC_corr.SetMarkerColor(kViolet)
gr_E_sigma_time_MC_corr.SetLineColor(kViolet)
gr_E_sigma_time_MC_corr.SetLineWidth(2)
#gr_E_sigma_time_MC_corr.Draw("Psame")


tf1_time_vs_E_MC = TF1("tf1_time_vs_E_MC","sqrt([0]/(x*x)+[1])", 59.0, 700.0)
tf1_time_vs_E_MC.SetLineColor(kRed)
tf1_time_vs_E_MC.SetParameters(200.0, 130.0*130.0)
gr_E_sigma_time_MC.Fit("tf1_time_vs_E_MC","","",59.0, 700.0)
fit_time_a_MC = tf1_time_vs_E_MC.GetParameter(0)
fit_time_b_MC = tf1_time_vs_E_MC.GetParameter(1)


gr_E_sigma_time_diff  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_time_diff), np.array(ex_E), np.array(ey_E_sigma_time_diff))
gr_E_sigma_time_diff.SetMarkerColor(kBlack)
gr_E_sigma_time_diff.SetLineColor(kBlack)
gr_E_sigma_time_diff.SetLineWidth(2)
gr_E_sigma_time_diff.Draw("Psame")

gr_E_sigma_time_diff_corr  =  TGraphErrors(N_E_points, np.array(x_E), np.array(y_E_sigma_time_diff_corr), np.array(ex_E), np.array(ey_E_sigma_time_diff_corr))
gr_E_sigma_time_diff_corr.SetMarkerColor(kBlack)
gr_E_sigma_time_diff_corr.SetLineColor(kBlack)
gr_E_sigma_time_diff_corr.SetLineWidth(2)
#gr_E_sigma_time_diff_corr.Draw("Psame")

leg_sigma_time = TLegend(0.18,0.75,0.93,0.89)
leg_sigma_time.SetNColumns(3)
leg_sigma_time.SetBorderSize(0)
leg_sigma_time.SetTextSize(0.03)
leg_sigma_time.SetLineColor(1)
leg_sigma_time.SetLineStyle(1)
leg_sigma_time.SetLineWidth(1)
leg_sigma_time.SetFillColor(0)
leg_sigma_time.SetFillStyle(1001)
leg_sigma_time.AddEntry(gr_E_sigma_time_data, "data", "lep")
leg_sigma_time.AddEntry(gr_E_sigma_time_MC, "MC", "lep")
leg_sigma_time.AddEntry(gr_E_sigma_time_diff, "#Delta(data, MC)", "lep")
#leg_sigma_time.AddEntry(gr_E_sigma_time_MC_corr, "MC corr.", "lep")
leg_sigma_time.Draw()


leg_fit_time_data = TLegend(0.42,0.615,0.93,0.715)
leg_fit_time_data.SetNColumns(3)
leg_fit_time_data.SetBorderSize(0)
leg_fit_time_data.SetTextSize(0.035)
leg_fit_time_data.SetTextColor(kBlue)
leg_fit_time_data.SetLineColor(1)
leg_fit_time_data.SetLineStyle(1)
leg_fit_time_data.SetLineWidth(1)
#leg_fit_time_data.SetFillColor(0)
leg_fit_time_data.SetFillStyle(0)
fit_ab_data = "data:  #sigma = #frac{"+ "%.1f" % np.sqrt(np.abs(fit_time_a_data))+"}{E^{e}} #oplus #sqrt{2} #times "+"%.1f" % np.sqrt(np.abs(fit_time_b_data)/2.0)
leg_fit_time_data.AddEntry(gr_E_sigma_time_data, fit_ab_data , "")
#leg_fit_time_data.Draw()

leg_fit_time_MC = TLegend(0.42,0.315,0.93,0.415)
leg_fit_time_MC.SetNColumns(3)
leg_fit_time_MC.SetBorderSize(0)
leg_fit_time_MC.SetTextSize(0.035)
leg_fit_time_MC.SetTextColor(kRed)
leg_fit_time_MC.SetLineColor(1)
leg_fit_time_MC.SetLineStyle(1)
leg_fit_time_MC.SetLineWidth(1)
#leg_fit_time_MC.SetFillColor(0)
leg_fit_time_MC.SetFillStyle(0)
fit_ab_MC = "MC:  #sigma = #frac{"+ "%.1f" % np.sqrt(np.abs(fit_time_a_MC))+"}{E^{e}} #oplus #sqrt{2} #times "+"%.1f" % np.sqrt(np.abs(fit_time_b_MC)/2.0)
leg_fit_time_MC.AddEntry(gr_E_sigma_time_MC, fit_ab_MC , "")
#leg_fit_time_MC.Draw()

drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_time_vs_E_Data_vs_MC_2016_noCorr.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_time_vs_E_Data_vs_MC_2016_noCorr.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_time_vs_E_Data_vs_MC_2016_noCorr.C")

gr_E_sigma_time_data.Draw("AP")
gr_E_sigma_time_data.GetYaxis().SetRangeUser(0,600)
gr_E_sigma_time_MC_corr.Draw("Psame")
gr_E_sigma_time_diff_corr.Draw("Psame")
leg_sigma_time.Draw()
drawCMS(myC, 13, lumi)
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_time_vs_E_Data_vs_MC_2016_Corr.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_time_vs_E_Data_vs_MC_2016_Corr.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_time_vs_E_Data_vs_MC_2016_Corr.C")
