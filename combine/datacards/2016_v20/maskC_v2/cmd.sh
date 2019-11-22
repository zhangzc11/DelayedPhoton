
combineCards.py DelayedPhotonCard_L300TeV_Ctau200cm.txt -S > DelayedPhotonCard_L300TeV_Ctau200cm_S.txt
text2workspace.py DelayedPhotonCard_L300TeV_Ctau200cm_S.txt --channel-masks
combine -M FitDiagnostics DelayedPhotonCard_L300TeV_Ctau200cm_S.root --setParameters mask_ch1_ch11=1 -n L300_Ctau200cm

combineCards.py DelayedPhotonCard_L350TeV_Ctau200cm.txt -S > DelayedPhotonCard_L350TeV_Ctau200cm_S.txt
text2workspace.py DelayedPhotonCard_L350TeV_Ctau200cm_S.txt --channel-masks
combine -M FitDiagnostics DelayedPhotonCard_L350TeV_Ctau200cm_S.root --setParameters mask_ch1_ch11=1 -n L350_Ctau200cm
