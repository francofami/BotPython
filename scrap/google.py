from package import module
import pandas as panda
from selenium import webdriver
import sys

sys.path.append('../')


def main():
    print("Iniciando...")
    ScraperGoogle.search()


class ScraperGoogle:
    def __init__(self, name, date, title, link):

        self.name = name

        self.date = date

        self.title = title

        self.link = link

    @staticmethod
    def search():

        # scrap user names from forum
        users = module.ScraperForo.buscar_foro()
        users = ScraperGoogle(users.Name, users.Date, users.Title, users.Link)

        print("User names:\n")
        print(users.name)

        # new Chrome tab
        driver = webdriver.Chrome('../chromedriver.exe')

        links_perfiles = []



        # adjunto nombre de usuario y link a linkedin
        for usuario in users.name:

            # opens google
            ScraperGoogle.cargar_google(driver)


            try:
                ScraperGoogle.iniciar_busqueda(driver, usuario, "salesforce")

                ScraperGoogle.tomar_links(links_perfiles, driver)
            except:
                print("NoSuchElementException - user(" + usuario + ") was probably not found on google")
                print("Searching again without the salesforce keyword...")

                ScraperGoogle.cargar_google(driver)

                ScraperGoogle.iniciar_busqueda(driver, usuario, "")

                ScraperGoogle.tomar_links(links_perfiles, driver)

        # myFile = {'Linkedin': LinkedLinks}
        users2 = {'Date': u1.date, 'Name': u1.name, 'Title': u1.title, 'Link forum': u1.link, 'Linkedin': links_perfiles}
        myFileObj = type('obj', (object,), users2)

        df = panda.DataFrame(users2)
        df.to_csv('links.csv', index=False)

        driver.close()
        print("Scraping finished")
        return myFileObj

    @staticmethod
    def cargar_google(driver):
        driver.get("https://google.com")

    @staticmethod
    def tomar_links(links_perfiles, driver):
        links = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/div[1]/a')
        links_perfiles.append(links.get_attribute("href"))

    @staticmethod
    def iniciar_busqueda(driver, usuario, parametros_busqueda):
        buscador_input = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        buscador_input.send_keys("\"" + usuario + "\" \"" + parametros_busqueda + '\" site:linkedin.com')
        driver.find_element_by_xpath('//*[@id="lga"]').click()
        driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]').click()


if __name__ == '__main__':
    main()
