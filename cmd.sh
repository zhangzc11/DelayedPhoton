./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_32p0742ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
datacard \
no \
> log_L350TeV_Ctau200cm_datacard.log

./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim_withBDT/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_32p0742ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim_withBDT/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
datacard \
yes \
> log_L350TeV_Ctau200cm_datacard_withBDT.log


./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_32p0742ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
bias \
no \
0.000 \
10000 \
> log_L350TeV_Ctau200cm_bias.log

./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_32p0742ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
binning \
no \
> log_L350TeV_Ctau200cm_binning.log



