from package import scraper_foro
import pandas as panda
from selenium.common.exceptions import NoSuchElementException
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
        users = scraper_foro.ScraperForo.buscar_foro()
        users = ScraperGoogle(users.Name, users.Date, users.Title, users.Link)

        driver = scraper_foro.ScraperForo.abrir_navegador()

        for usuario in users.name:

            ScraperGoogle.cargar_google(driver)

            try:
                ScraperGoogle.iniciar_busqueda(driver, usuario, "salesforce")

                links_perfiles = ScraperGoogle.tomar_links(driver)
            except NoSuchElementException as e:
                ScraperGoogle.notificar_excepcion(e, usuario)

                ScraperGoogle.cargar_google(driver)

                ScraperGoogle.iniciar_busqueda(driver, usuario, "")

                links_perfiles = ScraperGoogle.tomar_links(driver)

            except ValueError as e:
                print(e)
                continue

            finally:
                continue

        # myFile = {'Linkedin': LinkedLinks}
        objeto_perfiles, users2 = ScraperGoogle.parse_objeto(links_perfiles, users)

        df = panda.DataFrame(users2)
        df.to_csv('links.csv', index=False)

        driver.close()
        print("Scraping finished")
        return objeto_perfiles

    @staticmethod
    def parse_objeto(links_perfiles, users):
        users2 = {'Date': users.date, 'Name': users.name, 'Title': users.title, 'Link forum': users.link,
                  'Linkedin': links_perfiles}
        objeto_perfiles = type('obj', (object,), users2)
        return objeto_perfiles, users2

    @staticmethod
    def notificar_excepcion(e, usuario):
        print(e + " - user(" + usuario + ") was probably not found on google")
        print("Searching again without the salesforce keyword...")

    @staticmethod
    def cargar_google(driver):
        driver.get("https://google.com")

    @staticmethod
    def tomar_links(driver):
        links_perfiles = []
        links = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/div[1]/a')
        links_perfiles.append(links.get_attribute("href"))
        return links_perfiles

    @staticmethod
    def iniciar_busqueda(driver, usuario, parametros_busqueda):
        buscador_input = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        buscador_input.send_keys("\"" + usuario + "\" \"" + parametros_busqueda + '\" site:linkedin.com')
        driver.find_element_by_xpath('//*[@id="lga"]').click()
        driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]').click()


if __name__ == '__main__':
    main()