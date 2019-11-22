from ROOT import gROOT, gStyle, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TGraph, kDashed, kGreen, kYellow, TF1, kPink, kGray, TGaxis
import os, sys
from Aux import *
import numpy as np
import array

lumi_2016 = 35922.0
lumi_2017 = 41530.0
lumi = lumi_2016+lumi_2017

lumis = [lumi_2016, lumi_2017, lumi_2017, lumi_2017, lumi]
years_to_plot = ['2016', '2017', '2017CAT1', '2017CAT2', '2016And2017']
labels = ['#gamma#gamma (2016)', '#gamma(#gamma) (2017)', '#gamma (2017)', '#gamma#gamma (2017)', '#gamma(#gamma) (2016 + 2017)']

outputDir = '/data/zhicaiz/www/sharebox/DelayedPhoton/ARCReview_June2019/orderByPt/'

lambda_points = [100, 150, 200, 250, 300, 350, 400]
ctau_points = [10.0, 50, 100, 200, 400, 600, 800, 1000, 1200, 10000]


tree_dir = "limitTrees_v18_HybridNew"
plot_tag = "_v18_HybridNew_noBand"

drawObs=True
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


N_lambda = len(lambda_points)
N_ctau = len(ctau_points)


for idx_year in range(len(years_to_plot)):
	year_this = years_to_plot[idx_year]
	lumi_this = lumis[idx_year]
	label_this = labels[idx_year]

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


	r_exp_2d_grid_ = np.zeros((N_ctau, N_lambda))
	r_obs_2d_grid_ = np.zeros((N_ctau, N_lambda))

	print "initial value of the 2D r grid (exp, "+year_this+"): "
	print r_exp_2d_grid_
	print "initial value of the 2D r grid (obs, "+year_this+"): "
	print r_obs_2d_grid_

	##################limit vs mass #######################3

	index_ctau = -1
	for ctau_this in ctau_points:
		index_ctau = index_ctau + 1

		xValue_lambda = []
		xValue_mass = []
		yValue_limit_this_Th = []

		limit_this__exp50p0 = []
		limit_this__obs = []
		
		yValue_limit_this__exp = []
		yValue_limit_this__obs = []
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

			if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Observed.HybridNew.mH120.root"):
				continue
			if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p5.HybridNew.mH120.quant0.500.root"):
				continue

			th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)

			limits_ = []
			file_limit__exp0p5 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p5.HybridNew.mH120.quant0.500.root")
			file_limit__obs = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Observed.HybridNew.mH120.root")
			limitTree__exp0p5 = file_limit__exp0p5.Get("limit")
			limitTree__obs = file_limit__obs.Get("limit")
			for entry in limitTree__exp0p5:
				limits_.append(entry.limit)
			for entry in limitTree__obs:
				limits_.append(entry.limit)
			print " limits:"
			print limits_

			if len(limits_) < 2:
				continue
			
			for idx in range(len(limits_)):
				limits_[idx] = limits_[idx]*limits_SF

			xValue_lambda.append(lambda_this)
			xValue_mass.append(lambda_this*1.454-6.0)
			yValue_limit_this_Th.append(th_xsec_this)

			limit_this__exp50p0.append(limits_[0]*th_xsec_this)	
			limit_this__obs.append(limits_[1]*th_xsec_this)	

			r_exp_2d_grid_[index_ctau][index_lambda] = limits_[0]
			r_obs_2d_grid_[index_ctau][index_lambda] = limits_[1]

		NPoints_mass = len(xValue_mass)

		for i in range(0, NPoints_mass):
			xValue_mass.append(xValue_mass[i])
			
			yValue_limit_this__obs.append(limit_this__obs[i])
			yValue_limit_this__exp.append(limit_this__exp50p0[i])

		myC.SetLogy(1)
		myC.SetLogx(0)
		
		#
		graph_limit_vs_mass__obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this__obs))
		graph_limit_vs_mass__Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
		graph_limit_vs_mass__exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this__exp))

		graph_limit_vs_mass__obs_limit.SetMarkerStyle(22)
		graph_limit_vs_mass__obs_limit.SetMarkerSize(1.5)
		graph_limit_vs_mass__obs_limit.SetLineColor(kBlack)
		graph_limit_vs_mass__obs_limit.SetLineWidth(3)

		graph_limit_vs_mass__Th_limit.SetMarkerStyle(22)
		graph_limit_vs_mass__Th_limit.SetMarkerSize(1.5)
		graph_limit_vs_mass__Th_limit.SetLineColor(kRed)
		graph_limit_vs_mass__Th_limit.SetLineWidth(2)

		graph_limit_vs_mass__exp_limit.SetMarkerStyle(19)
		graph_limit_vs_mass__exp_limit.SetMarkerSize(1.5)
		graph_limit_vs_mass__exp_limit.SetLineColor(kBlack)
		graph_limit_vs_mass__exp_limit.SetLineWidth(3)
		graph_limit_vs_mass__exp_limit.SetLineStyle(kDashed)


		graph_limit_vs_mass__exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
		graph_limit_vs_mass__exp_limit.GetXaxis().SetLimits(100.0,600.0)
		graph_limit_vs_mass__exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
		graph_limit_vs_mass__exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
		graph_limit_vs_mass__exp_limit.SetTitle("")

		graph_limit_vs_mass__exp_limit.Draw("LA")

		graph_limit_vs_mass__exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
		graph_limit_vs_mass__exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
		graph_limit_vs_mass__exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
		graph_limit_vs_mass__exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

		if drawObs:
			graph_limit_vs_mass__obs_limit.Draw("Lsame")
		graph_limit_vs_mass__exp_limit.Draw("Lsame")
		graph_limit_vs_mass__Th_limit.Draw("Lsame")

		drawCMS2(myC, 13, lumi_this)

		leg_limit_vs_mass_ = TLegend(0.25,0.62,0.9,0.89)

		leg_limit_vs_mass_.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
		leg_limit_vs_mass_.SetBorderSize(0)
		leg_limit_vs_mass_.SetTextSize(0.03)
		leg_limit_vs_mass_.SetLineColor(1)
		leg_limit_vs_mass_.SetLineStyle(1)
		leg_limit_vs_mass_.SetLineWidth(1)
		leg_limit_vs_mass_.SetFillColor(0)
		leg_limit_vs_mass_.SetFillStyle(1001)

		leg_limit_vs_mass_.AddEntry(graph_limit_vs_mass__Th_limit, "Theoretical cross-section", "L")
		if drawObs:
			leg_limit_vs_mass_.AddEntry(graph_limit_vs_mass__obs_limit, "Observed  95% CL upper limit", "L")
		leg_limit_vs_mass_.AddEntry(graph_limit_vs_mass__exp_limit, "Expected  95% CL upper limit", "L")
		leg_limit_vs_mass_.Draw()

		myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+year_this+"_ctau"+ctau_this_str+plot_tag+".pdf")
		myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+year_this+"_ctau"+ctau_this_str+plot_tag+".png")
		myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+year_this+"_ctau"+ctau_this_str+plot_tag+".C")

	##################exclusion region of ctau and Lambda/mass #######################
	print "value of the 2D r grid (exp, "+year_this+") provided from samples: "
	print r_exp_2d_grid_
	print "value of the 2D r grid (obs, "+year_this+") provided from samples: "
	print r_obs_2d_grid_


	lambda_point_boundary_exp_ = np.zeros(N_ctau)
	lambda_point_boundary_obs_ = np.zeros(N_ctau)


	for i in range(0, N_ctau):
		print "doing linear interpolation to get the boundary value of lambda for ctau = "+str(ctau_points[i])

		lambda_interp_ = []
		r_exp_interp_ = []
		r_obs_interp_ = []
		
		for j in range(0, N_lambda):
			if r_exp_2d_grid_[i][j] > 0.00000001:
				lambda_interp_.append(lambda_points[j]*1.0)
				r_exp_interp_.append(r_exp_2d_grid_[i][j]*1.0)
				r_obs_interp_.append(r_obs_2d_grid_[i][j]*1.0)
		graph_lambda_vs_r_exp_ =  TGraph(len(lambda_interp_), np.array(r_exp_interp_), np.array(lambda_interp_))
		lambda_point_boundary_exp_[i] = graph_lambda_vs_r_exp_.Eval(1.0)
		graph_lambda_vs_r_obs_ =  TGraph(len(lambda_interp_), np.array(r_obs_interp_), np.array(lambda_interp_))
		lambda_point_boundary_obs_[i] = graph_lambda_vs_r_obs_.Eval(1.0)

	print "lambda points:"
	print lambda_points

	print "exp () exclusion lambda boundary for different ctau:"
	print lambda_point_boundary_exp_
	print "obs () exclusion lambda boundary for different ctau:"
	print lambda_point_boundary_obs_

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


	### only
	graph_exclusion_exp_ = TGraph(len(lambda_point_boundary_exp_), np.array(1.454*lambda_point_boundary_exp_-6.0), np.array(ctau_points))
	graph_exclusion_obs_ = TGraph(len(lambda_point_boundary_obs_), np.array(1.454*lambda_point_boundary_obs_-6.0), np.array(ctau_points))

	graph_exclusion_exp_.GetXaxis().SetTitleSize( axisTitleSize )
	graph_exclusion_exp_.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_exclusion_exp_.GetYaxis().SetTitleSize( axisTitleSize )
	graph_exclusion_exp_.GetYaxis().SetTitleOffset( axisTitleOffset )
	graph_exclusion_exp_.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_exclusion_exp_.GetXaxis().SetLimits(100.0, 600.0)
	graph_exclusion_exp_.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
	graph_exclusion_exp_.GetYaxis().SetRangeUser(0.5,1.0e7)
	graph_exclusion_exp_.SetTitle("")

	graph_exclusion_exp_.SetMarkerStyle(19)
	graph_exclusion_exp_.SetMarkerSize(0.0)
	graph_exclusion_exp_.SetLineColor(kRed + 1)
	graph_exclusion_exp_.SetLineWidth(3)
	graph_exclusion_exp_.SetFillColorAlpha(kOrange - 9, 0.65)
	graph_exclusion_exp_.SetFillStyle(3353)
	graph_exclusion_exp_.SetLineStyle(kDashed)

	graph_exclusion_obs_.SetMarkerStyle(19)
	graph_exclusion_obs_.SetMarkerSize(0.0)
	graph_exclusion_obs_.SetLineColor(kBlack)
	graph_exclusion_obs_.SetLineWidth(3)


	graph_exclusion_exp_.Draw("AL")
	if drawObs:
		graph_exclusion_obs_.Draw("Lsames")

	graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
	graph_exclusion_cms_7TeV_1g.Draw("Fsames")
	graph_exclusion_cms_8TeV_1g.Draw("Fsames")
	graph_exclusion_cms_8TeV_2g.Draw("Fsames")

	####legend
	leg_2d_exclusion_ = TLegend(0.28,0.64,0.92,0.91)
	leg_2d_exclusion_.SetBorderSize(0)
	leg_2d_exclusion_.SetTextSize(0.03)
	leg_2d_exclusion_.SetLineColor(1)
	leg_2d_exclusion_.SetLineStyle(1)
	leg_2d_exclusion_.SetLineWidth(1)
	leg_2d_exclusion_.SetFillColor(0)
	leg_2d_exclusion_.SetFillStyle(1001)

	leg_2d_exclusion_.AddEntry(graph_exclusion_exp_, "CMS Exp 13 TeV "+label_this, "L")
	if drawObs:
		leg_2d_exclusion_.AddEntry(graph_exclusion_obs_, "CMS Obs 13 TeV "+label_this, "L")
	leg_2d_exclusion_.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
	leg_2d_exclusion_.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
	leg_2d_exclusion_.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
	leg_2d_exclusion_.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

	leg_2d_exclusion_.Draw()

	drawCMS2(myC2D, 13, lumi_this)

	A1_lambda.Draw()

	myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_this+plot_tag+".pdf")
	myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_this+plot_tag+".png")
	myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_this+plot_tag+".C")


