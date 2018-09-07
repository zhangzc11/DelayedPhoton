from ROOT import *
import os, sys
from Aux import *
from config_noBDT import fileNameData, fileNameSig, fileNameGJets, fileNameQCD, cut_noDisc, splots, lumi, outputDir, xsecSig, xsecGJets, xsecQCD

from config_noBDT import fractionGJets, useFraction, scaleBkg, cut_GJets, cut_loose, xbins_MET, xbins_time, timeShift
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
print "GJets tree: "
print fileNameGJets


print "NTotal before cut: "

fileData = TFile(fileNameData.replace('.root','_noreweight.root'))
treeData = fileData.Get("DelayedPhoton")
hNEventsData = fileData.Get("NEvents")
NEventsData = hNEventsData.GetBinContent(1)
print "Data: " + str(NEventsData)




treeGJets = {}
NEventsGJets = [0 for i in range(len(fileNameGJets))]

for i in range(0,len(fileNameGJets)):
	treeGJets[i] = TChain("DelayedPhoton")
	treeGJets[i].AddFile(fileNameGJets[i])
	SetOwnership( treeGJets[i], True)
	fileThis = TFile(fileNameGJets[i])
	hNEventsGJets_ = fileThis.Get("NEvents")
	#NEventsGJets_.append(hNEventsGJets_.GetBinContent(1))
	NEventsGJets[i]=hNEventsGJets_.GetBinContent(1)
	print "GJets - " + str(i) + "  " +str(hNEventsGJets_.GetBinContent(1))



print NEventsGJets

cut = "abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 "


print "\n cut = " + cut

weightedcut = "(weight*pileupWeight) * " + cut 

plot_noSmear = ["pho1ClusterTime", "phoTimeCluster_noSmear_log", "#gamma cluster time [ns]", 100,-1,1, False]
plot_Smear = ["pho1ClusterTime_SmearToData", "phoTimeCluster_Smear_log", "#gamma cluster time [ns]", 100,-1,1, False]
	
#data
histData = TH1F(plot_noSmear[1]+"_histData","",plot_noSmear[3],plot_noSmear[4],plot_noSmear[5])	
treeData.Draw(plot_noSmear[0]+">>"+plot_noSmear[1]+"_histData",cut)
histData.SetMarkerStyle( 20 )
histData.SetMarkerColor( kBlack )
histData.SetLineColor( kBlack )

	
#GJets_pt70
histGJets_pt70_Smear = TH1F(plot_Smear[1]+"_histGJets_pt70_Smear","",plot_Smear[3],plot_Smear[4],plot_Smear[5])	
histGJets_pt100_Smear = TH1F(plot_Smear[1]+"_histGJets_pt100_Smear","",plot_Smear[3],plot_Smear[4],plot_Smear[5])	
histGJets_pt150_Smear = TH1F(plot_Smear[1]+"_histGJets_pt150_Smear","",plot_Smear[3],plot_Smear[4],plot_Smear[5])	

print NEventsGJets

for i in range(0, len(treeGJets)):
	print "#GJets_pt70 - "+str(i)+" - before/after cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut+" && pho1Pt>70"))
	normGJets_pt70 = NEventsGJets[i] 
	histThis = TH1F(plot_Smear[1]+"_histGJets_pt70_Smear"+str(i),"",plot_Smear[3],plot_Smear[4],plot_Smear[5])	
	treeGJets[i].Draw(plot_Smear[0]+"+"+str(timeShift)+">>"+plot_Smear[1]+"_histGJets_pt70_Smear"+str(i),weightedcut+" && pho1Pt>70")
	if histThis.Integral()>10:
		histThis.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets_pt70))
	histGJets_pt70_Smear.Add(histThis)
	print "#GJets_pt70 - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())

	print "#GJets_pt100 - "+str(i)+" - before/after cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut+" && pho1Pt>100"))
	normGJets_pt100 = NEventsGJets[i] 
	histThis = TH1F(plot_Smear[1]+"_histGJets_pt100_Smear"+str(i),"",plot_Smear[3],plot_Smear[4],plot_Smear[5])	
	treeGJets[i].Draw(plot_Smear[0]+"+"+str(timeShift)+">>"+plot_Smear[1]+"_histGJets_pt100_Smear"+str(i),weightedcut+" && pho1Pt>100")
	if histThis.Integral()>10:
		histThis.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets_pt100))
	histGJets_pt100_Smear.Add(histThis)
	print "#GJets_pt100 - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())

	print "#GJets_pt150 - "+str(i)+" - before/after cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut+" && pho1Pt>150"))
	normGJets_pt150 = NEventsGJets[i] 
	histThis = TH1F(plot_Smear[1]+"_histGJets_pt150_Smear"+str(i),"",plot_Smear[3],plot_Smear[4],plot_Smear[5])	
	treeGJets[i].Draw(plot_Smear[0]+"+"+str(timeShift)+">>"+plot_Smear[1]+"_histGJets_pt150_Smear"+str(i),weightedcut+" && pho1Pt>150")
	if histThis.Integral()>10:
		histThis.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets_pt150))
	histGJets_pt150_Smear.Add(histThis)
	print "#GJets_pt150 - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())


