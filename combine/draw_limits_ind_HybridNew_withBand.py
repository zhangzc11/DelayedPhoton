from ROOT import gROOT, gStyle, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TGraph, kDashed, kGreen, kYellow, TF1, kPink, kGray, TGaxis, TH2F, TGraph, TColor, gPad
import os, sys
from Aux import *
import numpy as np
import array

lumi_2016 = 35922.0
lumi_2017 = 41530.0
lumi = lumi_2016+lumi_2017

#lumis = [lumi_2016, lumi_2017, lumi_2017, lumi_2017, lumi]
#years_to_plot = ['2016', '2017', '2017CAT1', '2017CAT2', '2016And2017']
#labels = ['#gamma#gamma (2016)', '#gamma(#gamma) (2017)', '#gamma (2017)', '#gamma#gamma (2017)', '#gamma(#gamma) (2016 + 2017)']

lumis = [lumi]
years_to_plot = ['2016And2017']
labels = ['#gamma(#gamma) (2016 + 2017)']

outputDir = '/data/zhicaiz/www/sharebox/DelayedPhoton/ARCReview_June2019/orderByPt/'

lambda_points = [100, 150, 200, 250, 300, 350, 400]
ctau_points = [10.0, 50, 100, 200, 400, 600, 800, 1000, 1200, 10000]

tree_dir = "limitTrees_v18_HybridNew"
plot_tag = "_v18_HybridNew"

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

axisTitleSize = 0.041
axisTitleOffset = 1.2
axisTitleSizeRatioX   = 0.18
axisLabelSizeRatioX   = 0.12
axisTitleOffsetRatioX = 0.94
axisTitleSizeRatioY   = 0.15
axisLabelSizeRatioY   = 0.108
axisTitleOffsetRatioY = 0.32

leftMargin   = 0.18
rightMargin  = 0.15
topMargin    = 0.05
bottomMargin = 0.14
bottomMargin2 = 0.22

N_lambda = len(lambda_points)
N_ctau = len(ctau_points)



