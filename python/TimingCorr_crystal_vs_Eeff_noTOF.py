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
	x_mean=hist.GetMean()
	x_stddev=hist.GetStdDev()
	x_min=x_mean - 3.5*x_stddev
	x_max=x_mean + 3.5*x_stddev
	sig_small = 0.7*x_stddev
	sig_big = 1.0*x_stddev
	tf1_doubGaus = TF1("tf1_doubGaus","gaus(0)+gaus(3)", x_min,x_max)
	#tf1_doubGaus.SetParameters(0.5*hist.Integral(),0.5*(x_min+x_max),0.2*(x_max-x_min), 0.5*hist.Integral(),0.5*(x_min+x_max),0.1*(x_max-x_min))
	tf1_doubGaus.SetParameters(0.6*hist.Integral(),0.5*(x_min+x_max),sig_small, 0.4*hist.Integral(),0.5*(x_min+x_max),sig_big)
	tf1_doubGaus.SetParLimits(0,0.1,hist.Integral())
	tf1_doubGaus.SetParLimits(3,0.1,hist.Integral())
	tf1_doubGaus.SetParLimits(2,0.0500,0.500)
	tf1_doubGaus.SetParLimits(5,0.0500,0.500)
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
#cut = "mass>60 && mass <150 && ele1IsEB && ele2IsEB"
#cut = "ele1IsEB && ele1subseedE/ele1seedE > 0.7 && ele1seedE>10.0 && ele1subseedE>10.0"
cut = "ele1IsEB && ele1seedE/ele1subseedE < 1.2"

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

########correction vs. pt##########
N_Eeff_points = 10
#Eeff_divide = [30, 34.0, 38.0, 42.0, 46.0, 50.0, 54.0, 58.0, 62.0, 66.0, 70.0, 74.0, 77.0, 81.0, 85.0, 91.0, 100.0, 115.0, 140.0, 200.0]
#Eeff_divide_0 = [10, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 57.0, 70.0, 120.0]
#Eeff_divide = [a*25.0 for a in Eeff_divide_0]
Eeff_divide = [200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 600.0, 700.0, 900.0, 2000.0]

x_Eeff = np.zeros(N_Eeff_points)
ex_Eeff = np.zeros(N_Eeff_points)
y_Eeff_mean_data = np.zeros(N_Eeff_points)
y_Eeff_mean_MC = np.zeros(N_Eeff_points)
y_Eeff_mean_MC_corr = np.zeros(N_Eeff_points)
y_Eeff_mean_diff = np.zeros(N_Eeff_points)
y_Eeff_sigma_dt_data = np.zeros(N_Eeff_points)
y_Eeff_sigma_dt_MC = np.zeros(N_Eeff_points)
y_Eeff_sigma_dt_MC_corr= np.zeros(N_Eeff_points)
y_Eeff_sigma_dt_diff = np.zeros(N_Eeff_points)


ey_Eeff_mean_data = np.zeros(N_Eeff_points)
ey_Eeff_mean_MC = np.zeros(N_Eeff_points)
ey_Eeff_mean_MC_corr = np.zeros(N_Eeff_points)
ey_Eeff_mean_diff = np.zeros(N_Eeff_points)

ey_Eeff_sigma_dt_data = np.zeros(N_Eeff_points)
ey_Eeff_sigma_dt_MC = np.zeros(N_Eeff_points)
ey_Eeff_sigma_dt_MC_corr = np.zeros(N_Eeff_points)
ey_Eeff_sigma_dt_diff = np.zeros(N_Eeff_points)



