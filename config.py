########################################################
##common configuration parameters for all plot scripts##
########################################################

#######################input trees######################
fileNameData = '/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_DoubleEG_2016_All_GoodLumi.root'
fileNameGJets = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]
fileNameQCD = [
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
		'/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'
		]	
fileNameSig = '/eos/cms/store/group/phys_susy/razor/Run2Analysis/DelayedPhotonAnalysis/2016/V4p1_private_REMINIAOD/DelayedPhoton_GluinoToNeutralinoToGratinoPhoton_M1000_CTau500mm.root'

sigLegend = "#tilde{g}#rightarrow#tilde{#chi}_{1}^{0}#rightarrow#gamma#tilde{G} (500mm)"

################lumi and cross sections#################
lumi = 128.337 #35900 #pb^-1
xsecSig = 0.086*32.5 #pb, scaled from AN2011-081 based on gluino production xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections7TeVgluglu, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVgluglu
xsecGJets = [20790.0, 9238.0, 2305, 274.4, 93.46] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Gamma_jets
xsecQCD = [1712000, 347700, 32100, 6831, 1207, 119.9, 25.24] #pb, see: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD

###############cuts and outputs########################
cut = 'pho1Pt > 70 && abs(pho1Eta)<1.44 && pho1passIsoLoose && pho1passEleVeto && n_Jets > 2 && pho1Smajor>0.1'
outputDir = '/afs/cern.ch/user/z/zhicaiz/www/sharebox/DelayedPhoton/25Sept2017/'

############define the plot you want to make##########
plots = []
#variable name in the tree, output plot file name, description/title, Nbins, lowX, upX 
plots.append(["pho1Sminor", "Sminor", "S_{minor}", 50,0,1])
plots.append(["pho1Smajor", "Smajor", "S_{major}", 50,0,1])
plots.append(["nPV", "nPV", "number of vertices", 50,0,50])
plots.append(["n_Jets", "nJets", "number of jets", 15,0,15])
plots.append(["pho1Pt", "phoPt", "p_{T}^{#gamma} [GeV]", 100,0,2000])
plots.append(["pho1SeedTimeRaw", "phoTimeSeedRaw", "#gamma seed raw time [ns]", 50,-5,15])
plots.append(["pho1SeedTimeCalib", "phoTimeSeedCalib", "#gamma seed calibrated time [ns]", 50,-5,15])
plots.append(["pho1SeedTimeCalibTOF", "phoTimeSeedCalibTOF", "#gamma seed calibrated time & TOF [ns]", 50,-5,15])
plots.append(["pho1ClusterTime", "phoTimeCluster", "#gamma cluster time [ns]", 50,-5,15])
plots.append(["MET", "MET", "#slash{E}_{T} [GeV]", 100,0,1500])
plots.append(["pho1Sminor/pho1Smajor", "SminorOverSmajor", "S_{minor}/S_{major}", 50,0,1.1])
