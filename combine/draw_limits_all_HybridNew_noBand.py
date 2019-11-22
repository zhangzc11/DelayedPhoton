from ROOT import gROOT, gStyle, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TGraph, kDashed, kGreen, kYellow, TF1, kPink, kGray, TGaxis
import os, sys
from Aux import *
import numpy as np
import array

lumi_2016 = 35922.0
lumi_2017 = 41530.0
lumi = lumi_2016+lumi_2017
outputDir = '/data/zhicaiz/www/sharebox/DelayedPhoton/ARCReview_June2019/orderByPt/'

lambda_points = [100, 150, 200, 250, 300, 350, 400]
ctau_points = [10.0, 50, 100, 200, 400, 600, 800, 1000, 1200, 10000]


tree_dir = "limitTrees_v18_HybridNew"
plot_tag = "_v18_HybridNew_noBand"

drawObs=False
gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=200)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/limits")
os.system("cp draw_limits_all.py "+outputDir+"/limits")
#os.system("mkdir -p ../data")
#################plot settings###########################

axisTitleSize = 0.044
axisTitleOffset = 1.2
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

r_exp_2d_grid_2016 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_2016 = np.zeros((N_ctau, N_lambda))

r_exp_2d_grid_2017 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_2017 = np.zeros((N_ctau, N_lambda))

r_exp_2d_grid_2017CAT1 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_2017CAT1 = np.zeros((N_ctau, N_lambda))

r_exp_2d_grid_2017CAT2 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_2017CAT2 = np.zeros((N_ctau, N_lambda))

r_exp_2d_grid_2016And2017 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_2016And2017 = np.zeros((N_ctau, N_lambda))


print "initial value of the 2D r grid (exp, 2016And2017): "
print r_exp_2d_grid_2016And2017
print "initial value of the 2D r grid (obs, 2016And2017): "
print r_obs_2d_grid_2016And2017

##################limit vs mass #######################3

