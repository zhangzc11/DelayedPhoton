########################################################
##common configuration parameters for all plot scripts##
########################################################

#######################input trees######################
fileNameData = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_DoubleEG_2016All_GoodLumi.root'
fileNameGJets = [
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]
fileNameQCD = [
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]	
fileNameSig = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root'
sigLegend = "signal (L350TeV-Ctau200cm)"
#fileNameSig = '/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/skim_noBDT/DelayedPhoton_GMSB_Ctau2190mm.root'
#sigLegend = "GMSB (2190mm)"

################lumi and cross sections#################
lumi =  35922.0 #pb^-1
xsecSig = 0.15 #pb 0.0015
xsecGJets = [20790.0, 9238.0, 2305, 274.4, 93.46] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Gamma_jets
xsecQCD = [1712000, 347700, 32100, 6831, 1207, 119.9, 25.24] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
fractionGJets = 0.5414 # from fit to SigmaIetaIeta
fractionQCD = 0.4585 # from fit fo SigmaIetaIeta
useFraction = True
scaleBkg = 1.0
timeShift = 0.297

###############cuts and outputs########################
cut_MET_filter = " && Flag_HBHENoiseFilter == 1 && Flag_HBHEIsoNoiseFilter ==1 && Flag_goodVertices == 1 && Flag_eeBadScFilter == 1 && Flag_EcalDeadCellTriggerPrimitiveFilter == 1 && Flag_CSCTightHaloFilter == 1 && Flag_badChargedCandidateFilter == 1 && Flag_badMuonFilter == 1 && Flag_badGlobalMuonFilter == 0 && Flag_duplicateMuonFilter ==0"

cut_3J = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2' + cut_MET_filter + " && pho1SigmaIetaIeta < 0.00994"
cut_3J_noSigmaIetaIeta = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2' + cut_MET_filter 
cut_2J = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets == 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2' + cut_MET_filter + " && pho1SigmaIetaIeta < 0.00994"
cut_2J_noSigmaIetaIeta = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets == 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2' + cut_MET_filter


cut_QCD_shape_3J = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && (!pho1isPromptPhoton)' + cut_MET_filter + " && pho1SigmaIetaIeta < 0.00994"
cut_QCD_shape_3J_noSigmaIetaIeta = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && (!pho1isPromptPhoton)' + cut_MET_filter
cut_QCD_shape_2J = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && (!pho1isPromptPhoton)' + cut_MET_filter + " && pho1SigmaIetaIeta < 0.00994"
cut_QCD_shape_2J_noSigmaIetaIeta = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && (!pho1isPromptPhoton)' + cut_MET_filter

cut_GJets_shape_3J = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && pho1isPromptPhoton' + cut_MET_filter + " && pho1SigmaIetaIeta < 0.00994"
cut_GJets_shape_3J_noSigmaIetaIeta = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && pho1isPromptPhoton' + cut_MET_filter
cut_GJets_shape_2J = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets == 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && pho1isPromptPhoton' + cut_MET_filter + " && pho1SigmaIetaIeta < 0.00994"
cut_GJets_shape_2J_noSigmaIetaIeta = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets == 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && pho1isPromptPhoton' + cut_MET_filter


cut_loose_3J = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.7 && (HLTDecision[81] == 1) && n_Photons == 2" + cut_MET_filter + " && pho1SigmaIetaIeta < 0.01031"
cut_loose_3J_noSigmaIetaIeta = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.7 && (HLTDecision[81] == 1) && n_Photons == 2" + cut_MET_filter
cut_loose_2J = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && n_Jets == 2 && pho1Sminor>0.15 && pho1Sminor<0.7 && (HLTDecision[81] == 1) && n_Photons == 2" + cut_MET_filter + " && pho1SigmaIetaIeta < 0.01031"
cut_loose_2J_noSigmaIetaIeta = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose_PFClusterIso && pho1passEleVeto && n_Jets == 2 && pho1Sminor>0.15 && pho1Sminor<0.7 && (HLTDecision[81] == 1) && n_Photons == 2" + cut_MET_filter


cut_GJets_3J = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets < 3 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)" + cut_MET_filter+ " && pho1SigmaIetaIeta < 0.00994"
cut_GJets_3J_noSigmaIetaIeta = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets < 3 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)" + cut_MET_filter
cut_GJets_2J = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets == 1 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)" + cut_MET_filter+ " && pho1SigmaIetaIeta < 0.00994"
cut_GJets_2J_noSigmaIetaIeta = "pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight_PFClusterIso && pho1passEleVeto && n_Jets == 1 && pho1Sminor>0.15 && pho1Sminor<0.3 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)" + cut_MET_filter

