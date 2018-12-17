from ROOT import gROOT, gStyle, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TGraph, kDashed, kGreen, kYellow, TF1, kPink, kGray, TGaxis
import os, sys
from Aux import *
import numpy as np
import array

lumi_withTCorr = 35922.0
lumi_noTCorr = lumi_withTCorr
lumi = lumi_withTCorr
outputDir = '/data/zhicaiz/www/sharebox/DelayedPhoton/15Nov2018/orderByPt/'

lambda_points = [100, 150, 200, 250, 300, 350, 400]
ctau_points = [0.1, 10, 200, 400, 600, 1000, 1200]

drawObs=False
gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=200)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/limits")
os.system("cp draw_limits.py "+outputDir+"/limits")
#os.system("mkdir -p ../data")
#################plot settings###########################

axisTitleSize = 0.05
axisTitleOffset = 1.0
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
bottomMargin2 = 0.22


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
myC.SetLogx(1)

N_lambda = len(lambda_points)
N_ctau = len(ctau_points)

r_exp_2d_grid_withTCorr = np.zeros((N_ctau, N_lambda))
r_exp_p1sig_2d_grid_withTCorr = np.zeros((N_ctau, N_lambda))
r_exp_m1sig_2d_grid_withTCorr = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_withTCorr = np.zeros((N_ctau, N_lambda))

r_exp_2d_grid_noTCorr = np.zeros((N_ctau, N_lambda))
r_exp_p1sig_2d_grid_noTCorr = np.zeros((N_ctau, N_lambda))
r_exp_m1sig_2d_grid_noTCorr = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_noTCorr = np.zeros((N_ctau, N_lambda))


##################limit vs mass #######################3

