from py2neo import authenticate
from wikitools import wiki
from wikitools import category, Page
import re
from wikitools.page import NoPage
from py2neo import neo4j, node, rel
import logging
from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree

st = StanfordNERTagger('/home/nowismytime/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz', '/home/nowismytime/Downloads/stanford-ner-2014-06-16/stanford-ner.jar',encoding='utf-8')
text = """Kathak is one of the eight forms of Indian classical dance. This dance form traces its origins to the nomadic bards of ancient northern India, known as Kathakars or storytellers. Its form today contains traces of temple and ritual dances, and the influence of the bhakti movement.from the Sanskrit word katha meaning "story", and katthaka in Sanskrit means "he who tells a story", or "to do with stories". The name of the form is properly katthak, with the geminated dental to show a derived form, but this has since simplified to modern-day kathak. kathaa kahe so kathak is a saying many teachers pass on to their pupils, which is generally translated as "she/he who tells a story, is a kathak", but which can also be translated as "that which tells a story, that is 'Kathak'".There are two major schools or gharana of Kathak from which performers today generally draw their lineage: the gharanas of Jaipur, Lucknow and (born in the courts of the Kachwaha Rajput kings, the Nawab of Oudh, and Benaras respectively); there is also a less prominent (and later) Raigarh gharana which amalgamated technique from all three preceding gharanas but became famous for its own distinctive compositions."""
tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)
print(classified_text)
for i in range(len(classified_text)):
    print(classified_text[i])

def stanfordNE2BIO(tagged_sent):
    bio_tagged_sent = []
    prev_tag = "O"
    for token, tag in tagged_sent:
        if tag == "O": #O
            bio_tagged_sent.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O": # Begin NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag: # Inside NE
            bio_tagged_sent.append((token, "I-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag: # Adjacent NE
            bio_tagged_sent.append((token, "B-"+tag))
            prev_tag = tag
    return bio_tagged_sent

def stanfordNE2tree(ne_tagged_sent):
    bio_tagged_sent = stanfordNE2BIO(ne_tagged_sent)
    sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
    sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]

    sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
    ne_tree = conlltags2tree(sent_conlltags)
    return ne_tree

ne_tagged_sent = classified_text

ne_tree = stanfordNE2tree(ne_tagged_sent)

entities = []
for subtree in ne_tree:
    if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
        ne_label = subtree.label()
        ne_string = " ".join([token for token, pos in subtree.leaves()])
        entities.append((ne_string, ne_label))
print entities

logging.basicConfig(level=logging.WARNING)
authenticate("localhost:7474", "neo4j", "10p13dd0053")
needless = re.compile(r' \(')
#site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

graph_db = neo4j.Graph("http://localhost:7474/db/data")

for i in range(len(entities)):
    etype = entities[i][1].encode('ascii', 'ignore')
    entity = entities[i][0].encode('ascii', 'ignore')
    node1 = graph_db.legacy.get_indexed_node("Pages" ,"name" , entity.lower())

# what it we measure the average distance of an entity candidate with all other entity candidates.








'''page1 = Page(site, "Page:"+page)
urlname = page1.urltitle
urlname = urlname[7:]
link = "http://en.wikipedia.org/wiki/"+ urlname'''