weight_cut = "(weight*pileupWeight*triggerEffSFWeight*photonEffSF*triggerEffWeight) * "

cut = cut_3J
cut_noSigmaIetaIeta = cut_3J_noSigmaIetaIeta
cut_noDisc = cut_3J
cut_QCD_shape = cut_QCD_shape_3J
cut_QCD_shape_noSigmaIetaIeta = cut_QCD_shape_3J_noSigmaIetaIeta
cut_GJets_shape = cut_GJets_shape_3J
cut_GJets_shape_noSigmaIetaIeta = cut_GJets_shape_3J_noSigmaIetaIeta
cut_loose = cut_loose_3J
cut_loose_noSigmaIetaIeta = cut_loose_3J_noSigmaIetaIeta
cut_GJets = cut_GJets_3J
cut_GJets_noSigmaIetaIeta = cut_GJets_3J_noSigmaIetaIeta


cut_skim = "pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passEleVeto && (HLTDecision[81] == 1 || HLTDecision[100] == 1 || HLTDecision[102]==1 || HLTDecision[92] == 1 || HLTDecision[93] == 1)"
cut_skim_bkg = "pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passEleVeto && (HLTDecision[81] == 1 || HLTDecision[100] == 1 || HLTDecision[102]==1 || HLTDecision[92] == 1 || HLTDecision[93] == 1)"

outputDir = '/data/zhicaiz/www/sharebox/DelayedPhoton/28Oct2018/orderByPt/'

############define the plot you want to make##########
##for stack plots
xbins_MET = [0.0, 10.0, 20.0, 40.0, 60.0, 80, 100.0, 125.0, 150.0, 175.0, 200.0, 250.0, 300.0, 400.0, 500.0, 1000.0]
xbins_time = [-15, -10, -5, -4, -3, -2.5, -2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3, 4, 5, 10, 15]

splots = []
#variable name in the tree, output plot file name, description/title, Nbins, lowX, upX, useLogy
splots.append(["t1MET", "MET_linear", "#slash{E}_{T} [GeV]", 100,0,800, False])
splots.append(["t1MET", "MET_log", "#slash{E}_{T} [GeV]", 100,0,800, True])
splots.append(["sumMET", "sumMET_linear", "#Sigma E_{T} [GeV]", 100,0,8000, False])
splots.append(["sumMET", "sumMET_log", "#Sigma E_{T} [GeV]", 100,0,8000, True])

splots.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta_linear", "#sigma_{i#eta i#eta}", 100,0.005,0.025, False])
splots.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta_log", "#sigma_{i#eta i#eta}", 100,0.005,0.025, True])

splots.append(["pho1ClusterTime", "phoTimeCluster_noSmear_linear", "#gamma cluster time [ns]", 100,-15,15, False])
splots.append(["pho1ClusterTime", "phoTimeCluster_noSmear_log", "#gamma cluster time [ns]", 100,-15,15, True])
splots.append(["pho1ClusterTime_SmearToData", "phoTimeCluster_linear", "#gamma cluster time [ns]", 100,-15,15, False])
splots.append(["pho1ClusterTime_SmearToData", "phoTimeCluster_log", "#gamma cluster time [ns]", 100,-15,15, True])

splots.append(["pho1Sminor/pho1Smajor", "SminorOverSmajor_linear", "S_{minor}/S_{major}", 50,0,1.1, False])
splots.append(["pho1Sminor/pho1Smajor", "SminorOverSmajor_log", "S_{minor}/S_{major}", 50,0,1.1, True])
splots.append(["sqrt(pho1Sminor)/sqrt(pho1Smajor)", "SminorSqrtOverSmajorSqrt_linear", "#sqrt{S_{minor}}/#sqrt{S_{major}}", 50,0,1.1, False])
splots.append(["sqrt(pho1Sminor)/sqrt(pho1Smajor)", "SminorSqrtOverSmajorSqrt_log", "#sqrt{S_{minor}}/#sqrt{S_{major}}", 50,0,1.1, True])