index_ctau = -1
for ctau_this in ctau_points:
	index_ctau = index_ctau + 1

	xValue_lambda = []
	xValue_mass = []
	yValue_limit_this_Th = []

	limit_this_2016_exp50p0 = []
	limit_this_2016_obs = []

	limit_this_2017_exp50p0 = []
	limit_this_2017_obs = []

	limit_this_2017CAT1_exp50p0 = []
	limit_this_2017CAT1_obs = []


	limit_this_2017CAT2_exp50p0 = []
	limit_this_2017CAT2_obs = []


	limit_this_2016And2017_exp50p0 = []
	limit_this_2016And2017_obs = []

	yValue_limit_this_2016_exp = []
	yValue_limit_this_2016_obs = []
	
	yValue_limit_this_2017_exp = []
	yValue_limit_this_2017_obs = []

	yValue_limit_this_2017CAT1_exp = []
	yValue_limit_this_2017CAT1_obs = []

	yValue_limit_this_2017CAT2_exp = []
	yValue_limit_this_2017CAT2_obs = []
		
	yValue_limit_this_2016And2017_exp = []
	yValue_limit_this_2016And2017_obs = []

	ctau_this_str = str(ctau_this)
	if ctau_this_str == "10.0":
		ctau_this_str = "10"
	if ctau_this_str == "0.1":
		ctau_this_str = "0p1"
	if ctau_this_str == "0.001":
		ctau_this_str = "0p001"
		
	index_lambda = - 1
	for lambda_this in lambda_points:
		print "limits for ctau = "+str(ctau_this)+" and lambda = "+str(lambda_this)
		index_lambda = index_lambda + 1
		limits_SF = 1.0
                if lambda_this == 100:
                        limits_SF = 0.01
                if lambda_this == 150 and ctau_this == 10:
                        limits_SF = 0.01
                if lambda_this == 150 and ctau_this == 50:
                        limits_SF = 0.01
                if lambda_this == 150 and ctau_this == 100:
                        limits_SF = 0.01
                if lambda_this == 150 and ctau_this == 200:
                        limits_SF = 0.01

		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2016_Observed.HybridNew.mH120.root"):
			continue
		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2016_Exp0p5.HybridNew.mH120.quant0.500.root"):
			continue

		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017CAT1_Observed.HybridNew.mH120.root"):
			continue
		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017CAT1_Exp0p5.HybridNew.mH120.quant0.500.root"):
			continue

		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017CAT2_Observed.HybridNew.mH120.root"):
			continue
		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017CAT2_Exp0p5.HybridNew.mH120.quant0.500.root"):
			continue

		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017_Observed.HybridNew.mH120.root"):
			continue
		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017_Exp0p5.HybridNew.mH120.quant0.500.root"):
			continue

		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2016And2017_Observed.HybridNew.mH120.root"):
			continue
		if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2016And2017_Exp0p5.HybridNew.mH120.quant0.500.root"):
			continue

		th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)



		limits_2016 = []
		file_limit_2016_exp0p5 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2016_Exp0p5.HybridNew.mH120.quant0.500.root")
		file_limit_2016_obs = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2016_Observed.HybridNew.mH120.root")
		limitTree_2016_exp0p5 = file_limit_2016_exp0p5.Get("limit")
		limitTree_2016_obs = file_limit_2016_obs.Get("limit")
		for entry in limitTree_2016_exp0p5:
			limits_2016.append(entry.limit)
		for entry in limitTree_2016_obs:
			limits_2016.append(entry.limit)
		print "2016 limits:"
		print limits_2016


		limits_2017 = []
		file_limit_2017_exp0p5 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017_Exp0p5.HybridNew.mH120.quant0.500.root")
		file_limit_2017_obs = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017_Observed.HybridNew.mH120.root")
		limitTree_2017_exp0p5 = file_limit_2017_exp0p5.Get("limit")
		limitTree_2017_obs = file_limit_2017_obs.Get("limit")
		for entry in limitTree_2017_exp0p5:
			limits_2017.append(entry.limit)
		for entry in limitTree_2017_obs:
			limits_2017.append(entry.limit)
		print "2017 limits:"
		print limits_2017


		limits_2017CAT1 = []
		file_limit_2017CAT1_exp0p5 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017CAT1_Exp0p5.HybridNew.mH120.quant0.500.root")
		file_limit_2017CAT1_obs = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017CAT1_Observed.HybridNew.mH120.root")
		limitTree_2017CAT1_exp0p5 = file_limit_2017CAT1_exp0p5.Get("limit")
		limitTree_2017CAT1_obs = file_limit_2017CAT1_obs.Get("limit")
		for entry in limitTree_2017CAT1_exp0p5:
			limits_2017CAT1.append(entry.limit)
		for entry in limitTree_2017CAT1_obs:
			limits_2017CAT1.append(entry.limit)
		print "2017CAT1 limits:"
		print limits_2017CAT1


		limits_2017CAT2 = []
		file_limit_2017CAT2_exp0p5 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017CAT2_Exp0p5.HybridNew.mH120.quant0.500.root")
		file_limit_2017CAT2_obs = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2017CAT2_Observed.HybridNew.mH120.root")
		limitTree_2017CAT2_exp0p5 = file_limit_2017CAT2_exp0p5.Get("limit")
		limitTree_2017CAT2_obs = file_limit_2017CAT2_obs.Get("limit")
		for entry in limitTree_2017CAT2_exp0p5:
			limits_2017CAT2.append(entry.limit)
		for entry in limitTree_2017CAT2_obs:
			limits_2017CAT2.append(entry.limit)
		print "2017CAT2 limits:"
		print limits_2017CAT2


		limits_2016And2017 = []
		file_limit_2016And2017_exp0p5 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2016And2017_Exp0p5.HybridNew.mH120.quant0.500.root")
		file_limit_2016And2017_obs = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_2016And2017_Observed.HybridNew.mH120.root")
		limitTree_2016And2017_exp0p5 = file_limit_2016And2017_exp0p5.Get("limit")
		limitTree_2016And2017_obs = file_limit_2016And2017_obs.Get("limit")
		for entry in limitTree_2016And2017_exp0p5:
			limits_2016And2017.append(entry.limit)
		for entry in limitTree_2016And2017_obs:
			limits_2016And2017.append(entry.limit)
		print "2016And2017 limits:"
		print limits_2016And2017


		if len(limits_2016) < 2 or len(limits_2017) < 2 or len(limits_2016And2017) < 2 or len(limits_2017CAT1) < 2 or len(limits_2017CAT2) < 2:
			continue
		
		for idx in range(len(limits_2016)):
			limits_2016[idx] = limits_2016[idx]*limits_SF
			limits_2017[idx] = limits_2017[idx]*limits_SF
			limits_2017CAT1[idx] = limits_2017CAT1[idx]*limits_SF
			limits_2017CAT2[idx] = limits_2017CAT2[idx]*limits_SF
			limits_2016And2017[idx] = limits_2016And2017[idx]*limits_SF

		xValue_lambda.append(lambda_this)
		xValue_mass.append(lambda_this*1.454-6.0)
		yValue_limit_this_Th.append(th_xsec_this)

		limit_this_2017_exp50p0.append(limits_2017[0]*th_xsec_this)	
		limit_this_2017_obs.append(limits_2017[1]*th_xsec_this)	

		limit_this_2017CAT1_exp50p0.append(limits_2017CAT1[0]*th_xsec_this)	
		limit_this_2017CAT1_obs.append(limits_2017CAT1[1]*th_xsec_this)	

		limit_this_2017CAT2_exp50p0.append(limits_2017CAT2[0]*th_xsec_this)	
		limit_this_2017CAT2_obs.append(limits_2017CAT2[1]*th_xsec_this)	

		limit_this_2016_exp50p0.append(limits_2016[0]*th_xsec_this)	
		limit_this_2016_obs.append(limits_2016[1]*th_xsec_this)	

		r_exp_2d_grid_2016[index_ctau][index_lambda] = limits_2016[0]
		r_obs_2d_grid_2016[index_ctau][index_lambda] = limits_2016[1]

		r_exp_2d_grid_2017[index_ctau][index_lambda] = limits_2017[0]
		r_obs_2d_grid_2017[index_ctau][index_lambda] = limits_2017[1]

		r_exp_2d_grid_2017CAT1[index_ctau][index_lambda] = limits_2017CAT1[0]
		r_obs_2d_grid_2017CAT1[index_ctau][index_lambda] = limits_2017CAT1[1]

		r_exp_2d_grid_2017CAT2[index_ctau][index_lambda] = limits_2017CAT2[0]
		r_obs_2d_grid_2017CAT2[index_ctau][index_lambda] = limits_2017CAT2[1]

		limit_this_2016And2017_exp50p0.append(limits_2016And2017[0]*th_xsec_this)	
		limit_this_2016And2017_obs.append(limits_2016And2017[1]*th_xsec_this)	

		r_exp_2d_grid_2016And2017[index_ctau][index_lambda] = limits_2016And2017[0]
		r_obs_2d_grid_2016And2017[index_ctau][index_lambda] = limits_2016And2017[1]

	NPoints_mass = len(xValue_mass)

	for i in range(0, NPoints_mass):
		xValue_mass.append(xValue_mass[i])
		
		yValue_limit_this_2016_obs.append(limit_this_2016_obs[i])
		yValue_limit_this_2016_exp.append(limit_this_2016_exp50p0[i])
			
		yValue_limit_this_2017_obs.append(limit_this_2017_obs[i])
		yValue_limit_this_2017_exp.append(limit_this_2017_exp50p0[i])

		yValue_limit_this_2017CAT1_obs.append(limit_this_2017CAT1_obs[i])
		yValue_limit_this_2017CAT1_exp.append(limit_this_2017CAT1_exp50p0[i])


		yValue_limit_this_2017CAT2_obs.append(limit_this_2017CAT2_obs[i])
		yValue_limit_this_2017CAT2_exp.append(limit_this_2017CAT2_exp50p0[i])
			
		yValue_limit_this_2016And2017_obs.append(limit_this_2016And2017_obs[i])
		yValue_limit_this_2016And2017_exp.append(limit_this_2016And2017_exp50p0[i])



	myC.SetLogy(1)
	myC.SetLogx(0)
	
	#2016
	graph_limit_vs_mass_2016_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2016_obs))
	graph_limit_vs_mass_2016_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_2016_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2016_exp))

	graph_limit_vs_mass_2016_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2016_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2016_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2016_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_2016_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2016_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2016_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_2016_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_2016_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2016_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2016_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2016_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_2016_exp_limit.SetLineStyle(kDashed)


	graph_limit_vs_mass_2016_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_2016_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_2016_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_2016_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_2016_exp_limit.SetTitle("")

	graph_limit_vs_mass_2016_exp_limit.Draw("LA")

	graph_limit_vs_mass_2016_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2016_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_2016_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2016_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	if drawObs:
		graph_limit_vs_mass_2016_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_2016_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_2016_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi_2016)

	leg_limit_vs_mass_2016 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_2016.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_2016.SetBorderSize(0)
	leg_limit_vs_mass_2016.SetTextSize(0.03)
	leg_limit_vs_mass_2016.SetLineColor(1)
	leg_limit_vs_mass_2016.SetLineStyle(1)
	leg_limit_vs_mass_2016.SetLineWidth(1)
	leg_limit_vs_mass_2016.SetFillColor(0)
	leg_limit_vs_mass_2016.SetFillStyle(1001)

	leg_limit_vs_mass_2016.AddEntry(graph_limit_vs_mass_2016_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_2016.AddEntry(graph_limit_vs_mass_2016_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_2016.AddEntry(graph_limit_vs_mass_2016_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_2016.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_ctau"+ctau_this_str+plot_tag+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_ctau"+ctau_this_str+plot_tag+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_ctau"+ctau_this_str+plot_tag+".C")

	#2017CAT1
	graph_limit_vs_mass_2017CAT1_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2017CAT1_obs))
	graph_limit_vs_mass_2017CAT1_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_2017CAT1_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2017CAT1_exp))

	graph_limit_vs_mass_2017CAT1_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2017CAT1_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017CAT1_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2017CAT1_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_2017CAT1_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2017CAT1_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017CAT1_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_2017CAT1_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_2017CAT1_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2017CAT1_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017CAT1_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2017CAT1_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_2017CAT1_exp_limit.SetLineStyle(kDashed)


	graph_limit_vs_mass_2017CAT1_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_2017CAT1_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_2017CAT1_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_2017CAT1_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_2017CAT1_exp_limit.SetTitle("")

	graph_limit_vs_mass_2017CAT1_exp_limit.Draw("LA")

	graph_limit_vs_mass_2017CAT1_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2017CAT1_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_2017CAT1_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2017CAT1_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	if drawObs:
		graph_limit_vs_mass_2017CAT1_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_2017CAT1_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_2017CAT1_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi_2017)

	leg_limit_vs_mass_2017CAT1 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_2017CAT1.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_2017CAT1.SetBorderSize(0)
	leg_limit_vs_mass_2017CAT1.SetTextSize(0.03)
	leg_limit_vs_mass_2017CAT1.SetLineColor(1)
	leg_limit_vs_mass_2017CAT1.SetLineStyle(1)
	leg_limit_vs_mass_2017CAT1.SetLineWidth(1)
	leg_limit_vs_mass_2017CAT1.SetFillColor(0)
	leg_limit_vs_mass_2017CAT1.SetFillStyle(1001)

	leg_limit_vs_mass_2017CAT1.AddEntry(graph_limit_vs_mass_2017CAT1_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_2017CAT1.AddEntry(graph_limit_vs_mass_2017CAT1_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_2017CAT1.AddEntry(graph_limit_vs_mass_2017CAT1_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_2017CAT1.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017CAT1_ctau"+ctau_this_str+plot_tag+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017CAT1_ctau"+ctau_this_str+plot_tag+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017CAT1_ctau"+ctau_this_str+plot_tag+".C")

	#2017CAT2
	graph_limit_vs_mass_2017CAT2_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2017CAT2_obs))
	graph_limit_vs_mass_2017CAT2_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_2017CAT2_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2017CAT2_exp))

	graph_limit_vs_mass_2017CAT2_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2017CAT2_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017CAT2_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2017CAT2_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_2017CAT2_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2017CAT2_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017CAT2_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_2017CAT2_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_2017CAT2_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2017CAT2_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017CAT2_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2017CAT2_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_2017CAT2_exp_limit.SetLineStyle(kDashed)


	graph_limit_vs_mass_2017CAT2_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_2017CAT2_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_2017CAT2_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_2017CAT2_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_2017CAT2_exp_limit.SetTitle("")

	graph_limit_vs_mass_2017CAT2_exp_limit.Draw("LA")

	graph_limit_vs_mass_2017CAT2_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2017CAT2_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_2017CAT2_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2017CAT2_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	if drawObs:
		graph_limit_vs_mass_2017CAT2_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_2017CAT2_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_2017CAT2_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi_2017)

	leg_limit_vs_mass_2017CAT2 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_2017CAT2.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_2017CAT2.SetBorderSize(0)
	leg_limit_vs_mass_2017CAT2.SetTextSize(0.03)
	leg_limit_vs_mass_2017CAT2.SetLineColor(1)
	leg_limit_vs_mass_2017CAT2.SetLineStyle(1)
	leg_limit_vs_mass_2017CAT2.SetLineWidth(1)
	leg_limit_vs_mass_2017CAT2.SetFillColor(0)
	leg_limit_vs_mass_2017CAT2.SetFillStyle(1001)

	leg_limit_vs_mass_2017CAT2.AddEntry(graph_limit_vs_mass_2017CAT2_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_2017CAT2.AddEntry(graph_limit_vs_mass_2017CAT2_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_2017CAT2.AddEntry(graph_limit_vs_mass_2017CAT2_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_2017CAT2.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017CAT2_ctau"+ctau_this_str+plot_tag+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017CAT2_ctau"+ctau_this_str+plot_tag+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017CAT2_ctau"+ctau_this_str+plot_tag+".C")



	#2017, all
	graph_limit_vs_mass_2017_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2017_obs))
	graph_limit_vs_mass_2017_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_2017_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2017_exp))

	graph_limit_vs_mass_2017_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2017_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2017_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_2017_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2017_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_2017_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_2017_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2017_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2017_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_2017_exp_limit.SetLineStyle(kDashed)


	graph_limit_vs_mass_2017_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_2017_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_2017_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_2017_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_2017_exp_limit.SetTitle("")

	graph_limit_vs_mass_2017_exp_limit.Draw("LA")

	graph_limit_vs_mass_2017_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2017_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_2017_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2017_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	if drawObs:
		graph_limit_vs_mass_2017_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_2017_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_2017_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi_2017)

	leg_limit_vs_mass_2017 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_2017.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_2017.SetBorderSize(0)
	leg_limit_vs_mass_2017.SetTextSize(0.03)
	leg_limit_vs_mass_2017.SetLineColor(1)
	leg_limit_vs_mass_2017.SetLineStyle(1)
	leg_limit_vs_mass_2017.SetLineWidth(1)
	leg_limit_vs_mass_2017.SetFillColor(0)
	leg_limit_vs_mass_2017.SetFillStyle(1001)

	leg_limit_vs_mass_2017.AddEntry(graph_limit_vs_mass_2017_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_2017.AddEntry(graph_limit_vs_mass_2017_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_2017.AddEntry(graph_limit_vs_mass_2017_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_2017.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017_ctau"+ctau_this_str+plot_tag+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017_ctau"+ctau_this_str+plot_tag+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2017_ctau"+ctau_this_str+plot_tag+".C")

	#2016And2017
	graph_limit_vs_mass_2016And2017_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2016And2017_obs))
	graph_limit_vs_mass_2016And2017_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_2016And2017_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2016And2017_exp))

	graph_limit_vs_mass_2016And2017_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2016And2017_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2016And2017_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2016And2017_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_2016And2017_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_2016And2017_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2016And2017_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_2016And2017_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_2016And2017_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2016And2017_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2016And2017_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_2016And2017_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_2016And2017_exp_limit.SetLineStyle(kDashed)


	graph_limit_vs_mass_2016And2017_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_2016And2017_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_2016And2017_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_2016And2017_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_2016And2017_exp_limit.SetTitle("")

	graph_limit_vs_mass_2016And2017_exp_limit.Draw("LA")

	graph_limit_vs_mass_2016And2017_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2016And2017_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_2016And2017_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_2016And2017_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	if drawObs:
		graph_limit_vs_mass_2016And2017_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_2016And2017_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_2016And2017_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_mass_2016And2017 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_2016And2017.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_2016And2017.SetBorderSize(0)
	leg_limit_vs_mass_2016And2017.SetTextSize(0.03)
	leg_limit_vs_mass_2016And2017.SetLineColor(1)
	leg_limit_vs_mass_2016And2017.SetLineStyle(1)
	leg_limit_vs_mass_2016And2017.SetLineWidth(1)
	leg_limit_vs_mass_2016And2017.SetFillColor(0)
	leg_limit_vs_mass_2016And2017.SetFillStyle(1001)

	leg_limit_vs_mass_2016And2017.AddEntry(graph_limit_vs_mass_2016And2017_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_2016And2017.AddEntry(graph_limit_vs_mass_2016And2017_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_2016And2017.AddEntry(graph_limit_vs_mass_2016And2017_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_2016And2017.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016And2017_ctau"+ctau_this_str+plot_tag+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016And2017_ctau"+ctau_this_str+plot_tag+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016And2017_ctau"+ctau_this_str+plot_tag+".C")

	###overlay 2016 and 2017 in the same plot

	graph_limit_vs_mass_2016_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2016_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2016_exp_limit.SetLineColor(4)
	graph_limit_vs_mass_2016_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_2017_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2017_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017_exp_limit.SetLineColor(7)
	graph_limit_vs_mass_2017_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_2017CAT1_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2017CAT1_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017CAT1_exp_limit.SetLineColor(5)
	graph_limit_vs_mass_2017CAT1_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_2017CAT2_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2017CAT2_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2017CAT2_exp_limit.SetLineColor(6)
	graph_limit_vs_mass_2017CAT2_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_2016And2017_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_2016And2017_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_2016And2017_exp_limit.SetLineColor(6)
	graph_limit_vs_mass_2016And2017_exp_limit.SetLineWidth(3)

	graph_limit_vs_mass_2016_exp_limit.Draw("LA")
	graph_limit_vs_mass_2017_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_2017CAT1_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_2017CAT2_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_2016And2017_exp_limit.Draw("Lsame")

	if drawObs:
		graph_limit_vs_mass_2016_obs_limit.Draw("Lsame")
		graph_limit_vs_mass_2017_obs_limit.Draw("Lsame")
		graph_limit_vs_mass_2017CAT1_obs_limit.Draw("Lsame")
		graph_limit_vs_mass_2017CAT1_obs_limit.Draw("Lsame")
		graph_limit_vs_mass_2016And2017_obs_limit.Draw("Lsame")

	graph_limit_vs_mass_2016_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_mass = TLegend(0.25,0.60,0.9,0.89)

	leg_limit_vs_mass.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass.SetBorderSize(0)
	leg_limit_vs_mass.SetTextSize(0.03)
	leg_limit_vs_mass.SetLineColor(1)
	leg_limit_vs_mass.SetLineStyle(1)
	leg_limit_vs_mass.SetLineWidth(1)
	leg_limit_vs_mass.SetFillColor(0)
	leg_limit_vs_mass.SetFillStyle(1001)

	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_2016_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_2016_obs_limit, "Observed  95% CL upper limit, 2016", "L")
		leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_2017_obs_limit, "Observed  95% CL upper limit, 2017", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_2016_exp_limit, "Expected  95% CL upper limit, 2016", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_2017CAT1_exp_limit, "Expected  95% CL upper limit, 2017 1#gamma", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_2017CAT2_exp_limit, "Expected  95% CL upper limit, 2017 2#gamma", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_2017_exp_limit, "Expected  95% CL upper limit, 2017 1+2#gamma", "L")
	leg_limit_vs_mass.AddEntry(graph_limit_vs_mass_2016And2017_exp_limit, "Expected  95% CL upper limit, 2016+2017", "L")
	leg_limit_vs_mass.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_2017_ctau"+ctau_this_str+plot_tag+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_2017_ctau"+ctau_this_str+plot_tag+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_2017_ctau"+ctau_this_str+plot_tag+".C")


##################exclusion region of ctau and Lambda/mass #######################

print "value of the 2D r grid (exp, 2016) provided from samples: "
print r_exp_2d_grid_2016
print "value of the 2D r grid (obs, 2016) provided from samples: "
print r_obs_2d_grid_2016


print "value of the 2D r grid (exp, 2017) provided from samples: "
print r_exp_2d_grid_2017
print "value of the 2D r grid (obs, 2017) provided from samples: "
print r_obs_2d_grid_2017


print "value of the 2D r grid (exp, 2017CAT1) provided from samples: "
print r_exp_2d_grid_2017CAT1
print "value of the 2D r grid (obs, 2017CAT1) provided from samples: "
print r_obs_2d_grid_2017CAT1


print "value of the 2D r grid (exp, 2017CAT2) provided from samples: "
print r_exp_2d_grid_2017CAT2
print "value of the 2D r grid (obs, 2017CAT2) provided from samples: "
print r_obs_2d_grid_2017CAT2

print "value of the 2D r grid (exp, 2016And2017) provided from samples: "
print r_exp_2d_grid_2016And2017
print "value of the 2D r grid (obs, 2016And2017) provided from samples: "
print r_obs_2d_grid_2016And2017

###linear interpolation to get the boundary points

lambda_point_boundary_exp_2016 = np.zeros(N_ctau)
lambda_point_boundary_obs_2016 = np.zeros(N_ctau)

lambda_point_boundary_exp_2017 = np.zeros(N_ctau)
lambda_point_boundary_obs_2017 = np.zeros(N_ctau)

lambda_point_boundary_exp_2017CAT1 = np.zeros(N_ctau)
lambda_point_boundary_obs_2017CAT1 = np.zeros(N_ctau)

lambda_point_boundary_exp_2017CAT2 = np.zeros(N_ctau)
lambda_point_boundary_obs_2017CAT2 = np.zeros(N_ctau)

lambda_point_boundary_exp_2016And2017 = np.zeros(N_ctau)
lambda_point_boundary_obs_2016And2017 = np.zeros(N_ctau)


for i in range(0, N_ctau):
	print "doing linear interpolation to get the boundary value of lambda for ctau = "+str(ctau_points[i])

	lambda_interp_2016 = []
	r_exp_interp_2016 = []
	r_obs_interp_2016 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_2016[i][j] > 0.00000001:
			lambda_interp_2016.append(lambda_points[j]*1.0)
			r_exp_interp_2016.append(r_exp_2d_grid_2016[i][j]*1.0)
			r_obs_interp_2016.append(r_obs_2d_grid_2016[i][j]*1.0)
	graph_lambda_vs_r_exp_2016 =  TGraph(len(lambda_interp_2016), np.array(r_exp_interp_2016), np.array(lambda_interp_2016))
	lambda_point_boundary_exp_2016[i] = graph_lambda_vs_r_exp_2016.Eval(1.0)
	graph_lambda_vs_r_obs_2016 =  TGraph(len(lambda_interp_2016), np.array(r_obs_interp_2016), np.array(lambda_interp_2016))
	lambda_point_boundary_obs_2016[i] = graph_lambda_vs_r_obs_2016.Eval(1.0)

	lambda_interp_2017 = []
	r_exp_interp_2017 = []
	r_obs_interp_2017 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_2017[i][j] > 0.00000001:
			lambda_interp_2017.append(lambda_points[j]*1.0)
			r_exp_interp_2017.append(r_exp_2d_grid_2017[i][j]*1.0)
			r_obs_interp_2017.append(r_obs_2d_grid_2017[i][j]*1.0)
	graph_lambda_vs_r_exp_2017 =  TGraph(len(lambda_interp_2017), np.array(r_exp_interp_2017), np.array(lambda_interp_2017))
	lambda_point_boundary_exp_2017[i] = graph_lambda_vs_r_exp_2017.Eval(1.0)
	graph_lambda_vs_r_obs_2017 =  TGraph(len(lambda_interp_2017), np.array(r_obs_interp_2017), np.array(lambda_interp_2017))
	lambda_point_boundary_obs_2017[i] = graph_lambda_vs_r_obs_2017.Eval(1.0)


	lambda_interp_2017CAT1 = []
	r_exp_interp_2017CAT1 = []
	r_obs_interp_2017CAT1 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_2017CAT1[i][j] > 0.00000001:
			lambda_interp_2017CAT1.append(lambda_points[j]*1.0)
			r_exp_interp_2017CAT1.append(r_exp_2d_grid_2017CAT1[i][j]*1.0)
			r_obs_interp_2017CAT1.append(r_obs_2d_grid_2017CAT1[i][j]*1.0)
	graph_lambda_vs_r_exp_2017CAT1 =  TGraph(len(lambda_interp_2017CAT1), np.array(r_exp_interp_2017CAT1), np.array(lambda_interp_2017CAT1))
	lambda_point_boundary_exp_2017CAT1[i] = graph_lambda_vs_r_exp_2017CAT1.Eval(1.0)
	graph_lambda_vs_r_obs_2017CAT1 =  TGraph(len(lambda_interp_2017CAT1), np.array(r_obs_interp_2017CAT1), np.array(lambda_interp_2017CAT1))
	lambda_point_boundary_obs_2017CAT1[i] = graph_lambda_vs_r_obs_2017CAT1.Eval(1.0)


	lambda_interp_2017CAT2 = []
	r_exp_interp_2017CAT2 = []
	r_obs_interp_2017CAT2 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_2017CAT2[i][j] > 0.00000001:
			lambda_interp_2017CAT2.append(lambda_points[j]*1.0)
			r_exp_interp_2017CAT2.append(r_exp_2d_grid_2017CAT2[i][j]*1.0)
			r_obs_interp_2017CAT2.append(r_obs_2d_grid_2017CAT2[i][j]*1.0)
	graph_lambda_vs_r_exp_2017CAT2 =  TGraph(len(lambda_interp_2017CAT2), np.array(r_exp_interp_2017CAT2), np.array(lambda_interp_2017CAT2))
	lambda_point_boundary_exp_2017CAT2[i] = graph_lambda_vs_r_exp_2017CAT2.Eval(1.0)
	graph_lambda_vs_r_obs_2017CAT2 =  TGraph(len(lambda_interp_2017CAT2), np.array(r_obs_interp_2017CAT2), np.array(lambda_interp_2017CAT2))
	lambda_point_boundary_obs_2017CAT2[i] = graph_lambda_vs_r_obs_2017CAT2.Eval(1.0)


	lambda_interp_2016And2017 = []
	r_exp_interp_2016And2017 = []
	r_obs_interp_2016And2017 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_2016And2017[i][j] > 0.00000001:
			lambda_interp_2016And2017.append(lambda_points[j]*1.0)
			r_exp_interp_2016And2017.append(r_exp_2d_grid_2016And2017[i][j]*1.0)
			r_obs_interp_2016And2017.append(r_obs_2d_grid_2016And2017[i][j]*1.0)
	graph_lambda_vs_r_exp_2016And2017 =  TGraph(len(lambda_interp_2016And2017), np.array(r_exp_interp_2016And2017), np.array(lambda_interp_2016And2017))
	lambda_point_boundary_exp_2016And2017[i] = graph_lambda_vs_r_exp_2016And2017.Eval(1.0)
	graph_lambda_vs_r_obs_2016And2017 =  TGraph(len(lambda_interp_2016And2017), np.array(r_obs_interp_2016And2017), np.array(lambda_interp_2016And2017))
	lambda_point_boundary_obs_2016And2017[i] = graph_lambda_vs_r_obs_2016And2017.Eval(1.0)


print "lambda points:"
print lambda_points

print "exp (2016) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_2016
print "obs (2016) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_2016

print "exp (2017) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_2017
print "obs (2017) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_2017

print "exp (2017CAT1) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_2017CAT1
print "obs (2017CAT1) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_2017CAT1

print "exp (2017CAT2) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_2017CAT2
print "obs (2017CAT2) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_2017CAT2

print "exp (2016And2017) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_2016And2017
print "obs (2016And2017) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_2016And2017

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

ctau_points_loop = []

for i in range(0,len(ctau_points)):
	ctau_points_loop.append(ctau_points[i])

for i in range(0, len(ctau_points)):
	ctau_points_loop.append(ctau_points[len(ctau_points)-i-1]*1.0) 

###2016 only
graph_exclusion_exp_2016 = TGraph(len(lambda_point_boundary_exp_2016), np.array(1.454*lambda_point_boundary_exp_2016-6.0), np.array(ctau_points))
graph_exclusion_obs_2016 = TGraph(len(lambda_point_boundary_obs_2016), np.array(1.454*lambda_point_boundary_obs_2016-6.0), np.array(ctau_points))

graph_exclusion_exp_2016.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2016.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2016.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2016.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2016.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_2016.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_2016.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_2016.GetYaxis().SetRangeUser(0.5,1.0e7)
graph_exclusion_exp_2016.SetTitle("")

graph_exclusion_exp_2016.SetMarkerStyle(19)
graph_exclusion_exp_2016.SetMarkerSize(0.0)
graph_exclusion_exp_2016.SetLineColor(kRed+1)
graph_exclusion_exp_2016.SetLineWidth(3)
graph_exclusion_exp_2016.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_2016.SetFillStyle(3353)
graph_exclusion_exp_2016.SetLineStyle(kDashed)




graph_exclusion_obs_2016.SetMarkerStyle(19)
graph_exclusion_obs_2016.SetMarkerSize(0.0)
graph_exclusion_obs_2016.SetLineColor(kBlack)
graph_exclusion_obs_2016.SetLineWidth(3)

graph_exclusion_exp_2016.Draw("AL")

if drawObs:
	graph_exclusion_obs_2016.Draw("Lsames")

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
ctau_cms_7TeV_1g  = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 10., 25.0, 50.0, 100.0, 200.0, 400.0, 600.0, 600.0])
graph_exclusion_cms_7TeV_1g = TGraph(16, mass_cms_7TeV_1g, ctau_cms_7TeV_1g)
graph_exclusion_cms_7TeV_1g.SetFillColorAlpha(kYellow, 0.6)
graph_exclusion_cms_7TeV_1g.SetLineColorAlpha(kYellow, 0.6)
graph_exclusion_cms_7TeV_1g.Draw("Fsames")

