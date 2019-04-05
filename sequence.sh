./Fit2D \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root \
/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root \
"L350TeV_Ctau200cm" \
"signal (L350-Ctau200)" \
3J \
datacard \
no \
> log_GMSB_L350TeV_Ctau200cm_13TeV-pythia8.log

echo "L350TeV_Ctau200cm limits below (3J):"
cd fit_results/2016/datacards_3J_noBDT

combine DelayedPhotonCard_L350TeV_Ctau200cm.txt -M Asymptotic -n L350TeV_Ctau200cm

cd -
