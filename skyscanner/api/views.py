from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from pyvirtualdisplay import Display

from multiprocessing.dummy import Pool

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage,ImageCarouselColumn,URITemplateAction,TemplateSendMessage,ImageCarouselTemplate
from linebot.exceptions import LineBotApiError, InvalidSignatureError


from datetime import datetime as dt
import time

line_bot_api = LineBotApi('fSDjokoamI2lnlDZE8GJ2+PoZBn8DHsDba8zCtW57zR++3X+Iiy5jwtMQFB1oynrcHd3pU4g5S3IikMXzTmCkPueLieW/ilvst42POA6I6cyt/+z3u13OPxjof+Jq12l046ITxA2+sSMC95uRwEdHQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a3e92910d347b8dcda29a8bfaba8e3bc')
pool = Pool(3)

class Bot(APIView):
    def post(self, request):
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']
        # get request body as text
        body = request.get_data(as_text=True)
        data = request.json
        print(data)
        print(data['events'][0]['source']['userId'])
        # app.logger.info("Request body: " + body)
        
        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            # abort(400)
            pass
        return 'OK'

class Country(APIView):

    def get(self, request):
        print('come')
        data = self.request
        countrycode = data.query_params.get('country')

        ''' for Ubuntu SERVER '''
        cap = DesiredCapabilities().FIREFOX
        display = Display(visible=0, size=(1024, 768)).start()
        driver = webdriver.Firefox(capabilities=cap, executable_path='/home/ubuntu/anaconda3/bin/geckodriver')
        driver.implicitly_wait(30) # seconds
        actions = webdriver.ActionChains(driver)
        
        ''' for Window & MAC Client '''
        # driver = webdriver.Firefox()
        # countrycode = 'ch'

        print(countrycode)
        datadict = {'dataList' : []}
        price_min = 0
        price_max = 30000
        urlMain ="https://www.skyscanner.co.th/transport/flights/bkkt/"+countrycode+"?adults=2&children=0&adultsv2=2&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home"
        # urlMain ="https://www.skyscanner.co.th/"
        print(urlMain)
        driver.get(urlMain)
        time.sleep(10)
        driver.save_screenshot('screenie.png')
        # print("OK")
        # try:
        province = driver.find_elements(By.CLASS_NAME, 'with-image')[0]

        print(province)

        # print("FOUND READY")

        # province_ele = driver.find_elements(By.CLASS_NAME, 'with-image')
        # for province in province_ele:
            
        wheretoshow = province.find_element(By.CLASS_NAME, 'browse-data-entry').text
        url = province.find_element(By.TAG_NAME,'a').get_attribute('href')
        
        where = {
            'wheretoshow' : wheretoshow ,
            'url' : url
        }

        datadict['dataList'].append(where)
        # print(datadict['dataList'])
        # except:
        #     print('No DATA')
        #     pass
        
        driver.close()
        display.stop()   
        print(datadict)
        return Response(datadict)



        
