from ROOT import *
import os, sys
from Aux import *
from config import *


gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p ../data")
#os.system("mkdir -p ../data")
#################shape settings###########################
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
NEventsGJets = []
treeQCD = {}
NEventsQCD = []

for i in range(0,len(fileNameGJets)):
	treeGJets[i] = TChain("DelayedPhoton")
	treeGJets[i].AddFile(fileNameGJets[i])
	SetOwnership( treeGJets[i], True)
	fileThis = TFile(fileNameGJets[i])
	hNEventsGJets = fileThis.Get("NEvents")
	NEventsGJets.append(hNEventsGJets.GetBinContent(1))
	print "GJets - " + str(i) + str(hNEventsGJets.GetBinContent(1))

for i in range(0,len(fileNameQCD)):
	treeQCD[i] = TChain("DelayedPhoton")
	treeQCD[i].AddFile(fileNameQCD[i])
	SetOwnership( treeQCD[i], True)
	fileThis = TFile(fileNameQCD[i])
	hNEventsQCD = fileThis.Get("NEvents")
	NEventsQCD.append(hNEventsQCD.GetBinContent(1))
	print "QCD - " + str(i) + str(hNEventsQCD.GetBinContent(1))


print "\n cut_QCD_shape = " + cut_QCD_shape
print "\n cut_GJets_shape = " + cut_GJets_shape

weightedcut_QCD_shape = "(weight) * " + cut_QCD_shape 
weightedcut_GJets_shape = "(weight) * " + cut_GJets_shape 

fileOut = TFile("../data/shapes.root","RECREATE")
fileOut.cd()

for shape in shapes:
	print "\n shapeting stack shapes for " + shape[1]


	#data
        print "#data before/after cut: " + str(treeData.GetEntries()) + " => " + str(treeData.GetEntries(cut))
        histData = TH1F(shape[1]+"_histData","",shape[3],shape[4],shape[5])
        treeData.Draw(shape[0]+">>"+shape[1]+"_histData",cut)
        treeData.Draw(shape[0]+">>"+shape[1]+"_histDataOOT",cut+" && !pho1isStandardPhoton")
        histData.SetMarkerStyle( 20 )
        histData.SetMarkerColor( kBlack )
        histData.SetLineColor( kBlack )
        histData.SetLineWidth( 2 )
	histData.GetXaxis().SetTitle(shape[2])
	histData.GetYaxis().SetTitle("Events")
	histData.Write()	
	
	
	#QCD
	histQCD = TH1F(shape[1]+"_histQCD","",shape[3],shape[4],shape[5])	
	for i in range(0, len(treeQCD)):
		print "#QCD - "+str(i)+" - before/after cut: " + str(treeQCD[i].GetEntries()) + " => " + str(treeQCD[i].GetEntries(weightedcut_QCD_shape))
		normQCD = NEventsQCD[i] * 1.0  
		histThis = TH1F(shape[1]+"_histQCD"+str(i),"",shape[3],shape[4],shape[5])	
		treeQCD[i].Draw(shape[0]+">>"+shape[1]+"_histQCD"+str(i),weightedcut_QCD_shape)
		#if histThis.Integral()>100:
		#	histThis.Scale(lumi*scaleBkg*xsecQCD[i]/(normQCD))
		histQCD.Add(histThis)
		print "#QCD - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())
		histThis.Write()
	#histQCD.SetFillColor(kOrange - 9)
	histQCD.SetLineColor(kOrange - 9)
	#histQCD.Scale((1.0*histData.Integral())/histQCD.Integral())
        histQCD.SetLineWidth( 2 )
	histQCD.Write()
	print "#QCD - all: xsec * lumi * cut " + str(histQCD.Integral())
	
	#GJets
	histGJets = TH1F(shape[1]+"_histGJets","",shape[3],shape[4],shape[5])	
	for i in range(0, len(treeGJets)):
		print "#GJets - "+str(i)+" - before/after cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut_GJets_shape))
		normGJets = NEventsGJets[i] * 1.0  
		histThis = TH1F(shape[1]+"_histGJets"+str(i),"",shape[3],shape[4],shape[5])	
		treeGJets[i].Draw(shape[0]+">>"+shape[1]+"_histGJets"+str(i),weightedcut_GJets_shape)
		#if histThis.Integral()>100:
		#	histThis.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets))
		histGJets.Add(histThis)
		print "#GJets - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())
		histThis.Write()
	#histGJets.SetFillColor(kAzure + 7)
	histGJets.SetLineColor(kAzure + 7)
	#histGJets.Scale((1.0*histData.Integral())/histGJets.Integral())
        histGJets.SetLineWidth( 2 )
	histGJets.Write()
	print "#GJets - all: xsec * lumi * cut " + str(histGJets.Integral())

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
	
	myC.SetLogy()
	
	histData.Draw("E")
	histData.GetYaxis().SetRangeUser(0.1, 200.0*max(histData.GetMaximum(),histGJets.GetMaximum(), histQCD.GetMaximum()))
	histGJets.Draw("same")
	histQCD.Draw("same")
	
	leg = TLegend(0.18, 0.7, 0.93, 0.89)
        leg.SetNColumns(3)
        leg.SetBorderSize(0)
        leg.SetTextSize(0.03)
        leg.SetLineColor(1)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        leg.SetFillColor(0)
        leg.SetFillStyle(1001)
        leg.AddEntry(histData, "data","lep")
        leg.AddEntry(histGJets, "#gamma+jets","l")
        leg.AddEntry(histQCD, "QCD","l")

	leg.Draw()	
	drawCMS2(myC, 13, lumi)

	myC.SaveAs(outputDir+"/shapes_"+shape[1]+".pdf")
        myC.SaveAs(outputDir+"/shapes_"+shape[1]+".png")
        myC.SaveAs(outputDir+"/shapes_"+shape[1]+".C")
	
