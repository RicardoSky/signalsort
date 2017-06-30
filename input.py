

def input():
	TOA = list()
	DOA_FW = list()
	DOA_FY = list()
	CF = list()
	PW = list()

	f = open('D:\\work\\TOA.txt','r')
	for line in f.readlines():
		line = int(line.strip())
		TOA.append(line)
	f.close()
	
	f = open('D:\\work\\DOA_fangwei.txt','r')
	for line in f.readlines():
		line = int(line.strip())
		DOA_FW.append(line)
	f.close()
	
	f = open('D:\\work\\DOA_fuyang.txt','r')
	for line in f.readlines():
		line = int(line.strip())
		DOA_FY.append(line)
	f.close()
	
	f = open('D:\\work\\cf.txt','r')
	for line in f.readlines():
		line = int(line.strip())
		CF.append(line)
	f.close()
	
	f = open('D:\\work\\PW.txt','r')
	for line in f.readlines():
		line = int(line.strip())
		PW.append(line)
	f.close()
	return TOA , DOA_FW , DOA_FY , CF , PW