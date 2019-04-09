#!/bin/bash
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L300TeV_Ctau200cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L300TeV_Ctau200cm_13TeV-pythia8.root "L300TeV_Ctau200cm" "signal ( L300TeV_Ctau200 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L300TeV_Ctau200cm limits below (3J):" 
combine DelayedPhotonCard_L300TeV_Ctau200cm.txt -M Asymptotic -n L300TeV_Ctau200cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L300TeV_Ctau400cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L300TeV_Ctau400cm_13TeV-pythia8.root "L300TeV_Ctau400cm" "signal ( L300TeV_Ctau400 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L300TeV_Ctau400cm limits below (3J):" 
combine DelayedPhotonCard_L300TeV_Ctau400cm.txt -M Asymptotic -n L300TeV_Ctau400cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L300TeV_Ctau600cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L300TeV_Ctau600cm_13TeV-pythia8.root "L300TeV_Ctau600cm" "signal ( L300TeV_Ctau600 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L300TeV_Ctau600cm limits below (3J):" 
combine DelayedPhotonCard_L300TeV_Ctau600cm.txt -M Asymptotic -n L300TeV_Ctau600cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L300TeV_Ctau800cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L300TeV_Ctau800cm_13TeV-pythia8.root "L300TeV_Ctau800cm" "signal ( L300TeV_Ctau800 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L300TeV_Ctau800cm limits below (3J):" 
combine DelayedPhotonCard_L300TeV_Ctau800cm.txt -M Asymptotic -n L300TeV_Ctau800cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L300TeV_Ctau1000cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L300TeV_Ctau1000cm_13TeV-pythia8.root "L300TeV_Ctau1000cm" "signal ( L300TeV_Ctau1000 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L300TeV_Ctau1000cm limits below (3J):" 
combine DelayedPhotonCard_L300TeV_Ctau1000cm.txt -M Asymptotic -n L300TeV_Ctau1000cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L300TeV_Ctau1200cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L300TeV_Ctau1200cm_13TeV-pythia8.root "L300TeV_Ctau1200cm" "signal ( L300TeV_Ctau1200 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L300TeV_Ctau1200cm limits below (3J):" 
combine DelayedPhotonCard_L300TeV_Ctau1200cm.txt -M Asymptotic -n L300TeV_Ctau1200cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L350TeV_Ctau0_1cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau0_1cm_13TeV-pythia8.root "L350TeV_Ctau0_1cm" "signal ( L350TeV_Ctau0_1 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L350TeV_Ctau0_1cm limits below (3J):" 
combine DelayedPhotonCard_L350TeV_Ctau0_1cm.txt -M Asymptotic -n L350TeV_Ctau0_1cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L350TeV_Ctau10cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau10cm_13TeV-pythia8.root "L350TeV_Ctau10cm" "signal ( L350TeV_Ctau10 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L350TeV_Ctau10cm limits below (3J):" 
combine DelayedPhotonCard_L350TeV_Ctau10cm.txt -M Asymptotic -n L350TeV_Ctau10cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L350TeV_Ctau200cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root "L350TeV_Ctau200cm" "signal ( L350TeV_Ctau200 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L350TeV_Ctau200cm limits below (3J):" 
combine DelayedPhotonCard_L350TeV_Ctau200cm.txt -M Asymptotic -n L350TeV_Ctau200cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L350TeV_Ctau400cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau400cm_13TeV-pythia8.root "L350TeV_Ctau400cm" "signal ( L350TeV_Ctau400 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L350TeV_Ctau400cm limits below (3J):" 
combine DelayedPhotonCard_L350TeV_Ctau400cm.txt -M Asymptotic -n L350TeV_Ctau400cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L350TeV_Ctau600cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau600cm_13TeV-pythia8.root "L350TeV_Ctau600cm" "signal ( L350TeV_Ctau600 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L350TeV_Ctau600cm limits below (3J):" 
combine DelayedPhotonCard_L350TeV_Ctau600cm.txt -M Asymptotic -n L350TeV_Ctau600cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L350TeV_Ctau800cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau800cm_13TeV-pythia8.root "L350TeV_Ctau800cm" "signal ( L350TeV_Ctau800 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L350TeV_Ctau800cm limits below (3J):" 
combine DelayedPhotonCard_L350TeV_Ctau800cm.txt -M Asymptotic -n L350TeV_Ctau800cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L350TeV_Ctau1000cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau1000cm_13TeV-pythia8.root "L350TeV_Ctau1000cm" "signal ( L350TeV_Ctau1000 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L350TeV_Ctau1000cm limits below (3J):" 
combine DelayedPhotonCard_L350TeV_Ctau1000cm.txt -M Asymptotic -n L350TeV_Ctau1000cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L350TeV_Ctau1200cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau1200cm_13TeV-pythia8.root "L350TeV_Ctau1200cm" "signal ( L350TeV_Ctau1200 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L350TeV_Ctau1200cm limits below (3J):" 
combine DelayedPhotonCard_L350TeV_Ctau1200cm.txt -M Asymptotic -n L350TeV_Ctau1200cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L400TeV_Ctau0_1cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root "L400TeV_Ctau0_1cm" "signal ( L400TeV_Ctau0_1 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L400TeV_Ctau0_1cm limits below (3J):" 
combine DelayedPhotonCard_L400TeV_Ctau0_1cm.txt -M Asymptotic -n L400TeV_Ctau0_1cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L400TeV_Ctau10cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau10cm_13TeV-pythia8.root "L400TeV_Ctau10cm" "signal ( L400TeV_Ctau10 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L400TeV_Ctau10cm limits below (3J):" 
combine DelayedPhotonCard_L400TeV_Ctau10cm.txt -M Asymptotic -n L400TeV_Ctau10cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L400TeV_Ctau200cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root "L400TeV_Ctau200cm" "signal ( L400TeV_Ctau200 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L400TeV_Ctau200cm limits below (3J):" 
combine DelayedPhotonCard_L400TeV_Ctau200cm.txt -M Asymptotic -n L400TeV_Ctau200cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L400TeV_Ctau400cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau400cm_13TeV-pythia8.root "L400TeV_Ctau400cm" "signal ( L400TeV_Ctau400 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L400TeV_Ctau400cm limits below (3J):" 
combine DelayedPhotonCard_L400TeV_Ctau400cm.txt -M Asymptotic -n L400TeV_Ctau400cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L400TeV_Ctau600cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau600cm_13TeV-pythia8.root "L400TeV_Ctau600cm" "signal ( L400TeV_Ctau600 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L400TeV_Ctau600cm limits below (3J):" 
combine DelayedPhotonCard_L400TeV_Ctau600cm.txt -M Asymptotic -n L400TeV_Ctau600cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L400TeV_Ctau800cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau800cm_13TeV-pythia8.root "L400TeV_Ctau800cm" "signal ( L400TeV_Ctau800 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L400TeV_Ctau800cm limits below (3J):" 
combine DelayedPhotonCard_L400TeV_Ctau800cm.txt -M Asymptotic -n L400TeV_Ctau800cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L400TeV_Ctau1000cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau1000cm_13TeV-pythia8.root "L400TeV_Ctau1000cm" "signal ( L400TeV_Ctau1000 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L400TeV_Ctau1000cm limits below (3J):" 
combine DelayedPhotonCard_L400TeV_Ctau1000cm.txt -M Asymptotic -n L400TeV_Ctau1000cm
date
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/
echo "running on category 3J ======= for signal model L400TeV_Ctau1200cm" 
./Fit2D /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root /mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L400TeV_Ctau1200cm_13TeV-pythia8.root "L400TeV_Ctau1200cm" "signal ( L400TeV_Ctau1200 )" 3J datacard no 
cd /data/zhicaiz/release/DelayedPhoton/CMSSW_8_1_0/src/HiggsAnalysis/DelayedPhoton/fit_results/2016/datacards_3J_noBDT 
echo "L400TeV_Ctau1200cm limits below (3J):" 
combine DelayedPhotonCard_L400TeV_Ctau1200cm.txt -M Asymptotic -n L400TeV_Ctau1200cm
date
