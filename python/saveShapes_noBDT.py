from ROOT import TFile, TH1F, TLegend, TCanvas, TPad, gROOT, gStyle, TChain, TColor
import ROOT
import os, sys
from Aux import drawCMS, drawCMS2
from config_noBDT import fileNameData, fileNameSig, fileNameGJets, fileNameQCD, cut_2J, cut_3J, cut_2J_noSigmaIetaIeta, cut_3J_noSigmaIetaIeta, splots, lumi, outputDir, xsecSig, xsecGJets, xsecQCD
from config_noBDT import scaleBkg
from config_noBDT import cut_GJets_shape_2J, cut_QCD_shape_2J, shapes
from config_noBDT import cut_GJets_shape_2J_noSigmaIetaIeta, cut_QCD_shape_2J_noSigmaIetaIeta
from config_noBDT import cut_GJets_shape_3J, cut_QCD_shape_3J
from config_noBDT import cut_GJets_shape_3J_noSigmaIetaIeta, cut_QCD_shape_3J_noSigmaIetaIeta


gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p ../data")
os.system("mkdir -p "+outputDir)
os.system("mkdir -p "+outputDir+"/shapes")
os.system("cp config_noBDT.py "+outputDir)
os.system("cp saveShapes_noBDT.py "+outputDir)
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
	ROOT.SetOwnership( treeGJets[i], True)
	fileThis = TFile(fileNameGJets[i])
	hNEventsGJets = fileThis.Get("NEvents")
	NEventsGJets.append(hNEventsGJets.GetBinContent(1))
	print "GJets - " + str(i) + str(hNEventsGJets.GetBinContent(1))

for i in range(0,len(fileNameQCD)):
	treeQCD[i] = TChain("DelayedPhoton")
	treeQCD[i].AddFile(fileNameQCD[i])
	ROOT.SetOwnership( treeQCD[i], True)
	fileThis = TFile(fileNameQCD[i])
	hNEventsQCD = fileThis.Get("NEvents")
	NEventsQCD.append(hNEventsQCD.GetBinContent(1))
	print "QCD - " + str(i) + str(hNEventsQCD.GetBinContent(1))


print "\n cut_QCD_shape_2J = " + cut_QCD_shape_2J
print "\n cut_GJets_shape_2J = " + cut_GJets_shape_2J

print "\n cut_QCD_shape_3J = " + cut_QCD_shape_3J
print "\n cut_GJets_shape_3J = " + cut_GJets_shape_3J


weightedcut_QCD_shape_2J = "(weight*pileupWeight) * " + cut_QCD_shape_2J 
weightedcut_QCD_shape_2J_noSigmaIetaIeta = "(weight*pileupWeight) * " + cut_QCD_shape_2J_noSigmaIetaIeta
weightedcut_GJets_shape_2J = "(weight*pileupWeight) * " + cut_GJets_shape_2J 
weightedcut_GJets_shape_2J_noSigmaIetaIeta = "(weight*pileupWeight) * " + cut_GJets_shape_2J_noSigmaIetaIeta
weightedcut_QCD_shape_3J = "(weight*pileupWeight) * " + cut_QCD_shape_3J 
weightedcut_QCD_shape_3J_noSigmaIetaIeta = "(weight*pileupWeight) * " + cut_QCD_shape_3J_noSigmaIetaIeta
weightedcut_GJets_shape_3J = "(weight*pileupWeight) * " + cut_GJets_shape_3J 
weightedcut_GJets_shape_3J_noSigmaIetaIeta = "(weight*pileupWeight) * " + cut_GJets_shape_3J_noSigmaIetaIeta

#print "weightedcut_QCD_shape_3J: "+weightedcut_QCD_shape_3J
#print "weightedcut_GJets_shape_3J: "+weightedcut_GJets_shape_3J


print "now working on 2J category: "
fileOut_2J = TFile("../data/shapes_2J_noBDT.root","RECREATE")
fileOut_2J.cd()

