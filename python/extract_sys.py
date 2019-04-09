import numpy as np

#lambda_points = [100, 200, 300]
#ctau_points = [10, 200, 1000]

lambda_points = [100, 150, 200, 250, 300, 350, 400]
ctau_points = [10, 200, 400, 600, 800, 1000, 1200, 10000]

phoScaleUp = np.zeros((4, len(lambda_points)*len(ctau_points)))
phoScaleUp_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
phoSmearUp = np.zeros((4, len(lambda_points)*len(ctau_points)))
phoSmearUp_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
JESUp = np.zeros((4, len(lambda_points)*len(ctau_points)))
JESUp_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeScaleUp = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeScaleUp_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeSmearUp = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeSmearUp_err = np.zeros((4, len(lambda_points)*len(ctau_points)))

phoScaleDown = np.zeros((4, len(lambda_points)*len(ctau_points)))
phoScaleDown_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
phoSmearDown = np.zeros((4, len(lambda_points)*len(ctau_points)))
phoSmearDown_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
JESDown = np.zeros((4, len(lambda_points)*len(ctau_points)))
JESDown_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeScaleDown = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeScaleDown_err = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeSmearDown = np.zeros((4, len(lambda_points)*len(ctau_points)))
timeSmearDown_err = np.zeros((4, len(lambda_points)*len(ctau_points)))


npoints = len(lambda_points)*len(ctau_points)
npoints_lambda = len(lambda_points)
npoints_ctau = len(ctau_points)

average_phoScaleUp_averageOverCtau = np.zeros(npoints_lambda)
average_phoScaleDown_averageOverCtau = np.zeros(npoints_lambda)
average_phoSmearUp_averageOverCtau = np.zeros(npoints_lambda)
average_phoSmearDown_averageOverCtau = np.zeros(npoints_lambda)
average_JESUp_averageOverCtau = np.zeros(npoints_lambda)
average_JESDown_averageOverCtau = np.zeros(npoints_lambda)
average_timeScaleUp_averageOverCtau = np.zeros(npoints_lambda)
average_timeScaleDown_averageOverCtau = np.zeros(npoints_lambda)
average_timeSmearUp_averageOverCtau = np.zeros(npoints_lambda)
average_timeSmearDown_averageOverCtau = np.zeros(npoints_lambda)

sumWeights_phoScaleUp_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_phoScaleDown_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_phoSmearUp_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_phoSmearDown_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_JESUp_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_JESDown_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_timeScaleUp_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_timeScaleDown_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_timeSmearUp_averageOverCtau = np.zeros(npoints_lambda)
sumWeights_timeSmearDown_averageOverCtau = np.zeros(npoints_lambda)

average_phoScaleUp_averageOverLambda = np.zeros(npoints_ctau)
average_phoScaleDown_averageOverLambda = np.zeros(npoints_ctau)
average_phoSmearUp_averageOverLambda = np.zeros(npoints_ctau)
average_phoSmearDown_averageOverLambda = np.zeros(npoints_ctau)
average_JESUp_averageOverLambda = np.zeros(npoints_ctau)
average_JESDown_averageOverLambda = np.zeros(npoints_ctau)
average_timeScaleUp_averageOverLambda = np.zeros(npoints_ctau)
average_timeScaleDown_averageOverLambda = np.zeros(npoints_ctau)
average_timeSmearUp_averageOverLambda = np.zeros(npoints_ctau)
average_timeSmearDown_averageOverLambda = np.zeros(npoints_ctau)

sumWeights_phoScaleUp_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_phoScaleDown_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_phoSmearUp_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_phoSmearDown_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_JESUp_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_JESDown_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_timeScaleUp_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_timeScaleDown_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_timeSmearUp_averageOverLambda = np.zeros(npoints_ctau)
sumWeights_timeSmearDown_averageOverLambda = np.zeros(npoints_ctau)

