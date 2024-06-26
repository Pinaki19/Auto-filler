from flask import Flask, jsonify, request, render_template, json, redirect, url_for, session, abort, send_file, send_from_directory
from flask_pymongo import PyMongo
import pymongo
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time
from random import randint,choice
import pandas as pd

csv_file_path = 'Names.csv'

app = Flask(__name__)

ext_js = '''main();

function main() {
    var p =document.querySelector('[role="list"]').children;
    var k, x;
    for (k = 0; k < p.length; k++) {
        x = p[k].children[0];
        
        try {
            x = x.children[0].children[1];
            if (x.children[1].getAttribute("role") == "list") {
                x = x.children[1];
                var l = x.childElementCount;
                console.log(x);
    
                if(l==1){
                    x.children[0].childre[0].children[0].click();
                }
                else if (true) {
                    var select = Math.floor(Math.random() * (l - 1))
                    x.children[select].children[0].children[0].click();
                    select = Math.floor(Math.random() * (l - 1));
                    x.children[select].children[0].children[0].click();
                    select = Math.floor(Math.random() * (l - 1));
                    x.children[select].childre[0].children[0].click();
                } 
            }
            else {
                x = x.children[1].children[0];
                x = x.children[0].children[0].children;
                var select = Math.floor(Math.random() * (x.length-1))
                x[select].children[0].click();
            }

        }
        catch (e) {
            null;
        }
    }
    setTimeout(sub,200);
}

function sub() {
    document.forms[0].submit();
    return;
}
'''

def validForm(form):
    return "forms.gle" in form or "docs.google.com/forms/" in form

def get_random_names(n):
    df = pd.read_csv(csv_file_path)
    if 'Name' not in df.columns:
        raise ValueError("CSV file must contain a column named 'Name'")
    random_names = df['Name'].sample(n).tolist()
    return random_names


def getQuestionClassName(form):
    if not validForm(form):
        return None

    service = Service(executable_path=os.path.join(
        os.path.dirname(__file__), 'chromedriver.exe'))
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(form)
    driver.implicitly_wait(1)
    try:
        # Specific XPath to target the first div with role='list'
        xpath = "//div[@role='list'][1]"
        element = driver.find_element(By.XPATH, xpath)
        class_name = element.get_attribute("class")
        print(class_name)
        return class_name
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()



def main(Res,form,data,N):
    if not validForm(form):
        return None
    try:
        N=int(N)
    except:
        N=1
    try:
        NAMES=data["names"]
        EMAILS=data['emails']
    except:
        NAMES="DEFAULT"
        EMAILS = "DEFAULT"
    
    if (NAMES == "DEFAULT"):
        NAMES = get_random_names(N)
    else:
        NAMES=[ i.strip() for i in NAMES.split(',') ]
    if (len(NAMES) < N):
        NAMES.extend(get_random_names(N-len(NAMES)))
    if (EMAILS == "DEFAULT" or len(EMAILS) == 1 and EMAILS[0] == "DEFUALT"):
        EMAILS = []
    else:
        EMAILS = [i.strip() for i in EMAILS.split(',')]
    NAMES.append(NAMES[-1])
    service = Service(executable_path=os.path.join(
        os.path.dirname(__file__), 'chromedriver'))
    options = Options()
    options.binary_location = r"/opt/render/project/.render/chrome/opt/google/chrome/chrome"
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(service=service, options=options)
    i = 0
    t=N
    t2=i
    if(N<=0 or N>1000):
        return 'ok'
    while(N>0):
        t=N
        t2=i
        try:
            print(f"Submitting form no: {i+1}")
            driver.get(form)
            flag1,flag2=0,0
            try:
                l = driver.find_elements(By.XPATH, '*//input[@type="text"]')
                flag1=1
            except:
                pass
            try:
                L2 = driver.find_elements(By.XPATH, '*//input[@type="email"]')
                L2=L2[:2]
                flag2=1
            except:
                pass
            if i<len(NAMES):
                NAME=NAMES[i]
            else:
                NAME="None"
            if i<len(EMAILS):
                EMAIL=EMAILS[i]
            else:
                Mail_name=NAME.replace(' ','')
                EMAIL = Mail_name+str(randint(10, 1000))+'@'+choice(
                    ['gmail', 'yahoo', 'outlook'])+choice(['.com', '.in'])
            i+=1
            print(f"Data used for this form Name:{NAME} Email:{EMAIL}")
            if Res==4:
                c=1
            else:
                c=0
            if flag1:
                for X in l:
                    if (c == 0 and i < len(NAMES)):
                        X.send_keys(NAME.title())
                        X.send_keys(Keys.RETURN)
                        c += 1
                    else:
                        X.send_keys("None")
                        X.send_keys(Keys.RETURN)
                        c += 1
                    
            if flag2:
                for X in L2:
                    X.send_keys(EMAIL)
                    X.send_keys(Keys.RETURN)
            Rate = driver.find_elements(By.XPATH, '*//div[@role="radiogroup"]')
            if len(Rate)>0:
                for element in Rate:
                    try:
                        children = element.find_elements(By.XPATH,"./child::*")
                        if len(children)==0:
                            continue
                        children = children[0].find_elements(By.XPATH, "./child::*")
                        if len(children)<2:
                            continue
                        children = children[1].find_elements(By.XPATH, "./child::*")
                        random_selected_child=randint(2,len(children)-2)
                        children[random_selected_child].click()
                    except:
                        pass
                    
            driver.execute_script(ext_js)
            #// Before you try to switch to the so given alert, it needs to be present.
            try:
                time.sleep(.25)
                alert = Alert(driver)
                alert.accept()
            except:
                pass
            N-=1
            if(N==0):
                time.sleep(1)
                driver.quit()
        except:
            time.sleep(.2)
            N=t
            i=t2
   

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")
        
      

@app.get('/favicon.ico')
def favicon():
    return send_from_directory('./static/assets',
                               'Forms.ico', mimetype='image/vnd.microsoft.icon')
@app.get('/contact')
def contact():
    return render_template('contact.html')

@app.get('/about')
def about():
    return render_template('about.html')

@app.route('/fill', methods=['POST'])
def fill():
    Data = request.get_json()
    print(Data)
    Res=Data.get("Request_NO")
    form=Data.get("Form")
    data=Data.get("Form_data")
    N=Data.get("Total")
    main(Res,form,data,N)
    return jsonify({'status':'ok'})
  
if __name__ == "__main__":
    app.run(port=8080)
