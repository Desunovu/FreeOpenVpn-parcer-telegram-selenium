import time
from time import sleep
import sys
import os

from twocaptcha.solver import TwoCaptcha

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# urllist = [
#     "https://www.freeopenvpn.org/premium.php?cntid=USA&lang=en",
#     "https://www.freeopenvpn.org/premium.php?cntid=UK&lang=en",
#     "https://www.freeopenvpn.org/premium.php?cntid=Germany&lang=en",
#     "https://www.freeopenvpn.org/premium.php?cntid=Netherlands&lang=en"
# ]


def driver_init():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver


def solver_init():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    config = {
        'server': '2captcha.com',
        'apiKey': '',
        'defaultTimeout': 120,
        'pollingInterval': 5,
    }

    solver = TwoCaptcha(**config)
    return solver


def get_download_link(driver: webdriver.Chrome):
    try:
        download_link = driver.find_element(by=By.XPATH,
                                            value="/html[1]/body[1]/center[3]/div[1]/div[2]/div[1]/p[1]/a[1]")
        return download_link.get_attribute('href')

    except Exception as ex:
        print("Error: cant find download link")
        return "no url"


def get_capthca(driver: webdriver.Chrome):
    try:
        img = driver.find_element(by=By.XPATH, value="/html[1]/body[1]/center[3]/div[1]/div[2]/div[1]/p[3]/img[1]")
        ActionChains(driver).scroll(0, 0, 0, 300, origin=img).perform()
        sleep(2)
        return img
    except Exception as ex:
        print("Error: cant find captcha")
        return None


def solve(solver: TwoCaptcha, imgpath):
    try:
        result = solver.normal(imgpath, numeric=1, minLength=9)

    except Exception as e:
        sys.exit(e)

    else:
        print('solved: ' + str(result))
        return result['code']


class SeleniumScript:
    def __init__(self):
        self.solver = None
        self.driver = None
        self.urllist = ["https://www.freeopenvpn.org/premium.php?cntid=Netherlands&lang=en"]

    def start_script(self):
        self.driver = driver_init()
        self.solver = solver_init()

        try:
            captcha_solved = "NoCaptcha"
            download_link = "NoURL"

            for i, url in enumerate(self.urllist):
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "result")))
                download_link = get_download_link(self.driver)
                captchaimg = get_capthca(self.driver)
                filename = f'{download_link.split("/")[4]}.png'
                captchaimg.screenshot(filename)
                time.sleep(4)
                self.driver.close()
                self.driver.quit()

                captcha_solved = solve(self.solver, filename)
                print(f"{captcha_solved} : {download_link}")
            return download_link, captcha_solved

        except Exception as ex:
            print(ex)
            self.driver.close()
            self.driver.quit()
        finally:
            pass


if __name__ == "__main__":
    script = SeleniumScript()
    link, captcha = script.start_script()
    print(f"{link}\n{captcha}")
