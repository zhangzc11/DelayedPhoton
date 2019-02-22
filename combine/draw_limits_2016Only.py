from ROOT import gROOT, gStyle, TFile, TTree, TH1, TH1F, THStack, kRed, kBlue, kBlack, kViolet, kOrange, kAzure, TChain, SetOwnership, TCanvas, TLegend, TPad, TGraph, kDashed, kGreen, kYellow, TF1, kPink, kGray, TGaxis
import os, sys
from Aux import *
import numpy as np
import array

lumi_2016 = 35922.0
outputDir = '/data/zhicaiz/www/sharebox/DelayedPhoton/16Jan2019/orderByPt/'

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

r_exp_2d_grid_2016 = np.zeros((N_ctau, N_lambda))
r_exp_p1sig_2d_grid_2016 = np.zeros((N_ctau, N_lambda))
r_exp_m1sig_2d_grid_2016 = np.zeros((N_ctau, N_lambda))
r_obs_2d_grid_2016 = np.zeros((N_ctau, N_lambda))


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

	limit_this_2016_exp2p5 = []
	limit_this_2016_exp16p0 = []
	limit_this_2016_exp50p0 = []
	limit_this_2016_exp84p0 = []
	limit_this_2016_exp97p5 = []
	limit_this_2016_obs = []



	yValue_limit_this_2016_exp = []
	yValue_limit_this_2016_obs = []
	yValue_limit_this_2016_exp1sigma = []
	yValue_limit_this_2016_exp2sigma = []
	
		

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
		minsize = 1000
		actualsize_2016 = 0
		if os.path.isfile("../fit_results/2016/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root"):
			actualsize_2016 = os.path.getsize("../fit_results/2016/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")	

		if actualsize_2016 > minsize:
			xValue_lambda.append(lambda_this)
			xValue_mass.append(lambda_this*1.454-6.0)
			th_xsec_this, eth_xsec_this = getXsecBR(lambda_this, ctau_this)
			yValue_limit_this_Th.append(th_xsec_this)

			file_limit_2016 = TFile("../fit_results/2016/datacards_3J_noBDT//higgsCombineL"+str(lambda_this)+"TeV_Ctau"+ctau_this_str+"cm.Asymptotic.mH120.root")
			limits_2016 = []
			limitTree_2016 = file_limit_2016.Get("limit")
			for entry in limitTree_2016:
				limits_2016.append(entry.limit)
			print limits_2016

			limit_this_2016_exp2p5.append(limits_2016[0]*th_xsec_this)	
			limit_this_2016_exp16p0.append(limits_2016[1]*th_xsec_this)	
			limit_this_2016_exp50p0.append(limits_2016[2]*th_xsec_this)	
			limit_this_2016_exp84p0.append(limits_2016[3]*th_xsec_this)	
			limit_this_2016_exp97p5.append(limits_2016[4]*th_xsec_this)	
			limit_this_2016_obs.append(limits_2016[5]*th_xsec_this)	

			r_exp_2d_grid_2016[index_ctau][index_lambda] = limits_2016[2]
			r_exp_p1sig_2d_grid_2016[index_ctau][index_lambda] = limits_2016[3]
			r_exp_m1sig_2d_grid_2016[index_ctau][index_lambda] = limits_2016[1]
			r_obs_2d_grid_2016[index_ctau][index_lambda] = limits_2016[5]

	NPoints_mass = len(xValue_mass)

	for i in range(0, NPoints_mass):
		xValue_mass.append(xValue_mass[i])
		xValue_mass_exp1sigma.append(xValue_mass[i])
		xValue_mass_exp2sigma.append(xValue_mass[i])
		
		yValue_limit_this_2016_obs.append(limit_this_2016_obs[i])
		yValue_limit_this_2016_exp.append(limit_this_2016_exp50p0[i])
		yValue_limit_this_2016_exp1sigma.append(limit_this_2016_exp16p0[i])
		yValue_limit_this_2016_exp2sigma.append(limit_this_2016_exp2p5[i])
			
			


	for i in range(0, NPoints_mass):
		xValue_mass_exp1sigma.append(xValue_mass[NPoints_mass-i-1])
		xValue_mass_exp2sigma.append(xValue_mass[NPoints_mass-i-1])
		
		yValue_limit_this_2016_exp1sigma.append(limit_this_2016_exp84p0[NPoints_mass-i-1])
		yValue_limit_this_2016_exp2sigma.append(limit_this_2016_exp97p5[NPoints_mass-i-1])

		

	myC.SetLogy(1)
	myC.SetLogx(0)
	
	#2016
	graph_limit_vs_mass_2016_obs_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2016_obs))
	graph_limit_vs_mass_2016_Th_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_Th))
	graph_limit_vs_mass_2016_exp_limit = TGraph(NPoints_mass, np.array(xValue_mass), np.array(yValue_limit_this_2016_exp))
	graph_limit_vs_mass_2016_exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp1sigma), np.array(yValue_limit_this_2016_exp1sigma))
	graph_limit_vs_mass_2016_exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_mass_exp2sigma), np.array(yValue_limit_this_2016_exp2sigma))

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

	graph_limit_vs_mass_2016_exp1sigma_limit.SetFillColor(kGreen)
	graph_limit_vs_mass_2016_exp2sigma_limit.SetFillColor(kYellow)

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

	graph_limit_vs_mass_2016_exp2sigma_limit.Draw("Fsame")
	graph_limit_vs_mass_2016_exp1sigma_limit.Draw("Fsame")
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
	leg_limit_vs_mass_2016.AddEntry(graph_limit_vs_mass_2016_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
	leg_limit_vs_mass_2016.AddEntry(graph_limit_vs_mass_2016_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
	leg_limit_vs_mass_2016.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_ctau"+ctau_this_str+"_2016Only.pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_ctau"+ctau_this_str+"_2016Only.png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_2016_ctau"+ctau_this_str+"_2016Only.C")


##################exclusion region of ctau and Lambda/mass #######################

print "value of the 2D r grid (exp, 2016) provided from samples: "
print r_exp_2d_grid_2016
print "value of the 2D r grid (obs, 2016) provided from samples: "
print r_obs_2d_grid_2016


###linear interpolation to get the boundary points

lambda_point_boundary_exp_2016 = np.zeros(N_ctau)
lambda_point_boundary_exp_p1sig_2016 = np.zeros(N_ctau)
lambda_point_boundary_exp_m1sig_2016 = np.zeros(N_ctau)
lambda_point_boundary_obs_2016 = np.zeros(N_ctau)


for i in range(0, N_ctau):
	print "doing linear interpolation to get the boundary value of lambda for ctau = "+str(ctau_points[i])

	lambda_interp_2016 = []
	r_exp_interp_2016 = []
	r_exp_p1sig_interp_2016 = []
	r_exp_m1sig_interp_2016 = []
	r_obs_interp_2016 = []
	
	for j in range(0, N_lambda):
		if r_exp_2d_grid_2016[i][j] > 0.00000001:
			lambda_interp_2016.append(lambda_points[j]*1.0)
			r_exp_interp_2016.append(r_exp_2d_grid_2016[i][j]*1.0)
			r_exp_p1sig_interp_2016.append(r_exp_p1sig_2d_grid_2016[i][j]*1.0)
			r_exp_m1sig_interp_2016.append(r_exp_m1sig_2d_grid_2016[i][j]*1.0)
			r_obs_interp_2016.append(r_obs_2d_grid_2016[i][j]*1.0)
	graph_lambda_vs_r_exp_2016 =  TGraph(len(lambda_interp_2016), np.array(r_exp_interp_2016), np.array(lambda_interp_2016))
	graph_lambda_vs_r_exp_p1sig_2016 =  TGraph(len(lambda_interp_2016), np.array(r_exp_p1sig_interp_2016), np.array(lambda_interp_2016))
	graph_lambda_vs_r_exp_m1sig_2016 =  TGraph(len(lambda_interp_2016), np.array(r_exp_m1sig_interp_2016), np.array(lambda_interp_2016))
	lambda_point_boundary_exp_2016[i] = graph_lambda_vs_r_exp_2016.Eval(1.0)
	lambda_point_boundary_exp_p1sig_2016[i] = graph_lambda_vs_r_exp_p1sig_2016.Eval(1.0)
	lambda_point_boundary_exp_m1sig_2016[i] = graph_lambda_vs_r_exp_m1sig_2016.Eval(1.0)
	graph_lambda_vs_r_obs_2016 =  TGraph(len(lambda_interp_2016), np.array(r_obs_interp_2016), np.array(lambda_interp_2016))
	lambda_point_boundary_obs_2016[i] = graph_lambda_vs_r_obs_2016.Eval(1.0)
	print "lambda boundary (obs) = "+str(lambda_point_boundary_obs_2016[i])
	print "lambda boundary (exp) = "+str(lambda_point_boundary_exp_2016[i])


print "lambda points:"
print lambda_points

print "exp (2016) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_2016
print "exp p1sig (2016) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_p1sig_2016
print "exp m1sig (2016) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_exp_m1sig_2016
print "obs (2016) exclusion lambda boundary for different ctau:"
print lambda_point_boundary_obs_2016



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

lambda_point_boundary_exp_pm1sig_2016 = []
ctau_points_loop = []

for i in range(0,len(ctau_points)):
	ctau_points_loop.append(ctau_points[i])
	lambda_point_boundary_exp_pm1sig_2016.append(lambda_point_boundary_exp_p1sig_2016[i]*1.0)

for i in range(0, len(ctau_points)):
	ctau_points_loop.append(ctau_points[len(ctau_points)-i-1]*1.0) 
	lambda_point_boundary_exp_pm1sig_2016.append(lambda_point_boundary_exp_m1sig_2016[len(ctau_points)-i-1]*1.0)

graph_exclusion_exp_2016 = TGraph(len(lambda_point_boundary_exp_2016), np.array(1.454*lambda_point_boundary_exp_2016-6.0), np.array(ctau_points))
graph_exclusion_exp_p1sig_2016 = TGraph(len(lambda_point_boundary_exp_p1sig_2016), np.array(1.454*lambda_point_boundary_exp_p1sig_2016-6.0), np.array(ctau_points))
graph_exclusion_exp_m1sig_2016 = TGraph(len(lambda_point_boundary_exp_m1sig_2016), np.array(1.454*lambda_point_boundary_exp_m1sig_2016-6.0), np.array(ctau_points))
graph_exclusion_exp_pm1sig_2016 = TGraph(len(lambda_point_boundary_exp_pm1sig_2016), np.array(1.454*np.array(lambda_point_boundary_exp_pm1sig_2016)-6.0), np.array(ctau_points_loop))
graph_exclusion_obs_2016 = TGraph(len(lambda_point_boundary_obs_2016), np.array(1.454*lambda_point_boundary_obs_2016-6.0), np.array(ctau_points))

graph_exclusion_exp_2016.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2016.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2016.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp_2016.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp_2016.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp_2016.GetXaxis().SetLimits(100.0, 600.0)
graph_exclusion_exp_2016.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp_2016.GetYaxis().SetRangeUser(0.001,1.0e10)
graph_exclusion_exp_2016.SetTitle("")

graph_exclusion_exp_2016.SetMarkerStyle(19)
graph_exclusion_exp_2016.SetMarkerSize(0.0)
graph_exclusion_exp_2016.SetLineColor(kOrange - 9)
graph_exclusion_exp_2016.SetLineWidth(3)
graph_exclusion_exp_2016.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_2016.SetFillStyle(3353)
#graph_exclusion_exp_2016.SetLineStyle(kDashed)

graph_exclusion_exp_p1sig_2016.SetMarkerStyle(19)
graph_exclusion_exp_p1sig_2016.SetMarkerSize(0.0)
graph_exclusion_exp_p1sig_2016.SetLineColor(kOrange - 9)
graph_exclusion_exp_p1sig_2016.SetLineWidth(2)
graph_exclusion_exp_p1sig_2016.SetLineStyle(kDashed)

graph_exclusion_exp_m1sig_2016.SetMarkerStyle(19)
graph_exclusion_exp_m1sig_2016.SetMarkerSize(0.0)
graph_exclusion_exp_m1sig_2016.SetLineColor(kOrange - 9)
graph_exclusion_exp_m1sig_2016.SetLineWidth(2)
graph_exclusion_exp_m1sig_2016.SetLineStyle(kDashed)

graph_exclusion_exp_pm1sig_2016.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp_pm1sig_2016.SetFillStyle(3353)

graph_exclusion_obs_2016.SetMarkerStyle(19)
graph_exclusion_obs_2016.SetMarkerSize(0.0)
graph_exclusion_obs_2016.SetLineColor(kBlack)
graph_exclusion_obs_2016.SetLineWidth(3)
graph_exclusion_obs_2016.SetLineStyle(kDashed)

#graph_exclusion_exp_2016.SetFillColor(kAzure + 7)
#graph_exclusion_exp_2016.SetFillColorAlpha(kOrange - 9, 0.65)

graph_exclusion_exp_2016.Draw("AL")
#graph_exclusion_exp_p1sig_2016.Draw("Lsame")
#graph_exclusion_exp_m1sig_2016.Draw("Lsame")
graph_exclusion_exp_pm1sig_2016.Draw("Fsame")

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
leg_2d_exclusion_2016 = TLegend(0.25,0.64,0.92,0.91)
leg_2d_exclusion_2016.SetBorderSize(0)
leg_2d_exclusion_2016.SetTextSize(0.03)
leg_2d_exclusion_2016.SetLineColor(1)
leg_2d_exclusion_2016.SetLineStyle(1)
leg_2d_exclusion_2016.SetLineWidth(1)
leg_2d_exclusion_2016.SetFillColor(0)
leg_2d_exclusion_2016.SetFillStyle(1001)

leg_2d_exclusion_2016.AddEntry(graph_exclusion_exp_2016, "CMS Exp (#pm 1#sigma) 13 TeV, #gamma#gamma + #slash{E}_{T}", "LF")
if drawObs:
	leg_2d_exclusion_2016.AddEntry(graph_exclusion_obs_2016, "CMS Obs 13 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_2016.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion_2016.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_2016.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
leg_2d_exclusion_2016.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion_2016.Draw()

drawCMS2(myC2D, 13, lumi_2016)

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

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016Only.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016Only.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D_2016Only.C")