######CMS 8TeV, single photon
mass_cms_8TeV_1g = np.array([139.51,  168.16, 197.17, 226.17, 264.65, 283.83, 254.65, 226.17, 197.17, 171.36, 139.51])
ctau_cms_8TeV_1g  = np.array([3.5164, 2.4777, 2.7902, 2.9517, 4.2685, 6.53,   15.188, 26.828, 38.797, 46.219, 43.147])*29.9792458
graph_exclusion_cms_8TeV_1g = TGraph(11, mass_cms_8TeV_1g, ctau_cms_8TeV_1g)
graph_exclusion_cms_8TeV_1g.SetFillColorAlpha(kAzure+10, 0.65)
graph_exclusion_cms_8TeV_1g.SetLineColorAlpha(kAzure+10, 0.65)
graph_exclusion_cms_8TeV_1g.Draw("Fsames")

######CMS 8TeV, two photons
mass_cms_8TeV_2g = np.array([198., 227., 256., 256., 227., 198.])
ctau_cms_8TeV_2g  = np.array([0.4, 2, 9, 9, 25., 50.])
graph_exclusion_cms_8TeV_2g = TGraph(6, mass_cms_8TeV_2g, ctau_cms_8TeV_2g)
graph_exclusion_cms_8TeV_2g.SetFillColorAlpha(kGray, 0.6)
graph_exclusion_cms_8TeV_2g.SetLineColorAlpha(kGray, 0.6)
graph_exclusion_cms_8TeV_2g.Draw("Fsames")


