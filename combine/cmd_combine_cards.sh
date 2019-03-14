#!/bin/bash

cards_2016_dir=/data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/combine/datacards/2016
cards_2017_dir=/data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/combine/datacards/2017

mkdir -p datacards
cd datacards

for ctau in 0p001 0p1 10 200 400 600 800 1000 1200 10000
do
	ctau_2016=${ctau}
	if [ ${ctau} == "0p1" ]
	then
		ctau_2016="0_1"
	fi
	if [ ${ctau} == "0p001" ]
	then
		ctau_2016="0_001"
	fi

	#for lambda in 100 150 200 250 300 350 400
	for lambda in 150
	do
		echo "combining cards for ctau = ${ctau_2016} and lambda = ${lambda}"
		echo "compute limits for 2016 data..."
		echo "combine ${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016"
		combine ${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016
		echo "compute limits for 2017 data..."
		echo "combine ${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017"
		combine ${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017
		echo "combine 2016 and 2017..."
		echo "combineCards.py ch2016=${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt ch2017=${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt > combine/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt"	
		combineCards.py ch2016=${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt ch2017=${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt > combine/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt
		echo "combine combine/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016And2017"
		combine combine/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016And2017
	done
done

cd -
