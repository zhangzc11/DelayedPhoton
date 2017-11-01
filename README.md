# DelayedPhoton
Plots and limits for delayed photon analysis
=============================
-----------------------------
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
python skim.py
```

-----------------------------
2. get the background shapes
-----------------------------
```
cd python 
python saveShapes.py
```

-----------------------------
3. run the fit and obtain datacards
-----------------------------
```
./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p389ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L100TeV_Ctau1000cm_13TeV-pythia8.root \
"L100TeV_CTau1000cm" \
"signal (L100-CTau1000)" \
datacard > log.log
```
make sure that you put the signal cross sections in data/XsecBR.dat file
and open the log.log file, search for 'result of fit with SigmaIetaIeta', remember the two fraction numbers and put them in python/config.py (fractionGJets and fractionQCD)

-----------------------------
4. draw the control plots
-----------------------------
```
cd python
python StackPlots.py
```

-----------------------------
5. run the combine limit tool
-----------------------------
```
cd fit_results/datacards/
combine DelayedPhotonCard_L100TeV_CTau1000cm.txt -M Asymptotic -n L100TeV_CTau1000cm
```

-----------------------------
6. draw the limit plots
-----------------------------
```
cd python
python LimitPlots.py
```
-----------------------------
7(optional). bias test
-----------------------------
```
./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p389ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L100TeV_Ctau1000cm_13TeV-pythia8.root \
"L100TeV_CTau1000cm" \
"signal (L100-CTau1000)" \
bias \
0.000 \
10000 > log_bias.log
```



