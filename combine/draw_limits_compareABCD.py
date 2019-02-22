from ROOT import gROOT, gStyle, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TGraph, kDashed, kGreen, kYellow, TF1, kPink, kGray, TGaxis
import os, sys
from Aux import *
import numpy as np
import array

lumi = 35922.0
outputDir = '/data/zhicaiz/www/sharebox/DelayedPhoton/14Feb2019/orderByPt/'

plotABCDLabel = "_MaxSignificanceMethod"

datacards_template = "../fit_results/2016Template/datacards_3J_noBDT/"
datacards_ABCD_2x2 = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/2016ABCD_OptimizeSignificance/2016ABCD_2x2/datacards_3J_noBDT/"
datacards_ABCD_3x3 = "/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/2016ABCD_OptimizeSignificance/2016ABCD_3x3/datacards_3J_noBDT/"


lambda_points = [100, 150, 200, 250, 300, 350, 400]
ctau_points = [0.001, 0.1, 10, 200, 400, 600, 800, 1000, 1200, 10000]


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

r_exp_2d_grid_template = np.zeros((N_ctau, N_lambda))
r_exp_p1sig_2d_grid_template = np.zeros((N_ctau, N_lambda))
r_exp_m1sig_2d_grid_template = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_template = np.zeros((N_ctau, N_lambda))

r_exp_2d_grid_ABCD_2x2 = np.zeros((N_ctau, N_lambda))
r_exp_p1sig_2d_grid_ABCD_2x2 = np.zeros((N_ctau, N_lambda))
r_exp_m1sig_2d_grid_ABCD_2x2 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_ABCD_2x2 = np.zeros((N_ctau, N_lambda))

r_exp_2d_grid_ABCD_3x3 = np.zeros((N_ctau, N_lambda))
r_exp_p1sig_2d_grid_ABCD_3x3 = np.zeros((N_ctau, N_lambda))
r_exp_m1sig_2d_grid_ABCD_3x3 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_ABCD_3x3 = np.zeros((N_ctau, N_lambda))


