from ROOT import gROOT, gStyle, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TGraph, kDashed, kGreen, kYellow, TF1, kPink, kGray, TGaxis
import os, sys
from Aux import *
import numpy as np
import array

lumi = 35922.0  + 41530.0
#lumi = 35922.0

outputDir = '/data/zhicaiz/www/sharebox/DelayedPhoton/ARCReview_June2019/orderByPt/'

v1_tag = "v18_Asymptotic"
v2_tag = "v18_HybridNew"
v1_label = "Asymptotic Limits"
v2_label = "HybridNew Limits"

v1_dir = "limitTrees_v18"
v2_dir = "limitTrees_v18_HybridNew"
year_to_plot = "2016And2017"


lambda_points = [100, 150, 200, 250, 300, 350, 400]
ctau_points = [10.0, 50, 100, 200, 400, 600, 800, 1000, 1200, 10000]


drawObs=True
gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=200)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/limits")
os.system("cp draw_limits_compare.py "+outputDir+"/limits")
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

leftMargin   = 0.18
rightMargin  = 0.15
topMargin    = 0.05
bottomMargin = 0.14
bottomMargin2 = 0.22

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

N_lambda = len(lambda_points)
N_ctau = len(ctau_points)

r_exp_2d_grid_v1 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_v1 = np.zeros((N_ctau, N_lambda))

r_exp_2d_grid_v2 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_v2 = np.zeros((N_ctau, N_lambda))




##################limit vs mass #######################3