####legend
leg_2d_exclusion_2016 = TLegend(0.28,0.64,0.92,0.91)
leg_2d_exclusion_2016.SetBorderSize(0)
leg_2d_exclusion_2016.SetTextSize(0.03)
leg_2d_exclusion_2016.SetLineColor(1)
leg_2d_exclusion_2016.SetLineStyle(1)
leg_2d_exclusion_2016.SetLineWidth(1)
leg_2d_exclusion_2016.SetFillColor(0)
leg_2d_exclusion_2016.SetFillStyle(1001)

leg_2d_exclusion_2016.AddEntry(graph_exclusion_exp_2016, "CMS Exp 13 TeV #gamma#gamma (2016)", "LF")
if drawObs:
	leg_2d_exclusion_2016.AddEntry(graph_exclusion_obs_2016, "CMS Obs 13 TeV #gamma#gamma (2016)", "L")
leg_2d_exclusion_2016.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
leg_2d_exclusion_2016.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
leg_2d_exclusion_2016.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
leg_2d_exclusion_2016.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

leg_2d_exclusion_2016.Draw()

drawCMS2(myC2D, 13, lumi_2016)

#Lambda axis
f1_lambda = TF1("f1","(x+6.00)/1.454",72.902, 416.78)
A1_lambda = TGaxis(100.0, 0.02,600.0,0.02,"f1",1010,"NI")
A1_lambda.SetLabelFont(42)
A1_lambda.SetLabelSize(0.035)
A1_lambda.SetTextFont(42)
A1_lambda.SetTextSize(1.2)
A1_lambda.SetTitle("#Lambda [TeV]")
A1_lambda.SetTitleSize(0.04)
A1_lambda.SetTitleOffset(0.9)
A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016"+plot_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016"+plot_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016"+plot_tag+".C")

