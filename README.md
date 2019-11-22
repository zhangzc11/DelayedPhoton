# DelayedPhoton 

Plots and limits for delayed photon analysis

CADI for 2016+2017 analysis: EXO-19-005

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
git checkout 81x-root606
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
2. run the fit and obtain datacards
-----------------------------
```
./FitABCD \
/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
datacard \
no
```

This will generate the datacard for that signal points
all datacards are in /storage/user/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/combine/datacards
for signals of ctau = 10cm, we use v20 (Closure systematics 90%), for other signal points, we use v18 (Closure systematics 2%)


-----------------------------
5. run the combine limit tool
-----------------------------

We use HybridNews method to run the limits: https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods/#complex-models

It takes a lot of time to run this thing.... so don't try it until you are doing your APPROVAL talk in one week or so... you don't want to do it twice!

As a good approximate, you can just run with the Asymptotic method:

```
cd fit_results/datacards_3J_noBDT/
combine DelayedPhotonCard_L200TeV_Ctau200cm.txt -M Asymptotic -n L200TeV_Ctau200cm
```

to run toys with HybridNew (again, don't even try it now, it's a waste of time to try it at an early stage), we need to submit condor jobs with this script: scripts_condor/submit_HybridNew.py

The limit trees we use for the 2016+2017 paper (calculated with toys from HybridNew) are here: combine/limitTrees_v20v18mix_HybridNew (about 1GB of space)

-----------------------------
6. draw the limit plots
-----------------------------
Once you run all the signal points and you get the limit trees for all of them, you can plot the 2D exclusion region plot (the one in the paper):

```
cd combine
python draw_limits_ind_HybridNew_withBand.py
```