index_ctau = -1
for ctau_this in ctau_points:
	index_ctau = index_ctau + 1

	xValue_lambda = []
	xValue_mass = []
	yValue_limit_this_Th = []

	limit_this_v1_exp50p0 = []
	limit_this_v1_obs = []

	limit_this_v2_exp50p0 = []
	limit_this_v2_obs = []

	
	yValue_limit_this_v1_exp = []
	yValue_limit_this_v1_obs = []
	
	yValue_limit_this_v2_exp = []
	yValue_limit_this_v2_obs = []
		

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

		minsize = 1000
		actualsize_v1 = 0
		actualsize_v2_exp = 0
		actualsize_v2_obs = 0
		if os.path.isfile(v1_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+".Asymptotic.mH120.root"):
			actualsize_v1 = os.path.getsize(v1_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+".Asymptotic.mH120.root")	
		if os.path.isfile(v2_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+"_Observed.HybridNew.mH120.root"):
			actualsize_v2_obs = os.path.getsize(v2_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+"_Observed.HybridNew.mH120.root")	
		if os.path.isfile(v2_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+"_Exp0p5.HybridNew.mH120.quant0.500.root"):
			actualsize_v2_exp = os.path.getsize(v2_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+"_Exp0p5.HybridNew.mH120.quant0.500.root")	
		if actualsize_v1 > minsize and actualsize_v2_obs > minsize and actualsize_v2_exp > minsize:
			th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)

			file_limit_v1 = TFile(v1_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+".Asymptotic.mH120.root")
			limits_v1 = []
			limitTree_v1 = file_limit_v1.Get("limit")
			for entry in limitTree_v1:
				limits_v1.append(entry.limit)
			print "v1 limits:"
			print limits_v1

			limits_v2 = []

			file_limit_v2_Exp0p5 = TFile(v2_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+"_Exp0p5.HybridNew.mH120.quant0.500.root")
			limitTree_v2_Exp0p5 = file_limit_v2_Exp0p5.Get("limit")

			file_limit_v2_Observed = TFile(v2_dir+"/higgsCombineL"+str(lambda_this)+"TeV_CTau"+ctau_this_str+"cm_"+year_to_plot+"_Observed.HybridNew.mH120.root")
			limitTree_v2_Observed = file_limit_v2_Observed.Get("limit")

			for entry in limitTree_v2_Exp0p5:
				limits_v2.append(entry.limit)
			for entry in limitTree_v2_Observed:
				limits_v2.append(entry.limit)

			print "v2 limits:"
			print limits_v2

			if len(limits_v1) < 6 or len(limits_v2) < 2:
				continue
			
			for idx in range(len(limits_v1)):
				limits_v1[idx] = limits_v1[idx]*limits_SF
			for idx in range(len(limits_v2)):
				limits_v2[idx] = limits_v2[idx]*limits_SF

			xValue_lambda.append(lambda_this)
			xValue_mass.append(lambda_this*1.454-6.0)
			yValue_limit_this_Th.append(th_xsec_this)

			limit_this_v2_exp50p0.append(limits_v2[0]*th_xsec_this)	
			limit_this_v2_obs.append(limits_v2[1]*th_xsec_this)	

			limit_this_v1_exp50p0.append(limits_v1[2]*th_xsec_this)	
			limit_this_v1_obs.append(limits_v1[5]*th_xsec_this)	

			r_exp_2d_grid_v1[index_ctau][index_lambda] = limits_v1[2]
			r_obs_2d_grid_v1[index_ctau][index_lambda] = limits_v1[5]

			r_exp_2d_grid_v2[index_ctau][index_lambda] = limits_v2[0]
			r_obs_2d_grid_v2[index_ctau][index_lambda] = limits_v2[1]

	NPoints_mass = len(xValue_mass)

	for i in range(0, NPoints_mass):
		xValue_mass.append(xValue_mass[i])
		
		yValue_limit_this_v1_obs.append(limit_this_v1_obs[i])
		yValue_limit_this_v1_exp.append(limit_this_v1_exp50p0[i])
			
		yValue_limit_this_v2_obs.append(limit_this_v2_obs[i])
		yValue_limit_this_v2_exp.append(limit_this_v2_exp50p0[i])
		
	myC.SetLogy(1)
	myC.SetLogx(0)
	
	#v1
	graph_limit_vs_mass_v1_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_v1_obs))
	graph_limit_vs_mass_v1_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_v1_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_v1_exp))

	graph_limit_vs_mass_v1_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_v1_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_v1_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_v1_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_v1_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_v1_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_v1_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_v1_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_v1_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_v1_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_v1_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_v1_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_v1_exp_limit.SetLineStyle(kDashed)


	graph_limit_vs_mass_v1_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_v1_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_v1_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_v1_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_v1_exp_limit.SetTitle("")

	graph_limit_vs_mass_v1_exp_limit.Draw("LA")

	graph_limit_vs_mass_v1_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_v1_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_v1_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_v1_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	if drawObs:
		graph_limit_vs_mass_v1_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_v1_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_v1_Th_limit.Draw("Lsame")

	drawCMS3(myC, 13, lumi)

	leg_limit_vs_mass_v1 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_v1.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_v1.SetBorderSize(0)
	leg_limit_vs_mass_v1.SetTextSize(0.03)
	leg_limit_vs_mass_v1.SetLineColor(1)
	leg_limit_vs_mass_v1.SetLineStyle(1)
	leg_limit_vs_mass_v1.SetLineWidth(1)
	leg_limit_vs_mass_v1.SetFillColor(0)
	leg_limit_vs_mass_v1.SetFillStyle(1001)

	leg_limit_vs_mass_v1.AddEntry(graph_limit_vs_mass_v1_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_v1.AddEntry(graph_limit_vs_mass_v1_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_v1.AddEntry(graph_limit_vs_mass_v1_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_v1.Draw()

	#myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+v1_tag+"_ctau"+ctau_this_str+".pdf")
	#myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+v1_tag+"_ctau"+ctau_this_str+".png")
	#myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+v1_tag+"_ctau"+ctau_this_str+".C")

	#v2
	graph_limit_vs_mass_v2_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_v2_obs))
	graph_limit_vs_mass_v2_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_v2_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_v2_exp))

	graph_limit_vs_mass_v2_obs_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_v2_obs_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_v2_obs_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_v2_obs_limit.SetLineWidth(3)

	graph_limit_vs_mass_v2_Th_limit.SetMarkerStyle(22)
	graph_limit_vs_mass_v2_Th_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_v2_Th_limit.SetLineColor(kRed)
	graph_limit_vs_mass_v2_Th_limit.SetLineWidth(2)

	graph_limit_vs_mass_v2_exp_limit.SetMarkerStyle(19)
	graph_limit_vs_mass_v2_exp_limit.SetMarkerSize(1.5)
	graph_limit_vs_mass_v2_exp_limit.SetLineColor(kBlack)
	graph_limit_vs_mass_v2_exp_limit.SetLineWidth(3)
	graph_limit_vs_mass_v2_exp_limit.SetLineStyle(kDashed)


	graph_limit_vs_mass_v2_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_limit_vs_mass_v2_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_limit_vs_mass_v2_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_limit_vs_mass_v2_exp_limit.GetYaxis().SetRangeUser(1e-4,1e4)
	graph_limit_vs_mass_v2_exp_limit.SetTitle("")

	graph_limit_vs_mass_v2_exp_limit.Draw("LA")

	graph_limit_vs_mass_v2_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_v2_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_limit_vs_mass_v2_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_limit_vs_mass_v2_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	if drawObs:
		graph_limit_vs_mass_v2_obs_limit.Draw("Lsame")
	graph_limit_vs_mass_v2_exp_limit.Draw("Lsame")
	graph_limit_vs_mass_v2_Th_limit.Draw("Lsame")

	drawCMS3(myC, 13, lumi)

	leg_limit_vs_mass_v2 = TLegend(0.25,0.62,0.9,0.89)

	leg_limit_vs_mass_v2.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(ctau_this)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass_v2.SetBorderSize(0)
	leg_limit_vs_mass_v2.SetTextSize(0.03)
	leg_limit_vs_mass_v2.SetLineColor(1)
	leg_limit_vs_mass_v2.SetLineStyle(1)
	leg_limit_vs_mass_v2.SetLineWidth(1)
	leg_limit_vs_mass_v2.SetFillColor(0)
	leg_limit_vs_mass_v2.SetFillStyle(1001)

	leg_limit_vs_mass_v2.AddEntry(graph_limit_vs_mass_v2_Th_limit, "Theoretical cross-section", "L")
	if drawObs:
		leg_limit_vs_mass_v2.AddEntry(graph_limit_vs_mass_v2_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass_v2.AddEntry(graph_limit_vs_mass_v2_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass_v2.Draw()

	#myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+v2_tag+"_ctau"+ctau_this_str+".pdf")
	#myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+v2_tag+"_ctau"+ctau_this_str+".png")
	#myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_"+v2_tag+"_ctau"+ctau_this_str+".C")

##################exclusion region of ctau and Lambda/mass #######################

print "value of the 2D r grid (exp, v1) provided from samples: "
print r_exp_2d_grid_v1
print "value of the 2D r grid (obs, v1) provided from samples: "
print r_obs_2d_grid_v1


print "value of the 2D r grid (exp, v2) provided from samples: "
print r_exp_2d_grid_v2
print "value of the 2D r grid (obs, v2) provided from samples: "
print r_obs_2d_grid_v2

###linear interpolation to get the boundary points

lambda_point_boundary_exp_v1 = np.zeros(N_ctau)
lambda_point_boundary_obs_v1 = np.zeros(N_ctau)

lambda_point_boundary_exp_v2 = np.zeros(N_ctau)
lambda_point_boundary_obs_v2 = np.zeros(N_ctau)

for i in range(0, N_ctau):
	print "doing linear interpolation to get the boundary value of lambda for ctau = "+str(ctau_points[i])

	lambda_interp_v1 = []
	r_exp_interp_v1 = []
	r_obs_interp_v1 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_v1[i][j] > 0.00000001:
			lambda_interp_v1.append(lambda_points[j]*1.0)
			r_exp_interp_v1.append(r_exp_2d_grid_v1[i][j]*1.0)
			r_obs_interp_v1.append(r_obs_2d_grid_v1[i][j]*1.0)
	graph_lambda_vs_r_exp_v1 =  TGraph(len(lambda_interp_v1), np.array(r_exp_interp_v1), np.array(lambda_interp_v1))
	lambda_point_boundary_exp_v1[i] = graph_lambda_vs_r_exp_v1.Eval(1.0)
	graph_lambda_vs_r_obs_v1 =  TGraph(len(lambda_interp_v1), np.array(r_obs_interp_v1), np.array(lambda_interp_v1))
	lambda_point_boundary_obs_v1[i] = graph_lambda_vs_r_obs_v1.Eval(1.0)

	lambda_interp_v2 = []
	r_exp_interp_v2 = []
	r_obs_interp_v2 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_v2[i][j] > 0.00000001:
			lambda_interp_v2.append(lambda_points[j]*1.0)
			r_exp_interp_v2.append(r_exp_2d_grid_v2[i][j]*1.0)
			r_obs_interp_v2.append(r_obs_2d_grid_v2[i][j]*1.0)
	graph_lambda_vs_r_exp_v2 =  TGraph(len(lambda_interp_v2), np.array(r_exp_interp_v2), np.array(lambda_interp_v2))
	lambda_point_boundary_exp_v2[i] = graph_lambda_vs_r_exp_v2.Eval(1.0)
	graph_lambda_vs_r_obs_v2 =  TGraph(len(lambda_interp_v2), np.array(r_obs_interp_v2), np.array(lambda_interp_v2))
	lambda_point_boundary_obs_v2[i] = graph_lambda_vs_r_obs_v2.Eval(1.0)

print "lambda points:"
print lambda_points

print "exp (v1) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_v1
print "obs (v1) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_v1

print "exp (v2) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_v2
print "obs (v2) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_v2

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

ctau_points_loop = []

for i in range(0,len(ctau_points)):
	ctau_points_loop.append(ctau_points[i])

for i in range(0, len(ctau_points)):
	ctau_points_loop.append(ctau_points[len(ctau_points)-i-1]*1.0) 

graph_exclusion_exp_v1 = TGraph(len(lambda_point_boundary_exp_v1), np.array(1.454*lambda_point_boundary_exp_v1-6.0), np.array(ctau_points))
graph_exclusion_obs_v1 = TGraph(len(lambda_point_boundary_obs_v1), np.array(1.454*lambda_point_boundary_obs_v1-6.0), np.array(ctau_points))

graph_exclusion_exp_v1.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_v1.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_v1.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_v1.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_v1.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_v1.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_v1.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_v1.GetYaxis().SetRangeUser(0.5,1.0e7)
graph_exclusion_exp_v1.SetTitle("")

graph_exclusion_exp_v1.SetMarkerStyle(19)
graph_exclusion_exp_v1.SetMarkerSize(0.0)
graph_exclusion_exp_v1.SetLineColor(kBlue+1)
graph_exclusion_exp_v1.SetLineWidth(3)
graph_exclusion_exp_v1.SetFillColorAlpha(kBlue+1, 0.65)
graph_exclusion_exp_v1.SetFillStyle(3353)
graph_exclusion_exp_v1.SetLineStyle(kDashed)




graph_exclusion_obs_v1.SetMarkerStyle(19)
graph_exclusion_obs_v1.SetMarkerSize(0.0)
graph_exclusion_obs_v1.SetLineColor(kBlack)
graph_exclusion_obs_v1.SetLineWidth(3)
#graph_exclusion_obs_v1.SetLineStyle(kDashed)

###v2 only
graph_exclusion_exp_v2 = TGraph(len(lambda_point_boundary_exp_v2), np.array(1.454*lambda_point_boundary_exp_v2-6.0), np.array(ctau_points))
graph_exclusion_obs_v2 = TGraph(len(lambda_point_boundary_obs_v2), np.array(1.454*lambda_point_boundary_obs_v2-6.0), np.array(ctau_points))

graph_exclusion_exp_v2.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_v2.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_v2.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_v2.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_v2.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_v2.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_v2.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_v2.GetYaxis().SetRangeUser(0.5,1.0e7)
graph_exclusion_exp_v2.SetTitle("")

graph_exclusion_exp_v2.SetMarkerStyle(19)
graph_exclusion_exp_v2.SetMarkerSize(0.0)
graph_exclusion_exp_v2.SetLineColor(kGreen+3)
graph_exclusion_exp_v2.SetLineWidth(3)
graph_exclusion_exp_v2.SetFillColorAlpha(kGreen+3, 0.65)
graph_exclusion_exp_v2.SetFillStyle(3353)
graph_exclusion_exp_v2.SetLineStyle(kDashed)




graph_exclusion_obs_v2.SetMarkerStyle(19)
graph_exclusion_obs_v2.SetMarkerSize(0.0)
graph_exclusion_obs_v2.SetLineColor(kBlack)
graph_exclusion_obs_v2.SetLineWidth(3)
#graph_exclusion_obs_v2.SetLineStyle(kDashed)

###overlay v1 and v2

graph_exclusion_exp_v1.SetMarkerStyle(19)
graph_exclusion_exp_v1.SetLineColor(kRed)
graph_exclusion_exp_v1.SetFillColorAlpha(kRed, 0.85)
graph_exclusion_exp_v1.SetFillStyle(3356)
graph_exclusion_obs_v1.SetMarkerStyle(19)
graph_exclusion_obs_v1.SetLineColor(kRed)

graph_exclusion_exp_v2.SetMarkerStyle(19)
graph_exclusion_exp_v2.SetLineColor(kBlue)
graph_exclusion_exp_v2.SetFillColorAlpha(kBlue, 0.65)
graph_exclusion_exp_v2.SetFillStyle(3365)
graph_exclusion_obs_v2.SetMarkerStyle(19)
graph_exclusion_obs_v2.SetLineColor(kBlue)

graph_exclusion_exp_v2.Draw("AL")
graph_exclusion_exp_v1.Draw("Lsame")
if drawObs:
	graph_exclusion_obs_v1.Draw("Lsames")
	graph_exclusion_obs_v2.Draw("Lsames")

####legend
leg_2d_exclusion_v1_v2 = TLegend(0.35,0.74,0.92,0.91)
leg_2d_exclusion_v1_v2.SetBorderSize(0)
leg_2d_exclusion_v1_v2.SetTextSize(0.03)
leg_2d_exclusion_v1_v2.SetLineColor(1)
leg_2d_exclusion_v1_v2.SetLineStyle(1)
leg_2d_exclusion_v1_v2.SetLineWidth(1)
leg_2d_exclusion_v1_v2.SetFillColor(0)
leg_2d_exclusion_v1_v2.SetFillStyle(1001)

leg_2d_exclusion_v1_v2.AddEntry(graph_exclusion_exp_v1, v1_label+" Exp", "L")
leg_2d_exclusion_v1_v2.AddEntry(graph_exclusion_exp_v2, v2_label+" Exp", "L")
if drawObs:
	leg_2d_exclusion_v1_v2.AddEntry(graph_exclusion_obs_v1, v1_label+" Obs", "L")
	leg_2d_exclusion_v1_v2.AddEntry(graph_exclusion_obs_v2, v2_label+" Obs", "L")

leg_2d_exclusion_v1_v2.Draw()

drawCMS3(myC2D, 13, lumi)

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

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_to_plot+"_"+v1_tag+"_vs_"+v2_tag+".pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_to_plot+"_"+v1_tag+"_vs_"+v2_tag+".png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_"+year_to_plot+"_"+v1_tag+"_vs_"+v2_tag+".C")

