#!/bin/bash

cards_2016_dir=/data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT
cards_2017_dir=/data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2017

mkdir -p datacards
cd datacards

for ctau in 0p1 10 600 1200
do
	ctau_2016=${ctau}
	if [ ${ctau} == "0p1" ]
	then
		ctau_2016="0_1"
	fi
	for lambda in 100 150 200 250 300 350 400
	do
		echo "combining cards for ctau = ${ctau_2016} and lambda = ${lambda}"
		echo "compute limits for 2016 data..."
		echo "combine ${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016"
		combine ${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016
		echo "compute limits for 2017 data..."
		echo "combine ${cards_2017_dir}/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017"
		combine ${cards_2017_dir}/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017
		echo "combine 2016 and 2017..."
		echo "combineCards.py ch2016=${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt ch2017=${cards_2017_dir}/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm.txt > datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt"	
		combineCards.py ch2016=${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt ch2017=${cards_2017_dir}/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm.txt > datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt
		echo "combine datacard_GMSB_L${lambda}TeV_CTau${ctau}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016And2017"
		combine datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016And2017
	done
done

cd -
