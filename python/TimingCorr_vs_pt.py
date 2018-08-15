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
	sigEff = 1000.0*np.abs(tf1_singGaus.GetParameter(2))
	esigEff = 1000.0*tf1_singGaus.GetParError(2)
	meanEff = 1000.0*tf1_singGaus.GetParameter(1)
	emeanEff = 1000.0*tf1_singGaus.GetParError(1)
	result = np.array([meanEff,emeanEff,sigEff,esigEff])
	return result

def doubGausFit(hist, x_min, x_max):
	tf1_doubGaus = TF1("tf1_doubGaus","gaus(0)+gaus(3)", x_min,x_max)
	#tf1_doubGaus.SetParameters(0.5*hist.Integral(),0.5*(x_min+x_max),0.2*(x_max-x_min), 0.5*hist.Integral(),0.5*(x_min+x_max),0.1*(x_max-x_min))
	tf1_doubGaus.SetParameters(0.5*hist.Integral(),0.5*(x_min+x_max),0.15, 0.5*hist.Integral(),0.5*(x_min+x_max),0.35)
	hist.Fit("tf1_doubGaus","","",x_min,x_max)
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
cut = "mass>75 && mass <105 && ele1Pt>30 && ele2Pt>30 && ele1IsEB && ele2IsEB"

file_data = TFile("/eos/cms/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/All2016.root")
tree_data = file_data.Get("ZeeTiming")

file_MC = TFile("/eos/cms/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/MC2016_all.root")
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
N_pt_points = 19
pt_divide = [40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 78.0, 84.0, 91.0, 100.0, 115.0, 140.0, 190.0, 1000.0]

x_pt = np.zeros(N_pt_points)
ex_pt = np.zeros(N_pt_points)
y_pt_mean_data = np.zeros(N_pt_points)
y_pt_mean_MC = np.zeros(N_pt_points)
y_pt_mean_diff = np.zeros(N_pt_points)
y_pt_sigma_data = np.zeros(N_pt_points)
y_pt_sigma_MC = np.zeros(N_pt_points)
y_pt_sigma_diff = np.zeros(N_pt_points)
ey_pt_mean_data = np.zeros(N_pt_points)
ey_pt_mean_MC = np.zeros(N_pt_points)
ey_pt_mean_diff = np.zeros(N_pt_points)
ey_pt_sigma_data = np.zeros(N_pt_points)
ey_pt_sigma_MC = np.zeros(N_pt_points)
ey_pt_sigma_diff = np.zeros(N_pt_points)