for i in range(0, N_Eeff_points):
	x_Eeff[i] = 0.5*(Eeff_divide[i+1]+Eeff_divide[i])
	ex_Eeff[i] = 0.5*(Eeff_divide[i+1]-Eeff_divide[i])
	Eeff_low_this = Eeff_divide[i]
	Eeff_high_this = Eeff_divide[i+1]
	cut_2e_this = cut+" && ele1seedE < 120 && ele1subseedE<120 && 25.31*(ele1seedE/seed1_pedestal)*(ele1subseedE/subseed1_pedestal)/sqrt((ele1seedE/seed1_pedestal)*(ele1seedE/seed1_pedestal)+(ele1subseedE/subseed1_pedestal)*(ele1subseedE/subseed1_pedestal)) > "+str(Eeff_low_this)+" && 25.31*(ele1seedE/seed1_pedestal)*(ele1subseedE/subseed1_pedestal)/sqrt((ele1seedE/seed1_pedestal)*(ele1seedE/seed1_pedestal)+(ele1subseedE/subseed1_pedestal)*(ele1subseedE/subseed1_pedestal)) < "+str(Eeff_high_this)
	cut_2e_this_MC = cut+" && 23.81*(ele1seedE/seed1_pedestal)*(ele1subseedE/subseed1_pedestal)/sqrt((ele1seedE/seed1_pedestal)*(ele1seedE/seed1_pedestal)+(ele1subseedE/subseed1_pedestal)*(ele1subseedE/subseed1_pedestal)) > "+str(Eeff_low_this)+" && 23.81*(ele1seedE/seed1_pedestal)*(ele1subseedE/subseed1_pedestal)/sqrt((ele1seedE/seed1_pedestal)*(ele1seedE/seed1_pedestal)+(ele1subseedE/subseed1_pedestal)*(ele1subseedE/subseed1_pedestal)) < "+str(Eeff_high_this)

	hist_2e_this_data = TH1F("hist_2e_this_data_"+str(i),"hist_2e_this_data_"+str(i), 60, -1.5, 1.5)
	tree_data.Draw("t1raw_seed-t1raw_subseed>>hist_2e_this_data_"+str(i), cut_2e_this)
	hist_2e_this_data.Draw()
	result_2e_this_data = doubGausFit(hist_2e_this_data)#, -1.5, 1.5, 0.2, 0.4) 
	myC.SaveAs(outputDir+"/ZeeTiming/iEeffFit_neighboring_xtal_"+str(i)+"_dt_data_noTOF.png")
	y_Eeff_sigma_dt_data[i] = result_2e_this_data[2]
	ey_Eeff_sigma_dt_data[i] = result_2e_this_data[3]


	hist_2e_this_MC = TH1F("hist_2e_this_MC_"+str(i),"hist_2e_this_MC_"+str(i), 60, -1.5, 1.5)
	tree_MC.Draw("t1raw_seed-t1raw_subseed>>hist_2e_this_MC_"+str(i),  "(weight*pileupWeight) * " + cut_2e_this_MC)
	hist_2e_this_MC.Draw()
	result_2e_this_MC = doubGausFit(hist_2e_this_MC)#, -1.0, 1.0, 0.15, 0.30) 
	myC.SaveAs(outputDir+"/ZeeTiming/iEeffFit_neighboring_xtal_"+str(i)+"_dt_MC_noTOF.png")
	y_Eeff_sigma_dt_MC[i] = result_2e_this_MC[2]
	ey_Eeff_sigma_dt_MC[i] = result_2e_this_MC[3]

	y_Eeff_mean_diff[i] = y_Eeff_mean_data[i] -  y_Eeff_mean_MC[i]
	ey_Eeff_mean_diff[i] = np.sqrt(ey_Eeff_mean_data[i]*ey_Eeff_mean_data[i] + ey_Eeff_mean_MC[i]*ey_Eeff_mean_MC[i])
	y_Eeff_sigma_dt_diff[i] = np.sqrt(y_Eeff_sigma_dt_data[i]*y_Eeff_sigma_dt_data[i] -  y_Eeff_sigma_dt_MC[i]*y_Eeff_sigma_dt_MC[i])
	ey_Eeff_sigma_dt_diff[i] = np.sqrt(4.0*y_Eeff_sigma_dt_data[i]*y_Eeff_sigma_dt_data[i]*ey_Eeff_sigma_dt_data[i]*ey_Eeff_sigma_dt_data[i]+4.0*y_Eeff_sigma_dt_MC[i]*y_Eeff_sigma_dt_MC[i]*ey_Eeff_sigma_dt_MC[i]*ey_Eeff_sigma_dt_MC[i])/(2.0*y_Eeff_sigma_dt_diff[i])

	hist_2e_this_MC_corr = TH1F("hist_2e_this_MC_corr_"+str(i),"hist_2e_this_MC_corr_"+str(i), 60, -1.5, 1.5)
	tree_MC.Draw("t1_seed_ShiftToData-t1_subseed_ShiftToData>>hist_2e_this_MC_corr_"+str(i),  "(weight*pileupWeight) * " + cut_2e_this_MC)
	hist_2e_this_MC_corr.Draw()
	result_2e_this_MC_corr = doubGausFit(hist_2e_this_MC_corr)#, -1.0, 1.0, 0.15, 0.30) 
	myC.SaveAs(outputDir+"/ZeeTiming/iEeffFit_neighboring_xtal_"+str(i)+"_dt_MC_corr.png")
	y_Eeff_sigma_dt_MC_corr[i] = result_2e_this_MC_corr[2]
	ey_Eeff_sigma_dt_MC_corr[i] = result_2e_this_MC_corr[3]


