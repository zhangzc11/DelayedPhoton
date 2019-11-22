#!/bin/bash


version=v20
cards_2016_dir=/data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/combine/datacards/2016_$version
cards_2017_dir=/data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/combine/datacards/2017_$version


mkdir -p datacards
cd datacards

for ctau in 10 50 100 200 400 600 800 1000 1200 10000
#for ctau in 50 100
#for ctau in 50 100 200
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
	#for lambda in 150
	do
		echo "combining cards for ctau = ${ctau_2016} and lambda = ${lambda}"
		echo "compute limits for 2016 data..."
		echo "combine ${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016 -v 2"
		combine ${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016 -v 2 > log/log_L${lambda}TeV_Ctau${ctau_2016}cm_2016.log
		echo "compute limits for 2017 data (combined)..."
		echo "combine ${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017 -v 2"
		combine ${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017 -v 2 > log/log_L${lambda}TeV_Ctau${ctau_2016}cm_2017.log
		echo "compute limits for 2017 data (CAT1)..."
		echo "combine ${cards_2017_dir}/input/exclusive_1pho/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017CAT1 -v 2"
		combine ${cards_2017_dir}/input/exclusive_1pho/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017CAT1 -v 2 > log/log_L${lambda}TeV_Ctau${ctau_2016}cm_2017CAT1.log
		echo "compute limits for 2017 data (CAT2)..."
		echo "combine ${cards_2017_dir}/input/inclusive_2pho/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017CAT2 -v 2"
		combine ${cards_2017_dir}/input/inclusive_2pho/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2017CAT2 -v 2 > log/log_L${lambda}TeV_Ctau${ctau_2016}cm_2017CAT2.log
		echo "combine 2016 and 2017..."
		echo "combineCards.py Year2016=${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt Year2017=${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt > combine_$version/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt -v 2"	
		combineCards.py Year2016=${cards_2016_dir}/DelayedPhotonCard_L${lambda}TeV_Ctau${ctau_2016}cm.txt Year2017=${cards_2017_dir}/datacardABCD_GMSB_L${lambda}_CTau${ctau}.txt > combine_$version/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt
		echo "combine combine_$version/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016And2017 -v 2"
		combine combine_$version/datacard_GMSB_L${lambda}TeV_CTau${ctau}cm_2016And2017.txt -M Asymptotic -n L${lambda}TeV_CTau${ctau}cm_2016And2017 -v 2 > log/log_L${lambda}TeV_Ctau${ctau_2016}cm_2016And2017.log
	done
done

cd -
