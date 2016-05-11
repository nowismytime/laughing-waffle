from py2neo import authenticate
from wikitools import wiki
from wikitools import page, category
import re
from py2neo import neo4j, node, rel
import logging
from nltk.tag.stanford import StanfordNERTagger
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
import sys, os
parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/../mitielib')
from mitie import *
from collections import defaultdict

#st = StanfordNERTagger('/home/nowismytime/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz', '/home/nowismytime/Downloads/stanford-ner-2014-06-16/stanford-ner.jar',encoding='utf-8')
#ner = named_entity_extractor('MITIE-models/english/ner_model.dat')

text = """Culture is, in the words of E.B. Tylor, "that complex whole which includes knowledge, belief, art, morals, law, custom and any other capabilities and habits acquired by man as a member of society."
As a defining aspect of what it means to be human, culture is a central concept in anthropology, encompassing the range of phenomena that are transmitted through social learning in human societies. The word is used in a general sense as the evolved ability to categorize and represent experiences with symbols and to act imaginatively and creatively. This ability arose with the evolution of behavioral modernity in humans around 50,000 years ago. This capacity is often thought to be unique to humans, although some other species have demonstrated similar, though much less complex abilities for social learning. It is also used to denote the complex networks of practices and accumulated knowledge and ideas that is transmitted through social interaction and exist in specific human groups, or cultures, using the plural form. Some aspects of human behavior, such as language, social practices such as kinship, gender and marriage, expressive forms such as art, music, dance, ritual, religion, and technologies such as cooking, shelter, clothing are said to be cultural universals, found in all human societies. The concept material culture covers the physical expressions of culture, such as technology, architecture and art, whereas the immaterial aspects of culture such as principles of social organization (including, practices of political organization and social institutions), mythology, philosophy, literature (both written and oral), and science make up the intangible cultural heritage of a society.
In the humanities, one sense of culture, as an attribute of the individual, has been the degree to which they have cultivated a particular level of sophistication, in the arts, sciences, education, or manners. The level of cultural sophistication has also sometimes been seen to distinguish civilizations from less complex societies. Such hierarchical perspectives on culture are also found in class-based distinctions between a high culture of the social elite and a low culture, popular culture or folk culture of the lower classes, distinguished by the stratified access to cultural capital. In common parlance, culture is often used to refer specifically to the symbolic markers used by ethnic groups to distinguish themselves visibly from each other such as body modification, clothing or jewelry. Mass culture refers to the mass-produced and mass mediated forms of consumer culture that emerged in the 20th century. Some schools of philosophy, such as Marxism and critical theory, have argued that culture is often used politically as a tool of the elites to manipulate the lower classes and create a false consciousness, such perspectives common in the discipline of cultural studies. In the wider social sciences, the theoretical perspective of cultural materialism holds that human symbolic culture arises from the material conditions of human life, as humans create the conditions for physical survival, and that the basis of culture is found in evolved biological dispositions.
When used as a count noun, "a culture" is the set of customs, traditions and values of a society or community, such as an ethnic group or nation. In this sense, multiculturalism is a concept that values the peaceful coexistence and mutual respect between different cultures inhabiting the same territory. Sometimes "culture" is also used to describe specific practices within a subgroup of a society, a subculture (e.g. "bro culture"), or a counter culture. Within cultural anthropology, the ideology and analytical stance of cultural relativism holds that cultures cannot easily be objectively ranked or evaluated because any evaluation is necessarily situated within the value system of a given culture. This dance form traces its origins to the nomadic bards of ancient northern India, known as Kathakars or storytellers. Its form today contains traces of temple and ritual dances, and the influence of the bhakti movement.from the Sanskrit word katha meaning "story", and katthaka in Sanskrit means "he who tells a story", or "to do with stories"."""
"""
tokenized_text = tokenize(text)

#classified_text = st.tag(tokenized_text)
classified_text1 = ner.extract_entities(tokenized_text)

""""""def stanfordNE2BIO(tagged_sent):
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
print entities"""
"""
entities =[]
for e in classified_text1:
    range = e[0]
    tag = e[1]
    entity_text = " ".join(tokenized_text[i] for i in range)
    entities.append(entity_text)

logging.basicConfig(level=logging.WARNING)
authenticate("localhost:7474", "neo4j", "10p13dd0053")
needless = re.compile(r' \(')
site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

graph_db = neo4j.Graph("http://localhost:7474/db/data")

for entity in entities:
    node1 = graph_db.legacy.get_indexed_node("Pages" ,"name" , '*'+entity.lower()+'*')
    #print node1

    try:
        page1 = page.Page(site, entity)
        categories = page1.getCategories(force=True)


    except Exception as ex:
            print ex.message

    print "http://en.wikipedia.org/wiki/"+ page1.urltitle
    node1 = graph_db.legacy.get_indexed_node("Pages" ,"name" , entity.lower())
    #print node1


from spotlight import annotate
from functools import partial

query = """"""select distinct ?page where {
  ?syn (dbpedia-owl:wikiPageDisambiguates|^dbpedia-owl:wikiPageDisambiguates)* dbpedia:name ;
       foaf:isPrimaryTopicOf ?page

}""""""

api = partial(annotate,'http://localhost/rest/annotate',confidence=0.4,support=20,spotter='AtLeastOneNounSelector')

from agdistispy.agdistis import Agdistis
ag = Agdistis()
print ag.disambiguate("<entity>Apple Inc.</entity>")"""

import textrazor

client = textrazor.TextRazor('43591ed43b2c52d7496ad032d78e16d7c4b86b4ad318c838829a047f',extractors=["entities"])

response = client.analyze(text)

for entity in response.entities():
    print entity.wikipedia_link





# what it we measure the average distance of an entity candidate with all other entity candidates.





