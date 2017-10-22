########################################################
##common configuration parameters for all plot scripts##
########################################################

#######################input trees######################
fileNameData = '/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_DoubleEG_2016BCDEFGH_GoodLumi_31p389ifb.root'
fileNameGJets = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]
fileNameQCD = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]	
fileNameSig = '/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_GluinoToNeutralinoToGratinoPhoton_M1000_CTau500mm.root'
sigLegend = "signal (M1000-CTau500)"
#fileNameSig = '/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/skim/DelayedPhoton_GMSB_CTau2190mm.root'
#sigLegend = "GMSB (2190mm)"

################lumi and cross sections#################
lumi = 31389.2 #35900 #pb^-1
xsecSig = 0.086*32.5 #pb, scaled from AN2011-081 based on gluino production xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections7TeVgluglu, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVgluglu
xsecGJets = [20790.0, 9238.0, 2305, 274.4, 93.46] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Gamma_jets
xsecQCD = [1712000, 347700, 32100, 6831, 1207, 119.9, 25.24] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
fractionGJets = 0.4025 # from fit to SigmaIetaIeta
fractionQCD = 0.5975 # from fit fo SigmaIetaIeta
useFraction = True
scaleBkg = 1.0

###############cuts and outputs########################
#cut = 'pho1Pt > 100 && abs(pho1Eta)<1.44 && pho1passIsoMedium && pho1passEleVeto && n_Jets > 2 && pho1Smajor>0.1'
#cut = 'pho1Pt > 100 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Smajor>0.1 && pho1Sminor>0.1 && pho1Sminor<0.53 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0'
#cut = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Smajor>0.1 && pho1Sminor>0.1 && pho1Sminor<0.53 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2'
cut = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2'
cut_iso = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2 && pho1sumChargedHadronPt < 1.30 && pho1sumNeutralHadronEt < 0.26 && pho1sumPhotonEt < 2.36'

cut_QCD_shape_iso = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && (!pho1isPromptPhoton) && pho1sumChargedHadronPt < 1.30 && pho1sumNeutralHadronEt < 0.26 && pho1sumPhotonEt < 2.36'
cut_QCD_shape = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && (!pho1isPromptPhoton)'
#cut_QCD_shape = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && (!pho1isPromptPhoton)'
#cut_QCD_shape = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && (HLTDecision[81] == 1) && (!pho1isPromptPhoton)'

cut_GJets_shape_iso = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && pho1isPromptPhoton && pho1sumChargedHadronPt < 1.30 && pho1sumNeutralHadronEt < 0.26 && pho1sumPhotonEt < 2.36'
cut_GJets_shape = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && pho1isPromptPhoton'

cut_loose = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.7 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2'
cut_GJets = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoTight && pho1passEleVeto && n_Jets > 2 && pho1Sminor>0.15 && pho1Sminor<0.3 && ((pho1sumNeutralHadronEt/pho1Pt+pho1HoverE)*pho1E) < 6.0 && (HLTDecision[81] == 1) && n_Photons == 2 && (jet1Pt/pho1Pt > 0.6) && (jet1Pt/pho1Pt < 1.4) && (jet2Pt/pho1Pt > 0.2) && (abs(jet1Phi - pho1Phi) > 2.09) && (abs(jet1Phi - pho1Phi) < 4.18)'
cut_skim = "pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto && n_Jets >= 2 && (HLTDecision[81] == 1 || HLTDecision[100] == 1 || HLTDecision[102]==1 || HLTDecision[92] == 1 || HLTDecision[93] == 1)"
cut_skim_QCD = "pho1Pt > 40 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto && (HLTDecision[81] == 1 || HLTDecision[100] == 1 || HLTDecision[102]==1 || HLTDecision[92] == 1 || HLTDecision[93] == 1)"
outputDir = '/afs/cern.ch/user/z/zhicaiz/www/sharebox/DelayedPhoton/22Oct2017/'

############define the plot you want to make##########
##for stack plots
xbins_MET = [0.0, 10.0, 20.0, 40.0, 60.0, 80, 100.0, 125.0, 150.0, 175.0, 200.0, 250.0, 300.0, 400.0, 500.0, 1000.0]
xbins_time = [-15, -10, -5, -4, -3, -2.5, -2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3, 4, 5, 10, 15]

