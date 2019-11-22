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

leftMargin   = 0.15
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

file_MC = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/MC2016_all.root")
tree_MC = file_MC.Get("ZeeTiming")

myC = TCanvas( "myC", "myC", 0, 0, 700, 600 )
myC.Range(1.478223,-1.31174,3.682881,0.1140644)
myC.SetFillColor(0)
myC.SetBorderMode(0)
myC.SetBorderSize(2)
myC.SetLogy(1)
myC.SetGridx()
myC.SetGridy()
myC.SetLeftMargin(0.18)
myC.SetRightMargin(0.15)
myC.SetTopMargin(0.08)
myC.SetFrameFillStyle(0)
myC.SetFrameBorderMode(0)
myC.SetFrameFillStyle(0)
myC.SetFrameBorderMode(0)

N_Eeff_points = 9
Eeff_divide = [150.0, 175.0, 225.0, 275.0, 325.0, 375.0, 475.0, 600.0, 750.0, 1700.0]

x_Eeff = np.zeros(N_Eeff_points)
ex_Eeff = np.zeros(N_Eeff_points)
y_Eeff_mean_data = np.zeros(N_Eeff_points)
y_Eeff_mean_MC = np.zeros(N_Eeff_points)
y_Eeff_mean_diff = np.zeros(N_Eeff_points)
y_Eeff_sigma_dt_data = np.zeros(N_Eeff_points)
y_Eeff_sigma_dt_MC = np.zeros(N_Eeff_points)
y_Eeff_sigma_dt_diff = np.zeros(N_Eeff_points)


ey_Eeff_mean_data = np.zeros(N_Eeff_points)
ey_Eeff_mean_MC = np.zeros(N_Eeff_points)
ey_Eeff_mean_diff = np.zeros(N_Eeff_points)

ey_Eeff_sigma_dt_data = np.zeros(N_Eeff_points)
ey_Eeff_sigma_dt_MC = np.zeros(N_Eeff_points)
ey_Eeff_sigma_dt_diff = np.zeros(N_Eeff_points)



for i in range(0, N_Eeff_points):
	x_Eeff[i] = 0.5*(Eeff_divide[i+1]+Eeff_divide[i])
	ex_Eeff[i] = 0.5*(Eeff_divide[i+1]-Eeff_divide[i])
	Eeff_low_this = Eeff_divide[i]
	Eeff_high_this = Eeff_divide[i+1]
	cut_2e_this = cut+" && ele1seedE < 120 && ele2seedE<120 && 25.31*(ele1seedE/seed1_pedestal)*(ele2seedE/seed2_pedestal)/sqrt((ele1seedE/seed1_pedestal)*(ele1seedE/seed1_pedestal)+(ele2seedE/seed2_pedestal)*(ele2seedE/seed2_pedestal)) > "+str(Eeff_low_this)+" && 25.31*(ele1seedE/seed1_pedestal)*(ele2seedE/seed2_pedestal)/sqrt((ele1seedE/seed1_pedestal)*(ele1seedE/seed1_pedestal)+(ele2seedE/seed2_pedestal)*(ele2seedE/seed2_pedestal)) < "+str(Eeff_high_this)
	cut_2e_this_MC = cut+" && 16.18*(ele1seedE/seed1_pedestal)*(ele2seedE/seed2_pedestal)/sqrt((ele1seedE/seed1_pedestal)*(ele1seedE/seed1_pedestal)+(ele2seedE/seed2_pedestal)*(ele2seedE/seed2_pedestal)) > "+str(Eeff_low_this)+" && 16.18*(ele1seedE/seed1_pedestal)*(ele2seedE/seed2_pedestal)/sqrt((ele1seedE/seed1_pedestal)*(ele1seedE/seed1_pedestal)+(ele2seedE/seed2_pedestal)*(ele2seedE/seed2_pedestal)) < "+str(Eeff_high_this)

	hist_2e_this_data = TH1F("hist_2e_this_data_"+str(i),"hist_2e_this_data_"+str(i), 60, -1.5, 1.5)
	tree_data.Draw("t1_seed-t2_seed>>hist_2e_this_data_"+str(i), cut_2e_this)
	hist_2e_this_data.Draw()
	result_2e_this_data = singGausFit(hist_2e_this_data)#, -1.5, 1.5, 0.2, 0.4) 
	myC.SaveAs(outputDir+"/ZeeTiming/style_plots/fits/iEeffFit_Zee_"+str(i)+"_dt_data.png")
	y_Eeff_sigma_dt_data[i] = result_2e_this_data[2]
	ey_Eeff_sigma_dt_data[i] = result_2e_this_data[3]


	hist_2e_this_MC = TH1F("hist_2e_this_MC_"+str(i),"hist_2e_this_MC_"+str(i), 60, -1.5, 1.5)
	tree_MC.Draw("t1_seed-t2_seed>>hist_2e_this_MC_"+str(i),  "(weight*pileupWeight) * " + cut_2e_this_MC)
	hist_2e_this_MC.Draw()
	result_2e_this_MC = singGausFit(hist_2e_this_MC)#, -1.0, 1.0, 0.15, 0.30) 
	myC.SaveAs(outputDir+"/ZeeTiming/style_plots/fits/iEeffFit_Zee_"+str(i)+"_dt_MC.png")
	y_Eeff_sigma_dt_MC[i] = result_2e_this_MC[2]
	ey_Eeff_sigma_dt_MC[i] = result_2e_this_MC[3]

	y_Eeff_mean_diff[i] = y_Eeff_mean_data[i] -  y_Eeff_mean_MC[i]
	ey_Eeff_mean_diff[i] = np.sqrt(ey_Eeff_mean_data[i]*ey_Eeff_mean_data[i] + ey_Eeff_mean_MC[i]*ey_Eeff_mean_MC[i])
	y_Eeff_sigma_dt_diff[i] = np.sqrt(y_Eeff_sigma_dt_data[i]*y_Eeff_sigma_dt_data[i] -  y_Eeff_sigma_dt_MC[i]*y_Eeff_sigma_dt_MC[i])
	ey_Eeff_sigma_dt_diff[i] = np.sqrt(4.0*y_Eeff_sigma_dt_data[i]*y_Eeff_sigma_dt_data[i]*ey_Eeff_sigma_dt_data[i]*ey_Eeff_sigma_dt_data[i]+4.0*y_Eeff_sigma_dt_MC[i]*y_Eeff_sigma_dt_MC[i]*ey_Eeff_sigma_dt_MC[i]*ey_Eeff_sigma_dt_MC[i])/(2.0*y_Eeff_sigma_dt_diff[i])