for i in range(0, N_pt_points):
	x_pt[i] = 0.5*(pt_divide[i+1]+pt_divide[i])
	ex_pt[i] = 0.5*(pt_divide[i+1]-pt_divide[i])
	pt_low_this = pt_divide[i]
	pt_high_this = pt_divide[i+1]
	cut_1e_this = cut+" && ele1Pt > "+str(pt_low_this)+" && ele1Pt < "+str(pt_high_this)
	cut_2e_this = cut+" && ele1Pt > "+str(pt_low_this)+" && ele1Pt < "+str(pt_high_this)+" && ele2Pt < "+str(pt_high_this)

	hist_1e_this_data = TH1F("hist_1e_this_data_"+str(i),"hist_1e_this_data_"+str(i), 60, -1.5, 1.5)
	hist_2e_this_data = TH1F("hist_2e_this_data_"+str(i),"hist_2e_this_data_"+str(i), 60, -1.5, 1.5)
	tree_data.Draw("t1>>hist_1e_this_data_"+str(i), cut_1e_this)
	tree_data.Draw("t1-t2>>hist_2e_this_data_"+str(i), cut_2e_this)
	result_1e_this_data = singGausFit(hist_1e_this_data, -0.6, 0.6) 
	hist_2e_this_data.Draw()
	result_2e_this_data = doubGausFit(hist_2e_this_data, -1.5, 1.5) 
	myC.SaveAs(outputDir+"/ZeeTiming/iptFit_"+str(i)+"_dt_data.pdf")
	myC.SaveAs(outputDir+"/ZeeTiming/iptFit_"+str(i)+"_dt_data.png")
	myC.SaveAs(outputDir+"/ZeeTiming/iptFit_"+str(i)+"_dt_data.C")
	y_pt_mean_data[i] = result_1e_this_data[0]
	ey_pt_mean_data[i] = result_1e_this_data[1]
	y_pt_sigma_data[i] = result_2e_this_data[2]
	ey_pt_sigma_data[i] = result_2e_this_data[3]


	hist_1e_this_MC = TH1F("hist_1e_this_MC_"+str(i),"hist_1e_this_MC_"+str(i), 60, -1.5, 1.5)
	hist_2e_this_MC = TH1F("hist_2e_this_MC_"+str(i),"hist_2e_this_MC_"+str(i), 60, -1.5, 1.5)
	tree_MC.Draw("t1>>hist_1e_this_MC_"+str(i), cut_1e_this)
	tree_MC.Draw("t1-t2>>hist_2e_this_MC_"+str(i), cut_2e_this)
	result_1e_this_MC = singGausFit(hist_1e_this_MC, -0.6, 0.6) 
	hist_2e_this_MC.Draw()
	result_2e_this_MC = doubGausFit(hist_2e_this_MC, -1.0, 1.0) 
	myC.SaveAs(outputDir+"/ZeeTiming/iptFit_"+str(i)+"_dt_MC.pdf")
	myC.SaveAs(outputDir+"/ZeeTiming/iptFit_"+str(i)+"_dt_MC.png")
	myC.SaveAs(outputDir+"/ZeeTiming/iptFit_"+str(i)+"_dt_MC.C")
	y_pt_mean_MC[i] = result_1e_this_MC[0]
	ey_pt_mean_MC[i] = result_1e_this_MC[1]
	y_pt_sigma_MC[i] = result_2e_this_MC[2]
	ey_pt_sigma_MC[i] = result_2e_this_MC[3]

	y_pt_mean_diff[i] = y_pt_mean_data[i] -  y_pt_mean_MC[i]
	ey_pt_mean_diff[i] = np.sqrt(ey_pt_mean_data[i]*ey_pt_mean_data[i] + ey_pt_mean_MC[i]*ey_pt_mean_MC[i])
	y_pt_sigma_diff[i] = np.sqrt(y_pt_sigma_data[i]*y_pt_sigma_data[i] -  y_pt_sigma_MC[i]*y_pt_sigma_MC[i])
	ey_pt_sigma_diff[i] = np.sqrt(4.0*y_pt_sigma_data[i]*y_pt_sigma_data[i]*ey_pt_sigma_data[i]*ey_pt_sigma_data[i]+4.0*y_pt_sigma_MC[i]*y_pt_sigma_MC[i]*ey_pt_sigma_MC[i]*ey_pt_sigma_MC[i])/(2.0*y_pt_sigma_diff[i])

print "y_pt_mean_data:"
print y_pt_mean_data
print "ey_pt_mean_data:"
print ey_pt_mean_data

print "y_pt_mean_MC:"
print y_pt_mean_MC
print "ey_pt_mean_MC:"
print ey_pt_mean_MC

print "y_pt_mean_diff:"
print y_pt_mean_diff
print "ey_pt_mean_diff:"
print ey_pt_mean_diff

print "y_pt_sigma_data:"
print y_pt_sigma_data
print "ey_pt_sigma_data:"
print ey_pt_sigma_data

print "y_pt_sigma_MC:"
print y_pt_sigma_MC
print "ey_pt_sigma_MC:"
print ey_pt_sigma_MC

print "y_pt_sigma_diff:"
print y_pt_sigma_diff
print "ey_pt_sigma_diff:"
print ey_pt_sigma_diff



gStyle.SetOptFit(0)
myC.SetGridy(1)
myC.SetLogx(1)

gr_pt_mean_data  =  TGraphErrors(N_pt_points, np.array(x_pt), np.array(y_pt_mean_data), np.array(ex_pt), np.array(ey_pt_mean_data))
gr_pt_mean_data.Draw("AP")
gr_pt_mean_data.SetMarkerColor(kBlue)
gr_pt_mean_data.SetLineColor(kBlue)
gr_pt_mean_data.SetLineWidth(2)
gr_pt_mean_data.SetTitle("")
gr_pt_mean_data.GetXaxis().SetTitle("p_{T}^{#gamma} [GeV]")
gr_pt_mean_data.GetYaxis().SetTitle("electron time [ps]")
gr_pt_mean_data.GetXaxis().SetTitleSize( axisTitleSize )
gr_pt_mean_data.GetXaxis().SetTitleOffset( axisTitleOffset )
gr_pt_mean_data.GetYaxis().SetTitleSize( axisTitleSize )
gr_pt_mean_data.GetYaxis().SetTitleOffset( axisTitleOffset +0.18 )
gr_pt_mean_data.GetYaxis().SetRangeUser(-350,600)