npoints = 0
for ilamb in range(len(lambda_points)):
	lamb = lambda_points[ilamb]
	for ictau in range(len(ctau_points)):
		ctau = ctau_points[ictau]
		with open('../fit_results/2016ABCD/datacards_3J_noBDT/scaleSys_L'+str(lamb)+'TeV_Ctau'+str(ctau)+'cm.txt') as f:
			lines = f.readlines()
			for idx_line in range(len(lines)):
				line_items = lines[idx_line].strip('\n').split()
				print line_items
				phoScaleUp[idx_line][npoints] = float(line_items[1])	
				phoScaleUp_err[idx_line][npoints] = float(line_items[3])	
				phoScaleDown[idx_line][npoints] = float(line_items[4])	
				phoScaleDown_err[idx_line][npoints] = float(line_items[6])	
				phoSmearUp[idx_line][npoints] = float(line_items[7])	
				phoSmearUp_err[idx_line][npoints] = float(line_items[9])	
				phoSmearDown[idx_line][npoints] = float(line_items[10])	
				phoSmearDown_err[idx_line][npoints] = float(line_items[12])	
				JESUp[idx_line][npoints] = float(line_items[13])	
				JESUp_err[idx_line][npoints] = float(line_items[15])	
				JESDown[idx_line][npoints] = float(line_items[16])	
				JESDown_err[idx_line][npoints] = float(line_items[18])	
				timeScaleUp[idx_line][npoints] = float(line_items[19])	
				timeScaleUp_err[idx_line][npoints] = float(line_items[21])	
				timeScaleDown[idx_line][npoints] = float(line_items[22])	
				timeScaleDown_err[idx_line][npoints] = float(line_items[24])	
				timeSmearUp[idx_line][npoints] = float(line_items[25])	
				timeSmearUp_err[idx_line][npoints] = float(line_items[27])	
				timeSmearDown[idx_line][npoints] = float(line_items[28])	
				timeSmearDown_err[idx_line][npoints] = float(line_items[30])	
				
				average_phoScaleUp_averageOverCtau[ilamb] += abs(phoScaleUp[idx_line][npoints])/(phoScaleUp_err[idx_line][npoints]*phoScaleUp_err[idx_line][npoints])
				average_phoScaleDown_averageOverCtau[ilamb] += abs(phoScaleDown[idx_line][npoints])/(phoScaleDown_err[idx_line][npoints]*phoScaleDown_err[idx_line][npoints])
				average_phoSmearUp_averageOverCtau[ilamb] += abs(phoSmearUp[idx_line][npoints])/(phoSmearUp_err[idx_line][npoints]*phoSmearUp_err[idx_line][npoints])
				average_phoSmearDown_averageOverCtau[ilamb] += abs(phoSmearDown[idx_line][npoints])/(phoSmearDown_err[idx_line][npoints]*phoSmearDown_err[idx_line][npoints])
				average_JESUp_averageOverCtau[ilamb] += abs(JESUp[idx_line][npoints])/(JESUp_err[idx_line][npoints]*JESUp_err[idx_line][npoints])
				average_JESDown_averageOverCtau[ilamb] += abs(JESDown[idx_line][npoints])/(JESDown_err[idx_line][npoints]*JESDown_err[idx_line][npoints])
				average_timeScaleUp_averageOverCtau[ilamb] += abs(timeScaleUp[idx_line][npoints])/(timeScaleUp_err[idx_line][npoints]*timeScaleUp_err[idx_line][npoints])
				average_timeScaleDown_averageOverCtau[ilamb] += abs(timeScaleDown[idx_line][npoints])/(timeScaleDown_err[idx_line][npoints]*timeScaleDown_err[idx_line][npoints])
				average_timeSmearUp_averageOverCtau[ilamb] += abs(timeSmearUp[idx_line][npoints])/(timeSmearUp_err[idx_line][npoints]*timeSmearUp_err[idx_line][npoints])
				average_timeSmearDown_averageOverCtau[ilamb] += abs(timeSmearDown[idx_line][npoints])/(timeSmearDown_err[idx_line][npoints]*timeSmearDown_err[idx_line][npoints])
				
				sumWeights_phoScaleUp_averageOverCtau[ilamb] += 1.0/(phoScaleUp_err[idx_line][npoints]*phoScaleUp_err[idx_line][npoints])
				sumWeights_phoScaleDown_averageOverCtau[ilamb] += 1.0/(phoScaleDown_err[idx_line][npoints]*phoScaleDown_err[idx_line][npoints])
				sumWeights_phoSmearUp_averageOverCtau[ilamb] += 1.0/(phoSmearUp_err[idx_line][npoints]*phoSmearUp_err[idx_line][npoints])
				sumWeights_phoSmearDown_averageOverCtau[ilamb] += 1.0/(phoSmearDown_err[idx_line][npoints]*phoSmearDown_err[idx_line][npoints])
				sumWeights_JESUp_averageOverCtau[ilamb] += 1.0/(JESUp_err[idx_line][npoints]*JESUp_err[idx_line][npoints])
				sumWeights_JESDown_averageOverCtau[ilamb] += 1.0/(JESDown_err[idx_line][npoints]*JESDown_err[idx_line][npoints])
				sumWeights_timeScaleUp_averageOverCtau[ilamb] += 1.0/(timeScaleUp_err[idx_line][npoints]*timeScaleUp_err[idx_line][npoints])
				sumWeights_timeScaleDown_averageOverCtau[ilamb] += 1.0/(timeScaleDown_err[idx_line][npoints]*timeScaleDown_err[idx_line][npoints])
				sumWeights_timeSmearUp_averageOverCtau[ilamb] += 1.0/(timeSmearUp_err[idx_line][npoints]*timeSmearUp_err[idx_line][npoints])
				sumWeights_timeSmearDown_averageOverCtau[ilamb] += 1.0/(timeSmearDown_err[idx_line][npoints]*timeSmearDown_err[idx_line][npoints])
	
				average_phoScaleUp_averageOverLambda[ictau] += abs(phoScaleUp[idx_line][npoints])/(phoScaleUp_err[idx_line][npoints]*phoScaleUp_err[idx_line][npoints])
				average_phoScaleDown_averageOverLambda[ictau] += abs(phoScaleDown[idx_line][npoints])/(phoScaleDown_err[idx_line][npoints]*phoScaleDown_err[idx_line][npoints])
				average_phoSmearUp_averageOverLambda[ictau] += abs(phoSmearUp[idx_line][npoints])/(phoSmearUp_err[idx_line][npoints]*phoSmearUp_err[idx_line][npoints])
				average_phoSmearDown_averageOverLambda[ictau] += abs(phoSmearDown[idx_line][npoints])/(phoSmearDown_err[idx_line][npoints]*phoSmearDown_err[idx_line][npoints])
				average_JESUp_averageOverLambda[ictau] += abs(JESUp[idx_line][npoints])/(JESUp_err[idx_line][npoints]*JESUp_err[idx_line][npoints])
				average_JESDown_averageOverLambda[ictau] += abs(JESDown[idx_line][npoints])/(JESDown_err[idx_line][npoints]*JESDown_err[idx_line][npoints])
				average_timeScaleUp_averageOverLambda[ictau] += abs(timeScaleUp[idx_line][npoints])/(timeScaleUp_err[idx_line][npoints]*timeScaleUp_err[idx_line][npoints])
				average_timeScaleDown_averageOverLambda[ictau] += abs(timeScaleDown[idx_line][npoints])/(timeScaleDown_err[idx_line][npoints]*timeScaleDown_err[idx_line][npoints])
				average_timeSmearUp_averageOverLambda[ictau] += abs(timeSmearUp[idx_line][npoints])/(timeSmearUp_err[idx_line][npoints]*timeSmearUp_err[idx_line][npoints])
				average_timeSmearDown_averageOverLambda[ictau] += abs(timeSmearDown[idx_line][npoints])/(timeSmearDown_err[idx_line][npoints]*timeSmearDown_err[idx_line][npoints])
				
				sumWeights_phoScaleUp_averageOverLambda[ictau] += 1.0/(phoScaleUp_err[idx_line][npoints]*phoScaleUp_err[idx_line][npoints])
				sumWeights_phoScaleDown_averageOverLambda[ictau] += 1.0/(phoScaleDown_err[idx_line][npoints]*phoScaleDown_err[idx_line][npoints])
				sumWeights_phoSmearUp_averageOverLambda[ictau] += 1.0/(phoSmearUp_err[idx_line][npoints]*phoSmearUp_err[idx_line][npoints])
				sumWeights_phoSmearDown_averageOverLambda[ictau] += 1.0/(phoSmearDown_err[idx_line][npoints]*phoSmearDown_err[idx_line][npoints])
				sumWeights_JESUp_averageOverLambda[ictau] += 1.0/(JESUp_err[idx_line][npoints]*JESUp_err[idx_line][npoints])
				sumWeights_JESDown_averageOverLambda[ictau] += 1.0/(JESDown_err[idx_line][npoints]*JESDown_err[idx_line][npoints])
				sumWeights_timeScaleUp_averageOverLambda[ictau] += 1.0/(timeScaleUp_err[idx_line][npoints]*timeScaleUp_err[idx_line][npoints])
				sumWeights_timeScaleDown_averageOverLambda[ictau] += 1.0/(timeScaleDown_err[idx_line][npoints]*timeScaleDown_err[idx_line][npoints])
				sumWeights_timeSmearUp_averageOverLambda[ictau] += 1.0/(timeSmearUp_err[idx_line][npoints]*timeSmearUp_err[idx_line][npoints])
				sumWeights_timeSmearDown_averageOverLambda[ictau] += 1.0/(timeSmearDown_err[idx_line][npoints]*timeSmearDown_err[idx_line][npoints])



		npoints = npoints +1