histGJets_pt70_Smear.Scale(histData.Integral()/histGJets_pt70_Smear.Integral())
histGJets_pt70_Smear.SetLineColor(kAzure + 7)
histGJets_pt70_Smear.SetLineWidth( 2 )
#histGJets_pt70_Smear.SetLineStyle( 7 )


histGJets_pt100_Smear.Scale(histData.Integral()/histGJets_pt100_Smear.Integral())
histGJets_pt100_Smear.SetLineColor(kViolet + 7)
histGJets_pt100_Smear.SetLineWidth( 2 )
#histGJets_pt100_Smear.SetLineStyle( 7 )

histGJets_pt150_Smear.Scale(histData.Integral()/histGJets_pt150_Smear.Integral())
histGJets_pt150_Smear.SetLineColor(kPink + 7)
histGJets_pt150_Smear.SetLineWidth( 2 )
#histGJets_pt150_Smear.SetLineStyle( 7 )



leg = TLegend(0.12, 0.55, 0.5, 0.89)
#leg.SetNColumns(2)
leg.SetBorderSize(0)
leg.SetTextSize(0.03)
leg.SetLineColor(1)
leg.SetLineStyle(1)
leg.SetLineWidth(1)
leg.SetFillColor(0)
leg.SetFillStyle(1001)
#leg.AddEntry(histData, "data","lep")
leg.AddEntry(histGJets_pt70_Smear, "#gamma + jets (MC) - p_{T}^{#gamma}>70")
leg.AddEntry(histGJets_pt100_Smear, "#gamma + jets (MC) - p_{T}^{#gamma}>100")
leg.AddEntry(histGJets_pt150_Smear, "#gamma + jets (MC) - p_{T}^{#gamma}>150")

	
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
myC.SetLogy(plot_Smear[6])
	
histGJets_pt70_Smear.SetTitle("")
histGJets_pt70_Smear.Draw()
histGJets_pt70_Smear.GetXaxis().SetTitleSize( axisTitleSize )
histGJets_pt70_Smear.GetXaxis().SetTitleOffset( axisTitleOffset )
histGJets_pt70_Smear.GetYaxis().SetTitleSize( axisTitleSize )
histGJets_pt70_Smear.GetYaxis().SetTitleOffset( axisTitleOffset )
histGJets_pt70_Smear.GetYaxis().SetTitle("events")
histGJets_pt70_Smear.GetXaxis().SetTitle(plot_Smear[2])

if plot_Smear[6]:
	histGJets_pt70_Smear.SetMinimum(0.1)
else:
	histGJets_pt70_Smear.SetMinimum(0)

histGJets_pt100_Smear.Draw("samehisto")	
histGJets_pt150_Smear.Draw("samehisto")	
#histData.Draw("sameE")	
leg.Draw()
	
drawCMS2(myC, 13, lumi)	

myC.SaveAs(outputDir+"/stack/phoClusterTime_log_before_and_after_smear_IDcut_pt.pdf")
myC.SaveAs(outputDir+"/stack/phoClusterTime_log_before_and_after_smear_IDcut_pt.png")
myC.SaveAs(outputDir+"/stack/phoClusterTime_log_before_and_after_smear_IDcut_pt.C")


