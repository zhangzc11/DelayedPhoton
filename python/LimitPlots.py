from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array

from config import lumi
from config import outputDir
from config import limits_vs_lifetime
from config import mass_limits_vs_lifetime

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
os.system("cp config.py "+outputDir)
os.system("cp StackPlots.py "+outputDir)
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

##################limit vs lifetime #######################3

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
	file_limit = TFile("../fit_results/higgsCombine"+limit_lifetime[0]+".Asymptotic.mH120.root")
	limits = []
	limitTree = file_limit.Get("limit")
	for entry in limitTree:
		limits.append(entry.limit)
	print limits
	yValue_limit_lifetime_Th.append(limit_lifetime[2])
	limit_lifetime_exp2p5.append(limits[0]*limit_lifetime[2])	
	limit_lifetime_exp16p0.append(limits[1]*limit_lifetime[2])	
	limit_lifetime_exp50p0.append(limits[2]*limit_lifetime[2])	
	limit_lifetime_exp84p0.append(limits[3]*limit_lifetime[2])	
	limit_lifetime_exp97p5.append(limits[4]*limit_lifetime[2])	
	limit_lifetime_obs.append(limits[5]*limit_lifetime[2])	
	limit_lifetime_lifetime.append(limit_lifetime[1])

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


graph_obs_limit = TGraph(NPoints_lifetime, np.array(xValue_limit_lifetime_obs), np.array(yValue_limit_lifetime_obs))
graph_Th_limit = TGraph(NPoints_lifetime, np.array(xValue_limit_lifetime_Th), np.array(yValue_limit_lifetime_Th))
graph_exp_limit = TGraph(NPoints_lifetime, np.array(xValue_limit_lifetime_exp), np.array(yValue_limit_lifetime_exp))
graph_exp1sigma_limit = TGraph(2*NPoints_lifetime, np.array(xValue_limit_lifetime_exp1sigma), np.array(yValue_limit_lifetime_exp1sigma))
graph_exp2sigma_limit = TGraph(2*NPoints_lifetime, np.array(xValue_limit_lifetime_exp2sigma), np.array(yValue_limit_lifetime_exp2sigma))

graph_obs_limit.SetMarkerStyle(22)
graph_obs_limit.SetMarkerSize(1.5)
graph_obs_limit.SetLineColor(kBlack)
graph_obs_limit.SetLineWidth(2)

graph_Th_limit.SetMarkerStyle(22)
graph_Th_limit.SetMarkerSize(1.5)
graph_Th_limit.SetLineColor(kRed)
graph_Th_limit.SetLineWidth(2)

graph_exp_limit.SetMarkerStyle(19)
graph_exp_limit.SetMarkerSize(1.5)
graph_exp_limit.SetLineColor(kBlack)
graph_exp_limit.SetLineWidth(2)
graph_exp_limit.SetLineStyle(kDashed)

graph_exp1sigma_limit.SetFillColor(kGreen)
graph_exp2sigma_limit.SetFillColor(kYellow)

graph_exp_limit.GetXaxis().SetTitle("c#tau_{#tilde{#chi}_{1}^{0}} [mm]")
graph_exp_limit.GetXaxis().SetLimits(1e2,1e4)
graph_exp_limit.GetYaxis().SetTitle("#sigma x BR [pb]")
graph_exp_limit.GetYaxis().SetRangeUser(1e-1,5e3)
graph_exp_limit.SetTitle("")

graph_exp_limit.Draw("LA")

graph_exp_limit.GetXaxis().SetTitleSize( axisTitleSize )
graph_exp_limit.GetXaxis().SetTitleOffset( axisTitleOffset )
graph_exp_limit.GetYaxis().SetTitleSize( axisTitleSize )
graph_exp_limit.GetYaxis().SetTitleOffset( axisTitleOffset )

graph_exp2sigma_limit.Draw("Fsame")
graph_exp1sigma_limit.Draw("Fsame")
graph_obs_limit.Draw("Lsame")
graph_exp_limit.Draw("Lsame")
graph_Th_limit.Draw("Lsame")

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

leg_limit_vs_time.AddEntry(graph_Th_limit, "Theoretical cross-section", "L")
leg_limit_vs_time.AddEntry(graph_obs_limit, "Observed  95% CL upper limit", "L")
leg_limit_vs_time.AddEntry(graph_exp_limit, "Expected  95% CL upper limit", "L")
leg_limit_vs_time.AddEntry(graph_exp1sigma_limit, "#pm 1 #sigma Expected", "F")
leg_limit_vs_time.AddEntry(graph_exp2sigma_limit, "#pm 2 #sigma Expected", "F")
leg_limit_vs_time.Draw()

myC.SaveAs(outputDir+"/limit_vs_lifetime_M"+str(mass_limits_vs_lifetime)+".pdf")
myC.SaveAs(outputDir+"/limit_vs_lifetime_M"+str(mass_limits_vs_lifetime)+".png")
myC.SaveAs(outputDir+"/limit_vs_lifetime_M"+str(mass_limits_vs_lifetime)+".C")