average_phoScaleUp_all = 0.0
average_phoScaleDown_all = 0.0
average_phoSmearUp_all = 0.0
average_phoSmearDown_all = 0.0
average_phoScaleSmear = 0.0
average_JESUp_all = 0.0
average_JESDown_all = 0.0
average_JEC = 0.0
average_timeScaleUp_all = 0.0
average_timeScaleDown_all = 0.0
average_timeSmearUp_all = 0.0
average_timeSmearDown_all = 0.0
average_timeScaleSmear = 0.0

sumWeights_phoScaleUp_all = 0.0
sumWeights_phoScaleDown_all = 0.0
sumWeights_phoSmearUp_all = 0.0
sumWeights_phoSmearDown_all = 0.0
sumWeights_JESUp_all = 0.0
sumWeights_JESDown_all = 0.0
sumWeights_timeScaleUp_all = 0.0
sumWeights_timeScaleDown_all = 0.0
sumWeights_timeSmearUp_all = 0.0
sumWeights_timeSmearDown_all = 0.0

print "=================================================================="
print "===================average over all points========================="

for ip in range(npoints):
	for ich in range(4):
		average_phoScaleUp_all += 1.0/(phoScaleUp_err[ich][ip]*phoScaleUp_err[ich][ip])*abs(phoScaleUp[ich][ip])
		sumWeights_phoScaleUp_all += 1.0/(phoScaleUp_err[ich][ip]*phoScaleUp_err[ich][ip])		

		average_phoScaleDown_all += 1.0/(phoScaleDown_err[ich][ip]*phoScaleDown_err[ich][ip])*abs(phoScaleDown[ich][ip])
		sumWeights_phoScaleDown_all += 1.0/(phoScaleDown_err[ich][ip]*phoScaleDown_err[ich][ip])		
		
		average_phoSmearUp_all += 1.0/(phoSmearUp_err[ich][ip]*phoSmearUp_err[ich][ip])*abs(phoSmearUp[ich][ip])
		sumWeights_phoSmearUp_all += 1.0/(phoSmearUp_err[ich][ip]*phoSmearUp_err[ich][ip])		

		average_phoSmearDown_all += 1.0/(phoSmearDown_err[ich][ip]*phoSmearDown_err[ich][ip])*abs(phoSmearDown[ich][ip])
		sumWeights_phoSmearDown_all += 1.0/(phoSmearDown_err[ich][ip]*phoSmearDown_err[ich][ip])		

		average_JESUp_all += 1.0/(JESUp_err[ich][ip]*JESUp_err[ich][ip])*abs(JESUp[ich][ip])
		sumWeights_JESUp_all += 1.0/(JESUp_err[ich][ip]*JESUp_err[ich][ip])		

		average_JESDown_all += 1.0/(JESDown_err[ich][ip]*JESDown_err[ich][ip])*abs(JESDown[ich][ip])
		sumWeights_JESDown_all += 1.0/(JESDown_err[ich][ip]*JESDown_err[ich][ip])		

		average_timeScaleUp_all += 1.0/(timeScaleUp_err[ich][ip]*timeScaleUp_err[ich][ip])*abs(timeScaleUp[ich][ip])
		sumWeights_timeScaleUp_all += 1.0/(timeScaleUp_err[ich][ip]*timeScaleUp_err[ich][ip])		

		average_timeScaleDown_all += 1.0/(timeScaleDown_err[ich][ip]*timeScaleDown_err[ich][ip])*abs(timeScaleDown[ich][ip])
		sumWeights_timeScaleDown_all += 1.0/(timeScaleDown_err[ich][ip]*timeScaleDown_err[ich][ip])		
		
		average_timeSmearUp_all += 1.0/(timeSmearUp_err[ich][ip]*timeSmearUp_err[ich][ip])*abs(timeSmearUp[ich][ip])
		sumWeights_timeSmearUp_all += 1.0/(timeSmearUp_err[ich][ip]*timeSmearUp_err[ich][ip])		

		average_timeSmearDown_all += 1.0/(timeSmearDown_err[ich][ip]*timeSmearDown_err[ich][ip])*abs(timeSmearDown[ich][ip])
		sumWeights_timeSmearDown_all += 1.0/(timeSmearDown_err[ich][ip]*timeSmearDown_err[ich][ip])		