###2017CAT1 only
graph_exclusion_exp_2017CAT1 = TGraph(len(lambda_point_boundary_exp_2017CAT1), np.array(1.454*lambda_point_boundary_exp_2017CAT1-6.0), np.array(ctau_points))
graph_exclusion_obs_2017CAT1 = TGraph(len(lambda_point_boundary_obs_2017CAT1), np.array(1.454*lambda_point_boundary_obs_2017CAT1-6.0), np.array(ctau_points))

graph_exclusion_exp_2017CAT1.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2017CAT1.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2017CAT1.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2017CAT1.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2017CAT1.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_2017CAT1.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_2017CAT1.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_2017CAT1.GetYaxis().SetRangeUser(0.5,1.0e7)
graph_exclusion_exp_2017CAT1.SetTitle("")

graph_exclusion_exp_2017CAT1.SetMarkerStyle(19)
graph_exclusion_exp_2017CAT1.SetMarkerSize(0.0)
graph_exclusion_exp_2017CAT1.SetLineColor(kRed+1)
graph_exclusion_exp_2017CAT1.SetLineWidth(3)
graph_exclusion_exp_2017CAT1.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_2017CAT1.SetFillStyle(3353)
graph_exclusion_exp_2017CAT1.SetLineStyle(kDashed)