for shape in shapes:
	print "\n shapeting stack shapes for " + shape[1]
	
	#data
	if shape[0] == "pho1SigmaIetaIeta":
		print "#data before/after cut: " + str(treeData.GetEntries()) + " => " + str(treeData.GetEntries(cut_2J_noSigmaIetaIeta))
	else:
		print "#data before/after cut: " + str(treeData.GetEntries()) + " => " + str(treeData.GetEntries(cut_2J))
		
        histData = TH1F(shape[1]+"_histData","",shape[3],shape[4],shape[5])
	if shape[0] == "pho1SigmaIetaIeta":
		treeData.Draw(shape[0]+">>"+shape[1]+"_histData",cut_2J_noSigmaIetaIeta)
	else:
		treeData.Draw(shape[0]+">>"+shape[1]+"_histData",cut_2J)
        histData.SetMarkerStyle( 20 )
        histData.SetMarkerColor( ROOT.kBlack )
        histData.SetLineColor( ROOT.kBlack )
        histData.SetLineWidth( 2 )
	histData.GetXaxis().SetTitle(shape[2])
	histData.GetYaxis().SetTitle("Events")
	histData.Write()	
	
	
	#QCD
	histQCD = TH1F(shape[1]+"_histQCD","",shape[3],shape[4],shape[5])	
	for i in range(0, len(treeQCD)):
		print "#QCD - "+str(i)+" - before/after cut: " + str(treeQCD[i].GetEntries()) + " => " + str(treeQCD[i].GetEntries(weightedcut_QCD_shape_2J))
		normQCD = NEventsQCD[i] * 1.0  
		histThis = TH1F(shape[1]+"_histQCD"+str(i),"",shape[3],shape[4],shape[5])	
		if shape[0] == "pho1SigmaIetaIeta":
			treeQCD[i].Draw(shape[0]+">>"+shape[1]+"_histQCD"+str(i),weightedcut_QCD_shape_2J_noSigmaIetaIeta)
		else:
			treeQCD[i].Draw(shape[0]+">>"+shape[1]+"_histQCD"+str(i),weightedcut_QCD_shape_2J)
		if histThis.Integral()>10:
			histThis.Scale(lumi*scaleBkg*xsecQCD[i]/(normQCD))
		histQCD.Add(histThis)
		print "#QCD - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())
		histThis.Write()
	#histQCD.SetFillColor(ROOT.kOrange - 9)
	histQCD.SetLineColor(ROOT.kOrange - 9)
	#histQCD.Scale((1.0*histData.Integral())/histQCD.Integral())
        histQCD.SetLineWidth( 2 )
	histQCD.Write()
	print "#QCD - all: xsec * lumi * cut " + str(histQCD.Integral())
	
	#GJets
	histGJets = TH1F(shape[1]+"_histGJets","",shape[3],shape[4],shape[5])	
	for i in range(0, len(treeGJets)):
		print "#GJets - "+str(i)+" - before/after cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut_GJets_shape_2J))
		normGJets = NEventsGJets[i] * 1.0  
		histThis = TH1F(shape[1]+"_histGJets"+str(i),"",shape[3],shape[4],shape[5])	
		if shape[0] == "pho1SigmaIetaIeta":
			treeGJets[i].Draw(shape[0]+">>"+shape[1]+"_histGJets"+str(i),weightedcut_GJets_shape_2J_noSigmaIetaIeta)
		else:
			treeGJets[i].Draw(shape[0]+">>"+shape[1]+"_histGJets"+str(i),weightedcut_GJets_shape_2J)
		if histThis.Integral()>10:
			histThis.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets))
		histGJets.Add(histThis)
		print "#GJets - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())
		histThis.Write()
	#histGJets.SetFillColor(ROOT.kAzure + 7)
	histGJets.SetLineColor(ROOT.kAzure + 7)
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

	myC.SaveAs(outputDir+"/shapes/shapes_"+shape[1]+"_2J.pdf")
        myC.SaveAs(outputDir+"/shapes/shapes_"+shape[1]+"_2J.png")
        myC.SaveAs(outputDir+"/shapes/shapes_"+shape[1]+"_2J.C")


fileOut_3J = TFile("../data/shapes_3J_noBDT.root","RECREATE")
fileOut_3J.cd()


