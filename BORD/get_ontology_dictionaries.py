from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import os, inflect, pickle, math, nltk, sys, string
from nltk.corpus import stopwords
import re
p = inflect.engine()
stop_words={x:True for x in stopwords.words('english')}
stop_words["'"]=True
stop_words[","]=True
stop_words['-']=True
stop_words['(']=True
stop_words[')']=True
stop_words['"']=True
del(stop_words['as'])
lemmatizer = WordNetLemmatizer()
def get_pos(tag):
    res=''
    if tag.startswith('R') or tag=='IN':
        res=wordnet.ADV
    if tag.startswith('J'):
        res=wordnet.ADJ
    elif tag.startswith('V'):
        res=wordnet.VERB
    elif tag.startswith('N'):
        res=wordnet.NOUN
    else:
        res=wordnet.NOUN
    return res

def build_dict(filename):
    f=open(filename,encoding='utf-8')
    fout=open('ifiles/all.dic','w+')
    content=f.read().strip().split('\n\n')
    f.close()
    obo_dic={}
    for i,l in enumerate(content):
        if i<2:
            continue
        lines=l.split('\n')
        first_name=[]
        seen_synonyms=[]
        class_id=0
        for line in lines:
            if line.startswith('id: ')>0:
                class_id=line[len('id: '):]
            elif 'name:' in line:
                name=line[len('name: '):].lower().replace("'s","")
                name=re.sub(' +',' ',name.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))).strip()
                tokens = word_tokenize(name)
                token_pos = nltk.pos_tag(tokens)
                lemmas = [lemmatizer.lemmatize(token[0], get_pos(token[1])) for token in token_pos]    
                full_name=' '.join([t for t in tokens if t not in stop_words])
                full_lemma=' '.join([t for t in lemmas if t not in stop_words])
                try:
                    plural=p.plural(name)
                except:
                    print('issue: ', name)
                    plural=''
                
                first_name=[full_name,plural,full_lemma]
            elif 'synonym:' in line:
                eid=line.find('" ')
                name=line[len('synonym: "'):eid].lower().replace("'s","")
                name=re.sub(' +',' ',name.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))).strip()
                if len(name)<2 and name.lower() not in stopwords:
                    pass
                else:
                    tokens = word_tokenize(name)
                    token_pos = nltk.pos_tag(tokens)
                    lemmas = [lemmatizer.lemmatize(token[0], get_pos(token[1])) for token in token_pos]
                    full_name=' '.join([t for t in tokens if t not in stop_words])
                    full_lemma=' '.join([t for t in lemmas if t not in stop_words])
                    try:
                        plural=p.plural(name)
                    except:
                        plural=''
                    temp_list=[full_name,plural, full_lemma]
                    if temp_list not in seen_synonyms: 
                        seen_synonyms.append(temp_list)
                    
        obo_dic[class_id]={'name':first_name,'synonym':seen_synonyms}
        for n in first_name[:-1]:
            if len(n)<2:
                continue
            fout.write(class_id+'\t'+n+'\n')
        if len(seen_synonyms)>0:
            for syn in seen_synonyms:
                for n in syn[:-1]:
                    if len(n)<2:
                        continue
                    fout.write(class_id+'\t'+n+'\n')
    fout.close()
#    f=open('ifiles/ont_dic.pkl','wb')
#    obj=pickle.dumps(obo_dic)
#    f.write(obj)
#    f.close()

    return obo_dic

def build_word_dicts(ont_dic):
        total_freq=0
        word_freq={}
        exact_dic={}
        words_dic={}
        tokens_dic={}
        for d in ont_dic:
                tokens_dic[d]={}
                index=0
                for i,desc in enumerate(ont_dic[d]['name']):
                        if desc not in exact_dic:
                            exact_dic[desc]={}
                        exact_dic[desc][d]=True
                        #words=nltk.tokenize.word_tokenize(desc)
                        words=desc.split(' ')
                        tokens_dic[d][index]=words
                        for w in words:
                            if w not in words_dic:
                                words_dic[w]={}
                            if d not in words_dic[w]:
                                words_dic[w][d]=[]
                            words_dic[w][d].append(index)
                        index+=1
                        if i==1:
                            for w in desc.split(' '):
                                total_freq+=1
                                if w not in word_freq:
                                    word_freq[w]=1
                                else:
                                    word_freq[w]+=1

                for syn in (ont_dic[d]['synonym']):
                        for i,desc in enumerate(syn):
                               if desc not in exact_dic:
                                    exact_dic[desc]={}
                               exact_dic[desc][d]=True
                               #words=nltk.tokenize.word_tokenize(desc)
                               words=desc.split(' ')
                               tokens_dic[d][index]=words
                               for w in words:
                                    if w not in words_dic:
                                        words_dic[w]={}
                                    if d not in words_dic[w]:
                                        words_dic[w][d]=[]
                                    words_dic[w][d].append(index)
                               index+=1
                               if i==1:
                                   for w in desc.split(' '):
                                       total_freq+=1
                                       if w not in word_freq:
                                           word_freq[w]=1
                                       else:
                                           word_freq[w]+=1
        IC={}
        for w in word_freq:
            IC[w]=-math.log10(word_freq[w]/total_freq)

        f=open("ifiles/words_dic.pkl",'wb')
        obj=pickle.dumps(words_dic)
        f.write(obj)
        f.close()
        f=open('ifiles/tokens_dic.pkl','wb')
        obj=pickle.dumps(tokens_dic)
        f.write(obj)
        f.close()
        f=open('ifiles/exact_dic.pkl','wb')
        obj=pickle.dumps(exact_dic)
        f.write(obj)
        f.close()
        f=open('ifiles/wordIC_dic.pkl','wb')
        obj=pickle.dumps(IC)
        f.write(obj)
        f.close()

		
	

if __name__=="__main__":
    ont_dic=build_dict(sys.argv[1])
    word_dic=build_word_dicts(ont_dic)
