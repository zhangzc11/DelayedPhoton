#!/bin/bash

cards_2016_dir=/data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/combine/datacards/2016
cards_2017_dir=/data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/combine/datacards/2017

mkdir -p datacards
cd datacards

for ctau in 10 200 400 600 800 1000 1200 10000
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

	for lambda in 100 150 200 250 300 350 400
	do
		echo "combining cards for ctau = ${ctau_2016} and lambda = ${lambda}"
		echo "compute limits for 2016 data..."
		echo "combine ${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016 -v 2"
		combine ${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016 -v 2 > log/log_L${lambda}TeV_Ctau${ctau_2016}cm_2016.log
		echo "compute limits for 2017 data..."
		echo "combine ${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017 -v 2"
		combine ${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017 -v 2 > log/log_L${lambda}TeV_Ctau${ctau_2016}cm_2017.log
		echo "combine 2016 and 2017..."
		echo "combineCards.py Year2016=${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt Year2017=${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt > combine/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt -v 2"	
		combineCards.py Year2016=${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt Year2017=${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt > combine/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt
		echo "combine combine/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016And2017 -v 2"
		combine combine/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016And2017 -v 2 > log/log_L${lambda}TeV_Ctau${ctau_2016}cm_2016And2017.log
	done
done

cd -