average_phoScaleSmear = (((average_phoScaleUp_all/sumWeights_phoScaleUp_all > average_phoScaleDown_all/sumWeights_phoScaleDown_all)*average_phoScaleUp_all/sumWeights_phoScaleUp_all + 	(average_phoScaleUp_all/sumWeights_phoScaleUp_all < average_phoScaleDown_all/sumWeights_phoScaleDown_all)*average_phoScaleDown_all/sumWeights_phoScaleDown_all)**2.0 + ((average_phoSmearUp_all/sumWeights_phoSmearUp_all > average_phoSmearDown_all/sumWeights_phoSmearDown_all)*average_phoSmearUp_all/sumWeights_phoSmearUp_all + (average_phoSmearUp_all/sumWeights_phoSmearUp_all < average_phoSmearDown_all/sumWeights_phoSmearDown_all)*average_phoSmearDown_all/sumWeights_phoSmearDown_all)**2.0)**0.5
average_timeScaleSmear = (((average_timeScaleUp_all/sumWeights_timeScaleUp_all > average_timeScaleDown_all/sumWeights_timeScaleDown_all)*average_timeScaleUp_all/sumWeights_timeScaleUp_all + 	(average_timeScaleUp_all/sumWeights_timeScaleUp_all < average_timeScaleDown_all/sumWeights_timeScaleDown_all)*average_timeScaleDown_all/sumWeights_timeScaleDown_all)**2.0 + ((average_timeSmearUp_all/sumWeights_timeSmearUp_all > average_timeSmearDown_all/sumWeights_timeSmearDown_all)*average_timeSmearUp_all/sumWeights_timeSmearUp_all + (average_timeSmearUp_all/sumWeights_timeSmearUp_all < average_timeSmearDown_all/sumWeights_timeSmearDown_all)*average_timeSmearDown_all/sumWeights_timeSmearDown_all)**2.0)**0.5
average_JEC = (average_JESUp_all/sumWeights_JESUp_all > average_JESDown_all/sumWeights_JESDown_all)*average_JESUp_all/sumWeights_JESUp_all + (average_JESUp_all/sumWeights_JESUp_all < average_JESDown_all/sumWeights_JESDown_all)*average_JESDown_all/sumWeights_JESDown_all