splots = []
#variable name in the tree, output plot file name, description/title, Nbins, lowX, upX, useLogy
splots.append(["pho1sumChargedHadronPt", "phosumChargedHadronPt_linear", "charged isolation [GeV]", 100,-0.1,1.30, False])
splots.append(["pho1sumChargedHadronPt", "phosumChargedHadronPt_log", "charged isolation [GeV]", 100,-0.1,1.30, True])
splots.append(["pho1sigmaEOverE", "phosigmaEOverE_linear", "#sigma_{E}/E", 100,0.,0.5, False])
splots.append(["pho1sigmaEOverE", "phosigmaEOverE_log", "#sigma_{E}/E", 100,0.,0.5, True])

splots.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta_linear", "#sigma_{i#eta i#eta}", 100,0.005,0.025, False])
splots.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta_log", "#sigma_{i#eta i#eta}", 100,0.005,0.025, True])

splots.append(["pho1ClusterTime", "phoTimeCluster_linear", "#gamma cluster time [ns]", 100,-15,15, False])
splots.append(["pho1ClusterTime", "phoTimeCluster_log", "#gamma cluster time [ns]", 100,-15,15, True])
splots.append(["MET", "MET_linear", "#slash{E}_{T} [GeV]", 100,0,800, False])
splots.append(["MET", "MET_log", "#slash{E}_{T} [GeV]", 100,0,800, True])
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
splots.append(["pho1Sminor/pho1Smajor", "SminorOverSmajor_linear", "S_{minor}/S_{major}", 50,0,1.1, False])
splots.append(["pho1Sminor/pho1Smajor", "SminorOverSmajor_log", "S_{minor}/S_{major}", 50,0,1.1, True])
splots.append(["sqrt(pho1Sminor)/sqrt(pho1Smajor)", "SminorSqrtOverSmajorSqrt_linear", "#sqrt{S_{minor}}/#sqrt{S_{major}}", 50,0,1.1, False])
splots.append(["sqrt(pho1Sminor)/sqrt(pho1Smajor)", "SminorSqrtOverSmajorSqrt_log", "#sqrt{S_{minor}}/#sqrt{S_{major}}", 50,0,1.1, True])

############define the variables for which you want to save the bkg shape##########
shapes = []
shapes.append(["pho1sumChargedHadronPt", "phosumChargedHadronPt", "charged isolation [GeV]", 100,-0.1,1.30])
shapes.append(["pho1SigmaIetaIeta", "phoSigmaIetaIeta", "#sigma_{i#eta i#eta}", 100,0.005,0.025])
shapes.append(["pho1sigmaEOverE", "phosigmaEOverE", "#sigma_{E}/E", 100,0.,0.5])
shapes.append(["pho1Smajor", "Smajor", "S_{major}", 100,0,1])
shapes.append(["pho1Sminor", "Sminor", "S_{minor}", 100,0,0.5])
shapes.append(["pho1Pt", "phoPt", "p_{T}^{#gamma} [GeV]", 100,50,1500])
shapes.append(["n_Jets", "nJets", "number of jets", 15,-0.5,14.5])


#####################limit plot settings####################################
limits_vs_lifetime = []
limits_vs_lifetime.append(["M1000GeV_CTau500mm", 500.0, 2.8])
limits_vs_lifetime.append(["M1000GeV_CTau500mm", 5000.0, 2.5])
mass_limits_vs_lifetime = 1000

#############################input files to skim script#####################

fileNameDataSkim = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_DoubleEG_2016B_ver1_GoodLumi.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_DoubleEG_2016B_ver2_GoodLumi.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_DoubleEG_2016C_GoodLumi.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_DoubleEG_2016D_GoodLumi.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_DoubleEG_2016E_GoodLumi.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_DoubleEG_2016F_GoodLumi.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_DoubleEG_2016G_GoodLumi.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_DoubleEG_2016H_GoodLumi.root'
		]

fileNameGJetsSkim = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]
fileNameQCDSkim = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]	
fileNameSigSkim = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_GluinoToNeutralinoToGratinoPhoton_M1000_CTau500mm.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_GluinoToNeutralinoToGratinoPhoton_M1000_CTau5000mm.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_NeutralinoNeutralinoToGravitinoGravitinoPhotonPhoton_M1000_CTau500mm.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_NeutralinoNeutralinoToGravitinoGravitinoPhotonPhoton_M1000_CTau5000mm.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/withcut/DelayedPhoton_GMSB_CTau2190mm.root'
		]
