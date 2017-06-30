from __init__ import *

def k_means_doa(temp , gas):
	temp.temp = list()
	result = list()
	i = 0
	while i < len(temp.toa):
		temp.temp.append(1)
		i = i + 1
	i = 0
	while i<len(temp.toa):
		j = 0
		if not temp.temp[i] == 0:
			ID = list()
			set = PDW()
			set.cf.append(temp.cf[i])
			set.doa_fw.append(temp.doa_fw[i])
			set.doa_fy.append(temp.doa_fy[i])
			set.toa.append(temp.toa[i])
			set.pw.append(temp.toa[i])
			temp.temp[i] = 0
			ID.append(i)
			while j<len(temp.toa):
				if not temp.temp[j] == 0:
					if abs(temp.doa_fw[j] - set.doa_fw[0]) <= gas and abs(temp.doa_fy[j] - set.doa_fy[0]) <= gas:
						set.cf.append(temp.cf[j])
						set.doa_fw.append(temp.doa_fw[j])
						set.doa_fy.append(temp.doa_fy[j])
						set.toa.append(temp.toa[j])
						set.pw.append(temp.pw[j])
						ID.append(j)
						temp.temp[j] = 0
				j = j + 1
			if len(set.toa) < 20:
				for a in range(0,len(ID)):
					temp.temp[a] = 1
			else:
				result.append(set)
		i = i + 1
	print('set_doa\'s number is : %d' % len(result))
	a = 1
	for cell in result:
		print('set %d\'s pulse number is : %d' % (a,len(cell.toa)))
		a = a + 1
	return result

def k_means_cf(temp , gas):
	temp.temp = list()
	result = list()
	cf_pulse = PDW()
	i = 0
	while i < len(temp.toa):
		temp.temp.append(1)
		i = i + 1	
	i = 0
	while i<len(temp.toa):
		j = 0
		if not temp.temp[i] == 0:
			ID = []
			set = PDW()
			set.cf.append(temp.cf[i])
			set.doa_fw.append(temp.doa_fw[i])
			set.doa_fy.append(temp.doa_fy[i])
			set.toa.append(temp.toa[i])
			set.pw.append(temp.pw[i])
			temp.temp[i] = 0
			ID.append(i)
			while j<len(temp.toa):
				if not temp.temp[j] == 0:
					if abs(temp.cf[j] - set.cf[0]) <= gas and abs(temp.cf[j] - set.cf[0]) <= gas:
						set.cf.append(temp.cf[j])
						set.doa_fw.append(temp.doa_fw[j])
						set.doa_fy.append(temp.doa_fy[j])
						set.toa.append(temp.toa[j])
						set.pw.append(temp.pw[j])
						ID.append(j)
						temp.temp[j] = 0
				j = j + 1
			if len(set.toa) < 20:
				for a in range(0,len(ID)):
					temp.temp[ID[a]] = 1
			else:
				result.append(set)
		i = i + 1
	print('set_cf\'s number is : %d' % len(result))
	a = 1
	for index , a in enumerate(temp.temp):
		if a == 1:
			cf_pulse.cf.append(temp.cf[index])
			cf_pulse.pw.append(temp.pw[index])
			cf_pulse.toa.append(temp.toa[index])
			cf_pulse.doa_fw.append(temp.doa_fw[index])
			cf_pulse.doa_fy.append(temp.doa_fy[index])
	for cell in result:
		print('set %d\'s pulse number is : %d' % (a,len(cell.toa)))
		a = a + 1
	return result , cf_pulse

def k_means_cenci(temp , gas):
	result = []
	cenci_pri = []
	temp.toaf = temp.toa[0:len(temp.toa)-1]
	temp.toan = temp.toa[1:len(temp.toa)]
	toac_pri = []
	toac_pri = sorted(map(lambda x:x[0]-x[1] , zip(temp.toan,temp.toaf)))
	# print(len(toac_pri))
	i = 0
	toac_temp = []
	while i < len(toac_pri):
		toac_temp.append(1)
		i = i + 1
	i = 0 
	while i < len(toac_pri):
		j = 0
		if not toac_temp[i] == 0:
			ID = []
			toac_temp[i] = 0
			ID.append(toac_pri[i])
			while j < len(toac_pri):
				if not toac_temp[j] == 0:
					if abs(toac_pri[j] - sum(ID)/len(ID) <= gas):
						ID.append(toac_pri[j])
						toac_temp[j] = 0
				j = j + 1
			cenci_pri.append(ID)
		i = i + 1
	for a in cenci_pri:
		# print(sum(a)/len(a))
		result.append(sum(a)/len(a))
	return result