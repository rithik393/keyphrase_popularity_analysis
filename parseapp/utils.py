from nltk.sentiment.vader import SentimentIntensityAnalyzer
from rake_nltk import Rake

def senti(data, word):
    s=0
    c=0
    #calculate sentiment
    for j in data:
        if(type(j)==str):
            
            
            if word in j:
                sid = SentimentIntensityAnalyzer()
                s=s+(sid.polarity_scores(j)["pos"])
                c=c+1
    try:
        return s/(c-1)
    except:
        return s

        
def wordcount(data, word):
    c=[]
    keyphrase={}
    #extracting keyphrases
    for i in data:
        if(type(i)==str):
            rake_nltk_var = Rake(max_length=2)# intializing the max no of words of keyphrase as 2
            rake_nltk_var.extract_keywords_from_text(i)#rake keyword extract function
            keyword_extracted1 = rake_nltk_var.get_ranked_phrases()

            for i in keyword_extracted1:
                c.append(i)
                if len(i)>=2:
                    if i.isnumeric():
                        continue
            
                    keyphrase[i]=keyphrase.get(i,0)+1
        else:
            continue
    try:
        return keyphrase[word]
    except:
        return 0
