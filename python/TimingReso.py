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
cut = "mass>75 && mass <105 && ele1Pt>30 && ele2Pt>30 && ele1IsEB && ele2IsEB"

file_2016B = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/ZeeTiming_DoubleEG_2016B.root")
tree_2016B = file_2016B.Get("ZeeTiming")
hist_2016B = TH1F("hist_2016B","hist_2016B",100,-1.5,1.5)
tree_2016B.Draw("t1-t2>>hist_2016B",cut)
hist_2016B.SetMarkerStyle( 20 )
hist_2016B.SetMarkerColor(kRed-5)
hist_2016B.SetLineColor(kRed-5)
properScale(hist_2016B)


file_2016C = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/ZeeTiming_DoubleEG_2016C.root")
tree_2016C = file_2016C.Get("ZeeTiming")
hist_2016C = TH1F("hist_2016C","hist_2016C",100,-1.5,1.5)
tree_2016C.Draw("t1-t2>>hist_2016C",cut)
hist_2016C.SetMarkerStyle( 20 )
hist_2016C.SetMarkerColor(kOrange-5)
hist_2016C.SetLineColor(kOrange-5)
properScale(hist_2016C)

file_2016D = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/ZeeTiming_DoubleEG_2016D.root")
tree_2016D = file_2016D.Get("ZeeTiming")
hist_2016D = TH1F("hist_2016D","hist_2016D",100,-1.5,1.5)
tree_2016D.Draw("t1-t2>>hist_2016D",cut)
hist_2016D.SetMarkerStyle( 20 )
hist_2016D.SetMarkerColor(kYellow-5)
hist_2016D.SetLineColor(kYellow-5)
properScale(hist_2016D)

file_2016E = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/ZeeTiming_DoubleEG_2016E.root")
tree_2016E = file_2016E.Get("ZeeTiming")
hist_2016E = TH1F("hist_2016E","hist_2016E",100,-1.5,1.5)
tree_2016E.Draw("t1-t2>>hist_2016E",cut)
hist_2016E.SetMarkerStyle( 20 )
hist_2016E.SetMarkerColor(kSpring-5)
hist_2016E.SetLineColor(kSpring-5)
properScale(hist_2016E)


file_2016F = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/ZeeTiming_DoubleEG_2016F.root")
tree_2016F = file_2016F.Get("ZeeTiming")
hist_2016F = TH1F("hist_2016F","hist_2016F",100,-1.5,1.5)
tree_2016F.Draw("t1-t2>>hist_2016F",cut)
hist_2016F.SetMarkerStyle( 20 )
hist_2016F.SetMarkerColor(kGreen-5)
hist_2016F.SetLineColor(kGreen-5)
properScale(hist_2016F)

file_2016G = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/ZeeTiming_DoubleEG_2016G.root")
tree_2016G = file_2016G.Get("ZeeTiming")
hist_2016G = TH1F("hist_2016G","hist_2016G",100,-1.5,1.5)
tree_2016G.Draw("t1-t2>>hist_2016G",cut)
hist_2016G.SetMarkerStyle( 20 )
hist_2016G.SetMarkerColor(kPink-5)
hist_2016G.SetLineColor(kPink-5)
properScale(hist_2016G)


file_2016H = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/ZeeTiming_DoubleEG_2016H.root")
tree_2016H = file_2016H.Get("ZeeTiming")
hist_2016H = TH1F("hist_2016H","hist_2016H",100,-1.5,1.5)
tree_2016H.Draw("t1-t2>>hist_2016H",cut)
hist_2016H.SetMarkerStyle( 20 )
hist_2016H.SetMarkerColor(kViolet-5)
hist_2016H.SetLineColor(kViolet-5)
properScale(hist_2016H)



file_2016All = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/All2016.root")
tree_2016All = file_2016All.Get("ZeeTiming")
hist_2016All = TH1F("hist_2016All","hist_2016All",100,-1.5,1.5)
tree_2016All.Draw("t1-t2>>hist_2016All",cut)
hist_2016All.SetMarkerStyle( 20 )
hist_2016All.SetMarkerColor(kBlue-5)
hist_2016All.SetLineColor(kBlue-5)
properScale(hist_2016All)

file_2016MC = TFile("/mnt/hadoop/store/group/phys_susy/razor/EcalTiming/ntuples_V3p16_30Aug2017/MC2016_all.root")
tree_2016MC = file_2016MC.Get("ZeeTiming")
hist_2016MC = TH1F("hist_2016MC","hist_2016MC",100,-1.5,1.5)
tree_2016MC.Draw("t1-t2>>hist_2016MC",cut)
hist_2016MC.SetMarkerStyle( 20 )
hist_2016MC.SetMarkerColor(kBlack)
hist_2016MC.SetLineColor(kBlack)
properScale(hist_2016MC)




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