print "now working on 3J category: "
for shape in shapes:

	print "\n shapeting stack shapes for " + shape[1]
	
	#data
	if shape[0] == "pho1SigmaIetaIeta":
		print "#data before/after cut: " + str(treeData.GetEntries()) + " => " + str(treeData.GetEntries(cut_3J_noSigmaIetaIeta))
	else:
		print "#data before/after cut: " + str(treeData.GetEntries()) + " => " + str(treeData.GetEntries(cut_3J))
		
        histData = TH1F(shape[1]+"_histData","",shape[3],shape[4],shape[5])
	if shape[0] == "pho1SigmaIetaIeta":
		treeData.Draw(shape[0]+">>"+shape[1]+"_histData",cut_3J_noSigmaIetaIeta)
	else:
		treeData.Draw(shape[0]+">>"+shape[1]+"_histData",cut_3J)
        histData.SetMarkerStyle( 20 )
        histData.SetMarkerColor( ROOT.kBlack )
        histData.SetLineColor( ROOT.kBlack )
        histData.SetLineWidth( 2 )
	histData.GetXaxis().SetTitle(shape[2])
	histData.GetYaxis().SetTitle("Events")
	histData.Write()	
	
	
	#QCD
	histQCD = TH1F(shape[1]+"_histQCD","",shape[3],shape[4],shape[5])	
	for i in range(0, len(treeQCD)):
		print "#QCD - "+str(i)+" - before/after cut: " + str(treeQCD[i].GetEntries()) + " => " + str(treeQCD[i].GetEntries(weightedcut_QCD_shape_3J))
		normQCD = NEventsQCD[i] * 1.0  
		histThis = TH1F(shape[1]+"_histQCD"+str(i),"",shape[3],shape[4],shape[5])	
		if shape[0] == "pho1SigmaIetaIeta":
			treeQCD[i].Draw(shape[0]+">>"+shape[1]+"_histQCD"+str(i),weightedcut_QCD_shape_3J_noSigmaIetaIeta)
		else:
			treeQCD[i].Draw(shape[0]+">>"+shape[1]+"_histQCD"+str(i),weightedcut_QCD_shape_3J)
		if histThis.Integral()>10:
			histThis.Scale(lumi*scaleBkg*xsecQCD[i]/(normQCD))
		histQCD.Add(histThis)
		print "#QCD - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())
		histThis.Write()
	#histQCD.SetFillColor(ROOT.kOrange - 9)
	histQCD.SetLineColor(ROOT.kOrange - 9)
	#histQCD.Scale((1.0*histData.Integral())/histQCD.Integral())
        histQCD.SetLineWidth( 2 )
	histQCD.Write()
	print "#QCD - all: xsec * lumi * cut " + str(histQCD.Integral())
	
	#GJets
	histGJets = TH1F(shape[1]+"_histGJets","",shape[3],shape[4],shape[5])	
	for i in range(0, len(treeGJets)):
		print "#GJets - "+str(i)+" - before/after cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut_GJets_shape_3J))
		normGJets = NEventsGJets[i] * 1.0  
		histThis = TH1F(shape[1]+"_histGJets"+str(i),"",shape[3],shape[4],shape[5])	
		if shape[0] == "pho1SigmaIetaIeta":
			treeGJets[i].Draw(shape[0]+">>"+shape[1]+"_histGJets"+str(i),weightedcut_GJets_shape_3J_noSigmaIetaIeta)
		else:
			treeGJets[i].Draw(shape[0]+">>"+shape[1]+"_histGJets"+str(i),weightedcut_GJets_shape_3J)
		if histThis.Integral()>10:
			histThis.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets))
		histGJets.Add(histThis)
		print "#GJets - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())
		histThis.Write()
	#histGJets.SetFillColor(ROOT.kAzure + 7)
	histGJets.SetLineColor(ROOT.kAzure + 7)
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

	myC.SaveAs(outputDir+"/shapes/shapes_"+shape[1]+"_3J.pdf")
        myC.SaveAs(outputDir+"/shapes/shapes_"+shape[1]+"_3J.png")
        myC.SaveAs(outputDir+"/shapes/shapes_"+shape[1]+"_3J.C")
	
	