graph_exclusion_obs_2017CAT1.SetMarkerStyle(19)
graph_exclusion_obs_2017CAT1.SetMarkerSize(0.0)
graph_exclusion_obs_2017CAT1.SetLineColor(kBlack)
graph_exclusion_obs_2017CAT1.SetLineWidth(3)

graph_exclusion_exp_2017CAT1.Draw("AL")
if drawObs:
	graph_exclusion_obs_2017CAT1.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_2017CAT1 = TLegend(0.28,0.64,0.92,0.91)
leg_2d_exclusion_2017CAT1.SetBorderSize(0)
leg_2d_exclusion_2017CAT1.SetTextSize(0.03)
leg_2d_exclusion_2017CAT1.SetLineColor(1)
leg_2d_exclusion_2017CAT1.SetLineStyle(1)
leg_2d_exclusion_2017CAT1.SetLineWidth(1)
leg_2d_exclusion_2017CAT1.SetFillColor(0)
leg_2d_exclusion_2017CAT1.SetFillStyle(1001)

leg_2d_exclusion_2017CAT1.AddEntry(graph_exclusion_exp_2017CAT1, "CMS Exp 13 TeV #gamma (2017)", "LF")
if drawObs:
	leg_2d_exclusion_2017CAT1.AddEntry(graph_exclusion_obs_2017CAT1, "CMS Obs 13 TeV #gamma (2017)", "L")
leg_2d_exclusion_2017CAT1.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
leg_2d_exclusion_2017CAT1.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
leg_2d_exclusion_2017CAT1.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
leg_2d_exclusion_2017CAT1.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

leg_2d_exclusion_2017CAT1.Draw()

drawCMS2(myC2D, 13, lumi_2017)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017CAT1"+plot_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017CAT1"+plot_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017CAT1"+plot_tag+".C")


###2017CAT2 only
graph_exclusion_exp_2017CAT2 = TGraph(len(lambda_point_boundary_exp_2017CAT2), np.array(1.454*lambda_point_boundary_exp_2017CAT2-6.0), np.array(ctau_points))
graph_exclusion_obs_2017CAT2 = TGraph(len(lambda_point_boundary_obs_2017CAT2), np.array(1.454*lambda_point_boundary_obs_2017CAT2-6.0), np.array(ctau_points))

graph_exclusion_exp_2017CAT2.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2017CAT2.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2017CAT2.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2017CAT2.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2017CAT2.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_2017CAT2.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_2017CAT2.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_2017CAT2.GetYaxis().SetRangeUser(0.5,1.0e7)
graph_exclusion_exp_2017CAT2.SetTitle("")

graph_exclusion_exp_2017CAT2.SetMarkerStyle(19)
graph_exclusion_exp_2017CAT2.SetMarkerSize(0.0)
graph_exclusion_exp_2017CAT2.SetLineColor(kRed+1)
graph_exclusion_exp_2017CAT2.SetLineWidth(3)
graph_exclusion_exp_2017CAT2.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_2017CAT2.SetFillStyle(3353)
graph_exclusion_exp_2017CAT2.SetLineStyle(kDashed)




graph_exclusion_obs_2017CAT2.SetMarkerStyle(19)
graph_exclusion_obs_2017CAT2.SetMarkerSize(0.0)
graph_exclusion_obs_2017CAT2.SetLineColor(kBlack)
graph_exclusion_obs_2017CAT2.SetLineWidth(3)


