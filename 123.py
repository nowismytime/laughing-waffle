import pprint
import datetime
from py2neo import authenticate, Node
from py2neo.neo4j import Index
from wikitools import api
from wikitools import wiki
import py2neo.legacy.index
from wikitools import category
import wikitools
from wikitools import page
import re
from wikitools.page import NoPage, Page
from py2neo import neo4j, node, rel
import logging
logging.basicConfig(level=logging.WARNING)
authenticate("localhost:7474", "neo4j", "10p13dd0053")
#people = re.compile(r'Category:.*People', re.I)
#badlinks = re.compile(r'stubs|Help:|Talk:|Wikipedia|Template:|Portal:|Outline of|List of|Outlines of|Catalog of|Lists of|Glossary|Glossaries|Index of|Timeline of|History of|Chronology|Index of|Overview|Journals|Redirects|Book:')
needless = re.compile(r' \(')
site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

#local
graph_db = neo4j.Graph("http://localhost:7474/db/data/")
graph_db.delete_all()
## for testing only, make sure we have a clean slate!!
#graph_db.clear()
#@type : Index

db_categories = graph_db.legacy.get_or_create_index(neo4j.Node, "Categories")
#@type : Index
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

    # wronglinks = re.search(badlinks, name)
    # if wronglinks:
    #   log("wrongslinks matched, exiting")
    #   return

    # try:
    visitedCategories.add(name)

    cat = category.Category(site, "Category:"+name)
    if dbcat is None:
        dbcat = db_categories.get_or_create("name", name, {"name": name, "pageid": cat.pageid})
        dbcat.set_labels('Category')
    else:
        dbcat["pageid"] = cat.pageid

    catlist = cat.getAllMembers(namespaces=[14], titleonly=True)

    # :type pagelist:list[Page]
    pagelist = cat.getAllMembers(namespaces=[0], titleonly=True)

    #
    # do pages first
    #
    for page in pagelist:
        try:
            # no longer filtering people, so don't need page contents
#               txt = page.getWikiText(expandtemplates=False, force=False)
#               if txt is None: continue
#
# #             log("len of wikitext = {}".format(len(txt)))
#               txt = txt.decode('utf8').encode('ascii', 'ignore')
#               if re.search(people, txt):
#                   continue

            title = page.encode('ascii', 'ignore')
#               log("             page: {}".format(title))

            # at this point, have all the info we need, so save to db
            # (try to find node first, if exists, just make a connection, if not, create it first
            db_page = db_pages.get("name", title)
            if not len(db_page):
                db_page = db_pages.create("name", title, {"name": title, "is": "page"})
                db_page.set_labels('Page')
            else:
                db_page = db_page[0]


            # db_page = db_pages.get_or_create("name", title, {"name": title})
            # db_page.set_labels('Page')
            graph_db.create(rel(dbcat, "has page", db_page))

        except Exception as ex:
            if ex is NoPage:
                log("Page not found! {}".format(page))
            else:
                log('exception occured! page: {}, msg: {}'.format(page, ex.message))

    log("       {} pages saved".format(len(pagelist)))
    #
    # now do categories
    #

    for catname in catlist:
        new = False
        # get or create child category
        catname = catname[9:]
        childcat = db_categories.get("name", catname)
        if not len(childcat):
            new = True
            childcat = db_categories.create("name", catname, {"name": catname, "is": "category"})
            childcat.set_labels('Category')
        else:
            childcat = childcat[0]

        # link up to parent
        graph_db.create(rel(dbcat, "has category", childcat))

        # if existing AND already visited, skip
        # NOTE: in the future, might change to just not go into existing ones at all, but it might lead to lost data if run was never finished
        if new is False and ('d' in childcat or catname in visitedCategories ):
            continue
        if len(visitedCategories)>2 :
            continue
        #log(" - about to dive into subcategory '{}'".format(catname))
        WTree(catname, visitedCategories, childcat)
        childcat['d'] = datetime.datetime.now()

    #log("Finished processing {}".format(name))

#   except Exception as ex:
# #     if ex is NoPage:
#       log('main exception occurred! page not found='+ex.message)
#       pprint.pprint(ex)



if __name__ == "__main__":

    CategoryTree = {}

    cat = 'Geography'

    print("{} Started processing category '{}'".format(str(datetime.datetime.now()), cat))

    WTree(cat)

    print("{} Finished processing category '{}'".format(str(datetime.datetime.now()), cat))

    pprint.pprint(CategoryTree)