gr_pt_mean_MC  =  TGraphErrors(N_pt_points, np.array(x_pt), np.array(y_pt_mean_MC), np.array(ex_pt), np.array(ey_pt_mean_MC))
gr_pt_mean_MC.SetMarkerColor(kRed)
gr_pt_mean_MC.SetLineColor(kRed)
gr_pt_mean_MC.SetLineWidth(2)
gr_pt_mean_MC.Draw("Psame")

gr_pt_mean_diff  =  TGraphErrors(N_pt_points, np.array(x_pt), np.array(y_pt_mean_diff), np.array(ex_pt), np.array(ey_pt_mean_diff))
gr_pt_mean_diff.SetMarkerColor(kBlack)
gr_pt_mean_diff.SetLineColor(kBlack)
gr_pt_mean_diff.SetLineWidth(2)
gr_pt_mean_diff.Draw("Psame")


leg_mean = TLegend(0.18,0.8,0.93,0.89)
leg_mean.SetNColumns(3)
leg_mean.SetBorderSize(0)
leg_mean.SetTextSize(0.03)
leg_mean.SetLineColor(1)
leg_mean.SetLineStyle(1)
leg_mean.SetLineWidth(1)
leg_mean.SetFillColor(0)
leg_mean.SetFillStyle(1001)
leg_mean.AddEntry(gr_pt_mean_data, "data", "lep")
leg_mean.AddEntry(gr_pt_mean_MC, "MC", "lep")
leg_mean.AddEntry(gr_pt_mean_diff, "#Delta(data, MC)", "lep")
leg_mean.Draw()

drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_vs_pt_Data_vs_MC_2016.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_vs_pt_Data_vs_MC_2016.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingShift_vs_pt_Data_vs_MC_2016.C")

gr_pt_sigma_data  =  TGraphErrors(N_pt_points, np.array(x_pt), np.array(y_pt_sigma_data), np.array(ex_pt), np.array(ey_pt_sigma_data))
gr_pt_sigma_data.Draw("AP")
gr_pt_sigma_data.SetMarkerColor(kBlue)
gr_pt_sigma_data.SetLineColor(kBlue)
gr_pt_sigma_data.SetLineWidth(2)
gr_pt_sigma_data.SetTitle("")
gr_pt_sigma_data.GetXaxis().SetTitle("p_{T}^{#gamma} [GeV]")
gr_pt_sigma_data.GetYaxis().SetTitle("#sigma_{t1-t2} [ps]")
gr_pt_sigma_data.GetXaxis().SetTitleSize( axisTitleSize )
gr_pt_sigma_data.GetXaxis().SetTitleOffset( axisTitleOffset )
gr_pt_sigma_data.GetYaxis().SetTitleSize( axisTitleSize )
gr_pt_sigma_data.GetYaxis().SetTitleOffset( axisTitleOffset +0.18 )
gr_pt_sigma_data.GetYaxis().SetRangeUser(100,500)

tf1_dt_vs_pt_data = TF1("tf1_dt_vs_pt_data","sqrt([0]/(x*x)+[1])", 49.0, 300.0)
tf1_dt_vs_pt_data.SetLineColor(kBlue)
tf1_dt_vs_pt_data.SetParameters(200.0, 300.0*300.0)
gr_pt_sigma_data.Fit("tf1_dt_vs_pt_data","","",49.0, 300.0)
fit_a_data = tf1_dt_vs_pt_data.GetParameter(0)
fit_b_data = tf1_dt_vs_pt_data.GetParameter(1)