graph_exclusion_exp_2017CAT2.Draw("AL")
if drawObs:
	graph_exclusion_obs_2017CAT2.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_2017CAT2 = TLegend(0.28,0.64,0.92,0.91)
leg_2d_exclusion_2017CAT2.SetBorderSize(0)
leg_2d_exclusion_2017CAT2.SetTextSize(0.03)
leg_2d_exclusion_2017CAT2.SetLineColor(1)
leg_2d_exclusion_2017CAT2.SetLineStyle(1)
leg_2d_exclusion_2017CAT2.SetLineWidth(1)
leg_2d_exclusion_2017CAT2.SetFillColor(0)
leg_2d_exclusion_2017CAT2.SetFillStyle(1001)

leg_2d_exclusion_2017CAT2.AddEntry(graph_exclusion_exp_2017CAT2, "CMS Exp 13 TeV #gamma#gamma (2017)", "LF")
if drawObs:
	leg_2d_exclusion_2017CAT2.AddEntry(graph_exclusion_obs_2017CAT2, "CMS Obs 13 TeV #gamma#gamma (2017)", "L")
leg_2d_exclusion_2017CAT2.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
leg_2d_exclusion_2017CAT2.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
leg_2d_exclusion_2017CAT2.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
leg_2d_exclusion_2017CAT2.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

leg_2d_exclusion_2017CAT2.Draw()

drawCMS2(myC2D, 13, lumi_2017)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017CAT2"+plot_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017CAT2"+plot_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017CAT2"+plot_tag+".C")


###2017 only
graph_exclusion_exp_2017 = TGraph(len(lambda_point_boundary_exp_2017), np.array(1.454*lambda_point_boundary_exp_2017-6.0), np.array(ctau_points))
graph_exclusion_obs_2017 = TGraph(len(lambda_point_boundary_obs_2017), np.array(1.454*lambda_point_boundary_obs_2017-6.0), np.array(ctau_points))

graph_exclusion_exp_2017.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2017.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2017.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2017.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2017.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_2017.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_2017.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_2017.GetYaxis().SetRangeUser(0.5,1.0e7)
graph_exclusion_exp_2017.SetTitle("")

graph_exclusion_exp_2017.SetMarkerStyle(19)
graph_exclusion_exp_2017.SetMarkerSize(0.0)
graph_exclusion_exp_2017.SetLineColor(kRed+1)
graph_exclusion_exp_2017.SetLineWidth(3)
graph_exclusion_exp_2017.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_2017.SetFillStyle(3353)
graph_exclusion_exp_2017.SetLineStyle(kDashed)




graph_exclusion_obs_2017.SetMarkerStyle(19)
graph_exclusion_obs_2017.SetMarkerSize(0.0)
graph_exclusion_obs_2017.SetLineColor(kBlack)
graph_exclusion_obs_2017.SetLineWidth(3)


graph_exclusion_exp_2017.Draw("AL")
if drawObs:
	graph_exclusion_obs_2017.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_2017 = TLegend(0.28,0.64,0.92,0.91)
leg_2d_exclusion_2017.SetBorderSize(0)
leg_2d_exclusion_2017.SetTextSize(0.03)
leg_2d_exclusion_2017.SetLineColor(1)
leg_2d_exclusion_2017.SetLineStyle(1)
leg_2d_exclusion_2017.SetLineWidth(1)
leg_2d_exclusion_2017.SetFillColor(0)
leg_2d_exclusion_2017.SetFillStyle(1001)

leg_2d_exclusion_2017.AddEntry(graph_exclusion_exp_2017, "CMS Exp 13 TeV #gamma(#gamma) (2017)", "LF")
if drawObs:
	leg_2d_exclusion_2017.AddEntry(graph_exclusion_obs_2017, "CMS Obs 13 TeV #gamma(#gamma) (2017)", "L")
leg_2d_exclusion_2017.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
leg_2d_exclusion_2017.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
leg_2d_exclusion_2017.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
leg_2d_exclusion_2017.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

leg_2d_exclusion_2017.Draw()

drawCMS2(myC2D, 13, lumi_2017)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017"+plot_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017"+plot_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017"+plot_tag+".C")


###2016And2017 only
graph_exclusion_exp_2016And2017 = TGraph(len(lambda_point_boundary_exp_2016And2017), np.array(1.454*lambda_point_boundary_exp_2016And2017-6.0), np.array(ctau_points))
graph_exclusion_obs_2016And2017 = TGraph(len(lambda_point_boundary_obs_2016And2017), np.array(1.454*lambda_point_boundary_obs_2016And2017-6.0), np.array(ctau_points))

graph_exclusion_exp_2016And2017.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2016And2017.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2016And2017.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2016And2017.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2016And2017.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_2016And2017.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_2016And2017.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_2016And2017.GetYaxis().SetRangeUser(0.5,1.0e7)
graph_exclusion_exp_2016And2017.SetTitle("")

graph_exclusion_exp_2016And2017.SetMarkerStyle(19)
graph_exclusion_exp_2016And2017.SetMarkerSize(0.0)
graph_exclusion_exp_2016And2017.SetLineColor(kRed + 1)
graph_exclusion_exp_2016And2017.SetLineWidth(3)
graph_exclusion_exp_2016And2017.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_2016And2017.SetFillStyle(3353)
graph_exclusion_exp_2016And2017.SetLineStyle(kDashed)




graph_exclusion_obs_2016And2017.SetMarkerStyle(19)
graph_exclusion_obs_2016And2017.SetMarkerSize(0.0)
graph_exclusion_obs_2016And2017.SetLineColor(kBlack)
graph_exclusion_obs_2016And2017.SetLineWidth(3)


graph_exclusion_exp_2016And2017.Draw("AL")
if drawObs:
	graph_exclusion_obs_2016And2017.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_2016And2017 = TLegend(0.28,0.64,0.92,0.91)
leg_2d_exclusion_2016And2017.SetBorderSize(0)
leg_2d_exclusion_2016And2017.SetTextSize(0.03)
leg_2d_exclusion_2016And2017.SetLineColor(1)
leg_2d_exclusion_2016And2017.SetLineStyle(1)
leg_2d_exclusion_2016And2017.SetLineWidth(1)
leg_2d_exclusion_2016And2017.SetFillColor(0)
leg_2d_exclusion_2016And2017.SetFillStyle(1001)

leg_2d_exclusion_2016And2017.AddEntry(graph_exclusion_exp_2016And2017, "CMS Exp 13 TeV #gamma(#gamma) (2016+2017)", "LF")
if drawObs:
	leg_2d_exclusion_2016And2017.AddEntry(graph_exclusion_obs_2016And2017, "CMS Obs 13 TeV #gamma(#gamma) (2016+2017)", "L")
leg_2d_exclusion_2016And2017.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
leg_2d_exclusion_2016And2017.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
leg_2d_exclusion_2016And2017.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
leg_2d_exclusion_2016And2017.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

leg_2d_exclusion_2016And2017.Draw()

drawCMS2(myC2D, 13, lumi)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016And2017"+plot_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016And2017"+plot_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016And2017"+plot_tag+".C")


###overlay: 2016, 2017, 2016And2017

