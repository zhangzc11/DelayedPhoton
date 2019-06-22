#!/bin/sh

joboutDir=/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/HybridNew_v18

currentDir=`pwd`

cd ../
appDir=`pwd`
cd ${currentDir}

rm -rf temp
mkdir -p temp
mkdir -p temp/trees
mkdir -p temp/plots
cd temp

#for vs in _2016And2017_2000Tx5 _2016And2017_2000Tx10 _2016And2017_2000Tx10_r4p0 _2016And2017_2000Tx10_r3to6p0
for vs in _2016_10000T _2016_10000T_4p0
do
	for lambda in 100 150 200 250 300 350 400
	do
		for ctau in 10 50 100 200 400 600 800 1000 1200 10000
		do
			tar -zxvf ${joboutDir}${vs}/L${lambda}TeV_CTau${ctau}cm.tar
			mkdir -p trees/L${lambda}TeV_CTau${ctau}cm
			rm L${lambda}TeV_CTau${ctau}cm/*merged*.root	
			rm L${lambda}TeV_CTau${ctau}cm/*quant*.root	
			rm L${lambda}TeV_CTau${ctau}cm/*Observed*.root	
			mv L${lambda}TeV_CTau${ctau}cm/*.root trees/L${lambda}TeV_CTau${ctau}cm/
			rm -rf L${lambda}TeV_CTau${ctau}cm/
		done
	done
done

cd -