print "y_Eeff_sigma_dt_data:"
print y_Eeff_sigma_dt_data
print "ey_Eeff_sigma_dt_data:"
print ey_Eeff_sigma_dt_data

print "y_Eeff_sigma_dt_MC:"
print y_Eeff_sigma_dt_MC
print "ey_Eeff_sigma_dt_MC:"
print ey_Eeff_sigma_dt_MC

print "y_Eeff_sigma_dt_MC_corr:"
print y_Eeff_sigma_dt_MC_corr
print "ey_Eeff_sigma_dt_MC_corr:"
print ey_Eeff_sigma_dt_MC_corr


print "y_Eeff_sigma_dt_diff:"
print y_Eeff_sigma_dt_diff
print "ey_Eeff_sigma_dt_diff:"
print ey_Eeff_sigma_dt_diff


gStyle.SetOptFit(0)
myC.SetGridy(1)
myC.SetGridx(1)
myC.SetLogx(1)

gr_Eeff_sigma_dt_data  =  TGraphErrors(N_Eeff_points, np.array(x_Eeff), np.array(y_Eeff_sigma_dt_data), np.array(ex_Eeff), np.array(ey_Eeff_sigma_dt_data))
gr_Eeff_sigma_dt_data.Draw("AP")
gr_Eeff_sigma_dt_data.SetMarkerColor(kBlue)
gr_Eeff_sigma_dt_data.SetLineColor(kBlue)
gr_Eeff_sigma_dt_data.SetLineWidth(2)
gr_Eeff_sigma_dt_data.SetTitle("")
gr_Eeff_sigma_dt_data.GetXaxis().SetTitle("A_{eff}/#sigma_{n}")
gr_Eeff_sigma_dt_data.GetYaxis().SetTitle("#sigma_{t1-t2} [ns]")
gr_Eeff_sigma_dt_data.GetXaxis().SetTitleSize( axisTitleSize - 0.02 )
gr_Eeff_sigma_dt_data.GetXaxis().SetTitleOffset( axisTitleOffset  + 0.6)
gr_Eeff_sigma_dt_data.GetYaxis().SetTitleSize( axisTitleSize )
gr_Eeff_sigma_dt_data.GetYaxis().SetTitleOffset( axisTitleOffset +0.18 )
gr_Eeff_sigma_dt_data.GetYaxis().SetRangeUser(0.05,0.35)
gr_Eeff_sigma_dt_data.GetXaxis().SetRangeUser(200,2000)
gr_Eeff_sigma_dt_data.GetXaxis().SetMoreLogLabels()

tf1_dt_vs_Eeff_data = TF1("tf1_dt_vs_Eeff_data","sqrt([0]/(x*x)+[1])", 200.0, 2000.0)
tf1_dt_vs_Eeff_data.SetLineColor(kBlue)
tf1_dt_vs_Eeff_data.SetParameters(50.0*50.0, 0.1*0.1)
gr_Eeff_sigma_dt_data.Fit("tf1_dt_vs_Eeff_data","","",200.0, 2000.0)
fit_dt_a_data = tf1_dt_vs_Eeff_data.GetParameter(0)
efit_dt_a_data = tf1_dt_vs_Eeff_data.GetParError(0)
fit_dt_b_data = tf1_dt_vs_Eeff_data.GetParameter(1)
efit_dt_b_data = tf1_dt_vs_Eeff_data.GetParError(1)

gr_Eeff_sigma_dt_MC  =  TGraphErrors(N_Eeff_points, np.array(x_Eeff), np.array(y_Eeff_sigma_dt_MC), np.array(ex_Eeff), np.array(ey_Eeff_sigma_dt_MC))
gr_Eeff_sigma_dt_MC.SetMarkerColor(kRed)
gr_Eeff_sigma_dt_MC.SetLineColor(kRed)
gr_Eeff_sigma_dt_MC.SetLineWidth(2)
gr_Eeff_sigma_dt_MC.Draw("Psame")


gr_Eeff_sigma_dt_MC_corr  =  TGraphErrors(N_Eeff_points, np.array(x_Eeff), np.array(y_Eeff_sigma_dt_MC_corr), np.array(ex_Eeff), np.array(ey_Eeff_sigma_dt_MC_corr))
gr_Eeff_sigma_dt_MC_corr.SetMarkerColor(kRed)
gr_Eeff_sigma_dt_MC_corr.SetLineColor(kRed)
gr_Eeff_sigma_dt_MC_corr.SetLineWidth(2)
#gr_Eeff_sigma_dt_MC_corr.Draw("Psame")