print "phoScaleUp : "+str(average_phoScaleUp_all/sumWeights_phoScaleUp_all)
print "phoScaleDown : "+str(average_phoScaleDown_all/sumWeights_phoScaleDown_all)
print "phoSmearUp : "+str(average_phoSmearUp_all/sumWeights_phoSmearUp_all)
print "phoSmearDown : "+str(average_phoSmearDown_all/sumWeights_phoSmearDown_all)
print "phoScaleSmear : "+str(average_phoScaleSmear)
print "JESUp : "+str(average_JESUp_all/sumWeights_JESUp_all)
print "JESDown : "+str(average_JESDown_all/sumWeights_JESDown_all)
print "JEC : "+str(average_JEC)
print "timeScaleUp : "+str(average_timeScaleUp_all/sumWeights_timeScaleUp_all)
print "timeScaleDown : "+str(average_timeScaleDown_all/sumWeights_timeScaleDown_all)
print "timeSmearUp : "+str(average_timeSmearUp_all/sumWeights_timeSmearUp_all)
print "timeSmearDown : "+str(average_timeSmearDown_all/sumWeights_timeSmearDown_all)
print "timeScaleSmear : "+str(average_timeScaleSmear)


print "=================================================================="
print "===================average over ctau========================="
print "lambda, phoScaleUp, phoScaleDown, phoSmearUp, phoSmearDown, phoScaleSmear, JESUp, JESDown, JEC, timeScaleUp, timeScaleDown, timeSmearUp, timeSmearDown, timeScaleSmear"
for ip in range(npoints_lambda):

	average_phoScaleSmear = (((average_phoScaleUp_averageOverCtau[ip]/sumWeights_phoScaleUp_averageOverCtau[ip] > average_phoScaleDown_averageOverCtau[ip]/sumWeights_phoScaleDown_averageOverCtau[ip])*average_phoScaleUp_averageOverCtau[ip]/sumWeights_phoScaleUp_averageOverCtau[ip] + 	(average_phoScaleUp_averageOverCtau[ip]/sumWeights_phoScaleUp_averageOverCtau[ip] < average_phoScaleDown_averageOverCtau[ip]/sumWeights_phoScaleDown_averageOverCtau[ip])*average_phoScaleDown_averageOverCtau[ip]/sumWeights_phoScaleDown_averageOverCtau[ip])**2.0 + ((average_phoSmearUp_averageOverCtau[ip]/sumWeights_phoSmearUp_averageOverCtau[ip] > average_phoSmearDown_averageOverCtau[ip]/sumWeights_phoSmearDown_averageOverCtau[ip])*average_phoSmearUp_averageOverCtau[ip]/sumWeights_phoSmearUp_averageOverCtau[ip] + (average_phoSmearUp_averageOverCtau[ip]/sumWeights_phoSmearUp_averageOverCtau[ip] < average_phoSmearDown_averageOverCtau[ip]/sumWeights_phoSmearDown_averageOverCtau[ip])*average_phoSmearDown_averageOverCtau[ip]/sumWeights_phoSmearDown_averageOverCtau[ip])**2.0)**0.5
	average_timeScaleSmear = (((average_timeScaleUp_averageOverCtau[ip]/sumWeights_timeScaleUp_averageOverCtau[ip] > average_timeScaleDown_averageOverCtau[ip]/sumWeights_timeScaleDown_averageOverCtau[ip])*average_timeScaleUp_averageOverCtau[ip]/sumWeights_timeScaleUp_averageOverCtau[ip] + 	(average_timeScaleUp_averageOverCtau[ip]/sumWeights_timeScaleUp_averageOverCtau[ip] < average_timeScaleDown_averageOverCtau[ip]/sumWeights_timeScaleDown_averageOverCtau[ip])*average_timeScaleDown_averageOverCtau[ip]/sumWeights_timeScaleDown_averageOverCtau[ip])**2.0 + ((average_timeSmearUp_averageOverCtau[ip]/sumWeights_timeSmearUp_averageOverCtau[ip] > average_timeSmearDown_averageOverCtau[ip]/sumWeights_timeSmearDown_averageOverCtau[ip])*average_timeSmearUp_averageOverCtau[ip]/sumWeights_timeSmearUp_averageOverCtau[ip] + (average_timeSmearUp_averageOverCtau[ip]/sumWeights_timeSmearUp_averageOverCtau[ip] < average_timeSmearDown_averageOverCtau[ip]/sumWeights_timeSmearDown_averageOverCtau[ip])*average_timeSmearDown_averageOverCtau[ip]/sumWeights_timeSmearDown_averageOverCtau[ip])**2.0)**0.5
	average_JEC = (average_JESUp_averageOverCtau[ip]/sumWeights_JESUp_averageOverCtau[ip] > average_JESDown_averageOverCtau[ip]/sumWeights_JESDown_averageOverCtau[ip])*average_JESUp_averageOverCtau[ip]/sumWeights_JESUp_averageOverCtau[ip] + (average_JESUp_averageOverCtau[ip]/sumWeights_JESUp_averageOverCtau[ip] < average_JESDown_averageOverCtau[ip]/sumWeights_JESDown_averageOverCtau[ip])*average_JESDown_averageOverCtau[ip]/sumWeights_JESDown_averageOverCtau[ip]
	print str(lambda_points[ip])+",    %4.2f,       %4.2f,         %4.2f,       %4.2f,          %4.2f,          %4.2f,    %4.2f,  %4.2f,       %4.2f,        %4.2f,        %4.2f,        %4.2f,       %4.2f"%(
		average_phoScaleUp_averageOverCtau[ip]/sumWeights_phoScaleUp_averageOverCtau[ip],
		average_phoScaleDown_averageOverCtau[ip]/sumWeights_phoScaleDown_averageOverCtau[ip],
		average_phoSmearUp_averageOverCtau[ip]/sumWeights_phoSmearUp_averageOverCtau[ip],
		average_phoSmearDown_averageOverCtau[ip]/sumWeights_phoSmearDown_averageOverCtau[ip],
		average_phoScaleSmear,
		average_JESUp_averageOverCtau[ip]/sumWeights_JESUp_averageOverCtau[ip],
		average_JESDown_averageOverCtau[ip]/sumWeights_JESDown_averageOverCtau[ip],
		average_JEC,
		average_timeScaleUp_averageOverCtau[ip]/sumWeights_timeScaleUp_averageOverCtau[ip],
		average_timeScaleDown_averageOverCtau[ip]/sumWeights_timeScaleDown_averageOverCtau[ip],
		average_timeSmearUp_averageOverCtau[ip]/sumWeights_timeSmearUp_averageOverCtau[ip],
		average_timeSmearDown_averageOverCtau[ip]/sumWeights_timeSmearDown_averageOverCtau[ip],
		average_timeScaleSmear
		)


