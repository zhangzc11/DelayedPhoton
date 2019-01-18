
for Lambda in 100 150 200 250 300 350 400
do
	for Ctau in 0_001 0_1 10 200 400 600 800 1000 1200 10000
	do
		combineCards.py ch2J=../datacards_2J_noBDT/DelayedPhotonCard_L${Lambda}TeV_Ctau${Ctau}cm.txt ch3J=../datacards_3J_noBDT/DelayedPhotonCard_L${Lambda}TeV_Ctau${Ctau}cm.txt > DelayedPhotonCard_L${Lambda}TeV_Ctau${Ctau}cm.txt

		combine DelayedPhotonCard_L${Lambda}TeV_Ctau${Ctau}cm.txt -M Asymptotic -n L${Lambda}TeV_Ctau${Ctau}cm
	done
done
