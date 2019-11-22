./FitABCD \
/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
datacard \
no \
> log_L200TeV_Ctau200cm_datacard_noBDT.log

combine fit_results/2016ABCD/datacards_3J_noBDT/DelayedPhotonCard_L200TeV_Ctau200cm.txt -M Asymptotic -n L200TeV_Ctau200cm

./FitABCD \
/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
scaleSys \
no \


./FitABCD \
/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/data/zhicaiz/data/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
binAndDatacard \
no \
> log_L200TeV_Ctau200cm_binAndDatacard_noBDT.log



./FitABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
datacard \
no \
> log_L200TeV_Ctau200cm_datacard_noBDT.log

./FitABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_withBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_withBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
datacard \
yes \
> log_L200TeV_Ctau200cm_datacard_withBDT.log


./FitABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
bias \
no \
0.000 \
10000 \
> log_L200TeV_Ctau200cm_bias_noBDT.log

./FitABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
binning \
no \
> log_L200TeV_Ctau200cm_binning_noBDT.log



