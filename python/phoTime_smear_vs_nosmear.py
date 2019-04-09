from ROOT import gROOT, gStyle, TFile, TTree, TCanvas, TH1F, TH1, TLegend, TLatex, TColor, TF1, TGraphErrors, kBlue, kRed, kViolet, kBlack, kOrange, kAzure
import os, sys
from Aux import *
from config_noBDT import fileNameData, fileNameSig, fileNameGJets, fileNameQCD, cut, cut_noDisc, splots, lumi, outputDir, xsecSig, xsecGJets, xsecQCD
from config_noBDT import fractionGJets, fractionQCD, useFraction, kFactor, cut_GJets, cut_QCD_CR, xbins_MET, xbins_time, sigLegend, timeShift, weight_cut
import numpy as np
import array

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir+"/stack")
os.system("mkdir -p "+outputDir+"/stack")
os.system("cp config_noBDT.py "+outputDir+"/stack")
os.system("cp phoTime_smear_vs_nosmear.py "+outputDir+"/stack")
#os.system("mkdir -p ../data")
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
topMargin    = 0.07
bottomMargin = 0.12
##############load delayed photon input tree#############

print "\n"
print "input file names: "
print "Data tree: "+fileNameData
print "Sig tree: "+fileNameSig
print "GJets tree: "
print fileNameGJets
print "QCD tree: "
print fileNameQCD


print "NTotal before cut: "

fileData = TFile(fileNameData)
treeData = fileData.Get("DelayedPhoton")
hNEventsData = fileData.Get("NEvents")
NEventsData = hNEventsData.GetBinContent(1)
print "Data: " + str(NEventsData)

fileSig = TFile(fileNameSig)
treeSig = fileSig.Get("DelayedPhoton")
hNEventsSig = fileSig.Get("NEvents")
NEventsSig = hNEventsSig.GetBinContent(1)
print "Sig: " + str(NEventsSig)

fileSig_t2 = TFile(fileNameSig.replace('200cm','0_1cm'))
treeSig_t2 = fileSig_t2.Get("DelayedPhoton")
hNEventsSig_t2 = fileSig_t2.Get("NEvents")
NEventsSig_t2 = hNEventsSig_t2.GetBinContent(1)
print "Sig_t2: " + str(NEventsSig_t2)



fileGJets = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HTAll_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
treeGJets = fileGJets.Get("DelayedPhoton")
hNEventsGJets = fileGJets.Get("NEvents")
NEventsGJets = hNEventsGJets.GetBinContent(1)
print "GJets: " + str(NEventsGJets)

