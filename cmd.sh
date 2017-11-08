./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p389ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L100TeV_Ctau1000cm_13TeV-pythia8.root \
"L100TeV_Ctau1000cm" \
"signal (L100-Ctau1000)" \
datacard \
> log_L100TeV_Ctau1000cm_datacard.log


./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p389ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L100TeV_Ctau1000cm_13TeV-pythia8.root \
"L100TeV_Ctau1000cm" \
"signal (L100-Ctau1000)" \
bias \
0.000 \
10000 \
> log_L100TeV_Ctau1000cm_bias.log

./Fit2D \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p389ifb.root \
/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/GMSB_L100TeV_Ctau1000cm_13TeV-pythia8.root \
"L100TeV_Ctau1000cm" \
"signal (L100-Ctau1000)" \
binning \
> log_L100TeV_Ctau1000cm_binning.log



