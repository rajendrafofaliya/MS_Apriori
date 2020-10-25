import re
from operator import *

MS = {}
sdc = 0
F = [[],[],[],[],[],[]]
C = [[],[],[],[],[],[]]
L = []

def level2_candidate_gen(L, sdc, MS, sc):
	i = 0
	temp = []
	for l in L:
		i +=1
		if sc[l] >= MS[l]:
			for h in L[i:]:
				if sc[h] >= MS[l] and abs(sc[h] - sc[l]) <= sdc:
					t = l,h
					temp.append(t)
	return temp

###############################################################

def MSCandidate_gen(F, sdc, sc, k, MS):
	temp = []
	i=0
	for f1 in F:
		for f2 in F:
			if f1 != f2:
				if (f1[len(f1)-1]<f2[len(f2)-1]) and (f1[:-1] == f2[:-1]) and abs(sc[f1[len(f1)-1]] - sc[f2[len(f2)-1]]) <= sdc:
					temp.append(f1+f2[-1:])
					c = f1+f2[-1:]

					for k in range(1,len(c)+1):
						s = c[:k-1] + c[k:]
						if c[0] in s or MS[c[1]] == MS[c[0]]:
							if s not in F:
								temp.remove(c)
								break

	return temp

###############################################################

data = open("para-2.txt", "r+").readlines()
dataf = [line.rstrip('\n') for line in data]
for line in dataf:
	if line.find("M")> -1:
		key = int(line[line.find("(")+1:line.find(")")])
		value = float((line[line.find("= ")+1:]).strip())
		MS[key] = value
	if line.find('SDC') > -1:
		sdc = float((line[line.find("= ")+1:]).strip())

###############################################################

file = open("data-2.txt", "r+").readlines()
filef = [line.rstrip('\n') for line in file]
transaction = [[int(n) for n in re.split('{|}|, ', line) if n.isdigit()] for line in filef]

M = sorted(MS.items(), key=itemgetter(1))

###############################################################

cv = MS.copy()
for key,value in cv.items():
	cv[(key)] = 0

for trans in transaction:
	for item in trans:
		cv[item] += 1

sc = cv
final_support_count = sc.copy()
number_of_transactions = len(transaction)
for item, count in sc.items():
	sc[item] = float(count/number_of_transactions)

conf_flag = True
for (i, mis_val) in M:
	if sc[i] >= MS[i] and conf_flag:
		L.append(i)
		min_mis_reqiured = MS[i]
		conf_flag = False
	elif not conf_flag:
		if sc[i] >= min_mis_reqiured:
			L.append(i)

for l in L:
	if sc[l] >= MS[l]:
		F[1].append(l)
		#print(F)

k = 2

while F[k-1] : 
	if k == 2:
		C[k].extend(level2_candidate_gen(L, sdc, MS, sc))

	else:
		C[k].extend(MSCandidate_gen(F[k-1], sdc, sc,k, MS)) 
	temp_dict = {} 
	for c in C[k]:
		temp_dict[c] = 0
 
	for trans in transaction:
		for c in C[k]:
			if set(c).issubset(trans):
				temp_dict[c] += 1

	for c,value in temp_dict.items():
		if temp_dict[c]/number_of_transactions >= MS[c[0]]:
			F[k].append(c)
			sc[c] = temp_dict[c]/number_of_transactions
			final_support_count[c] = temp_dict[c]
	
	k = k + 1

Final_f = []
for val in F:
	if len(val)>0:
		final_dict = dict()
		for s in val:
			final_dict[s] = final_support_count[s]
		Final_f.append(final_dict)

res = ""
out_file = open("1_2_result.txt", "w")
out_file.write("(678147784\n")
if len(Final_f) == 0:
	res = res + "Length-1 0"
	
set_num = 1
for freq_sets in Final_f:
	res = res + "(Length-" + str(set_num)
	res = res + " " + str(len(freq_sets)) + "\n"
	for sets in freq_sets:
		if set_num == 1:	
			res = res + " ("  + str(sets) + ")\n"
		if set_num > 1:
			res = res + " (" + " ".join(list(map(str,sets))) + ")\n"
	res = res + ")\n"
	set_num = set_num + 1
out_file.write(res)
out_file.write(")")
out_file.close()