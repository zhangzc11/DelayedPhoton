import os
import numpy as np

#logfiledir = '../scripts_condor/ABCD_cut_obsexp10/ABCD_2x2/log_noBDT_ABCD/'
logfiledir = '../scripts_condor/log_noBDT_ABCD_binAndDatacard/'

ctaus = ['10', '50', '100', '200', '400', '600', '800', '1000', '1200', '10000']
lambdas = ['100', '150', '200', '250', '300', '350', '400']


for idx1 in range(len(ctaus)):
	print ctaus[idx1],
	for idx2 in range(len(lambdas)):
		#print "grep time: "+logfiledir+"L"+lambdas[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm*.out"
		lines_time = os.popen("grep time: "+logfiledir+"L"+lambdas[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm*.out").read().split(',')
		lines_met = os.popen("grep met: "+logfiledir+"L"+lambdas[idx2]+"TeV_Ctau"+ctaus[idx1]+"cm*.out").read().split(',')
		if len(lines_time) > 1 and len(lines_met) > 1:
			print " & "+lines_time[1]+", "+lines_met[1],
		else:
			print " & -- ",
	print "\\\\"