splots.append(["pho1ecalPFClusterIso", "pho1ecalPFClusterIso_linear", "PF Cluster ECAL isolation [GeV]", 100,-0.1,30.0, False])
splots.append(["pho1hcalPFClusterIso", "pho1hcalPFClusterIso_linear", "PF Cluster HCAL isolation [GeV]", 100,-0.1,30.0, False])
splots.append(["pho1trkSumPtHollowConeDR03", "pho1trkSumPtHollowConeDR03_linear", "PF Cluster tracker isolation [GeV]", 100,-0.1,30.0, False])
splots.append(["pho1sumPhotonEt", "pho1sumPhotonEt_linear", "PF photon isolation [GeV]", 100,-0.1,30.0, False])
splots.append(["pho1sumNeutralHadronEt", "pho1sumNeutralHadronEt_linear", "PF neutral hadron isolation [GeV]", 100,-0.1,30.0, False])
splots.append(["pho1sumChargedHadronPt", "phosumChargedHadronPt_linear", "PF charged hadron isolation [GeV]", 100,-0.1,30.0, False])
splots.append(["pho1sumChargedHadronPt", "phosumChargedHadronPt_log", "charged isolation [GeV]", 100,-0.1,30.0, True])
splots.append(["pho1sigmaEOverE", "phosigmaEOverE_linear", "#sigma_{E}/E", 100,0.,0.5, False])
splots.append(["pho1sigmaEOverE", "phosigmaEOverE_log", "#sigma_{E}/E", 100,0.,0.5, True])
splots.append(["pho1Pt", "phoPt_linear", "p_{T}^{#gamma} [GeV]", 100,50,2000, False])
splots.append(["pho1Pt", "phoPt_log", "p_{T}^{#gamma} [GeV]", 100,50,2000, True])

splots.append(["pho1Sminor", "Sminor_linear", "S_{minor}", 50,0,0.5, False])
splots.append(["pho1Sminor", "Sminor_log", "S_{minor}", 50,0,0.5, True])
splots.append(["sqrt(pho1Sminor)", "SminorSqrt_linear", "#sqrt{S_{minor}}", 50,0,1, False])
splots.append(["sqrt(pho1Sminor)", "SminorSqrt_log", "#sqrt{S_{minor}}", 50,0,1, True])
splots.append(["pho1Smajor", "Smajor_linear", "S_{major}", 50,0,1, False])
splots.append(["pho1Smajor", "Smajor_log", "S_{major}", 50,0,1, True])
splots.append(["sqrt(pho1Smajor)", "SmajorSqrt_linear", "#sqrt{S_{major}}", 50,0,1, False])
splots.append(["sqrt(pho1Smajor)", "SmajorSqrt_log", "#sqrt{S_{major}}", 50,0,1, True])
splots.append(["nPV", "nPV_linear", "number of vertices", 50,-0.5,49.5, False])
splots.append(["nPV", "nPV_log", "number of vertices", 50,-0.5,49.5, True])
splots.append(["n_Jets", "nJets_linear", "number of jets", 15,-0.5,14.5, False])
splots.append(["n_Jets", "nJets_log", "number of jets", 15,-0.5,14.5, True])
splots.append(["pho1Pt", "phoPt_linear", "p_{T}^{#gamma} [GeV]", 100,100,2000, False])
splots.append(["pho1Pt", "phoPt_log", "p_{T}^{#gamma} [GeV]", 100,100,2000, True])
splots.append(["pho1SeedTimeRaw", "phoTimeSeedRaw_linear", "#gamma seed raw time [ns]", 100,-15,15, False])
splots.append(["pho1SeedTimeRaw", "phoTimeSeedRaw_log", "#gamma seed raw time [ns]", 100,-15,15, True])
splots.append(["pho1SeedTimeCalib", "phoTimeSeedCalib_linear", "#gamma seed calibrated time [ns]", 100,-15,15, False])
splots.append(["pho1SeedTimeCalib", "phoTimeSeedCalib_log", "#gamma seed calibrated time [ns]", 100,-15,15, True])
splots.append(["pho1SeedTimeCalibTOF", "phoTimeSeedCalibTOF_linear", "#gamma seed calibrated time & TOF [ns]", 100,-15,15, False])
splots.append(["pho1SeedTimeCalibTOF", "phoTimeSeedCalibTOF_log", "#gamma seed calibrated time & TOF [ns]", 100,-15,15, True])

