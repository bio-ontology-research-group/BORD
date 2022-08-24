import json, math, pickle, sys
dic=json.load(open(sys.argv[1])) #direct children json file
IC={}
maxi=0
full_dic={}
dic['owl:Nothing']=[]
from tqdm import tqdm 

def get_all_children(parent):
	children=list(set(dic[parent]))
	for c in children:
		children += get_all_children(c)
	return set(children)
		
			

for i, term in tqdm(enumerate(dic)):
	aterm=term[term.rfind('/')+1:].replace('_',':')
	children=get_all_children(term)
	full_dic[aterm]=[term[term.rfind('/')+1:].replace('_',':') for term in children]
	IC[aterm]=len(children)
	if IC[aterm]>maxi:
		maxi=IC[aterm]
	
mini=0
miniv=''
for key, value in IC.items():
	try:
		IC[key]=-math.log10(float(value/maxi))
	except:
		print('check:',value, key)
	if IC[key]>mini:
		miniv=key
	mini=max(mini,IC[key])

print(mini, miniv)
f=open('ifiles/struct_IC.pkl','wb')
f.write(pickle.dumps(IC))
f.close()
f=open('ifiles/all_children.pkl','wb')
f.write(pickle.dumps(full_dic))
f.close()