hist_2016B.Draw("E")
hist_2016B.SetTitle("")
hist_2016B.GetXaxis().SetTitle("#Delta T (e1, e2) / ns")
hist_2016B.GetYaxis().SetTitle("Events")
hist_2016B.GetXaxis().SetTitleSize( axisTitleSize )
hist_2016B.GetXaxis().SetTitleOffset( axisTitleOffset )
hist_2016B.GetYaxis().SetTitleSize( axisTitleSize )
hist_2016B.GetYaxis().SetTitleOffset( axisTitleOffset +0.22 )
hist_2016B.GetYaxis().SetRangeUser(0.0,0.08)


hist_2016C.Draw("sameE")
hist_2016D.Draw("sameE")
hist_2016E.Draw("sameE")
hist_2016F.Draw("sameE")
hist_2016G.Draw("sameE")
hist_2016H.Draw("sameE")
hist_2016All.Draw("sameE")
hist_2016MC.Draw("sameE")

##fit
tf1_doubGaus_2016B = TF1("tf1_doubGaus_2016B","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016B.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016B.SetLineColor(kRed-5)
hist_2016B.Fit("tf1_doubGaus_2016B")
sigEff_2016B = 1000.0*(tf1_doubGaus_2016B.GetParameter(0)*np.abs(tf1_doubGaus_2016B.GetParameter(2)) + tf1_doubGaus_2016B.GetParameter(3)*np.abs(tf1_doubGaus_2016B.GetParameter(5)))/(tf1_doubGaus_2016B.GetParameter(0) + tf1_doubGaus_2016B.GetParameter(3) )
meanEff_2016B = 1000.0*(tf1_doubGaus_2016B.GetParameter(0)*np.abs(tf1_doubGaus_2016B.GetParameter(1)) + tf1_doubGaus_2016B.GetParameter(3)*np.abs(tf1_doubGaus_2016B.GetParameter(4)))/(tf1_doubGaus_2016B.GetParameter(0) + tf1_doubGaus_2016B.GetParameter(3) )

tf1_doubGaus_2016C = TF1("tf1_doubGaus_2016C","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016C.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016C.SetLineColor(kOrange-5)
hist_2016C.Fit("tf1_doubGaus_2016C")
sigEff_2016C = 1000.0*(tf1_doubGaus_2016C.GetParameter(0)*np.abs(tf1_doubGaus_2016C.GetParameter(2)) + tf1_doubGaus_2016C.GetParameter(3)*np.abs(tf1_doubGaus_2016C.GetParameter(5)))/(tf1_doubGaus_2016C.GetParameter(0) + tf1_doubGaus_2016C.GetParameter(3) )
meanEff_2016C = 1000.0*(tf1_doubGaus_2016C.GetParameter(0)*np.abs(tf1_doubGaus_2016C.GetParameter(1)) + tf1_doubGaus_2016C.GetParameter(3)*np.abs(tf1_doubGaus_2016C.GetParameter(4)))/(tf1_doubGaus_2016C.GetParameter(0) + tf1_doubGaus_2016C.GetParameter(3) )

tf1_doubGaus_2016D = TF1("tf1_doubGaus_2016D","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016D.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016D.SetLineColor(kYellow-5)
hist_2016D.Fit("tf1_doubGaus_2016D")
sigEff_2016D = 1000.0*(tf1_doubGaus_2016D.GetParameter(0)*np.abs(tf1_doubGaus_2016D.GetParameter(2)) + tf1_doubGaus_2016D.GetParameter(3)*np.abs(tf1_doubGaus_2016D.GetParameter(5)))/(tf1_doubGaus_2016D.GetParameter(0) + tf1_doubGaus_2016D.GetParameter(3) )
meanEff_2016D = 1000.0*(tf1_doubGaus_2016D.GetParameter(0)*np.abs(tf1_doubGaus_2016D.GetParameter(1)) + tf1_doubGaus_2016D.GetParameter(3)*np.abs(tf1_doubGaus_2016D.GetParameter(4)))/(tf1_doubGaus_2016D.GetParameter(0) + tf1_doubGaus_2016D.GetParameter(3) )

tf1_doubGaus_2016E = TF1("tf1_doubGaus_2016E","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016E.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016E.SetLineColor(kSpring-5)
hist_2016E.Fit("tf1_doubGaus_2016E")
sigEff_2016E = 1000.0*(tf1_doubGaus_2016E.GetParameter(0)*np.abs(tf1_doubGaus_2016E.GetParameter(2)) + tf1_doubGaus_2016E.GetParameter(3)*np.abs(tf1_doubGaus_2016E.GetParameter(5)))/(tf1_doubGaus_2016E.GetParameter(0) + tf1_doubGaus_2016E.GetParameter(3) )
meanEff_2016E = 1000.0*(tf1_doubGaus_2016E.GetParameter(0)*np.abs(tf1_doubGaus_2016E.GetParameter(1)) + tf1_doubGaus_2016E.GetParameter(3)*np.abs(tf1_doubGaus_2016E.GetParameter(4)))/(tf1_doubGaus_2016E.GetParameter(0) + tf1_doubGaus_2016E.GetParameter(3) )

tf1_doubGaus_2016F = TF1("tf1_doubGaus_2016F","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016F.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016F.SetLineColor(kGreen-5)
hist_2016F.Fit("tf1_doubGaus_2016F")
sigEff_2016F = 1000.0*(tf1_doubGaus_2016F.GetParameter(0)*np.abs(tf1_doubGaus_2016F.GetParameter(2)) + tf1_doubGaus_2016F.GetParameter(3)*np.abs(tf1_doubGaus_2016F.GetParameter(5)))/(tf1_doubGaus_2016F.GetParameter(0) + tf1_doubGaus_2016F.GetParameter(3) )
meanEff_2016F = 1000.0*(tf1_doubGaus_2016F.GetParameter(0)*np.abs(tf1_doubGaus_2016F.GetParameter(1)) + tf1_doubGaus_2016F.GetParameter(3)*np.abs(tf1_doubGaus_2016F.GetParameter(4)))/(tf1_doubGaus_2016F.GetParameter(0) + tf1_doubGaus_2016F.GetParameter(3) )

tf1_doubGaus_2016G = TF1("tf1_doubGaus_2016G","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016G.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016G.SetLineColor(kPink-5)
hist_2016G.Fit("tf1_doubGaus_2016G")
sigEff_2016G = 1000.0*(tf1_doubGaus_2016G.GetParameter(0)*np.abs(tf1_doubGaus_2016G.GetParameter(2)) + tf1_doubGaus_2016G.GetParameter(3)*np.abs(tf1_doubGaus_2016G.GetParameter(5)))/(tf1_doubGaus_2016G.GetParameter(0) + tf1_doubGaus_2016G.GetParameter(3) )
meanEff_2016G = 1000.0*(tf1_doubGaus_2016G.GetParameter(0)*np.abs(tf1_doubGaus_2016G.GetParameter(1)) + tf1_doubGaus_2016G.GetParameter(3)*np.abs(tf1_doubGaus_2016G.GetParameter(4)))/(tf1_doubGaus_2016G.GetParameter(0) + tf1_doubGaus_2016G.GetParameter(3) )


tf1_doubGaus_2016H = TF1("tf1_doubGaus_2016H","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016H.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016H.SetLineColor(kViolet-5)
hist_2016H.Fit("tf1_doubGaus_2016H")
sigEff_2016H = 1000.0*(tf1_doubGaus_2016H.GetParameter(0)*np.abs(tf1_doubGaus_2016H.GetParameter(2)) + tf1_doubGaus_2016H.GetParameter(3)*np.abs(tf1_doubGaus_2016H.GetParameter(5)))/(tf1_doubGaus_2016H.GetParameter(0) + tf1_doubGaus_2016H.GetParameter(3) )
meanEff_2016H = 1000.0*(tf1_doubGaus_2016H.GetParameter(0)*np.abs(tf1_doubGaus_2016H.GetParameter(1)) + tf1_doubGaus_2016H.GetParameter(3)*np.abs(tf1_doubGaus_2016H.GetParameter(4)))/(tf1_doubGaus_2016H.GetParameter(0) + tf1_doubGaus_2016H.GetParameter(3) )



tf1_doubGaus_2016All = TF1("tf1_doubGaus_2016All","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016All.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016All.SetLineColor(kBlue-5)
hist_2016All.Fit("tf1_doubGaus_2016All")
sigEff_2016All = 1000.0*(tf1_doubGaus_2016All.GetParameter(0)*np.abs(tf1_doubGaus_2016All.GetParameter(2)) + tf1_doubGaus_2016All.GetParameter(3)*np.abs(tf1_doubGaus_2016All.GetParameter(5)))/(tf1_doubGaus_2016All.GetParameter(0) + tf1_doubGaus_2016All.GetParameter(3) )
meanEff_2016All = 1000.0*(tf1_doubGaus_2016All.GetParameter(0)*np.abs(tf1_doubGaus_2016All.GetParameter(1)) + tf1_doubGaus_2016All.GetParameter(3)*np.abs(tf1_doubGaus_2016All.GetParameter(4)))/(tf1_doubGaus_2016All.GetParameter(0) + tf1_doubGaus_2016All.GetParameter(3) )

tf1_doubGaus_2016MC = TF1("tf1_doubGaus_2016MC","gaus(0)+gaus(3)", -1.0,1.0)
tf1_doubGaus_2016MC.SetParameters(0.5,0.0,0.25,0.5,0.0,0.35)
tf1_doubGaus_2016MC.SetLineColor(kBlack)
hist_2016MC.Fit("tf1_doubGaus_2016MC")
sigEff_2016MC = 1000.0*(tf1_doubGaus_2016MC.GetParameter(0)*np.abs(tf1_doubGaus_2016MC.GetParameter(2)) + tf1_doubGaus_2016MC.GetParameter(3)*np.abs(tf1_doubGaus_2016MC.GetParameter(5)))/(tf1_doubGaus_2016MC.GetParameter(0) + tf1_doubGaus_2016MC.GetParameter(3) )
meanEff_2016MC = 1000.0*(tf1_doubGaus_2016MC.GetParameter(0)*np.abs(tf1_doubGaus_2016MC.GetParameter(1)) + tf1_doubGaus_2016MC.GetParameter(3)*np.abs(tf1_doubGaus_2016MC.GetParameter(4)))/(tf1_doubGaus_2016MC.GetParameter(0) + tf1_doubGaus_2016MC.GetParameter(3) )



##legend
leg_mean = TLegend(0.15,0.45,0.35,0.9)
leg_mean.SetBorderSize(0)
leg_mean.SetTextSize(0.03)
leg_mean.SetLineColor(1)
leg_mean.SetLineStyle(1)
leg_mean.SetLineWidth(1)
leg_mean.SetFillColor(0)
leg_mean.SetFillStyle(1001)
leg_mean.AddEntry(hist_2016B, "2016B - #mu = "+"%.1f"%meanEff_2016B+"ps", "lep")
leg_mean.AddEntry(hist_2016C, "2016C - #mu = "+"%.1f"%meanEff_2016C+"ps", "lep")
leg_mean.AddEntry(hist_2016D, "2016D - #mu = "+"%.1f"%meanEff_2016D+"ps", "lep")
leg_mean.AddEntry(hist_2016E, "2016E - #mu = "+"%.1f"%meanEff_2016E+"ps", "lep")
leg_mean.AddEntry(hist_2016F, "2016F - #mu = "+"%.1f"%meanEff_2016F+"ps", "lep")
leg_mean.AddEntry(hist_2016G, "2016G - #mu = "+"%.1f"%meanEff_2016G+"ps", "lep")
leg_mean.AddEntry(hist_2016H, "2016H - #mu = "+"%.1f"%meanEff_2016H+"ps", "lep")
leg_mean.AddEntry(hist_2016All, "2016All - #mu = "+"%.1f"%meanEff_2016All+"ps", "lep")
leg_mean.AddEntry(hist_2016MC, "MC - #mu = "+"%.1f"%meanEff_2016MC+"ps", "lep")
#leg_mean.Draw()

leg_sig = TLegend(0.65,0.45,0.85,0.9)
leg_sig.SetBorderSize(0)
leg_sig.SetTextSize(0.03)
leg_sig.SetLineColor(1)
leg_sig.SetLineStyle(1)
leg_sig.SetLineWidth(1)
leg_sig.SetFillColor(0)
leg_sig.SetFillStyle(1001)
leg_sig.AddEntry(hist_2016B, "2016B - #sigma = "+"%.0f"%sigEff_2016B+"ps", "lep")
leg_sig.AddEntry(hist_2016C, "2016C - #sigma = "+"%.0f"%sigEff_2016C+"ps", "lep")
leg_sig.AddEntry(hist_2016D, "2016D - #sigma = "+"%.0f"%sigEff_2016D+"ps", "lep")
leg_sig.AddEntry(hist_2016E, "2016E - #sigma = "+"%.0f"%sigEff_2016E+"ps", "lep")
leg_sig.AddEntry(hist_2016F, "2016F - #sigma = "+"%.0f"%sigEff_2016F+"ps", "lep")
leg_sig.AddEntry(hist_2016G, "2016G - #sigma = "+"%.0f"%sigEff_2016G+"ps", "lep")
leg_sig.AddEntry(hist_2016H, "2016H - #sigma = "+"%.0f"%sigEff_2016H+"ps", "lep")
leg_sig.AddEntry(hist_2016All, "2016All - #sigma = "+"%.0f"%sigEff_2016All+"ps", "lep")
leg_sig.AddEntry(hist_2016MC, "MC - #sigma = "+"%.0f"%sigEff_2016MC+"ps", "lep")
leg_sig.Draw()


drawCMS(myC, 13, lumi)	

myC.SaveAs(outputDir+"/ZeeTiming/ZeeTiming_Data_vs_MC_2016.pdf")
myC.SaveAs(outputDir+"/ZeeTiming/ZeeTiming_Data_vs_MC_2016.png")
myC.SaveAs(outputDir+"/ZeeTiming/ZeeTiming_Data_vs_MC_2016.C")

