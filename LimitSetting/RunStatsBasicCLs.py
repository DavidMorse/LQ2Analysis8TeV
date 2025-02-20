import os
import sys
import subprocess
import math 

import random
 #betas = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.41,0.42,0.43,0.44,0.45,0.46,0.47,0.48,0.49,0.5,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.6,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.7,0.71,0.72,0.73,0.74,0.75,0.76,0.77,0.78,0.79,0.8,0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,0.99999]
#betas = [.3,0.5]
#betas = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99]
betas = [0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.18,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,0.9995]
ESTIMATIONMETHOD = ' -M AsymptoticLimits '
METHOD = '-M HybridNew --rule CLs --frequentist CONFIGURATION --clsAcc=0 -s -1 -T 70 -i 70 --singlePoint SINGLEPOINT --saveToys --saveHybridResult'
person = (os.popen('whoami').readlines())[0].replace('\n','')

blind = False

masses = []
do_BetaOne = 0
do_BetaHalf = 0 
do_combo = 0
do_observedonly = 0
do_fullHybrid = 0

fullcardfile = 'FinalCardsLQ_2016.txt'
lqtype = 'LQ'
cdir = ''

if 'do_BetaOne' in str(sys.argv):
	do_BetaOne = 1
if 'do_BetaHalf' in str(sys.argv):
	do_BetaHalf = 1
if 'do_Combo' in str(sys.argv):
	do_combo = 1
if 'just_observed' in str(sys.argv):
	do_observedonly = 1	
if '--scalar' in sys.argv:
	lqtype = 'LQ'
if '--vectorAM' in sys.argv:
	lqtype = 'AM'
	fullcardfile = 'FinalCardsAM.txt'
if '--vectorYM' in sys.argv:
	lqtype = 'YM'
	fullcardfile = 'FinalCardsYM.txt'
if '--vectorMM' in sys.argv:
	lqtype = 'MM'
	fullcardfile = 'FinalCardsMM.txt'
if '--vectorMC' in sys.argv:
	lqtype = 'MC'		
	fullcardfile = 'FinalCardsMC.txt'
if '--susyRV' in sys.argv:
	lqtype = 'RV'		
	fullcardfile = 'FinalCardsRV.txt'
if '--displacedBL' in sys.argv or '--displacedBLMuEle' in sys.argv:
	lqtype = 'BL'
	fullcardfile = 'FinalCardsBLCTau'
	if '--displacedBLMuEle' in sys.argv:
		fullcardfile = 'combinedEleMu_BLCTau'

if '--doFullHybridCLs' in sys.argv:
	do_fullHybrid = 1



singlebeta = -1

numdo = 1	
queue = '1nd'
if 'CLSLimits' not in os.listdir('.'):
	os.system('mkdir CLSLimits')
if 'ShellScriptsForBatch' not in os.listdir('.'):
	os.system('mkdir ShellScriptsForBatch')

dobatch = True
for x in range(len(sys.argv)):
	if sys.argv[x] == '-c':
		cdir = sys.argv[x+1]

		os.system('mkdir CLSLimits/BetaOne'+cdir)
		os.system('mkdir CLSLimits/BetaHalf'+cdir)
		os.system('mkdir CLSLimits/Combo'+cdir)

	if sys.argv[x] == '-d':
		fullcardfile = sys.argv[x+1]
	if sys.argv[x] == '-n':
		numdo = int(sys.argv[x+1])
	if sys.argv[x] == '-q':
		queue = str(sys.argv[x+1])
	if sys.argv[x] == '--single_beta':
		singlebeta = float(sys.argv[x+1])
	if '--Asymptotic_Only' in sys.argv[x]:
		dobatch = False 
	if '--displacedBL' in sys.argv[x]:
		ctau = sys.argv[x+1]
		fullcardfile = fullcardfile+ctau+'.txt'
		print fullcardfile
	if '--displacedBLee' in sys.argv[x]:
		ctau = sys.argv[x+1]
		fullcardfile = 'datacard_rpv_apr6_ctau'+ctau+'.txt'
		print fullcardfile
	if '--cardFile' in sys.argv[x]:
		fullcardfile = sys.argv[x+1]
                
print 'Using cardfile:',fullcardfile


from ROOT import *
from array import array


if singlebeta>0:
	betas = []
	betas.append(singlebeta)
beta_combo = []
m_combo = []
dif_combo = []
cr = '  \n'

fullcards = open(fullcardfile,'r')
mycards = []
for line in fullcards:
	mycards.append((line.replace('\n','')).replace('\r',''))
digis = '0123456789'
name = []
for x in mycards:
	if '.txt' in x:
		name.append((x.replace('.txt','')).replace('\n','')) 
		mm = ''
		for a in x:
			if a in digis:
				mm += a
		if int(mm) not in masses:
			masses.append(int(mm))

BetaOneObs = []
BetaOne95down = []
BetaOne95up = []
BetaOne68down = []
BetaOne68up = []
BetaOneExp = []

BetaOneObsFreq = []
BetaOne95downFreq = []
BetaOne95upFreq = []
BetaOne68downFreq = []
BetaOne68upFreq = []
BetaOneExpFreq = []

BetaHalfObs = []
BetaHalf95down = []
BetaHalf95up = []
BetaHalf68down = []
BetaHalf68up = []
BetaHalfExp = []

ComboObs = []
Combo95down = []
Combo95up = []
Combo68down = []
Combo68up = []
ComboExp = []

ComboBetaOneObs = []
ComboBetaOne95down = []
ComboBetaOne68down = []
ComboBetaOneExp = []
ComboBetaOne68up = []
ComboBetaOne95up = []


ComboBetaHalfObs = []
ComboBetaHalf95down = []
ComboBetaHalf68down = []
ComboBetaHalfExp = []
ComboBetaHalf68up = []
ComboBetaHalf95up = []
						