graph_exclusion_exp_2016.SetLineColor(kBlue + 1)
graph_exclusion_exp_2017.SetLineColor(kGreen + 3)
graph_exclusion_exp_2016And2017.SetLineColor(kRed + 1)

graph_exclusion_exp_2016.SetLineStyle(kDashed)
graph_exclusion_exp_2017.SetLineStyle(kDashed)
graph_exclusion_exp_2016And2017.SetLineStyle(kDashed)

graph_exclusion_obs_2016.SetLineColor(kBlue + 1)
graph_exclusion_obs_2017.SetLineColor(kGreen + 3)
graph_exclusion_obs_2016And2017.SetLineColor(kRed + 1)

graph_exclusion_exp_2017.Draw("AL")
graph_exclusion_exp_2016.Draw("Lsame")
graph_exclusion_exp_2016And2017.Draw("Lsame")
if drawObs:
	graph_exclusion_obs_2016.Draw("Lsames")
	graph_exclusion_obs_2017.Draw("Lsames")
	graph_exclusion_obs_2016And2017.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_2016_2017 = TLegend(0.35,0.64,0.92,0.91)
leg_2d_exclusion_2016_2017.SetBorderSize(0)
leg_2d_exclusion_2016_2017.SetTextSize(0.03)
leg_2d_exclusion_2016_2017.SetLineColor(1)
leg_2d_exclusion_2016_2017.SetLineStyle(1)
leg_2d_exclusion_2016_2017.SetLineWidth(1)
leg_2d_exclusion_2016_2017.SetFillColor(0)
leg_2d_exclusion_2016_2017.SetFillStyle(1001)

leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_exp_2016, "CMS Exp 13TeV #gamma#gamma (2016)", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_exp_2017, "CMS Exp 13TeV #gamma(#gamma) (2017)", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_exp_2016And2017, "CMS Exp 13TeV #gamma(#gamma) (2016+2017)", "L")
if drawObs:
	leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_obs_2016, "CMS Obs 13TeV #gamma#gamma (2016)", "L")
	leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_obs_2017, "CMS Obs 13TeV #gamma(#gamma) (2017)", "L")
	leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_obs_2016And2017, "CMS Obs 13TeV #gamma(#gamma) (2016+2017)", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

leg_2d_exclusion_2016_2017.Draw()

drawCMS2(myC2D, 13, lumi)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016_2017"+plot_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016_2017"+plot_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016_2017"+plot_tag+".C")



###overlay: 2017CAT1, 2017CAT2, 2017Combo

graph_exclusion_exp_2017CAT1.SetLineColor(kBlue + 1)
graph_exclusion_exp_2017CAT2.SetLineColor(kGreen + 3)
graph_exclusion_exp_2017.SetLineColor(kRed + 1)

graph_exclusion_exp_2017CAT1.SetLineStyle(kDashed)
graph_exclusion_exp_2017CAT2.SetLineStyle(kDashed)
graph_exclusion_exp_2017.SetLineStyle(kDashed)

graph_exclusion_obs_2017CAT1.SetLineColor(kBlue + 1)
graph_exclusion_obs_2017CAT2.SetLineColor(kGreen + 3)
graph_exclusion_obs_2017.SetLineColor(kRed + 1)


graph_exclusion_exp_2017.Draw("AL")
graph_exclusion_exp_2017CAT1.Draw("Lsame")
graph_exclusion_exp_2017CAT2.Draw("Lsame")
if drawObs:
	graph_exclusion_obs_2017.Draw("Lsames")
	graph_exclusion_obs_2017CAT1.Draw("Lsames")
	graph_exclusion_obs_2017CAT2.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_2016_2017 = TLegend(0.35,0.64,0.92,0.91)
leg_2d_exclusion_2016_2017.SetBorderSize(0)
leg_2d_exclusion_2016_2017.SetTextSize(0.03)
leg_2d_exclusion_2016_2017.SetLineColor(1)
leg_2d_exclusion_2016_2017.SetLineStyle(1)
leg_2d_exclusion_2016_2017.SetLineWidth(1)
leg_2d_exclusion_2016_2017.SetFillColor(0)
leg_2d_exclusion_2016_2017.SetFillStyle(1001)

leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_exp_2017CAT1, "CMS Exp 13TeV #gamma (2017)", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_exp_2017CAT2, "CMS Exp 13TeV #gamma#gamma (2017)", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_exp_2017, "CMS Exp 13TeV #gamma(#gamma) (2017)", "L")
if drawObs:
	leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_obs_2017CAT1, "CMS Obs 13TeV #gamma (2017)", "L")
	leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_obs_2017CAT2, "CMS Obs 13TeV #gamma#gamma (2017)", "L")
	leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_obs_2017, "CMS Obs 13TeV #gamma(#gamma) (2017)", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

leg_2d_exclusion_2016_2017.Draw()

drawCMS2(myC2D, 13, lumi_2017)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017All"+plot_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017All"+plot_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2017All"+plot_tag+".C")

###overlay: 2016, 2017CAT2

graph_exclusion_exp_2016.SetLineColor(kBlue + 1)
graph_exclusion_exp_2017CAT2.SetLineColor(kRed + 1)

graph_exclusion_exp_2016.SetLineStyle(kDashed)
graph_exclusion_exp_2017CAT2.SetLineStyle(kDashed)

graph_exclusion_obs_2016.SetLineColor(kBlue + 1)
graph_exclusion_obs_2017CAT2.SetLineColor(kRed + 1)

graph_exclusion_exp_2016.Draw("AL")
graph_exclusion_exp_2017CAT2.Draw("Lsame")
if drawObs:
	graph_exclusion_obs_2016.Draw("Lsames")
	graph_exclusion_obs_2017CAT2.Draw("Lsames")

graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
graph_exclusion_cms_7TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_1g.Draw("Fsames")
graph_exclusion_cms_8TeV_2g.Draw("Fsames")

####legend
leg_2d_exclusion_2016_2017 = TLegend(0.35,0.64,0.92,0.91)
leg_2d_exclusion_2016_2017.SetBorderSize(0)
leg_2d_exclusion_2016_2017.SetTextSize(0.03)
leg_2d_exclusion_2016_2017.SetLineColor(1)
leg_2d_exclusion_2016_2017.SetLineStyle(1)
leg_2d_exclusion_2016_2017.SetLineWidth(1)
leg_2d_exclusion_2016_2017.SetFillColor(0)
leg_2d_exclusion_2016_2017.SetFillStyle(1001)

leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_exp_2016, "CMS Exp 13TeV #gamma#gamma (2016)", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_exp_2017CAT2, "CMS Exp 13TeV #gamma#gamma (2017)", "L")
if drawObs:
	leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_obs_2016, "CMS Obs 13TeV #gamma#gamma (2016)", "L")
	leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_obs_2017CAT2, "CMS Obs 13TeV #gamma#gamma (2017)", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
leg_2d_exclusion_2016_2017.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

leg_2d_exclusion_2016_2017.Draw()

drawCMS2(myC2D, 13, lumi)

A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016_2017CAT2"+plot_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016_2017CAT2"+plot_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016_2017CAT2"+plot_tag+".C")

