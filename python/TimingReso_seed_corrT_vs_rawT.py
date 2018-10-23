from ROOT import *
import os, sys
from Aux import *
import numpy as np
import array
from config_noBDT import outputDir
from config_noBDT import lumi

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(0)

os.system("mkdir -p "+outputDir+"/ZeeTiming")
os.system("cp TimingReso.py "+outputDir+"/ZeeTiming/")
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


####load data
cut = "mass>60 && mass <120 && ele1Pt>30 && ele2Pt>30 && ele1IsEB && ele2IsEB"

label="timeAll"

#file_2016All = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/EcalTiming/ntuples_V4p1_31Aug2018/All2016.root")
file_2016All = TFile("/data/zhicaiz/release/RazorAnalyzer/CMSSW_9_4_9/src/RazorAnalyzer/ZeeTiming_test_"+label+".root")

tree_2016All = file_2016All.Get("ZeeTiming")
hist_2016All_corrT = TH1F("hist_2016All_corrT","hist_2016All_corrT",100,-1.5,1.5)
hist_2016All_rawT = TH1F("hist_2016All_rawT","hist_2016All_rawT",100,-1.5,1.5)
tree_2016All.Draw("t1calib_seed-t2calib_seed>>hist_2016All_corrT",cut)
tree_2016All.Draw("t1raw_seed-t2raw_seed>>hist_2016All_rawT",cut)

hist_2016All_corrT.SetMarkerStyle( 20 )
hist_2016All_corrT.SetMarkerColor(kBlue)
hist_2016All_corrT.SetLineColor(kBlue)
#properScale(hist_2016All_corrT)

hist_2016All_rawT.SetMarkerStyle( 20 )
hist_2016All_rawT.SetMarkerColor(kRed)
hist_2016All_rawT.SetLineColor(kRed)
#properScale(hist_2016All_rawT)



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

maxY=hist_2016All_rawT.GetMaximum()

hist_2016All_corrT.Draw("E")
hist_2016All_corrT.SetTitle("")
hist_2016All_corrT.GetXaxis().SetTitle("#Delta T (e1 seed, e2 seed) / ns")
hist_2016All_corrT.GetYaxis().SetTitle("Events")
hist_2016All_corrT.GetXaxis().SetTitleSize( axisTitleSize )
hist_2016All_corrT.GetXaxis().SetTitleOffset( axisTitleOffset )
hist_2016All_corrT.GetYaxis().SetTitleSize( axisTitleSize )
hist_2016All_corrT.GetYaxis().SetTitleOffset( axisTitleOffset +0.22 )
hist_2016All_corrT.GetYaxis().SetRangeUser(0.0,1.5*maxY)

hist_2016All_rawT.Draw("sameE")


