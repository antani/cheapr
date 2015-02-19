__author__ = 'vantani'
import bleach
from fuzzywuzzy import fuzz
from cheapr.books import GoodReadsClient
from bs4 import BeautifulSoup

import memcache
from bottlenose import Amazon

import hashlib
import requests

GOODREADS_API_KEY='qSXq4Sses56f03nSCrVw'
GOODREADS_API_SECRET='KyNzNDWPHLukQOVmZpYIT9h0CLv2T0iXBlCqnicnePA'
mc = memcache.Client(['localhost:11211'], debug=1)

def write_query_to_db(cache_url, data):
        mc.set(cache_url, data)

def read_query_from_db(cache_url):
        found = mc.get(cache_url)
        return found
AWS_ACCESS_KEY_ID="AKIAIFYA4LL4UVHAQDSQ"
AWS_SECRET_ACCESS_KEY="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"
AMAZON_ASSOCIATE_TAG="cheapr-21"

amazon=Amazon(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AMAZON_ASSOCIATE_TAG,Parser=BeautifulSoup,
               CacheWriter=write_query_to_db,CacheReader=read_query_from_db)


class GoodReads():

    def get_book_reviews(self,title):
        key = GOODREADS_API_KEY
        secret = GOODREADS_API_SECRET
        g = GoodReadsClient(key, secret)
        reviews=g.get_reviews(title)
        return reviews

    def get_goodreads_info(self,title):
        goodreads=[]
        reviews = self.get_book_reviews(title)

        # description =""
        reviews_widget=""
        # reviews_link=""
        # image_url=""
        author_str=""
        # average_rating=0
        # isbn=""
        # published=""
        # publisher=""
        # pages=0
        # format=""
        # edition=""
        # similar_books=[]
        similar_books_data=[]

        for review in reviews:
            print review
            review_title = review["title"]
            try:
                if(fuzz.token_set_ratio(title,review_title) > 0.9):
                    description = bleach.clean(review["description"], strip=True)
                    # soup = BeautifulSoup(review["reviews_widget"], 'lxml') if review["reviews_widget"] else None
                    # reviews_widget =soup.select('iframe#the_iframe')[0].get('src') if soup else None
                    # x=reviews_widget
                    reviews_link = review["link"]
                    image_url=review["image_url"]
                    authors = review["authors"]
                    average_rating = review['average_rating']
                    isbn=review['isbn13']
                    published=review['publication_year']
                    publisher=review['publisher']
                    pages=review['num_pages']
                    format=review['format']
                    edition=review['edition_information']
                    #similar_books=review['similar_books']
                    for author in authors:
                        author_str += author['name'] + ", "

                    # for similar in similar_books:
                    #     similar_books_data.append(similar)

                    goodreads.append({'description':description ,'reviews_link': reviews_link, 'image_url': image_url,
                              "author_str":author_str,"reviews_widget":reviews_widget,"average_rating":float(average_rating),
                              "isbn":isbn, "published":published, "publisher":publisher,"pages":pages,"format":format,"edition":edition})

            except KeyError:
                pass
        return goodreads

