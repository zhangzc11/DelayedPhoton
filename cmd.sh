./Fit2DABCD \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L300TeV_Ctau1200cm_13TeV-pythia8.root \
"L300TeV_Ctau1200cm" \
"signal (L300-Ctau1200)" \
3J \
datacard \
no 

./Fit2D \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
datacard \
no \
> log_L200TeV_Ctau200cm_datacard_noBDT.log

./Fit2D \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_withBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_withBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
datacard \
yes \
> log_L200TeV_Ctau200cm_datacard_withBDT.log


./Fit2D \
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

./Fit2D \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root \
"L200TeV_Ctau200cm" \
"signal (L200-Ctau200)" \
3J \
binning \
no \
> log_L200TeV_Ctau200cm_binning_noBDT.log



