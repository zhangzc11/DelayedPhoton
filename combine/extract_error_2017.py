import os
import numpy as np

lambda_points = [100, 150, 200, 250, 300, 350, 400]
ctau_points = [0.001, 0.1, 10, 200, 400, 600, 800, 1000, 1200, 10000]

for ctau in ctau_points:
	ctaus = str(ctau)
	if ctaus == "0.001":
		ctaus = "0_001"
	if ctaus == "0.1":
		ctaus = "0_1"
	for lambd in lambda_points:
		lambds = str(lambd)
		os.system("grep none datacards/log/log_L"+lambds+"TeV_Ctau"+ctaus+"cm_2017.log > temp.log")
		NA = 1.0
		NA_err = 0.0
		x1 = 1.0
		y1 = 1.0
		x1_err = 0.0
		y1_err = 0.0
		with open("temp.log") as f:
			lines = f.readlines()
			if len(lines) < 4:
				continue
			line_NA_items = lines[0].strip('\n').split()
			line_x1_items = lines[2].strip('\n').split()
			line_y1_items = lines[1].strip('\n').split()
			NA = float(line_NA_items[2])
			x1 = float(line_x1_items[2])
			y1 = float(line_y1_items[2])
			NA_err = float(line_NA_items[4])
			x1_err = float(line_x1_items[4])
			y1_err = float(line_y1_items[4])
		
		print str(ctau)+", "+lambds+", "+str(NA)+" \\pm "+str(NA_err) + "(%.3f"%(NA_err/NA)+"), "+str(x1)+" \\pm "+str(x1_err) + "(%.3f"%(x1_err/x1)+"), "+str(y1)+" \\pm "+str(y1_err) + "(%.3f"%(y1_err/y1)+")"