class Amazon():

    def smart_truncate(self,content, length=100, suffix='...'):
        if len(content) <= length:
            return content
        else:
            return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def amazon_query_isbn(self,title):
        response = amazon.ItemSearch(Keywords="Algorithms", ResponseGroup="ItemAttributes",
                                     SearchIndex="Books")
        item=response.findAll("item")[0]
        isbn=item.itemattributes.isbn.text
        return isbn

    def amazon_similar_items(self,title):
        amazon_values=[]

        response = amazon.ItemSearch(Keywords=title, SearchIndex="Books",ResponseGroup="Large")
        url=""
        item=response.findAll("item")[0]
        url=item.detailpageurl.text
        book_title=item.itemattributes.title.text
        book_publisher=item.itemattributes.label.text
        book_pages=item.itemattributes.numberofpages.text
        book_author=""
        for author in item.itemattributes.author:
            book_author += author

        book_description = item.editorialreviews.editorialreview.content.text
        book_customer_reviews=item.customerreviews.iframeurl.text
        book_img = item.mediumimage.url.text

        amazon_values.append({"book_title":book_title, "book_publisher":book_publisher, "book_pages": book_pages, "book_author": book_author,
                              "book_small_description":self.smart_truncate(book_description,200),"book_description":book_description,"book_customer_reviews":book_customer_reviews,"book_img":book_img})
        amazon_response=""
        if not read_query_from_db(str(hashlib.md5(url).hexdigest())):
            amazon_response=requests.get(url)
            print amazon_response.status_code
            write_query_to_db(str(hashlib.md5(url).hexdigest()), amazon_response)
        else:
            amazon_response = read_query_from_db(str(hashlib.md5(url).hexdigest()))

        if amazon_response.status_code == 200:
            book_attrs=[]

            soup=BeautifulSoup(amazon_response.content, 'lxml')
            # book_img= soup.select("img#imgBlkFront")[0].get('src')
            # book_author = soup.select("span.author.notFaded a.a-link-normal")
            # amazon_values.append({"book_img":book_img, "book_author":book_author})
            title_urls = soup.select("div.a-carousel-viewport ol.a-carousel li.a-carousel-card a.a-link-normal")
            urls=[]
            for title_url in title_urls:
                title = title_url.text.strip()
                if title and not self.is_number(title):
                    urls.append(title)

            title_imgs = soup.select("div.a-carousel-viewport ol.a-carousel li.a-carousel-card a.a-link-normal div.a-spacing-mini img")
            imgs=[]
            for title_img in title_imgs:
                imgs.append(title_img.get('src'))

            for index, g in enumerate(urls):
                try:
                    item={"url":urls[index],"img":imgs[index],"book_title":book_title}
                    amazon_values.append(item)
                except IndexError:
                    pass

        return amazon_values

    def amazon_top_books(self):
            url="http://www.amazon.in/gp/bestsellers/books/"
            title_expr="div#zg_centerListWrapper div.zg_itemImmersion div.zg_itemWrapper div.zg_title a"
            price_expr="div#zg_centerListWrapper div.zg_itemImmersion div.zg_itemWrapper div.zg_itemPriceBlock_compact div.zg_price strong.price"
            img_expr="div#zg_centerListWrapper div.zg_itemImmersion div.zg_itemWrapper div.zg_image div.zg_itemImageImmersion a img"

            found = self.mc.get('amazon_best_seller')

            if (found!=None):
                return found
            else:
                amazon_response=requests.get(url)
                soup=BeautifulSoup(amazon_response.content, 'lxml')
                items=[]
                titles=soup.select(title_expr)
                prices=soup.select(price_expr)
                imgs=soup.select(img_expr)

                for title, price, img in zip(titles, prices, imgs):
                    item={'title':title.text, 'price':price.text, 'img':img.get('src')}
                    items.append(item)
                self.mc.set('amazon_best_seller',items,time=84000)
                return items


    def amazon_new_books(self):
        url="http://www.amazon.in/gp/new-releases/books/"
        title_expr="div#zg_centerListWrapper div.zg_itemImmersion div.zg_itemWrapper div.zg_title a"
        price_expr="div#zg_centerListWrapper div.zg_itemImmersion div.zg_itemWrapper div.zg_itemPriceBlock_compact div.zg_price strong.price"
        img_expr="div#zg_centerListWrapper div.zg_itemImmersion div.zg_itemWrapper div.zg_image div.zg_itemImageImmersion a img"

        found = self.mc.get('amazon_new_books')

        if (found!=None):
            return found
        else:
            amazon_response=requests.get(url)
            soup=BeautifulSoup(amazon_response.content, 'lxml')
            items=[]
            titles=soup.select(title_expr)
            prices=soup.select(price_expr)
            imgs=soup.select(img_expr)

            for title, price, img in zip(titles, prices, imgs):
                item={'title':title.text, 'price':price.text, 'img':img.get('src')}
                items.append(item)
            self.mc.set('amazon_new_books',items,time=84000)
            return items