if do_BetaOne == 1:
	masses_betaone = []

	for x in range(len(name)):
		if 'BetaHalf' in name[x]:
			continue
		print 'Calculating limit for: ' + name[x]
		f = open('CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg','w')
		count = 0
		#print name[x]

		for l in mycards:
			if '.txt' in l and name[x] in l and str(name[x]+'0') not in l:
				count = 1
				for m in masses:
					if str(m) in l and int(m) not in masses_betaone:
						masses_betaone.append(int(m))
			if '.txt' in l and name[x] not in l:
				count = 0


			if count ==1 and '.txt' not in l:
				f.write(l+'\n')
	

		f.close()

		os.system('mkdir CLSLimits/BetaOne'+cdir+'/'+name[x])

		mdir = (os.popen('pwd').readlines())[0]
		mdir = mdir.replace('\n','')
		fsub = open('ShellScriptsForBatch/subbetaone_'+cdir+name[x]+'.csh','w')
		fsub.write('#!/bin/csh'+ cr)
		fsub.write('cd ' + mdir+ cr)
		fsub.write('eval `scramv1 runtime -csh`'+ cr)
		fsub.write('cd -'+ cr)
		fsub.write('cp '+mdir+'/CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+ '.cfg . '+ cr)
		fsub.write('SUBCOMMAND'+'\n')
		fsub.close()
                #continue   # this is if you just want to make the individual cards for combination

		## Estimate the r values with Asymptotic CLs
		EstimationInformation = [' r < 0.000000']
		if 'LQ' in lqtype:
			if float(name[x].replace('LQ_M_',''))<900:
				rmax = float(name[x].replace('LQ_M_',''))/300.#fixme was 10000.0
			elif float(name[x].replace('LQ_M_',''))<1200:
				rmax = float(name[x].replace('LQ_M_',''))/100.#fixme was 10000.0
			elif float(name[x].replace('LQ_M_',''))<2000:
				rmax = float(name[x].replace('LQ_M_',''))/1.#fixme was 10000.0
			else:
				rmax = float(name[x].replace('LQ_M_',''))*5.#fixme was 10000.0
		if 'BL' in lqtype:
			rmax = float(name[x].replace('BLCTau'+ctau+'_M_',''))/60.#fixme was 10000.0
			if '1000' in ctau: rmax = 50000.0
		breaker = False
		ntry = 0 
		oldrmax = 100000.0

		while 'r < 0.000000' in str(EstimationInformation):
			ntry += 1
			rAbsAcc='.000005'
			print ('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg --expectSignal 1'+' --rMax '+str(rmax)+'  --rAbsAcc '+rAbsAcc)
			if blind:
				EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg  --expectSignal 1'+' --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc+' --run blind').readlines()
			else:
				EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg  --expectSignal 1'+' --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc).readlines()
			#print ('combine '+METHOD.replace('SINGLEPOINT',str(rmax)).replace('CONFIGURATION','CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg'))
			#EstimationInformation = os.popen('combine '+METHOD.replace('SINGLEPOINT',str(rmax)).replace('CONFIGURATION','CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg')).readlines()

                        #print EstimationInformation
			print 'finished combine'
			if abs(rmax - oldrmax)<.1*rmax:
				breaker=True		
				
			if breaker ==True:
				break

			effrmax = -999999
			for e in EstimationInformation:
				if 'r <'  in e and 'Expected' in e:
					thisrval = e.split('<')[-1]
					thisrval = thisrval.replace('\n','')
					thisrval = float(thisrval)
					if thisrval>effrmax:
						effrmax = thisrval

			oldrmax = float(rmax)

			if effrmax < 0:
				rmax = 0.6*rmax
			else:
				rmax = effrmax*2.0

			EstimationInformation = [' r < 0.000000']
			if ntry>100:
				breaker = True

		
		expectedlines = []
		for line in EstimationInformation:
			if 'Observed' in line and '<' in line: pass
			else: print line
			if 'Expected' in line and 'r <' in line:
				expectedlines.append(line.replace('\n',''))
		values = []
		for e in expectedlines:
			print e
			values.append(float(e.split()[-1]))
		
		## Fill the arrays of Asymptotic Values
		for line in EstimationInformation:
			if 'Observed' in line and '<' in line:
				BetaOneObs.append((line.split('<')[-1]).replace('\n',''))
				if not blind: print line
			if 'Expected' in line and '<' in line:
				if '2.5%' in line:
					BetaOne95down.append((line.split('<')[-1]).replace('\n',''))
				if '16.0%' in line:
					BetaOne68down.append((line.split('<')[-1]).replace('\n',''))
				if '50.0%' in line:
					BetaOneExp.append((line.split('<')[-1]).replace('\n',''))
				if '84.0%' in line:
					BetaOne68up.append((line.split('<')[-1]).replace('\n',''))
				if '97.5%' in line:
					BetaOne95up.append((line.split('<')[-1]).replace('\n',''))

		if do_fullHybrid == 1 :#and int(name[x].split('_')[-1])>475 : #do full Hybrid CLs

			values = []
			limitLines=[]
			absAcc='0.001'
			t='500'
			rMax=str(2.0*max(float(BetaOneObs[-1]),float(BetaOneExp[-1]),float(BetaOne68up[-1]),float(BetaOne95up[-1])))
			#if int(name[x].split('_')[-1])<625: 
			#	t='500'
			#	if int(name[x].split('_')[-1])<425: 
			#		rMax='0.1'
			#	if int(name[x].split('_')[-1])<325: 
			#		rMax='0.05'
			#rmax=5.0

			#print 'combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rRelAcc 0.01 -T '+t+' --expectedFromGrid 0.025'
			#EstimationInformationExpM2sigma = os.popen('combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rRelAcc 0.01 -T '+t+' --expectedFromGrid 0.025').readlines()
			print 'combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.025'
			EstimationInformationExpM2sigma = os.popen('combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.025').readlines()

			goForLimit = False
			for line in EstimationInformationExpM2sigma:
				print line
				if '-- Hybrid New --' in line:
					goForLimit = True
				if 'Limit' in line and 'r <' in line and '+/-' in line and 'CL' in line and goForLimit==True:
					BetaOne95downFreq.append(((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					limitLines.append(name[x])
					limitLines.append('Expected  2.5%: r <'+((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					values.append(float((line.split('<')[-1]).replace('\n','').split('+/-')[0]))

			print 'combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.16'
			EstimationInformationExpM1sigma = os.popen('combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.16').readlines()


			goForLimit = False
			for line in EstimationInformationExpM1sigma:
				print line
				if '-- Hybrid New --' in line:
					goForLimit = True
				if 'Limit' in line and 'r <' in line and '+/-' in line and 'CL' in line and goForLimit==True:
					BetaOne68downFreq.append(((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					limitLines.append('Expected 16.0%: r <'+((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					values.append(float((line.split('<')[-1]).replace('\n','').split('+/-')[0]))


			print 'combine -M ybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.5'
			EstimationInformationExpMed = os.popen('combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.5').readlines()

			goForLimit = False
			for line in EstimationInformationExpMed:
				print line
				if '-- Hybrid New --' in line:
					goForLimit = True
				if 'Limit' in line and 'r <' in line and '+/-' in line and 'CL' in line and goForLimit==True:
					BetaOneExpFreq.append(((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					limitLines.append('Expected 50.0%: r <'+((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					values.append(float((line.split('<')[-1]).replace('\n','').split('+/-')[0]))

			print 'combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.84'
			EstimationInformationExpP1sigma = os.popen('combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.84').readlines()


			goForLimit = False
			for line in EstimationInformationExpP1sigma:
				print line
				if '-- Hybrid New --' in line:
					goForLimit = True
				if 'Limit' in line and 'r <' in line and '+/-' in line and 'CL' in line and goForLimit==True:
					BetaOne68upFreq.append(((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					limitLines.append('Expected 84.0%: r <'+((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					values.append(float((line.split('<')[-1]).replace('\n','').split('+/-')[0]))


			print 'combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.975'
			EstimationInformationExpP2sigma = os.popen('combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+' -T '+t+' --expectedFromGrid 0.975').readlines()


			goForLimit = False
			for line in EstimationInformationExpP2sigma:
				print line
				if '-- Hybrid New --' in line:
					goForLimit = True
				if 'Limit' in line and 'r <' in line and '+/-' in line and 'CL' in line and goForLimit==True:
					BetaOne95upFreq.append(((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					limitLines.append('Expected 97.5%: r <'+((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					values.append(float((line.split('<')[-1]).replace('\n','').split('+/-')[0]))


			print 'combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+''
			EstimationInformationObs = os.popen('combine -M HybridNew --rule CLs --frequentist --testStat LHC CLSLimits/BetaOne'+cdir+'/confbetaone_'+cdir+'_'+name[x]+'.cfg -H ProfileLikelihood --fork 4 --rMax '+rMax+' --rAbsAcc '+absAcc+'').readlines()


			goForLimit = False
			for line in EstimationInformationObs:
				print line
				if '-- Hybrid New --' in line:
					goForLimit = True
				if 'Limit' in line and 'r <' in line and '+/-' in line and 'CL' in line and goForLimit==True:
					BetaOneObsFreq.append(((line.split('<')[-1]).replace('\n','')).split('+/-')[0])
					limitLines.append('Observed Limit: r <'+((line.split('<')[-1]).replace('\n','')).split('+/-')[0])


			for line in limitLines:
				print line

		vstart = round((min(values)/3),14)
		vstop = round((max(values)*3),14)
		rvalues = []
		interval = abs(vstop-vstart)/100.0
		
		nindex = 0
		thisr = 0
		while thisr<vstop:
			thisr = vstart*1.05**(float(nindex))
			rvalues.append(thisr)
			# print thisr
			nindex +=1
		strRvalues = []
		for r in rvalues:
			strRvalues.append(str(round(r,14)))
		# print strRvalues
		"""
		for r in strRvalues:
			command = 'combine '+METHOD.replace('SINGLEPOINT',r).replace('CONFIGURATION','confbetaone_'+cdir+'_'+name[x]+'.cfg')
			strR = r.replace('.','_')
			os.system('cat ShellScriptsForBatch/subbetaone_'+cdir+name[x]+'.csh | sed  \'s/SUBCOMMAND/'+command+'/g\'  > ShellScriptsForBatch/subbetaone_'+strR+'_'+cdir+name[x]+'.csh')
			os.system('chmod 777 ShellScriptsForBatch/subbetaone_'+strR+'_'+cdir+name[x]+'.csh')

			for nn in range(numdo):
				if (dobatch):
					os.system('bsub -o /dev/null -e /dev/null -q '+queue+' -J jobbetaone'+str(nn)+'_R_'+strR+'_'+name[x]+' < ShellScriptsForBatch/subbetaone_'+strR+'_'+cdir+name[x]+'.csh')
	       """
if do_BetaHalf == 1:
	masses_betahalf = []
	for x in range(len(name)):
		if 'BetaHalf' not in name[x]:
			continue		
		print 'Calculating limit for: ' + name[x]			
		f = open('CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+'.cfg','w')
		count = 0
		# print name[x]
		for l in mycards:
			if '.txt' in l and name[x] in l and str(name[x]+'0') not in l:
				count = 1
				for m in masses:
					if str(m) in l and int(m) not in masses_betahalf:
						masses_betahalf.append(int(m))

				
			if '.txt' in l and name[x] not in l:
				count = 0
			if count ==1 and '.txt' not in l:
				f.write(l+'\n')
					
		f.close()
	
		os.system('mkdir CLSLimits/BetaHalf'+cdir+'/'+name[x])

		mdir = (os.popen('pwd').readlines())[0]
		mdir = mdir.replace('\n','')
		fsub = open('ShellScriptsForBatch/subbetahalf_'+cdir+name[x]+'.csh','w')
		fsub.write('#!/bin/csh'+ cr)
		fsub.write('cd ' + mdir+ cr)
		fsub.write('eval `scramv1 runtime -csh`'+ cr)
		fsub.write('cd -'+ cr)
		fsub.write('cp '+mdir+'/CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+ '.cfg . '+ cr)
		fsub.write('SUBCOMMAND'+'\n')
		fsub.close()

		## Estimate the r values with Asymptotic CLs
		EstimationInformation = [' r < 0.000000']
		if 'LQ' in lqtype:
			if float(name[x].replace('LQ_BetaHalf_M_',''))<700:
				rmax = float(name[x].replace('LQ_BetaHalf_M_',''))/100.#fixme was 10000.0
			elif float(name[x].replace('LQ_BetaHalf_M_',''))<1000:
				rmax = float(name[x].replace('LQ_BetaHalf_M_',''))/10.#fixme was 10000.0
			else:
				rmax = float(name[x].replace('LQ_BetaHalf_M_',''))/4.#fixme was 10000.0
		#rmax = 10000.0
		breaker = False 
		ntry = 0
		oldrmax = 100000.0

		while 'r < 0.000000' in str(EstimationInformation):
			ntry += 1
			#EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+'.cfg --rMax '+str(rmax)+' --rAbsAcc .0000005').readlines()
			#print ('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+'.cfg --rMax '+str(rmax)+' --rAbsAcc .0000005')
			rAbsAcc='.000005'
			print ('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+'.cfg --rMax '+str(rmax)+'  --rAbsAcc '+rAbsAcc)
			EstimationInformation = os.popen('combine '+ESTIMATIONMETHOD+' CLSLimits/BetaHalf'+cdir+'/confbetahalf_'+cdir+'_'+name[x]+'.cfg --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc).readlines()
			if abs(rmax - oldrmax)<.1*rmax:
				breaker=True		

			if breaker ==True:
				break
			effrmax = -999999
			for e in EstimationInformation:
				if 'r <'  in e and 'Expected' in e:
					thisrval = e.split('<')[-1]
					thisrval = thisrval.replace('\n','')
					thisrval = float(thisrval)
					if thisrval>effrmax:
						effrmax = thisrval

			oldrmax = float(rmax)
			
			if effrmax < 0:
				rmax = 0.6*rmax
			else:
				rmax = effrmax*2.0
			EstimationInformation = [' r < 0.000000']
			if ntry > 100:
				breaker = True
		## Estimation Complete
		print '='*60
		
		expectedlines = []
		for line in EstimationInformation:
			if 'Expected' in line and 'r <' in line:
				expectedlines.append(line.replace('\n',''))
		values = []
		for e in expectedlines:
			print e
			values.append(float(e.split()[-1]))

		## Fill the arrays of Asymptotic Values
		for line in EstimationInformation:
			if 'Observed' in line and '<' in line:
				BetaHalfObs.append((line.split('<')[-1]).replace('\n',''))
				print line
			if 'Expected' in line and '<' in line:
				if '2.5%' in line:
					BetaHalf95down.append((line.split('<')[-1]).replace('\n',''))
				if '16.0%' in line:
					BetaHalf68down.append((line.split('<')[-1]).replace('\n',''))
				if '50.0%' in line:
					BetaHalfExp.append((line.split('<')[-1]).replace('\n',''))
				if '84.0%' in line:
					BetaHalf68up.append((line.split('<')[-1]).replace('\n',''))
				if '97.5%' in line:
					BetaHalf95up.append((line.split('<')[-1]).replace('\n',''))
		print '='*60
		
		vstart = round((min(values)/3),14)
		while vstart == 0.0 :
			#print values
			values.remove(0.0)
			vstart = round((min(values)/3),14)
		vstop = round((max(values)*3),14)
		rvalues = []
		interval = abs(vstop-vstart)/100.0
		
		nindex = 0
		thisr = 0
		while thisr<vstop:
			thisr = vstart*1.05**(float(nindex))
			rvalues.append(thisr)
			nindex += 1
		strRvalues = []
		for r in rvalues:
			strRvalues.append(str(round(r,14)))
		# print strRvalues
		"""
		for r in strRvalues:
			command = 'combine '+METHOD.replace('SINGLEPOINT',r).replace('CONFIGURATION','confbetahalf_'+cdir+'_'+name[x]+'.cfg')
			strR = r.replace('.','_')
			os.system('cat ShellScriptsForBatch/subbetahalf_'+cdir+name[x]+'.csh | sed  \'s/SUBCOMMAND/'+command+'/g\'  > ShellScriptsForBatch/subbetahalf_'+strR+'_'+cdir+name[x]+'.csh')
			os.system('chmod 777 ShellScriptsForBatch/subbetahalf_'+strR+'_'+cdir+name[x]+'.csh')

			for nn in range(numdo):
				if (dobatch):
					os.system('bsub -o /dev/null -e /dev/null -q '+queue+' -J jobbetahalf'+str(nn)+'_R_'+strR+'_'+name[x]+' < ShellScriptsForBatch/subbetahalf_'+strR+'_'+cdir+name[x]+'.csh')
		"""			
		# sys.exit()
################################################################################################################
################################################################################################################

if do_combo == 1:
	digits = '0123456789'

	cards = []
	cardmasses = []
	cardcontent = []
	card = ''

	flog = open(fullcardfile,'r')
	os.system('rm -r TMPComboCards/; mkdir TMPComboCards')	
	for line in flog:
		if '.txt' not in line:
			card += line
		if '.txt' in line or ("Combination of" in line and lqtype == 'BL'):
			cardcontent.append(card)
	
			card  = ''
			
			line = line.replace('.txt\n','')
			cards.append(line)
			m = ''
			for x in line:
				if x in digits:
					m+=(x)
			cardmasses.append(m)
			
	cardcontent.append(card)
	
	cardcontent = cardcontent[1:]
	combocards = []
	for x in cardcontent:
		for y in cards:
			if y in x and y+'0' not in x and '1'+y not in x:
				fout = open('combocard_'+y+'.cfg','w')
				x = x.replace('stat_','stat_'+y)
				fout.write(x)
				fout.close()
				combocards.append('combocard_'+y+'.cfg')
	uniquecardmasses = []
	for x in cardmasses:
		if x not in uniquecardmasses:
			uniquecardmasses.append(x)
	for m in uniquecardmasses:
		print 'Printing cards for mass ' +str(m)
		pair = ['','']
		nn = 0
		for x in combocards:
			#print x
			if m in x and m+'0' not in x and '1'+m not in x:
				#print nn,x
				pair[nn] = x
				nn += 1
		if 'BetaHalf' in pair[0]:
			bcard = pair[0]
			ocard = pair[1]
		if 'BetaHalf' not in pair[0]:
			bcard = pair[1]
			ocard = pair[0]	

		os.system('combineCards.py '+bcard+ ' '+ocard+ '  > TMPComboCards/combocard_COMBO_M_'+m+'.cfg ' )
		os.system('combineCards.py '+bcard+' > TMPComboCards/combocard_COMBO_BetaHalf_M_'+m+'.cfg ' )
		os.system('combineCards.py '+ocard+' > TMPComboCards/combocard_COMBO_BetaOne_M_'+m+'.cfg ' )
		print pair

	for m in uniquecardmasses:
		combocards.append('TMPComboCards/combocard_COMBO_M_'+m+'.cfg')

	betaind = -1

	for beta in betas:
		betaind += 1
		ComboObs.append([])
		Combo95down.append([])
		Combo68down.append([])
		ComboExp.append([])
		Combo68up.append([])
		Combo95up.append([])

		ComboBetaOneObs.append([])
		ComboBetaOne95down.append([])
		ComboBetaOne68down.append([])
		ComboBetaOneExp.append([])
		ComboBetaOne68up.append([])
		ComboBetaOne95up.append([])
		

		ComboBetaHalfObs.append([])
		ComboBetaHalf95down.append([])
		ComboBetaHalf68down.append([])
		ComboBetaHalfExp.append([])
		ComboBetaHalf68up.append([])
		ComboBetaHalf95up.append([])
						
								
		betaval = str(beta).replace('.','_')
		os.system('mkdir CLSLimits/Combo'+cdir+'/Combo_beta_'+betaval)

		for x in range(len(uniquecardmasses)):	
			print 'Calculating limit for combination mass: ' + str(uniquecardmasses[x]) + ' , beta = '+str(beta)			
			newcard = ('CLSLimits/Combo'+cdir+'/combocard_COMBO_M_'+uniquecardmasses[x]+'.cfg').replace('COMBO','beta_'+betaval+'_COMBO')

			newcard_BetaOne = ('CLSLimits/Combo'+cdir+'/combocard_COMBO_BetaOne_M_'+uniquecardmasses[x]+'.cfg').replace('COMBO_BetaOne','beta_'+betaval+'_COMBO_BetaOne')
			
			newcard_BetaHalf = ('CLSLimits/Combo'+cdir+'/combocard_COMBO_BetaHalf_M_'+uniquecardmasses[x]+'.cfg').replace('COMBO_BetaHalf','beta_'+betaval+'_COMBO_BetaHalf')
			
			ctypes = ['','_BetaOne','_BetaHalf']
			for c in ctypes:
				tcard = newcard
				if 'BetaHalf' in c:
					tcard = newcard_BetaHalf
				if 'BetaOne' in c:
					tcard = newcard_BetaOne
				ftmp = open(tcard,'w')
				fnorm = open('TMPComboCards/combocard_COMBO'+c+'_M_'+str(uniquecardmasses[x])+'.cfg','r')
				
				betahalfplace = 99
				betaoneplace = 99
				for line in fnorm:
	
					if (lqtype in line and 'process' in line):
						linesplit = line.split()
						for place in range(len(linesplit)):
							if lqtype in linesplit[place] and 'BetaHalf' in linesplit[place]:
								betahalfplace = place
							if lqtype in linesplit[place] and 'BetaHalf' not in linesplit[place]:
								betaoneplace = place
								
					if ( 'rate' in line):
	
						linesplit = line.split()
						linesplit2 = []
						for place in range(len(linesplit)):
							arg = linesplit[place]
							if betahalfplace == place:
								arg = str(float(arg)*beta*(1.0-beta)*4.0)
							
							if betaoneplace == place:						
								arg = str(float(arg)*beta*beta)
							linesplit2.append(arg)
						line2 = ''
						for xpart in linesplit2:
							line2 += xpart + '    '
						line2 += '\n'
						line = line2
					if  'stat' in line and 'Signal' in line and 'gmN' in line:
						linesplit = line.split()
						print linesplit
						for nsp in range(len(linesplit)):
							if 'BetaHalf' not in line and nsp == betaoneplace+1:
								repsold =  str(linesplit[nsp+1])
								repsnew = str(float(repsold)*beta*beta)
								line = line.replace(repsold,repsnew)
							if 'BetaHalf' in line and nsp == betahalfplace+1:
								repsold =  str(linesplit[nsp+1])
								repsnew = str(float(repsold)*beta*(1.0-beta)*4.0)
								line = line.replace(repsold,repsnew)
					ftmp.write(line)
				ftmp.close()
		
			thisname ='beta_'+ betaval + '_M_'+str(uniquecardmasses[x])
			mdir = (os.popen('pwd').readlines())[0]
			mdir = mdir.replace('\n','')
			fsub = open('ShellScriptsForBatch/subcombo_'+cdir+thisname+'.csh','w')
			fsub.write('#!/bin/csh'+ cr)
			fsub.write('cd ' + mdir+ cr)
			fsub.write('eval `scramv1 runtime -csh`'+ cr)
			fsub.write('cd -'+ cr)
			fsub.write('cp '+mdir+'/'+newcard+' .'+ cr)
			fsub.write('cp '+mdir+'/'+newcard_BetaOne+' .'+ cr)
			fsub.write('cp '+mdir+'/'+newcard_BetaHalf+' .'+ cr)

			fsub.write('SUBCOMMAND0'+'\n')
			fsub.write('mv higgs*root Combo_'+thisname+'_R_RVALUE0_ind_`bash -c \'echo $RANDOM\'`.root \n')			
			fsub.write('SUBCOMMAND1'+'\n')
			fsub.write('mv higgs*root ComboBetaOne_'+thisname+'_R_RVALUE1_ind_`bash -c \'echo $RANDOM\'`.root \n')			
			fsub.write('SUBCOMMAND2'+'\n')
			fsub.write('mv higgs*root ComboBetaHalf_'+thisname+'_R_RVALUE2_ind_`bash -c \'echo $RANDOM\'`.root \n')						
			fsub.close()

			## Estimate the r values with Asymptotic CLs
			EstimationInformation0 = [' r < 0.000000']
			rmax = 10000.0
			breaker = False 
			ntry = 0
			oldrmax = 100000.0
			betaCoruujj = (float(beta)*10)*(float(beta)<.1)+(float(beta))*(float(beta)>.1)*(float(beta)<.2)+1.0*(float(beta)>.2)
			betaCoruvjj = 1.0*(float(beta)<.75)+(float(beta))*(float(beta)>.75)*(float(beta)<.9)+(float(beta)*10)*(float(beta)>.9)
			betaCorComb = (float(beta)>0.4)*(float(beta)*10)*(float(beta)<.1)+(float(beta))*(float(beta)>.1)*(float(beta)<.2)+1.0*(float(beta)>.2) + (float(beta)<0.4)* 1.0*(float(beta)<.75)+(float(beta))*(float(beta)>.75)*(float(beta)<.9)+(float(beta)*10)*(float(beta)>.9)
			if 'LQ' in lqtype:
				if float(name[x].replace('LQ_M_',''))<900:
					rmax = float(name[x].replace('LQ_M_',''))/10./betaCorComb#fixme was 10000.0
				elif float(name[x].replace('LQ_M_',''))<1200:
					rmax = float(name[x].replace('LQ_M_',''))/10./betaCorComb#fixme was 10000.0
				else:
					rmax = float(name[x].replace('LQ_M_',''))/4./betaCorComb#fixme was 10000.0
			#rmax = 1000.0
			while 'r < 0.000000' in str(EstimationInformation0):
				ntry += 1
				rAbsAcc='.00005'
				print 'combine '+ESTIMATIONMETHOD+' '+newcard +' --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc
				EstimationInformation0 = os.popen('combine '+ESTIMATIONMETHOD+' '+newcard +' --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc).readlines()
				if abs(rmax - oldrmax)<.01*rmax:
					breaker=True				
				if breaker ==True:
					break
				effrmax = -999999
				for e in EstimationInformation0:
					if 'r <'  in e and 'Expected' in e:
						thisrval = e.split('<')[-1]
						thisrval = thisrval.replace('\n','')
						thisrval = float(thisrval)
						if thisrval>effrmax:
							effrmax = thisrval

				oldrmax = float(rmax)

				if effrmax < 0:
					rmax = 0.8*rmax
				else:
					rmax = effrmax*2.0

				# rmax = effrmax*2.0
				EstimationInformation0 = [' r < 0.000000']
				if ntry > 30:
					breaker = True


			EstimationInformation1 = [' r < 0.000000']
			rmax = 10000.0
			breaker = False 
			ntry = 0
			oldrmax = 100000.0
			if 'LQ' in lqtype:
				if float(name[x].replace('LQ_M_',''))<900:
					rmax = float(name[x].replace('LQ_M_',''))/10./betaCoruujj#fixme was 10000.0
				elif float(name[x].replace('LQ_M_',''))<1200:
					rmax = float(name[x].replace('LQ_M_',''))/10./betaCoruujj#fixme was 10000.0
				else:
					rmax = float(name[x].replace('LQ_M_',''))/4./betaCoruujj#fixme was 10000.0
			#rmax = 1000.0
			while 'r < 0.000000' in str(EstimationInformation1):
				ntry += 1				
				print 'combine '+ESTIMATIONMETHOD+' '+newcard_BetaOne +' --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc
				EstimationInformation1 = os.popen('combine '+ESTIMATIONMETHOD+' '+newcard_BetaOne +' --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc).readlines()
				
				if abs(rmax - oldrmax)<.01*rmax:
					breaker=True

				if breaker ==True:
					break
				effrmax = -999999
				for e in EstimationInformation1:
					if 'r <'  in e and 'Expected' in e:
						thisrval = e.split('<')[-1]
						thisrval = thisrval.replace('\n','')
						thisrval = float(thisrval)
						if thisrval>effrmax:
							effrmax = thisrval



				oldrmax = float(rmax)
				if effrmax < 0:
					rmax = 0.8*rmax
				else:
					rmax = effrmax*2.0

				EstimationInformation1 = [' r < 0.000000']
				if ntry > 30:
					breaker = True

				
			EstimationInformation2 = [' r < 0.000000']
			rmax = 10000.0
			breaker = False 
			ntry = 0
			oldrmax = 100000.0
			if 'LQ' in lqtype:
				if float(name[x].replace('LQ_M_',''))<900:
					rmax = float(name[x].replace('LQ_M_',''))/10./betaCoruvjj#fixme was 10000.0
				elif float(name[x].replace('LQ_M_',''))<1200:
					rmax = float(name[x].replace('LQ_M_',''))/10./betaCoruvjj#fixme was 10000.0
				else:
					rmax = float(name[x].replace('LQ_M_',''))/4./betaCoruvjj#fixme was 10000.0

			#rmax = 1000.0
			while 'r < 0.000000' in str(EstimationInformation2):
				ntry += 1
				print 'combine '+ESTIMATIONMETHOD+' '+newcard_BetaHalf +' --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc
				EstimationInformation2 = os.popen('combine '+ESTIMATIONMETHOD+' '+newcard_BetaHalf +' --rMax '+str(rmax)+' --rAbsAcc '+rAbsAcc).readlines()
				if abs(rmax - oldrmax)<.01*rmax:
					breaker=True				
				if breaker ==True:
					break
				effrmax = -999999
				for e in EstimationInformation2:
					if 'r <'  in e and 'Expected' in e:
						thisrval = e.split('<')[-1]
						thisrval = thisrval.replace('\n','')
						thisrval = float(thisrval)
						if thisrval>effrmax:
							effrmax = thisrval

				oldrmax = float(rmax)

				if effrmax < 0:
					rmax = 0.8*rmax
				else:
					rmax = effrmax*2.0

				EstimationInformation2 = [' r < 0.000000']
				if ntry > 30:
					breaker = True


			
			expectedlines0 = []
			for line in EstimationInformation0:
				if 'Expected' in line and 'r <' in line:
					expectedlines0.append(line.replace('\n',''))
			values0 = []
			for e in expectedlines0:
				print e
				values0.append(float(e.split()[-1]))


			expectedlines1 = []
			for line in EstimationInformation1:
				if 'Expected' in line and 'r <' in line:
					expectedlines1.append(line.replace('\n',''))
			values1 = []
			for e in expectedlines1:
				print e
				values1.append(float(e.split()[-1]))
				
				
			expectedlines2 = []
			for line in EstimationInformation2:
				if 'Expected' in line and 'r <' in line:
					expectedlines2.append(line.replace('\n',''))
			values2 = []
			for e in expectedlines2:
				print e
				values2.append(float(e.split()[-1]))				

			## Estimation Complete


			## Fill the arrays of Asymptotic Values
			for line in EstimationInformation0:
				if 'Observed' in line and '<' in line:
					ComboObs[betaind].append((line.split('<')[-1]).replace('\n',''))
				if 'Expected' in line and '<' in line:
					if '2.5%' in line:
						Combo95down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '16.0%' in line:
						Combo68down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '50.0%' in line:
						ComboExp[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '84.0%' in line:
						Combo68up[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '97.5%' in line:
						Combo95up[betaind].append((line.split('<')[-1]).replace('\n',''))

			for line in EstimationInformation1:
				if 'Observed' in line and '<' in line:
					ComboBetaOneObs[betaind].append((line.split('<')[-1]).replace('\n',''))
				if 'Expected' in line and '<' in line:
					if '2.5%' in line:
						ComboBetaOne95down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '16.0%' in line:
						ComboBetaOne68down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '50.0%' in line:
						ComboBetaOneExp[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '84.0%' in line:
						ComboBetaOne68up[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '97.5%' in line:
						ComboBetaOne95up[betaind].append((line.split('<')[-1]).replace('\n',''))

			for line in EstimationInformation2:
				if 'Observed' in line and '<' in line:
					ComboBetaHalfObs[betaind].append((line.split('<')[-1]).replace('\n',''))
				if 'Expected' in line and '<' in line:
					if '2.5%' in line:
						ComboBetaHalf95down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '16.0%' in line:
						ComboBetaHalf68down[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '50.0%' in line:
						ComboBetaHalfExp[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '84.0%' in line:
						ComboBetaHalf68up[betaind].append((line.split('<')[-1]).replace('\n',''))
					if '97.5%' in line:
						ComboBetaHalf95up[betaind].append((line.split('<')[-1]).replace('\n',''))
			
			## Asymptotic Information Filled
			
			
			vstart0 = round((min(values0)/2),14)
			vstop0 = round((max(values0)*2),14)
			rvalues0 = []


			vstart1 = round((min(values1)/2),14)
			vstop1 = round((max(values1)*2),14)
			rvalues1 = []
			
			vstart2 = round((min(values2)/2),14)
			vstop2 = round((max(values2)*2),14)
			rvalues2 = []			
			
			nindex0 = 0
			thisr0 = 0

			nindex1 = 0
			thisr1= 0
			
			nindex2 = 0
			thisr2 = 0
			
			print 'vstop0 '+str(vstop0) + '   vstart0  '+str(vstart0)
			print 'vstop1 '+str(vstop1) + '   vstart1  '+str(vstart1)
			print 'vstop2 '+str(vstop2) + '   vstart2  '+str(vstart2)

			expinc0 = 0.9999*(2.718281828**((0.0666666666667*(math.log(vstop0/vstart0)))))
			expinc1 = 0.9999*(2.718281828**((0.0666666666667*(math.log(vstop1/vstart1)))))
			expinc2 = 0.9999*(2.718281828**((0.0666666666667*(math.log(vstop2/vstart2)))))
			
			
			while thisr0<vstop0:
				thisr0 = vstart0*expinc0**(float(nindex0))
				rvalues0.append(thisr0)
				nindex0 += 1
			strRvalues0 = []
			for r in rvalues0:
				strRvalues0.append(str(round(r,14)))
			#print strRvalues0


			while thisr1<vstop1:
				thisr1 = vstart1*expinc1**(float(nindex1))
				rvalues1.append(thisr1)
				nindex1 += 1
			strRvalues1 = []
			for r in rvalues1:
				strRvalues1.append(str(round(r,14)))
			#print strRvalues1

			while thisr2<vstop2:
				thisr2 = vstart2*expinc2**(float(nindex2))
				rvalues2.append(thisr2)
				nindex2 += 1
			strRvalues2 = []
			for r in rvalues2:
				strRvalues2.append(str(round(r,14)))
			#print strRvalues2
			

			
			for rind in range(len(strRvalues0)):
				r0 = strRvalues0[rind]
				r1 = strRvalues1[rind]
				r2 = strRvalues2[rind]

				command0 = 'combine '+METHOD.replace('SINGLEPOINT',r0).replace('CONFIGURATION',newcard.split('/')[-1])
				command1 = 'combine '+METHOD.replace('SINGLEPOINT',r1).replace('CONFIGURATION',newcard_BetaOne.split('/')[-1])
				command2 = 'combine '+METHOD.replace('SINGLEPOINT',r2).replace('CONFIGURATION',newcard_BetaHalf.split('/')[-1])

				strR0 = r0.replace('.','_')
				strR1 = r1.replace('.','_')
				strR2 = r2.replace('.','_')

				os.system('cat ShellScriptsForBatch/subcombo_'+cdir+thisname+'.csh | sed  \'s/SUBCOMMAND0/'+command0+'/g\' | sed  \'s/RVALUE0/'+strR0+'/g\' | sed  \'s/SUBCOMMAND1/'+command1+'/g\' | sed  \'s/RVALUE1/'+strR1+'/g\' | sed  \'s/SUBCOMMAND2/'+command2+'/g\' | sed  \'s/RVALUE2/'+strR2+'/g\' > ShellScriptsForBatch/subcombo_R_'+str(rind)+'_'+cdir+thisname+'.csh')
				os.system('chmod 777 ShellScriptsForBatch/subcombo_R_'+str(rind)+'_'+cdir+thisname+'.csh')
	
				for nn in range(numdo):
					if (dobatch):
						os.system('bsub -o /dev/null -e /dev/null -q '+queue+' -J jobcombo'+str(nn)+'_R_'+str(rind)+'_'+thisname+' < ShellScriptsForBatch/subcombo_R_'+str(rind)+'_'+cdir+thisname+'.csh')


################################################################################################################
################################################################################################################






os.system('rm higgsCombineTest*root')

print '\n\n\n'

#### ASYMPTOTIC CLS PRINTOUT ###

#LQToCMu 2012-2016
#mTh = [0.200E+03,0.210E+03,0.220E+03,0.230E+03,0.240E+03,0.250E+03,0.260E+03,0.270E+03,0.290E+03,0.300E+03,0.310E+03,0.320E+03,0.330E+03,0.340E+03,0.350E+03,0.360E+03,0.370E+03,0.380E+03,0.390E+03,0.400E+03,0.410E+03,0.420E+03,0.430E+03,0.440E+03,0.450E+03,0.460E+03,0.470E+03,0.480E+03,0.490E+03,0.500E+03,0.510E+03,0.520E+03,0.530E+03,0.540E+03,0.550E+03,0.560E+03,0.570E+03,0.580E+03,0.590E+03,0.600E+03,0.610E+03,0.620E+03,0.630E+03,0.640E+03,0.650E+03,0.660E+03,0.670E+03,0.680E+03,0.690E+03,0.700E+03,0.710E+03,0.720E+03,0.730E+03,0.740E+03,0.750E+03,0.760E+03,0.770E+03,0.780E+03,0.790E+03,0.800E+03,0.810E+03,0.820E+03,0.830E+03,0.840E+03,0.850E+03,0.860E+03,0.870E+03,0.880E+03,0.890E+03,0.900E+03,0.910E+03,0.920E+03,0.930E+03,0.940E+03,0.950E+03,0.960E+03,0.970E+03,0.980E+03,0.990E+03,0.100E+04,0.101E+04,0.102E+04,0.103E+04,0.104E+04,0.105E+04,0.106E+04,0.107E+04,0.108E+04,0.109E+04,0.110E+04,0.111E+04,0.112E+04,0.113E+04,0.114E+04,0.115E+04,0.116E+04,0.117E+04,0.118E+04,0.119E+04,0.120E+04,0.121E+04,0.122E+04,0.123E+04,0.124E+04,0.125E+04,0.126E+04,0.127E+04,0.128E+04,0.129E+04,0.130E+04,0.131E+04,0.132E+04,0.133E+04,0.134E+04,0.135E+04,0.136E+04,0.137E+04,0.138E+04,0.139E+04,0.140E+04,0.141E+04,0.142E+04,0.143E+04,0.144E+04,0.145E+04,0.146E+04,0.147E+04,0.148E+04,0.149E+04,0.150E+04,0.151E+04,0.152E+04,0.153E+04,0.154E+04,0.155E+04,0.156E+04,0.157E+04,0.158E+04,0.159E+04,0.160E+04,0.161E+04,0.162E+04,0.163E+04,0.164E+04,0.165E+04,0.166E+04,0.167E+04,0.168E+04,0.169E+04,0.170E+04,0.171E+04,0.172E+04,0.173E+04,0.174E+04,0.175E+04,0.176E+04,0.177E+04,0.178E+04,0.179E+04,0.180E+04,0.181E+04,0.182E+04,0.183E+04,0.184E+04,0.185E+04,0.186E+04,0.187E+04,0.188E+04,0.189E+04,0.190E+04,0.191E+04,0.192E+04,0.193E+04,0.194E+04,0.195E+04,0.196E+04,0.197E+04,0.198E+04,0.199E+04,0.200E+04,0.201E+04,0.202E+04,0.203E+04,0.204E+04,0.205E+04,0.206E+04,0.207E+04,0.208E+04,0.209E+04,0.210E+04,0.211E+04,0.212E+04,0.213E+04,0.214E+04,0.215E+04,0.216E+04,0.217E+04,0.218E+04,0.219E+04,0.220E+04,0.221E+04,0.222E+04,0.223E+04,0.224E+04,0.225E+04,0.226E+04,0.227E+04,0.228E+04,0.229E+04,0.230E+04,0.231E+04,0.232E+04,0.233E+04,0.234E+04,0.235E+04,0.236E+04,0.237E+04,0.238E+04,0.239E+04,0.240E+04,0.241E+04,0.242E+04,0.243E+04,0.244E+04,0.245E+04,0.246E+04,0.247E+04,0.248E+04,0.249E+04,0.250E+04,0.251E+04,0.252E+04,0.253E+04,0.254E+04,0.255E+04,0.256E+04,0.257E+04,0.258E+04,0.259E+04,0.260E+04,0.261E+04,0.262E+04,0.263E+04,0.264E+04,0.265E+04,0.266E+04,0.267E+04,0.268E+04,0.269E+04,0.270E+04,0.271E+04,0.272E+04,0.273E+04,0.274E+04,0.275E+04,0.276E+04,0.277E+04,0.278E+04,0.279E+04,0.280E+04,0.281E+04,0.282E+04,0.283E+04,0.284E+04,0.285E+04,0.286E+04,0.287E+04,0.288E+04,0.289E+04,0.290E+04,0.291E+04,0.292E+04,0.293E+04,0.294E+04,0.295E+04,0.296E+04,0.297E+04,0.298E+04,0.299E+04 ]

#xsTh = [6.06E+01,4.79E+01,3.82E+01,3.07E+01,2.49E+01,2.03E+01,1.67E+01,1.38E+01,1.15E+01,9.60E+00,8.04E+00,6.80E+00,5.75E+00,4.90E+00,4.18E+00,3.59E+00,3.09E+00,2.66E+00,2.31E+00,2.00E+00,1.74E+00,1.52E+00,1.33E+00,1.17E+00,1.03E+00,9.06E-01,8.00E-01,7.07E-01,6.27E-01,5.58E-01,4.96E-01,4.43E-01,3.95E-01,3.54E-01,3.16E-01,2.84E-01,2.55E-01,2.29E-01,2.07E-01,1.87E-01,1.69E-01,1.53E-01,1.38E-01,1.25E-01,1.14E-01,1.03E-01,9.39E-02,8.54E-02,7.78E-02,7.10E-02,6.48E-02,5.92E-02,5.42E-02,4.97E-02,4.55E-02,4.16E-02,3.82E-02,3.51E-02,3.22E-02,2.97E-02,2.73E-02,2.51E-02,2.31E-02,2.13E-02,1.97E-02,1.82E-02,1.68E-02,1.55E-02,1.44E-02,1.33E-02,1.23E-02,1.14E-02,1.06E-02,9.79E-03,9.09E-03,8.45E-03,7.84E-03,7.28E-03,6.77E-03,6.30E-03,5.86E-03,5.45E-03,5.08E-03,4.73E-03,4.41E-03,4.11E-03,3.83E-03,3.58E-03,3.34E-03,3.12E-03,2.91E-03,2.72E-03,2.54E-03,2.38E-03,2.22E-03,2.08E-03,1.95E-03,1.82E-03,1.71E-03,1.60E-03,1.50E-03,1.41E-03,1.32E-03,1.24E-03,1.16E-03,1.09E-03,1.02E-03,9.59E-04,9.01E-04,8.46E-04,7.95E-04,7.48E-04,7.03E-04,6.61E-04,6.22E-04,5.85E-04,5.50E-04,5.18E-04,4.87E-04,4.59E-04,4.33E-04,4.07E-04,3.84E-04,3.61E-04,3.41E-04,3.21E-04,3.03E-04,2.85E-04,2.69E-04,2.54E-04,2.40E-04,2.26E-04,2.13E-04,2.02E-04,1.90E-04,1.80E-04,1.70E-04,1.60E-04,1.51E-04,1.43E-04,1.35E-04,1.28E-04,1.21E-04,1.14E-04,1.08E-04,1.02E-04,9.66E-05,9.13E-05,8.64E-05,8.18E-05,7.74E-05,7.32E-05,6.93E-05,6.56E-05,6.21E-05,5.88E-05,5.57E-05,5.27E-05,5.00E-05,4.73E-05,4.48E-05,4.25E-05,4.02E-05,3.81E-05,3.61E-05,3.43E-05,3.25E-05,3.08E-05,2.92E-05,2.77E-05,2.62E-05,2.49E-05,2.36E-05,2.24E-05,2.12E-05,2.01E-05,1.91E-05,1.81E-05,1.72E-05,1.63E-05,1.55E-05,1.47E-05,1.39E-05,1.32E-05,1.26E-05,1.19E-05,1.13E-05,1.07E-05,1.02E-05,9.68E-06,9.20E-06,8.73E-06,8.29E-06,7.87E-06,7.47E-06,7.10E-06,6.74E-06,6.41E-06,6.08E-06,5.78E-06,5.49E-06,5.22E-06,4.96E-06,4.71E-06,4.47E-06,4.26E-06,4.04E-06,3.84E-06,3.65E-06,3.46E-06,3.30E-06,3.13E-06,2.97E-06,2.83E-06,2.69E-06,2.55E-06,2.43E-06,2.31E-06,2.19E-06,2.08E-06,1.98E-06,1.88E-06,1.79E-06,1.70E-06,1.62E-06,1.54E-06,1.46E-06,1.39E-06,1.32E-06,1.25E-06,1.19E-06,1.13E-06,1.08E-06,1.03E-06,9.74E-07,9.27E-07,8.81E-07,8.37E-07,7.96E-07,7.57E-07,7.20E-07,6.84E-07,6.50E-07,6.19E-07,5.88E-07,5.60E-07,5.32E-07,5.05E-07,4.80E-07,4.57E-07,4.35E-07,4.13E-07,3.92E-07,3.73E-07,3.55E-07,3.38E-07,3.21E-07,3.05E-07,2.90E-07,2.75E-07,2.62E-07,2.49E-07,2.36E-07,2.25E-07,2.14E-07,2.03E-07,1.93E-07,1.83E-07,1.74E-07,1.66E-07,1.58E-07,1.50E-07,1.42E-07,1.35E-07,1.28E-07,1.22E-07,1.16E-07,1.10E-07,1.05E-07,9.95E-08,9.46E-08 ]

#LQToBMu / LQToSMU 2020->

mTh = [300.0,310.0,320.0,330.0,340.0,350.0,360.0,370.0,380.0,390.0,400.0,410.0,420.0,430.0,440.0,450.0,460.0,470.0,480.0,490.0,500.0,510.0,520.0,530.0,540.0,550.0,560.0,570.0,580.0,590.0,600.0,610.0,620.0,630.0,640.0,650.0,660.0,670.0,680.0,690.0,700.0,710.0,720.0,730.0,740.0,750.0,760.0,770.0,780.0,790.0,800.0,810.0,820.0,830.0,840.0,850.0,860.0,870.0,880.0,890.0,900.0,910.0,920.0,930.0,940.0,950.0,960.0,970.0,980.0,990.0,1000.0,1010.0,1020.0,1030.0,1040.0,1050.0,1060.0,1070.0,1080.0,1090.0,1100.0,1110.0,1120.0,1130.0,1140.0,1150.0,1160.0,1170.0,1180.0,1190.0,1200.0,1210.0,1220.0,1230.0,1240.0,1250.0,1260.0,1270.0,1280.0,1290.0,1300.0,1310.0,1320.0,1330.0,1340.0,1350.0,1360.0,1370.0,1380.0,1390.0,1400.0,1410.0,1420.0,1430.0,1440.0,1450.0,1460.0,1470.0,1480.0,1490.0,1500.0,1510.0,1520.0,1530.0,1540.0,1550.0,1560.0,1570.0,1580.0,1590.0,1600.0,1610.0,1620.0,1630.0,1640.0,1650.0,1660.0,1670.0,1680.0,1690.0,1700.0,1710.0,1720.0,1730.0,1740.0,1750.0,1760.0,1770.0,1780.0,1790.0,1800.0,1810.0,1820.0,1830.0,1840.0,1850.0,1860.0,1870.0,1880.0,1890.0,1900.0,1910.0,1920.0,1930.0,1940.0,1950.0,1960.0,1970.0,1980.0,1990.0,2000.0,2010.0,2020.0,2030.0,2040.0,2050.0,2060.0,2070.0,2080.0,2090.0,2100.0,2110.0,2120.0,2130.0,2140.0,2150.0,2160.0,2170.0,2180.0,2190.0,2200.0,2210.0,2220.0,2230.0,2240.0,2250.0,2260.0,2270.0,2280.0,2290.0,2300.0,2310.0,2320.0,2330.0,2340.0,2350.0,2360.0,2370.0,2380.0,2390.0,2400.0,2410.0,2420.0,2430.0,2440.0,2450.0,2460.0,2470.0,2480.0,2490.0,2500.0,2510.0,2520.0,2530.0,2540.0,2550.0,2560.0,2570.0,2580.0,2590.0,2600.0,2610.0,2620.0,2630.0,2640.0,2650.0,2660.0,2670.0,2680.0,2690.0,2700.0,2710.0,2720.0,2730.0,2740.0,2750.0,2760.0,2770.0,2780.0,2790.0,2800.0,2810.0,2820.0,2830.0,2840.0,2850.0,2860.0,2870.0,2880.0,2890.0,2900.0,2910.0,2920.0,2930.0,2940.0,2950.0,2960.0,2970.0,2980.0,2990.0,3000.0,3500.0,4000.0]

xsTh = [8.402e+00,7.025e+00,5.995e+00,5.102e+00,4.345e+00,3.744e+00,3.203e+00,2.783e+00,2.384e+00,2.062e+00,1.813e+00,1.561e+00,1.371e+00,1.199e+00,1.062e+00,9.321e-01,8.180e-01,7.236e-01,6.396e-01,5.617e-01,5.010e-01,4.514e-01,4.040e-01,3.598e-01,3.265e-01,2.887e-01,2.598e-01,2.340e-01,2.091e-01,1.899e-01,1.706e-01,1.541e-01,1.385e-01,1.261e-01,1.156e-01,1.034e-01,9.401e-02,8.593e-02,7.781e-02,7.087e-02,6.449e-02,5.861e-02,5.451e-02,4.918e-02,4.532e-02,4.100e-02,3.798e-02,3.445e-02,3.188e-02,2.908e-02,2.680e-02,2.437e-02,2.277e-02,2.104e-02,1.906e-02,1.770e-02,1.628e-02,1.503e-02,1.386e-02,1.293e-02,1.190e-02,1.098e-02,1.012e-02,9.435e-03,8.646e-03,8.060e-03,7.462e-03,6.913e-03,6.393e-03,5.979e-03,5.515e-03,5.167e-03,4.770e-03,4.399e-03,4.139e-03,3.851e-03,3.579e-03,3.306e-03,3.102e-03,2.897e-03,2.696e-03,2.529e-03,2.347e-03,2.178e-03,2.038e-03,1.915e-03,1.768e-03,1.649e-03,1.527e-03,1.447e-03,1.346e-03,1.271e-03,1.169e-03,1.114e-03,1.037e-03,9.656e-04,8.998e-04,8.506e-04,8.009e-04,7.435e-04,6.991e-04,6.530e-04,6.067e-04,5.752e-04,5.332e-04,5.026e-04,4.760e-04,4.421e-04,4.177e-04,3.908e-04,3.675e-04,3.431e-04,3.208e-04,3.052e-04,2.839e-04,2.704e-04,2.520e-04,2.377e-04,2.243e-04,2.093e-04,1.964e-04,1.857e-04,1.737e-04,1.658e-04,1.527e-04,1.449e-04,1.368e-04,1.273e-04,1.211e-04,1.141e-04,1.065e-04,1.011e-04,9.495e-05,8.928e-05,8.374e-05,7.930e-05,7.478e-05,7.063e-05,6.654e-05,6.266e-05,5.903e-05,5.565e-05,5.229e-05,4.952e-05,4.649e-05,4.382e-05,4.125e-05,3.897e-05,3.703e-05,3.446e-05,3.288e-05,3.096e-05,2.892e-05,2.732e-05,2.570e-05,2.439e-05,2.315e-05,2.176e-05,2.041e-05,1.939e-05,1.828e-05,1.740e-05,1.639e-05,1.537e-05,1.455e-05,1.376e-05,1.298e-05,1.222e-05,1.157e-05,1.093e-05,1.042e-05,9.700e-06,9.199e-06,8.707e-06,8.174e-06,7.690e-06,7.306e-06,6.972e-06,6.526e-06,6.177e-06,5.865e-06,5.532e-06,5.219e-06,4.913e-06,4.669e-06,4.401e-06,4.138e-06,3.919e-06,3.720e-06,3.521e-06,3.286e-06,3.131e-06,2.936e-06,2.775e-06,2.649e-06,2.491e-06,2.355e-06,2.225e-06,2.107e-06,1.989e-06,1.861e-06,1.768e-06,1.674e-06,1.595e-06,1.503e-06,1.418e-06,1.336e-06,1.268e-06,1.203e-06,1.130e-06,1.060e-06,1.018e-06,9.541e-07,9.103e-07,8.495e-07,8.014e-07,7.557e-07,7.208e-07,6.784e-07,6.485e-07,6.150e-07,5.764e-07,5.447e-07,5.209e-07,4.910e-07,4.584e-07,4.352e-07,4.087e-07,3.897e-07,3.697e-07,3.470e-07,3.270e-07,3.109e-07,2.926e-07,2.754e-07,2.619e-07,2.491e-07,2.337e-07,2.236e-07,2.103e-07,1.990e-07,1.858e-07,1.770e-07,1.672e-07,1.574e-07,1.474e-07,1.401e-07,1.325e-07,1.251e-07,1.194e-07,1.122e-07,1.073e-07,1.007e-07,9.517e-08,8.980e-08,8.482e-08,8.062e-08,7.604e-08,7.138e-08,6.906e-08,6.403e-08,6.143e-08,5.739e-08,5.423e-08,5.121e-08,4.917e-08,4.613e-08,4.333e-08,4.079e-08,3.916e-08,3.698e-08,2.565e-09,2.426e-10]

if lqtype in ['AM','YM','MM','MC']:
	print 'WARNING WARNING WARNING WARNING'
	print 'USING VECTOR LQ INCLUSIVE CROSS SECTIONS'
	mTh = [200.,300.,400.,500.,600.,700.,800.,900.,1000.,1100.,1200.,1300.,1400.,1500.,1600.,1700.,1800.]
	if lqtype == 'YM':
		xsTh = [1064,104.6,17.74,4.03,1.125,0.3519,0.1194,0.04373,0.01731,0.006853,0.002832,0.001203,0.0005089,0.0002236,9.675E-05,4.159E-05,1.794E-05]
	if lqtype == 'MC':
		xsTh = [246.7,21.19,3.354,0.7378,0.2034,0.06362,0.02177,0.008059,0.003231,0.001298,0.0005442,0.0002344,0.0001006,4.478E-05,1.96E-05,8.518E-06,3.711E-06]
	if lqtype == 'MM':
		xsTh = [74640,2510,242.9,40.14,9.204,2.528,0.7827,0.2678,0.1006,0.03822,0.01528,0.006316,0.002614,0.001128,0.0004799,0.0002037,8.697E-05]
	if lqtype == 'AM':
		xsTh = [242.3,20.06,2.956,0.5897,0.1458,0.04056,0.01228,0.004027,0.001431,0.0005108,0.0001909,7.373E-05,2.849E-05,1.148E-05,4.578E-06,1.829E-06,7.371E-07]

if lqtype in ['RV','BL']:
	print 'WARNING WARNING WARNING WARNING'
	print 'USING SUSY CROSS SECTIONS FROM https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVstopsbottom'
	mTh = [100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,205,210,215,220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295,300,305,310,315,320,325,330,335,340,345,350,355,360,365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,650,655,660,665,670,675,680,685,690,695,700,705,710,715,720,725,730,735,740,745,750,755,760,765,770,775,780,785,790,795,800,805,810,815,820,825,830,835,840,845,850,855,860,865,870,875,880,885,890,895,900,905,910,915,920,925,930,935,940,945,950,955,960,965,970,975,980,985,990,995,1000,1005,1010,1015,1020,1025,1030,1035,1040,1045,1050,1055,1060,1065,1070,1075,1080,1085,1090,1095,1100,1105,1110,1115,1120,1125,1130,1135,1140,1145,1150,1155,1160,1165,1170,1175,1180,1185,1190,1195,1200]

        #8 TeV#xsTh = [559.757,448.456,361.917,293.281,240.077,197.122,163.376,135.791,113.319,95.0292,80.268,68.0456,58.01,49.6639,42.6441,36.7994,31.8695,27.7028,24.1585,21.1597,18.5245,16.2439,14.3201,12.6497,11.1808,9.90959,8.78125,7.81646,6.96892,6.22701,5.57596,5.00108,4.48773,4.03416,3.63085,3.2781,2.95613,2.67442,2.42299,2.19684,1.99608,1.81486,1.64956,1.50385,1.3733,1.25277,1.14277,1.04713,0.959617,0.879793,0.807323,0.74141,0.681346,0.626913,0.576882,0.531443,0.489973,0.452072,0.4176,0.385775,0.35683,0.329881,0.305512,0.283519,0.262683,0.243755,0.226367,0.209966,0.195812,0.181783,0.169668,0.158567,0.147492,0.137392,0.128326,0.119275,0.112241,0.104155,0.0977878,0.091451,0.0855847,0.0801322,0.0751004,0.0703432,0.0660189,0.0618641,0.0580348,0.0545113,0.0511747,0.0481537,0.0452067,0.0424781,0.0399591,0.0376398,0.0354242,0.0333988,0.0313654,0.0295471,0.0279395,0.0263263,0.0248009,0.0233806,0.0220672,0.0208461,0.0196331,0.0185257,0.0175075,0.0164955,0.0155809,0.0147721,0.0139566,0.0132456,0.0125393,0.0118287,0.0112223,0.0106123,0.0100516,0.0095256,0.0090306,0.00856339,0.0081141,0.00769525,0.00730084,0.00692243,0.00656729,0.00623244,0.00591771,0.00561049,0.00532605,0.00506044,0.00480639,0.00455979,0.00433688,0.00412174,0.00391839,0.00372717,0.00354211,0.00336904,0.00320476,0.00304935,0.00289588,0.00275424,0.0026184,0.00249291,0.00237168,0.00226163,0.00214607,0.00204589,0.00195172,0.0018573,0.00176742,0.00168383,0.00160403,0.00153063,0.00145772,0.0013878,0.00132077,0.00126234,0.00120568,0.00114627,0.00109501,0.001044,0.000996193,0.00095071,0.000907494,0.000866391,0.000826533,0.000789573,0.000753768,0.000719675,0.000687022,0.000656279,0.000626876,0.000598955,0.000571551,0.000546728,0.000522495,0.000499017,0.000476255,0.000455959,0.000435488,0.000416116,0.00039791,0.000379994,0.000363934,0.000347646,0.00033204,0.000318049,0.000303756,0.000290392,0.000277943,0.000265929,0.000254659,0.000243251,0.00023289,0.000222651,0.000213396,0.000204211,0.000196038,0.000187913,0.000179699,0.000172125,0.000165045,0.000157905,0.000151236,0.000144737,0.000138657,0.000133343,0.000127478,0.00012234,0.000117215,0.000112199,0.000107256,0.000103046,9.86633E-05,9.44977E-05,9.05131E-05,8.67972E-05,8.31669E-05,7.96568E-05,7.63052E-05]
	xsTh = [1521.11,1233.18,1013.76,832.656,689.799,574.981,481.397,405.159,342.865,291.752,249.409,214.221,184.623,159.614,139.252,121.416,106.194,93.3347,82.2541,72.7397,64.5085,57.2279,50.9226,45.3761,40.5941,36.3818,32.6679,29.3155,26.4761,23.8853,21.5949,19.5614,17.6836,16.112,14.6459,13.3231,12.1575,11.0925,10.1363,9.29002,8.51615,7.81428,7.17876,6.60266,6.08444,5.60471,5.17188,4.77871,4.41629,4.08881,3.78661,3.50911,3.25619,3.02472,2.8077,2.61162,2.43031,2.26365,2.10786,1.9665,1.83537,1.70927,1.60378,1.49798,1.39688,1.31169,1.22589,1.14553,1.07484,1.01019,0.948333,0.890847,0.836762,0.787221,0.740549,0.697075,0.655954,0.618562,0.582467,0.549524,0.51848,0.489324,0.462439,0.436832,0.412828,0.390303,0.368755,0.348705,0.330157,0.312672,0.296128,0.280734,0.266138,0.251557,0.238537,0.226118,0.214557,0.203566,0.193079,0.183604,0.174599,0.166131,0.158242,0.150275,0.142787,0.136372,0.129886,0.123402,0.11795,0.112008,0.107045,0.102081,0.09725,0.0927515,0.0885084,0.0844877,0.0806192,0.0769099,0.0734901,0.0701805,0.0670476,0.0641426,0.0612942,0.0585678,0.0560753,0.0536438,0.0513219,0.0491001,0.0470801,0.045061,0.0431418,0.0413447,0.0396264,0.0379036,0.0363856,0.0348796,0.0334669,0.0320548,0.0307373,0.0295348,0.0283338,0.0272206,0.0261233,0.0251107,0.0241099,0.0230866,0.0221834,0.0213766,0.0204715,0.0197653,0.0189612,0.0182516,0.0175509,0.0168336,0.0162314,0.015625,0.0150143,0.0144112,0.0138979,0.0133962,0.0128895,0.0123843,0.0119837,0.0114713,0.0110688,0.0106631,0.0102629,0.0098874,0.00952142,0.00916636,0.00883465,0.00851073,0.00820884,0.00791403,0.00763112,0.00735655,0.00710317,0.00684867,0.00660695,0.00637546,0.00615134,0.00593765,0.00572452,0.00553094,0.00533968,0.00514619,0.00497235,0.00479906,0.00463806,0.00447537,0.00432261,0.00417983,0.00403886,0.0038962,0.00376343,0.00364174,0.00352093,0.00339813,0.00328695,0.00317628,0.00307413,0.00297377,0.00287148,0.00278078,0.00268873,0.00260821,0.00251529,0.00243484,0.00236295,0.00228192,0.00221047,0.00213907,0.00206845,0.0020063,0.00194569,0.0018741,0.00182266,0.00176211,0.00170006,0.00164968,0.00159844]


#### BETA ONE CHANNEL
if do_BetaOne == 1:

	masses = masses_betaone
	
	#masses=[200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000]
	#if 'LQ' in lqtype:
		#masses=[200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2000]
	#	masses=[300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3500, 4000]
	if 'BL' in lqtype:
		#masses=[125,150,175,200,300,400,500,600,700,800,900,1000,1100,1200]
		masses=[200,300,400,500,600,700,800,900,1000,1100,1200]
		#masses=[200]

	print "*"*40 + '\n BETA ONE ASYMPTOTIC CLS RESULTS\n\n' +"*"*40
	
	band1sigma = 'Double_t y_1sigma['+str(int(len(masses))*2)+']={'
	band1sigma1 = 'Double_t y_1sigma_1['+str(int(len(masses)))+']={'
	band1sigma2 = 'Double_t y_1sigma_2['+str(int(len(masses)))+']={'
	band2sigma = 'Double_t y_2sigma['+str(int(len(masses))*2)+']={'
	band2sigma1 = 'Double_t y_2sigma_1['+str(int(len(masses)))+']={'
	band2sigma2 = 'Double_t y_2sigma_2['+str(int(len(masses)))+']={'
	excurve = 'Double_t xsUp_expected['+str(int(len(masses)))+'] = {' 
	obcurve = 'Double_t xsUp_observed['+str(int(len(masses)))+'] = {'  
 	mcurve = 'Double_t mData['+str(int(len(masses)))+'] = {'  
 	scurve = 'Double_t x_shademasses['+str(int(len(masses)*2))+'] = {'  
	

	if do_fullHybrid == 1 :#do full Hybrid CLs
		BetaOneObs = BetaOneObsFreq
		BetaOne95down = BetaOne95downFreq
		BetaOne95up = BetaOne95upFreq
		BetaOne68down = BetaOne68downFreq
		BetaOne68up = BetaOne68upFreq
		BetaOneExp = BetaOneExpFreq

	ob = BetaOneObs 
	down2 = BetaOne95down 
	up2 = BetaOne95up 
	down1 = BetaOne68down 
	up1 = BetaOne68up 
	med = BetaOneExp 

	fac = 1.0
	sigma = []
	for x in range(len(mTh)):
		if (mTh[x]) in masses: 
			sigma.append(xsTh[x]*fac)
	for x in range(len(masses)):
		excurve += str(float(med[x])*float(sigma[x])) + ' , ' 
		if (len(ob)>0) and (not blind):
                        obcurve += str(float(ob[x])*float(sigma[x])) + ' , ' 
                else:
                        obcurve += '0 , '
		band1sigma += str(float(down1[x])*float(sigma[x])) + ' , ' 
		band1sigma1 += str(float(down1[x])*float(sigma[x])) + ' , ' 
		band2sigma += str(float(down2[x])*float(sigma[x])) + ' , ' 
		band2sigma1 += str(float(down2[x])*float(sigma[x])) + ' , ' 
		mcurve += str(float(masses[x])) + ' , '
		scurve += str(float(masses[x])) + ' , '

	for x in range(len(masses)):
		band1sigma += str(float(up1[-(x+1)])*float(sigma[-(x+1)])) + ' , ' 
		band2sigma += str(float(up2[-(x+1)])*float(sigma[-(x+1)])) + ' , ' 
		band1sigma2 += str(float(up1[x])*float(sigma[x])) + ' , ' 
		band2sigma2 += str(float(up2[x])*float(sigma[x])) + ' , ' 
		scurve += str(float(masses[-x-1])) + ' , '
	excurve += '}'
	obcurve += '}'
	mcurve += '}'
	scurve += '}'
	band1sigma += '}'
	band1sigma1 += '}'
	band1sigma2 += '}'
	band2sigma += '}'
	band2sigma1 += '}'
	band2sigma2 += '}'
	excurve = excurve.replace(' , }',' }; ' )
	obcurve = obcurve.replace(' , }',' }; ' )
	mcurve = mcurve.replace(' , }',' }; ' )
	scurve = scurve.replace(' , }',' }; ' )

	band1sigma = band1sigma.replace(' , }',' }; ' )
	band1sigma1 = band1sigma1.replace(' , }',' }; ' )
	band1sigma2 = band1sigma2.replace(' , }',' }; ' )
	band2sigma = band2sigma.replace(' , }',' }; ' )
	band2sigma1 = band2sigma1.replace(' , }',' }; ' )
	band2sigma2 = band2sigma2.replace(' , }',' }; ' )
	
	print '\n'
	print mcurve
	print scurve
	print excurve
	print obcurve
	print band1sigma
	print band1sigma1
	print band1sigma2
	print band2sigma
	print band2sigma1
	print band2sigma2
	print '\n'

#### BETA HALF CHANNEL
if do_BetaHalf == 1:

	masses = masses_betahalf
	print "*"*40 + '\n BETA HALF ASYMPTOTIC CLS RESULTS\n' +"*"*40
	
	band1sigma = 'Double_t y_1sigma['+str(int(len(masses)*2))+']={'
	band1sigma1 = 'Double_t y_1sigma_1['+str(int(len(masses)))+']={'
	band1sigma2 = 'Double_t y_1sigma_2['+str(int(len(masses)))+']={'
	band2sigma = 'Double_t y_2sigma['+str(int(len(masses)*2))+']={'
	band2sigma1 = 'Double_t y_2sigma_1['+str(int(len(masses)))+']={'
	band2sigma2 = 'Double_t y_2sigma_2['+str(int(len(masses)))+']={'
	excurve = 'Double_t xsUp_expected['+str(int(len(masses)))+'] = {' 
	obcurve = 'Double_t xsUp_observed['+str(int(len(masses)))+'] = {'  
 	mcurve = 'Double_t mData['+str(int(len(masses)))+'] = {'  
 	scurve = 'Double_t x_shademasses['+str(int(len(masses)*2))+'] = {'  

	
	ob = BetaHalfObs 
	down2 = BetaHalf95down 
	up2 = BetaHalf95up 
	down1 = BetaHalf68down 
	up1 = BetaHalf68up 
	med = BetaHalfExp 

	fac = 0.5
	sigma = []
	for x in range(len(mTh)):
		if (mTh[x]) in masses: 
			sigma.append(xsTh[x]*fac)
			# print '*',mTh[x],xsTh[x]
	
	for x in range(len(masses)):
		excurve += str(float(med[x])*float(sigma[x])) + ' , ' 
		obcurve += str(float(ob[x])*float(sigma[x])) + ' , ' 
		band1sigma += str(float(down1[x])*float(sigma[x])) + ' , ' 
		band1sigma1 += str(float(down1[x])*float(sigma[x])) + ' , ' 
		band2sigma += str(float(down2[x])*float(sigma[x])) + ' , ' 
		band2sigma1 += str(float(down2[x])*float(sigma[x])) + ' , ' 
		mcurve += str(float(masses[x])) + ' , '
		scurve += str(float(masses[x])) + ' , '
	
	for x in range(len(masses)):
		band1sigma += str(float(up1[-(x+1)])*float(sigma[-(x+1)])) + ' , ' 
		band2sigma += str(float(up2[-(x+1)])*float(sigma[-(x+1)])) + ' , ' 
		band1sigma2 += str(float(up1[x])*float(sigma[x])) + ' , ' 
		band2sigma2 += str(float(up2[x])*float(sigma[x])) + ' , ' 
		scurve += str(float(masses[-x-1])) + ' , '

	excurve += '}'
	obcurve += '}'
	mcurve += '}'
	scurve += '}'		
	band1sigma += '}'
	band1sigma1 += '}'
	band1sigma2 += '}'
	band2sigma += '}'
	band2sigma1 += '}'
	band2sigma2 += '}'
	excurve = excurve.replace(' , }',' }; ' )
	obcurve = obcurve.replace(' , }',' }; ' )
	mcurve = mcurve.replace(' , }',' }; ' )	
	scurve = scurve.replace(' , }',' }; ' )	
	band1sigma = band1sigma.replace(' , }',' }; ' )
	band1sigma1 = band1sigma1.replace(' , }',' }; ' )
	band1sigma2 = band1sigma2.replace(' , }',' }; ' )
	band2sigma = band2sigma.replace(' , }',' }; ' )
	band2sigma1 = band2sigma1.replace(' , }',' }; ' )
	band2sigma2 = band2sigma2.replace(' , }',' }; ' )
	

	print '\n'
	print mcurve
	print scurve	
	print excurve
	print obcurve
	print band1sigma
	print band1sigma1
	print band1sigma2
	print band2sigma
	print band2sigma1
	print band2sigma2
	print '\n'
	


#### COMBINATION CHANNEL
if do_combo == 1:

	print "*"*40 + '\n COMBINATION ASYMPTOTIC CLS RESULTS\n' +"*"*40

					

	sigma = []
	fac = 1.0
	for x in range(len(mTh)):
		if (mTh[x]) in masses: 
			sigma.append(xsTh[x]*fac)
	
	def re_eval(rlist):
		outlist = []
		for mset in rlist:
			newset = []
			for r_ind in range(len(mset)):
				newset.append(sigma[r_ind]*float(mset[r_ind]))		
			outlist.append(newset)
		return outlist
	
	s_ComboObs = re_eval(ComboObs)
	s_Combo95down = re_eval(Combo95down)
	s_Combo68down = re_eval(Combo68down)
	s_ComboExp = re_eval(ComboExp)
	s_Combo68up = re_eval(Combo68up)
	s_Combo95up = re_eval(Combo95up)
	
	s_ComboBetaOneObs = re_eval(ComboBetaOneObs)
	s_ComboBetaOne95down = re_eval(ComboBetaOne95down)
	s_ComboBetaOne68down = re_eval(ComboBetaOne68down)
	s_ComboBetaOneExp = re_eval(ComboBetaOneExp)
	s_ComboBetaOne68up = re_eval(ComboBetaOne68up)
	s_ComboBetaOne95up = re_eval(ComboBetaOne95up)
	
	s_ComboBetaHalfObs = re_eval(ComboBetaHalfObs)
	s_ComboBetaHalf95down = re_eval(ComboBetaHalf95down)
	s_ComboBetaHalf68down = re_eval(ComboBetaHalf68down)
	s_ComboBetaHalfExp = re_eval(ComboBetaHalfExp)
	s_ComboBetaHalf68up = re_eval(ComboBetaHalf68up)
	s_ComboBetaHalf95up = re_eval(ComboBetaHalf95up)


	from ROOT import *
	from array import array
		

	#xx = (spline.Eval(310));
	M_th=[ xm for xm in mTh]
	X_th=[ xx for xx in xsTh]
		
	mTh = array("d",mTh)
	xsTh = array("d",xsTh)
	

	g = TGraph(len(mTh),mTh,xsTh);
	spline = TSpline3("xsection",g) 
	
		
	def sigmaval(mval):
		return spline.Eval(mval)
		
	
	def mval(sigma):
		testm = 150
		oldtestm = 2000
		inc = 50
		dif = 55
		olddif = 000
		while abs(oldtestm - testm)>0.01:
			testsigma = sigmaval(testm)
			olddif = dif
			dif = testsigma -sigma
			if testm>1900:
				break
			if dif*olddif <= 0.0:
				inc = -inc/2.3
			oldtestm = testm
			#print '**' + str(testm) + '  ' + str(testsigma) +'  ' +str(dif) + '   ' + str(dif*olddif)
	
			testm = testm + inc
		return testm
	import math
	inputarrayX = []
	inputarrayY = []

	def loggraph(inputarrayX,inputarrayY):
		logarray = []
		for j in inputarrayY:
			logarray.append(math.log10(j))
		x = array("d",inputarrayX)
		y = array("d",logarray)
		g = TGraph(len(x),x,y)
		return g
		
	logtheory = loggraph(M_th,X_th)

	def logspline(inputarrayX,inputarrayY):
		logarray = []
		for j in inputarrayY:
			logarray.append(math.log(j))
		x = array("d",inputarrayX)
		y = array("d",logarray)
		g = TGraph(len(x),x,y)
		outspline = TSpline3("",g)
		return outspline
	
	from math import exp
	def get_intersection(spline1, spline2, xmin,xmax):
		num = xmax-xmin
		inc = (xmax - xmin)/num
		dif = []
		sdif = []
		x = xmin
		xvals = []
		xx = []
		yy = []
		xvals = []
		while x<xmax:
			thisdif = (exp(spline1.Eval(x)) - exp(spline2.Eval(x)))
			#print (str(x)) + '   ' + str(thisdif)
			xx.append(exp(spline1.Eval(x)))
			yy.append(exp(spline2.Eval(x)))
			sdif.append(thisdif)
			dif.append(abs(thisdif))
			xvals.append(x)
			#print  str(x) + '   ' +str(exp(spline1.Eval(x))) + '    '+str(exp(spline2.Eval(x))) + '    ' + str(thisdif)
			x = x+inc
		mindif = min(dif)
		bestmass = 0	
		
	
		for x in range(len(dif)-2):
			a = sdif[x]
			b = sdif[x+1]	
			#print str(xvals[x+1]) +'    '+str(a)  + '     ' +str(b) 
			if ((a/abs(a))*(b/abs(b))) < 0.0 and a >0.0 :
				#print 'Limit found at: '+ (str(xvals[x]))
				bestmass = xvals[x]
				break;
						
		return [bestmass,mindif]
		
	def get_simple_intersection(graph1, graph2, xmin,xmax):
		num = (xmax-xmin)*10
		inc = (xmax - xmin)/(1.0*num)

		dif = []
		sdif = []
		x = xmin +0.1
		xvals = []
		xx = []
		yy = []
		xvals = []
		while x<(xmax-.1):
			thisdif = (exp(graph1.Eval(x)) - exp(graph2.Eval(x)))
			#print (str(x)) + '   '+ str(xmax-.1) +'   '+ str(thisdif)
			xx.append(exp(graph1.Eval(x)))
			yy.append(exp(graph2.Eval(x)))
			sdif.append(thisdif)
			dif.append(abs(thisdif))
			xvals.append(x)
			#print  str(x) + '   ' +str(exp(graph1.Eval(x))) + '    '+str(exp(graph2.Eval(x))) + '    ' + str(thisdif)
			x = x+inc
		#print 'Done Looping for Difs'
		mindif = min(dif)
		bestmass = 0	
		
	
		for x in range(len(dif)-2):
			a = sdif[x]
			b = sdif[x+1]	
			#print str(xvals[x+1]) +'    '+str(a)  + '     ' +str(b) 
			if ((a/abs(a))*(b/abs(b))) < 0.0 and a >0.0 :
				print 'Limit found at: '+ (str(xvals[x]))
				bestmass = xvals[x]
				break;
						
		return [bestmass,mindif]
		


	def fill_mlists(clist):
		mlist = []
		for limit_set in clist:
			fitted_limits = loggraph(masses,limit_set)
			goodm = get_simple_intersection(logtheory,fitted_limits,200,2000)
			mlist.append(str(round(goodm[0],2)))
		return mlist
		
	m_ComboObs = fill_mlists(s_ComboObs)
	m_Combo95down = fill_mlists(s_Combo95down)
	m_Combo68down = fill_mlists(s_Combo68down)
	m_ComboExp = fill_mlists(s_ComboExp)
	m_Combo68up = fill_mlists(s_Combo68up)
	m_Combo95up = fill_mlists(s_Combo95up)

	m_ComboBetaOneObs = fill_mlists(s_ComboBetaOneObs)
	m_ComboBetaOne95down = fill_mlists(s_ComboBetaOne95down)
	m_ComboBetaOne68down = fill_mlists(s_ComboBetaOne68down)
	m_ComboBetaOneExp = fill_mlists(s_ComboBetaOneExp)
	m_ComboBetaOne68up = fill_mlists(s_ComboBetaOne68up)
	m_ComboBetaOne95up = fill_mlists(s_ComboBetaOne95up)

	m_ComboBetaHalfObs = fill_mlists(s_ComboBetaHalfObs)
	m_ComboBetaHalf95down = fill_mlists(s_ComboBetaHalf95down)
	m_ComboBetaHalf68down = fill_mlists(s_ComboBetaHalf68down)
	m_ComboBetaHalfExp = fill_mlists(s_ComboBetaHalfExp)
	m_ComboBetaHalf68up = fill_mlists(s_ComboBetaHalf68up)
	m_ComboBetaHalf95up = fill_mlists(s_ComboBetaHalf95up)
	
	
	betav = []
	for x in betas:
		betav.append(str(round(x,4)))
	betastring = 'static int numbetas = '+str(len(betas))+';\n'+'Double_t beta_vals['+str(len(betas))+'] = {' +str(betav).replace('[','').replace(']','').replace('\'','')+'};'

	band1sigma_combo = 'Double_t m_1sigma_combo['+str(2*len(betas))+']={'
	band2sigma_combo = 'Double_t m_2sigma_combo['+str(2*len(betas))+']={'
	excurve_combo = 'Double_t m_expected_combo['+str(len(betas))+'] = {' 
	obcurve_combo = 'Double_t m_observed_combo['+str(len(betas))+'] = {'  

	band1sigma_lljj = 'Double_t m_1sigma_lljj['+str(2*len(betas))+']={'
	band2sigma_lljj = 'Double_t m_2sigma_lljj['+str(2*len(betas))+']={'
	excurve_lljj = 'Double_t m_expected_lljj['+str(len(betas))+'] = {' 
	obcurve_lljj = 'Double_t m_observed_lljj['+str(len(betas))+'] = {'  
	
	band1sigma_lvjj = 'Double_t m_1sigma_lvjj['+str(2*len(betas))+']={'
	band2sigma_lvjj = 'Double_t m_2sigma_lvjj['+str(2*len(betas))+']={'
	excurve_lvjj = 'Double_t m_expected_lvjj['+str(len(betas))+'] = {' 
	obcurve_lvjj = 'Double_t m_observed_lvjj['+str(len(betas))+'] = {'  
	
	
	excurve_combo += str(m_ComboExp).replace('[','').replace(']','').replace('\'','')+'};'
	obcurve_combo += str(m_ComboObs).replace('[','').replace(']','').replace('\'','')+'};'

	excurve_lljj += str(m_ComboBetaOneExp).replace('[','').replace(']','').replace('\'','')+'};'
	obcurve_lljj += str(m_ComboBetaOneObs).replace('[','').replace(']','').replace('\'','')+'};'
	
	excurve_lvjj += str(m_ComboBetaHalfExp).replace('[','').replace(']','').replace('\'','')+'};'
	obcurve_lvjj += str(m_ComboBetaHalfObs).replace('[','').replace(']','').replace('\'','')+'};'	

	m_Combo68up.reverse()
	m_Combo95up.reverse()

	m_ComboBetaOne68up.reverse()
	m_ComboBetaOne95up.reverse()
	
	m_ComboBetaHalf68up.reverse()
	m_ComboBetaHalf95up.reverse()
	
		
	band1sigma_combo += str(m_Combo68down).replace('[','').replace(']','').replace('\'','')+ ', '+  str(m_Combo68up).replace('[','').replace(']','').replace('\'','')+'};'
	band2sigma_combo += str(m_Combo95down).replace('[','').replace(']','').replace('\'','') + ', '+ str(m_Combo95up).replace('[','').replace(']','').replace('\'','')+'};'

	band1sigma_lljj += str(m_ComboBetaOne68down).replace('[','').replace(']','').replace('\'','') + ', '+  str(m_ComboBetaOne68up).replace('[','').replace(']','').replace('\'','')+'};'
	band2sigma_lljj += str(m_ComboBetaOne95down).replace('[','').replace(']','').replace('\'','') + ', '+ str(m_ComboBetaOne95up).replace('[','').replace(']','').replace('\'','')+'};'
	
	band1sigma_lvjj += str(m_ComboBetaHalf68down).replace('[','').replace(']','').replace('\'','') + ', '+  str(m_ComboBetaHalf68up).replace('[','').replace(']','').replace('\'','')+'};'
	band2sigma_lvjj += str(m_ComboBetaHalf95down).replace('[','').replace(']','').replace('\'','') + ', '+ str(m_ComboBetaHalf95up).replace('[','').replace(']','').replace('\'','')+'};'
	
	
	
	print '\n'
	print betastring
	print '\n'
	print excurve_combo
	print obcurve_combo
	print band1sigma_combo
	print band2sigma_combo

	print '\n'
	print excurve_lljj
	print obcurve_lljj
	print band1sigma_lljj
	print band2sigma_lljj
	
	print '\n'
	print excurve_lvjj
	print obcurve_lvjj
	print band1sigma_lvjj
	print band2sigma_lvjj	
	print '\n'
	print '\n'
	
	