print "initial value of the 2D r grid (exp, ABCD_3x3): "
print r_exp_2d_grid_ABCD_3x3
print "initial value of the 2D r grid (obs, ABCD_3x3): "
print r_obs_2d_grid_ABCD_3x3

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

	limit_this_template_exp2p5 = []
	limit_this_template_exp16p0 = []
	limit_this_template_exp50p0 = []
	limit_this_template_exp84p0 = []
	limit_this_template_exp97p5 = []
	limit_this_template_obs = []

	limit_this_ABCD_2x2_exp2p5 = []
	limit_this_ABCD_2x2_exp16p0 = []
	limit_this_ABCD_2x2_exp50p0 = []
	limit_this_ABCD_2x2_exp84p0 = []
	limit_this_ABCD_2x2_exp97p5 = []
	limit_this_ABCD_2x2_obs = []

	limit_this_ABCD_3x3_exp2p5 = []
	limit_this_ABCD_3x3_exp16p0 = []
	limit_this_ABCD_3x3_exp50p0 = []
	limit_this_ABCD_3x3_exp84p0 = []
	limit_this_ABCD_3x3_exp97p5 = []
	limit_this_ABCD_3x3_obs = []

	yValue_limit_this_template_exp = []
	yValue_limit_this_template_obs = []
	yValue_limit_this_template_exp1sigma = []
	yValue_limit_this_template_exp2sigma = []
	
	yValue_limit_this_ABCD_2x2_exp = []
	yValue_limit_this_ABCD_2x2_obs = []
	yValue_limit_this_ABCD_2x2_exp1sigma = []
	yValue_limit_this_ABCD_2x2_exp2sigma = []
		
	yValue_limit_this_ABCD_3x3_exp = []
	yValue_limit_this_ABCD_3x3_obs = []
	yValue_limit_this_ABCD_3x3_exp1sigma = []
	yValue_limit_this_ABCD_3x3_exp2sigma = []

	ctau_this_str = str(ctau_this)
	if ctau_this_str == "0.1":
		ctau_this_str = "0_1"
	if ctau_this_str == "0.01":
		ctau_this_str = "0_01"
	if ctau_this_str == "0.001":
		ctau_this_str = "0_001"

	index_lambda = - 1
	for lambda_this in lambda_points:
		index_lambda = index_lambda + 1
		minsize = 6100
		actualsize_template = 0
		actualsize_ABCD_2x2 = 0
		actualsize_ABCD_3x3 = 0
		if os.path.isfile(datacards_template+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root"):
			actualsize_template = os.path.getsize(datacards_template+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")	
		if os.path.isfile(datacards_ABCD_2x2+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root"):
			actualsize_ABCD_2x2 = os.path.getsize(datacards_ABCD_2x2+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")	
		if os.path.isfile(datacards_ABCD_3x3+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root"):
			actualsize_ABCD_3x3 = os.path.getsize(datacards_ABCD_3x3+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")	

		if actualsize_template > minsize and actualsize_ABCD_2x2 > minsize and actualsize_ABCD_3x3 > minsize:

			file_limit_template = TFile(datacards_template+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")
			limits_template = []
			limitTree_template = file_limit_template.Get("limit")
			for entry in limitTree_template:
				limits_template.append(entry.limit)
			print limits_template

			file_limit_ABCD_2x2 = TFile(datacards_ABCD_2x2+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")
			limits_ABCD_2x2 = []
			limitTree_ABCD_2x2 = file_limit_ABCD_2x2.Get("limit")
			for entry in limitTree_ABCD_2x2:
				limits_ABCD_2x2.append(entry.limit)
			print limits_ABCD_2x2

			file_limit_ABCD_3x3 = TFile(datacards_ABCD_3x3+"/higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")
			limits_ABCD_3x3 = []
			limitTree_ABCD_3x3 = file_limit_ABCD_3x3.Get("limit")
			for entry in limitTree_ABCD_3x3:
				limits_ABCD_3x3.append(entry.limit)
			print limits_ABCD_3x3

			if len(limits_template) > 5 and len(limits_ABCD_2x2) > 5 and len(limits_ABCD_3x3) > 5:

				xValue_lambda.append(lambda_this)
				xValue_mass.append(lambda_this*1.454-6.0)
				th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)
				yValue_limit_this_Th.append(th_xsec_this)
				limit_this_template_exp2p5.append(limits_template[0]*th_xsec_this)	
				limit_this_template_exp16p0.append(limits_template[1]*th_xsec_this)	
				limit_this_template_exp50p0.append(limits_template[2]*th_xsec_this)	
				limit_this_template_exp84p0.append(limits_template[3]*th_xsec_this)	
				limit_this_template_exp97p5.append(limits_template[4]*th_xsec_this)	
				limit_this_template_obs.append(limits_template[5]*th_xsec_this)	

				r_exp_2d_grid_template[index_ctau][index_lambda] = limits_template[2]
				r_exp_p1sig_2d_grid_template[index_ctau][index_lambda] = limits_template[3]
				r_exp_m1sig_2d_grid_template[index_ctau][index_lambda] = limits_template[1]
				r_obs_2d_grid_template[index_ctau][index_lambda] = limits_template[5]

				limit_this_ABCD_2x2_exp2p5.append(limits_ABCD_2x2[0]*th_xsec_this)	
				limit_this_ABCD_2x2_exp16p0.append(limits_ABCD_2x2[1]*th_xsec_this)	
				limit_this_ABCD_2x2_exp50p0.append(limits_ABCD_2x2[2]*th_xsec_this)	
				limit_this_ABCD_2x2_exp84p0.append(limits_ABCD_2x2[3]*th_xsec_this)	
				limit_this_ABCD_2x2_exp97p5.append(limits_ABCD_2x2[4]*th_xsec_this)	
				limit_this_ABCD_2x2_obs.append(limits_ABCD_2x2[5]*th_xsec_this)	

				r_exp_2d_grid_ABCD_2x2[index_ctau][index_lambda] = limits_ABCD_2x2[2]
				r_exp_p1sig_2d_grid_ABCD_2x2[index_ctau][index_lambda] = limits_ABCD_2x2[3]
				r_exp_m1sig_2d_grid_ABCD_2x2[index_ctau][index_lambda] = limits_ABCD_2x2[1]
				r_obs_2d_grid_ABCD_2x2[index_ctau][index_lambda] = limits_ABCD_2x2[5]

				limit_this_ABCD_3x3_exp2p5.append(limits_ABCD_3x3[0]*th_xsec_this)	
				limit_this_ABCD_3x3_exp16p0.append(limits_ABCD_3x3[1]*th_xsec_this)	
				limit_this_ABCD_3x3_exp50p0.append(limits_ABCD_3x3[2]*th_xsec_this)	
				limit_this_ABCD_3x3_exp84p0.append(limits_ABCD_3x3[3]*th_xsec_this)	
				limit_this_ABCD_3x3_exp97p5.append(limits_ABCD_3x3[4]*th_xsec_this)	
				limit_this_ABCD_3x3_obs.append(limits_ABCD_3x3[5]*th_xsec_this)	

				r_exp_2d_grid_ABCD_3x3[index_ctau][index_lambda] = limits_ABCD_3x3[2]
				r_exp_p1sig_2d_grid_ABCD_3x3[index_ctau][index_lambda] = limits_ABCD_3x3[3]
				r_exp_m1sig_2d_grid_ABCD_3x3[index_ctau][index_lambda] = limits_ABCD_3x3[1]
				r_obs_2d_grid_ABCD_3x3[index_ctau][index_lambda] = limits_ABCD_3x3[5]

	NPoints_mass = len(xValue_mass)

	for i in range(0, NPoints_mass):
		xValue_mass.append(xValue_mass[i])
		xValue_mass_exp1sigma.append(xValue_mass[i])
		xValue_mass_exp2sigma.append(xValue_mass[i])
		
		yValue_limit_this_template_obs.append(limit_this_template_obs[i])
		yValue_limit_this_template_exp.append(limit_this_template_exp50p0[i])
		yValue_limit_this_template_exp1sigma.append(limit_this_template_exp16p0[i])
		yValue_limit_this_template_exp2sigma.append(limit_this_template_exp2p5[i])
			
		yValue_limit_this_ABCD_2x2_obs.append(limit_this_ABCD_2x2_obs[i])
		yValue_limit_this_ABCD_2x2_exp.append(limit_this_ABCD_2x2_exp50p0[i])
		yValue_limit_this_ABCD_2x2_exp1sigma.append(limit_this_ABCD_2x2_exp16p0[i])
		yValue_limit_this_ABCD_2x2_exp2sigma.append(limit_this_ABCD_2x2_exp2p5[i])
			
		yValue_limit_this_ABCD_3x3_obs.append(limit_this_ABCD_3x3_obs[i])
		yValue_limit_this_ABCD_3x3_exp.append(limit_this_ABCD_3x3_exp50p0[i])
		yValue_limit_this_ABCD_3x3_exp1sigma.append(limit_this_ABCD_3x3_exp16p0[i])
		yValue_limit_this_ABCD_3x3_exp2sigma.append(limit_this_ABCD_3x3_exp2p5[i])


	for i in range(0, NPoints_mass):
		xValue_mass_exp1sigma.append(xValue_mass[NPoints_mass-i-1])
		xValue_mass_exp2sigma.append(xValue_mass[NPoints_mass-i-1])
		
		yValue_limit_this_template_exp1sigma.append(limit_this_template_exp84p0[NPoints_mass-i-1])
		yValue_limit_this_template_exp2sigma.append(limit_this_template_exp97p5[NPoints_mass-i-1])

		yValue_limit_this_ABCD_2x2_exp1sigma.append(limit_this_ABCD_2x2_exp84p0[NPoints_mass-i-1])
		yValue_limit_this_ABCD_2x2_exp2sigma.append(limit_this_ABCD_2x2_exp97p5[NPoints_mass-i-1])
		
		yValue_limit_this_ABCD_3x3_exp1sigma.append(limit_this_ABCD_3x3_exp84p0[NPoints_mass-i-1])
		yValue_limit_this_ABCD_3x3_exp2sigma.append(limit_this_ABCD_3x3_exp97p5[NPoints_mass-i-1])

	myC.SetLogy(1)
	myC.SetLogx(0)
	
	#template
	graph_limit_vs_mass_template_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_template_obs))
	graph_limit_vs_mass_template_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_template_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_template_exp))
	graph_limit_vs_mass_template_exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp1sigma), np.array(yValue_limit_this_template_exp1sigma))
	graph_limit_vs_mass_template_exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp2sigma), np.array(yValue_limit_this_template_exp2sigma))

	graph_limit_vs_mass_template_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_template_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_template_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_template_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_template_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_template_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_template_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_template_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_template_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_template_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_template_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_template_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_template_exp_limit.SetLineStyle(kDashed)

	graph_limit_vs_mass_template_exp1sigma_limit.SetFillColor(kGreen)
	graph_limit_vs_mass_template_exp2sigma_limit.SetFillColor(kYellow)

	graph_limit_vs_mass_template_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_template_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_template_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_template_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_template_exp_limit.SetTitle("")

	graph_limit_vs_mass_template_exp_limit.Draw("LA")

	graph_limit_vs_mass_template_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_template_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_template_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_template_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	graph_limit_vs_mass_template_exp2sigma_limit.Draw("Fsame")
	graph_limit_vs_mass_template_exp1sigma_limit.Draw("Fsame")
	if drawObs:
		graph_limit_vs_mass_template_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_template_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_template_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_mass_template = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_template.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_template.SetBorderSize(0)
	leg_limit_vs_mass_template.SetTextSize(0.03)
	leg_limit_vs_mass_template.SetLineColor(1)
	leg_limit_vs_mass_template.SetLineStyle(1)
	leg_limit_vs_mass_template.SetLineWidth(1)
	leg_limit_vs_mass_template.SetFillColor(0)
	leg_limit_vs_mass_template.SetFillStyle(1001)

	leg_limit_vs_mass_template.AddEntry(graph_limit_vs_mass_template_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_template.AddEntry(graph_limit_vs_mass_template_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_template.AddEntry(graph_limit_vs_mass_template_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_template.AddEntry(graph_limit_vs_mass_template_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
	leg_limit_vs_mass_template.AddEntry(graph_limit_vs_mass_template_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
	leg_limit_vs_mass_template.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_template_ctau"+ctau_this_str+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_template_ctau"+ctau_this_str+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_template_ctau"+ctau_this_str+".C")

	#ABCD_2x2
	graph_limit_vs_mass_ABCD_2x2_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_ABCD_2x2_obs))
	graph_limit_vs_mass_ABCD_2x2_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_ABCD_2x2_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_ABCD_2x2_exp))
	graph_limit_vs_mass_ABCD_2x2_exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp1sigma), np.array(yValue_limit_this_ABCD_2x2_exp1sigma))
	graph_limit_vs_mass_ABCD_2x2_exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp2sigma), np.array(yValue_limit_this_ABCD_2x2_exp2sigma))

	graph_limit_vs_mass_ABCD_2x2_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_ABCD_2x2_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_ABCD_2x2_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_ABCD_2x2_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_ABCD_2x2_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_ABCD_2x2_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_ABCD_2x2_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_ABCD_2x2_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetLineStyle(kDashed)

	graph_limit_vs_mass_ABCD_2x2_exp1sigma_limit.SetFillColor(kGreen)
	graph_limit_vs_mass_ABCD_2x2_exp2sigma_limit.SetFillColor(kYellow)

	graph_limit_vs_mass_ABCD_2x2_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_ABCD_2x2_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_ABCD_2x2_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetTitle("")

	graph_limit_vs_mass_ABCD_2x2_exp_limit.Draw("LA")

	graph_limit_vs_mass_ABCD_2x2_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_ABCD_2x2_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_ABCD_2x2_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_ABCD_2x2_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	graph_limit_vs_mass_ABCD_2x2_exp2sigma_limit.Draw("Fsame")
	graph_limit_vs_mass_ABCD_2x2_exp1sigma_limit.Draw("Fsame")
	if drawObs:
		graph_limit_vs_mass_ABCD_2x2_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_ABCD_2x2_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_ABCD_2x2_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_mass_ABCD_2x2 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_ABCD_2x2.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_ABCD_2x2.SetBorderSize(0)
	leg_limit_vs_mass_ABCD_2x2.SetTextSize(0.03)
	leg_limit_vs_mass_ABCD_2x2.SetLineColor(1)
	leg_limit_vs_mass_ABCD_2x2.SetLineStyle(1)
	leg_limit_vs_mass_ABCD_2x2.SetLineWidth(1)
	leg_limit_vs_mass_ABCD_2x2.SetFillColor(0)
	leg_limit_vs_mass_ABCD_2x2.SetFillStyle(1001)

	leg_limit_vs_mass_ABCD_2x2.AddEntry(graph_limit_vs_mass_ABCD_2x2_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_ABCD_2x2.AddEntry(graph_limit_vs_mass_ABCD_2x2_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_ABCD_2x2.AddEntry(graph_limit_vs_mass_ABCD_2x2_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_ABCD_2x2.AddEntry(graph_limit_vs_mass_ABCD_2x2_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
	leg_limit_vs_mass_ABCD_2x2.AddEntry(graph_limit_vs_mass_ABCD_2x2_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
	leg_limit_vs_mass_ABCD_2x2.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_ABCD_2x2_ctau"+ctau_this_str+plotABCDLabel+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_ABCD_2x2_ctau"+ctau_this_str+plotABCDLabel+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_ABCD_2x2_ctau"+ctau_this_str+plotABCDLabel+".C")

	#ABCD_3x3
	graph_limit_vs_mass_ABCD_3x3_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_ABCD_3x3_obs))
	graph_limit_vs_mass_ABCD_3x3_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_ABCD_3x3_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_ABCD_3x3_exp))
	graph_limit_vs_mass_ABCD_3x3_exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp1sigma), np.array(yValue_limit_this_ABCD_3x3_exp1sigma))
	graph_limit_vs_mass_ABCD_3x3_exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp2sigma), np.array(yValue_limit_this_ABCD_3x3_exp2sigma))

	graph_limit_vs_mass_ABCD_3x3_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_ABCD_3x3_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_ABCD_3x3_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_ABCD_3x3_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_ABCD_3x3_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_ABCD_3x3_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_ABCD_3x3_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_ABCD_3x3_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetLineStyle(kDashed)

	graph_limit_vs_mass_ABCD_3x3_exp1sigma_limit.SetFillColor(kGreen)
	graph_limit_vs_mass_ABCD_3x3_exp2sigma_limit.SetFillColor(kYellow)

	graph_limit_vs_mass_ABCD_3x3_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_ABCD_3x3_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_ABCD_3x3_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetTitle("")

	graph_limit_vs_mass_ABCD_3x3_exp_limit.Draw("LA")

	graph_limit_vs_mass_ABCD_3x3_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_ABCD_3x3_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_ABCD_3x3_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_ABCD_3x3_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	graph_limit_vs_mass_ABCD_3x3_exp2sigma_limit.Draw("Fsame")
	graph_limit_vs_mass_ABCD_3x3_exp1sigma_limit.Draw("Fsame")
	if drawObs:
		graph_limit_vs_mass_ABCD_3x3_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_ABCD_3x3_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_ABCD_3x3_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_mass_ABCD_3x3 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_ABCD_3x3.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_ABCD_3x3.SetBorderSize(0)
	leg_limit_vs_mass_ABCD_3x3.SetTextSize(0.03)
	leg_limit_vs_mass_ABCD_3x3.SetLineColor(1)
	leg_limit_vs_mass_ABCD_3x3.SetLineStyle(1)
	leg_limit_vs_mass_ABCD_3x3.SetLineWidth(1)
	leg_limit_vs_mass_ABCD_3x3.SetFillColor(0)
	leg_limit_vs_mass_ABCD_3x3.SetFillStyle(1001)

	leg_limit_vs_mass_ABCD_3x3.AddEntry(graph_limit_vs_mass_ABCD_3x3_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_ABCD_3x3.AddEntry(graph_limit_vs_mass_ABCD_3x3_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_ABCD_3x3.AddEntry(graph_limit_vs_mass_ABCD_3x3_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_ABCD_3x3.AddEntry(graph_limit_vs_mass_ABCD_3x3_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
	leg_limit_vs_mass_ABCD_3x3.AddEntry(graph_limit_vs_mass_ABCD_3x3_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
	leg_limit_vs_mass_ABCD_3x3.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_ABCD_3x3_ctau"+ctau_this_str+plotABCDLabel+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_ABCD_3x3_ctau"+ctau_this_str+plotABCDLabel+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_ABCD_3x3_ctau"+ctau_this_str+plotABCDLabel+".C")

	###overlay template and ABCD_2x2 in the same plot

	graph_limit_vs_mass_template_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_template_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_template_exp_limit.SetLineColor(4)
	graph_limit_vs_mass_template_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetLineColor(7)
	graph_limit_vs_mass_ABCD_2x2_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetLineColor(6)
	graph_limit_vs_mass_ABCD_3x3_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_template_exp_limit.Draw("LA")
	graph_limit_vs_mass_ABCD_2x2_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_ABCD_3x3_exp_limit.Draw("Lsame")

	if drawObs:
		graph_limit_vs_mass_template_obs_limit.Draw("Lsame")
		graph_limit_vs_mass_ABCD_2x2_obs_limit.Draw("Lsame")
		graph_limit_vs_mass_ABCD_3x3_obs_limit.Draw("Lsame")

	graph_limit_vs_mass_template_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_mass = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass.SetBorderSize(0)
	leg_limit_vs_mass.SetTextSize(0.03)
	leg_limit_vs_mass.SetLineColor(1)
	leg_limit_vs_mass.SetLineStyle(1)
	leg_limit_vs_mass.SetLineWidth(1)
	leg_limit_vs_mass.SetFillColor(0)
	leg_limit_vs_mass.SetFillStyle(1001)

	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_template_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_template_obs_limit, "Observed  95% CL upper limit, template", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_template_exp_limit, "Expected  95% CL upper limit, template", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_ABCD_2x2_exp_limit, "Expected  95% CL upper limit, ABCD_2x2", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_ABCD_3x3_exp_limit, "Expected  95% CL upper limit, ABCD_3x3", "L")
	leg_limit_vs_mass.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_template_ABCD_ctau"+ctau_this_str+plotABCDLabel+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_template_ABCD_ctau"+ctau_this_str+plotABCDLabel+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_template_ABCD_ctau"+ctau_this_str+plotABCDLabel+".C")


##################exclusion region of ctau and Lambda/mass #######################

print "value of the 2D r grid (exp, template) provided from samples: "
print r_exp_2d_grid_template
print "value of the 2D r grid (obs, template) provided from samples: "
print r_obs_2d_grid_template


print "value of the 2D r grid (exp, ABCD_2x2) provided from samples: "
print r_exp_2d_grid_ABCD_2x2
print "value of the 2D r grid (obs, ABCD_2x2) provided from samples: "
print r_obs_2d_grid_ABCD_2x2

print "value of the 2D r grid (exp, ABCD_3x3) provided from samples: "
print r_exp_2d_grid_ABCD_3x3
print "value of the 2D r grid (obs, ABCD_3x3) provided from samples: "
print r_obs_2d_grid_ABCD_3x3

###linear interpolation to get the boundary points

lambda_point_boundary_exp_template = np.zeros(N_ctau)
lambda_point_boundary_exp_p1sig_template = np.zeros(N_ctau)
lambda_point_boundary_exp_m1sig_template = np.zeros(N_ctau)
lambda_point_boundary_obs_template = np.zeros(N_ctau)

lambda_point_boundary_exp_ABCD_2x2 = np.zeros(N_ctau)
lambda_point_boundary_exp_p1sig_ABCD_2x2 = np.zeros(N_ctau)
lambda_point_boundary_exp_m1sig_ABCD_2x2 = np.zeros(N_ctau)
lambda_point_boundary_obs_ABCD_2x2 = np.zeros(N_ctau)

lambda_point_boundary_exp_ABCD_3x3 = np.zeros(N_ctau)
lambda_point_boundary_exp_p1sig_ABCD_3x3 = np.zeros(N_ctau)
lambda_point_boundary_exp_m1sig_ABCD_3x3 = np.zeros(N_ctau)
lambda_point_boundary_obs_ABCD_3x3 = np.zeros(N_ctau)


for i in range(0, N_ctau):
	print "doing linear interpolation to get the boundary value of lambda for ctau = "+str(ctau_points[i])

	lambda_interp_template = []
	r_exp_interp_template = []
	r_exp_p1sig_interp_template = []
	r_exp_m1sig_interp_template = []
	r_obs_interp_template = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_template[i][j] > 0.00000001:
			lambda_interp_template.append(lambda_points[j]*1.0)
			r_exp_interp_template.append(r_exp_2d_grid_template[i][j]*1.0)
			r_exp_p1sig_interp_template.append(r_exp_p1sig_2d_grid_template[i][j]*1.0)
			r_exp_m1sig_interp_template.append(r_exp_m1sig_2d_grid_template[i][j]*1.0)
			r_obs_interp_template.append(r_obs_2d_grid_template[i][j]*1.0)
	graph_lambda_vs_r_exp_template =  TGraph(len(lambda_interp_template), np.array(r_exp_interp_template), np.array(lambda_interp_template))
	graph_lambda_vs_r_exp_p1sig_template =  TGraph(len(lambda_interp_template), np.array(r_exp_p1sig_interp_template), np.array(lambda_interp_template))
	graph_lambda_vs_r_exp_m1sig_template =  TGraph(len(lambda_interp_template), np.array(r_exp_m1sig_interp_template), np.array(lambda_interp_template))
	lambda_point_boundary_exp_template[i] = graph_lambda_vs_r_exp_template.Eval(1.0)
	lambda_point_boundary_exp_p1sig_template[i] = graph_lambda_vs_r_exp_p1sig_template.Eval(1.0)
	lambda_point_boundary_exp_m1sig_template[i] = graph_lambda_vs_r_exp_m1sig_template.Eval(1.0)
	graph_lambda_vs_r_obs_template =  TGraph(len(lambda_interp_template), np.array(r_obs_interp_template), np.array(lambda_interp_template))
	lambda_point_boundary_obs_template[i] = graph_lambda_vs_r_obs_template.Eval(1.0)

	lambda_interp_ABCD_2x2 = []
	r_exp_interp_ABCD_2x2 = []
	r_exp_p1sig_interp_ABCD_2x2 = []
	r_exp_m1sig_interp_ABCD_2x2 = []
	r_obs_interp_ABCD_2x2 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_ABCD_2x2[i][j] > 0.00000001:
			lambda_interp_ABCD_2x2.append(lambda_points[j]*1.0)
			r_exp_interp_ABCD_2x2.append(r_exp_2d_grid_ABCD_2x2[i][j]*1.0)
			r_exp_p1sig_interp_ABCD_2x2.append(r_exp_p1sig_2d_grid_ABCD_2x2[i][j]*1.0)
			r_exp_m1sig_interp_ABCD_2x2.append(r_exp_m1sig_2d_grid_ABCD_2x2[i][j]*1.0)
			r_obs_interp_ABCD_2x2.append(r_obs_2d_grid_ABCD_2x2[i][j]*1.0)
	graph_lambda_vs_r_exp_ABCD_2x2 =  TGraph(len(lambda_interp_ABCD_2x2), np.array(r_exp_interp_ABCD_2x2), np.array(lambda_interp_ABCD_2x2))
	graph_lambda_vs_r_exp_p1sig_ABCD_2x2 =  TGraph(len(lambda_interp_ABCD_2x2), np.array(r_exp_p1sig_interp_ABCD_2x2), np.array(lambda_interp_ABCD_2x2))
	graph_lambda_vs_r_exp_m1sig_ABCD_2x2 =  TGraph(len(lambda_interp_ABCD_2x2), np.array(r_exp_m1sig_interp_ABCD_2x2), np.array(lambda_interp_ABCD_2x2))
	lambda_point_boundary_exp_ABCD_2x2[i] = graph_lambda_vs_r_exp_ABCD_2x2.Eval(1.0)
	lambda_point_boundary_exp_p1sig_ABCD_2x2[i] = graph_lambda_vs_r_exp_p1sig_ABCD_2x2.Eval(1.0)
	lambda_point_boundary_exp_m1sig_ABCD_2x2[i] = graph_lambda_vs_r_exp_m1sig_ABCD_2x2.Eval(1.0)
	graph_lambda_vs_r_obs_ABCD_2x2 =  TGraph(len(lambda_interp_ABCD_2x2), np.array(r_obs_interp_ABCD_2x2), np.array(lambda_interp_ABCD_2x2))
	lambda_point_boundary_obs_ABCD_2x2[i] = graph_lambda_vs_r_obs_ABCD_2x2.Eval(1.0)

	lambda_interp_ABCD_3x3 = []
	r_exp_interp_ABCD_3x3 = []
	r_exp_p1sig_interp_ABCD_3x3 = []
	r_exp_m1sig_interp_ABCD_3x3 = []
	r_obs_interp_ABCD_3x3 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_ABCD_3x3[i][j] > 0.00000001:
			lambda_interp_ABCD_3x3.append(lambda_points[j]*1.0)
			r_exp_interp_ABCD_3x3.append(r_exp_2d_grid_ABCD_3x3[i][j]*1.0)
			r_exp_p1sig_interp_ABCD_3x3.append(r_exp_p1sig_2d_grid_ABCD_3x3[i][j]*1.0)
			r_exp_m1sig_interp_ABCD_3x3.append(r_exp_m1sig_2d_grid_ABCD_3x3[i][j]*1.0)
			r_obs_interp_ABCD_3x3.append(r_obs_2d_grid_ABCD_3x3[i][j]*1.0)
	graph_lambda_vs_r_exp_ABCD_3x3 =  TGraph(len(lambda_interp_ABCD_3x3), np.array(r_exp_interp_ABCD_3x3), np.array(lambda_interp_ABCD_3x3))
	graph_lambda_vs_r_exp_p1sig_ABCD_3x3 =  TGraph(len(lambda_interp_ABCD_3x3), np.array(r_exp_p1sig_interp_ABCD_3x3), np.array(lambda_interp_ABCD_3x3))
	graph_lambda_vs_r_exp_m1sig_ABCD_3x3 =  TGraph(len(lambda_interp_ABCD_3x3), np.array(r_exp_m1sig_interp_ABCD_3x3), np.array(lambda_interp_ABCD_3x3))
	lambda_point_boundary_exp_ABCD_3x3[i] = graph_lambda_vs_r_exp_ABCD_3x3.Eval(1.0)
	lambda_point_boundary_exp_p1sig_ABCD_3x3[i] = graph_lambda_vs_r_exp_p1sig_ABCD_3x3.Eval(1.0)
	lambda_point_boundary_exp_m1sig_ABCD_3x3[i] = graph_lambda_vs_r_exp_m1sig_ABCD_3x3.Eval(1.0)
	graph_lambda_vs_r_obs_ABCD_3x3 =  TGraph(len(lambda_interp_ABCD_3x3), np.array(r_obs_interp_ABCD_3x3), np.array(lambda_interp_ABCD_3x3))
	lambda_point_boundary_obs_ABCD_3x3[i] = graph_lambda_vs_r_obs_ABCD_3x3.Eval(1.0)


print "lambda points:"
print lambda_points

print "exp (template) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_template
print "exp p1sig (template) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_p1sig_template
print "exp m1sig (template) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_m1sig_template
print "obs (template) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_template

print "exp (ABCD_2x2) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_ABCD_2x2
print "exp p1sig (ABCD_2x2) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_p1sig_ABCD_2x2
print "exp m1sig (ABCD_2x2) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_m1sig_ABCD_2x2
print "obs (ABCD_2x2) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_ABCD_2x2

print "exp (ABCD_3x3) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_ABCD_3x3
print "exp p1sig (ABCD_3x3) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_p1sig_ABCD_3x3
print "exp m1sig (ABCD_3x3) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_m1sig_ABCD_3x3
print "obs (ABCD_3x3) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_ABCD_3x3

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

lambda_point_boundary_exp_pm1sig_template = []
lambda_point_boundary_exp_pm1sig_ABCD_2x2 = []
lambda_point_boundary_exp_pm1sig_ABCD_3x3 = []
ctau_points_loop = []

for i in range(0,len(ctau_points)):
	ctau_points_loop.append(ctau_points[i])
	lambda_point_boundary_exp_pm1sig_template.append(lambda_point_boundary_exp_p1sig_template[i]*1.0)
	lambda_point_boundary_exp_pm1sig_ABCD_2x2.append(lambda_point_boundary_exp_p1sig_ABCD_2x2[i]*1.0)
	lambda_point_boundary_exp_pm1sig_ABCD_3x3.append(lambda_point_boundary_exp_p1sig_ABCD_3x3[i]*1.0)

for i in range(0, len(ctau_points)):
	ctau_points_loop.append(ctau_points[len(ctau_points)-i-1]*1.0) 
	lambda_point_boundary_exp_pm1sig_template.append(lambda_point_boundary_exp_m1sig_template[len(ctau_points)-i-1]*1.0)
	lambda_point_boundary_exp_pm1sig_ABCD_2x2.append(lambda_point_boundary_exp_m1sig_ABCD_2x2[len(ctau_points)-i-1]*1.0)
	lambda_point_boundary_exp_pm1sig_ABCD_3x3.append(lambda_point_boundary_exp_m1sig_ABCD_3x3[len(ctau_points)-i-1]*1.0)

graph_exclusion_exp_template = TGraph(len(lambda_point_boundary_exp_template), np.array(1.454*lambda_point_boundary_exp_template-6.0), np.array(ctau_points))
graph_exclusion_exp_p1sig_template = TGraph(len(lambda_point_boundary_exp_p1sig_template), np.array(1.454*lambda_point_boundary_exp_p1sig_template-6.0), np.array(ctau_points))
graph_exclusion_exp_m1sig_template = TGraph(len(lambda_point_boundary_exp_m1sig_template), np.array(1.454*lambda_point_boundary_exp_m1sig_template-6.0), np.array(ctau_points))
graph_exclusion_exp_pm1sig_template = TGraph(len(lambda_point_boundary_exp_pm1sig_template), np.array(1.454*np.array(lambda_point_boundary_exp_pm1sig_template)-6.0), np.array(ctau_points_loop))
graph_exclusion_obs_template = TGraph(len(lambda_point_boundary_obs_template), np.array(1.454*lambda_point_boundary_obs_template-6.0), np.array(ctau_points))

graph_exclusion_exp_template.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_template.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_template.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_template.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_template.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_template.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_template.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_template.GetYaxis().SetRangeUser(0.001,1.0e10)
graph_exclusion_exp_template.SetTitle("")

graph_exclusion_exp_template.SetMarkerStyle(19)
graph_exclusion_exp_template.SetMarkerSize(0.0)
graph_exclusion_exp_template.SetLineColor(kOrange - 9)
graph_exclusion_exp_template.SetLineWidth(3)
graph_exclusion_exp_template.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_template.SetFillStyle(3353)
#graph_exclusion_exp_template.SetLineStyle(kDashed)

graph_exclusion_exp_p1sig_template.SetMarkerStyle(19)
graph_exclusion_exp_p1sig_template.SetMarkerSize(0.0)
graph_exclusion_exp_p1sig_template.SetLineColor(kOrange - 9)
graph_exclusion_exp_p1sig_template.SetLineWidth(2)
graph_exclusion_exp_p1sig_template.SetLineStyle(kDashed)

graph_exclusion_exp_m1sig_template.SetMarkerStyle(19)
graph_exclusion_exp_m1sig_template.SetMarkerSize(0.0)
graph_exclusion_exp_m1sig_template.SetLineColor(kOrange - 9)
graph_exclusion_exp_m1sig_template.SetLineWidth(2)
graph_exclusion_exp_m1sig_template.SetLineStyle(kDashed)

graph_exclusion_exp_pm1sig_template.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_pm1sig_template.SetFillStyle(3353)

graph_exclusion_obs_template.SetMarkerStyle(19)
graph_exclusion_obs_template.SetMarkerSize(0.0)
graph_exclusion_obs_template.SetLineColor(kBlack)
graph_exclusion_obs_template.SetLineWidth(3)
graph_exclusion_obs_template.SetLineStyle(kDashed)

#graph_exclusion_exp_template.SetFillColor(kAzure + 7)
#graph_exclusion_exp_template.SetFillColorAlpha(kOrange - 9, 0.65)

graph_exclusion_exp_template.Draw("AL")
#graph_exclusion_exp_p1sig_template.Draw("Lsame")
#graph_exclusion_exp_m1sig_template.Draw("Lsame")
graph_exclusion_exp_pm1sig_template.Draw("Fsame")

if drawObs:
	graph_exclusion_obs_template.Draw("Lsames")

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
leg_2d_exclusion_template = TLegend(0.25,0.64,0.92,0.91)
leg_2d_exclusion_template.SetBorderSize(0)
leg_2d_exclusion_template.SetTextSize(0.03)
leg_2d_exclusion_template.SetLineColor(1)
leg_2d_exclusion_template.SetLineStyle(1)
leg_2d_exclusion_template.SetLineWidth(1)
leg_2d_exclusion_template.SetFillColor(0)
leg_2d_exclusion_template.SetFillStyle(1001)

leg_2d_exclusion_template.AddEntry(graph_exclusion_exp_template, "CMS Exp (#pm 1#sigma) 13 TeV, #gamma#gamma + #slash{E}_{T}", "LF")
if drawObs:
	leg_2d_exclusion_template.AddEntry(graph_exclusion_obs_template, "CMS Obs 13 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_template.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_template.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_template.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_template.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion_template.Draw()

drawCMS2(myC2D, 13, lumi)

#Lambda axis
f1_lambda = TF1("f1","(x+6.00)/1.454",72.902, 416.78)
A1_lambda = TGaxis(100.0, 0.00001,600.0,0.00001,"f1",1010)
A1_lambda.SetLabelFont(42)
A1_lambda.SetLabelSize(0.035)
A1_lambda.SetTextFont(42)
A1_lambda.SetTextSize(1.2)
A1_lambda.SetTitle("#Lambda [TeV]")
A1_lambda.SetTitleSize(0.04)
A1_lambda.SetTitleOffset(0.9)
A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_template.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_template.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_template.C")

###ABCD_2x2 only
graph_exclusion_exp_ABCD_2x2 = TGraph(len(lambda_point_boundary_exp_ABCD_2x2), np.array(1.454*lambda_point_boundary_exp_ABCD_2x2-6.0), np.array(ctau_points))
graph_exclusion_exp_p1sig_ABCD_2x2 = TGraph(len(lambda_point_boundary_exp_p1sig_ABCD_2x2), np.array(1.454*lambda_point_boundary_exp_p1sig_ABCD_2x2-6.0), np.array(ctau_points))
graph_exclusion_exp_m1sig_ABCD_2x2 = TGraph(len(lambda_point_boundary_exp_m1sig_ABCD_2x2), np.array(1.454*lambda_point_boundary_exp_m1sig_ABCD_2x2-6.0), np.array(ctau_points))
graph_exclusion_exp_pm1sig_ABCD_2x2 = TGraph(len(lambda_point_boundary_exp_pm1sig_ABCD_2x2), np.array(1.454*np.array(lambda_point_boundary_exp_pm1sig_ABCD_2x2)-6.0), np.array(ctau_points_loop))
graph_exclusion_obs_ABCD_2x2 = TGraph(len(lambda_point_boundary_obs_ABCD_2x2), np.array(1.454*lambda_point_boundary_obs_ABCD_2x2-6.0), np.array(ctau_points))

graph_exclusion_exp_ABCD_2x2.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_ABCD_2x2.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_ABCD_2x2.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_ABCD_2x2.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_ABCD_2x2.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_ABCD_2x2.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_ABCD_2x2.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_ABCD_2x2.GetYaxis().SetRangeUser(0.001,1.0e10)
graph_exclusion_exp_ABCD_2x2.SetTitle("")

graph_exclusion_exp_ABCD_2x2.SetMarkerStyle(19)
graph_exclusion_exp_ABCD_2x2.SetMarkerSize(0.0)
graph_exclusion_exp_ABCD_2x2.SetLineColor(kOrange - 9)
graph_exclusion_exp_ABCD_2x2.SetLineWidth(3)
graph_exclusion_exp_ABCD_2x2.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_ABCD_2x2.SetFillStyle(3353)
#graph_exclusion_exp_ABCD_2x2.SetLineStyle(kDashed)

graph_exclusion_exp_p1sig_ABCD_2x2.SetMarkerStyle(19)
graph_exclusion_exp_p1sig_ABCD_2x2.SetMarkerSize(0.0)
graph_exclusion_exp_p1sig_ABCD_2x2.SetLineColor(kOrange - 9)
graph_exclusion_exp_p1sig_ABCD_2x2.SetLineWidth(2)
graph_exclusion_exp_p1sig_ABCD_2x2.SetLineStyle(kDashed)

graph_exclusion_exp_m1sig_ABCD_2x2.SetMarkerStyle(19)
graph_exclusion_exp_m1sig_ABCD_2x2.SetMarkerSize(0.0)
graph_exclusion_exp_m1sig_ABCD_2x2.SetLineColor(kOrange - 9)
graph_exclusion_exp_m1sig_ABCD_2x2.SetLineWidth(2)
graph_exclusion_exp_m1sig_ABCD_2x2.SetLineStyle(kDashed)

graph_exclusion_exp_pm1sig_ABCD_2x2.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_pm1sig_ABCD_2x2.SetFillStyle(3353)

graph_exclusion_obs_ABCD_2x2.SetMarkerStyle(19)
graph_exclusion_obs_ABCD_2x2.SetMarkerSize(0.0)
graph_exclusion_obs_ABCD_2x2.SetLineColor(kBlack)
graph_exclusion_obs_ABCD_2x2.SetLineWidth(3)
graph_exclusion_obs_ABCD_2x2.SetLineStyle(kDashed)

#graph_exclusion_exp_ABCD_2x2.SetFillColor(kAzure + 7)
#graph_exclusion_exp_ABCD_2x2.SetFillColorAlpha(kOrange - 9, 0.65)

graph_exclusion_exp_ABCD_2x2.Draw("AL")
graph_exclusion_exp_pm1sig_ABCD_2x2.Draw("Fsame")
#graph_exclusion_exp_p1sig_ABCD_2x2.Draw("Lsame")
#graph_exclusion_exp_m1sig_ABCD_2x2.Draw("Lsame")
if drawObs:
	graph_exclusion_obs_ABCD_2x2.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_ABCD_2x2 = TLegend(0.25,0.64,0.92,0.91)
leg_2d_exclusion_ABCD_2x2.SetBorderSize(0)
leg_2d_exclusion_ABCD_2x2.SetTextSize(0.03)
leg_2d_exclusion_ABCD_2x2.SetLineColor(1)
leg_2d_exclusion_ABCD_2x2.SetLineStyle(1)
leg_2d_exclusion_ABCD_2x2.SetLineWidth(1)
leg_2d_exclusion_ABCD_2x2.SetFillColor(0)
leg_2d_exclusion_ABCD_2x2.SetFillStyle(1001)

leg_2d_exclusion_ABCD_2x2.AddEntry(graph_exclusion_exp_ABCD_2x2, "CMS Exp (#pm 1#sigma) 13 TeV, #gamma#gamma + #slash{E}_{T}", "LF")
if drawObs:
	leg_2d_exclusion_ABCD_2x2.AddEntry(graph_exclusion_obs_ABCD_2x2, "CMS Obs 13 TeV, #gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_ABCD_2x2.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_ABCD_2x2.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_ABCD_2x2.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_ABCD_2x2.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion_ABCD_2x2.Draw()

drawCMS2(myC2D, 13, lumi)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_ABCD_2x2.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_ABCD_2x2.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_ABCD_2x2.C")


###ABCD_3x3 only
graph_exclusion_exp_ABCD_3x3 = TGraph(len(lambda_point_boundary_exp_ABCD_3x3), np.array(1.454*lambda_point_boundary_exp_ABCD_3x3-6.0), np.array(ctau_points))
graph_exclusion_exp_p1sig_ABCD_3x3 = TGraph(len(lambda_point_boundary_exp_p1sig_ABCD_3x3), np.array(1.454*lambda_point_boundary_exp_p1sig_ABCD_3x3-6.0), np.array(ctau_points))
graph_exclusion_exp_m1sig_ABCD_3x3 = TGraph(len(lambda_point_boundary_exp_m1sig_ABCD_3x3), np.array(1.454*lambda_point_boundary_exp_m1sig_ABCD_3x3-6.0), np.array(ctau_points))
graph_exclusion_exp_pm1sig_ABCD_3x3 = TGraph(len(lambda_point_boundary_exp_pm1sig_ABCD_3x3), np.array(1.454*np.array(lambda_point_boundary_exp_pm1sig_ABCD_3x3)-6.0), np.array(ctau_points_loop))
graph_exclusion_obs_ABCD_3x3 = TGraph(len(lambda_point_boundary_obs_ABCD_3x3), np.array(1.454*lambda_point_boundary_obs_ABCD_3x3-6.0), np.array(ctau_points))

graph_exclusion_exp_ABCD_3x3.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_ABCD_3x3.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_ABCD_3x3.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_ABCD_3x3.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_ABCD_3x3.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_ABCD_3x3.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_ABCD_3x3.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_ABCD_3x3.GetYaxis().SetRangeUser(0.001,1.0e10)
graph_exclusion_exp_ABCD_3x3.SetTitle("")

graph_exclusion_exp_ABCD_3x3.SetMarkerStyle(19)
graph_exclusion_exp_ABCD_3x3.SetMarkerSize(0.0)
graph_exclusion_exp_ABCD_3x3.SetLineColor(kOrange - 9)
graph_exclusion_exp_ABCD_3x3.SetLineWidth(3)
graph_exclusion_exp_ABCD_3x3.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_ABCD_3x3.SetFillStyle(3353)
#graph_exclusion_exp_ABCD_3x3.SetLineStyle(kDashed)

graph_exclusion_exp_p1sig_ABCD_3x3.SetMarkerStyle(19)
graph_exclusion_exp_p1sig_ABCD_3x3.SetMarkerSize(0.0)
graph_exclusion_exp_p1sig_ABCD_3x3.SetLineColor(kOrange - 9)
graph_exclusion_exp_p1sig_ABCD_3x3.SetLineWidth(2)
graph_exclusion_exp_p1sig_ABCD_3x3.SetLineStyle(kDashed)

graph_exclusion_exp_m1sig_ABCD_3x3.SetMarkerStyle(19)
graph_exclusion_exp_m1sig_ABCD_3x3.SetMarkerSize(0.0)
graph_exclusion_exp_m1sig_ABCD_3x3.SetLineColor(kOrange - 9)
graph_exclusion_exp_m1sig_ABCD_3x3.SetLineWidth(2)
graph_exclusion_exp_m1sig_ABCD_3x3.SetLineStyle(kDashed)

graph_exclusion_exp_pm1sig_ABCD_3x3.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_pm1sig_ABCD_3x3.SetFillStyle(3353)

graph_exclusion_obs_ABCD_3x3.SetMarkerStyle(19)
graph_exclusion_obs_ABCD_3x3.SetMarkerSize(0.0)
graph_exclusion_obs_ABCD_3x3.SetLineColor(kBlack)
graph_exclusion_obs_ABCD_3x3.SetLineWidth(3)
graph_exclusion_obs_ABCD_3x3.SetLineStyle(kDashed)

#graph_exclusion_exp_ABCD_3x3.SetFillColor(kAzure + 7)
#graph_exclusion_exp_ABCD_3x3.SetFillColorAlpha(kOrange - 9, 0.65)

graph_exclusion_exp_ABCD_3x3.Draw("AL")
graph_exclusion_exp_pm1sig_ABCD_3x3.Draw("Fsame")
#graph_exclusion_exp_p1sig_ABCD_3x3.Draw("Lsame")
#graph_exclusion_exp_m1sig_ABCD_3x3.Draw("Lsame")
if drawObs:
	graph_exclusion_obs_ABCD_3x3.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_ABCD_3x3 = TLegend(0.25,0.64,0.92,0.91)
leg_2d_exclusion_ABCD_3x3.SetBorderSize(0)
leg_2d_exclusion_ABCD_3x3.SetTextSize(0.03)
leg_2d_exclusion_ABCD_3x3.SetLineColor(1)
leg_2d_exclusion_ABCD_3x3.SetLineStyle(1)
leg_2d_exclusion_ABCD_3x3.SetLineWidth(1)
leg_2d_exclusion_ABCD_3x3.SetFillColor(0)
leg_2d_exclusion_ABCD_3x3.SetFillStyle(1001)

leg_2d_exclusion_ABCD_3x3.AddEntry(graph_exclusion_exp_ABCD_3x3, "CMS Exp (#pm 1#sigma) 13 TeV, #gamma#gamma + #slash{E}_{T}", "LF")
if drawObs:
	leg_2d_exclusion_ABCD_3x3.AddEntry(graph_exclusion_obs_ABCD_3x3, "CMS Obs 13 TeV, #gamma(#gamma) + #slash{E}_{T}", "L")
leg_2d_exclusion_ABCD_3x3.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_ABCD_3x3.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_ABCD_3x3.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_ABCD_3x3.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion_ABCD_3x3.Draw()

drawCMS2(myC2D, 13, lumi)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_ABCD_3x3.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_ABCD_3x3.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_ABCD_3x3.C")


###overlay ABCD_2x2 and ABCD_2x2

graph_exclusion_exp_template.SetMarkerStyle(19)
graph_exclusion_exp_template.SetLineColor(kGray+1)
graph_exclusion_exp_template.SetFillColorAlpha(kGray+1, 0.85)
graph_exclusion_exp_template.SetFillStyle(3356)
graph_exclusion_exp_p1sig_template.SetLineColor(kGray+1)
graph_exclusion_exp_m1sig_template.SetLineColor(kGray+1)
graph_exclusion_exp_pm1sig_template.SetFillColorAlpha(kGray+1, 0.85)
graph_exclusion_exp_pm1sig_template.SetFillStyle(3356)
graph_exclusion_obs_template.SetMarkerStyle(19)
graph_exclusion_obs_template.SetLineColor(kBlack)

graph_exclusion_exp_ABCD_2x2.SetMarkerStyle(19)
graph_exclusion_exp_ABCD_2x2.SetLineColor(4)
graph_exclusion_exp_ABCD_2x2.SetFillColorAlpha(4, 0.65)
graph_exclusion_exp_ABCD_2x2.SetFillStyle(3365)
graph_exclusion_exp_p1sig_ABCD_2x2.SetLineColor(4)
graph_exclusion_exp_m1sig_ABCD_2x2.SetLineColor(4)
graph_exclusion_exp_pm1sig_ABCD_2x2.SetFillColorAlpha(4, 0.65)
graph_exclusion_exp_pm1sig_ABCD_2x2.SetFillStyle(3365)
graph_exclusion_obs_ABCD_2x2.SetMarkerStyle(19)
graph_exclusion_obs_ABCD_2x2.SetLineColor(kBlack)

graph_exclusion_exp_ABCD_3x3.SetMarkerStyle(19)
graph_exclusion_exp_ABCD_3x3.SetLineColor(kPink)
graph_exclusion_exp_ABCD_3x3.SetFillColorAlpha(kPink, 0.65)
graph_exclusion_exp_ABCD_3x3.SetFillStyle(3344)
graph_exclusion_exp_p1sig_ABCD_3x3.SetLineColor(kPink)
graph_exclusion_exp_m1sig_ABCD_3x3.SetLineColor(kPink)
graph_exclusion_exp_pm1sig_ABCD_3x3.SetFillColorAlpha(kPink, 0.65)
graph_exclusion_exp_pm1sig_ABCD_3x3.SetFillStyle(3344)
graph_exclusion_obs_ABCD_3x3.SetMarkerStyle(19)
graph_exclusion_obs_ABCD_3x3.SetLineColor(kBlack)

graph_exclusion_exp_ABCD_2x2.Draw("AL")
#graph_exclusion_exp_p1sig_ABCD_2x2.Draw("Lsame")
#graph_exclusion_exp_m1sig_ABCD_2x2.Draw("Lsame")
graph_exclusion_exp_pm1sig_ABCD_2x2.Draw("Fsame")
graph_exclusion_exp_template.Draw("Lsame")
#graph_exclusion_exp_p1sig_template.Draw("Lsame")
#graph_exclusion_exp_m1sig_template.Draw("Lsame")
graph_exclusion_exp_pm1sig_template.Draw("Fsame")
graph_exclusion_exp_ABCD_3x3.Draw("Lsame")
#graph_exclusion_exp_p1sig_ABCD_3x3.Draw("Lsame")
#graph_exclusion_exp_m1sig_ABCD_3x3.Draw("Lsame")
graph_exclusion_exp_pm1sig_ABCD_3x3.Draw("Fsame")
if drawObs:
	graph_exclusion_obs_template.Draw("Lsames")
	graph_exclusion_obs_ABCD_2x2.Draw("Lsames")
	graph_exclusion_obs_ABCD_3x3.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_template_ABCD_2x2 = TLegend(0.2,0.64,0.92,0.91)
leg_2d_exclusion_template_ABCD_2x2.SetBorderSize(0)
leg_2d_exclusion_template_ABCD_2x2.SetTextSize(0.03)
leg_2d_exclusion_template_ABCD_2x2.SetLineColor(1)
leg_2d_exclusion_template_ABCD_2x2.SetLineStyle(1)
leg_2d_exclusion_template_ABCD_2x2.SetLineWidth(1)
leg_2d_exclusion_template_ABCD_2x2.SetFillColor(0)
leg_2d_exclusion_template_ABCD_2x2.SetFillStyle(1001)

leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_exp_template, "CMS Exp (#pm 1#sigma) 13 TeV (template), #gamma#gamma + #slash{E}_{T}", "LF")
leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_exp_ABCD_2x2, "CMS Exp (#pm 1#sigma) 13 TeV (ABCD 2x2), #gamma#gamma + #slash{E}_{T}", "LF")
leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_exp_ABCD_3x3, "CMS Exp (#pm 1#sigma) 13 TeV (ABCD 3x3), #gamma#gamma + #slash{E}_{T}", "LF")
if drawObs:
	leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_obs_template, "CMS Obs 13 TeV (template), #gamma#gamma + #slash{E}_{T}", "L")
	leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_obs_ABCD_2x2, "CMS Obs 13 TeV (ABCD 2x2), #gamma#gamma + #slash{E}_{T}", "L")
	leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_obs_ABCD_3x3, "CMS Obs 13 TeV (ABCD 3x3), #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_template_ABCD_2x2.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion_template_ABCD_2x2.Draw()

drawCMS2(myC2D, 13, lumi)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_template_ABCD"+plotABCDLabel+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_template_ABCD"+plotABCDLabel+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_template_ABCD"+plotABCDLabel+".C")