############define the variables for which you want to save the bkg shape##########
shapes = []
shapes.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta", "#sigma_{i#eta i#eta}", 100,0.005,0.025])
shapes.append(["pho1sigmaEOverE", "phosigmaEOverE", "#sigma_{E}/E", 100,0.,0.5])
shapes.append(["pho1Smajor", "Smajor", "S_{major}", 100,0,1])
shapes.append(["pho1Sminor", "Sminor", "S_{minor}", 100,0,0.5])
shapes.append(["pho1Pt", "phoPt", "p_{T}^{#gamma} [GeV]", 100,50,1500])
shapes.append(["n_Jets", "nJets", "number of jets", 15,-0.5,14.5])

#####################limit plot settings####################################

list_limits_vs_lifetime = []

limits_vs_lifetime1 = []
limits_vs_lifetime1.append(["L150TeV_Ctau0_1cm",   150.0, 212.1, 0.1,   0.233382])
limits_vs_lifetime1.append(["L150TeV_Ctau10cm",   150.0, 212.1, 10.0,   0.23281])
limits_vs_lifetime1.append(["L150TeV_Ctau200cm",   150.0, 212.1, 200.0,   0.23355])
limits_vs_lifetime1.append(["L150TeV_Ctau400cm",   150.0, 212.1, 400.0,   0.231478])
limits_vs_lifetime1.append(["L150TeV_Ctau600cm",   150.0, 212.1, 600.0,   0.234354])
#limits_vs_lifetime1.append(["L150TeV_Ctau800cm",   150.0, 212.1, 800.0,   0.230648])
limits_vs_lifetime1.append(["L150TeV_Ctau1000cm",  150.0, 212.1, 1000.0,  0.233782])
mass_limits_vs_lifetime1 = 212.1
list_limits_vs_lifetime.append([mass_limits_vs_lifetime1, limits_vs_lifetime1])


limits_vs_lifetime2 = []
limits_vs_lifetime2.append(["L200TeV_Ctau0_1cm",   200.0, 284.8, 0.1,   0.0428312])
limits_vs_lifetime2.append(["L200TeV_Ctau10cm",   200.0, 284.8, 10.0,   0.0428514])
limits_vs_lifetime2.append(["L200TeV_Ctau200cm",   200.0, 284.8, 200.0,   0.0424614])
limits_vs_lifetime2.append(["L200TeV_Ctau400cm",   200.0, 284.8, 400.0,   0.0427252])
limits_vs_lifetime2.append(["L200TeV_Ctau600cm",   200.0, 284.8, 600.0,   0.0431458])
limits_vs_lifetime2.append(["L200TeV_Ctau800cm",   200.0, 284.8, 800.0,   0.0423242])
#limits_vs_lifetime2.append(["L200TeV_Ctau1000cm",   200.0, 284.8, 1000.0,   0.042969])
limits_vs_lifetime2.append(["L200TeV_Ctau1200cm",   200.0, 284.8, 1200.0,   0.0422256])
mass_limits_vs_lifetime2 = 284.8
list_limits_vs_lifetime.append([mass_limits_vs_lifetime2, limits_vs_lifetime2])


limits_vs_lifetime3 = []
limits_vs_lifetime3.append(["L250TeV_Ctau10cm",   250.0, 357.5, 10.0,   0.0116892])
limits_vs_lifetime3.append(["L250TeV_Ctau200cm",   250.0, 357.5, 200.0,   0.0118048])
limits_vs_lifetime3.append(["L250TeV_Ctau400cm",  250.0, 357.5, 400.0,  0.0115646])
limits_vs_lifetime3.append(["L250TeV_Ctau600cm",  250.0, 357.5, 600.0,  0.0116992])
limits_vs_lifetime3.append(["L250TeV_Ctau800cm",  250.0, 357.5, 800.0,  0.0116992])
limits_vs_lifetime3.append(["L250TeV_Ctau1000cm",  250.0, 357.5, 1000.0,  0.0116992])
limits_vs_lifetime3.append(["L250TeV_Ctau1200cm",  250.0, 357.5, 1200.0,  0.0116992])
mass_limits_vs_lifetime3 = 357.5
list_limits_vs_lifetime.append([mass_limits_vs_lifetime3, limits_vs_lifetime3])

