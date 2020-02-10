import pandas as pd
import time
from selenium import webdriver


class ScraperForo:

    @staticmethod
    def buscar_foro():

        driver = ScraperForo.abrir_navegador()

        ScraperForo.ir_foro(driver)

        ScraperForo.cerrar_popups(driver)

        dates, names, q_titles = ScraperForo.tomar_datos(driver)

        all_dates, all_names, all_q_links, all_q_titles = ScraperForo.pasar_datos_a_array(dates, names, q_titles)

        total = {'Date': all_dates,
                 'Name': all_names,
                 'Title': all_q_links,
                 'Link': all_q_titles}

        df, objeto_usuario = ScraperForo.pasar_a_objeto(total)

        ScraperForo.pasar_a_csv(df)

        driver.close()

        return objeto_usuario

    @staticmethod
    def pasar_a_csv(df):
        df.to_csv('quoted.csv', index=False)

    @staticmethod
    def pasar_a_objeto(total):
        objeto_usuarios = type('obj', (object,), total)
        df = pd.DataFrame(total)
        return df, objeto_usuarios

    @staticmethod
    def ir_foro(driver):
        # Abro foro
        driver.get("https://developer.salesforce.com/forums#!/feedtype=RECENT&dc=Jobs_Board&criteria=OPENQUESTIONS")

    @staticmethod
    def abrir_navegador():
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome('../chromedriver.exe')
        return driver

    @staticmethod
    def cerrar_popups(driver):
        # Cierro los pop-ups del foro (SOLO SI USO CHROMEDRIVER, SI USO PHANTOM COMENTAR LAS LINEAS)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()  # Cierro pop up 1
        driver.find_element_by_xpath('//*[@id="dfc-cookie-info-bar-button"]').click()  # Cierro pop up 2

    @staticmethod
    def pasar_datos_a_array(dates, names, qTitles):
        # Declaro array donde voy a guardar los nombres, fechas, etc
        totalNames = []
        totalDates = []
        totalqTitles = []
        totalqLinks = []
        # Recorrer nombres y agregar al Array
        for name in names:
            author = name.find_element_by_css_selector("div.user_profile_name a")
            totalNames.append(''.join([c for c in author.text if c not in "1234567890"]))
        # Recorrer Fechas y agregarlas al Array
        for date in dates:
            totalDates.append(date.text)
        # Recorrer Titulos y agregarlos al Array
        for title in qTitles:
            titleHeader = title.find_element_by_css_selector("h4.feeditemtext.cxquestiontitlewithlink a")
            totalqTitles.append(titleHeader.text)
            totalqLinks.append(titleHeader.get_attribute('href'))
        return totalDates, totalNames, totalqLinks, totalqTitles

    @staticmethod
    def tomar_datos(driver):
        # Tomar datos
        names = driver.find_elements_by_class_name("user_profile_name")  # Tomar nombes
        dates = driver.find_elements_by_class_name("feeditemtimestamp")  # Tomar fechas
        qTitles = driver.find_elements_by_css_selector(
            ".feeditemtext.cxquestiontitlewithlink")  # Tomar Titulos de preguntas
        return dates, names, qTitles
