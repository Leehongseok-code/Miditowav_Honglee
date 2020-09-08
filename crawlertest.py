
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.onlineconverter.com/midi-to-wav')
sam=driver.find_element_by_css_selector("file")
driver.execute_script("arguments[0].click();", sam)

#sam.click()
print(sam)
#sam.send_keys(r"C:\Users\User\PycharmProjects\PyFluid\Music\aqua.mid")
