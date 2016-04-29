import datetime
from py2neo import authenticate
from wikitools import wiki
from wikitools import category
import re
from wikitools.page import NoPage, Page
from py2neo import neo4j, node, rel
import logging
from nltk.tag.stanford import StanfordNERTagger as NER

logging.basicConfig(level=logging.WARNING)
authenticate("localhost:7474", "neo4j", "10p13dd0053")
needless = re.compile(r' \(')
site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

graph_db = neo4j.Graph("http://localhost:7474/db/data")

db_categories = graph_db.legacy.get_or_create_index(neo4j.Node, "Categories")
db_pages = graph_db.legacy.get_or_create_index(neo4j.Node, "Pages")


def log(msg):
    print("{} {}".format(str(datetime.datetime.now()), msg))

def WTree(name, visitedCategories=set(), dbcat=None):
    """
    For a given category, query subcategories and get categories and pages.
    Query subcategories recursively
    :type name: str
    :type visitedCategories: set
    """

    visitedCategories.add(name)

    cat = category.Category(site, "Category:"+name)
    if dbcat is None:
        dbcat = db_categories.get_or_create("name", name, {"name": name, "pageid": cat.pageid})
        dbcat.add_labels('Category')
    else:
        dbcat["pageid"] = cat.pageid

    catlist = cat.getAllMembers(namespaces=[14], titleonly=True)
    pagelist = cat.getAllMembers(namespaces=[0], titleonly=True)

    for page in pagelist:
        try:

            title = page.encode('ascii', 'ignore')

            db_page = db_pages.get("name", title)
            if not len(db_page):
                db_page = db_pages.create("name", title, {"name": title, "is": "page"})
                db_page.add_labels('Pages')
            else:
                db_page = db_page[0]

            graph_db.create(rel(dbcat, "has page", db_page))

        except Exception as ex:
            if ex is NoPage:
                log("Page not found! {}".format(page))
            else:
                log('exception occured! page: {}, msg: {}'.format(page, ex.message))

    log("       {} pages saved".format(len(pagelist)))

    for catname in catlist:
        new = False
        catname = catname[9:]
        cat1= category.Category(site, "Category:"+catname)
        childcat = db_categories.get("name", catname)
        if not len(childcat):
            new = True
            childcat = db_categories.create("name", catname, {"name": catname, "is": "category", "pageid": cat1.pageid})
            childcat.add_labels('Category')
        else:
            childcat = childcat[0]

        graph_db.create(rel(dbcat, "has category", childcat))

        if new is False and ('d' in childcat or catname in visitedCategories ):
            continue
        if len(visitedCategories)>100:
            continue

        WTree(catname, visitedCategories, childcat)
        childcat['d'] = datetime.datetime.now()

if __name__ == "__main__":

    CategoryTree = {}

    cat = 'Fictional characters'

    print("{} Started processing category '{}'".format(str(datetime.datetime.now()), cat))

    WTree(cat)

    print("{} Finished processing category '{}'".format(str(datetime.datetime.now()), cat))