index_ctau = -1
for ctau_this in ctau_points:
	index_ctau = index_ctau + 1
	print "plotting xsec*BR limit for ctau = "+str(ctau_this)

	xValue_lambda = []
	xValue_lambda_exp1sigma = []
	xValue_lambda_exp2sigma = []
	xValue_mass = []
	xValue_mass_exp1sigma = []
	xValue_mass_exp2sigma = []
	yValue_limit_this_Th = []

	limit_this_withTCorr_exp2p5 = []
	limit_this_withTCorr_exp16p0 = []
	limit_this_withTCorr_exp50p0 = []
	limit_this_withTCorr_exp84p0 = []
	limit_this_withTCorr_exp97p5 = []
	limit_this_withTCorr_obs = []

	limit_this_noTCorr_exp2p5 = []
	limit_this_noTCorr_exp16p0 = []
	limit_this_noTCorr_exp50p0 = []
	limit_this_noTCorr_exp84p0 = []
	limit_this_noTCorr_exp97p5 = []
	limit_this_noTCorr_obs = []


	yValue_limit_this_withTCorr_exp = []
	yValue_limit_this_withTCorr_obs = []
	yValue_limit_this_withTCorr_exp1sigma = []
	yValue_limit_this_withTCorr_exp2sigma = []
	
	yValue_limit_this_noTCorr_exp = []
	yValue_limit_this_noTCorr_obs = []
	yValue_limit_this_noTCorr_exp1sigma = []
	yValue_limit_this_noTCorr_exp2sigma = []
		

	ctau_this_str = str(ctau_this)
	if ctau_this_str == "0.1":
		ctau_this_str = "0_1"
	if ctau_this_str == "0.01":
		ctau_this_str = "0_01"
		
	index_lambda = - 1
	for lambda_this in lambda_points:
		index_lambda = index_lambda + 1
		minsize = 1000
		actualsize_withTCorr = 0
		actualsize_noTCorr = 1
		if os.path.isfile("../fit_results/2016_withTCorr/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root"):
                        actualsize_withTCorr = os.path.getsize("../fit_results/2016_withTCorr/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")
		if os.path.isfile("../fit_results/2016_noTCorr/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root"):
                        actualsize_noTCorr = os.path.getsize("../fit_results/2016_noTCorr/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")


		if actualsize_withTCorr > minsize and actualsize_noTCorr > minsize:
			print "extracting lambda = "+str(lambda_this)

			xValue_lambda.append(lambda_this)
			xValue_mass.append(lambda_this*1.454-6.0)
			th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)
			yValue_limit_this_Th.append(th_xsec_this)

			file_limit_withTCorr = TFile("../fit_results/2016_withTCorr/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")
			limits_withTCorr = []
			limitTree_withTCorr = file_limit_withTCorr.Get("limit")
			for entry in limitTree_withTCorr:
				limits_withTCorr.append(entry.limit)
			print limits_withTCorr

			limit_this_withTCorr_exp2p5.append(limits_withTCorr[0]*th_xsec_this)	
			limit_this_withTCorr_exp16p0.append(limits_withTCorr[1]*th_xsec_this)	
			limit_this_withTCorr_exp50p0.append(limits_withTCorr[2]*th_xsec_this)	
			limit_this_withTCorr_exp84p0.append(limits_withTCorr[3]*th_xsec_this)	
			limit_this_withTCorr_exp97p5.append(limits_withTCorr[4]*th_xsec_this)	
			limit_this_withTCorr_obs.append(limits_withTCorr[5]*th_xsec_this)	

			r_exp_2d_grid_withTCorr[index_ctau][index_lambda] = limits_withTCorr[2]
			r_exp_p1sig_2d_grid_withTCorr[index_ctau][index_lambda] = limits_withTCorr[3]
			r_exp_m1sig_2d_grid_withTCorr[index_ctau][index_lambda] = limits_withTCorr[1]
			r_obs_2d_grid_withTCorr[index_ctau][index_lambda] = limits_withTCorr[5]

			file_limit_noTCorr = TFile("../fit_results/2016_noTCorr/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")
			limits_noTCorr = []
			limitTree_noTCorr = file_limit_noTCorr.Get("limit")
			for entry in limitTree_noTCorr:
				limits_noTCorr.append(entry.limit)
			print limits_noTCorr

			limit_this_noTCorr_exp2p5.append(limits_noTCorr[0]*th_xsec_this)	
			limit_this_noTCorr_exp16p0.append(limits_noTCorr[1]*th_xsec_this)	
			limit_this_noTCorr_exp50p0.append(limits_noTCorr[2]*th_xsec_this)	
			limit_this_noTCorr_exp84p0.append(limits_noTCorr[3]*th_xsec_this)	
			limit_this_noTCorr_exp97p5.append(limits_noTCorr[4]*th_xsec_this)	
			limit_this_noTCorr_obs.append(limits_noTCorr[5]*th_xsec_this)	

			r_exp_2d_grid_noTCorr[index_ctau][index_lambda] = limits_noTCorr[2]
			r_exp_p1sig_2d_grid_noTCorr[index_ctau][index_lambda] = limits_noTCorr[3]
			r_exp_m1sig_2d_grid_noTCorr[index_ctau][index_lambda] = limits_noTCorr[1]
			r_obs_2d_grid_noTCorr[index_ctau][index_lambda] = limits_noTCorr[5]


	NPoints_mass = len(xValue_mass)
	print "NPoints_mass = "+str(NPoints_mass)

	for i in range(0, NPoints_mass):
		xValue_mass.append(xValue_mass[i])
		xValue_mass_exp1sigma.append(xValue_mass[i])
		xValue_mass_exp2sigma.append(xValue_mass[i])
		
		yValue_limit_this_withTCorr_obs.append(limit_this_withTCorr_obs[i])
		yValue_limit_this_withTCorr_exp.append(limit_this_withTCorr_exp50p0[i])
		yValue_limit_this_withTCorr_exp1sigma.append(limit_this_withTCorr_exp16p0[i])
		yValue_limit_this_withTCorr_exp2sigma.append(limit_this_withTCorr_exp2p5[i])
			
		yValue_limit_this_noTCorr_obs.append(limit_this_noTCorr_obs[i])
		yValue_limit_this_noTCorr_exp.append(limit_this_noTCorr_exp50p0[i])
		yValue_limit_this_noTCorr_exp1sigma.append(limit_this_noTCorr_exp16p0[i])
		yValue_limit_this_noTCorr_exp2sigma.append(limit_this_noTCorr_exp2p5[i])
			


	for i in range(0, NPoints_mass):
		xValue_mass_exp1sigma.append(xValue_mass[NPoints_mass-i-1])
		xValue_mass_exp2sigma.append(xValue_mass[NPoints_mass-i-1])
		
		yValue_limit_this_withTCorr_exp1sigma.append(limit_this_withTCorr_exp84p0[NPoints_mass-i-1])
		yValue_limit_this_withTCorr_exp2sigma.append(limit_this_withTCorr_exp97p5[NPoints_mass-i-1])

		yValue_limit_this_noTCorr_exp1sigma.append(limit_this_noTCorr_exp84p0[NPoints_mass-i-1])
		yValue_limit_this_noTCorr_exp2sigma.append(limit_this_noTCorr_exp97p5[NPoints_mass-i-1])
		

	myC.SetLogy(1)
	myC.SetLogx(0)
	
	#withTCorr
	graph_limit_vs_mass_withTCorr_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_withTCorr_obs))
	graph_limit_vs_mass_withTCorr_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_withTCorr_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_withTCorr_exp))
	graph_limit_vs_mass_withTCorr_exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp1sigma), np.array(yValue_limit_this_withTCorr_exp1sigma))
	graph_limit_vs_mass_withTCorr_exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp2sigma), np.array(yValue_limit_this_withTCorr_exp2sigma))

	graph_limit_vs_mass_withTCorr_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_withTCorr_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_withTCorr_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_withTCorr_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_withTCorr_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_withTCorr_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_withTCorr_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_withTCorr_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_withTCorr_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_withTCorr_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_withTCorr_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_withTCorr_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_withTCorr_exp_limit.SetLineStyle(kDashed)

	graph_limit_vs_mass_withTCorr_exp1sigma_limit.SetFillColor(kGreen)
	graph_limit_vs_mass_withTCorr_exp2sigma_limit.SetFillColor(kYellow)

	graph_limit_vs_mass_withTCorr_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_withTCorr_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_withTCorr_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_withTCorr_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_withTCorr_exp_limit.SetTitle("")

	graph_limit_vs_mass_withTCorr_exp_limit.Draw("LA")

	graph_limit_vs_mass_withTCorr_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_withTCorr_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_withTCorr_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_withTCorr_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	graph_limit_vs_mass_withTCorr_exp2sigma_limit.Draw("Fsame")
	graph_limit_vs_mass_withTCorr_exp1sigma_limit.Draw("Fsame")
	if drawObs:
		graph_limit_vs_mass_withTCorr_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_withTCorr_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_withTCorr_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi_withTCorr)

	leg_limit_vs_mass_withTCorr = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_withTCorr.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_withTCorr.SetBorderSize(0)
	leg_limit_vs_mass_withTCorr.SetTextSize(0.03)
	leg_limit_vs_mass_withTCorr.SetLineColor(1)
	leg_limit_vs_mass_withTCorr.SetLineStyle(1)
	leg_limit_vs_mass_withTCorr.SetLineWidth(1)
	leg_limit_vs_mass_withTCorr.SetFillColor(0)
	leg_limit_vs_mass_withTCorr.SetFillStyle(1001)

	leg_limit_vs_mass_withTCorr.AddEntry(graph_limit_vs_mass_withTCorr_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_withTCorr.AddEntry(graph_limit_vs_mass_withTCorr_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_withTCorr.AddEntry(graph_limit_vs_mass_withTCorr_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_withTCorr.AddEntry(graph_limit_vs_mass_withTCorr_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
	leg_limit_vs_mass_withTCorr.AddEntry(graph_limit_vs_mass_withTCorr_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
	leg_limit_vs_mass_withTCorr.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_withTCorr_ctau"+ctau_this_str+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_withTCorr_ctau"+ctau_this_str+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_withTCorr_ctau"+ctau_this_str+".C")

	#noTCorr
	graph_limit_vs_mass_noTCorr_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_noTCorr_obs))
	graph_limit_vs_mass_noTCorr_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_noTCorr_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_noTCorr_exp))
	graph_limit_vs_mass_noTCorr_exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp1sigma), np.array(yValue_limit_this_noTCorr_exp1sigma))
	graph_limit_vs_mass_noTCorr_exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp2sigma), np.array(yValue_limit_this_noTCorr_exp2sigma))

	graph_limit_vs_mass_noTCorr_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_noTCorr_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_noTCorr_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_noTCorr_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_noTCorr_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_noTCorr_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_noTCorr_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_noTCorr_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_noTCorr_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_noTCorr_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_noTCorr_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_noTCorr_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_noTCorr_exp_limit.SetLineStyle(kDashed)

	graph_limit_vs_mass_noTCorr_exp1sigma_limit.SetFillColor(kGreen)
	graph_limit_vs_mass_noTCorr_exp2sigma_limit.SetFillColor(kYellow)

	graph_limit_vs_mass_noTCorr_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_noTCorr_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_noTCorr_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_noTCorr_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_noTCorr_exp_limit.SetTitle("")

	graph_limit_vs_mass_noTCorr_exp_limit.Draw("LA")

	graph_limit_vs_mass_noTCorr_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_noTCorr_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_noTCorr_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_noTCorr_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	graph_limit_vs_mass_noTCorr_exp2sigma_limit.Draw("Fsame")
	graph_limit_vs_mass_noTCorr_exp1sigma_limit.Draw("Fsame")
	if drawObs:
		graph_limit_vs_mass_noTCorr_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_noTCorr_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_noTCorr_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi_noTCorr)

	leg_limit_vs_mass_noTCorr = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_noTCorr.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_noTCorr.SetBorderSize(0)
	leg_limit_vs_mass_noTCorr.SetTextSize(0.03)
	leg_limit_vs_mass_noTCorr.SetLineColor(1)
	leg_limit_vs_mass_noTCorr.SetLineStyle(1)
	leg_limit_vs_mass_noTCorr.SetLineWidth(1)
	leg_limit_vs_mass_noTCorr.SetFillColor(0)
	leg_limit_vs_mass_noTCorr.SetFillStyle(1001)

	leg_limit_vs_mass_noTCorr.AddEntry(graph_limit_vs_mass_noTCorr_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_noTCorr.AddEntry(graph_limit_vs_mass_noTCorr_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_noTCorr.AddEntry(graph_limit_vs_mass_noTCorr_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_noTCorr.AddEntry(graph_limit_vs_mass_noTCorr_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
	leg_limit_vs_mass_noTCorr.AddEntry(graph_limit_vs_mass_noTCorr_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
	leg_limit_vs_mass_noTCorr.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_noTCorr_ctau"+ctau_this_str+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_noTCorr_ctau"+ctau_this_str+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_noTCorr_ctau"+ctau_this_str+".C")

	###overlay withTCorr and noTCorr in the same plot

	graph_limit_vs_mass_withTCorr_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_withTCorr_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_withTCorr_exp_limit.SetLineColor(4)
	graph_limit_vs_mass_withTCorr_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_noTCorr_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_noTCorr_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_noTCorr_exp_limit.SetLineColor(7)
	graph_limit_vs_mass_noTCorr_exp_limit.SetLineWidth(3)


	graph_limit_vs_mass_withTCorr_exp_limit.Draw("LA")
	graph_limit_vs_mass_noTCorr_exp_limit.Draw("Lsame")

	if drawObs:
		graph_limit_vs_mass_withTCorr_obs_limit.Draw("Lsame")
		graph_limit_vs_mass_noTCorr_obs_limit.Draw("Lsame")

	graph_limit_vs_mass_withTCorr_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_mass = TLegend(0.15,0.62,0.9,0.89)

	leg_limit_vs_mass.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass.SetBorderSize(0)
	leg_limit_vs_mass.SetTextSize(0.03)
	leg_limit_vs_mass.SetLineColor(1)
	leg_limit_vs_mass.SetLineStyle(1)
	leg_limit_vs_mass.SetLineWidth(1)
	leg_limit_vs_mass.SetFillColor(0)
	leg_limit_vs_mass.SetFillStyle(1001)

	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_withTCorr_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_withTCorr_obs_limit, "Observed  95% CL upper limit, withTCorr", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_withTCorr_exp_limit, "Expected  95% CL upper limit, with time correction", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_noTCorr_exp_limit, "Expected  95% CL upper limit, no time correction", "L")
	leg_limit_vs_mass.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_withTCorr_noTCorr_ctau"+ctau_this_str+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_withTCorr_noTCorr_ctau"+ctau_this_str+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_withTCorr_noTCorr_ctau"+ctau_this_str+".C")


##################exclusion region of ctau and Lambda/mass #######################

print "value of the 2D r grid (exp, withTCorr) provided from samples: "
print r_exp_2d_grid_withTCorr
print "value of the 2D r grid (obs, withTCorr) provided from samples: "
print r_obs_2d_grid_withTCorr


print "value of the 2D r grid (exp, noTCorr) provided from samples: "
print r_exp_2d_grid_noTCorr
print "value of the 2D r grid (obs, noTCorr) provided from samples: "
print r_obs_2d_grid_noTCorr


###linear interpolation to get the boundary points

lambda_point_boundary_exp_withTCorr = np.zeros(N_ctau)
lambda_point_boundary_exp_p1sig_withTCorr = np.zeros(N_ctau)
lambda_point_boundary_exp_m1sig_withTCorr = np.zeros(N_ctau)
lambda_point_boundary_obs_withTCorr = np.zeros(N_ctau)

lambda_point_boundary_exp_noTCorr = np.zeros(N_ctau)
lambda_point_boundary_exp_p1sig_noTCorr = np.zeros(N_ctau)
lambda_point_boundary_exp_m1sig_noTCorr = np.zeros(N_ctau)
lambda_point_boundary_obs_noTCorr = np.zeros(N_ctau)



for i in range(0, N_ctau):
	print "doing linear interpolation to get the boundary value of lambda for ctau = "+str(ctau_points[i])

	lambda_interp_withTCorr = []
	r_exp_interp_withTCorr = []
	r_exp_p1sig_interp_withTCorr = []
	r_exp_m1sig_interp_withTCorr = []
	r_obs_interp_withTCorr = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_withTCorr[i][j] > 0.00000001:
			lambda_interp_withTCorr.append(lambda_points[j]*1.0)
			r_exp_interp_withTCorr.append(r_exp_2d_grid_withTCorr[i][j]*1.0)
			r_exp_p1sig_interp_withTCorr.append(r_exp_p1sig_2d_grid_withTCorr[i][j]*1.0)
			r_exp_m1sig_interp_withTCorr.append(r_exp_m1sig_2d_grid_withTCorr[i][j]*1.0)
			r_obs_interp_withTCorr.append(r_obs_2d_grid_withTCorr[i][j]*1.0)
	graph_lambda_vs_r_exp_withTCorr =  TGraph(len(lambda_interp_withTCorr), np.array(r_exp_interp_withTCorr), np.array(lambda_interp_withTCorr))
	graph_lambda_vs_r_exp_p1sig_withTCorr =  TGraph(len(lambda_interp_withTCorr), np.array(r_exp_p1sig_interp_withTCorr), np.array(lambda_interp_withTCorr))
	graph_lambda_vs_r_exp_m1sig_withTCorr =  TGraph(len(lambda_interp_withTCorr), np.array(r_exp_m1sig_interp_withTCorr), np.array(lambda_interp_withTCorr))
	lambda_point_boundary_exp_withTCorr[i] = graph_lambda_vs_r_exp_withTCorr.Eval(1.0)
	lambda_point_boundary_exp_p1sig_withTCorr[i] = graph_lambda_vs_r_exp_p1sig_withTCorr.Eval(1.0)
	lambda_point_boundary_exp_m1sig_withTCorr[i] = graph_lambda_vs_r_exp_m1sig_withTCorr.Eval(1.0)
	graph_lambda_vs_r_obs_withTCorr =  TGraph(len(lambda_interp_withTCorr), np.array(r_obs_interp_withTCorr), np.array(lambda_interp_withTCorr))
	lambda_point_boundary_obs_withTCorr[i] = graph_lambda_vs_r_obs_withTCorr.Eval(1.0)

	lambda_interp_noTCorr = []
	r_exp_interp_noTCorr = []
	r_exp_p1sig_interp_noTCorr = []
	r_exp_m1sig_interp_noTCorr = []
	r_obs_interp_noTCorr = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_noTCorr[i][j] > 0.00000001:
			lambda_interp_noTCorr.append(lambda_points[j]*1.0)
			r_exp_interp_noTCorr.append(r_exp_2d_grid_noTCorr[i][j]*1.0)
			r_exp_p1sig_interp_noTCorr.append(r_exp_p1sig_2d_grid_noTCorr[i][j]*1.0)
			r_exp_m1sig_interp_noTCorr.append(r_exp_m1sig_2d_grid_noTCorr[i][j]*1.0)
			r_obs_interp_noTCorr.append(r_obs_2d_grid_noTCorr[i][j]*1.0)
	graph_lambda_vs_r_exp_noTCorr =  TGraph(len(lambda_interp_noTCorr), np.array(r_exp_interp_noTCorr), np.array(lambda_interp_noTCorr))
	graph_lambda_vs_r_exp_p1sig_noTCorr =  TGraph(len(lambda_interp_noTCorr), np.array(r_exp_p1sig_interp_noTCorr), np.array(lambda_interp_noTCorr))
	graph_lambda_vs_r_exp_m1sig_noTCorr =  TGraph(len(lambda_interp_noTCorr), np.array(r_exp_m1sig_interp_noTCorr), np.array(lambda_interp_noTCorr))
	lambda_point_boundary_exp_noTCorr[i] = graph_lambda_vs_r_exp_noTCorr.Eval(1.0)
	lambda_point_boundary_exp_p1sig_noTCorr[i] = graph_lambda_vs_r_exp_p1sig_noTCorr.Eval(1.0)
	lambda_point_boundary_exp_m1sig_noTCorr[i] = graph_lambda_vs_r_exp_m1sig_noTCorr.Eval(1.0)
	graph_lambda_vs_r_obs_noTCorr =  TGraph(len(lambda_interp_noTCorr), np.array(r_obs_interp_noTCorr), np.array(lambda_interp_noTCorr))
	lambda_point_boundary_obs_noTCorr[i] = graph_lambda_vs_r_obs_noTCorr.Eval(1.0)



print "lambda points:"
print lambda_points

print "exp (withTCorr) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_withTCorr
print "exp p1sig (withTCorr) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_p1sig_withTCorr
print "exp m1sig (withTCorr) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_m1sig_withTCorr
print "obs (withTCorr) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_withTCorr

print "exp (noTCorr) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_noTCorr
print "exp p1sig (noTCorr) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_p1sig_noTCorr
print "exp m1sig (noTCorr) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_m1sig_noTCorr
print "obs (noTCorr) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_noTCorr


myC2D = TCanvas( "myC2D", "myC2D", 200, 10, 800, 800 )
myC2D.SetHighLightColor(2)
myC2D.SetFillColor(0)
myC2D.SetBorderMode(0)
myC2D.SetBorderSize(2)
myC2D.SetLeftMargin( leftMargin )
myC2D.SetRightMargin( rightMargin )
myC2D.SetTopMargin( topMargin )
myC2D.SetBottomMargin( bottomMargin2 )
myC2D.SetFrameBorderMode(0)
myC2D.SetFrameBorderMode(0)
myC2D.SetLogy(1)
myC2D.SetLogx(1)
myC2D.SetLogy(1)
myC2D.SetLogx(0)

lambda_point_boundary_exp_pm1sig_withTCorr = []
lambda_point_boundary_exp_pm1sig_noTCorr = []
ctau_points_loop = []

for i in range(0,len(ctau_points)):
	ctau_points_loop.append(ctau_points[i])
	lambda_point_boundary_exp_pm1sig_withTCorr.append(lambda_point_boundary_exp_p1sig_withTCorr[i]*1.0)
	lambda_point_boundary_exp_pm1sig_noTCorr.append(lambda_point_boundary_exp_p1sig_noTCorr[i]*1.0)

for i in range(0, len(ctau_points)):
	ctau_points_loop.append(ctau_points[len(ctau_points)-i-1]*1.0) 
	lambda_point_boundary_exp_pm1sig_withTCorr.append(lambda_point_boundary_exp_m1sig_withTCorr[len(ctau_points)-i-1]*1.0)
	lambda_point_boundary_exp_pm1sig_noTCorr.append(lambda_point_boundary_exp_m1sig_noTCorr[len(ctau_points)-i-1]*1.0)

graph_exclusion_exp_withTCorr = TGraph(len(lambda_point_boundary_exp_withTCorr), np.array(1.454*lambda_point_boundary_exp_withTCorr-6.0), np.array(ctau_points))
graph_exclusion_exp_p1sig_withTCorr = TGraph(len(lambda_point_boundary_exp_p1sig_withTCorr), np.array(1.454*lambda_point_boundary_exp_p1sig_withTCorr-6.0), np.array(ctau_points))
graph_exclusion_exp_m1sig_withTCorr = TGraph(len(lambda_point_boundary_exp_m1sig_withTCorr), np.array(1.454*lambda_point_boundary_exp_m1sig_withTCorr-6.0), np.array(ctau_points))
graph_exclusion_exp_pm1sig_withTCorr = TGraph(len(lambda_point_boundary_exp_pm1sig_withTCorr), np.array(1.454*np.array(lambda_point_boundary_exp_pm1sig_withTCorr)-6.0), np.array(ctau_points_loop))
graph_exclusion_obs_withTCorr = TGraph(len(lambda_point_boundary_obs_withTCorr), np.array(1.454*lambda_point_boundary_obs_withTCorr-6.0), np.array(ctau_points))

graph_exclusion_exp_withTCorr.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_withTCorr.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_withTCorr.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_withTCorr.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_withTCorr.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_withTCorr.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_withTCorr.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_withTCorr.GetYaxis().SetRangeUser(0.05,1.0e7)
graph_exclusion_exp_withTCorr.SetTitle("")

graph_exclusion_exp_withTCorr.SetMarkerStyle(19)
graph_exclusion_exp_withTCorr.SetMarkerSize(0.0)
graph_exclusion_exp_withTCorr.SetLineColor(kOrange - 9)
graph_exclusion_exp_withTCorr.SetLineWidth(3)
graph_exclusion_exp_withTCorr.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_withTCorr.SetFillStyle(3353)
#graph_exclusion_exp_withTCorr.SetLineStyle(kDashed)

graph_exclusion_exp_p1sig_withTCorr.SetMarkerStyle(19)
graph_exclusion_exp_p1sig_withTCorr.SetMarkerSize(0.0)
graph_exclusion_exp_p1sig_withTCorr.SetLineColor(kOrange - 9)
graph_exclusion_exp_p1sig_withTCorr.SetLineWidth(2)
graph_exclusion_exp_p1sig_withTCorr.SetLineStyle(kDashed)

graph_exclusion_exp_m1sig_withTCorr.SetMarkerStyle(19)
graph_exclusion_exp_m1sig_withTCorr.SetMarkerSize(0.0)
graph_exclusion_exp_m1sig_withTCorr.SetLineColor(kOrange - 9)
graph_exclusion_exp_m1sig_withTCorr.SetLineWidth(2)
graph_exclusion_exp_m1sig_withTCorr.SetLineStyle(kDashed)

graph_exclusion_exp_pm1sig_withTCorr.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_pm1sig_withTCorr.SetFillStyle(3353)

graph_exclusion_obs_withTCorr.SetMarkerStyle(19)
graph_exclusion_obs_withTCorr.SetMarkerSize(0.0)
graph_exclusion_obs_withTCorr.SetLineColor(kBlack)
graph_exclusion_obs_withTCorr.SetLineWidth(3)
graph_exclusion_obs_withTCorr.SetLineStyle(kDashed)

#graph_exclusion_exp_withTCorr.SetFillColor(kAzure + 7)
#graph_exclusion_exp_withTCorr.SetFillColorAlpha(kOrange - 9, 0.65)

graph_exclusion_exp_withTCorr.Draw("AL")
#graph_exclusion_exp_p1sig_withTCorr.Draw("Lsame")
#graph_exclusion_exp_m1sig_withTCorr.Draw("Lsame")
graph_exclusion_exp_pm1sig_withTCorr.Draw("Fsame")

if drawObs:
	graph_exclusion_obs_withTCorr.Draw("Lsames")

#####ATLAS 8TeV
lambda_atlas_8TeV_2g = np.array([82.5 , 102.5,   140,   160,   180,   200,   220, 260,  300, 302.58, 300, 260, 220, 200 ])
t_atlas_8TeV_2g = np.array([ 121.81, 90.94, 46.63, 36.12, 27.18, 20.26, 14.59, 7.47, 2.6, 1.83, 1.31, 0.61, 0.39, 0.30 ])
ctau_atlas_8TeV_2g = t_atlas_8TeV_2g * 30.0
mass_atlas_8TeV_2g = lambda_atlas_8TeV_2g*1.454 - 6.0
graph_exclusion_atlas_8TeV_2g = TGraph(14, mass_atlas_8TeV_2g, ctau_atlas_8TeV_2g)
graph_exclusion_atlas_8TeV_2g.SetLineColor(8)
graph_exclusion_atlas_8TeV_2g.SetLineWidth(3)
graph_exclusion_atlas_8TeV_2g.SetLineStyle(5)
graph_exclusion_atlas_8TeV_2g.Draw("Lsames")

######CMS 7TeV
mass_cms_7TeV_1g = np.array([100., 145., 157., 179., 192., 216., 221., 218., 218., 221., 216., 192., 179., 157., 145., 100.])
ctau_cms_7TeV_1g  = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10., 25.0, 50.0, 100.0, 200.0, 400.0, 600.0, 600.0])
graph_exclusion_cms_7TeV_1g = TGraph(16, mass_cms_7TeV_1g, ctau_cms_7TeV_1g)
graph_exclusion_cms_7TeV_1g.SetFillColorAlpha(kPink, 0.65)
graph_exclusion_cms_7TeV_1g.Draw("Fsames")

######CMS 8TeV, single photon
mass_cms_8TeV_1g = np.array([140.0,   169.0,   198.0,  227.0,   256.0,    314.,    314., 285.,    256.,     227.,     198.,     169.,     140.])
ctau_cms_8TeV_1g  = np.array([92.39, 56.98, 51.43, 48.6, 70.59, 138.78, 212.92, 290, 702.16, 1063.61, 1298.93, 1243.29, 1349.28])
graph_exclusion_cms_8TeV_1g = TGraph(13, mass_cms_8TeV_1g, ctau_cms_8TeV_1g)
graph_exclusion_cms_8TeV_1g.SetFillColorAlpha(kBlue, 0.65)
graph_exclusion_cms_8TeV_1g.Draw("Fsames")

######CMS 8TeV, two photons
mass_cms_8TeV_2g = np.array([198., 227., 256., 256., 227., 198.])
ctau_cms_8TeV_2g  = np.array([0.4, 2, 9, 9, 25., 50.])
graph_exclusion_cms_8TeV_2g = TGraph(6, mass_cms_8TeV_2g, ctau_cms_8TeV_2g)
graph_exclusion_cms_8TeV_2g.SetFillColorAlpha(kGray+1, 0.65)
graph_exclusion_cms_8TeV_2g.Draw("Fsames")


####legend
leg_2d_exclusion_withTCorr = TLegend(0.25,0.64,0.92,0.91)
leg_2d_exclusion_withTCorr.SetBorderSize(0)
leg_2d_exclusion_withTCorr.SetTextSize(0.03)
leg_2d_exclusion_withTCorr.SetLineColor(1)
leg_2d_exclusion_withTCorr.SetLineStyle(1)
leg_2d_exclusion_withTCorr.SetLineWidth(1)
leg_2d_exclusion_withTCorr.SetFillColor(0)
leg_2d_exclusion_withTCorr.SetFillStyle(1001)

leg_2d_exclusion_withTCorr.AddEntry(graph_exclusion_exp_withTCorr, "CMS Exp (#pm 1#sigma) 13 TeV, #gamma#gamma + #slash{E}_{T}", "LF")
if drawObs:
	leg_2d_exclusion_withTCorr.AddEntry(graph_exclusion_obs_withTCorr, "CMS Obs 13 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_withTCorr.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_withTCorr.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_withTCorr.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_withTCorr.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion_withTCorr.Draw()

drawCMS2(myC2D, 13, lumi_withTCorr)

#Lambda axis
f1_lambda = TF1("f1","(x+6.00)/1.454",72.902, 416.78)
A1_lambda = TGaxis(100.0, 0.0015,600.0,0.0015,"f1",1010)
A1_lambda.SetLabelFont(42)
A1_lambda.SetLabelSize(0.035)
A1_lambda.SetTextFont(42)
A1_lambda.SetTextSize(1.2)
A1_lambda.SetTitle("#Lambda [TeV]")
A1_lambda.SetTitleSize(0.04)
A1_lambda.SetTitleOffset(0.9)
A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_withTCorr.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_withTCorr.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_withTCorr.C")

###noTCorr only
graph_exclusion_exp_noTCorr = TGraph(len(lambda_point_boundary_exp_noTCorr), np.array(1.454*lambda_point_boundary_exp_noTCorr-6.0), np.array(ctau_points))
graph_exclusion_exp_p1sig_noTCorr = TGraph(len(lambda_point_boundary_exp_p1sig_noTCorr), np.array(1.454*lambda_point_boundary_exp_p1sig_noTCorr-6.0), np.array(ctau_points))
graph_exclusion_exp_m1sig_noTCorr = TGraph(len(lambda_point_boundary_exp_m1sig_noTCorr), np.array(1.454*lambda_point_boundary_exp_m1sig_noTCorr-6.0), np.array(ctau_points))
graph_exclusion_exp_pm1sig_noTCorr = TGraph(len(lambda_point_boundary_exp_pm1sig_noTCorr), np.array(1.454*np.array(lambda_point_boundary_exp_pm1sig_noTCorr)-6.0), np.array(ctau_points_loop))
graph_exclusion_obs_noTCorr = TGraph(len(lambda_point_boundary_obs_noTCorr), np.array(1.454*lambda_point_boundary_obs_noTCorr-6.0), np.array(ctau_points))

graph_exclusion_exp_noTCorr.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_noTCorr.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_noTCorr.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_noTCorr.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_noTCorr.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_noTCorr.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_noTCorr.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_noTCorr.GetYaxis().SetRangeUser(0.05,1.0e7)
graph_exclusion_exp_noTCorr.SetTitle("")

graph_exclusion_exp_noTCorr.SetMarkerStyle(19)
graph_exclusion_exp_noTCorr.SetMarkerSize(0.0)
graph_exclusion_exp_noTCorr.SetLineColor(kOrange - 9)
graph_exclusion_exp_noTCorr.SetLineWidth(3)
graph_exclusion_exp_noTCorr.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_noTCorr.SetFillStyle(3353)
#graph_exclusion_exp_noTCorr.SetLineStyle(kDashed)

graph_exclusion_exp_p1sig_noTCorr.SetMarkerStyle(19)
graph_exclusion_exp_p1sig_noTCorr.SetMarkerSize(0.0)
graph_exclusion_exp_p1sig_noTCorr.SetLineColor(kOrange - 9)
graph_exclusion_exp_p1sig_noTCorr.SetLineWidth(2)
graph_exclusion_exp_p1sig_noTCorr.SetLineStyle(kDashed)

graph_exclusion_exp_m1sig_noTCorr.SetMarkerStyle(19)
graph_exclusion_exp_m1sig_noTCorr.SetMarkerSize(0.0)
graph_exclusion_exp_m1sig_noTCorr.SetLineColor(kOrange - 9)
graph_exclusion_exp_m1sig_noTCorr.SetLineWidth(2)
graph_exclusion_exp_m1sig_noTCorr.SetLineStyle(kDashed)

graph_exclusion_exp_pm1sig_noTCorr.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_pm1sig_noTCorr.SetFillStyle(3353)

graph_exclusion_obs_noTCorr.SetMarkerStyle(19)
graph_exclusion_obs_noTCorr.SetMarkerSize(0.0)
graph_exclusion_obs_noTCorr.SetLineColor(kBlack)
graph_exclusion_obs_noTCorr.SetLineWidth(3)
graph_exclusion_obs_noTCorr.SetLineStyle(kDashed)

#graph_exclusion_exp_noTCorr.SetFillColor(kAzure + 7)
#graph_exclusion_exp_noTCorr.SetFillColorAlpha(kOrange - 9, 0.65)

graph_exclusion_exp_noTCorr.Draw("AL")
graph_exclusion_exp_pm1sig_noTCorr.Draw("Fsame")
#graph_exclusion_exp_p1sig_noTCorr.Draw("Lsame")
#graph_exclusion_exp_m1sig_noTCorr.Draw("Lsame")
if drawObs:
	graph_exclusion_obs_noTCorr.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_noTCorr = TLegend(0.25,0.64,0.92,0.91)
leg_2d_exclusion_noTCorr.SetBorderSize(0)
leg_2d_exclusion_noTCorr.SetTextSize(0.03)
leg_2d_exclusion_noTCorr.SetLineColor(1)
leg_2d_exclusion_noTCorr.SetLineStyle(1)
leg_2d_exclusion_noTCorr.SetLineWidth(1)
leg_2d_exclusion_noTCorr.SetFillColor(0)
leg_2d_exclusion_noTCorr.SetFillStyle(1001)

leg_2d_exclusion_noTCorr.AddEntry(graph_exclusion_exp_noTCorr, "CMS Exp (#pm 1#sigma) 13 TeV, #gamma + #slash{E}_{T}", "LF")
if drawObs:
	leg_2d_exclusion_noTCorr.AddEntry(graph_exclusion_obs_noTCorr, "CMS Obs 13 TeV, #gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_noTCorr.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_noTCorr.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_noTCorr.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_noTCorr.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion_noTCorr.Draw()

drawCMS2(myC2D, 13, lumi_noTCorr)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_noTCorr.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_noTCorr.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_noTCorr.C")

###overlay noTCorr and noTCorr

graph_exclusion_exp_withTCorr.SetMarkerStyle(19)
graph_exclusion_exp_withTCorr.SetLineColor(kGray+1)
graph_exclusion_exp_withTCorr.SetFillColorAlpha(kGray+1, 0.85)
graph_exclusion_exp_withTCorr.SetFillStyle(3356)
graph_exclusion_exp_p1sig_withTCorr.SetLineColor(kGray+1)
graph_exclusion_exp_m1sig_withTCorr.SetLineColor(kGray+1)
graph_exclusion_exp_pm1sig_withTCorr.SetFillColorAlpha(kGray+1, 0.85)
graph_exclusion_exp_pm1sig_withTCorr.SetFillStyle(3356)
graph_exclusion_obs_withTCorr.SetMarkerStyle(19)
graph_exclusion_obs_withTCorr.SetLineColor(kBlack)

graph_exclusion_exp_noTCorr.SetMarkerStyle(19)
graph_exclusion_exp_noTCorr.SetLineColor(4)
graph_exclusion_exp_noTCorr.SetFillColorAlpha(4, 0.65)
graph_exclusion_exp_noTCorr.SetFillStyle(3365)
graph_exclusion_exp_p1sig_noTCorr.SetLineColor(4)
graph_exclusion_exp_m1sig_noTCorr.SetLineColor(4)
graph_exclusion_exp_pm1sig_noTCorr.SetFillColorAlpha(4, 0.65)
graph_exclusion_exp_pm1sig_noTCorr.SetFillStyle(3365)
graph_exclusion_obs_noTCorr.SetMarkerStyle(19)
graph_exclusion_obs_noTCorr.SetLineColor(kBlack)


graph_exclusion_exp_noTCorr.Draw("AL")
#graph_exclusion_exp_p1sig_noTCorr.Draw("Lsame")
#graph_exclusion_exp_m1sig_noTCorr.Draw("Lsame")
graph_exclusion_exp_pm1sig_noTCorr.Draw("Fsame")
graph_exclusion_exp_withTCorr.Draw("Lsame")
#graph_exclusion_exp_p1sig_withTCorr.Draw("Lsame")
#graph_exclusion_exp_m1sig_withTCorr.Draw("Lsame")
graph_exclusion_exp_pm1sig_withTCorr.Draw("Fsame")
if drawObs:
	graph_exclusion_obs_withTCorr.Draw("Lsames")
	graph_exclusion_obs_noTCorr.Draw("Lsames")

#graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
#graph_exclusion_cms_7TeV_1g.Draw("Fsames")
#graph_exclusion_cms_8TeV_1g.Draw("Fsames")
#graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_withTCorr_noTCorr = TLegend(0.2,0.74,0.92,0.91)
leg_2d_exclusion_withTCorr_noTCorr.SetBorderSize(0)
leg_2d_exclusion_withTCorr_noTCorr.SetTextSize(0.03)
leg_2d_exclusion_withTCorr_noTCorr.SetLineColor(1)
leg_2d_exclusion_withTCorr_noTCorr.SetLineStyle(1)
leg_2d_exclusion_withTCorr_noTCorr.SetLineWidth(1)
leg_2d_exclusion_withTCorr_noTCorr.SetFillColor(0)
leg_2d_exclusion_withTCorr_noTCorr.SetFillStyle(1001)

leg_2d_exclusion_withTCorr_noTCorr.AddEntry(graph_exclusion_exp_withTCorr, "CMS Exp (#pm 1#sigma) 2016, with time correction", "LF")
leg_2d_exclusion_withTCorr_noTCorr.AddEntry(graph_exclusion_exp_noTCorr, "CMS Exp (#pm 1#sigma) 2016, no time correction", "LF")
if drawObs:
	leg_2d_exclusion_withTCorr_noTCorr.AddEntry(graph_exclusion_obs_withTCorr, "CMS Obs withTCorr data, #gamma#gamma + #slash{E}_{T}", "L")
	leg_2d_exclusion_withTCorr_noTCorr.AddEntry(graph_exclusion_obs_noTCorr, "CMS Obs noTCorr data, #gamma#gamma + #slash{E}_{T}", "L")
#leg_2d_exclusion_withTCorr_noTCorr.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
#leg_2d_exclusion_withTCorr_noTCorr.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
#leg_2d_exclusion_withTCorr_noTCorr.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
#leg_2d_exclusion_withTCorr_noTCorr.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion_withTCorr_noTCorr.Draw()

drawCMS2(myC2D, 13, lumi)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_withTCorr_noTCorr.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_withTCorr_noTCorr.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_withTCorr_noTCorr.C")