limits_vs_lifetime4 = []
limits_vs_lifetime4.append(["L300TeV_Ctau0_1cm",  300.0, 430.4, 0.1,  0.00418322])
limits_vs_lifetime4.append(["L300TeV_Ctau10cm",  300.0, 430.4, 10.0,  0.00410951])
limits_vs_lifetime4.append(["L300TeV_Ctau200cm",  300.0, 430.4, 200.0,  0.00418529])
limits_vs_lifetime4.append(["L300TeV_Ctau400cm",  300.0, 430.4, 400.0,  0.00418529])
limits_vs_lifetime4.append(["L300TeV_Ctau600cm",  300.0, 430.4, 600.0,  0.0041645])
limits_vs_lifetime4.append(["L300TeV_Ctau800cm",  300.0, 430.4, 800.0,  0.0041645])
limits_vs_lifetime4.append(["L300TeV_Ctau1000cm",  300.0, 430.4, 1000.0,  0.0041645])
limits_vs_lifetime4.append(["L300TeV_Ctau1200cm",  300.0, 430.4, 1200.0,  0.0041645])
mass_limits_vs_lifetime4 = 430.4
list_limits_vs_lifetime.append([mass_limits_vs_lifetime4, limits_vs_lifetime4])


list_limits_vs_mass = []

limits_vs_mass1 = []
limits_vs_mass1.append(["L100TeV_Ctau1200cm", 100.0, 139.4, 1200.0, 2.09996])
limits_vs_mass1.append(["L200TeV_Ctau1200cm",   200.0, 284.8, 1200.0,   0.0422256])
limits_vs_mass1.append(["L250TeV_Ctau1200cm",   250.0, 357.5, 1200.0,   0.0116992])
limits_vs_mass1.append(["L300TeV_Ctau1200cm",   300.0, 430.4, 1200.0,   0.0041645])
limits_vs_mass1.append(["L350TeV_Ctau1200cm",   350.0, 503.4, 1200.0,   0.00174708])
limits_vs_mass1.append(["L400TeV_Ctau1200cm",   400.0, 576.4, 1200.0,   0.000793036])
lifetime_limits_vs_mass1 = 1200.0
list_limits_vs_mass.append([lifetime_limits_vs_mass1, limits_vs_mass1])


limits_vs_mass2 = []
#limits_vs_mass2.append(["L100TeV_Ctau600cm",   100.0, 139.4, 600.0,   2.07166])
limits_vs_mass2.append(["L150TeV_Ctau600cm",   150.0, 212.1, 600.0,   0.234354])
limits_vs_mass2.append(["L200TeV_Ctau600cm",   200.0, 284.8, 600.0,   0.0431458])
limits_vs_mass2.append(["L250TeV_Ctau600cm",  250.0, 357.5, 600.0,  0.0116992])
limits_vs_mass2.append(["L300TeV_Ctau600cm",  300.0, 430.4, 600.0,  0.0041645])
limits_vs_mass2.append(["L350TeV_Ctau600cm",  300.0, 503.4, 600.0,  0.00174708])
limits_vs_mass2.append(["L400TeV_Ctau600cm",  300.0, 576.4, 600.0,  0.000790256])
lifetime_limits_vs_mass2 = 600.0
list_limits_vs_mass.append([lifetime_limits_vs_mass2, limits_vs_mass2])


limits_vs_mass3 = []
limits_vs_mass3.append(["L100TeV_Ctau200cm",   100.0, 139.4, 200.0,   2.07166])
limits_vs_mass3.append(["L150TeV_Ctau200cm",   150.0, 212.1, 200.0,   0.23555])
limits_vs_mass3.append(["L200TeV_Ctau200cm",   200.0, 284.8, 200.0,   0.0424614])
limits_vs_mass3.append(["L250TeV_Ctau200cm",   250.0, 357.5, 200.0,   0.0118048])
limits_vs_mass3.append(["L300TeV_Ctau200cm",   300.0, 430.4, 200.0,  0.00418529])
limits_vs_mass3.append(["L350TeV_Ctau200cm",   350.0, 503.4, 200.0,   0.00174708])
limits_vs_mass3.append(["L400TeV_Ctau200cm",   400.0, 576.4, 200.0,   0.000790256])
lifetime_limits_vs_mass3 = 200.0
list_limits_vs_mass.append([lifetime_limits_vs_mass3, limits_vs_mass3])

limits_vs_mass4 = []
limits_vs_mass4.append(["L100TeV_Ctau0_1cm",   100.0, 139.4, 0.1,   2.07166])
limits_vs_mass4.append(["L150TeV_Ctau0_1cm",   150.0, 212.1, 0.1,   0.233382])
limits_vs_mass4.append(["L200TeV_Ctau0_1cm",   200.0, 284.8, 0.1,   0.0428312])
limits_vs_mass4.append(["L300TeV_Ctau0_1cm",  300.0, 430.4, 0.1,  0.00418322])
limits_vs_mass4.append(["L350TeV_Ctau0_1cm",  350.0, 503.4, 0.1,  0.00172168])
limits_vs_mass4.append(["L400TeV_Ctau0_1cm",  400.0, 576.4, 0.1,  0.000798117])
lifetime_limits_vs_mass4 = 0.1
list_limits_vs_mass.append([lifetime_limits_vs_mass4, limits_vs_mass4])

