#!/bin/sh

joboutDir=/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/

currentDir=`pwd`

cd ../
appDir=`pwd`
cd ${currentDir}

mkdir temp
cd temp

for lambda in 100 150 200 250 300 350 400
do
        for ctau in 0_001 0_1 10 200 400 600 800 1000 1200 10000
        do
		rm -rf *
		tar -zxvf /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/fit_results/fitABCD_L${lambda}TeV_Ctau${ctau}cm.tar
		for subdirs in `ls fit_results/2016ABCD/`
		do
			cp fit_results/2016ABCD/${subdirs}/* ${appDir}/fit_results/2016ABCD/${subdirs}/
		done
	done
done

cd -

