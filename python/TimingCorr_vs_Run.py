from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array
from config_noBDT import outputDir
from config_noBDT import lumi

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
rightMargin  = 0.10
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
	sigEff = 1.000*np.abs(tf1_singGaus.GetParameter(2))
	esigEff = 1.000*tf1_singGaus.GetParError(2)
	meanEff = 1.000*tf1_singGaus.GetParameter(1)
	emeanEff = 1.000*tf1_singGaus.GetParError(1)
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
	sigEff = 1.000*np.abs(tf1_singGaus.GetParameter(2))
	esigEff = 1.000*tf1_singGaus.GetParError(2)
	meanEff = 1.000*tf1_singGaus.GetParameter(1)
	emeanEff = 1.000*tf1_singGaus.GetParError(1)
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

	sigEff = 1.000*(N1*s1 + N2*s2) / (N1+N2) 
	esigEff = 1.000* np.sqrt(N1*N1*es1*es1 + N2*N2*es2*es2)/(N1+N2)
	meanEff = 1.000*(N1*u1 + N2*u2) / (N1+N2) 
	emeanEff = 1.000* np.sqrt(N1*N1*eu1*eu1 + N2*N2*eu2*eu2)/(N1+N2)
	
	result = np.array([meanEff,emeanEff,sigEff,esigEff])
	return result

def doubGausFit(hist):
	x_mean = hist.GetMean()
        x_stddev = hist.GetStdDev()
        x_min = x_mean - 3.5*x_stddev
        x_max = x_mean + 3.5*x_stddev
	sig_small = 0.65*x_stddev
	sig_big = 1.0*x_stddev
	tf1_doubGaus = TF1("tf1_doubGaus","gaus(0)+gaus(3)", x_min,x_max)
	#tf1_doubGaus.SetParameters(0.5*hist.Integral(),0.5*(x_min+x_max),0.2*(x_max-x_min), 0.5*hist.Integral(),0.5*(x_min+x_max),0.1*(x_max-x_min))
	tf1_doubGaus.SetParameters(0.6*hist.Integral(),0.5*(x_min+x_max),sig_small, 0.4*hist.Integral(),0.5*(x_min+x_max),sig_big)
	tf1_doubGaus.SetParLimits(0,0.1,hist.Integral())
	tf1_doubGaus.SetParLimits(3,0.1,hist.Integral())
	tf1_doubGaus.SetParLimits(2,0.0850,1.000)
	tf1_doubGaus.SetParLimits(5,0.0850,1.000)
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

	sigEff = 0.0
	esigEff = 0.0
	meanEff = 0.0
	emeanEff = 0.0
	if N1+N2 > 0.0:
		sigEff = 1.000*(N1*s1 + N2*s2) / (N1+N2) 
		esigEff = 1.000* np.sqrt(N1*N1*es1*es1 + N2*N2*es2*es2)/(N1+N2)
		meanEff = 1.000*(N1*u1 + N2*u2) / (N1+N2) 
		emeanEff = 1.000* np.sqrt(N1*N1*eu1*eu1 + N2*N2*eu2*eu2)/(N1+N2)
	
	result = np.array([meanEff,emeanEff,sigEff,esigEff])
	return result



	
####load data
cut = "mass>60 && mass <150 && ele1IsEB && ele2IsEB"

file_data = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/All2016.root")
tree_data = file_data.Get("ZeeTiming")


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

N_Run_points = 100
Run_divide = []
start_run = 273000.0
end_run = 284000.0

for i in range(0, N_Run_points+1):
	Run_divide.append(1.0*(start_run+i*(end_run-start_run)/N_Run_points))

x_Run = np.zeros(N_Run_points)
ex_Run = np.zeros(N_Run_points)
y_Run_mean_data = np.zeros(N_Run_points)
y_Run_sigma_dt_data = np.zeros(N_Run_points)

ey_Run_mean_data = np.zeros(N_Run_points)
ey_Run_sigma_dt_data = np.zeros(N_Run_points)


for i in range(0, N_Run_points):
	x_Run[i] = 0.5*(Run_divide[i+1]+Run_divide[i])
	ex_Run[i] = 0.5*(Run_divide[i+1]-Run_divide[i])
	Run_low_this = Run_divide[i]
	Run_high_this = Run_divide[i+1]
	cut_2e_this = cut+" && ele1seedE < 120 && run > "+str(Run_low_this)+" && run < "+str(Run_high_this)

	hist_2e_this_data = TH1F("hist_2e_this_data_"+str(i),"hist_2e_this_data_"+str(i), 60, -1.5, 1.5)
	tree_data.Draw("t1_seed-t2_seed>>hist_2e_this_data_"+str(i), cut_2e_this)
	hist_2e_this_data.Draw()
	result_2e_this_data = doubGausFit(hist_2e_this_data)#, -1.5, 1.5, 0.2, 0.4) 
	myC.SaveAs(outputDir+"/ZeeTiming/fits/iRunFit_Zee_"+str(i)+"_dt_data.png")
	if result_2e_this_data[3] < 0.05:
		y_Run_sigma_dt_data[i] = result_2e_this_data[2]
		ey_Run_sigma_dt_data[i] = result_2e_this_data[3]
	else:
		y_Run_sigma_dt_data[i] = 0.0
		ey_Run_sigma_dt_data[i] = 0.0


print "y_Run_sigma_dt_data:"
print y_Run_sigma_dt_data
print "ey_Run_sigma_dt_data:"
print ey_Run_sigma_dt_data


gStyle.SetOptFit(0)
myC.SetGridy(1)
myC.SetGridx(1)

gr_Run_sigma_dt_data  =  TGraphErrors(N_Run_points, np.array(x_Run), np.array(y_Run_sigma_dt_data), np.array(ex_Run), np.array(ey_Run_sigma_dt_data))
gr_Run_sigma_dt_data.Draw("AP")
gr_Run_sigma_dt_data.SetMarkerColor(kBlue)
gr_Run_sigma_dt_data.SetMarkerStyle(20)
gr_Run_sigma_dt_data.SetLineColor(kBlue)
gr_Run_sigma_dt_data.SetLineWidth(2)
gr_Run_sigma_dt_data.SetTitle("")
gr_Run_sigma_dt_data.GetXaxis().SetTitle("Run Number")
gr_Run_sigma_dt_data.GetYaxis().SetTitle("#sigma_{t1-t2} [ns]")
gr_Run_sigma_dt_data.GetXaxis().SetTitleSize( axisTitleSize - 0.02 )
gr_Run_sigma_dt_data.GetXaxis().SetTitleOffset( axisTitleOffset  + 0.6)
gr_Run_sigma_dt_data.GetYaxis().SetTitleSize( axisTitleSize )
gr_Run_sigma_dt_data.GetYaxis().SetTitleOffset( axisTitleOffset +0.18 )
gr_Run_sigma_dt_data.GetYaxis().SetRangeUser(0.01,1.0)
gr_Run_sigma_dt_data.GetXaxis().SetRangeUser(start_run,end_run)
gr_Run_sigma_dt_data.GetXaxis().SetMoreLogLabels()
gr_Run_sigma_dt_data.GetYaxis().SetMoreLogLabels()


drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_Run_sigma_Data_2016.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_Run_sigma_Data_2016.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_Run_sigma_Data_2016.C")

file_out = TFile(outputDir+"/ZeeTiming/TimingReso_Zee_dt_vs_Run_sigma_Data_2016.root","RECREATE")
gr_Run_sigma_dt_data.Write("gr_data")
file_out.Close()


