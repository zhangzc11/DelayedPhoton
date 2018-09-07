python TimingCorr_vs_eta.py > log_cor_vs_eta.log
python TimingCorr_vs_pt.py > log_cor_vs_pt.log
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


Timing_vs_pt_photon_GJets.py
Timing_vs_pt_photon_QCD.py
Timing_vs_pt_photon_signal.py