tf1_doubGaus_2016All_corrT = TF1("tf1_doubGaus_2016All_corrT","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016All_corrT.SetParameters(0.5*maxY,0.0,0.25,0.5*maxY,0.0,0.35)
#tf1_doubGaus_2016All_corrT.SetParLimits(0,0.0000001,100.0000)
#tf1_doubGaus_2016All_corrT.SetParLimits(3,0.0000001,100.0000)
tf1_doubGaus_2016All_corrT.SetParLimits(2,0.1200,1.000)
tf1_doubGaus_2016All_corrT.SetParLimits(5,0.1200,1.000)
tf1_doubGaus_2016All_corrT.SetLineColor(kBlue)
hist_2016All_corrT.Fit("tf1_doubGaus_2016All_corrT","B")
sigEff_2016All_corrT = 1000.0*(tf1_doubGaus_2016All_corrT.GetParameter(0)*np.abs(tf1_doubGaus_2016All_corrT.GetParameter(2)) + tf1_doubGaus_2016All_corrT.GetParameter(3)*np.abs(tf1_doubGaus_2016All_corrT.GetParameter(5)))/(tf1_doubGaus_2016All_corrT.GetParameter(0) + tf1_doubGaus_2016All_corrT.GetParameter(3) )
meanEff_2016All_corrT = 1000.0*(tf1_doubGaus_2016All_corrT.GetParameter(0)*np.abs(tf1_doubGaus_2016All_corrT.GetParameter(1)) + tf1_doubGaus_2016All_corrT.GetParameter(3)*np.abs(tf1_doubGaus_2016All_corrT.GetParameter(4)))/(tf1_doubGaus_2016All_corrT.GetParameter(0) + tf1_doubGaus_2016All_corrT.GetParameter(3) )

tf1_doubGaus_2016All_rawT = TF1("tf1_doubGaus_2016All_rawT","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016All_rawT.SetParameters(0.5*maxY,0.0,0.25,0.5*maxY,0.0,0.35)
#tf1_doubGaus_2016All_rawT.SetParLimits(0,0.0000001,100.0000)
#tf1_doubGaus_2016All_rawT.SetParLimits(3,0.0000001,100.0000)
tf1_doubGaus_2016All_rawT.SetParLimits(2,0.1200,1.000)
tf1_doubGaus_2016All_rawT.SetParLimits(5,0.1200,1.000)
tf1_doubGaus_2016All_rawT.SetLineColor(kRed)
hist_2016All_rawT.Fit("tf1_doubGaus_2016All_rawT","B")
sigEff_2016All_rawT = 1000.0*(tf1_doubGaus_2016All_rawT.GetParameter(0)*np.abs(tf1_doubGaus_2016All_rawT.GetParameter(2)) + tf1_doubGaus_2016All_rawT.GetParameter(3)*np.abs(tf1_doubGaus_2016All_rawT.GetParameter(5)))/(tf1_doubGaus_2016All_rawT.GetParameter(0) + tf1_doubGaus_2016All_rawT.GetParameter(3) )
meanEff_2016All_rawT = 1000.0*(tf1_doubGaus_2016All_rawT.GetParameter(0)*np.abs(tf1_doubGaus_2016All_rawT.GetParameter(1)) + tf1_doubGaus_2016All_rawT.GetParameter(3)*np.abs(tf1_doubGaus_2016All_rawT.GetParameter(4)))/(tf1_doubGaus_2016All_rawT.GetParameter(0) + tf1_doubGaus_2016All_rawT.GetParameter(3) )


##legend
leg_mean = TLegend(0.15,0.7,0.35,0.9)
leg_mean.SetBorderSize(0)
leg_mean.SetTextSize(0.03)
leg_mean.SetLineColor(1)
leg_mean.SetLineStyle(1)
leg_mean.SetLineWidth(1)
leg_mean.SetFillColor(0)
leg_mean.SetFillStyle(1001)
leg_mean.AddEntry(hist_2016All_rawT, "w/o calibration - #mu = "+"%.1f"%meanEff_2016All_rawT+"ps", "lep")
leg_mean.AddEntry(hist_2016All_corrT, "w/ calibration - #mu = "+"%.1f"%meanEff_2016All_corrT+"ps", "lep")
#leg_mean.Draw()

leg_sig = TLegend(0.5,0.7,0.85,0.9)
leg_sig.SetBorderSize(0)
leg_sig.SetTextSize(0.03)
leg_sig.SetLineColor(1)
leg_sig.SetLineStyle(1)
leg_sig.SetLineWidth(1)
leg_sig.SetFillColor(0)
leg_sig.SetFillStyle(1001)
leg_sig.AddEntry(hist_2016All_rawT, "w/o calibration - #sigma = "+"%.0f"%sigEff_2016All_rawT+"ps", "lep")
leg_sig.AddEntry(hist_2016All_corrT, "w/ calibration - #sigma = "+"%.0f"%sigEff_2016All_corrT+"ps", "lep")
leg_sig.Draw()


#drawCMS(myC, 13, lumi)	


myC.SaveAs(outputDir+"/ZeeTiming/ZeeTiming_seed_2016_corrT_vs_rawT_"+label+".pdf")
myC.SaveAs(outputDir+"/ZeeTiming/ZeeTiming_seed_2016_corrT_vs_rawT_"+label+".png")
myC.SaveAs(outputDir+"/ZeeTiming/ZeeTiming_seed_2016_corrT_vs_rawT_"+label+".C")