limits_vs_mass5 = []
limits_vs_mass5.append(["L100TeV_Ctau10cm",   100.0, 139.4, 10.0,   2.07166])
limits_vs_mass5.append(["L150TeV_Ctau10cm",   150.0, 212.1, 10.0,   0.23281])
limits_vs_mass5.append(["L200TeV_Ctau10cm",   200.0, 284.8, 10.0,   0.0428512])
limits_vs_mass5.append(["L250TeV_Ctau10cm",   250.0, 357.5, 10.0,   0.0118188])
limits_vs_mass5.append(["L300TeV_Ctau10cm",  300.0, 430.4, 10.0,  0.00413536])
limits_vs_mass5.append(["L350TeV_Ctau10cm",  350.0, 503.4, 10.0,  0.00172168])
limits_vs_mass5.append(["L400TeV_Ctau10cm",  400.0, 576.4, 10.0,  0.000790256])
lifetime_limits_vs_mass5 = 10.0
list_limits_vs_mass.append([lifetime_limits_vs_mass5, limits_vs_mass5])

limits_vs_mass6 = []
limits_vs_mass6.append(["L100TeV_Ctau400cm",   100.0, 139.4, 400.0,   2.07166])
limits_vs_mass6.append(["L150TeV_Ctau400cm",   150.0, 212.1, 400.0,   0.23555])
limits_vs_mass6.append(["L200TeV_Ctau400cm",   200.0, 284.8, 400.0,   0.0424614])
limits_vs_mass6.append(["L250TeV_Ctau400cm",   250.0, 357.5, 400.0,   0.0118048])
limits_vs_mass6.append(["L300TeV_Ctau400cm",   300.0, 430.4, 400.0,  0.00418529])
limits_vs_mass6.append(["L350TeV_Ctau400cm",   350.0, 503.4, 400.0,   0.00174708])
limits_vs_mass6.append(["L400TeV_Ctau400cm",   400.0, 576.4, 400.0,   0.000790256])
lifetime_limits_vs_mass6 = 400.0
list_limits_vs_mass.append([lifetime_limits_vs_mass6, limits_vs_mass6])

limits_vs_mass7 = []
#limits_vs_mass7.append(["L150TeV_Ctau800cm",   150.0, 212.1, 800.0,   0.23555])
limits_vs_mass7.append(["L200TeV_Ctau800cm",   200.0, 284.8, 800.0,   0.0424614])
limits_vs_mass7.append(["L250TeV_Ctau800cm",   250.0, 357.5, 800.0,   0.0118048])
limits_vs_mass7.append(["L300TeV_Ctau800cm",   300.0, 430.4, 800.0,  0.00418529])
limits_vs_mass7.append(["L350TeV_Ctau800cm",   350.0, 503.4, 800.0,   0.00174708])
limits_vs_mass7.append(["L400TeV_Ctau800cm",   400.0, 576.4, 800.0,   0.000790256])
lifetime_limits_vs_mass7 = 800.0
list_limits_vs_mass.append([lifetime_limits_vs_mass7, limits_vs_mass7])

limits_vs_mass8 = []
limits_vs_mass8.append(["L100TeV_Ctau1000cm",   100.0, 139.4, 1000.0,   2.07166])
limits_vs_mass8.append(["L150TeV_Ctau1000cm",   150.0, 212.1, 1000.0,   0.23555])
#limits_vs_mass8.append(["L200TeV_Ctau1000cm",   200.0, 284.8, 1000.0,   0.0424614])
limits_vs_mass8.append(["L250TeV_Ctau1000cm",   250.0, 357.5, 1000.0,   0.0118048])
limits_vs_mass8.append(["L300TeV_Ctau1000cm",   300.0, 430.4, 1000.0,  0.00418529])
limits_vs_mass8.append(["L350TeV_Ctau1000cm",   350.0, 503.4, 1000.0,   0.00174708])
limits_vs_mass8.append(["L400TeV_Ctau1000cm",   400.0, 576.4, 1000.0,   0.000790256])
lifetime_limits_vs_mass8 = 1000.0
list_limits_vs_mass.append([lifetime_limits_vs_mass8, limits_vs_mass8])