fileQCD = TFile("/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HTAll_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
treeQCD = fileQCD.Get("DelayedPhoton")
hNEventsQCD = fileQCD.Get("NEvents")
NEventsQCD = hNEventsQCD.GetBinContent(1)
print "QCD: " + str(NEventsQCD)

print NEventsGJets
print NEventsQCD

#cut = "abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 "


print "\n cut = " + cut

weightedcut =  weight_cut + cut 

plot_noSmear = ["pho1ClusterTime", "phoTimeCluster_noSmear_log", "#gamma cluster time [ns]", 100,-5,15, True]
plot_Smear = ["pho1ClusterTime_SmearToData", "phoTimeCluster_Smear_log", "#gamma cluster time [ns]", 100,-5,15, True]
	
#data
histData = TH1F(plot_noSmear[1]+"_histData","",plot_noSmear[3],plot_noSmear[4],plot_noSmear[5])	
treeData.Draw(plot_noSmear[0]+">>"+plot_noSmear[1]+"_histData",cut_GJets)
histData.SetMarkerStyle( 20 )
histData.SetMarkerColor( kBlack )
histData.SetLineColor( kBlack )

#Sig
histSig_noSmear = TH1F(plot_noSmear[1]+"_histSig_noSmear","",plot_noSmear[3],plot_noSmear[4],plot_noSmear[5])	
histSig_Smear = TH1F(plot_Smear[1]+"_histSig_Smear","",plot_Smear[3],plot_Smear[4],plot_Smear[5])	

treeSig.Draw(plot_noSmear[0]+">>"+plot_noSmear[1]+"_histSig_noSmear",weightedcut)
treeSig.Draw(plot_Smear[0]+"+"+str(timeShift)+">>"+plot_Smear[1]+"_histSig_Smear",weightedcut)
histSig_noSmear.Scale(lumi*xsecSig/NEventsSig)
histSig_Smear.Scale(lumi*xsecSig/NEventsSig)

histSig_noSmear.SetLineWidth( 2 )
histSig_Smear.SetLineWidth( 2 )
histSig_noSmear.SetLineColor( kRed )
histSig_Smear.SetLineColor( kRed - 5)
histSig_Smear.SetLineStyle( 7 )

#Sig_t2
histSig_Ctau2_noSmear = TH1F(plot_noSmear[1]+"_histSig_Ctau2_noSmear","",plot_noSmear[3],plot_noSmear[4],plot_noSmear[5])	
histSig_Ctau2_Smear = TH1F(plot_Smear[1]+"_histSig_Ctau2_Smear","",plot_Smear[3],plot_Smear[4],plot_Smear[5])	

treeSig_t2.Draw(plot_noSmear[0]+">>"+plot_noSmear[1]+"_histSig_Ctau2_noSmear",weightedcut)
treeSig_t2.Draw(plot_Smear[0]+"+"+str(timeShift)+">>"+plot_Smear[1]+"_histSig_Ctau2_Smear",weightedcut)
histSig_Ctau2_noSmear.Scale(lumi*xsecSig/NEventsSig_t2)
histSig_Ctau2_Smear.Scale(lumi*xsecSig/NEventsSig_t2)

histSig_Ctau2_noSmear.SetLineWidth( 2 )
histSig_Ctau2_Smear.SetLineWidth( 2 )
histSig_Ctau2_noSmear.SetLineColor( kViolet )
histSig_Ctau2_Smear.SetLineColor( kViolet - 5)
histSig_Ctau2_Smear.SetLineStyle( 7 )


#QCD
histQCD_noSmear = TH1F(plot_noSmear[1]+"_histQCD_noSmear","",plot_noSmear[3],plot_noSmear[4],plot_noSmear[5])	
treeQCD.Draw(plot_noSmear[0]+">>"+plot_noSmear[1]+"_histQCD_noSmear",weightedcut)

histQCD_noSmear.Scale(histData.Integral()/histQCD_noSmear.Integral())
histQCD_noSmear.SetLineColor(kOrange)
histQCD_noSmear.SetLineWidth( 2 )

#QCD
histQCD_Smear = TH1F(plot_Smear[1]+"_histQCD_Smear","",plot_Smear[3],plot_Smear[4],plot_Smear[5])	
treeQCD.Draw(plot_Smear[0]+">>"+plot_Smear[1]+"_histQCD_Smear",weightedcut)

histQCD_Smear.Scale(histData.Integral()/histQCD_Smear.Integral())
histQCD_Smear.SetLineColor(kOrange - 9)
histQCD_Smear.SetLineWidth( 2 )
histQCD_Smear.SetLineStyle( 7 )


#GJets
histGJets_noSmear = TH1F(plot_noSmear[1]+"_histGJets_noSmear","",plot_noSmear[3],plot_noSmear[4],plot_noSmear[5])	
print NEventsGJets
print NEventsQCD
treeGJets.Draw(plot_noSmear[0]+">>"+plot_noSmear[1]+"_histGJets_noSmear",weightedcut)

histGJets_noSmear.Scale(histData.Integral()/histGJets_noSmear.Integral())
histGJets_noSmear.SetLineColor(kAzure )
histGJets_noSmear.SetLineWidth( 2 )

	
#GJets
histGJets_Smear = TH1F(plot_Smear[1]+"_histGJets_Smear","",plot_Smear[3],plot_Smear[4],plot_Smear[5])	
print NEventsGJets
print NEventsQCD
treeGJets.Draw(plot_Smear[0]+">>"+plot_Smear[1]+"_histGJets_Smear",weightedcut)
histGJets_Smear.Scale(histData.Integral()/histGJets_Smear.Integral())
histGJets_Smear.SetLineColor(kAzure + 7)
histGJets_Smear.SetLineWidth( 2 )
histGJets_Smear.SetLineStyle( 7 )


leg = TLegend(0.42, 0.55, 0.93, 0.89)
#leg.SetNColumns(2)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(0)
leg.SetFillStyle(1001)
leg.AddEntry(histData, "data - #gamma + jets CR","lep")
leg.AddEntry(histSig_noSmear, "signal(Ctau 200cm) - no corr.")
leg.AddEntry(histSig_Smear, "signal(Ctau 200cm) - after corr.")
leg.AddEntry(histSig_Ctau2_noSmear, "signal(Ctau 0.1cm) - no corr.")
leg.AddEntry(histSig_Ctau2_Smear, "signal(Ctau 0.1cm) - after corr.")
leg.AddEntry(histGJets_noSmear, "#gamma + jets (MC) - no corr.")
leg.AddEntry(histGJets_Smear, "#gamma + jets (MC) - after corr.")
leg.AddEntry(histQCD_noSmear, "QCD (MC) - no corr.")
leg.AddEntry(histQCD_Smear, "QCD (MC) - after corr.")

	
myC = TCanvas( "myC", "myC", 200, 10, 800, 800 )
#myC.SetGridx(1)
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
myC.SetLogy(plot_noSmear[6])
	
histGJets_noSmear.SetTitle("")
histGJets_noSmear.Draw()
histGJets_noSmear.GetXaxis().SetTitleSize( axisTitleSize )
histGJets_noSmear.GetXaxis().SetTitleOffset( axisTitleOffset )
histGJets_noSmear.GetYaxis().SetTitleSize( axisTitleSize )
histGJets_noSmear.GetYaxis().SetTitleOffset( axisTitleOffset )
histGJets_noSmear.GetYaxis().SetTitle("events")
histGJets_noSmear.GetXaxis().SetTitle(plot_noSmear[2])

if plot_noSmear[6]:
	histGJets_noSmear.SetMaximum(300*max(histData.GetMaximum(), histGJets_noSmear.GetMaximum(), histQCD_noSmear.GetMaximum(), histSig_noSmear.GetMaximum(), histSig_Ctau2_noSmear.GetMaximum(), histGJets_Smear.GetMaximum(), histQCD_Smear.GetMaximum(), histSig_Smear.GetMaximum(), histSig_Ctau2_Smear.GetMaximum())  )
	histGJets_noSmear.SetMinimum(0.1)
else:
	histGJets_noSmear.SetMaximum(1.5*max(histData.GetMaximum(), histGJets_noSmear.GetMaximum(), histQCD_noSmear.GetMaximum(), histSig_noSmear.GetMaximum(), histSig_Ctau2_noSmear.GetMaximum(), histGJets_Smear.GetMaximum(), histQCD_Smear.GetMaximum(), histSig_Smear.GetMaximum(), histSig_Ctau2_Smear.GetMaximum())  )
	histGJets_noSmear.SetMinimum(0)
	
histGJets_Smear.Draw("samehisto")
histQCD_noSmear.Draw("samehisto")
histQCD_Smear.Draw("samehisto")
histSig_noSmear.Draw("samehisto")
histSig_Smear.Draw("samehisto")
histSig_Ctau2_noSmear.Draw("samehisto")
histSig_Ctau2_Smear.Draw("samehisto")
histData.Draw("sameE")	
leg.Draw()
	
drawCMS2(myC, 13, lumi)	

myC.SaveAs(outputDir+"/stack/phoClusterTime_log_before_and_after_smear.pdf")
myC.SaveAs(outputDir+"/stack/phoClusterTime_log_before_and_after_smear.png")
myC.SaveAs(outputDir+"/stack/phoClusterTime_log_before_and_after_smear.C")


