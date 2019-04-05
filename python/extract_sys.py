import numpy as np

lambda_points = [100, 200, 300]
ctau_points = [10, 200, 1000]

phoScaleUp = np.zeros((4, len(lambda_points)*len(ctau_points)))
phoScaleUp_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
JESUp = np.zeros((4, len(lambda_points)*len(ctau_points)))
JESUp_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeCorrUp = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeCorrUp_err = np.zeros((4, len(lambda_points)*len(ctau_points)))

phoScaleDown = np.zeros((4, len(lambda_points)*len(ctau_points)))
phoScaleDown_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
JESDown = np.zeros((4, len(lambda_points)*len(ctau_points)))
JESDown_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeCorrDown = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeCorrDown_err = np.zeros((4, len(lambda_points)*len(ctau_points)))

npoints = 0
for lamb in lambda_points:
	for ctau in ctau_points:
		with open('../fit_results/2016ABCD/datacards_3J_noBDT/scaleSys_L'+str(lamb)+'TeV_Ctau'+str(ctau)+'cm.txt') as f:
			lines = f.readlines()
			for idx_line in range(len(lines)):
				line_items = lines[idx_line].strip('\n').split()
				print line_items
				phoScaleUp[idx_line][npoints] = float(line_items[1])	
				phoScaleUp_err[idx_line][npoints] = float(line_items[3])	
				phoScaleDown[idx_line][npoints] = float(line_items[4])	
				phoScaleDown_err[idx_line][npoints] = float(line_items[6])	
				JESUp[idx_line][npoints] = float(line_items[7])	
				JESUp_err[idx_line][npoints] = float(line_items[9])	
				JESDown[idx_line][npoints] = float(line_items[10])	
				JESDown_err[idx_line][npoints] = float(line_items[12])	
				timeCorrUp[idx_line][npoints] = float(line_items[13])	
				timeCorrUp_err[idx_line][npoints] = float(line_items[15])	
				timeCorrDown[idx_line][npoints] = float(line_items[16])	
				timeCorrDown_err[idx_line][npoints] = float(line_items[18])	
		npoints = npoints +1

average_phoScaleUp = np.zeros(4)
average_phoScaleDown = np.zeros(4)
average_JESUp = np.zeros(4)
average_JESDown = np.zeros(4)
average_timeCorrUp = np.zeros(4)
average_timeCorrDown = np.zeros(4)

sumWeights_phoScaleUp = np.zeros(4)
sumWeights_phoScaleDown = np.zeros(4)
sumWeights_JESUp = np.zeros(4)
sumWeights_JESDown = np.zeros(4)
sumWeights_timeCorrUp = np.zeros(4)
sumWeights_timeCorrDown = np.zeros(4)


npoints = len(lambda_points)*len(ctau_points)

for ip in range(npoints):
	for ich in range(4):
		average_phoScaleUp[ich] += 1.0/(phoScaleUp_err[ich][ip]*phoScaleUp_err[ich][ip])*abs(phoScaleUp[ich][ip])
		sumWeights_phoScaleUp[ich] += 1.0/(phoScaleUp_err[ich][ip]*phoScaleUp_err[ich][ip])		

		average_phoScaleDown[ich] += 1.0/(phoScaleDown_err[ich][ip]*phoScaleDown_err[ich][ip])*abs(phoScaleDown[ich][ip])
		sumWeights_phoScaleDown[ich] += 1.0/(phoScaleDown_err[ich][ip]*phoScaleDown_err[ich][ip])		

		average_JESUp[ich] += 1.0/(JESUp_err[ich][ip]*JESUp_err[ich][ip])*abs(JESUp[ich][ip])
		sumWeights_JESUp[ich] += 1.0/(JESUp_err[ich][ip]*JESUp_err[ich][ip])		

		average_JESDown[ich] += 1.0/(JESDown_err[ich][ip]*JESDown_err[ich][ip])*abs(JESDown[ich][ip])
		sumWeights_JESDown[ich] += 1.0/(JESDown_err[ich][ip]*JESDown_err[ich][ip])		

		average_timeCorrUp[ich] += 1.0/(timeCorrUp_err[ich][ip]*timeCorrUp_err[ich][ip])*abs(timeCorrUp[ich][ip])
		sumWeights_timeCorrUp[ich] += 1.0/(timeCorrUp_err[ich][ip]*timeCorrUp_err[ich][ip])		

		average_timeCorrDown[ich] += 1.0/(timeCorrDown_err[ich][ip]*timeCorrDown_err[ich][ip])*abs(timeCorrDown[ich][ip])
		sumWeights_timeCorrDown[ich] += 1.0/(timeCorrDown_err[ich][ip]*timeCorrDown_err[ich][ip])		


average_phoScaleUp_all = 0.0
average_phoScaleDown_all = 0.0
average_JESUp_all = 0.0
average_JESDown_all = 0.0
average_timeCorrUp_all = 0.0
average_timeCorrDown_all = 0.0

sumWeights_phoScaleUp_all = 0.0
sumWeights_phoScaleDown_all = 0.0
sumWeights_JESUp_all = 0.0
sumWeights_JESDown_all = 0.0
sumWeights_timeCorrUp_all = 0.0
sumWeights_timeCorrDown_all = 0.0

print "=================================================================="
for ich in range(4):
	print "======================"
	print "channel "+str(ich)
	print "phoScaleUp: "+str(average_phoScaleUp[ich]/sumWeights_phoScaleUp[ich])
	print "phoScaleDown: "+str(average_phoScaleDown[ich]/sumWeights_phoScaleDown[ich])
	print "JESUp: "+str(average_JESUp[ich]/sumWeights_JESUp[ich])
	print "JESDown: "+str(average_JESDown[ich]/sumWeights_JESDown[ich])
	print "timeCorrUp: "+str(average_timeCorrUp[ich]/sumWeights_timeCorrUp[ich])
	print "timeCorrDown: "+str(average_timeCorrDown[ich]/sumWeights_timeCorrDown[ich])
	
	average_phoScaleUp_all += average_phoScaleUp[ich]
	sumWeights_phoScaleUp_all += sumWeights_phoScaleUp[ich]
	average_phoScaleDown_all += average_phoScaleDown[ich]
	sumWeights_phoScaleDown_all += sumWeights_phoScaleDown[ich]

	average_JESUp_all += average_JESUp[ich]
	sumWeights_JESUp_all += sumWeights_JESUp[ich]
	average_JESDown_all += average_JESDown[ich]
	sumWeights_JESDown_all += sumWeights_JESDown[ich]

	average_timeCorrUp_all += average_timeCorrUp[ich]
	sumWeights_timeCorrUp_all += sumWeights_timeCorrUp[ich]
	average_timeCorrDown_all += average_timeCorrDown[ich]
	sumWeights_timeCorrDown_all += sumWeights_timeCorrDown[ich]


print "=================================================================="
print "average over all channels"

print "phoScaleUp : "+str(average_phoScaleUp_all/sumWeights_phoScaleUp_all)
print "phoScaleDown : "+str(average_phoScaleDown_all/sumWeights_phoScaleDown_all)

print "JESUp : "+str(average_JESUp_all/sumWeights_JESUp_all)
print "JESDown : "+str(average_JESDown_all/sumWeights_JESDown_all)

print "timeCorrUp : "+str(average_timeCorrUp_all/sumWeights_timeCorrUp_all)
print "timeCorrDown : "+str(average_timeCorrDown_all/sumWeights_timeCorrDown_all)


