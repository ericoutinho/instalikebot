from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from win10toast import ToastNotifier
from datetime import datetime
import time
import random

import credentials as c
import messages as m

from PySimpleGUI import PySimpleGUI as sg

class Instalikebot:

    def __init__(self, username, password, hashtag):
        self.messages = m.messages
        self.username = username
        self.password = password
        self.hashtag = hashtag
        # self.driver = webdriver.Firefox(executable_path=r"./geckodriver.exe")
        self.driver = webdriver.Firefox()

    @staticmethod
    def win_popup(title, content, duration=20):
        toast = ToastNotifier()
        toast.show_toast(title, content, duration=duration)


    @staticmethod
    def keylogger(message, target):
        for letter in message:
            target.send_keys(str(letter))
            time.sleep(random.randint(1,5)/10)


    def start(self):
        self.win_popup('Instalikebot','Bot iniciado')
        print('Instalikebot iniciado em ', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        driver = self.driver
        driver.get("https://instagram.com")
        time.sleep(3)
        input_username = driver.find_element_by_name('username')
        input_username.click()
        input_username.send_keys(self.username)
        input_password = driver.find_element_by_name('password')
        input_password.click()
        input_password.send_keys(self.password)
        input_password.send_keys(Keys.RETURN)
        time.sleep(5)

        # try:
        #     salvar = driver.find_element_by_class_name('yWX7d')
        #     salvar.click()
        #     time.sleep(4)
        # except Exception as e:
        #     print('Não encontrado')

        # try:
        #     notify = driver.find_element_by_class_name('HoLwm')
        #     notify.click()
        #     time.sleep(4)
        # except Exception as e:
        #     print('Não encontrado')

        self.like(self.hashtag)


    def like(self, hashtag):
        driver = self.driver
        driver.get("https://instagram.com/explore/tags/"+hashtag+"/")
        time.sleep(5)

        for i in range(4):
            # driver.execute_script("document.body.style.zoom = 1.0;")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        
        # hrefs = driver.find_elements_by_tag_name('a')
        hrefs = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']/a")
        pic_hrefs = [element.get_attribute('href') for element in hrefs]
        # [href for href in pic_hrefs if hashtag in href]

        print('Fotos com', hashtag, '=', str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            # tenta curtir
            try:
                driver.get(pic_href)
                time.sleep(random.randrange(10,15))
                # driver.execute_script("document.body.style.zoom = 0.5;")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.find_element_by_xpath("//span[@class='fr66n']/button[@class='wpO6b ']").click()
                print('Curtido: ', pic_href)
                time.sleep(10)
            except Exception as e:
                print('Não foi possível curtir', pic_href)
            # tenta comentar
            try:
                driver.find_element_by_class_name("Ypffh").click()
                comment = driver.find_element_by_class_name("Ypffh")
                time.sleep(2)
                self.keylogger(random.choice(self.messages), comment)
                time.sleep(5)
                comment.send_keys(Keys.RETURN)
                # driver.find_element_by_xpath('//button[@type='submit']').click()
                print('Comentado: ', pic_href)
            except Exception as e:
                # print('Não foi possível comentar', pic_href)
                print(e)
            
            time.sleep(random.randint(20,35))

        self.win_popup('Instalikebot', 'Bot encerrado')
        print('Instalikebot finalizado em', datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

mybot = Instalikebot(c.username, c.password, 'hastag_here')
mybot.start()