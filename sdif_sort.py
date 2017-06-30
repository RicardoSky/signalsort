from __init__ import *


def sdif_algorithm(temp):
	time_start_end = temp.toa[len(temp.toa)-1] - temp.toa[0]
	toa_tao = 40
	result_c = list()
	for toac in range(1,11):
		result = list()
		temp.toaf = temp.toa[0:len(temp.toa)-toac]
		temp.toan = temp.toa[toac:len(temp.toa)]
		toac_pri = list()
		toac_pri = sorted(map(lambda x:x[1]-x[0] , zip(temp.toaf,temp.toan)))
		# print(toac_pri)
		sdf = SDF()
		sdf.min = toac_pri[0]
		sdf.ave = toac_pri[0]
		sdf.num = 1
		toac_i = 1
		while toac_i < len(toac_pri):
			if abs(toac_pri[toac_i] - sdf.ave) > toa_tao and abs(toac_pri[toac_i] - sdf.ave) > 0.2 * sdf.ave or toac_i == len(toac_pri)-1:
				sdf.theorynum = time_start_end / sdf.ave
				result.append(sdf)
				# print(sdf.num , sdf.theorynum , sdf.ave)
				if not toac_i == len(toac_pri)-1:
					sdf = SDF()
					sdf.min = toac_pri[toac_i]
					sdf.ave = toac_pri[toac_i]
					sdf.num = 1
				toac_i = toac_i + 1
			else:
				sdf.num = sdf.num + 1
				sdf.ave = (sdf.ave * (sdf.num-1) + toac_pri[toac_i]) / sdf.num
				toac_i = toac_i + 1
		num = 0
		for cache in result:
			if cache.num >= cache.theorynum * 0.8:
				print(toac ,cache.num , cache.theorynum, cache.ave)
				num = num + 1
				pri = cache.ave
		if num == 1:
			return pri
			break
		else:
			if not num == 1 and toac == 10:
				return 0
		
def parameter(temp):
	result = []
	for a in temp:
		radar = radar_parameter()
		pri = sorted(map(lambda x:x[0]-x[1] , zip(a.toa[2:len(a.toa)],a.toa[1:len(a.toa)-1])))
		for b , index in enumerate(pri):
			if b > 2 * a.pri:
				break
		pri = pri[0:index]
		# print(type(pri))
		radar.pri = sum(pri) / len(pri)
		b = 0
		for c in pri:
			if abs(c - radar.pri) > b:
				b = abs(c - radar.pri)
		radar.jitter_ratio = b / radar.pri
		radar.pw = sum(a.pw) / len(a.pw)
		radar.doa_fw = sum(a.doa_fw) / len(a.doa_fw)
		radar.doa_fy = sum(a.doa_fy) / len(a.doa_fy)
		radar.cf = sum(a.cf) / len(a.cf)
		result.append(radar)
	# for a in result:
		# print(a.pri , a.pw , a.doa_fw , a.doa_fy , a.cf , a.jitter_ratio)
	return result	
	
