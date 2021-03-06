python TimingCorr_vs_E.py > log_cor_vs_E.log
python skim_noBDT.py

python saveShapes_noBDT.py
python MET_CR_vs_SR.py
python sumETreweight_noBDT.py
#mv /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi_noreweight.root
#mv /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi_reweight.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root

python GJets_vs_QCD_noBDT.py

rm effTable.txt
python signalEff_noBDT.py
python StackPlots_noBDT.py


python Timing_vs_E_photon_GJets.py
python Timing_vs_E_photon_QCD.py
python Timing_vs_E_photon_signal.py



