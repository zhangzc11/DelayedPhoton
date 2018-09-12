from ROOT import *
import os, sys
from Aux import *
from config_noBDT import fileNameData, fileNameSig, fileNameGJets, fileNameQCD, cut, cut_noDisc, splots, lumi, outputDir, xsecSig, xsecGJets, xsecQCD
from config_noBDT import fractionGJets, fractionQCD, useFraction, scaleBkg, cut_GJets, cut_loose, xbins_MET, xbins_time, sigLegend, weight_cut
import numpy as np
import array

gROOT.SetBatch(True)

gStyle.SetOptStat(0)
gStyle.SetOptFit(111)

os.system("mkdir -p "+outputDir+"/stack")
os.system("mkdir -p "+outputDir+"/stack")
os.system("cp config_noBDT.py "+outputDir+"/stack")
os.system("cp GJets_vs_QCD_noBDT.py "+outputDir+"/stack")
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
	SetOwnership( treeGJets[i], True)
	fileThis = TFile(fileNameGJets[i])
	hNEventsGJets_ = fileThis.Get("NEvents")
	#NEventsGJets_.append(hNEventsGJets_.GetBinContent(1))
	NEventsGJets[i]=hNEventsGJets_.GetBinContent(1)
	print "GJets - " + str(i) + "  " +str(hNEventsGJets_.GetBinContent(1))

for i in range(0,len(fileNameQCD)):
	treeQCD[i] = TChain("DelayedPhoton")
	treeQCD[i].AddFile(fileNameQCD[i])
	SetOwnership( treeQCD[i], True)
	fileThis = TFile(fileNameQCD[i])
	hNEventsQCD_ = fileThis.Get("NEvents")
	#NEventsQCD_.append(hNEventsQCD_.GetBinContent(1))
	NEventsQCD[i]=hNEventsQCD_.GetBinContent(1)
	print "QCD - " + str(i) + "  "+ str(hNEventsQCD_.GetBinContent(1))


print NEventsGJets
print NEventsQCD

print "\n cut = " + cut

weightedcut =  weight_cut + cut 
weightedcut_noDisc =  weight_cut + cut_noDisc

#fileOut = TFile("../data/shapes.root","RECREATE")
#fileOut.cd()

