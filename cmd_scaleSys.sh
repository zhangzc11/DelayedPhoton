#!/bin/sh

for lambda in 100 150 200 250 300 350 400
do
	#for ctau in 10 200 400 600 800 1000 1200 10000
	for ctau in 1200 10000
	do
		./FitABCD /data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L${lambda}TeV_Ctau${ctau}cm_13TeV-pythia8.root "L${lambda}TeV_Ctau${ctau}cm" "signal (L${lambda}-Ctau${ctau})" 3J scaleSys no
	done
done
