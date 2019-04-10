try:
    from PIL import Image

except ImportError:
    import Image

import pytesseract
import time
from datetime import datetime
from datetime import timedelta
from enroll_config import keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

def order(k):
	driver = webdriver.Chrome('.\chromedriver')
	pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
	driver.maximize_window()
	chrome_options = Options()
	chrome_options.add_experimental_option("detach", True)
	driver.get(k['web_url'])
	time.sleep(1)
	driver.find_element_by_xpath('//*[@id="username"]').send_keys(k["UCSC_ID"])
	driver.find_element_by_xpath('//*[@id="password"]').send_keys(k["GOLD_PASS"])
	driver.find_element_by_xpath('/html/body/section/div/form/button').click()
	driver.find_element_by_xpath('//*[@id="shibSubmit"]').click()
	driver.find_element_by_xpath('//*[@id="SCX_FA_CHECK$5"]').click()
	time.sleep(1)
	driver.find_element_by_xpath('//*[@id="PTGP_STEP_DVW_PTGP_STEP_LABEL$7"]').click()
	

	iframe = driver.find_elements_by_tag_name('iframe')[0]
	driver.switch_to.frame(iframe)
	driver.find_element_by_xpath('//*[@id="SSR_DUMMY_RECV1$sels$1$$0"]').click()
	driver.find_element_by_xpath('//*[@id="DERIVED_SSS_SCT_SSR_PB_GO"]').click()

	driver.switch_to.default_content()

	iframe1= driver.find_elements_by_tag_name('iframe')[0]
	driver.switch_to.frame(iframe1)
	time.sleep(1)
	driver.find_element_by_xpath('//*[@id="P_SELECT$0"]').click()

	runAt = run_at(k["enroll_date"])
	time_left = time_in_seconds(runAt)

	while(time_left != 0 and time_left > 0):
		runAt = run_at(k["enroll_date"])
		time_left = time_in_seconds(runAt)
		print(time_left)

	if time_left < 0:
		print("You missed your optimum enrollment time!!!")
		driver.find_element_by_xpath('//*[@id="DERIVED_REGFRM1_LINK_ADD_ENRL$291$"]').click()
		print("ENROLLED!")

	else:
		driver.find_element_by_xpath('//*[@id="DERIVED_REGFRM1_LINK_ADD_ENRL$291$"]').click()
		print("ENROLLED!")
	
	time.sleep(5)

	#ScreenShot of page
	pic_n = "Enrollment Status.png"
	driver.save_screenshot(pic_n)
	image_to_text = pytesseract.image_to_data(Image.open(pic_n))
	print("--------------------------------------------------------------------------------------------------------------------------")
	print(image_to_text)
	print("--------------------------------------------------------------------------------------------------------------------------")
	#Send output to file
	fh = open("output.txt", "w")
	fh.write(image_to_text)

def run_at(time):
	now = str(datetime.now()).split(".")[0]
	enroll_time = time
	FMT = '%Y-%m-%d %H:%M:%S'
	tdelta = datetime.strptime(enroll_time, FMT) - datetime.strptime(now, FMT)
	return tdelta

def time_in_seconds(t):
	return t.total_seconds()

def event(time):
	print("Your Enrollment Time is at: " + str(datetime.strptime(time, '%Y-%m-%d %H:%M:%S')))
        print("--------------------------------------------------------------------------------------------------------------------------")


if __name__ == '__main__':
	event(keys['enroll_date'])
	start_time = time.time()
	order(keys)
	end_time = time.time()
	print("EXECUTION TIME: " + str(round(end_time - start_time, 1)))
	