tf1_dt_vs_Eeff_MC = TF1("tf1_dt_vs_Eeff_MC","sqrt([0]/(x*x)+[1])", 200.0, 2000.0)
tf1_dt_vs_Eeff_MC.SetLineColor(kRed)
tf1_dt_vs_Eeff_MC.SetParameters(50.0*50.0, 0.01*0.01)
gr_Eeff_sigma_dt_MC.Fit("tf1_dt_vs_Eeff_MC","","",200.0, 2000.0)
fit_dt_a_MC = tf1_dt_vs_Eeff_MC.GetParameter(0)
efit_dt_a_MC = tf1_dt_vs_Eeff_MC.GetParError(0)
fit_dt_b_MC = tf1_dt_vs_Eeff_MC.GetParameter(1)
efit_dt_b_MC = tf1_dt_vs_Eeff_MC.GetParError(1)


gr_Eeff_sigma_dt_diff  =  TGraphErrors(N_Eeff_points, np.array(x_Eeff), np.array(y_Eeff_sigma_dt_diff), np.array(ex_Eeff), np.array(ey_Eeff_sigma_dt_diff))
gr_Eeff_sigma_dt_diff.SetMarkerColor(kBlack)
gr_Eeff_sigma_dt_diff.SetLineColor(kBlack)
gr_Eeff_sigma_dt_diff.SetLineWidth(2)
#gr_Eeff_sigma_dt_diff.Draw("Psame")


leg_sigma_dt = TLegend(0.18,0.84,0.48,0.90)
leg_sigma_dt.SetNColumns(3)
leg_sigma_dt.SetBorderSize(0)
leg_sigma_dt.SetTextSize(0.03)
leg_sigma_dt.SetLineColor(1)
leg_sigma_dt.SetLineStyle(1)
leg_sigma_dt.SetLineWidth(1)
leg_sigma_dt.SetFillColor(0)
leg_sigma_dt.SetFillStyle(1001)
leg_sigma_dt.AddEntry(gr_Eeff_sigma_dt_data, "data", "lep")
leg_sigma_dt.AddEntry(gr_Eeff_sigma_dt_MC, "MC", "lep")
#leg_sigma_dt.AddEntry(gr_Eeff_sigma_dt_diff, "#Delta(data, MC)", "lep")
#leg_sigma_dt.AddEntry(gr_Eeff_sigma_dt_MC_corr, "MC corr.", "lep")
leg_sigma_dt.Draw()

tlatex = TLatex()
tlatex.SetNDC()
tlatex.SetTextAngle(0)
tlatex.SetTextColor(1)
tlatex.SetTextFont(63)
tlatex.SetTextAlign(11)
tlatex.SetTextSize(25)
tlatex.DrawLatex(0.5, 0.85, "#sigma = #frac{N}{A_{eff}/#sigma_{n}} #oplus #sqrt{2} C")
tlatex.SetTextColor(kBlue)

N_data=np.sqrt(np.abs(fit_dt_a_data))
eN_data=np.abs(efit_dt_a_data)/(2.0*np.sqrt(np.abs(fit_dt_a_data)))
C_data=np.sqrt(np.abs(fit_dt_b_data)/2.0)
eC_data=np.abs(efit_dt_b_data)/(4.0*np.sqrt(np.abs(fit_dt_b_data)/2.0))

N_MC=np.sqrt(np.abs(fit_dt_a_MC))
eN_MC=np.abs(efit_dt_a_MC)/(2.0*np.sqrt(np.abs(fit_dt_a_MC)))
C_MC=np.sqrt(np.abs(fit_dt_b_MC)/2.0)
eC_MC=np.abs(efit_dt_b_MC)/(4.0*np.sqrt(np.abs(fit_dt_b_MC)/2.0))

tlatex.DrawLatex(0.5, 0.78, "N^{data} = "+"%.1f" % N_data + " #pm " + "%.1f" % eN_data +" ns")
tlatex.DrawLatex(0.5, 0.71, "C^{data} = "+"%.3f" % C_data + " #pm " + "%.3f" % eC_data + " ns")
tlatex.SetTextColor(kRed)
tlatex.DrawLatex(0.5, 0.64, "N^{MC} = "+"%.1f" % N_MC + " #pm " + "%.1f" % eN_MC +" ns")
tlatex.DrawLatex(0.5, 0.57, "C^{MC} = "+"%.3f" % C_MC + " #pm " + "%.3f" % eC_MC + " ns")


drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_neighboring_xtals_dt_vs_Eeff_sigma_Data_vs_MC_2016_noTOF.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_neighboring_xtals_dt_vs_Eeff_sigma_Data_vs_MC_2016_noTOF.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_neighboring_xtals_dt_vs_Eeff_sigma_Data_vs_MC_2016_noTOF.C")

gr_Eeff_sigma_dt_data.Draw("AP")
gr_Eeff_sigma_dt_MC_corr.Draw("Psame")

tf1_dt_vs_Eeff_MC_corr = TF1("tf1_dt_vs_Eeff_MC_corr","sqrt([0]/(x*x)+[1])", 200.0, 2000.0)
tf1_dt_vs_Eeff_MC_corr.SetLineColor(kRed)
tf1_dt_vs_Eeff_MC_corr.SetParameters(50.0*50.0, 0.1*0.1)
gr_Eeff_sigma_dt_MC_corr.Fit("tf1_dt_vs_Eeff_MC_corr","","",200.0, 2000.0)
fit_dt_a_MC_corr = tf1_dt_vs_Eeff_MC_corr.GetParameter(0)
efit_dt_a_MC_corr = tf1_dt_vs_Eeff_MC_corr.GetParError(0)
fit_dt_b_MC_corr = tf1_dt_vs_Eeff_MC_corr.GetParameter(1)
efit_dt_b_MC_corr = tf1_dt_vs_Eeff_MC_corr.GetParError(1)


leg_sigma_dt_corr = TLegend(0.18,0.84,0.48,0.90)
leg_sigma_dt_corr.SetNColumns(3)
leg_sigma_dt_corr.SetBorderSize(0)
leg_sigma_dt_corr.SetTextSize(0.03)
leg_sigma_dt_corr.SetLineColor(1)
leg_sigma_dt_corr.SetLineStyle(1)
leg_sigma_dt_corr.SetLineWidth(1)
leg_sigma_dt_corr.SetFillColor(0)
leg_sigma_dt_corr.SetFillStyle(1001)
leg_sigma_dt_corr.AddEntry(gr_Eeff_sigma_dt_data, "data", "lep")
leg_sigma_dt_corr.AddEntry(gr_Eeff_sigma_dt_MC_corr, "MC", "lep")
#leg_sigma_dt_corr.AddEntry(gr_Eeff_sigma_dt_diff, "#Delta(data, MC)", "lep")
#leg_sigma_dt_corr.AddEntry(gr_Eeff_sigma_dt_MC_corr, "MC corr.", "lep")
leg_sigma_dt_corr.Draw()

tlatex_corr = TLatex()
tlatex_corr.SetNDC()
tlatex_corr.SetTextAngle(0)
tlatex_corr.SetTextColor(1)
tlatex_corr.SetTextFont(63)
tlatex_corr.SetTextAlign(11)
tlatex_corr.SetTextSize(25)
tlatex_corr.DrawLatex(0.5, 0.85, "#sigma = #frac{N}{A_{eff}/#sigma_{n}} #oplus #sqrt{2} C")
tlatex_corr.SetTextColor(kBlue)

N_MC_corr=np.sqrt(np.abs(fit_dt_a_MC_corr))
eN_MC_corr=np.abs(efit_dt_a_MC_corr)/(2.0*np.sqrt(np.abs(fit_dt_a_MC_corr)))
C_MC_corr=np.sqrt(np.abs(fit_dt_b_MC_corr)/2.0)
eC_MC_corr=np.abs(efit_dt_b_MC_corr)/(4.0*np.sqrt(np.abs(fit_dt_b_MC_corr)/2.0))

tlatex_corr.DrawLatex(0.5, 0.78, "N^{data} = "+"%.1f" % N_data + " #pm " + "%.1f" % eN_data +" ns")
tlatex_corr.DrawLatex(0.5, 0.71, "C^{data} = "+"%.3f" % C_data + " #pm " + "%.3f" % eC_data + " ns")
tlatex_corr.SetTextColor(kRed)
tlatex_corr.DrawLatex(0.5, 0.64, "N^{MC} = "+"%.1f" % N_MC_corr + " #pm " + "%.1f" % eN_MC_corr +" ns")
tlatex_corr.DrawLatex(0.5, 0.57, "C^{MC} = "+"%.3f" % C_MC_corr + " #pm " + "%.3f" % eC_MC_corr + " ns")


drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_neighboring_xtals_dt_vs_Eeff_sigma_Data_vs_MC_corr_2016_noTOF.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_neighboring_xtals_dt_vs_Eeff_sigma_Data_vs_MC_corr_2016_noTOF.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_neighboring_xtals_dt_vs_Eeff_sigma_Data_vs_MC_corr_2016_noTOF.C")


