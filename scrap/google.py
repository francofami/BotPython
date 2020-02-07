import pandas as panda
from selenium import webdriver
try:
    import sys
    sys.path.append('../')
    from BotPython.package import module
except:
    from package import module
from selenium.webdriver.common.keys import Keys

def main():

    # scrap user names from forum
    """users = module.ScraperForo.buscarPersonasForo()
    u1 = ScraperGoogle(users.Name, users.Date, users.Title, users.Link)

    print("User names:\n")
    print(u1.name)"""
    print("hello")
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
        users = module.ScraperForo.buscarPersonasForo()
        u1 = []
        u1 = ScraperGoogle(users.Name, users.Date, users.Title, users.Link)


        print("User names:\n")
        print(u1.name)



        # Scrap google input tag
        # input = driver.find_elements_by_class_name("gLFyf")
        len = u1.__sizeof__()
        # new Chrome tab
        try:
            driver = webdriver.Chrome('../chromedriver')
        except:
            driver = webdriver.Chrome('./chromedriver')

        totalNames = []
        totalDates = []
        totalqTitles = []
        totalqLinks = []
        LinkedLinks = []

        #adjunto fecha
        #for date in dates:

        #adjunto titulo de la pregunta y link a pregunta en el foro
        #for title in qTitles:


        #adjunto nombre de usuario y link a linkedin
        for usuario in u1.name:


            # opens google
            driver.get("https://google.com")

            googleInput = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
            try:
                googleInput.send_keys("\"\"" + usuario + "\"\"" + 'salesforce site:linkedin.com' )
                # search button
                driver.find_element_by_xpath('//*[@id="lga"]').click()
                driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]').click()
                # googleInput.sendKeys(Keys.RETURN)

                # google scraping
                # bigDiv = driver.find_element_by_class_name('srg')
                Links = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/div[1]/a')
                LinkedLinks.append(Links.get_attribute("href"))
            except:
                print("NoSuchElementException - user("+usuario+") was probably not found on google")
                print("Searching again without the salesforce keyword...")

                # opens google
                driver.get("https://google.com")

                googleInput = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
                googleInput.send_keys("\"\"" + usuario + "\"\"" + ' site:linkedin.com')
                # search button
                driver.find_element_by_xpath('//*[@id="lga"]').click()
                driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]').click()
                # googleInput.sendKeys(Keys.RETURN)

                # google scraping
                # bigDiv = driver.find_element_by_class_name('srg')
                Links = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/div[1]/a')
                LinkedLinks.append(Links.get_attribute("href"))

        #myFile = {'Linkedin': LinkedLinks}
        users2 = {'Date':u1.date, 'Name':u1.name, 'Title':u1.title, 'Link forum':u1.link, 'Linkedin': LinkedLinks}
        myFileObj = type('obj', (object,), users2)

        df = panda.DataFrame(users2)
        df.to_csv('links.csv', index=False)

        driver.close()
        print("Scraping finished")
        return myFileObj


if __name__ == '__main__':
   main()