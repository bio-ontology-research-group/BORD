from tqdm import tqdm
def get_abbr(abbr_file):
	dic={}
	f=open(abbr_file)
	for l in f:
		p=l.rstrip().split('\t')
		pmid=p[0][5:]
		if pmid not in dic:
			dic[pmid]={}
		dic[pmid][p[1]]=p[2]
	return dic
def get_abs_dict(tlines):
        abstract_text={}
        current_absID=''
        current_absTX=''
        for t in tlines:
                if 'PMID=' in t:
                        if len(current_absTX)>0:
                                abstract_text [current_absID] = ''.join(current_absTX)
                        current_absTX = []
                        current_absID = t[t.find('=')+1:t.find('\t')]
                        continue
                if len(t)<3:
                        continue
                token=t.split('\t')
                current_absTX.append(token[0])
                current_absTX.append(' ')
        abstract_text [current_absID] = ''.join(current_absTX)
        return abstract_text
def write_pubtator(abs_dict, pairs, ofile):
        curr_idx=0
        f=open(ofile,'w+')
        for ID, txt in abs_dict.items():
                if len(txt)<2:
                        continue
                tidx=txt.find('!')
                f.write(ID+'|t|'+txt[:tidx]+'\n')
                f.write(ID+'|a|'+txt[tidx+1:]+'\n')
                while curr_idx < len(pairs):
                        if pairs[curr_idx][-1]!=ID:
                                curr_idx+=1
                                continue
                        p=pairs[curr_idx]
                        for pred in p[1]:
                            f.write(p[-1]+'\t'+str(p[2][0])+'\t'+str(p[2][1])+'\t'+txt[(p[2][0]):(p[2][1])]+'\tPhenotype\t'+pred+'\n')
                        curr_idx+=1
                f.write('\n')
                curr_idx=0
	
def get_pred(pred_file, abbr_file, original_pubtator):
	abstracts=open(original_pubtator).read().split('\n\n')
	abst_dic={}
	for abst in abstracts:
		index=abst.find('|')
		if index<1:
			continue
		nl_index=abst.find('\n')
		ID=abst[:index]
		abst_dic[ID]=abst[index+3:nl_index]+'!'+abst[nl_index+len(ID)+4:]
	abbr_dic=get_abbr(abbr_file)
	current_id=''
	current_idx=0
	current_abs=''
	pcurrent, pairs=[], []
	plines=open(pred_file).readlines()
	for pline in plines:
		if 'PMID=' in pline:
			current_idx=0
			current_id=pline[pline.find('=')+1:pline.find('\t')]
			current_abs=abst_dic[current_id]
			continue
		if len(pline)<3:
			continue
		ptoken = pline.split('\t')
		if current_idx == 0:
			current_idxi = current_abs.find(ptoken[0])
			if current_idxi>-1:
				current_idx=current_idxi
		else:
			current_idxi = current_abs.find(ptoken[0], current_idx)
			if current_idxi>-1:
				current_idx=current_idxi
		pred_label = ptoken[1].rstrip()
		if current_id in abbr_dic and ptoken[0] in abbr_dic[current_id]:
			pass
		elif pred_label[0]=='I' and len(pcurrent)>0:
			pcurrent[0]+=' '+ptoken[0]
			pcurrent[2][1]=current_idx+len(ptoken[0])
		elif pred_label=='B':
			pcurrent=['',['UNASSIGNED'],[-1,-1],current_id]
			pcurrent[0]=ptoken[0]
			pcurrent[2][0]=current_idx
			pcurrent[2][1]=current_idx+len(ptoken[0])
		elif pred_label=='O' and len(pcurrent)>0:
			pairs.append(pcurrent)
			pcurrent=[]
		if current_id in abbr_dic and pred_label=='B' and ptoken[0] in abbr_dic[current_id]:
			pairs.append([abbr_dic[current_id][ptoken[0]].replace('-',' - '),['UNASSINGED'],[current_idx,current_idx+len(ptoken[0])],current_id])
	return pairs, abst_dic
if __name__=='__main__':
	pairs, abst_dic=get_pred('predictions.medmentions.74K.txt','u.abbr.list.mm.test.txt','pubtator.txt')
	write_pubtator(abst_dic, pairs, 'output.txt')
