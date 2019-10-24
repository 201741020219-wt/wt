import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import time

t1 = time.time()

r = requests.get('http://www.shuhai.com/shuku/1_0_0_0_0_0_0_1.html')
c = r.text
soup = BeautifulSoup(c,'html.parser')
print(soup)
content = soup.find('div',{'class':'book-list-wrapper'})
print(content)
page_div = soup.find('div',{'class':'page'})
page = page_div.find_all('a')[-2].text
print(page)
books = []
urls = ['http://www.shuhai.com/shuku/1_0_0_0_0_0_0_' + str(i) +'.html' for i in range(1,10)]
def crawl_page(url):
    p_r = requests.get(url)
    p_c = p_r.text
    p_soup = BeautifulSoup(p_c,'html.parser')
    p_content = p_soup.find_all('div',{'class':'book-list-wrapper'})
    pageBook = []
    for book in p_content:
        bookDic = {}
        bookDic['picurl']=book.find('div',{'class':'book-cover-wrapper radius'}).find('img')['src']
        bookDic['name'] = book.find('div',{'class':'one-book'}).find('a').text
        try:
            bookDic['time'] = book.fid('span',{'class':'time'}).text
        except Exception as e:
                bookDic['time'] = ''

        pageBook.append(bookDic)
    return pageBook
pool = mp.Pool()
multi_res = [pool.apply_async(crawl_page,(url,)) for url in urls]
pageBooks = [res.get() for res in multi_res]


for pageBook in pageBooks:
    for book in pageBook:
        books.append(book)
print(len(books))
t2 = time.time()
print(t2-t1)        
