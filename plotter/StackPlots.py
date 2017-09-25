from ROOT import *
import os, sys
from Aux import *

sys.path.insert(0, '../')
from config import *


gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir)
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



fileData = TFile(fileNameData)
treeData = fileData.Get("DelayedPhoton")

fileSig = TFile(fileNameSig)
treeSig = fileSig.Get("DelayedPhoton")

treeGJets = {}
treeQCD = {}


for i in range(0,len(fileNameGJets)):
	treeGJets[i] = TChain("DelayedPhoton")
	treeGJets[i].AddFile(fileNameGJets[i])
	SetOwnership( treeGJets[i], True)

for i in range(0,len(fileNameQCD)):
	treeQCD[i] = TChain("DelayedPhoton")
	treeQCD[i].AddFile(fileNameQCD[i])
	SetOwnership( treeQCD[i], True)

print "\n cut = " + cut

weightedcut = "(weight) * " + cut 

for plot in plots:
	print "\n plotting stack plots for " + plot[1]
	thisStack = THStack(plot[1]+"_stack",plot[1]+"_stack")
	#data
	print "#data before/after cut: " + str(treeData.GetEntries()) + " => " + str(treeData.GetEntries(cut))
	histData = TH1F(plot[1]+"_histData","",plot[3],plot[4],plot[5])	
	treeData.Draw(plot[0]+">>"+plot[1]+"_histData",cut)
	histData.SetMarkerStyle( 20 )
	histData.SetMarkerColor( kBlack )
	histData.SetLineColor( kBlack )

	histMC = TH1F(plot[1]+"_histMC","",plot[3],plot[4],plot[5])

	#sig
	print "#signal before/after cut: " + str(treeSig.GetEntries()) + " => " + str(treeSig.GetEntries(cut))
	print "#signal xsec * lumi  " + str(xsecSig*lumi) 
	normSig = treeSig.GetEntries("weight")
	histSig = TH1F(plot[1]+"_histSig","",plot[3],plot[4],plot[5])	
	treeSig.Draw(plot[0]+">>"+plot[1]+"_histSig",weightedcut)
	histSig.Scale(lumi*xsecSig/normSig)
	histSig.SetLineWidth( 2 )
	histSig.SetLineColor( kRed )

	#QCD
	histQCD = TH1F(plot[1]+"_histQCD","",plot[3],plot[4],plot[5])	
	for i in range(0, len(treeQCD)):
		print "#QCD - "+str(i)+" - before/after cut: " + str(treeQCD[i].GetEntries()) + " => " + str(treeQCD[i].GetEntries(weightedcut))
		print "#QCD - "+str(i)+" xsec*lumi  " + str(lumi*xsecQCD[i])

		normQCD = treeQCD[i].GetEntries("weight")	
		histThis = TH1F(plot[1]+"_histQCD"+str(i),"",plot[3],plot[4],plot[5])	
		treeQCD[i].Draw(plot[0]+">>"+plot[1]+"_histQCD"+str(i),weightedcut)
		if histThis.Integral()>0:
			histThis.Scale(lumi*xsecQCD[i]/(normQCD))
		histQCD.Add(histThis)
	histQCD.SetFillColor(kOrange - 9)
	histQCD.SetLineColor(kOrange - 9)
	

	#GJets
	histGJets = TH1F(plot[1]+"_histGJets","",plot[3],plot[4],plot[5])	
	for i in range(0, len(treeGJets)):
		print "#GJets - "+str(i)+" - before/after cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut))
		print "#GJets - "+str(i)+" xsec*lumi  " + str(lumi*xsecGJets[i])
	
		normGJets = treeGJets[i].GetEntries("weight")	
		histThis = TH1F(plot[1]+"_histGJets"+str(i),"",plot[3],plot[4],plot[5])	
		treeGJets[i].Draw(plot[0]+">>"+plot[1]+"_histGJets"+str(i),weightedcut)
		if histThis.Integral()>0:
			histThis.Scale(lumi*xsecGJets[i]/(normGJets))
		histGJets.Add(histThis)
	histGJets.SetFillColor(kAzure + 7)
	histGJets.SetLineColor(kAzure + 7)

	thisStack.Add(histGJets, "histo")
	thisStack.Add(histQCD,"histo")
	
	#histMC.Add(histSig)
	histMC.Add(histGJets)
	histMC.Add(histQCD)

	leg = TLegend(0.4, 0.7, 0.93, 0.89)
	leg.SetNColumns(2)
	leg.SetBorderSize(0)
	leg.SetTextSize(0.03)
	leg.SetLineColor(1)
	leg.SetLineStyle(1)
	leg.SetLineWidth(1)
	leg.SetFillColor(0)
	leg.SetFillStyle(1001)
	leg.AddEntry(histData, "data","lep")
	leg.AddEntry(histSig, sigLegend)
	leg.AddEntry(histGJets, "#gamma + jets (MC)", "f")
	leg.AddEntry(histQCD, "QCD (MC)", "f")


	print "#MC all - xsec*lumi  " + str(histMC.Integral())
		
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
	pad1.SetLogy(1)
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
	thisStack.SetTitle("")
	thisStack.Draw()
	thisStack.GetXaxis().SetTitleSize( axisTitleSize )
  	thisStack.GetXaxis().SetTitleOffset( axisTitleOffset )
  	thisStack.GetYaxis().SetTitleSize( axisTitleSize )
  	thisStack.GetYaxis().SetTitleOffset( axisTitleOffset )
	thisStack.GetYaxis().SetTitle("events")
	thisStack.SetMaximum(50*thisStack.GetMaximum() )
	thisStack.SetMinimum(0.001)
	pad1.Update()
	histSig.Draw("samehisto")
	histData.Draw("sameE")	
	leg.Draw()
		
	pad2.cd()
	ratio = TH1F(plot[1]+"_histRatio","",plot[3],plot[4],plot[5])
	ratio.Add(histData)
	ratio.Divide(histMC)
	ratio.SetMarkerStyle( 20 )
	ratio.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
	ratio.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
	ratio.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
	ratio.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
	ratio.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
	ratio.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
	ratio.SetMarkerColor( kBlue )
	ratio.SetLineColor( kBlue )
	ratio.GetYaxis().SetRangeUser( 0.0, 2.0 )
	ratio.SetTitle("")
	ratio.GetYaxis().SetTitle("data / mc")
	ratio.GetYaxis().CenterTitle( True )
	ratio.GetYaxis().SetNdivisions( 5, False )
	ratio.SetStats( 0 )
	ratio.Draw("E")
	ratio.GetXaxis().SetTitle(plot[2])
	pad1.Update()
	pad2.Update()

	drawCMS(myC, 13, lumi)	

	myC.SaveAs(outputDir+plot[1]+".pdf")
	myC.SaveAs(outputDir+plot[1]+".png")
	myC.SaveAs(outputDir+plot[1]+".C")