#NEventsGJets_ = NEventsGJets[:]
#NEventsQCD_ = NEventsQCD[:]
for plot in splots:
	#print NEventsGJets
	#print NEventsQCD
	#NEventsGJets_ = NEventsGJets[:]
	#NEventsQCD_ = NEventsQCD[:]
		
	print "\n plotting stack plots for " + plot[1]
	#data
	print "#data before/after cut: " + str(treeData.GetEntries()) + " => " + str(treeData.GetEntries(cut))
	histData = TH1F(plot[1]+"_histData","",plot[3],plot[4],plot[5])	
	'''
	if plot[0]=="pho1ClusterTime":
		histData = TH1F(plot[1]+"_histData","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		histData = TH1F(plot[1]+"_histData","",len(xbins_MET)-1, np.array(xbins_MET))
	'''
	if plot[0]=="disc":
		treeData.Draw(plot[0]+">>"+plot[1]+"_histData",cut_noDisc)
	else:
		treeData.Draw(plot[0]+">>"+plot[1]+"_histData",cut)

	histData.SetMarkerStyle( 20 )
	histData.SetMarkerColor( kBlack )
	histData.SetLineColor( kBlack )

	#sig
	print "#signal before/after cut: " + str(treeSig.GetEntries()) + " => " + str(treeSig.GetEntries(cut))
	histSig = TH1F(plot[1]+"_histSig","",plot[3],plot[4],plot[5])	
	'''
	if plot[0]=="pho1ClusterTime":
		histSig = TH1F(plot[1]+"_histSig","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		histSig = TH1F(plot[1]+"_histSig","",len(xbins_MET)-1, np.array(xbins_MET))
	'''
	if plot[0]=="disc":
		treeSig.Draw(plot[0]+">>"+plot[1]+"_histSig",weightedcut_noDisc)
	else:
		treeSig.Draw(plot[0]+">>"+plot[1]+"_histSig",weightedcut)
	if plot[6]:
		histSig.Scale(lumi*xsecSig/NEventsSig)
	else:
		histSig.Scale(lumi*xsecSig/NEventsSig)
	histSig.SetLineWidth( 2 )
	histSig.SetLineColor( kRed )
	print "#signal xsec * lumi * cut  " + str(histSig.Integral()) 

	#QCD
	histQCD = TH1F(plot[1]+"_histQCD","",plot[3],plot[4],plot[5])	
	'''
	if plot[0]=="pho1ClusterTime":
		histQCD = TH1F(plot[1]+"_histQCD","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		histQCD = TH1F(plot[1]+"_histQCD","",len(xbins_MET)-1, np.array(xbins_MET))
	'''
	for i in range(0, len(treeQCD)):
		print "#QCD - "+str(i)+" - before/after cut: " + str(treeQCD[i].GetEntries()) + " => " + str(treeQCD[i].GetEntries(weightedcut))
		normQCD = NEventsQCD[i] 
		histThis = TH1F(plot[1]+"_histQCD"+str(i),"",plot[3],plot[4],plot[5])	
		'''
		if plot[0]=="pho1ClusterTime":
			histThis = TH1F(plot[1]+"_histQCD"+str(i),"",len(xbins_time)-1, np.array(xbins_time))
		if plot[0]=="MET":
			histThis = TH1F(plot[1]+"_histQCD"+str(i),"",len(xbins_MET)-1, np.array(xbins_MET))
		'''
		if plot[0]=="disc":
			treeQCD[i].Draw(plot[0]+">>"+plot[1]+"_histQCD"+str(i),weightedcut_noDisc)
		else:
			treeQCD[i].Draw(plot[0]+">>"+plot[1]+"_histQCD"+str(i),weightedcut)
		if histThis.Integral()>10:
			histThis.Scale(lumi*scaleBkg*xsecQCD[i]/(normQCD))
		histQCD.Add(histThis)
		print "#QCD - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())
		#histThis.Write()
	#histQCD.SetFillColor(kOrange - 9)
	histQCD.Scale(histData.Integral()/histQCD.Integral())
	histQCD.SetLineColor(kOrange - 9)
	histQCD.SetLineWidth( 2 )
	

	#GJets
	histGJets = TH1F(plot[1]+"_histGJets","",plot[3],plot[4],plot[5])	
	'''
	if plot[0]=="pho1ClusterTime":
		histGJets = TH1F(plot[1]+"_histGJets","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		histGJets = TH1F(plot[1]+"_histGJets","",len(xbins_MET)-1, np.array(xbins_MET))
	'''
	print NEventsGJets
	print NEventsQCD

	for i in range(0, len(treeGJets)):
		print "#GJets - "+str(i)+" - before/after cut: " + str(treeGJets[i].GetEntries()) + " => " + str(treeGJets[i].GetEntries(weightedcut))
		normGJets = NEventsGJets[i] 
		histThis = TH1F(plot[1]+"_histGJets"+str(i),"",plot[3],plot[4],plot[5])	
		'''
		if plot[0]=="pho1ClusterTime":
			histThis = TH1F(plot[1]+"_histGJets"+str(i),"",len(xbins_time)-1, np.array(xbins_time))
		if plot[0]=="MET":
			histThis = TH1F(plot[1]+"_histGJets"+str(i),"",len(xbins_MET)-1, np.array(xbins_MET))
		'''
		if plot[0]=="disc":
			treeGJets[i].Draw(plot[0]+">>"+plot[1]+"_histGJets"+str(i),weightedcut_noDisc)
		else:
			treeGJets[i].Draw(plot[0]+">>"+plot[1]+"_histGJets"+str(i),weightedcut)
		if histThis.Integral()>10:
			histThis.Scale(lumi*scaleBkg*xsecGJets[i]/(normGJets))
		histGJets.Add(histThis)
		print "#GJets - "+str(i)+" xsec * lumi * cut " + str(histThis.Integral())
		#histThis.Write()
	#histGJets.SetFillColor(kAzure + 7)
	histGJets.Scale(histData.Integral()/histGJets.Integral())
	histGJets.SetLineColor(kAzure + 7)
	histGJets.SetLineWidth( 2 )

		
	#GJets, data-driven
	histGJets_CR = TH1F(plot[1]+"_histGJets_CR","",plot[3],plot[4],plot[5])	
	'''
	if plot[0]=="pho1ClusterTime":
		histGJets_CR = TH1F(plot[1]+"_histGJets_CR","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		histGJets_CR = TH1F(plot[1]+"_histGJets_CR","",len(xbins_MET)-1, np.array(xbins_MET))
	'''
	treeData.Draw(plot[0]+">>"+plot[1]+"_histGJets_CR",cut_GJets)
	if useFraction:
		#histGJets_CR.Scale(histData.Integral()*fractionGJets/histGJets_CR.Integral())
		histGJets_CR.Scale(histData.Integral()*0.5498/histGJets_CR.Integral())
	else:
		histGJets_CR.Scale(histGJets.Integral()/histGJets_CR.Integral())
	#histGJets_CR.SetFillColor(kAzure + 7)
	histGJets_CR.Scale(histData.Integral()/histGJets_CR.Integral())
	histGJets_CR.SetLineColor(kAzure + 7)
	histGJets_CR.SetLineWidth( 2 )
		
	#GJets, data-driven, after reweighting
	histGJets_CR_reweight = TH1F(plot[1]+"_histGJets_CR_reweight","",plot[3],plot[4],plot[5])	
	'''
	if plot[0]=="pho1ClusterTime":
		histGJets_CR_reweight = TH1F(plot[1]+"_histGJets_CR_reweight","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		histGJets_CR_reweight = TH1F(plot[1]+"_histGJets_CR_reweight","",len(xbins_MET)-1, np.array(xbins_MET))
	'''
	treeData.Draw(plot[0]+">>"+plot[1]+"_histGJets_CR_reweight","weight_sumET*("+cut_GJets+")")
	if useFraction:
		#histGJets_CR_reweight.Scale(histData.Integral()*fractionGJets/histGJets_CR_reweight.Integral())
		histGJets_CR_reweight.Scale(histData.Integral()*0.5498/histGJets_CR_reweight.Integral())
	else:
		histGJets_CR_reweight.Scale(histGJets.Integral()/histGJets_CR_reweight.Integral())
	#histGJets_CR_reweight.SetFillColor(kAzure + 7)
	histGJets_CR_reweight.Scale(histData.Integral()/histGJets_CR_reweight.Integral())
	histGJets_CR_reweight.SetLineColor(kAzure + 7)
	histGJets_CR_reweight.SetLineWidth( 2 )
		
	#QCD, data-driven
	histQCD_CR = TH1F(plot[1]+"_histQCD_CR","",plot[3],plot[4],plot[5])	
	'''
	if plot[0]=="pho1ClusterTime":
		histQCD_CR = TH1F(plot[1]+"_histQCD_CR","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		histQCD_CR = TH1F(plot[1]+"_histQCD_CR","",len(xbins_MET)-1, np.array(xbins_MET))
	'''

	treeData.Draw(plot[0]+">>"+plot[1]+"_histQCD_CR", cut_loose + " && !( " + cut +")")
	if useFraction:
		#histQCD_CR.Scale(histData.Integral()*fractionQCD/histQCD_CR.Integral())
		histQCD_CR.Scale(histData.Integral()*0.4502/histQCD_CR.Integral())
	else:
		histQCD_CR.Scale(histQCD.Integral()/histQCD_CR.Integral())
	#histQCD_CR.SetFillColor(kOrange - 9)
	histQCD_CR.Scale(histData.Integral()/histQCD_CR.Integral())
	histQCD_CR.SetLineColor(kOrange - 9)
	histQCD_CR.SetLineWidth( 2 )
		

	#save histograms to file
	#histData.Write()
	#histGJets.Write()
	#histGJets_CR.Write()
	#histQCD.Write()
	#histQCD_CR.Write()
	

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
	if plot[6]:
		leg.AddEntry(histSig, sigLegend)
	else:
		leg.AddEntry(histSig, sigLegend)

	leg.AddEntry(histGJets, "#gamma + jets (MC)")
	leg.AddEntry(histQCD, "QCD (MC)")


	print "#GJets all - xsec * lumi * cut " + str(histGJets.Integral())
	print "#GJets all CR - xsec * lumi * cut " + str(histGJets_CR.Integral())
	print "#QCD all - xsec * lumi * cut " + str(histQCD.Integral())
	print "#QCD all CR - xsec * lumi * cut " + str(histQCD_CR.Integral())
		
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

	histGJets.SetTitle("")
	histGJets.Draw()
	histGJets.GetXaxis().SetTitleSize( axisTitleSize )
  	histGJets.GetXaxis().SetTitleOffset( axisTitleOffset )
  	histGJets.GetYaxis().SetTitleSize( axisTitleSize )
  	histGJets.GetYaxis().SetTitleOffset( axisTitleOffset )
	histGJets.GetYaxis().SetTitle("events")
	if plot[6]:
		histGJets.SetMaximum(200*max(histData.GetMaximum(), histGJets.GetMaximum(), histQCD.GetMaximum(), histSig.GetMaximum())  )
		histGJets.SetMinimum(0.1)
	else:
		histGJets.SetMaximum(1.5*max(histData.GetMaximum(), histGJets.GetMaximum(), histQCD.GetMaximum(), histSig.GetMaximum())  )
		histGJets.SetMinimum(0)
		
	pad1.Update()
	histQCD.Draw("samehisto")
	histSig.Draw("samehisto")
	histData.Draw("sameE")	
	leg.Draw()
		
	pad2.cd()
	ratio = TH1F(plot[1]+"_histRatio","",plot[3],plot[4],plot[5])
	ratio_QCD_vs_data = TH1F(plot[1]+"_histRatio_QCD_vs_data","",plot[3],plot[4],plot[5])
	'''
	if plot[0]=="pho1ClusterTime":
		ratio = TH1F(plot[1]+"_histRatio","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		ratio = TH1F(plot[1]+"_histRatio","",len(xbins_MET)-1, np.array(xbins_MET))
	'''

	ratio.Add(histGJets)
	ratio.Divide(histQCD)
	ratio.SetMarkerStyle( 20 )
	ratio.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
	ratio.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
	ratio.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
	ratio.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
	ratio.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
	ratio.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
	ratio.SetMarkerColor( kBlue )
	ratio.SetLineColor( kBlue )
	ratio.GetYaxis().SetRangeUser( 0.0, 2.5 )
	ratio.SetTitle("")
	ratio.GetYaxis().SetTitle("ratio")
	ratio.GetYaxis().CenterTitle( True )
	ratio.GetYaxis().SetNdivisions( 5, False )
	ratio.SetStats( 0 )
	ratio.Draw("E")
	ratio.GetXaxis().SetTitle(plot[2])

	ratio_QCD_vs_data.Add(histQCD)
	ratio_QCD_vs_data.Divide(histData)
	ratio_QCD_vs_data.SetMarkerStyle( 21 )
	ratio_QCD_vs_data.SetMarkerColor( kBlack )
	ratio_QCD_vs_data.SetLineColor( kBlack )
	ratio_QCD_vs_data.Draw("sameE")

	leg_ratio = TLegend(0.75,0.75,0.95,0.93)
	leg_ratio.SetBorderSize(0)
	leg_ratio.SetTextSize(0.08)
	leg_ratio.SetLineColor(1)
	leg_ratio.SetLineStyle(1)
	leg_ratio.SetLineWidth(1)
	leg_ratio.SetFillColor(0)
	leg_ratio.SetFillStyle(1001)
	leg_ratio.AddEntry(ratio,"#gamma+jets/QCD")
	leg_ratio.AddEntry(ratio_QCD_vs_data,"QCD/data")
	leg_ratio.Draw()

	pad1.Update()
	pad2.Update()


	drawCMS(myC, 13, lumi)	

	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD.pdf")
	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD.png")
	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD.C")


	#control plots with data driven QCD and GJets	
	leg_CR = TLegend(0.18, 0.7, 0.93, 0.89)
	leg_CR.SetNColumns(3)
	leg_CR.SetBorderSize(0)
	leg_CR.SetTextSize(0.03)
	leg_CR.SetLineColor(1)
	leg_CR.SetLineStyle(1)
	leg_CR.SetLineWidth(1)
	leg_CR.SetFillColor(0)
	leg_CR.SetFillStyle(1001)
	leg_CR.AddEntry(histData, "data","lep")
	if plot[6]:
		leg_CR.AddEntry(histSig, sigLegend)
	else:
		leg_CR.AddEntry(histSig, sigLegend)

	leg_CR.AddEntry(histGJets_CR, "#gamma + jets (control)")
	leg_CR.AddEntry(histQCD_CR, "QCD (control)")

	pad1.SetLogy(plot[6])
	pad1.Draw()

	pad2.SetGridy()
	pad2.Draw()
		
	pad1.cd()
	histGJets_CR.SetTitle("")
	histGJets_CR.Draw()
	histGJets_CR.GetXaxis().SetTitleSize( axisTitleSize )
  	histGJets_CR.GetXaxis().SetTitleOffset( axisTitleOffset )
  	histGJets_CR.GetYaxis().SetTitleSize( axisTitleSize )
  	histGJets_CR.GetYaxis().SetTitleOffset( axisTitleOffset )
	histGJets_CR.GetYaxis().SetTitle("events")
	if plot[6]:
		histGJets_CR.SetMaximum(200*max(histData.GetMaximum(), histGJets_CR.GetMaximum(), histQCD_CR.GetMaximum(), histSig.GetMaximum())  )
		histGJets_CR.SetMinimum(0.1)
	else:
		histGJets_CR.SetMaximum(1.5*max(histData.GetMaximum(), histGJets_CR.GetMaximum(), histQCD_CR.GetMaximum(), histSig.GetMaximum())  )
		histGJets_CR.SetMinimum(0)
		
	pad1.Update()
	histQCD_CR.Draw("samehisto")
	histSig.Draw("samehisto")
	histData.Draw("sameE")	
	leg_CR.Draw()
		
	pad2.cd()
	ratio_CR = TH1F(plot[1]+"_histRatio_CR","",plot[3],plot[4],plot[5])
	ratio_CR_QCD_vs_data = TH1F(plot[1]+"_histRatio_CR_QCD_vs_data","",plot[3],plot[4],plot[5])
	'''
	if plot[0]=="pho1ClusterTime":
		ratio_CR = TH1F(plot[1]+"_histRatio_CR","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		ratio_CR = TH1F(plot[1]+"_histRatio_CR","",len(xbins_MET)-1, np.array(xbins_MET))
	'''
	ratio_CR.Add(histGJets_CR)
	ratio_CR.Divide(histQCD_CR)
	ratio_CR.SetMarkerStyle( 20 )
	ratio_CR.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
	ratio_CR.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
	ratio_CR.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
	ratio_CR.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
	ratio_CR.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
	ratio_CR.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
	ratio_CR.SetMarkerColor( kBlue )
	ratio_CR.SetLineColor( kBlue )
	ratio_CR.GetYaxis().SetRangeUser( 0.0, 2.5 )
	ratio_CR.SetTitle("")
	ratio_CR.GetYaxis().SetTitle("ratio")
	ratio_CR.GetYaxis().CenterTitle( True )
	ratio_CR.GetYaxis().SetNdivisions( 5, False )
	ratio_CR.SetStats( 0 )
	ratio_CR.Draw("E")
	ratio_CR.GetXaxis().SetTitle(plot[2])

	ratio_CR_QCD_vs_data.Add(histQCD_CR)
	ratio_CR_QCD_vs_data.Divide(histData)
	ratio_CR_QCD_vs_data.SetMarkerStyle( 21 )
	ratio_CR_QCD_vs_data.SetMarkerColor( kBlack )
	ratio_CR_QCD_vs_data.SetLineColor( kBlack )
	ratio_CR_QCD_vs_data.Draw("sameE")

	leg_ratio_CR = TLegend(0.75,0.75,0.95,0.93)
	leg_ratio_CR.SetBorderSize(0)
	leg_ratio_CR.SetTextSize(0.08)
	leg_ratio_CR.SetLineColor(1)
	leg_ratio_CR.SetLineStyle(1)
	leg_ratio_CR.SetLineWidth(1)
	leg_ratio_CR.SetFillColor(0)
	leg_ratio_CR.SetFillStyle(1001)
	leg_ratio_CR.AddEntry(ratio_CR,"#gamma+jets/QCD")
	leg_ratio_CR.AddEntry(ratio_CR_QCD_vs_data,"QCD/data")
	leg_ratio_CR.Draw()


	pad1.Update()
	pad2.Update()

	drawCMS(myC, 13, lumi)	

	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD_dataDriven.pdf")
	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD_dataDriven.png")
	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD_dataDriven.C")


	#control plots with data driven QCD and GJets, after reweighting
	leg_CR_reweight = TLegend(0.18, 0.7, 0.93, 0.89)
	leg_CR_reweight.SetNColumns(3)
	leg_CR_reweight.SetBorderSize(0)
	leg_CR_reweight.SetTextSize(0.03)
	leg_CR_reweight.SetLineColor(1)
	leg_CR_reweight.SetLineStyle(1)
	leg_CR_reweight.SetLineWidth(1)
	leg_CR_reweight.SetFillColor(0)
	leg_CR_reweight.SetFillStyle(1001)
	leg_CR_reweight.AddEntry(histData, "data","lep")
	if plot[6]:
		leg_CR_reweight.AddEntry(histSig, sigLegend)
	else:
		leg_CR_reweight.AddEntry(histSig, sigLegend)

	leg_CR_reweight.AddEntry(histGJets_CR_reweight, "#gamma + jets (control)")
	leg_CR_reweight.AddEntry(histQCD_CR, "QCD (control)")

	pad1.SetLogy(plot[6])
	pad1.Draw()

	pad2.SetGridy()
	pad2.Draw()
		
	pad1.cd()
	histGJets_CR_reweight.SetTitle("")
	histGJets_CR_reweight.Draw("hist")
	histGJets_CR_reweight.GetXaxis().SetTitleSize( axisTitleSize )
  	histGJets_CR_reweight.GetXaxis().SetTitleOffset( axisTitleOffset )
  	histGJets_CR_reweight.GetYaxis().SetTitleSize( axisTitleSize )
  	histGJets_CR_reweight.GetYaxis().SetTitleOffset( axisTitleOffset )
	histGJets_CR_reweight.GetYaxis().SetTitle("events")
	if plot[6]:
		histGJets_CR_reweight.SetMaximum(200*max(histData.GetMaximum(), histGJets_CR_reweight.GetMaximum(), histQCD_CR.GetMaximum(), histSig.GetMaximum())  )
		histGJets_CR_reweight.SetMinimum(0.1)
	else:
		histGJets_CR_reweight.SetMaximum(1.5*max(histData.GetMaximum(), histGJets_CR_reweight.GetMaximum(), histQCD_CR.GetMaximum(), histSig.GetMaximum())  )
		histGJets_CR_reweight.SetMinimum(0)
		
	pad1.Update()
	histQCD_CR.Draw("samehisto")
	histSig.Draw("samehisto")
	histData.Draw("sameE")	
	leg_CR_reweight.Draw()
		
	pad2.cd()
	ratio_CR_reweight = TH1F(plot[1]+"_histRatio_CR_reweight","",plot[3],plot[4],plot[5])
	ratio_CR_reweight_QCD_vs_data = TH1F(plot[1]+"_histRatio_CR_reweight_QCD_vs_data","",plot[3],plot[4],plot[5])
	'''
	if plot[0]=="pho1ClusterTime":
		ratio_CR_reweight = TH1F(plot[1]+"_histRatio_CR_reweight","",len(xbins_time)-1, np.array(xbins_time))
	if plot[0]=="MET":
		ratio_CR_reweight = TH1F(plot[1]+"_histRatio_CR_reweight","",len(xbins_MET)-1, np.array(xbins_MET))
	'''
	ratio_CR_reweight.Add(histGJets_CR_reweight)
	ratio_CR_reweight.Divide(histQCD_CR)
	ratio_CR_reweight.SetMarkerStyle( 20 )
	ratio_CR_reweight.GetXaxis().SetTitleSize( axisTitleSizeRatioX )
	ratio_CR_reweight.GetXaxis().SetLabelSize( axisLabelSizeRatioX )
	ratio_CR_reweight.GetXaxis().SetTitleOffset( axisTitleOffsetRatioX )
	ratio_CR_reweight.GetYaxis().SetTitleSize( axisTitleSizeRatioY )
	ratio_CR_reweight.GetYaxis().SetLabelSize( axisLabelSizeRatioY )
	ratio_CR_reweight.GetYaxis().SetTitleOffset( axisTitleOffsetRatioY )
	ratio_CR_reweight.SetMarkerColor( kBlue )
	ratio_CR_reweight.SetLineColor( kBlue )
	ratio_CR_reweight.GetYaxis().SetRangeUser( 0.0, 2.5 )
	ratio_CR_reweight.SetTitle("")
	ratio_CR_reweight.GetYaxis().SetTitle("ratio")
	ratio_CR_reweight.GetYaxis().CenterTitle( True )
	ratio_CR_reweight.GetYaxis().SetNdivisions( 5, False )
	ratio_CR_reweight.SetStats( 0 )
	ratio_CR_reweight.Draw("E")
	ratio_CR_reweight.GetXaxis().SetTitle(plot[2])

	ratio_CR_reweight_QCD_vs_data.Add(histQCD_CR)
	ratio_CR_reweight_QCD_vs_data.Divide(histData)
	ratio_CR_reweight_QCD_vs_data.SetMarkerStyle( 21 )
	ratio_CR_reweight_QCD_vs_data.SetMarkerColor( kBlack )
	ratio_CR_reweight_QCD_vs_data.SetLineColor( kBlack )
	ratio_CR_reweight_QCD_vs_data.Draw("sameE")

	leg_ratio_CR_reweight = TLegend(0.75,0.75,0.95,0.93)
	leg_ratio_CR_reweight.SetBorderSize(0)
	leg_ratio_CR_reweight.SetTextSize(0.08)
	leg_ratio_CR_reweight.SetLineColor(1)
	leg_ratio_CR_reweight.SetLineStyle(1)
	leg_ratio_CR_reweight.SetLineWidth(1)
	leg_ratio_CR_reweight.SetFillColor(0)
	leg_ratio_CR_reweight.SetFillStyle(1001)
	leg_ratio_CR_reweight.AddEntry(ratio_CR_reweight,"#gamma+jets/QCD")
	leg_ratio_CR_reweight.AddEntry(ratio_CR_reweight_QCD_vs_data,"QCD/data")
	leg_ratio_CR_reweight.Draw()


	pad1.Update()
	pad2.Update()

	drawCMS(myC, 13, lumi)	

	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD_dataDriven_reweight.pdf")
	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD_dataDriven_reweight.png")
	myC.SaveAs(outputDir+"/stack"+"/"+plot[1]+"_GJets_vs_QCD_dataDriven_reweight.C")