print "=================================================================="
print "===================average over lambda========================="
print "ctau, phoScaleUp, phoScaleDown, phoSmearUp, phoSmearDown, phoScaleSmear, JESUp, JESDown, JEC, timeScaleUp, timeScaleDown, timeSmearUp, timeSmearDown, timeScaleSmear"
for ip in range(npoints_ctau):
	average_phoScaleSmear = (((average_phoScaleUp_averageOverLambda[ip]/sumWeights_phoScaleUp_averageOverLambda[ip] > average_phoScaleDown_averageOverLambda[ip]/sumWeights_phoScaleDown_averageOverLambda[ip])*average_phoScaleUp_averageOverLambda[ip]/sumWeights_phoScaleUp_averageOverLambda[ip] + 	(average_phoScaleUp_averageOverLambda[ip]/sumWeights_phoScaleUp_averageOverLambda[ip] < average_phoScaleDown_averageOverLambda[ip]/sumWeights_phoScaleDown_averageOverLambda[ip])*average_phoScaleDown_averageOverLambda[ip]/sumWeights_phoScaleDown_averageOverLambda[ip])**2.0 + ((average_phoSmearUp_averageOverLambda[ip]/sumWeights_phoSmearUp_averageOverLambda[ip] > average_phoSmearDown_averageOverLambda[ip]/sumWeights_phoSmearDown_averageOverLambda[ip])*average_phoSmearUp_averageOverLambda[ip]/sumWeights_phoSmearUp_averageOverLambda[ip] + (average_phoSmearUp_averageOverLambda[ip]/sumWeights_phoSmearUp_averageOverLambda[ip] < average_phoSmearDown_averageOverLambda[ip]/sumWeights_phoSmearDown_averageOverLambda[ip])*average_phoSmearDown_averageOverLambda[ip]/sumWeights_phoSmearDown_averageOverLambda[ip])**2.0)**0.5
	average_timeScaleSmear = (((average_timeScaleUp_averageOverLambda[ip]/sumWeights_timeScaleUp_averageOverLambda[ip] > average_timeScaleDown_averageOverLambda[ip]/sumWeights_timeScaleDown_averageOverLambda[ip])*average_timeScaleUp_averageOverLambda[ip]/sumWeights_timeScaleUp_averageOverLambda[ip] + 	(average_timeScaleUp_averageOverLambda[ip]/sumWeights_timeScaleUp_averageOverLambda[ip] < average_timeScaleDown_averageOverLambda[ip]/sumWeights_timeScaleDown_averageOverLambda[ip])*average_timeScaleDown_averageOverLambda[ip]/sumWeights_timeScaleDown_averageOverLambda[ip])**2.0 + ((average_timeSmearUp_averageOverLambda[ip]/sumWeights_timeSmearUp_averageOverLambda[ip] > average_timeSmearDown_averageOverLambda[ip]/sumWeights_timeSmearDown_averageOverLambda[ip])*average_timeSmearUp_averageOverLambda[ip]/sumWeights_timeSmearUp_averageOverLambda[ip] + (average_timeSmearUp_averageOverLambda[ip]/sumWeights_timeSmearUp_averageOverLambda[ip] < average_timeSmearDown_averageOverLambda[ip]/sumWeights_timeSmearDown_averageOverLambda[ip])*average_timeSmearDown_averageOverLambda[ip]/sumWeights_timeSmearDown_averageOverLambda[ip])**2.0)**0.5
	average_JEC = (average_JESUp_averageOverLambda[ip]/sumWeights_JESUp_averageOverLambda[ip] > average_JESDown_averageOverLambda[ip]/sumWeights_JESDown_averageOverLambda[ip])*average_JESUp_averageOverLambda[ip]/sumWeights_JESUp_averageOverLambda[ip] + (average_JESUp_averageOverLambda[ip]/sumWeights_JESUp_averageOverLambda[ip] < average_JESDown_averageOverLambda[ip]/sumWeights_JESDown_averageOverLambda[ip])*average_JESDown_averageOverLambda[ip]/sumWeights_JESDown_averageOverLambda[ip]
	print str(ctau_points[ip])+",    %4.2f,       %4.2f,         %4.2f,       %4.2f,          %4.2f,          %4.2f,   %4.2f,  %4.2f,      %4.2f,        %4.2f,        %4.2f,         %4.2f,       %4.2f"%(
		average_phoScaleUp_averageOverLambda[ip]/sumWeights_phoScaleUp_averageOverLambda[ip],
		average_phoScaleDown_averageOverLambda[ip]/sumWeights_phoScaleDown_averageOverLambda[ip],
		average_phoSmearUp_averageOverLambda[ip]/sumWeights_phoSmearUp_averageOverLambda[ip],
		average_phoSmearDown_averageOverLambda[ip]/sumWeights_phoSmearDown_averageOverLambda[ip],
		average_phoScaleSmear,
		average_JESUp_averageOverLambda[ip]/sumWeights_JESUp_averageOverLambda[ip],
		average_JESDown_averageOverLambda[ip]/sumWeights_JESDown_averageOverLambda[ip],
		average_JEC,
		average_timeScaleUp_averageOverLambda[ip]/sumWeights_timeScaleUp_averageOverLambda[ip],
		average_timeScaleDown_averageOverLambda[ip]/sumWeights_timeScaleDown_averageOverLambda[ip],
		average_timeSmearUp_averageOverLambda[ip]/sumWeights_timeSmearUp_averageOverLambda[ip],
		average_timeSmearDown_averageOverLambda[ip]/sumWeights_timeSmearDown_averageOverLambda[ip],
		average_timeScaleSmear
		)


