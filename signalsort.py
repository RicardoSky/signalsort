from input import *
from __init__ import *
from k_means import *
from sdif_sort import *
from numpy import *

def sequence_sort(temp , n , pri_range):
	temp_jitter = temp
	result = []	
	nn = 0
	while len(temp.toa)>= n and not nn == len(temp.toa):
		nn = len(temp.toa)
		pri = sdif_algorithm(temp)
		# print(pri)
		i = 0
		i_id = 0
		if not pri == 0:
			while i<len(temp.toa)-1:
				if i_id > 5:
					break
				for j in range(i+1 , len(temp.toa)):			
					prii = temp.toa[j] - temp.toa[i]
					if abs(prii - pri) <= pri_range:
						i_id = i_id + 1
						i = j
						break
					else:
						if j == len(temp.toa)-1 or prii > pri * 2:
							i_id = 0
							i = i + 1
							break
		if i_id > 5:
			if pri_range == 0:
				pri_range = pri * 0.2
			toa_sequence_id = [] #分选序列
			toa_sequence = PDW()
			pulse_i = 0
			while pulse_i < len(temp.toa)-1:
				temp_toa_id = []
				for index , i in enumerate(temp.toa):
					prii = i - temp.toa[pulse_i]
					if abs(prii - pri) < pri_range:
						temp_toa_id.append(index)
					else:
						if prii > pri*2:
							break
				if len(temp_toa_id) == 1:
					toa_sequence_id.append(temp_toa_id[0])
					# print(temp_toa_id[0])
					pulse_i = temp_toa_id.pop()
				else:
					if len(temp_toa_id) > 1:
						min = pri
						min_toa = 0
						min_id = 0
						for a in temp_toa_id:
							if abs(temp.toa[a]-temp.toa[pulse_i]) < min:
								min = abs(temp.toa[a]-temp.toa[pulse_i])
								min_toa = temp.toa[a]
								min_id = a
						pulse_i = min_id
						# print(min_id)
						toa_sequence_id.append(min_id)
					else:
						pulse_i = pulse_i + 1
			if len(toa_sequence_id) > n:
				for a in range(0,len(toa_sequence_id)):
					toa_sequence.toa.append(temp.toa.pop(toa_sequence_id[a]-a))
					toa_sequence.cf.append(temp.cf.pop(toa_sequence_id[a]-a))
					toa_sequence.pw.append(temp.pw.pop(toa_sequence_id[a]-a))
					toa_sequence.doa_fw.append(temp.doa_fw.pop(toa_sequence_id[a]-a))
					toa_sequence.doa_fy.append(temp.doa_fy.pop(toa_sequence_id[a]-a))
				toa_sequence.pri = pri
				result.append(toa_sequence)
	for a in result:
		print('****************result****************')
		print('sorted pulse number : %d' % len(a.toa))
	return result , temp

def cf_sequence(temp):
	cf_pulse = PDW()
	for a in temp:
		cf_pulse.cf = cf_pulse.cf + a.cf
		cf_pulse.toa = cf_pulse.toa + a.toa
		cf_pulse.pw = cf_pulse.pw + a.pw
		cf_pulse.doa_fw = cf_pulse.doa_fw + a.doa_fw
		cf_pulse.doa_fy = cf_pulse.doa_fy + a.doa_fy
	for a in range(0,len(cf_pulse.cf)):
		for b in range(a+1,len(cf_pulse.cf)):
			if cf_pulse.toa[a] > cf_pulse.toa[b]:
				cf_pulse_temp = cf_pulse.toa[b]
				cf_pulse.toa[b] = cf_pulse.toa[a]
				cf_pulse.toa[a] = cf_pulse_temp
				
				cf_pulse_temp = cf_pulse.cf[b]
				cf_pulse.cf[b] = cf_pulse.cf[a]
				cf_pulse.cf[a] = cf_pulse_temp
				
				cf_pulse_temp = cf_pulse.pw[b]
				cf_pulse.pw[b] = cf_pulse.pw[a]
				cf_pulse.pw[a] = cf_pulse_temp
				
				cf_pulse_temp = cf_pulse.doa_fw[b]
				cf_pulse.doa_fw[b] = cf_pulse.doa_fw[a]
				cf_pulse.doa_fw[a] = cf_pulse_temp
				
				cf_pulse_temp = cf_pulse.doa_fy[b]
				cf_pulse.doa_fy[b] = cf_pulse.doa_fy[a]
				cf_pulse.doa_fy[a] = cf_pulse_temp
	# print(len(cf_pulse.toa))
	return cf_pulse

