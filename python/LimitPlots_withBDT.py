from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array

from config_withBDT import lumi
from config_withBDT import outputDir
#from config_withBDT import limits_vs_lifetime
#from config_withBDT import mass_limits_vs_lifetime
#from config_withBDT import limits_vs_mass
#from config_withBDT import lifetime_limits_vs_mass
from config_withBDT import list_limits_vs_lifetime
from config_withBDT import list_limits_vs_mass

from config_withBDT import exclusion_region_2D
from config_withBDT import grid_mass_exclusion_region_2D
from config_withBDT import grid_lambda_exclusion_region_2D
from config_withBDT import grid_lifetime_exclusion_region_2D

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
np.set_printoptions(linewidth=200)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/limits")
os.system("cp config_withBDT.py "+outputDir+"/limits")
os.system("cp LimitPlots_withBDT.py "+outputDir+"/limits")
#os.system("mkdir -p ../data")
#################plot settings###########################
UseExpoInterp_time = False
UseExpoInterp_lambda = False
ManualSmooth = False

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

##################limit vs lifetime #######################3



for list_this in list_limits_vs_lifetime:
	limits_vs_lifetime = list_this[1]
	mass_limits_vs_lifetime = list_this[0]	

	print "plotting xsec*BR limit for mass point "+str(mass_limits_vs_lifetime)
	limit_lifetime_exp2p5 = []
	limit_lifetime_exp16p0 = []
	limit_lifetime_exp50p0 = []
	limit_lifetime_exp84p0 = []
	limit_lifetime_exp97p5 = []
	limit_lifetime_obs = []
	limit_lifetime_lifetime = []

	xValue_limit_lifetime_Th = []
	xValue_limit_lifetime_exp = []
	xValue_limit_lifetime_obs = []
	xValue_limit_lifetime_exp1sigma = []
	xValue_limit_lifetime_exp2sigma = []

	yValue_limit_lifetime_Th = []
	yValue_limit_lifetime_exp = []
	yValue_limit_lifetime_obs = []
	yValue_limit_lifetime_exp1sigma = []
	yValue_limit_lifetime_exp2sigma = []

	for limit_lifetime in limits_vs_lifetime:
		print "grid: "+limit_lifetime[0]
		file_limit = TFile("../fit_results_smear_reweight/datacards_3J_withBDT/higgsCombine"+limit_lifetime[0]+".Asymptotic.mH120.root")
		limits = []
		limitTree = file_limit.Get("limit")
		for entry in limitTree:
			limits.append(entry.limit)
		print limits
		yValue_limit_lifetime_Th.append(limit_lifetime[4])
		limit_lifetime_exp2p5.append(limits[0]*limit_lifetime[4])	
		limit_lifetime_exp16p0.append(limits[1]*limit_lifetime[4])	
		limit_lifetime_exp50p0.append(limits[2]*limit_lifetime[4])	
		limit_lifetime_exp84p0.append(limits[3]*limit_lifetime[4])	
		limit_lifetime_exp97p5.append(limits[4]*limit_lifetime[4])	
		limit_lifetime_obs.append(limits[5]*limit_lifetime[4])	
		limit_lifetime_lifetime.append(limit_lifetime[3])

	NPoints_lifetime = len(limit_lifetime_lifetime)

	print str(NPoints_lifetime)+" lifetime samples provided..."
	print limit_lifetime_lifetime

	for i in range(0, NPoints_lifetime):
		xValue_limit_lifetime_obs.append(limit_lifetime_lifetime[i])
		xValue_limit_lifetime_Th.append(limit_lifetime_lifetime[i])
		xValue_limit_lifetime_exp.append(limit_lifetime_lifetime[i])
		xValue_limit_lifetime_exp1sigma.append(limit_lifetime_lifetime[i])
		xValue_limit_lifetime_exp2sigma.append(limit_lifetime_lifetime[i])
		
		yValue_limit_lifetime_obs.append(limit_lifetime_obs[i])
		yValue_limit_lifetime_exp.append(limit_lifetime_exp50p0[i])
		yValue_limit_lifetime_exp1sigma.append(limit_lifetime_exp16p0[i])
		yValue_limit_lifetime_exp2sigma.append(limit_lifetime_exp2p5[i])
		

	for i in range(0, NPoints_lifetime):
		xValue_limit_lifetime_exp1sigma.append(limit_lifetime_lifetime[NPoints_lifetime-i-1])
		xValue_limit_lifetime_exp2sigma.append(limit_lifetime_lifetime[NPoints_lifetime-i-1])
		
		yValue_limit_lifetime_exp1sigma.append(limit_lifetime_exp84p0[NPoints_lifetime-i-1])
		yValue_limit_lifetime_exp2sigma.append(limit_lifetime_exp97p5[NPoints_lifetime-i-1])


	print "observed limit"
	print xValue_limit_lifetime_obs
	print yValue_limit_lifetime_obs

	print "theoretical xsec*BR:"
	print xValue_limit_lifetime_Th
	print yValue_limit_lifetime_Th

	print "expected mean limit:"
	print xValue_limit_lifetime_exp
	print yValue_limit_lifetime_exp


	print "expected 1sigma limit:"
	print xValue_limit_lifetime_exp1sigma
	print yValue_limit_lifetime_exp1sigma

	print "expected 2sigma limit:"
	print xValue_limit_lifetime_exp2sigma
	print yValue_limit_lifetime_exp2sigma

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


	graph_lifetime_obs_limit = TGraph(NPoints_lifetime, np.array(xValue_limit_lifetime_obs), np.array(yValue_limit_lifetime_obs))
	graph_lifetime_Th_limit = TGraph(NPoints_lifetime, np.array(xValue_limit_lifetime_Th), np.array(yValue_limit_lifetime_Th))
	graph_lifetime_exp_limit = TGraph(NPoints_lifetime, np.array(xValue_limit_lifetime_exp), np.array(yValue_limit_lifetime_exp))
	graph_lifetime_exp1sigma_limit = TGraph(2*NPoints_lifetime, np.array(xValue_limit_lifetime_exp1sigma), np.array(yValue_limit_lifetime_exp1sigma))
	graph_lifetime_exp2sigma_limit = TGraph(2*NPoints_lifetime, np.array(xValue_limit_lifetime_exp2sigma), np.array(yValue_limit_lifetime_exp2sigma))

	graph_lifetime_obs_limit.SetMarkerStyle(22)
	graph_lifetime_obs_limit.SetMarkerSize(1.5)
	graph_lifetime_obs_limit.SetLineColor(kBlack)
	graph_lifetime_obs_limit.SetLineWidth(2)

	graph_lifetime_Th_limit.SetMarkerStyle(22)
	graph_lifetime_Th_limit.SetMarkerSize(1.5)
	graph_lifetime_Th_limit.SetLineColor(kRed)
	graph_lifetime_Th_limit.SetLineWidth(2)

	graph_lifetime_exp_limit.SetMarkerStyle(19)
	graph_lifetime_exp_limit.SetMarkerSize(1.5)
	graph_lifetime_exp_limit.SetLineColor(kBlack)
	graph_lifetime_exp_limit.SetLineWidth(2)
	graph_lifetime_exp_limit.SetLineStyle(kDashed)

	graph_lifetime_exp1sigma_limit.SetFillColor(kGreen)
	graph_lifetime_exp2sigma_limit.SetFillColor(kYellow)

	graph_lifetime_exp_limit.GetXaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
	graph_lifetime_exp_limit.GetXaxis().SetLimits(0.001,100000.0)
	graph_lifetime_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_lifetime_exp_limit.GetYaxis().SetRangeUser(1e-4,100.0)
	graph_lifetime_exp_limit.SetTitle("")

	graph_lifetime_exp_limit.Draw("LA")

	graph_lifetime_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_lifetime_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_lifetime_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_lifetime_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	graph_lifetime_exp2sigma_limit.Draw("Fsame")
	graph_lifetime_exp1sigma_limit.Draw("Fsame")
	graph_lifetime_obs_limit.Draw("Lsame")
	graph_lifetime_exp_limit.Draw("Lsame")
	graph_lifetime_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_time = TLegend(0.32,0.62,0.9,0.89)

	leg_limit_vs_time.SetHeader("M_{#tilde{#chi}^{0}_{1}} = "+str(mass_limits_vs_lifetime)+" GeV/c^{2},  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_time.SetBorderSize(0)
	leg_limit_vs_time.SetTextSize(0.03)
	leg_limit_vs_time.SetLineColor(1)
	leg_limit_vs_time.SetLineStyle(1)
	leg_limit_vs_time.SetLineWidth(1)
	leg_limit_vs_time.SetFillColor(0)
	leg_limit_vs_time.SetFillStyle(1001)

	leg_limit_vs_time.AddEntry(graph_lifetime_Th_limit, "Theoretical cross-section", "L")
	leg_limit_vs_time.AddEntry(graph_lifetime_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_time.AddEntry(graph_lifetime_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_time.AddEntry(graph_lifetime_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
	leg_limit_vs_time.AddEntry(graph_lifetime_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
	leg_limit_vs_time.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_lifetime_M"+str(int(mass_limits_vs_lifetime))+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_lifetime_M"+str(int(mass_limits_vs_lifetime))+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_lifetime_M"+str(int(mass_limits_vs_lifetime))+".C")

##################limit vs mass #######################3

for list_this in list_limits_vs_mass:
	limits_vs_mass = list_this[1]
	lifetime_limits_vs_mass = list_this[0]	
	
	print "plotting xsec*BR limit for mass point "+str(lifetime_limits_vs_mass)

	limit_mass_exp2p5 = []
	limit_mass_exp16p0 = []
	limit_mass_exp50p0 = []
	limit_mass_exp84p0 = []
	limit_mass_exp97p5 = []
	limit_mass_obs = []
	limit_mass_mass = []

	xValue_limit_mass_Th = []
	xValue_limit_mass_exp = []
	xValue_limit_mass_obs = []
	xValue_limit_mass_exp1sigma = []
	xValue_limit_mass_exp2sigma = []

	yValue_limit_mass_Th = []
	yValue_limit_mass_exp = []
	yValue_limit_mass_obs = []
	yValue_limit_mass_exp1sigma = []
	yValue_limit_mass_exp2sigma = []

	for limit_mass in limits_vs_mass:
		print "grid: "+limit_mass[0]
		file_limit = TFile("../fit_results_smear_reweight/datacards_3J_withBDT/higgsCombine"+limit_mass[0]+".Asymptotic.mH120.root")
		limits = []
		limitTree = file_limit.Get("limit")
		for entry in limitTree:
			limits.append(entry.limit)
		print limits
		yValue_limit_mass_Th.append(limit_mass[4])
		limit_mass_exp2p5.append(limits[0]*limit_mass[4])	
		limit_mass_exp16p0.append(limits[1]*limit_mass[4])	
		limit_mass_exp50p0.append(limits[2]*limit_mass[4])	
		limit_mass_exp84p0.append(limits[3]*limit_mass[4])	
		limit_mass_exp97p5.append(limits[4]*limit_mass[4])	
		limit_mass_obs.append(limits[5]*limit_mass[4])	
		limit_mass_mass.append(limit_mass[2])

	NPoints_mass = len(limit_mass_mass)

	print str(NPoints_mass)+" mass samples provided..."
	print limit_mass_mass

	for i in range(0, NPoints_mass):
		xValue_limit_mass_obs.append(limit_mass_mass[i])
		xValue_limit_mass_Th.append(limit_mass_mass[i])
		xValue_limit_mass_exp.append(limit_mass_mass[i])
		xValue_limit_mass_exp1sigma.append(limit_mass_mass[i])
		xValue_limit_mass_exp2sigma.append(limit_mass_mass[i])
		
		yValue_limit_mass_obs.append(limit_mass_obs[i])
		yValue_limit_mass_exp.append(limit_mass_exp50p0[i])
		yValue_limit_mass_exp1sigma.append(limit_mass_exp16p0[i])
		yValue_limit_mass_exp2sigma.append(limit_mass_exp2p5[i])
		

	for i in range(0, NPoints_mass):
		xValue_limit_mass_exp1sigma.append(limit_mass_mass[NPoints_mass-i-1])
		xValue_limit_mass_exp2sigma.append(limit_mass_mass[NPoints_mass-i-1])
		
		yValue_limit_mass_exp1sigma.append(limit_mass_exp84p0[NPoints_mass-i-1])
		yValue_limit_mass_exp2sigma.append(limit_mass_exp97p5[NPoints_mass-i-1])


	print "observed limit"
	print xValue_limit_mass_obs
	print yValue_limit_mass_obs

	print "theoretical xsec*BR:"
	print xValue_limit_mass_Th
	print yValue_limit_mass_Th

	print "expected mean limit:"
	print xValue_limit_mass_exp
	print yValue_limit_mass_exp


	print "expected 1sigma limit:"
	print xValue_limit_mass_exp1sigma
	print yValue_limit_mass_exp1sigma

	print "expected 2sigma limit:"
	print xValue_limit_mass_exp2sigma
	print yValue_limit_mass_exp2sigma

	myC.SetLogy(1)
	myC.SetLogx(0)

	graph_mass_obs_limit = TGraph(NPoints_mass, np.array(xValue_limit_mass_obs), np.array(yValue_limit_mass_obs))
	graph_mass_Th_limit = TGraph(NPoints_mass, np.array(xValue_limit_mass_Th), np.array(yValue_limit_mass_Th))
	graph_mass_exp_limit = TGraph(NPoints_mass, np.array(xValue_limit_mass_exp), np.array(yValue_limit_mass_exp))
	graph_mass_exp1sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_limit_mass_exp1sigma), np.array(yValue_limit_mass_exp1sigma))
	graph_mass_exp2sigma_limit = TGraph(2*NPoints_mass, np.array(xValue_limit_mass_exp2sigma), np.array(yValue_limit_mass_exp2sigma))

	graph_mass_obs_limit.SetMarkerStyle(22)
	graph_mass_obs_limit.SetMarkerSize(1.5)
	graph_mass_obs_limit.SetLineColor(kBlack)
	graph_mass_obs_limit.SetLineWidth(2)

	graph_mass_Th_limit.SetMarkerStyle(22)
	graph_mass_Th_limit.SetMarkerSize(1.5)
	graph_mass_Th_limit.SetLineColor(kRed)
	graph_mass_Th_limit.SetLineWidth(2)

	graph_mass_exp_limit.SetMarkerStyle(19)
	graph_mass_exp_limit.SetMarkerSize(1.5)
	graph_mass_exp_limit.SetLineColor(kBlack)
	graph_mass_exp_limit.SetLineWidth(2)
	graph_mass_exp_limit.SetLineStyle(kDashed)

	graph_mass_exp1sigma_limit.SetFillColor(kGreen)
	graph_mass_exp2sigma_limit.SetFillColor(kYellow)

	graph_mass_exp_limit.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
	graph_mass_exp_limit.GetXaxis().SetLimits(100.0,600.0)
	graph_mass_exp_limit.GetYaxis().SetTitle("95% CL limit on #sigma x BR [pb]")
	graph_mass_exp_limit.GetYaxis().SetRangeUser(1e-6,1e4)
	#graph_mass_exp_limit.GetYaxis().SetRangeUser(0.0,10)
	graph_mass_exp_limit.SetTitle("")

	graph_mass_exp_limit.Draw("LA")

	graph_mass_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
	graph_mass_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
	graph_mass_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
	graph_mass_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

	graph_mass_exp2sigma_limit.Draw("Fsame")
	graph_mass_exp1sigma_limit.Draw("Fsame")
	graph_mass_obs_limit.Draw("Lsame")
	graph_mass_exp_limit.Draw("Lsame")
	graph_mass_Th_limit.Draw("Lsame")

	drawCMS2(myC, 13, lumi)

	leg_limit_vs_mass = TLegend(0.32,0.62,0.9,0.89)

	leg_limit_vs_mass.SetHeader("c#tau_{#tilde{#chi}_{1}^{0}} = "+str(lifetime_limits_vs_mass)+" cm,  #tilde{#chi}^{0}_{1} #rightarrow #gamma #tilde{G}")
	leg_limit_vs_mass.SetBorderSize(0)
	leg_limit_vs_mass.SetTextSize(0.03)
	leg_limit_vs_mass.SetLineColor(1)
	leg_limit_vs_mass.SetLineStyle(1)
	leg_limit_vs_mass.SetLineWidth(1)
	leg_limit_vs_mass.SetFillColor(0)
	leg_limit_vs_mass.SetFillStyle(1001)

	leg_limit_vs_mass.AddEntry(graph_mass_Th_limit, "Theoretical cross-section", "L")
	leg_limit_vs_mass.AddEntry(graph_mass_obs_limit, "Observed  95% CL upper limit", "L")
	leg_limit_vs_mass.AddEntry(graph_mass_exp_limit, "Expected  95% CL upper limit", "L")
	leg_limit_vs_mass.AddEntry(graph_mass_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
	leg_limit_vs_mass.AddEntry(graph_mass_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
	leg_limit_vs_mass.Draw()

	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_lifetime"+str(int(lifetime_limits_vs_mass))+".pdf")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_lifetime"+str(int(lifetime_limits_vs_mass))+".png")
	myC.SaveAs(outputDir+"/limits"+"/limit_vs_mass_lifetime"+str(int(lifetime_limits_vs_mass))+".C")


##################exclusion region of lifetime and Lambda/mass #######################
N_lambda = len(grid_lambda_exclusion_region_2D)
N_lifetime = len(grid_lifetime_exclusion_region_2D)
#r_exp_2d_grid = [[0.0 for x in range(N_lambda)] for y in range(N_lifetime)]
#r_obs_2d_grid = [[0.0 for x in range(N_lambda)] for y in range(N_lifetime)]
r_exp_2d_grid = np.zeros((N_lifetime, N_lambda))
r_obs_2d_grid = np.zeros((N_lifetime, N_lambda))

print "lifetime grid: "
print grid_lifetime_exclusion_region_2D
print "mass grid: "
print grid_mass_exclusion_region_2D
print "lambda grid: "
print grid_lambda_exclusion_region_2D

print "initial value of the 2D r grid (exp): "
print r_exp_2d_grid
print "initial value of the 2D r grid (obs): "
print r_obs_2d_grid

for limit_2D in exclusion_region_2D:
	#print "grid: "+limit_2D[0]
	file_limit = TFile("../fit_results_smear_reweight/datacards_3J_withBDT/higgsCombine"+limit_2D[0]+".Asymptotic.mH120.root")
	limits = []
	limitTree = file_limit.Get("limit")
	for entry in limitTree:
		limits.append(entry.limit)
	#print limits
	ind_lambda = -1
	ind_lifetime = -1
	for i in range(0, N_lambda):
		if grid_lambda_exclusion_region_2D[i] == limit_2D[1]:
			ind_lambda = i
	
	for i in range(0, N_lifetime):
		if grid_lifetime_exclusion_region_2D[i] == limit_2D[3]:
			ind_lifetime = i
	#print "ind_lambda = "+str(ind_lambda)	
	#print "ind_lifetime = "+str(ind_lifetime)	
	if len(limits) == 6 and ind_lambda > -1 and ind_lifetime > -1:
		r_exp_2d_grid[ind_lifetime][ind_lambda] = limits[2]
		r_obs_2d_grid[ind_lifetime][ind_lambda] = limits[5]

print "value of the 2D r grid (exp) provided from samples: "
print r_exp_2d_grid
print "value of the 2D r grid (obs) provided from samples: "
print r_obs_2d_grid

#do interpolation on the signal strength r

f1_lifetime = TF1("f1_lifetime","expo(0)", 0.0, grid_lifetime_exclusion_region_2D[N_lifetime-1])
f1_mass = TF1("f1_mass","expo(0)", 0.0, grid_mass_exclusion_region_2D[N_lambda-1])
f1_lambda = TF1("f1_lambda","expo(0)", 0.0, grid_lambda_exclusion_region_2D[N_lambda-1])


'''
#interpolation along lambda direction (for a fixed lifetime value)
for i in range(0, N_lifetime):
	N_interp = 0
	lambda_interp = []
	r_exp_interp = []
	r_obs_interp = []

	for j in range(0, N_lambda):
		if r_exp_2d_grid[i][j] > 0.00001:
			N_interp = 1 + N_interp
			lambda_interp.append(grid_lambda_exclusion_region_2D[j])
			r_exp_interp.append(r_exp_2d_grid[i][j])
			r_obs_interp.append(r_obs_2d_grid[i][j])
	if N_interp > 1:
		graph_exp_interp = TGraph(N_interp, np.array(lambda_interp), np.array(r_exp_interp))
		graph_obs_interp = TGraph(N_interp, np.array(lambda_interp), np.array(r_exp_interp))
		for j in range(0, N_lambda):
			if r_exp_2d_grid[i][j] == 0.0:
				
				r_exp_interp = graph_exp_interp.Eval(grid_lambda_exclusion_region_2D[j])
				r_obs_interp = graph_obs_interp.Eval(grid_lambda_exclusion_region_2D[j])
				if N_interp > 2 and UseExpoInterp_lambda:
					graph_exp_interp.Fit(f1_lambda)
					r_exp_interp_temp = f1_lambda.Eval(grid_lambda_exclusion_region_2D[j])
					if r_exp_interp_temp < 10000.0:
						r_exp_interp = r_exp_interp_temp
					graph_obs_interp.Fit(f1_lambda)
					r_obs_interp_temp = f1_lambda.Eval(grid_lambda_exclusion_region_2D[j])
					if r_obs_interp_temp < 10000.0:
						r_obs_interp = r_obs_interp_temp
	
				if r_exp_interp > 0.0:
					r_exp_2d_grid[i][j] = r_exp_interp
				else:
					r_exp_2d_grid[i][j] = 1e-4
				if r_obs_interp > 0.0:
					r_obs_2d_grid[i][j] = r_obs_interp
				else:
					r_obs_2d_grid[i][j] = 1e-4

print "value of the 2D r grid (exp) provided after interpolation in lambda direction: "
print r_exp_2d_grid
print "value of the 2D r grid (obs) provided after interpolation in lambda direction: "
print r_obs_2d_grid

#interpolation along lifetime direction (for a fixed lambda value)
for j in range(0, N_lambda):
	N_interp = 0
	lifetime_interp = []
	r_exp_interp = []
	r_obs_interp = []

	for i in range(0, N_lifetime):
		if r_exp_2d_grid[i][j] > 0.00001:
			N_interp = 1 + N_interp
			lifetime_interp.append(grid_lifetime_exclusion_region_2D[i])
			r_exp_interp.append(r_exp_2d_grid[i][j])
			r_obs_interp.append(r_obs_2d_grid[i][j])
	if N_interp > 1:
		graph_exp_interp = TGraph(N_interp, np.array(lifetime_interp), np.array(r_exp_interp))
		graph_obs_interp = TGraph(N_interp, np.array(lifetime_interp), np.array(r_obs_interp))
		for i in range(0, N_lifetime):
			if r_exp_2d_grid[i][j] == 0.0:
				r_exp_interp = graph_exp_interp.Eval(grid_lifetime_exclusion_region_2D[i])
				r_obs_interp = graph_obs_interp.Eval(grid_lifetime_exclusion_region_2D[i])
				if N_interp > 2 and UseExpoInterp_time:
					graph_exp_interp.Fit(f1_lifetime)
					r_exp_interp_temp = f1_lifetime.Eval(grid_lifetime_exclusion_region_2D[i])
					if r_exp_interp_temp < 10000.0:
						r_exp_interp = r_exp_interp_temp
					graph_obs_interp.Fit(f1_lifetime)
					r_obs_interp_temp = f1_lifetime.Eval(grid_lifetime_exclusion_region_2D[i])
					if r_obs_interp_temp < 10000.0:
						r_obs_interp = r_obs_interp_temp
						
				if r_exp_interp > 0.0:
					r_exp_2d_grid[i][j] = r_exp_interp
				else:
					r_exp_2d_grid[i][j] = 1e-4
				if r_obs_interp > 0.0:
					r_obs_2d_grid[i][j] = r_obs_interp
				else:
					r_obs_2d_grid[i][j] = 1e-4

print "value of the 2D r grid (exp) provided after interpolation in lifetime direction: "
print r_exp_2d_grid
print "value of the 2D r grid (obs) provided after interpolation in lifetime direction: "
print r_obs_2d_grid
'''




N_exp_exclusion_region_final = 0
lambda_exp_exclusion_region_final = []
mass_exp_exclusion_region_final = []
lifetime_exp_exclusion_region_final = []

N_obs_exclusion_region_final = 0
lambda_obs_exclusion_region_final = []
mass_obs_exclusion_region_final = []
lifetime_obs_exclusion_region_final = []


N_exp_exclusion_region_final = 1
N_obs_exclusion_region_final = 1

lambda_exp_exclusion_region_final.append(grid_lambda_exclusion_region_2D[0])
lifetime_exp_exclusion_region_final.append(grid_lifetime_exclusion_region_2D[0])
mass_exp_exclusion_region_final.append(grid_mass_exclusion_region_2D[0])

lambda_obs_exclusion_region_final.append(grid_lambda_exclusion_region_2D[0])
lifetime_obs_exclusion_region_final.append(grid_lifetime_exclusion_region_2D[0])
mass_obs_exclusion_region_final.append(grid_mass_exclusion_region_2D[0])


#now do interpolaton in lifetime direction to find the mass in which r = 1.0 (boundary of the exclusion region)

'''	
for j in range(1, N_lambda):
	N_interp = 0
	lifetime_interp = []
	r_exp_interp = []
	r_obs_interp = []

	for i in range(0, N_lifetime-1):
		if r_exp_2d_grid[i][j] > 0.0:
			N_interp = 1 + N_interp
			lifetime_interp.append(grid_lifetime_exclusion_region_2D[i])
			r_exp_interp.append(r_exp_2d_grid[i][j])
			r_obs_interp.append(r_obs_2d_grid[i][j])
	if N_interp > 1:
		graph_exp_interp = TGraph(N_interp, np.array(r_exp_interp), np.array(lifetime_interp))
		this_lifetime_exp = graph_exp_interp.Eval(1.0)
		if this_lifetime_exp > 0.0:
			lifetime_exp_exclusion_region_final.append(this_lifetime_exp)
			N_exp_exclusion_region_final = 1 + N_exp_exclusion_region_final
			lambda_exp_exclusion_region_final.append(grid_lambda_exclusion_region_2D[j])
			mass_exp_exclusion_region_final.append(grid_mass_exclusion_region_2D[j])

		graph_obs_interp = TGraph(N_interp, np.array(r_obs_interp), np.array(lifetime_interp))
		this_lifetime_obs = graph_obs_interp.Eval(1.0)
		if this_lifetime_obs > 0.0:
			N_obs_exclusion_region_final = 1 + N_obs_exclusion_region_final
			lambda_obs_exclusion_region_final.append(grid_lambda_exclusion_region_2D[j])
			mass_obs_exclusion_region_final.append(grid_mass_exclusion_region_2D[j])
			lifetime_obs_exclusion_region_final.append(graph_obs_interp.Eval(1.0))
'''
for i in range(0, N_lifetime-1):
	N_interp = 0
	lambda_interp = []
	mass_interp = []
	r_exp_interp = []
	r_obs_interp = []

	for j in range(1, N_lambda):
		if r_exp_2d_grid[i][j] > 0.0:
			N_interp = 1 + N_interp
			lambda_interp.append(grid_lambda_exclusion_region_2D[j])
			mass_interp.append(grid_mass_exclusion_region_2D[j])
			r_exp_interp.append(r_exp_2d_grid[i][j])
			r_obs_interp.append(r_obs_2d_grid[i][j])
	if N_interp > 1:
		graph_exp_interp_lambda = TGraph(N_interp, np.array(r_exp_interp), np.array(lambda_interp))
		graph_exp_interp_lambda2 = TGraph(N_interp, np.array(lambda_interp), np.array(r_exp_interp))
		graph_exp_interp_mass = TGraph(N_interp, np.array(r_exp_interp), np.array(mass_interp))
		graph_exp_interp_mass2 = TGraph(N_interp, np.array(mass_interp), np.array(r_exp_interp))
		this_lambda_exp = graph_exp_interp_lambda.Eval(1.0)
		this_mass_exp = graph_exp_interp_mass.Eval(1.0)
		
		print "==============================================================="	
		print "trying to interpolate the mass limit for lifetime = "+str(grid_lifetime_exclusion_region_2D[i])
		print "mass interp linear exp = "+str(this_mass_exp)

		if N_interp > 2 and UseExpoInterp_lambda:
			lambda_Up = grid_lambda_exclusion_region_2D[N_lambda-1] 
			mass_Up = grid_mass_exclusion_region_2D[N_lambda-1]
			'''
			for j in range(1, N_lambda):
				if r_exp_2d_grid[i][j] > r_exp_2d_grid[i][j-1]:
					lambda_Up = grid_lambda_exclusion_region_2D[j]
					mass_Up = grid_mass_exclusion_region_2D[j]
			'''
			
			graph_exp_interp_lambda2.Fit(f1_lambda, "", "", 10.0, lambda_Up)
			chi2_lambda = f1_lambda.GetChisquare()
			if chi2_lambda < 50.0:
				this_lambda_exp_temp = f1_lambda.GetX(1.0, 0.0, lambda_Up)
				if this_lambda_exp_temp > this_lambda_exp and this_lambda_exp_temp < 1.2*this_lambda_exp:
					this_lambda_exp = this_lambda_exp_temp
			graph_exp_interp_mass2.Fit(f1_mass, "", "", 10.0, mass_Up)
			chi2_mass = f1_mass.GetChisquare()
			if chi2_mass < 50.0:
				this_mass_exp_temp = f1_mass.GetX(1.0, 0.0, mass_Up)
				if this_mass_exp_temp > this_mass_exp and this_mass_exp_temp < 1.2* this_mass_exp:
					this_mass_exp = this_mass_exp_temp
			print "mass interp expo exp = "+str(this_mass_exp)

		if ManualSmooth and N_exp_exclusion_region_final > 0 and this_lambda_exp < lambda_exp_exclusion_region_final[N_exp_exclusion_region_final - 1]:
			this_lambda_exp = lambda_exp_exclusion_region_final[N_exp_exclusion_region_final - 1]
			this_mass_exp = mass_exp_exclusion_region_final[N_exp_exclusion_region_final - 1]
		if this_lambda_exp > 0.0:
			lambda_exp_exclusion_region_final.append(this_lambda_exp)
			mass_exp_exclusion_region_final.append(this_mass_exp)
			N_exp_exclusion_region_final = 1 + N_exp_exclusion_region_final
			lifetime_exp_exclusion_region_final.append(grid_lifetime_exclusion_region_2D[i])

		graph_obs_interp_lambda = TGraph(N_interp, np.array(r_obs_interp), np.array(lambda_interp))
		graph_obs_interp_lambda2 = TGraph(N_interp, np.array(lambda_interp), np.array(r_obs_interp))
		graph_obs_interp_mass = TGraph(N_interp, np.array(r_obs_interp), np.array(mass_interp))
		graph_obs_interp_mass2 = TGraph(N_interp, np.array(mass_interp), np.array(r_obs_interp))
		this_lambda_obs = graph_obs_interp_lambda.Eval(1.0)
		this_mass_obs = graph_obs_interp_mass.Eval(1.0)

		print "mass interp linear obs = "+str(this_mass_obs)
		if N_interp > 2 and UseExpoInterp_lambda:
			lambda_Up = grid_lambda_exclusion_region_2D[N_lambda-1] 
			mass_Up = grid_mass_exclusion_region_2D[N_lambda-1]
			'''
			for j in range(1, N_lambda):
				if r_obs_2d_grid[i][j] > r_obs_2d_grid[i][j-1]:
					lambda_Up = grid_lambda_exclusion_region_2D[j]
					mass_Up = grid_mass_exclusion_region_2D[j]
			'''
			
			graph_obs_interp_lambda2.Fit(f1_lambda, "", "", 10.0, lambda_Up)
			chi2_lambda = f1_lambda.GetChisquare()
			if chi2_lambda < 50.0:
				this_lambda_obs_temp = f1_lambda.GetX(1.0, 0.0, lambda_Up)
				if this_lambda_obs_temp > this_lambda_obs and this_lambda_obs_temp < 1.2* this_lambda_obs:
					this_lambda_obs = this_lambda_obs_temp
			graph_obs_interp_mass2.Fit(f1_mass, "", "", 10.0, mass_Up)
			chi2_mass = f1_mass.GetChisquare()
			if chi2_mass < 50.0:
				this_mass_obs_temp = f1_mass.GetX(1.0, 0.0, mass_Up)
				if this_mass_obs_temp > this_mass_obs and this_mass_obs_temp < 1.2*this_mass_obs:
					this_mass_obs = this_mass_obs_temp
			print "mass interp expo obs = "+str(this_mass_obs)

		if ManualSmooth and N_obs_exclusion_region_final > 0 and this_lambda_obs < lambda_obs_exclusion_region_final[N_obs_exclusion_region_final - 1]:
			this_lambda_obs = lambda_obs_exclusion_region_final[N_obs_exclusion_region_final - 1]
			this_mass_obs = mass_obs_exclusion_region_final[N_obs_exclusion_region_final - 1]
			print "mass interp obs smooth = "+str(this_mass_obs)
		if this_lambda_obs > 0.0:

			lambda_obs_exclusion_region_final.append(this_lambda_obs)
			mass_obs_exclusion_region_final.append(this_mass_obs)
			N_obs_exclusion_region_final = 1 + N_obs_exclusion_region_final
			lifetime_obs_exclusion_region_final.append(grid_lifetime_exclusion_region_2D[i])


N_exp_exclusion_region_final = 1 + N_exp_exclusion_region_final
lambda_exp_exclusion_region_final.append(grid_lambda_exclusion_region_2D[0])
lifetime_exp_exclusion_region_final.append(grid_lifetime_exclusion_region_2D[N_lifetime-1])
mass_exp_exclusion_region_final.append(grid_mass_exclusion_region_2D[0])

N_obs_exclusion_region_final = 1 + N_obs_exclusion_region_final
lambda_obs_exclusion_region_final.append(grid_lambda_exclusion_region_2D[0])
lifetime_obs_exclusion_region_final.append(grid_lifetime_exclusion_region_2D[N_lifetime-1])
mass_obs_exclusion_region_final.append(grid_mass_exclusion_region_2D[0])



print "final exclusion region boundary (exp):"
print "N = "+str(N_exp_exclusion_region_final)
print "mass: "
print mass_exp_exclusion_region_final
print "lambda: "
print lambda_exp_exclusion_region_final
print "lifetime: "
print lifetime_exp_exclusion_region_final

print "final exclusion region boundary (obs):"
print "N = "+str(N_obs_exclusion_region_final)
print "mass: "
print mass_obs_exclusion_region_final
print "lambda: "
print lambda_obs_exclusion_region_final
print "lifetime: "
print lifetime_obs_exclusion_region_final



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

graph_exclusion_exp = TGraph(N_exp_exclusion_region_final, np.array(mass_exp_exclusion_region_final), np.array(lifetime_exp_exclusion_region_final))
graph_exclusion_obs = TGraph(N_obs_exclusion_region_final, np.array(mass_obs_exclusion_region_final), np.array(lifetime_obs_exclusion_region_final))

graph_exclusion_exp.GetXaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp.GetYaxis().SetTitleSize( axisTitleSize )
graph_exclusion_exp.GetYaxis().SetTitleOffset( axisTitleOffset )
graph_exclusion_exp.GetXaxis().SetTitle("M_{#tilde{#chi}^{0}_{1}} [GeV]")
graph_exclusion_exp.GetXaxis().SetLimits(100.0, 800.0)
graph_exclusion_exp.GetYaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [cm]")
graph_exclusion_exp.GetYaxis().SetRangeUser(0.095,1e7)
graph_exclusion_exp.SetTitle("")

graph_exclusion_exp.SetMarkerStyle(19)
graph_exclusion_exp.SetMarkerSize(0.0)
graph_exclusion_exp.SetLineColor(kBlack)
graph_exclusion_exp.SetLineWidth(2)
graph_exclusion_exp.SetLineStyle(kDashed)

#graph_exclusion_obs.SetFillColor(kAzure + 7)
graph_exclusion_obs.SetFillColorAlpha(kOrange - 9, 0.65)
graph_exclusion_exp.Draw("AL*")
graph_exclusion_obs.Draw("F*same")

#####ATLAS 8TeV
lambda_atlas_8TeV_2g = np.array([82.5 , 102.5,   140,   160,   180,   200,   220, 260,  300, 302.58, 300, 260, 220, 200 ])
t_atlas_8TeV_2g = np.array([ 121.81, 90.94, 46.63, 36.12, 27.18, 20.26, 14.59, 7.47, 2.6, 1.83, 1.31, 0.61, 0.39, 0.30 ])
lifetime_atlas_8TeV_2g = t_atlas_8TeV_2g * 30.0
mass_atlas_8TeV_2g = lambda_atlas_8TeV_2g*1.45 - 5.0
graph_exclusion_atlas_8TeV_2g = TGraph(14, mass_atlas_8TeV_2g, lifetime_atlas_8TeV_2g)
graph_exclusion_atlas_8TeV_2g.SetLineColor(8)
graph_exclusion_atlas_8TeV_2g.SetLineWidth(3)
graph_exclusion_atlas_8TeV_2g.SetLineStyle(5)
graph_exclusion_atlas_8TeV_2g.Draw("Lsames")

######CMS 7TeV
mass_cms_7TeV_1g = np.array([100., 145., 157., 179., 192., 216., 221., 218., 218., 221., 216., 192., 179., 157., 145., 100.])
lifetime_cms_7TeV_1g  = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10., 25.0, 50.0, 100.0, 200.0, 400.0, 600.0, 600.0])
graph_exclusion_cms_7TeV_1g = TGraph(16, mass_cms_7TeV_1g, lifetime_cms_7TeV_1g)
graph_exclusion_cms_7TeV_1g.SetFillColorAlpha(kPink, 0.65)
graph_exclusion_cms_7TeV_1g.Draw("Fsames")

######CMS 8TeV, single photon
mass_cms_8TeV_1g = np.array([140.0,   169.0,   198.0,  227.0,   256.0,    314.,    314., 285.,    256.,     227.,     198.,     169.,     140.])
lifetime_cms_8TeV_1g  = np.array([92.39, 56.98, 51.43, 48.6, 70.59, 138.78, 212.92, 290, 702.16, 1063.61, 1298.93, 1243.29, 1349.28])
graph_exclusion_cms_8TeV_1g = TGraph(13, mass_cms_8TeV_1g, lifetime_cms_8TeV_1g)
graph_exclusion_cms_8TeV_1g.SetFillColorAlpha(kBlue, 0.65)
graph_exclusion_cms_8TeV_1g.Draw("Fsames")

######CMS 8TeV, two photons
mass_cms_8TeV_2g = np.array([198., 227., 256., 256., 227., 198.])
lifetime_cms_8TeV_2g  = np.array([0.4, 2, 9, 9, 25., 50.])
graph_exclusion_cms_8TeV_2g = TGraph(6, mass_cms_8TeV_2g, lifetime_cms_8TeV_2g)
graph_exclusion_cms_8TeV_2g.SetFillColorAlpha(kGray+1, 0.65)
graph_exclusion_cms_8TeV_2g.Draw("Fsames")


####legend
leg_2d_exclusion = TLegend(0.45,0.64,0.92,0.91)
leg_2d_exclusion.SetBorderSize(0)
leg_2d_exclusion.SetTextSize(0.03)
leg_2d_exclusion.SetLineColor(1)
leg_2d_exclusion.SetLineStyle(1)
leg_2d_exclusion.SetLineWidth(1)
leg_2d_exclusion.SetFillColor(0)
leg_2d_exclusion.SetFillStyle(1001)

leg_2d_exclusion.AddEntry(graph_exclusion_exp, "CMS Exp 13 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion.AddEntry(graph_exclusion_obs, "CMS Obs 13 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion.AddEntry(graph_exclusion_atlas_8TeV_2g, "ATLAS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "L")
leg_2d_exclusion.AddEntry(graph_exclusion_cms_8TeV_2g, "CMS Obs 8 TeV, #gamma#gamma + #slash{E}_{T}", "F")
leg_2d_exclusion.AddEntry(graph_exclusion_cms_8TeV_1g, "CMS Obs 8 TeV, #gamma + #slash{E}_{T}", "F")
leg_2d_exclusion.AddEntry(graph_exclusion_cms_7TeV_1g, "CMS Obs 7 TeV, #gamma + #slash{E}_{T}", "F")

leg_2d_exclusion.Draw()


drawCMS2(myC2D, 13, lumi)


#Lambda axis
f1_lambda = TF1("f1","(x+6.00)/1.454",72.902, 554.33)
A1_lambda = TGaxis(100.0, 0.0025,800.0,0.0025,"f1",1010)
A1_lambda.SetLabelFont(42)
A1_lambda.SetLabelSize(0.035)
A1_lambda.SetTextFont(42)
A1_lambda.SetTextSize(1.2)
A1_lambda.SetTitle("#Lambda [TeV]")
A1_lambda.SetTitleSize(0.04)
A1_lambda.SetTitleOffset(0.9)
A1_lambda.Draw()

myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D.pdf")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D.png")
myC2D.SaveAs(outputDir+"/limits"+"/limit_exclusion_region_2D.C")