for idx_year in range(len(years_to_plot)):
        year_this = years_to_plot[idx_year]
        lumi_this = lumis[idx_year]
        label_this = labels[idx_year]

	myC = TCanvas( "myC", "myC", 200, 10, 700, 600 )
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
	r_exp_p1sig_2d_grid_ = np.zeros((N_ctau, N_lambda))
	r_exp_m1sig_2d_grid_ = np.zeros((N_ctau, N_lambda))
	r_obs_p1sig_2d_grid_ = np.zeros((N_ctau, N_lambda))
	r_obs_m1sig_2d_grid_ = np.zeros((N_ctau, N_lambda))
	r_obs_2d_grid_ = np.zeros((N_ctau, N_lambda))
	limit_obs_2d_grid_ = np.zeros((N_ctau, N_lambda))


	print "initial value of the 2D r grid (exp, "+year_this+"): "
        print r_exp_2d_grid_
        print "initial value of the 2D r grid (obs, "+year_this+"): "
        print r_obs_2d_grid_

	##################limit vs mass #######################3

	index_ctau = -1
	for ctau_this in ctau_points:
		index_ctau = index_ctau + 1

		xValue_lambda = []
		xValue_lambda_exp1sigma = []
		xValue_lambda_exp2sigma = []
		xValue_mass = []
		xValue_mass_exp1sigma = []
		xValue_mass_exp2sigma = []
		yValue_limit_this_Th = []


		limit_this__exp2p5 = []
		limit_this__exp16p0 = []
		limit_this__exp50p0 = []
		limit_this__exp84p0 = []
		limit_this__exp97p5 = []
		limit_this__obs = []
			
		yValue_limit_this__exp = []
		yValue_limit_this__obs = []
		yValue_limit_this__exp1sigma = []
		yValue_limit_this__exp2sigma = []

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
			if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p025.HybridNew.mH120.quant0.025.root"):
				continue
			if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p16.HybridNew.mH120.quant0.160.root"):
				continue
			if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p5.HybridNew.mH120.quant0.500.root"):
				continue
			if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p84.HybridNew.mH120.quant0.840.root"):
				continue
			if not os.path.isfile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p975.HybridNew.mH120.quant0.975.root"):
				continue

			th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)


			limits_ = []
			file_limit__exp0p025 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p025.HybridNew.mH120.quant0.025.root")
			file_limit__exp0p16 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p16.HybridNew.mH120.quant0.160.root")
			file_limit__exp0p5 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p5.HybridNew.mH120.quant0.500.root")
			file_limit__exp0p84 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p84.HybridNew.mH120.quant0.840.root")
			file_limit__exp0p975 = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Exp0p975.HybridNew.mH120.quant0.975.root")
			file_limit__obs = TFile(tree_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_this+"_Observed.HybridNew.mH120.root")
			limitTree__exp0p025 = file_limit__exp0p025.Get("limit")
			limitTree__exp0p16 = file_limit__exp0p16.Get("limit")
			limitTree__exp0p5 = file_limit__exp0p5.Get("limit")
			limitTree__exp0p84 = file_limit__exp0p84.Get("limit")
			limitTree__exp0p975 = file_limit__exp0p975.Get("limit")
			limitTree__obs = file_limit__obs.Get("limit")
			for entry in limitTree__exp0p025:
				limits_.append(entry.limit)
			for entry in limitTree__exp0p16:
				limits_.append(entry.limit)
			for entry in limitTree__exp0p5:
				limits_.append(entry.limit)
			for entry in limitTree__exp0p84:
				limits_.append(entry.limit)
			for entry in limitTree__exp0p975:
				limits_.append(entry.limit)
			for entry in limitTree__obs:
				limits_.append(entry.limit)
			print " limits:"
			print limits_

			if len(limits_) < 6:
				continue
			
			for idx in range(len(limits_)):
				limits_[idx] = limits_[idx]*limits_SF

			xValue_lambda.append(lambda_this)
			xValue_mass.append(lambda_this*1.454-6.0)
			yValue_limit_this_Th.append(th_xsec_this)


			limit_this__exp2p5.append(limits_[0]*th_xsec_this)	
			limit_this__exp16p0.append(limits_[1]*th_xsec_this)	
			limit_this__exp50p0.append(limits_[2]*th_xsec_this)	
			limit_this__exp84p0.append(limits_[3]*th_xsec_this)	
			limit_this__exp97p5.append(limits_[4]*th_xsec_this)	
			limit_this__obs.append(limits_[5]*th_xsec_this)	

			r_exp_2d_grid_[index_ctau][index_lambda] = limits_[2]
			r_exp_p1sig_2d_grid_[index_ctau][index_lambda] = limits_[3]
			r_exp_m1sig_2d_grid_[index_ctau][index_lambda] = limits_[1]
			r_obs_p1sig_2d_grid_[index_ctau][index_lambda] = limits_[5]+(eth_xsec_this/th_xsec_this)
			r_obs_m1sig_2d_grid_[index_ctau][index_lambda] = limits_[5]-(eth_xsec_this/th_xsec_this)
			r_obs_2d_grid_[index_ctau][index_lambda] = limits_[5]
			limit_obs_2d_grid_[index_ctau][index_lambda] = limits_[5]*th_xsec_this

		NPoints_mass = len(xValue_mass)

		for i in range(0, NPoints_mass):
			xValue_mass.append(xValue_mass[i])
			xValue_mass_exp1sigma.append(xValue_mass[i])
			xValue_mass_exp2sigma.append(xValue_mass[i])
			
			yValue_limit_this__obs.append(limit_this__obs[i])
			yValue_limit_this__exp.append(limit_this__exp50p0[i])
			yValue_limit_this__exp1sigma.append(limit_this__exp16p0[i])
			yValue_limit_this__exp2sigma.append(limit_this__exp2p5[i])

		for i in range(0, NPoints_mass):
			xValue_mass_exp1sigma.append(xValue_mass[NPoints_mass-i-1])
			xValue_mass_exp2sigma.append(xValue_mass[NPoints_mass-i-1])
			
			yValue_limit_this__exp1sigma.append(limit_this__exp84p0[NPoints_mass-i-1])
			yValue_limit_this__exp2sigma.append(limit_this__exp97p5[NPoints_mass-i-1])

		myC.SetLogy(1)
		myC.SetLogx(0)

		#
		graph_limit_vs_mass__obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this__obs))
		graph_limit_vs_mass__Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
		graph_limit_vs_mass__exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this__exp))
		graph_limit_vs_mass__exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp1sigma), np.array(yValue_limit_this__exp1sigma))
		graph_limit_vs_mass__exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp2sigma), np.array(yValue_limit_this__exp2sigma))

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

		graph_limit_vs_mass__exp1sigma_limit.SetFillColor(kGreen)
		graph_limit_vs_mass__exp2sigma_limit.SetFillColor(kYellow)

		graph_limit_vs_mass__exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} (GeV)")
		graph_limit_vs_mass__exp_limit.GetXaxis().SetLimits(100.0,600.0)
		graph_limit_vs_mass__exp_limit.GetYaxis().SetTitle("95% CL upper limit on cross section (pb)")
		graph_limit_vs_mass__exp_limit.GetYaxis().SetRangeUser(1.0e-4,1.0e4)
		graph_limit_vs_mass__exp_limit.SetTitle("")

		graph_limit_vs_mass__exp_limit.Draw("LA")

		graph_limit_vs_mass__exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
		graph_limit_vs_mass__exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
		graph_limit_vs_mass__exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
		graph_limit_vs_mass__exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

		graph_limit_vs_mass__exp2sigma_limit.Draw("Fsame")
		graph_limit_vs_mass__exp1sigma_limit.Draw("Fsame")
		if drawObs:
			graph_limit_vs_mass__obs_limit.Draw("Lsame")
		graph_limit_vs_mass__exp_limit.Draw("Lsame")
		graph_limit_vs_mass__Th_limit.Draw("Lsame")

		drawCMS3(myC, 13, lumi_this)

		leg_limit_vs_mass_ = TLegend(0.2,0.62,0.84,0.89)

		leg_limit_vs_mass_.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
		leg_limit_vs_mass_.SetBorderSize(0)
		leg_limit_vs_mass_.SetTextSize(0.03)
		leg_limit_vs_mass_.SetLineColor(1)
		leg_limit_vs_mass_.SetLineStyle(1)
		leg_limit_vs_mass_.SetLineWidth(1)
		leg_limit_vs_mass_.SetFillColor(0)
		leg_limit_vs_mass_.SetFillStyle(1001)

		leg_limit_vs_mass_.AddEntry(graph_limit_vs_mass__Th_limit, "Theoretical cross section", "L")
		if drawObs:
			leg_limit_vs_mass_.AddEntry(graph_limit_vs_mass__obs_limit, "Observed  95% CL upper limit", "L")
		leg_limit_vs_mass_.AddEntry(graph_limit_vs_mass__exp_limit, "Expected  95% CL upper limit", "L")
		leg_limit_vs_mass_.AddEntry(graph_limit_vs_mass__exp1sigma_limit, "#pm 1 #sigma Expected", "F")
		leg_limit_vs_mass_.AddEntry(graph_limit_vs_mass__exp2sigma_limit, "#pm 2 #sigma Expected", "F")
		leg_limit_vs_mass_.Draw()

                myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+year_this+"_ctau"+ctau_this_str+plot_tag+".pdf")
                myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+year_this+"_ctau"+ctau_this_str+plot_tag+".png")
                myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+year_this+"_ctau"+ctau_this_str+plot_tag+".C")

	##################limit vs ctau #######################3

	index_lambda = -1
	for lambda_this in lambda_points:
		index_lambda = index_lambda + 1

		xValue_ctau = []

		yValue_limit_this_Th = []
		yValue_limit_this__exp = []
		yValue_limit_this__obs = []
		yValue_limit_this__exp1sigma = []
		yValue_limit_this__exp2sigma = []
		
		index_ctau = - 1
		for ctau_this in ctau_points:
			th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)
			yValue_limit_this_Th.append(th_xsec_this)
			xValue_ctau.append(ctau_this)




	##################exclusion region of ctau and Lambda/mass #######################

        print "value of the 2D r grid (exp, "+year_this+") provided from samples: "
        print r_exp_2d_grid_
        print "value of the 2D r grid (obs, "+year_this+") provided from samples: "
        print r_obs_2d_grid_
        print "value of the 2D obs limit grid (obs, "+year_this+"): "
        print limit_obs_2d_grid_

	###linear interpolation to get the boundary points
	lambda_point_boundary_exp_ = np.zeros(N_ctau)
	lambda_point_boundary_exp_p1sig_ = np.zeros(N_ctau)
	lambda_point_boundary_exp_m1sig_ = np.zeros(N_ctau)
	lambda_point_boundary_obs_p1sig_ = np.zeros(N_ctau)
	lambda_point_boundary_obs_m1sig_ = np.zeros(N_ctau)
	lambda_point_boundary_obs_ = np.zeros(N_ctau)


	for i in range(0, N_ctau):
		print "doing linear interpolation to get the boundary value of lambda for ctau = "+str(ctau_points[i])
		lambda_interp_ = []
		r_exp_interp_ = []
		r_exp_p1sig_interp_ = []
		r_exp_m1sig_interp_ = []
		r_obs_p1sig_interp_ = []
		r_obs_m1sig_interp_ = []
		r_obs_interp_ = []
		
		for j in range(0, N_lambda):
			if r_exp_2d_grid_[i][j] > 0.00000001:
				lambda_interp_.append(lambda_points[j]*1.0)
				r_exp_interp_.append(r_exp_2d_grid_[i][j]*1.0)
				r_exp_p1sig_interp_.append(r_exp_p1sig_2d_grid_[i][j]*1.0)
				r_exp_m1sig_interp_.append(r_exp_m1sig_2d_grid_[i][j]*1.0)
				r_obs_p1sig_interp_.append(r_obs_p1sig_2d_grid_[i][j]*1.0)
				r_obs_m1sig_interp_.append(r_obs_m1sig_2d_grid_[i][j]*1.0)
				r_obs_interp_.append(r_obs_2d_grid_[i][j]*1.0)
		graph_lambda_vs_r_exp_ =  TGraph(len(lambda_interp_), np.array(r_exp_interp_), np.array(lambda_interp_))
		graph_lambda_vs_r_exp_p1sig_ =  TGraph(len(lambda_interp_), np.array(r_exp_p1sig_interp_), np.array(lambda_interp_))
		graph_lambda_vs_r_exp_m1sig_ =  TGraph(len(lambda_interp_), np.array(r_exp_m1sig_interp_), np.array(lambda_interp_))
		graph_lambda_vs_r_obs_p1sig_ =  TGraph(len(lambda_interp_), np.array(r_obs_p1sig_interp_), np.array(lambda_interp_))
		graph_lambda_vs_r_obs_m1sig_ =  TGraph(len(lambda_interp_), np.array(r_obs_m1sig_interp_), np.array(lambda_interp_))
		lambda_point_boundary_exp_[i] = graph_lambda_vs_r_exp_.Eval(1.0)
		lambda_point_boundary_exp_p1sig_[i] = graph_lambda_vs_r_exp_p1sig_.Eval(1.0)
		lambda_point_boundary_exp_m1sig_[i] = graph_lambda_vs_r_exp_m1sig_.Eval(1.0)
		lambda_point_boundary_obs_p1sig_[i] = graph_lambda_vs_r_obs_p1sig_.Eval(1.0)
		lambda_point_boundary_obs_m1sig_[i] = graph_lambda_vs_r_obs_m1sig_.Eval(1.0)
		graph_lambda_vs_r_obs_ =  TGraph(len(lambda_interp_), np.array(r_obs_interp_), np.array(lambda_interp_))
		lambda_point_boundary_obs_[i] = graph_lambda_vs_r_obs_.Eval(1.0)


	print "lambda points:"
	print lambda_points


	print "exp () exclusion lambda boundary for different ctau:"
	print lambda_point_boundary_exp_
	print "exp p1sig () exclusion lambda boundary for different ctau:"
	print lambda_point_boundary_exp_p1sig_
	print "exp m1sig () exclusion lambda boundary for different ctau:"
	print lambda_point_boundary_exp_m1sig_
	print "obs () exclusion lambda boundary for different ctau:"
	print lambda_point_boundary_obs_
	print "obs p1sig () exclusion lambda boundary for different ctau:"
	print lambda_point_boundary_obs_p1sig_
	print "obs m1sig () exclusion lambda boundary for different ctau:"
	print lambda_point_boundary_obs_m1sig_

	myC2D = TCanvas( "myC2D", "myC2D", 200, 10, 700, 600 )
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
	myC2D.SetTickx(1)
	myC2D.SetTicky(1)

	lambda_point_boundary_exp_pm1sig_ = []
	lambda_point_boundary_obs_pm1sig_ = []
	ctau_points_loop = []

	for i in range(0,len(ctau_points)):
		ctau_points_loop.append(ctau_points[i])
		lambda_point_boundary_exp_pm1sig_.append(lambda_point_boundary_exp_p1sig_[i]*1.0)
		lambda_point_boundary_obs_pm1sig_.append(lambda_point_boundary_obs_p1sig_[i]*1.0)

	for i in range(0, len(ctau_points)):
		ctau_points_loop.append(ctau_points[len(ctau_points)-i-1]*1.0) 
		lambda_point_boundary_exp_pm1sig_.append(lambda_point_boundary_exp_m1sig_[len(ctau_points)-i-1]*1.0)
		lambda_point_boundary_obs_pm1sig_.append(lambda_point_boundary_obs_m1sig_[len(ctau_points)-i-1]*1.0)

	#####ATLAS 8TeV
	lambda_atlas_8TeV_2g = np.array([82.5 , 102.5,   140,   160,   180,   200,   220, 260,  300, 302.58, 300, 260, 220, 200 ])
	t_atlas_8TeV_2g = np.array([ 121.81, 90.94, 46.63, 36.12, 27.18, 20.26, 14.59, 7.47, 2.6, 1.83, 1.31, 0.61, 0.39, 0.30 ])
	ctau_atlas_8TeV_2g = t_atlas_8TeV_2g * 30.0
	mass_atlas_8TeV_2g = lambda_atlas_8TeV_2g*1.454 - 6.0
	graph_exclusion_atlas_8TeV_2g = TGraph(14, mass_atlas_8TeV_2g, ctau_atlas_8TeV_2g)
	graph_exclusion_atlas_8TeV_2g.SetLineColor(8)
	graph_exclusion_atlas_8TeV_2g.SetLineWidth(3)
	graph_exclusion_atlas_8TeV_2g.SetLineStyle(5)

	######CMS 7TeV
	mass_cms_7TeV_1g = np.array([100., 145., 157., 179., 192., 216., 221., 218., 218., 221., 216., 192., 179., 157., 145., 100.])
	ctau_cms_7TeV_1g  = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 10., 25.0, 50.0, 100.0, 200.0, 400.0, 600.0, 600.0])
	graph_exclusion_cms_7TeV_1g = TGraph(16, mass_cms_7TeV_1g, ctau_cms_7TeV_1g)
	graph_exclusion_cms_7TeV_1g.SetFillColorAlpha(kYellow, 0.6)
	graph_exclusion_cms_7TeV_1g.SetLineColorAlpha(kYellow, 0.6)

	######CMS 8TeV, single photon
	mass_cms_8TeV_1g = np.array([139.51,  168.16, 197.17, 226.17, 264.65, 283.83, 254.65, 226.17, 197.17, 171.36, 139.51])
	ctau_cms_8TeV_1g  = np.array([3.5164, 2.4777, 2.7902, 2.9517, 4.2685, 6.53,   15.188, 26.828, 38.797, 46.219, 43.147])*29.9792458
	graph_exclusion_cms_8TeV_1g = TGraph(11, mass_cms_8TeV_1g, ctau_cms_8TeV_1g)
	graph_exclusion_cms_8TeV_1g.SetFillColorAlpha(kAzure+10, 0.65)
	graph_exclusion_cms_8TeV_1g.SetLineColorAlpha(kAzure+10, 0.65)

	######CMS 8TeV, two photons
	mass_cms_8TeV_2g = np.array([198., 227., 256., 256., 227., 198.])
	ctau_cms_8TeV_2g  = np.array([0.4, 2, 9, 9, 25., 50.])
	graph_exclusion_cms_8TeV_2g = TGraph(6, mass_cms_8TeV_2g, ctau_cms_8TeV_2g)
	graph_exclusion_cms_8TeV_2g.SetFillColorAlpha(kGray, 0.6)
	graph_exclusion_cms_8TeV_2g.SetLineColorAlpha(kGray, 0.6)


	####legend

	#Lambda axis
	f1_lambda = TF1("f1","(x+6.00)/1.454",72.902, 416.78)
        A1_lambda = TGaxis(100.0, 0.6,600.0,0.6,"f1",1010,"NI")
	A1_lambda.SetLabelFont(42)
	A1_lambda.SetLabelSize(0.035)
	A1_lambda.SetTextFont(42)
	A1_lambda.SetTextSize(1.2)
	A1_lambda.SetTitle("#Lambda (TeV)")
	A1_lambda.SetTitleSize(0.04)
	A1_lambda.SetTitleOffset(0.9)

	### only
	graph_exclusion_exp_ = TGraph(len(lambda_point_boundary_exp_), np.array(1.454*lambda_point_boundary_exp_-6.0), np.array(ctau_points))
	graph_exclusion_exp_p1sig_ = TGraph(len(lambda_point_boundary_exp_p1sig_), np.array(1.454*lambda_point_boundary_exp_p1sig_-6.0), np.array(ctau_points))
	graph_exclusion_exp_m1sig_ = TGraph(len(lambda_point_boundary_exp_m1sig_), np.array(1.454*lambda_point_boundary_exp_m1sig_-6.0), np.array(ctau_points))
	graph_exclusion_exp_pm1sig_ = TGraph(len(lambda_point_boundary_exp_pm1sig_), np.array(1.454*np.array(lambda_point_boundary_exp_pm1sig_)-6.0), np.array(ctau_points_loop))
	graph_exclusion_obs_ = TGraph(len(lambda_point_boundary_obs_), np.array(1.454*lambda_point_boundary_obs_-6.0), np.array(ctau_points))
	graph_exclusion_obs_p1sig_ = TGraph(len(lambda_point_boundary_obs_p1sig_), np.array(1.454*lambda_point_boundary_obs_p1sig_-6.0), np.array(ctau_points))
	graph_exclusion_obs_m1sig_ = TGraph(len(lambda_point_boundary_obs_m1sig_), np.array(1.454*lambda_point_boundary_obs_m1sig_-6.0), np.array(ctau_points))
	graph_exclusion_obs_pm1sig_ = TGraph(len(lambda_point_boundary_obs_pm1sig_), np.array(1.454*np.array(lambda_point_boundary_obs_pm1sig_)-6.0), np.array(ctau_points_loop))

	graph_exclusion_exp_.GetXaxis().SetTitleSize( axisTitleSize )
	graph_exclusion_exp_.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_exclusion_exp_.GetYaxis().SetTitleSize( axisTitleSize )
	graph_exclusion_exp_.GetYaxis().SetTitleOffset( axisTitleOffset )
	graph_exclusion_exp_.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} (GeV)")
	graph_exclusion_exp_.GetXaxis().SetLimits(100.0, 600.0)
	graph_exclusion_exp_.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} (cm)")
	graph_exclusion_exp_.GetYaxis().SetRangeUser(9.0,5.0e6)
	graph_exclusion_exp_.SetTitle("")

	graph_exclusion_exp_.SetMarkerStyle(19)
	graph_exclusion_exp_.SetMarkerSize(0.0)
	graph_exclusion_exp_.SetLineColor(kRed - 0)
	graph_exclusion_exp_.SetLineWidth(3)
	graph_exclusion_exp_.SetFillColorAlpha(kRed - 0, 0.6)
	graph_exclusion_exp_.SetFillStyle(3353)
	graph_exclusion_exp_.SetLineStyle(kDashed)

	graph_exclusion_exp_p1sig_.SetMarkerStyle(19)
	graph_exclusion_exp_p1sig_.SetMarkerSize(0.0)
	graph_exclusion_exp_p1sig_.SetLineColor(kRed - 0)
	graph_exclusion_exp_p1sig_.SetLineWidth(1)
	graph_exclusion_exp_p1sig_.SetLineStyle(kDashed)

	graph_exclusion_exp_m1sig_.SetMarkerStyle(19)
	graph_exclusion_exp_m1sig_.SetMarkerSize(0.0)
	graph_exclusion_exp_m1sig_.SetLineColor(kRed - 0)
	graph_exclusion_exp_m1sig_.SetLineWidth(1)
	graph_exclusion_exp_m1sig_.SetLineStyle(kDashed)

	graph_exclusion_exp_pm1sig_.SetFillColorAlpha(kRed - 0, 0.6)
	graph_exclusion_exp_pm1sig_.SetFillStyle(3353)

	graph_exclusion_obs_.SetMarkerStyle(19)
	graph_exclusion_obs_.SetMarkerSize(0.0)
	graph_exclusion_obs_.SetLineColor(kBlack)
	graph_exclusion_obs_.SetLineWidth(3)

	graph_exclusion_obs_p1sig_.SetMarkerStyle(19)
	graph_exclusion_obs_p1sig_.SetMarkerSize(0.0)
	graph_exclusion_obs_p1sig_.SetLineColor(kBlack)
	graph_exclusion_obs_p1sig_.SetLineWidth(1)

	graph_exclusion_obs_m1sig_.SetMarkerStyle(19)
	graph_exclusion_obs_m1sig_.SetMarkerSize(0.0)
	graph_exclusion_obs_m1sig_.SetLineColor(kBlack)
	graph_exclusion_obs_m1sig_.SetLineWidth(1)

	graph_exclusion_obs_pm1sig_.SetFillColorAlpha(kBlack, 0.65)
	graph_exclusion_obs_pm1sig_.SetFillStyle(3353)


	graph_exclusion_exp_.Draw("AL")
	graph_exclusion_exp_pm1sig_.Draw("Fsame")
	graph_exclusion_exp_p1sig_.Draw("Lsame")
	graph_exclusion_exp_m1sig_.Draw("Lsame")
	if drawObs:
		graph_exclusion_obs_.Draw("Lsames")

	graph_exclusion_atlas_8TeV_2g.Draw("Lsames")
	graph_exclusion_cms_7TeV_1g.Draw("Fsames")
	graph_exclusion_cms_8TeV_1g.Draw("Fsames")
	graph_exclusion_cms_8TeV_2g.Draw("Fsames")

	####legend
	leg_2d_exclusion_ = TLegend(0.2,0.64,0.84,0.91)
	leg_2d_exclusion_.SetBorderSize(0)
	leg_2d_exclusion_.SetTextSize(0.03)
	#leg_2d_exclusion_.SetLineColor(1)
	#leg_2d_exclusion_.SetLineStyle(1)
	#leg_2d_exclusion_.SetLineWidth(1)
	leg_2d_exclusion_.SetFillColor(0)
	leg_2d_exclusion_.SetFillStyle(1001)

	leg_2d_exclusion_.AddEntry(graph_exclusion_exp_, "CMS Exp (#pm 1 #sigma) 13 TeV "+label_this, "LF")
	if drawObs:
		leg_2d_exclusion_.AddEntry(graph_exclusion_obs_, "CMS Obs 13 TeV "+label_this, "L")
	leg_2d_exclusion_.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV #gamma#gamma", "L")
	leg_2d_exclusion_.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV #gamma#gamma", "F")
	leg_2d_exclusion_.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV #gamma", "F")
	leg_2d_exclusion_.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV #gamma", "F")

	leg_2d_exclusion_.Draw("same")

	drawCMS3(myC2D, 13, lumi_this)

	A1_lambda.Draw("same")

        myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_this+plot_tag+".pdf")
        myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_this+plot_tag+".png")
        myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_this+plot_tag+".C")

	##draw only this analysis, with color map
	##2D color map
	myC2D.SetLogz(1)
	
	stops = np.array([0.0, 1.0])
	red = np.array([0.0, 0.8])
	green = np.array([0.3, 1.0])
	blue = np.array([0.5, 1.0])

	#stops = np.array([0.00, 0.34, 0.61, 0.84, 1.00])
        #red= np.array([0.50, 0.50, 1.00, 1.00, 1.00])
        #green = np.array([ 0.50, 1.00, 1.00, 0.60, 0.50])
        #blue = np.array([1.00, 1.00, 0.50, 0.40, 0.50])

	TColor.CreateGradientColorTable(len(stops), stops, red, green, blue, 255)
	#gStyle.SetPalette(70)	
	gStyle.SetNumberContours(255)
	#gStyle.InvertPalette()
	xbins_th2 = []
	ybins_th2 = []
	xbins_th2.append(100.0)
	for idx in range(len(lambda_points)-1):
		xbins_th2.append(0.5*(lambda_points[idx]+lambda_points[idx+1])*1.454 - 6.0)
	xbins_th2.append(600.0)
	ybins_th2.append(9.0)
	for idx in range(len(ctau_points)-1):
		ybins_th2.append(0.5*(ctau_points[idx]+ctau_points[idx+1]))
	ybins_th2.append(1.2e4)
	ybins_th2.append(1.0e5)
	
	h2_limit_obs = TH2F("h2_limit_obs","h2_limit_obs", len(xbins_th2)-1, np.array(xbins_th2), len(ybins_th2)-1, np.array(ybins_th2))
	for ix in range(len(xbins_th2)-1):
		for iy in range(len(ybins_th2)-2):
			h2_limit_obs.SetBinContent(ix+1, iy+1, limit_obs_2d_grid_[iy][ix])
		h2_limit_obs.SetBinContent(ix+1, len(ybins_th2)-1, 1.0e-6)

	print "xbins_th2"
	print xbins_th2	
	print "ybins_th2"
	print ybins_th2	
	#h2_limit_obs = interpolate2D(h2_limit_obs, epsilon=1,smooth=1,multiplyNbinsX=10, multiplyNbinsY=200)

	f1_lambda_color = TF1("f1_color","(x+6.00)/1.454",72.902, 416.78)
        A1_lambda_color = TGaxis(100.0, 1.5,600.0,1.5,"f1_color",1010,"NI")
	A1_lambda_color.SetLabelFont(42)
	A1_lambda_color.SetLabelSize(0.035)
	A1_lambda_color.SetTextFont(42)
	A1_lambda_color.SetTextSize(1.2)
	A1_lambda_color.SetTitle("#Lambda (TeV)")
	A1_lambda_color.SetTitleSize(0.04)
	A1_lambda_color.SetTitleOffset(0.9)


	h2_limit_obs.GetXaxis().SetTitleSize( axisTitleSize )
	h2_limit_obs.GetXaxis().SetTitleOffset( axisTitleOffset )
	h2_limit_obs.GetYaxis().SetTitleSize( axisTitleSize )
	h2_limit_obs.GetYaxis().SetTitleOffset( axisTitleOffset )
	h2_limit_obs.GetZaxis().SetTitleSize( axisTitleSize )
	h2_limit_obs.GetZaxis().SetTitleOffset( axisTitleOffset)
	h2_limit_obs.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} (GeV)")
	h2_limit_obs.GetZaxis().SetRangeUser(1e-3, 1.0)
	#h2_limit_obs.GetXaxis().SetLimits(100.0, 600.0)
	h2_limit_obs.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} (cm)")
	h2_limit_obs.GetZaxis().SetTitle("95% CL upper limit on cross section (pb)")
	h2_limit_obs.SetTitle("")
	h2_limit_obs.Draw("COLZ")
	#h2_limit_obs.GetYaxis().SetRangeUser(9.0,1.0e5)
	gPad.Update()
	myC.Modified()

	graph_exclusion_exp_.Draw("Lsame")
	graph_exclusion_exp_p1sig_.Draw("Lsame")
	graph_exclusion_exp_m1sig_.Draw("Lsame")
	if drawObs:
		graph_exclusion_obs_.Draw("Lsames")

	leg_2d_exclusion_color = TLegend(0.18,0.774,0.85,0.95)
	leg_2d_exclusion_color.SetBorderSize(1)
	leg_2d_exclusion_color.SetTextSize(0.03)
	leg_2d_exclusion_color.SetFillColor(0)
	leg_2d_exclusion_color.SetFillStyle(1001)
	leg_2d_exclusion_color.SetHeader("    pp #rightarrow #tilde{g}#tilde{g},  #tilde{g} #rightarrow #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")

	leg_2d_exclusion_color.AddEntry(graph_exclusion_exp_, "Expected (#pm 1 #sigma_{experiment}) "+label_this, "L")
	if drawObs:
		leg_2d_exclusion_color.AddEntry(graph_exclusion_obs_, "Observed "+label_this, "L")

	leg_2d_exclusion_color.Draw("same")
	
	##Draw the multiple lines for legend of 1 sigma
	LExpP = TGraph(2)
	LExpP.SetLineColor(kRed - 0)
	LExpP.SetLineWidth(1)
	LExpP.SetLineStyle(kDashed)
	LExpP.SetPoint(0, 119.0, 3.8e4)
	LExpP.SetPoint(1, 206.0, 3.8e4)
	LExpP.Draw("same")	
	
	LExpM = TGraph(2)
	LExpM.SetLineColor(kRed - 0)
	LExpM.SetLineWidth(1)
	LExpM.SetLineStyle(kDashed)
	LExpM.SetPoint(0, 119.0, 2.8e4)
	LExpM.SetPoint(1, 206.0, 2.8e4)
	LExpM.Draw("same")	

	drawCMS3(myC2D, 13, lumi_this)
	A1_lambda_color.Draw("same")

        myC2D.SaveAs(outputDir+"/limits"+"/limit_color_2D_"+year_this+plot_tag+".pdf")
        myC2D.SaveAs(outputDir+"/limits"+"/limit_color_2D_"+year_this+plot_tag+".png")
        myC2D.SaveAs(outputDir+"/limits"+"/limit_color_2D_"+year_this+plot_tag+".C")

	h2_limit_obs = interpolate2D(h2_limit_obs, epsilon=1,smooth=1,multiplyNbinsX=10, multiplyNbinsY=200)
	h2_limit_obs.GetXaxis().SetTitleSize( axisTitleSize )
	h2_limit_obs.GetXaxis().SetTitleOffset( axisTitleOffset )
	h2_limit_obs.GetYaxis().SetTitleSize( axisTitleSize )
	h2_limit_obs.GetYaxis().SetTitleOffset( axisTitleOffset )
	h2_limit_obs.GetZaxis().SetTitleSize( axisTitleSize )
	h2_limit_obs.GetZaxis().SetTitleOffset( axisTitleOffset)
	h2_limit_obs.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} (GeV)")
	h2_limit_obs.GetZaxis().SetRangeUser(1e-3, 1.0)
	#h2_limit_obs.GetXaxis().SetLimits(100.0, 600.0)
	h2_limit_obs.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} (cm)")
	h2_limit_obs.GetZaxis().SetTitle("95% CL upper limit on cross section (pb)")
	h2_limit_obs.SetTitle("")
	h2_limit_obs.Draw("COLZ")

	graph_exclusion_exp_.Draw("Lsame")
	graph_exclusion_exp_p1sig_.Draw("Lsame")
	graph_exclusion_exp_m1sig_.Draw("Lsame")
	if drawObs:
		graph_exclusion_obs_.Draw("Lsames")
	leg_2d_exclusion_color.Draw("same")
	LExpP.Draw("same")	
	LExpM.Draw("same")	
	drawCMS3(myC2D, 13, lumi_this)
	A1_lambda_color.Draw("same")
        myC2D.SaveAs(outputDir+"/limits"+"/limit_color_2D_"+year_this+plot_tag+"_smooth.pdf")
        myC2D.SaveAs(outputDir+"/limits"+"/limit_color_2D_"+year_this+plot_tag+"_smooth.png")
        myC2D.SaveAs(outputDir+"/limits"+"/limit_color_2D_"+year_this+plot_tag+"_smooth.C")
