./FitABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L350-Ctau200)" \
3J \
datacard \
no \
> log_L350TeV_Ctau200cm_datacard_noBDT.log

./FitABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_withBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_withBDT/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L350-Ctau200)" \
3J \
datacard \
yes \
> log_L350TeV_Ctau200cm_datacard_withBDT.log


./FitABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L350-Ctau200)" \
3J \
bias \
no \
0.000 \
10000 \
> log_L350TeV_Ctau200cm_bias_noBDT.log

./FitABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L350-Ctau200)" \
3J \
binning \
no \
> log_L350TeV_Ctau200cm_binning_noBDT.log


