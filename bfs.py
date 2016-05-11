import datetime
from py2neo import authenticate
from wikitools import wiki
from wikitools import category
import re
from wikitools import page
from py2neo import neo4j, rel
import logging
import Queue

logging.basicConfig(level=logging.WARNING)
authenticate("localhost:7474", "neo4j", "10p13dd0053")
needless = re.compile(r' \(')
site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

graph_db = neo4j.Graph("http://localhost:7474/db/data")
graph_db.delete_all()

db_categories = graph_db.legacy.get_or_create_index(neo4j.Node, "Categories")
db_pages = graph_db.legacy.get_or_create_index(neo4j.Node, "Pages")

q1 = Queue.Queue()
vc = set()


def log(msg):
    print("{} {}".format(str(datetime.datetime.now()), msg))


def WTree(c1, vc, q1):

    name = c1[0]
    dbcat = c1[1]
    cat = c1[2]

    if name in vc:
        return

    vc.add(name)
    print "Processing category ("+name+")"

    catlist = cat.getAllMembers(namespaces=[14], titleonly=True)
    pagelist = cat.getAllMembers(namespaces=[0], titleonly=True)

    for pg in pagelist:
        try:

            title = pg.encode('ascii', 'ignore')
            page1 = page.Page(site, title)
            title1 = title.lower()
            db_page = db_pages.get("name", title)

            if not len(db_page):
                db_page = db_pages.create("name", title, {"name": title1, "pageid": page1.pageid})
                db_page.add_labels('Page')
            else:
                db_page = db_page[0]

            graph_db.create(rel(dbcat, "has page", db_page))

        except Exception as ex:
            if ex is page.NoPage:
                log("Page not found! {}".format(page))
            else:
                log('exception occured! page: {}, msg: {}'.format(page, ex.message))

    log("       {} pages saved".format(len(pagelist)))

    for catname in catlist:
        if catname not in vc:

            catname = catname[9:]
            cat1= category.Category(site, "Category:"+catname)
            childcat = db_categories.get("name", catname)
            catname1 = catname.lower()

            if not len(childcat):
                childcat = db_categories.create("name", catname, {"name": catname1, "pageid": cat1.pageid})
                childcat.add_labels('Category')
            else:
                childcat = childcat[0]

            graph_db.create(rel(dbcat, "has category", childcat))
            q1.put((catname,childcat,cat1))

    log("       {} sub-categories saved".format(len(catlist)))


if __name__ == "__main__":

    name = 'Main topic classifications'
    cat = category.Category(site, "Category:"+name)
    dbcat = db_categories.get_or_create("name", name, {"name": name, "pageid": cat.pageid})
    dbcat.add_labels('Category')
    q1.put((name,dbcat,cat))

    print("{} Started processing category '{}'".format(str(datetime.datetime.now()), name))

    while len(vc)<30 and not q1.empty():
        c1=q1.get()
        WTree(c1,vc,q1)

    print("{} Finished processing category '{}'".format(str(datetime.datetime.now()), name))