###main
pdw = PDW()
[pdw.toa , pdw.doa_fw , pdw.doa_fy , pdw.cf , pdw.pw] = input()
emitter = []
print('********************************DOA_SORT********************************')
result_doa = k_means_doa(pdw , 5)
for set_doa in result_doa:
	print('**********************CF_SORT**********************')
	unsort_result = []
	unsort_pulse = PDW()
	[result_cf , unsort_pulse] = k_means_cf(set_doa , 20)
	unsort_result.append(unsort_pulse)
	sorted_pulse = PDW()
	unsort_pulse = PDW()
	for set_cf in result_cf:
		print('****************MAIN_SORT****************')
		[sorted_pulse , unsort_pulse] = sequence_sort(set_cf , 10 , 40) ##pulse
		if len(sorted_pulse) == 0:
			[sorted_pulse , unsort_pulse] = sequence_sort(unsort_pulse , 10 , 0)
		unsort_result.append(unsort_pulse)
		b = parameter(sorted_pulse)   ##parameter
		
	### stagger radar
		cenci_pri_judge = zeros((len(b),len(b)))
		id = []
		for i in range(0,len(b)):
			for j in range(i+1,len(b)):
				cenci_pri_judge[i][j] = abs(b[i].pri-b[j].pri) /(b[i].pri+b[j].pri)
				if cenci_pri_judge[i][j] < 0.1:
					id.append(i)
					id.append(j)
		# print(cenci_pri_judge)
		id = list(set(id))
		if len(id) >= 2:
			c = []
			for i in id:
				c.append(sorted_pulse[i])
			cenci_pulse = cf_sequence(c)
			# print(len(cenci_pulse.toa))
			emitter_cenci = radar_parameter()
			emitter_cenci.pri = k_means_cenci(cenci_pulse , 40)
			emitter_cenci.pw = sum(cenci_pulse.pw)/len(cenci_pulse.pw)
			emitter_cenci.cf = sum(cenci_pulse.cf)/len(cenci_pulse.cf)
			emitter_cenci.doa_fw = sum(cenci_pulse.doa_fw)/len(cenci_pulse.doa_fw)
			emitter_cenci.doa_fy = sum(cenci_pulse.doa_fy)/len(cenci_pulse.doa_fy)
			emitter_cenci.type = 2
			emitter.append(emitter_cenci)
			for i in range(0,len(id)):
				b.pop(id[i]-i)
	###	jitter radar
		for i in b:
			if i.jitter_ratio < 0.05:
				i.type = 1
				emitter.append(i)
			else:
				i.type = 3
				emitter.append(i)		
	print('****************HOP-FREQUENCY****************')
	unsort_pulse = cf_sequence(unsort_result)
	if len(unsort_pulse.toa) > 40:
		# fre_hop_pulse = PDW()
		[frehop_pulse , trash] = sequence_sort(unsort_pulse , 20 , 40)	##pulse
		for a in frehop_pulse:
			fre = sorted(a.cf)
			# print(fre)
			fre2 = sorted(map(lambda x:x[0]-x[1] ,zip(fre[1:len(fre)],fre[0:len(fre)-1])))
			# print(fre2)
			for index , b in enumerate(fre2):
				if b > 20:
					break
			emitter_hopfre = radar_parameter()
			emitter_hopfre.pri = []
			emitter_hopfre.pri.append(a.pri)
			emitter_hopfre.cf_hop_num = len(fre2) - index + 1
			emitter_hopfre.cf_hop = (fre[len(fre)-1] - fre[0]) / emitter_hopfre.cf_hop_num
			emitter_hopfre.pw = sum(a.pw) / len(a.pw)
			emitter_hopfre.cf = fre
			emitter_hopfre.doa_fw = sum(a.doa_fw) / len(a.doa_fw)
			emitter_hopfre.doa_fy = sum(a.doa_fy) / len(a.doa_fy)
			emitter_hopfre.type = 4
			emitter.append(emitter_hopfre)
print('****************RADAR TYPE****************')
for a in emitter:
	print('cf:' , a.cf)
	print('type: %s' % radar_type(a.type))
	if type(a.pri) == list:
		for b in a.pri:
			print('pri: %f' % b)
	else:
		print('pri:%f' % a.pri)
	print('pw: %d' % a.pw)
	print('doa_fw: %d' % a.doa_fw)
	print('doa_fy: %d' % a.doa_fy)
	print('hop: %d' % a.cf_hop)
	print('hop_num: %d' % a.cf_hop_num)
	print('*******************************')