print "y_Eeff_sigma_dt_data:"
print y_Eeff_sigma_dt_data
print "ey_Eeff_sigma_dt_data:"
print ey_Eeff_sigma_dt_data

print "y_Eeff_sigma_dt_MC:"
print y_Eeff_sigma_dt_MC
print "ey_Eeff_sigma_dt_MC:"
print ey_Eeff_sigma_dt_MC


print "y_Eeff_sigma_dt_diff:"
print y_Eeff_sigma_dt_diff
print "ey_Eeff_sigma_dt_diff:"
print ey_Eeff_sigma_dt_diff


gStyle.SetOptFit(0)
myC.SetGridy(1)
myC.SetGridx(1)
myC.SetLogx(1)
myC.SetLogy(1)

gr_Eeff_sigma_dt_data  =  TGraphErrors(N_Eeff_points, np.array(x_Eeff), np.array(y_Eeff_sigma_dt_data), np.array(ex_Eeff), np.array(ey_Eeff_sigma_dt_data))
gr_Eeff_sigma_dt_data.Draw("AEPZ")
gr_Eeff_sigma_dt_data.SetMarkerColor(kRed)
gr_Eeff_sigma_dt_data.SetLineColor(kRed)
gr_Eeff_sigma_dt_data.SetLineWidth(1)
gr_Eeff_sigma_dt_data.SetMarkerStyle(20)
gr_Eeff_sigma_dt_data.SetMarkerSize(0.6)
gr_Eeff_sigma_dt_data.SetTitle("")
gr_Eeff_sigma_dt_data.GetXaxis().SetTitle("A_{eff}/#sigma_{n}")
gr_Eeff_sigma_dt_data.GetXaxis().SetNdivisions(505)
gr_Eeff_sigma_dt_data.GetXaxis().SetTitleSize( 0.035 )
gr_Eeff_sigma_dt_data.GetXaxis().SetTitleOffset( 1.0 )
gr_Eeff_sigma_dt_data.GetXaxis().SetTitleFont( 42 )
gr_Eeff_sigma_dt_data.GetXaxis().SetLabelFont( 42 )
gr_Eeff_sigma_dt_data.GetXaxis().SetLabelOffset( 0.007 )
gr_Eeff_sigma_dt_data.GetYaxis().SetTitle("#sigma(#Deltat) (ns)")
gr_Eeff_sigma_dt_data.GetYaxis().SetTitleSize( 0.035 )
gr_Eeff_sigma_dt_data.GetYaxis().SetTitleOffset( 1.0 )
gr_Eeff_sigma_dt_data.GetYaxis().SetLabelFont( 42 )
gr_Eeff_sigma_dt_data.GetYaxis().SetTitleFont( 42 )
gr_Eeff_sigma_dt_data.GetYaxis().SetLabelOffset( 0.007 )
gr_Eeff_sigma_dt_data.GetYaxis().SetRangeUser(0.07,1.00)
gr_Eeff_sigma_dt_data.GetXaxis().SetLimits(99.,2250.)

