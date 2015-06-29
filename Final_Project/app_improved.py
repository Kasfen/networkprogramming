#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.
import ssl
import bank, uuid
import urllib.request
from bs4 import BeautifulSoup
import sys

from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'
temp_test=[1,2,3,4]

class test:
    def __init__(self,a,b,c):
        self.x = a
        self.y = b
        self.z = c

class test2:
    def __init__(self,tempa,tempb):
        self.x = tempa.x
        self.y = tempa.y
        self.z = tempa.z
        self.x2 = tempb.x
        self.y2= tempb.y
        self.z2= tempb.z

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('yuwen', 'qsz79217815'), ('man1', 'pass2'),('man2', 'pass2')]:
            session['username'] = username
            session['csrf_token'] = uuid.uuid4().hex
            return redirect(url_for('pay'))
    return render_template('login.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    payments = bank.get_payments_of(bank.open_database(), username)
    #x=test(123,456)
    #y=test(789,101112)
    imf=[]
    #imf.append(x)
    #imf.append(y)
    #hyl='https://www.google.com.tw'
    return render_template('index.html', payments=imf, username=username,
                           flash_messages=get_flashed_messages())

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    #x=test(123,456)
    #y=test(789,101112)
    imf=[]
    #imf.append(x)
    #imf.append(y)
    #hyl='https://www.google.com.tw'
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    search_keyword = request.form.get('search_keyword', '').strip()
    #dollars = request.form.get('dollars', '').strip()
    #memo = request.form.get('memo', '').strip()
    complaint = None
    if request.method == 'POST':
        if request.form.get('csrf_token') != session['csrf_token']:
            abort(403)
        if search_keyword:
            #db = bank.open_database()
            #bank.add_payment(db, username, account, dollars, memo)
            #db.commit()
            #flash('Payment successful')
            #x=test(123,456)
            #y=test(789,101112)
            imf=[]
            imf2=[]
            imf3=[]
            #imf.append(x)
            #imf.append(y)
            content = urllib.request.urlopen('http://search.books.com.tw/exep/prod_search.php?key='+search_keyword)
            soup = BeautifulSoup(content)
            tagA_list=soup.find_all('a',rel='mid_name')
            tagB_list=soup.find_all('b')
            j=0
            for i in range(0,len(tagA_list)):#num of list
                booktitle=tagA_list[i].get('title')
                book_link=tagA_list[i].get('href')
                bookprice=int(tagB_list[j].string)
                if int(bookprice) < 100 :
                   j=j+1
                   bookprice=int(tagB_list[j].string)
                #print ('{}Book title: {}\n\t{}Price: {}]\n\t link: {})'.format(i,booktitle,j,bookprice,book_link))
                j=j+1
                tempa=test(booktitle,book_link,bookprice)
                imf.append(tempa)
            content = urllib.request.urlopen('http://www.kingstone.com.tw/search/result.asp?c_name='+search_keyword)
            soup = BeautifulSoup(content)
            tagA_list=soup.find_all('a',class_='anchor')
            tagB_list=soup.find_all('em')
            j=0
            for i in range(0,len(tagA_list)):#num of list
                if i>22:
                    booktitle2=tagA_list[i].get('title')
                    #if isinstance(booktitle, str):
                    #print(booktitle)
                    book_link2=tagA_list[i].get('href')
                    flag=0
                    while(flag==0):
                        try:
                            float(tagB_list[j].string)
                            bookprice2=int(tagB_list[j].string)
                            flag=1
                        except:
                            j=j+1
                    #bookprice=int(tagB_list[j].string)
                    if int(bookprice2) < 100 :
                       j=j+1
                       bookprice2=int(tagB_list[j].string)
                    #print ('{}Book title: {}\n\t{}Price: {}]\n\t link: {})'.format(i,booktitle,j,bookprice,book_link))
                    j=j+1
                    tempb=test(booktitle2,book_link2,bookprice2)
                    imf2.append(tempb)
            if len(imf)>=len(imf2):
                temp_len=len(imf2)
            else:
                temp_len=len(imf)
            for num in range(0,temp_len):
                tempc=test2(imf[num],imf2[num])
                imf3.append(tempc)
            return render_template('index.html', payments=imf3, username=username,
                           flash_messages=get_flashed_messages())
            #return redirect(url_for('index'))
    return render_template('pay2.html', complaint=complaint,
                           csrf_token=session['csrf_token'])

#ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#ctx.load_cert_chain('crt-key-crs/download-system.crt', 'crt-key-crs/download-system.key')

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', debug=True, port=5000, ssl_context=('C:\Python34\key\server.crt','C:\Python34\key\server.key'))
