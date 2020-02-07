import pandas as pd
import time
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.chrome.options import Options



#def main():
#        ScraperForo.buscarPersonasForo()

class ScraperForo:        
    
    @staticmethod
    def buscarPersonasForo():
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        try:
            driver = webdriver.Chrome('../chromedriver')
        except:
            driver = webdriver.Chrome('./chromedriver')
        #Abro nueva ventana de Chrome Headless
        #driver = webdriver.Chrome('./chromedriver', options=options)
        #driver = webdriver.PhantomJS('./phantomjs-2.1.1-windows/bin/phantomjs')
        
        #Abro foro
        driver.get("https://developer.salesforce.com/forums#!/feedtype=RECENT&dc=Jobs_Board&criteria=OPENQUESTIONS")
        
        #Cierro los pop-ups del foro (SOLO SI USO CHROMEDRIVER, SI USO PHANTOM COMENTAR LAS LINEAS)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #Cierro pop up 1
        driver.find_element_by_xpath('//*[@id="dfc-cookie-info-bar-button"]').click() #Cierro pop up 2
        
        
        """
        #Scrollear abajo para obtener mas resultados
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
        
            new_height = driver.execute_script("return document.body.scrollHeight")
            print("Last height: "+str(last_height))
            print("New height: "+str(new_height))
            if new_height == last_height:
                break
            last_height = new_height
        """
        
        #driver.execute_script("window.scrollTo(0, 5000)")
        #time.sleep(20)

        
        #Declaro array donde voy a guardar los nombres, fechas, etc
        totalNames = []
        totalDates = []
        totalqTitles = []
        totalqLinks = []
        

 
        #Traigo todos los nombres, fechas, etc
        names = driver.find_elements_by_class_name("user_profile_name")
        dates = driver.find_elements_by_class_name("feeditemtimestamp")
        qTitles = driver.find_elements_by_css_selector(".feeditemtext.cxquestiontitlewithlink")
        
        
        #Recorro los nombres, fechas, etc que traje antes y los voy agregando uno por uno a su array correspondiente
        
        for name in names:
            author = name.find_element_by_css_selector("div.user_profile_name a")    
            totalNames.append(''.join([c for c in author.text if c not in "1234567890"]))  
            
        for date in dates:
            totalDates.append(date.text)
          
        for title in qTitles:
            titleHeader = title.find_element_by_css_selector("h4.feeditemtext.cxquestiontitlewithlink a")
            totalqTitles.append(titleHeader.text)
            totalqLinks.append(titleHeader.get_attribute('href'))
            
        total = {'Date':totalDates, 'Name':totalNames, 'Title':totalqTitles, 'Link':totalqLinks}
        #Creo objeto que contiene los arrays con las fechas, nombres, etc
        totalObj = type('obj', (object,), total)
        df = pd.DataFrame(total)
        
        #df = pd.DataFrame(total, columns=['author','date'])
        #Serializo csv
        df.to_csv('quoted.csv', index=False)
        driver.close()
        #Devuelvo el objeto que cree para su posterior uso
        return totalObj
    
    
#if __name__ == '__main__':
#    main()