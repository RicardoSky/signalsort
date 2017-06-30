class PDW:
	def __init__(self):
		self.cf = list()
		self.doa_fw = list()
		self.doa_fy = list()
		self.toa = list()
		self.pw = list()
class SDF:
	def __init__(self):
		self.min = 0
		self.ave = 0
		self.num = 0
		self.theorynum = 0

class radar_parameter:
	def __init__(self):
		self.pri = 0
		self.pw = 0
		self.cf = 0
		self.type = 0		## 1-constant 2-stagger 3-jitter 4-frequency hop
		self.doa_fw = 0
		self.doa_fy = 0
		self.jitter_ratio = 0
		self.cf_hop = 0
		self.cf_hop_num = 0

def radar_type(temp):
	switcher = {
	1:'constant',
	2:'stagger',
	3:'jitter',
	4:'frequency hop',
	}
	return switcher.get(temp , 'none')