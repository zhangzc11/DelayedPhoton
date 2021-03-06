#!/usr/bin/env
from ROOT import TFile, TH1F, TLegend, TCanvas, TPad, gROOT, gStyle, TChain, TColor
import ROOT
import os #, sys
from Aux import drawCMS
from config_noBDT import fileNameData, fileNameSig, fileNameGJets, fileNameQCD, cut, cut, splots, lumi, outputDir, xsecGJets, xsecQCD
from config_noBDT import fractionGJets, fractionQCD, useFraction, scaleBkg, cut_GJets, cut_loose, cut_GJets_shape, cut_QCD_shape, weight_cut
#import numpy as np
#import array

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/contamination")
os.system("cp config_noBDT.py "+outputDir)
os.system("cp containmination.py "+outputDir)
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

treeGJets = {}
NEventsGJets = [0 for i in range(len(fileNameGJets))]
treeQCD = {}
NEventsQCD = [0 for i in range(len(fileNameQCD))]

for i in range(0,len(fileNameGJets)):
	treeGJets[i] = TChain("DelayedPhoton")
	treeGJets[i].AddFile(fileNameGJets[i])
	ROOT.SetOwnership( treeGJets[i], True)
	fileThis = TFile(fileNameGJets[i])
	hNEventsGJets_ = fileThis.Get("NEvents")
	#NEventsGJets_.append(hNEventsGJets_.GetBinContent(1))
	NEventsGJets[i]=hNEventsGJets_.GetBinContent(1)
	print "GJets - " + str(i) + "  " +str(hNEventsGJets_.GetBinContent(1))

for i in range(0,len(fileNameQCD)):
	treeQCD[i] = TChain("DelayedPhoton")
	treeQCD[i].AddFile(fileNameQCD[i])
	ROOT.SetOwnership( treeQCD[i], True)
	fileThis = TFile(fileNameQCD[i])
	hNEventsQCD_ = fileThis.Get("NEvents")
	#NEventsQCD_.append(hNEventsQCD_.GetBinContent(1))
	NEventsQCD[i]=hNEventsQCD_.GetBinContent(1)
	print "QCD - " + str(i) + "  "+ str(hNEventsQCD_.GetBinContent(1))


print NEventsGJets
print NEventsQCD

print "\n cut = " + cut

weightedcut =  weight_cut + cut 
weightedcut_GJets_pure =  weight_cut + cut_GJets_shape 
#weightedcut_GJets_inGJets =  weight_cut + cut_GJets_shape + "&& " +cut_GJets 
weightedcut_GJets_inGJets =  weight_cut + cut_GJets 
#weightedcut_QCD_inGJets =  weight_cut + cut_loose + " && !( " + cut +")" + "&& " +cut_GJets_shape 
weightedcut_QCD_inGJets =  weight_cut + cut_loose + " && !( " + cut +")"
weightedcut_QCD_pure =  weight_cut + cut_QCD_shape 
#weightedcut_GJets_inQCD =  weight_cut + cut_QCD_shape + "&& " +cut_GJets 
weightedcut_GJets_inQCD =  weight_cut + cut_GJets 
#weightedcut_QCD_inQCD =  weight_cut + cut_loose + " && !( " + cut +")" + "&& " + cut_QCD_shape
weightedcut_QCD_inQCD =  weight_cut + cut_loose + " && !( " + cut +")"


#fileOut = TFile("../data/shapes.root","RECREATE")
#fileOut.cd()

NEventsGJets_ = NEventsGJets[:]
NEventsQCD_ = NEventsQCD[:]
splots_this = []
splots_this.append(["t1MET", "MET_linear", "#slash{E}_{T} [GeV]", 100,0,800, False])
splots_this.append(["t1MET", "MET_log", "#slash{E}_{T} [GeV]", 100,0,800, True])

splots_this.append(["pho1ClusterTime", "phoTimeCluster_noSmear_linear", "#gamma cluster time [ns]", 100,-15,15, False])
splots_this.append(["pho1ClusterTime", "phoTimeCluster_noSmear_log", "#gamma cluster time [ns]", 100,-15,15, True])
splots_this.append(["pho1ClusterTime_SmearToData", "phoTimeCluster_linear", "#gamma cluster time [ns]", 100,-15,15, False])
splots_this.append(["pho1ClusterTime_SmearToData", "phoTimeCluster_log", "#gamma cluster time [ns]", 100,-15,15, True])