gr_pt_sigma_MC  =  TGraphErrors(N_pt_points, np.array(x_pt), np.array(y_pt_sigma_MC), np.array(ex_pt), np.array(ey_pt_sigma_MC))
gr_pt_sigma_MC.SetMarkerColor(kRed)
gr_pt_sigma_MC.SetLineColor(kRed)
gr_pt_sigma_MC.SetLineWidth(2)
gr_pt_sigma_MC.Draw("Psame")

tf1_dt_vs_pt_MC = TF1("tf1_dt_vs_pt_MC","sqrt([0]/(x*x)+[1])", 49.0, 300.0)
tf1_dt_vs_pt_MC.SetLineColor(kRed)
tf1_dt_vs_pt_MC.SetParameters(200.0, 130.0*130.0)
gr_pt_sigma_MC.Fit("tf1_dt_vs_pt_MC","","",49.0, 300.0)
fit_a_MC = tf1_dt_vs_pt_MC.GetParameter(0)
fit_b_MC = tf1_dt_vs_pt_MC.GetParameter(1)


gr_pt_sigma_diff  =  TGraphErrors(N_pt_points, np.array(x_pt), np.array(y_pt_sigma_diff), np.array(ex_pt), np.array(ey_pt_sigma_diff))
gr_pt_sigma_diff.SetMarkerColor(kBlack)
gr_pt_sigma_diff.SetLineColor(kBlack)
gr_pt_sigma_diff.SetLineWidth(2)
gr_pt_sigma_diff.Draw("Psame")


leg_sigma = TLegend(0.18,0.8,0.93,0.89)
leg_sigma.SetNColumns(3)
leg_sigma.SetBorderSize(0)
leg_sigma.SetTextSize(0.03)
leg_sigma.SetLineColor(1)
leg_sigma.SetLineStyle(1)
leg_sigma.SetLineWidth(1)
leg_sigma.SetFillColor(0)
leg_sigma.SetFillStyle(1001)
leg_sigma.AddEntry(gr_pt_sigma_data, "data", "lep")
leg_sigma.AddEntry(gr_pt_sigma_MC, "MC", "lep")
leg_sigma.AddEntry(gr_pt_sigma_diff, "#Delta(data, MC)", "lep")
leg_sigma.Draw()


leg_fit_data = TLegend(0.42,0.615,0.93,0.715)
leg_fit_data.SetNColumns(3)
leg_fit_data.SetBorderSize(0)
leg_fit_data.SetTextSize(0.035)
leg_fit_data.SetTextColor(kBlue)
leg_fit_data.SetLineColor(1)
leg_fit_data.SetLineStyle(1)
leg_fit_data.SetLineWidth(1)
#leg_fit_data.SetFillColor(0)
leg_fit_data.SetFillStyle(0)
fit_ab_data = "data:  #sigma = #frac{"+ "%.1f" % np.sqrt(np.abs(fit_a_data))+"}{p_{T}^{#gamma}} #oplus #sqrt{2} #times "+"%.1f" % np.sqrt(np.abs(fit_b_data)/2.0)
leg_fit_data.AddEntry(gr_pt_sigma_data, fit_ab_data , "")
leg_fit_data.Draw()

leg_fit_MC = TLegend(0.42,0.315,0.93,0.415)
leg_fit_MC.SetNColumns(3)
leg_fit_MC.SetBorderSize(0)
leg_fit_MC.SetTextSize(0.035)
leg_fit_MC.SetTextColor(kRed)
leg_fit_MC.SetLineColor(1)
leg_fit_MC.SetLineStyle(1)
leg_fit_MC.SetLineWidth(1)
#leg_fit_MC.SetFillColor(0)
leg_fit_MC.SetFillStyle(0)
fit_ab_MC = "MC:  #sigma = #frac{"+ "%.1f" % np.sqrt(np.abs(fit_a_MC))+"}{p_{T}^{#gamma}} #oplus #sqrt{2} #times "+"%.1f" % np.sqrt(np.abs(fit_b_MC)/2.0)
leg_fit_MC.AddEntry(gr_pt_sigma_MC, fit_ab_MC , "")
leg_fit_MC.Draw()

drawCMS(myC, 13, lumi)

myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_vs_pt_Data_vs_MC_2016.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_vs_pt_Data_vs_MC_2016.png")
myC.SaveAs(outputDir+"/ZeeTiming/TimingReso_vs_pt_Data_vs_MC_2016.C")


