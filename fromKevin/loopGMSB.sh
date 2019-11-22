#!/bin/bash
tmpoutput="tmpxsec.txt"
fulloutput="all_xsecs.txt"
for lamb in 100 150 200 250 300 350 400
do
    for ctau in 1 50 100
    do
	basename=L${lamb}TeV_Ctau${ctau}cm
	#path=/eos/cms/store/group/phys_egamma/soffi/displacedPhotons/GEN-SIM_2304218/${basename}/${basename}
	path=/mnt/hadoop/store/group/phys_susy/razor/zhicaiz/GMSB_2017_Production/GMSB_${basename}_13TeV-pythia8/crab_CMSSW_9_3_9_GMSB_${basename}_GENSIM_CaltechT2_29Apr2019/

	./getXSecFromLogs.sh ${path} ${tmpoutput}
	line=$(head -n 1 ${tmpoutput})
	   
	#echo ${lamb} ${sctau} ${line} >> ${fulloutput}
	echo ${basename}	${line}		1.0 	${line} >> ${fulloutput}

	rm ${tmpoutput}
    done
done
