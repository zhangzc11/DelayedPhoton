#!/bin/bash

tmpoutput="tmpxsec.txt"
fulloutput="all_xsecs.txt"

for lamb in 100 150 200 250 300 350 400
do
    for ctau in "0p01" "0p1" "5" "10" "50" "100" "200" "400" "600" "800" "1000" "1200" "1400" "20000" #10 200 400 600 800 1000 1200
    do
	basename=L${lamb}TeV_Ctau${ctau}cm
	#path=/eos/cms/store/group/phys_egamma/soffi/displacedPhotons/GEN-SIM_2304218/${basename}/${basename}
	path=/eos/cms/store/user/zhicaiz/GMSB_2016_Production/GMSB_${basename}_13TeV-pythia8/crab_CMSSW_7_1_25_GMSB_${basename}_GENSIM_T2Caltech_forXsec_withLog_10k/

	./getXSecFromLogs.sh ${path} ${tmpoutput}
	line=$(head -n 1 ${tmpoutput})
	   
	#echo ${lamb} ${sctau} ${line} >> ${fulloutput}
	echo ${basename}	${line}		1.0 	${line} >> ${fulloutput}

	rm ${tmpoutput}
    done
done