tf1_dt_vs_Eeff_data = TF1("tf1_dt_vs_Eeff_data","sqrt([0]/(x*x)+[1])", 100.0, 2250.0)
tf1_dt_vs_Eeff_data.SetLineColor(kBlack)
tf1_dt_vs_Eeff_data.SetLineWidth(2)
tf1_dt_vs_Eeff_data.SetParameters(50.0*50.0, 0.3*0.3)
gr_Eeff_sigma_dt_data.Fit("tf1_dt_vs_Eeff_data","","",150.0, 2250.0)
fit_dt_a_data = tf1_dt_vs_Eeff_data.GetParameter(0)
efit_dt_a_data = tf1_dt_vs_Eeff_data.GetParError(0)
fit_dt_b_data = tf1_dt_vs_Eeff_data.GetParameter(1)
efit_dt_b_data = tf1_dt_vs_Eeff_data.GetParError(1)
tf1_dt_vs_Eeff_data.Draw("same")

gr_Eeff_sigma_dt_MC  =  TGraphErrors(N_Eeff_points, np.array(x_Eeff), np.array(y_Eeff_sigma_dt_MC), np.array(ex_Eeff), np.array(ey_Eeff_sigma_dt_MC))
gr_Eeff_sigma_dt_MC.SetMarkerColor(kBlue)
gr_Eeff_sigma_dt_MC.SetMarkerStyle(21)
gr_Eeff_sigma_dt_MC.SetLineColor(kBlue)
gr_Eeff_sigma_dt_MC.SetLineWidth(1)
gr_Eeff_sigma_dt_MC.Draw("EPZsame")


tf1_dt_vs_Eeff_MC = TF1("tf1_dt_vs_Eeff_MC","sqrt([0]/(x*x)+[1])", 100.0, 2250.0)
tf1_dt_vs_Eeff_MC.SetLineColor(kBlack)
tf1_dt_vs_Eeff_MC.SetLineWidth(2)
tf1_dt_vs_Eeff_MC.SetParameters(50.0*50.0, 0.1*0.1)
gr_Eeff_sigma_dt_MC.Fit("tf1_dt_vs_Eeff_MC","","",150.0, 2250.0)
fit_dt_a_MC = tf1_dt_vs_Eeff_MC.GetParameter(0)
efit_dt_a_MC = tf1_dt_vs_Eeff_MC.GetParError(0)
fit_dt_b_MC = tf1_dt_vs_Eeff_MC.GetParameter(1)
efit_dt_b_MC = tf1_dt_vs_Eeff_MC.GetParError(1)
tf1_dt_vs_Eeff_MC.Draw("same")



leg = TLegend(0.215,0.715,0.415,0.80)
leg.SetFillColorAlpha(0,0)
leg.SetBorderSize(0)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetFillStyle(1001)
leg.SetTextFont(42)
leg.AddEntry(gr_Eeff_sigma_dt_data,"Data","epl")
leg.AddEntry(gr_Eeff_sigma_dt_MC,"Simulation","epl")
leg.Draw("same")

N_data=np.sqrt(np.abs(fit_dt_a_data))
eN_data=np.abs(efit_dt_a_data)/(2.0*np.sqrt(np.abs(fit_dt_a_data)))
C_data=np.sqrt(np.abs(fit_dt_b_data)/2.0)
eC_data=np.abs(efit_dt_b_data)/(4.0*np.sqrt(np.abs(fit_dt_b_data)/2.0))

N_MC=np.sqrt(np.abs(fit_dt_a_MC))
eN_MC=np.abs(efit_dt_a_MC)/(2.0*np.sqrt(np.abs(fit_dt_a_MC)))
C_MC=np.sqrt(np.abs(fit_dt_b_MC)/2.0)
eC_MC=np.abs(efit_dt_b_MC)/(4.0*np.sqrt(np.abs(fit_dt_b_MC)/2.0))


