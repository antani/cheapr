__author__ = 'vantani'
import logging
from xml.dom import minidom, Node
from xml.parsers.expat import ExpatError, ErrorString


class GoodReadsParser(object):

    def parse_result(self, url_handler):
        try:
            goodreads_dom = minidom.parse(url_handler)
            return goodreads_dom
        except ExpatError, e:
            logging.error("XML Error: %s line: %d offset: %d" % (
                ErrorString(e.code), e.lineno, e.offset))
            return None

    def get_text(self, element):
        value = ""

        for text in element.childNodes:

            try:
                if text:
                    print text
                    value += text.data
            except AttributeError:
                logging.error("get_text() error: " + text.toxml())
                raise

        if value:
            return value.strip()
        else:
            return None

    def parse_books(self, url_handler):
        goodreads_dom = self.parse_result(url_handler)
        books = []
        for book_element in goodreads_dom.getElementsByTagName("book"):
            book = self.handle_book(book_element)
            if book:
                books.append(book)
        return books

    def handle_book(self, book_element):
        book = {}
        for child_node in book_element.childNodes:
            value = ""

            if child_node.nodeType == Node.TEXT_NODE:
                continue
            elif child_node.nodeName == "authors":
                value = self.handle_authors(child_node)
            elif child_node.nodeName == "work":
                value = self.handle_work(child_node)
            elif child_node.nodeName == "similar_books":
                #value = self.handle_similar(child_node)
                continue
            elif  child_node.nodeName == "popular_shelves":
                logging.info("found shelves")
                continue
            elif  child_node.nodeName == "book_links":
                logging.info("found shelves")
                continue
            elif  child_node.nodeName == "series_works":
                logging.info("found shelves")
                continue
            else:
                value = self.get_text(child_node)

            book[child_node.nodeName] = value
        return book



    def parse_shelfs(self, url_handler):
        goodreads_dom = self.parse_result(url_handler)
        shelfs = []
        for shelf_element in goodreads_dom.getElementsByTagName("shelf"):
            shelf = self.handle_shelf(shelf_element)
            if shelf:
                shelfs.append(shelf)
        return shelfs

    def handle_shelf(self, shelf_element):
        shelf = {}
        for child_node in shelf_element.childNodes:
            value = ""

            if child_node.nodeType == Node.TEXT_NODE:
                continue
            else:
                value = self.get_text(child_node)

            shelf[child_node.nodeName] = value
        return shelf

    def handle_authors(self, authors_element):
        authors = []
        for child_node in authors_element.childNodes:
            author = self.handle_author(child_node)
            if author:
                authors.append(author)
        return authors

    def handle_author(self, author_element):
        author = {}
        for child_node in author_element.childNodes:
            value = ""

            if child_node.nodeType == Node.TEXT_NODE:
                continue
            else:
                value = self.get_text(child_node)

            author[child_node.nodeName] = value
        if author:
            return author
        else:
            return None

    def handle_similar_books(self, similar_books_element):
        similar_books = []
        for child_node in similar_books_element.childNodes:
            similar_book = self.handle_similar_book(child_node)
            if similar_book:
                similar_books.append(similar_book)
        return similar_books

    def handle_similar_book(self, similar_book_element):
        similar_book = {}
        for child_node in similar_book_element.childNodes:
            value = ""

            # if child_node.nodeType == Node.TEXT_NODE:
            #     continue
            # else:
            value = self.get_text(child_node)
            similar_book[child_node.nodeName] = value
        if similar_book:
            return similar_book
        else:
            return None

    def handle_work(self, works_element):
        works = []
        for child_node in works_element.childNodes:
            work = self.handle_work(child_node)
            if work:
                works.append(work)
        return works

    def handle_work(self, work_element):
        work = {}
        for child_node in work_element.childNodes:
            value = ""

            if child_node.nodeType == Node.TEXT_NODE:
                continue
            else:
                value = self.get_text(child_node)

            work[child_node.nodeName] = value
        if work:
            return work
        else:
            return None

    def handle_similar(self, similars_element):
        similars = []
        for child_node in similars_element.childNodes:
            similar = self.handle_similar(child_node)
            if similar:
                similars.append(similar)
        return similars

    def handle_similar(self, similar_element):
        similar = {}
        for child_node in similar_element.childNodes:
            value = ""
            if  child_node.nodeName == "authors":
                logging.info("found similar authors")
                continue
            if  child_node.nodeName == "book":
                value = self.handle_similar_books(child_node)
            elif child_node.nodeType == Node.TEXT_NODE:
                continue
            else:
                value = self.get_text(child_node)

            similar[child_node.nodeName] = value
        if similar:
            return similar
        else:
            return None