exclusion_region_2D = []
exclusion_region_2D.append(["L100TeV_Ctau0_1cm", 100.0, 139.4, 0.1, 2.07166])
exclusion_region_2D.append(["L100TeV_Ctau10cm", 100.0, 139.4, 10.0, 2.07166])
exclusion_region_2D.append(["L100TeV_Ctau200cm", 100.0, 139.4, 200.0, 2.08663])
exclusion_region_2D.append(["L100TeV_Ctau400cm", 100.0, 139.4, 400.0, 2.08663])
#exclusion_region_2D.append(["L100TeV_Ctau600cm", 100.0, 139.4, 600.0, 2.08663])
exclusion_region_2D.append(["L100TeV_Ctau1000cm", 100.0, 139.4, 1000.0, 2.08663])
exclusion_region_2D.append(["L100TeV_Ctau1200cm", 100.0, 139.4, 1200.0, 2.09996])
exclusion_region_2D.append(["L150TeV_Ctau0_1cm",   150.0, 212.1, 0.1,   0.233382])
exclusion_region_2D.append(["L150TeV_Ctau10cm",   150.0, 212.1, 10.0,   0.23281])
exclusion_region_2D.append(["L150TeV_Ctau200cm",   150.0, 212.1, 200.0,   0.23355])
exclusion_region_2D.append(["L150TeV_Ctau400cm",   150.0, 212.1, 400.0,   0.231478])
exclusion_region_2D.append(["L150TeV_Ctau600cm",   150.0, 212.1, 600.0,   0.234354])
#exclusion_region_2D.append(["L150TeV_Ctau800cm",   150.0, 212.1, 800.0,   0.230648])
exclusion_region_2D.append(["L150TeV_Ctau1000cm",  150.0, 212.1, 1000.0,  0.233782])
exclusion_region_2D.append(["L200TeV_Ctau0_1cm",   200.0, 284.8, 0.1,   0.0428312])
exclusion_region_2D.append(["L200TeV_Ctau10cm",   200.0, 284.8, 10.0,   0.0428512])
exclusion_region_2D.append(["L200TeV_Ctau200cm",   200.0, 284.8, 200.0,   0.0424614])
exclusion_region_2D.append(["L200TeV_Ctau400cm",   200.0, 284.8, 400.0,   0.0427252])
exclusion_region_2D.append(["L200TeV_Ctau600cm",   200.0, 284.8, 600.0,   0.0431458])
exclusion_region_2D.append(["L200TeV_Ctau800cm",   200.0, 284.8, 800.0,   0.0423242])
#exclusion_region_2D.append(["L200TeV_Ctau1000cm",   200.0, 284.8, 1000.0,   0.042969])
exclusion_region_2D.append(["L200TeV_Ctau1200cm",   200.0, 284.8, 1200.0,   0.0422256])
exclusion_region_2D.append(["L250TeV_Ctau10cm",   250.0, 357.5, 10.0,   0.0118188])
exclusion_region_2D.append(["L250TeV_Ctau200cm",  250.0, 357.5, 200.0,  0.0118048])
exclusion_region_2D.append(["L250TeV_Ctau400cm",   250.0, 357.5, 400.0,   0.0115646])
exclusion_region_2D.append(["L250TeV_Ctau600cm",  250.0, 357.5, 600.0,  0.0116992])
exclusion_region_2D.append(["L250TeV_Ctau800cm",  250.0, 357.5, 800.0,  0.0116992])
exclusion_region_2D.append(["L250TeV_Ctau1000cm",  250.0, 357.5, 1000.0,  0.0116992])
exclusion_region_2D.append(["L250TeV_Ctau1200cm",  250.0, 357.5, 1200.0,  0.0116992])
exclusion_region_2D.append(["L300TeV_Ctau0_1cm",  300.0, 430.4, 0.1,  0.00418322])
exclusion_region_2D.append(["L300TeV_Ctau10cm",  300.0, 430.4, 10.0,  0.00413536])
exclusion_region_2D.append(["L300TeV_Ctau200cm",  300.0, 430.4, 200.0,  0.00418529])
exclusion_region_2D.append(["L300TeV_Ctau400cm",  300.0, 430.4, 400.0,  0.00418529])
exclusion_region_2D.append(["L300TeV_Ctau600cm",  300.0, 430.4, 600.0,  0.0041645])
exclusion_region_2D.append(["L300TeV_Ctau800cm",  300.0, 430.4, 800.0,  0.0041645])
exclusion_region_2D.append(["L300TeV_Ctau1000cm",  300.0, 430.4, 1000.0,  0.0041645])
exclusion_region_2D.append(["L300TeV_Ctau1200cm",  300.0, 430.4, 1200.0,  0.0041645])
exclusion_region_2D.append(["L350TeV_Ctau0_1cm",  350.0, 503.4, 0.1,  0.00172168])
exclusion_region_2D.append(["L350TeV_Ctau10cm",  350.0, 503.4, 10.0,  0.00172168])
exclusion_region_2D.append(["L350TeV_Ctau200cm",  350.0, 503.4, 200.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau400cm",  350.0, 503.4, 400.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau600cm",  350.0, 503.4, 600.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau800cm",  350.0, 503.4, 800.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau1000cm",  350.0, 503.4, 1000.0,  0.00174708])
exclusion_region_2D.append(["L350TeV_Ctau1200cm",  350.0, 503.4, 1200.0,  0.00174708])
exclusion_region_2D.append(["L400TeV_Ctau0_1cm",   400.0, 576.4, 0.1,   0.000798117])
exclusion_region_2D.append(["L400TeV_Ctau10cm",   400.0, 576.4, 10.0,   0.000798117])
exclusion_region_2D.append(["L400TeV_Ctau200cm",  400.0, 576.4, 200.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau400cm",  400.0, 576.4, 400.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau600cm",  400.0, 576.4, 600.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau800cm",  400.0, 576.4, 800.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau1000cm",  400.0, 576.4, 1000.0,  0.000793036])
exclusion_region_2D.append(["L400TeV_Ctau1200cm",  400.0, 576.4, 1200.0,  0.000793036])

