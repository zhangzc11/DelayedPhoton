./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p1186ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L250TeV_Ctau200cm_13TeV-pythia8.root \
"L250TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
datacard \
> log_L250TeV_Ctau200cm_datacard.log


./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p1186ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L250TeV_Ctau200cm_13TeV-pythia8.root \
"L250TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
bias \
0.000 \
10000 \
> log_L250TeV_Ctau200cm_bias.log

./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p1186ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L250TeV_Ctau200cm_13TeV-pythia8.root \
"L250TeV_Ctau200cm" \
"signal (L100-Ctau1000)" \
3J \
binning \
> log_L250TeV_Ctau200cm_binning.log