form_pave = TPaveText(0.55,0.73,0.8,0.85,"NDC")
form_pave.SetFillColorAlpha(0,0)
form_pave.SetTextFont(42)
form_pave.SetTextAlign(11)
form_pave.AddText("#sigma(#Deltat)=#frac{N}{A_{eff}/#sigma_{n}} #oplus #sqrt{2}C")
form_pave.Draw("same")

fit_pave = TPaveText(0.55,0.565,0.8,0.735,"NDC")
fit_pave.SetFillColorAlpha(0,0)
fit_pave.SetTextAlign(11)
fit_pave.SetTextFont(42)
fit_pave.AddText("N^{Data} = "+"%.1f" % N_data + " #pm " + "%.1f" % eN_data +" ns")
fit_pave.AddText("C^{Data} = "+"%.3f" % C_data + " #pm " + "%.3f" % eC_data + " ns")
fit_pave.AddText("N^{Sim} = "+"%.1f" % N_MC + " #pm " + "%.1f" % eN_MC +" ns")
fit_pave.AddText("C^{Sim} = "+"%.3f" % C_MC + " #pm " + "%.3f" % eC_MC + " ns")
fit_pave.Draw("same")

gaxis = TGaxis(100,1,2250,1,100*0.0618, 2250*0.0618,505,"-G")
gaxis.SetLabelOffset(0.005)
gaxis.SetLabelSize(0.035)
gaxis.SetTickSize(0.03)
gaxis.SetGridLength(0)
gaxis.SetTitleOffset(1)
gaxis.SetTitleSize(0.035)
gaxis.SetTitleColor(1)
gaxis.SetTitleFont(42)
gaxis.SetLabelFont(42)
gaxis.SetTitle("E (GeV)")
gaxis.SetNoExponent(1)
gaxis.Draw("same")
myC.Modified()
myC.cd()

cms_pave = TPaveText(0.20,0.855,0.3,0.895,"NDC")
cms_pave.SetFillColorAlpha(0,0)
cms_pave.SetTextFont(61)
cms_pave.AddText("CMS")
cms_pave.Draw("same")

prelim_pave = TPaveText(0.25,0.855,0.45,0.89,"NDC")
prelim_pave.SetFillColorAlpha(0,0)
prelim_pave.SetTextFont(52)
prelim_pave.AddText("Preliminary")
prelim_pave.Draw("same")

lumi_pave = TPaveText(0.218,0.80,0.478,0.86,"NDC")
lumi_pave.SetFillColorAlpha(0,0)
lumi_pave.SetTextFont(42)
lumi_pave.AddText("2016: 35.9 fb^{-1} (13 TeV)")
lumi_pave.Draw("same")

label_pave = TPaveText(0.6,0.855,0.8,0.895,"NDC")
label_pave.SetFillColorAlpha(0,0)
label_pave.SetTextFont(42)
label_pave.AddText("EB Z Study")
label_pave.Draw("same")

myC.SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_Zee_dt_vs_Eeff_sigma_Data_vs_MC.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_Zee_dt_vs_Eeff_sigma_Data_vs_MC.png")
myC.SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_Zee_dt_vs_Eeff_sigma_Data_vs_MC.C")

gr_Eeff_sigma_dt_data.Draw("AEPZ")
tf1_dt_vs_Eeff_data.Draw("same")
gr_Eeff_sigma_dt_data.SetMarkerColor(kBlack)
gr_Eeff_sigma_dt_data.SetLineColor(kBlack)
tf1_dt_vs_Eeff_data.SetLineColor(kRed+1)
cms_pave.Draw("same")
prelim_pave.Draw("same")
lumi_pave.Draw("same")
label_pave.Draw("same")
gaxis.Draw()
form_pave.Draw("same")
fit_pave2 = TPaveText(0.55,0.650,0.8,0.735,"NDC")
fit_pave2.SetFillColorAlpha(0,0)
fit_pave2.SetTextAlign(11)
fit_pave2.SetTextFont(42)
fit_pave2.AddText("N = "+"%.1f" % N_data + " #pm " + "%.1f" % eN_data +" ns")
fit_pave2.AddText("C = "+"%.3f" % C_data + " #pm " + "%.3f" % eC_data + " ns")
fit_pave2.Draw("same")

myC.SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_Zee_dt_vs_Eeff_sigma_DataOnly.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_Zee_dt_vs_Eeff_sigma_DataOnly.png")
myC.SaveAs(outputDir+"/ZeeTiming/style_plots/TimingReso_Zee_dt_vs_Eeff_sigma_DataOnly.C")