grid_mass_exclusion_region_2D = [0.0, 139.4, 212.1, 284.8, 357.5, 430.4, 503.4, 576.4]
grid_lambda_exclusion_region_2D = [0.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0]
#grid_lifetime_exclusion_region_2D = [20000.0, 4000.0, 1200.0, 1000.0, 800.0, 600.0, 400.0, 200.0, 100.0, 60.0, 50.0, 25.0, 10.0, 5.0, 1.0, 0.5, 0.1, 0.01, 0.0]
grid_lifetime_exclusion_region_2D = [4000.0, 1200.0, 1000.0, 800.0, 600.0, 400.0, 200.0, 100.0, 50.0, 10.0, 5.0, 0.1, 0.01, 0.0]


#############################input files to skim script#####################

fileNameDataSkim = [
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_DoubleEG_2016B_ver1.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_DoubleEG_2016B_ver2.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_DoubleEG_2016C.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_DoubleEG_2016D.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_DoubleEG_2016E.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_DoubleEG_2016F.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_DoubleEG_2016G.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_DoubleEG_2016H.root'
		]

fileNameGJetsSkim = [
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]
fileNameQCDSkim = [
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/DelayedPhoton_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]	


fileNameSigSkim_this = ['/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root']

fileNameSigSkim = [
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L100TeV_Ctau0_1cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L100TeV_Ctau1000cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L100TeV_Ctau10cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L100TeV_Ctau1200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L100TeV_Ctau200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L100TeV_Ctau400cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L100TeV_Ctau600cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L150TeV_Ctau0_1cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L150TeV_Ctau1000cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L150TeV_Ctau10cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L150TeV_Ctau200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L150TeV_Ctau400cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L150TeV_Ctau600cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L150TeV_Ctau800cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau0_1cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau1000cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau10cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau1200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau400cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau600cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L200TeV_Ctau800cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L250TeV_Ctau1000cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L250TeV_Ctau10cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L250TeV_Ctau1200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L250TeV_Ctau200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L250TeV_Ctau400cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L250TeV_Ctau600cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L250TeV_Ctau800cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L300TeV_Ctau0_1cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L300TeV_Ctau1000cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L300TeV_Ctau10cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L300TeV_Ctau1200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L300TeV_Ctau200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L300TeV_Ctau400cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L300TeV_Ctau600cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L300TeV_Ctau800cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau0_1cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau1000cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau10cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau1200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau400cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau600cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L350TeV_Ctau800cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau0_1cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau1000cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau10cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau1200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau200cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau400cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau600cm_13TeV-pythia8.root',
		'/mnt/hadoop/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/orderByPt/withcut/GMSB_L400TeV_Ctau800cm_13TeV-pythia8.root'
		]