for plot in splots_this:
	#print NEventsGJets
	#print NEventsQCD
	#NEventsGJets_ = NEventsGJets[:]
	#NEventsQCD_ = NEventsQCD[:]
		
	print "\n plotting stack plots for " + plot[1]

	#QCD and GJets control events in QCD sample
	histQCD_inQCD = TH1F(plot[1]+"_histQCD_inQCD","",plot[3],plot[4],plot[5])	
	histGJets_inQCD = TH1F(plot[1]+"_histGJets_inQCD","",plot[3],plot[4],plot[5])	
	for i in range(0, len(treeQCD)):
		print "#QCD - "+str(i)+" - before/after QCD/GJets cut: " + str(treeQCD[i].GetEntries()) + " => " + str(treeQCD[i].GetEntries(weightedcut_QCD_pure)) + " / "+str(treeQCD[i].GetEntries(weightedcut_GJets_pure))
		normQCD = NEventsQCD_[i] 
		histThis_QCD = TH1F(plot[1]+"_histQCD_inQCD"+str(i),"",plot[3],plot[4],plot[5])	
		histThis_GJets = TH1F(plot[1]+"_histGJets_inQCD"+str(i),"",plot[3],plot[4],plot[5])	
		treeQCD[i].Draw(plot[0]+">>"+plot[1]+"_histQCD_inQCD"+str(i),weightedcut_QCD_inQCD )
		treeQCD[i].Draw(plot[0]+">>"+plot[1]+"_histGJets_inQCD"+str(i),weightedcut_GJets_inQCD)

		if histThis_GJets.Integral()>0:
			histThis_GJets.Scale(lumi*scaleBkg*xsecQCD[i]/(normQCD))
		if histThis_QCD.Integral()>0:
			histThis_QCD.Scale(lumi*scaleBkg*xsecQCD[i]/(normQCD))
		histQCD_inQCD.Add(histThis_QCD)
		histGJets_inQCD.Add(histThis_GJets)
		print "#QCD in QCD - "+str(i)+" xsec * lumi * cut " + str(histThis_QCD.Integral())
		print "#GJets in QCD - "+str(i)+" xsec * lumi * cut " + str(histThis_GJets.Integral())
	histQCD_inQCD.SetLineColor(800 - 9)
	histGJets_inQCD.SetLineColor(860 + 7)
	histQCD_inQCD.SetLineWidth(2)
	histGJets_inQCD.SetLineWidth(2)

	#GJets and QCD control events in GJets sample
	histGJets_inGJets = TH1F(plot[1]+"_histGJets_inGJets","",plot[3],plot[4],plot[5])	
	histQCD_inGJets = TH1F(plot[1]+"_histQCD_inGJets","",plot[3],plot[4],plot[5])	
	for i in range(0, len(treeGJets)):
		print "#GJets - "+str(i)+" - before/after GJets/QCD cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut_GJets_pure)) + " / "+str(treeGJets[i].GetEntries(weightedcut_QCD_pure))
		normGJets = NEventsGJets_[i] 
		histThis_GJets = TH1F(plot[1]+"_histGJets_inGJets"+str(i),"",plot[3],plot[4],plot[5])	
		histThis_QCD = TH1F(plot[1]+"_histQCD_inGJets"+str(i),"",plot[3],plot[4],plot[5])	
		treeGJets[i].Draw(plot[0]+">>"+plot[1]+"_histGJets_inGJets"+str(i),weightedcut_GJets_inGJets)
		treeGJets[i].Draw(plot[0]+">>"+plot[1]+"_histQCD_inGJets"+str(i),weightedcut_QCD_inGJets)
		if histThis_QCD.Integral()>0:
			histThis_QCD.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets))
		if histThis_GJets.Integral()>0:
			histThis_GJets.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets))
		histGJets_inGJets.Add(histThis_GJets)
		histQCD_inGJets.Add(histThis_QCD)
		print "#GJets in GJets - "+str(i)+" xsec * lumi * cut " + str(histThis_GJets.Integral())
		print "#QCD in GJets - "+str(i)+" xsec * lumi * cut " + str(histThis_QCD.Integral())
	histQCD_inGJets.SetLineColor(800 - 9)
	histGJets_inGJets.SetLineColor(860 + 7)
	histQCD_inGJets.SetLineWidth(2)
	histGJets_inGJets.SetLineWidth(2)

	leg_inGJets = TLegend(0.18, 0.7, 0.93, 0.89)
	leg_inGJets.SetBorderSize(0)
	leg_inGJets.SetTextSize(0.03)
	leg_inGJets.SetLineColor(1)
	leg_inGJets.SetLineStyle(1)
	leg_inGJets.SetLineWidth(1)
	leg_inGJets.SetFillColor(0)
	leg_inGJets.SetFillStyle(1001)
	leg_inGJets.AddEntry(histGJets_inGJets, "#gamma + jets events in #gamma + jets sample", "l")
	leg_inGJets.AddEntry(histQCD_inGJets, "QCD control events in #gamma + jets sample", "l")

	leg_inQCD = TLegend(0.18, 0.7, 0.93, 0.89)
	leg_inQCD.SetBorderSize(0)
	leg_inQCD.SetTextSize(0.03)
	leg_inQCD.SetLineColor(1)
	leg_inQCD.SetLineStyle(1)
	leg_inQCD.SetLineWidth(1)
	leg_inQCD.SetFillColor(0)
	leg_inQCD.SetFillStyle(1001)
	leg_inQCD.AddEntry(histGJets_inQCD, "#gamma + jets control events in QCD sample", "l")
	leg_inQCD.AddEntry(histQCD_inQCD, "QCD events in QCD sample", "l")


	print "#GJets all in GJets sample - xsec * lumi * cut " + str(histGJets_inGJets.Integral())
	print "#QCD all in GJets sample - xsec * lumi * cut " + str(histQCD_inGJets.Integral())
	print "#QCD all in QCD sample - xsec * lumi * cut " + str(histQCD_inQCD.Integral())
	print "#GJets all in QCD sample - xsec * lumi * cut " + str(histGJets_inQCD.Integral())
	
	
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

	pad1 = TPad("pad1","pad1", 0.05, 0.3,0.95, 0.97)
	pad1.SetBottomMargin(0)
	pad1.SetRightMargin( rightMargin )
	pad1.SetLeftMargin( leftMargin )
	pad1.SetLogy(plot[6])
	pad1.Draw()

	pad2 = TPad("pad2","pad2", 0.05, 0.02, 0.95, 0.29)
	pad2.SetTopMargin(0.04)
	pad2.SetTopMargin(0.008)
	pad2.SetBottomMargin(0.4)
	pad2.SetRightMargin( rightMargin )
	pad2.SetLeftMargin( leftMargin )
	pad2.SetGridy()
	pad2.Draw()
	
		
	pad1.cd()
	histGJets_inGJets.SetTitle("")
	histGJets_inGJets.Draw()
	histGJets_inGJets.GetXaxis().SetTitleSize( axisTitleSize )
  	histGJets_inGJets.GetXaxis().SetTitleOffset( axisTitleOffset )
  	histGJets_inGJets.GetYaxis().SetTitleSize( axisTitleSize )
  	histGJets_inGJets.GetYaxis().SetTitleOffset( axisTitleOffset )
	histGJets_inGJets.GetYaxis().SetTitle("events")
	if plot[6]:
		histGJets_inGJets.SetMaximum(200*max(histGJets_inGJets.GetMaximum(), histQCD_inGJets.GetMaximum())  )
		histGJets_inGJets.SetMinimum(0.1)
	else:
		histGJets_inGJets.SetMaximum(1.5*max(histGJets_inGJets.GetMaximum(), histQCD_inGJets.GetMaximum())  )
		histGJets_inGJets.SetMinimum(0)
		
	pad1.Update()
	histQCD_inGJets.Draw("same")
	leg_inGJets.Draw()
		
	pad2.cd()
	ratio_inGJets = TH1F(plot[1]+"_histRatio_inGJets","",plot[3],plot[4],plot[5])

	ratio_inGJets.Add(histQCD_inGJets)
	ratio_inGJets.Divide(histGJets_inGJets)
	ratio_inGJets.SetMarkerStyle( 20 )
	ratio_inGJets.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
	ratio_inGJets.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
	ratio_inGJets.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
	ratio_inGJets.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
	ratio_inGJets.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
	ratio_inGJets.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
	ratio_inGJets.SetMarkerColor( 4 )
	ratio_inGJets.SetLineColor( 4 )
	ratio_inGJets.GetYaxis().SetRangeUser( 0.0, 1.0 )
	ratio_inGJets.SetTitle("")
	ratio_inGJets.GetYaxis().SetTitle("QCD / GJets")
	ratio_inGJets.GetYaxis().CenterTitle( True )
	ratio_inGJets.GetYaxis().SetNdivisions( 5, False )
	ratio_inGJets.SetStats( 0 )
	ratio_inGJets.Draw("E")
	ratio_inGJets.GetXaxis().SetTitle(plot[2])
	pad1.Update()
	pad2.Update()

	drawCMS(myC, 13, lumi)	

	myC.SaveAs(outputDir+"/contamination/"+plot[1]+"_contaimination_inGJets.pdf")
	myC.SaveAs(outputDir+"/contamination/"+plot[1]+"_contaimination_inGJets.png")
	myC.SaveAs(outputDir+"/contamination/"+plot[1]+"_contaimination_inGJets.C")

	pad1.SetLogy(plot[6])
	pad1.Draw()

	pad2.SetGridy()
	pad2.Draw()
		
	pad1.cd()
	
	histQCD_inQCD.SetTitle("")
	histQCD_inQCD.Draw()
	histQCD_inQCD.GetXaxis().SetTitleSize( axisTitleSize )
  	histQCD_inQCD.GetXaxis().SetTitleOffset( axisTitleOffset )
  	histQCD_inQCD.GetYaxis().SetTitleSize( axisTitleSize )
  	histQCD_inQCD.GetYaxis().SetTitleOffset( axisTitleOffset )
	histQCD_inQCD.GetYaxis().SetTitle("events")
	if plot[6]:
		histQCD_inQCD.SetMaximum(200*max(histQCD_inQCD.GetMaximum(), histGJets_inQCD.GetMaximum())  )
		histQCD_inQCD.SetMinimum(0.1)
	else:
		histQCD_inQCD.SetMaximum(1.5*max(histQCD_inQCD.GetMaximum(), histGJets_inQCD.GetMaximum())  )
		histQCD_inQCD.SetMinimum(0)
		
	pad1.Update()
	histGJets_inQCD.Draw("same")
	leg_inQCD.Draw()
	
	pad2.cd()
	
	ratio_inQCD = TH1F(plot[1]+"_histRatio_inQCD","",plot[3],plot[4],plot[5])

	ratio_inQCD.Add(histGJets_inQCD)
	ratio_inQCD.Divide(histQCD_inQCD)
	ratio_inQCD.SetMarkerStyle( 20 )
	ratio_inQCD.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
	ratio_inQCD.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
	ratio_inQCD.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
	ratio_inQCD.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
	ratio_inQCD.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
	ratio_inQCD.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
	ratio_inQCD.SetMarkerColor( 4 )
	ratio_inQCD.SetLineColor( 4 )
	ratio_inQCD.GetYaxis().SetRangeUser( 0.0, 1.0 )
	ratio_inQCD.SetTitle("")
	ratio_inQCD.GetYaxis().SetTitle("GJets / QCD")
	ratio_inQCD.GetYaxis().CenterTitle( True )
	ratio_inQCD.GetYaxis().SetNdivisions( 5, False )
	ratio_inQCD.SetStats( 0 )
	ratio_inQCD.Draw("E")
	ratio_inQCD.GetXaxis().SetTitle(plot[2])

	
	pad1.Update()
	pad2.Update()

	drawCMS(myC, 13, lumi)	

	myC.SaveAs(outputDir+"/contamination/"+plot[1]+"_contaimination_inQCD.pdf")
	myC.SaveAs(outputDir+"/contamination/"+plot[1]+"_contaimination_inQCD.png")
	myC.SaveAs(outputDir+"/contamination/"+plot[1]+"_contaimination_inQCD.C")

