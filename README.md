# DelayedPhoton

Plots and limits for delayed photon analysis

Analysis twiki: https://github.com/zhangzc11/Twiki/blob/master/CaltechDelayedPhoton2016.md#table-of-contents

setup
-----------------------------
```
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src
mkdir -p HiggsAnalysis
cd HiggsAnalysis
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git CombinedLimit
cd CombinedLimit
git fetch origin
git checkout v7.0.3
scramv1 b clean; scramv1 b
cd ../
git clone git@github.com:zhangzc11/DelayedPhoton.git
cd DelayedPhoton
make
```

Run the analysis step by step

-----------------------------
1. skim the ntuples (not necessary, just to speed up next steps)
-----------------------------
```
cd python
python skim_noBDT.py
```

-----------------------------
2. get the background shapes
-----------------------------
```
cd python 
python saveShapes_noBDT.py
```

-----------------------------
3. run the fit and obtain datacards
-----------------------------
```
./Fit2D \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
datacard \
no > log.log
```
make sure that you put the signal cross sections in data/XsecBR.dat file
and open the log.log file, search for 'result of fit with SigmaIetaIeta', remember the two fraction numbers and put them in python/config_noBDT.py (fractionGJets and fractionQCD)

-----------------------------
4. draw the control plots
-----------------------------
```
cd python
python StackPlots_noBDT.py
```

-----------------------------
5. run the combine limit tool
-----------------------------
```
cd fit_results/datacards_3J_noBDT/
combine DelayedPhotonCard_L200TeV_Ctau200cm.txt -M Asymptotic -n L200TeV_Ctau200cm
```

-----------------------------
6. draw the limit plots
-----------------------------
```
cd python
python LimitPlots_noBDT.py
```
-----------------------------
7. (optional) bias test
-----------------------------
```
./Fit2D \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
bias \
no \
0.000 \
10000 > log_bias.log
```



