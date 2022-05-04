# -*- coding: utf-8 -*-

import base64
import datetime
import logging
import os
import time
import traceback
import subprocess

from lxml import etree

_logger = logging.getLogger(__name__)

try:
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
	from selenium.webdriver.common.by import By
	from selenium.common.exceptions import NoSuchElementException, WebDriverException
	from selenium.webdriver import DesiredCapabilities
	from selenium.webdriver.common.action_chains import ActionChains
	_silenium_lib_imported = True
except ImportError:
	_silenium_lib_imported = False
	_logger.info(
		"The `selenium` Python module is not available. "
		"WhatsApp Automation will not work. "
		"Try `pip3 install selenium` to install it."
	)

driver = {}
wait={}
wait5={}
is_session_open = {}
options = {}
msg_sent = False

dir_path = os.path.dirname(os.path.realpath(__file__))

try:
	import phonenumbers
	from phonenumbers.phonenumberutil import region_code_for_country_code
	_sms_phonenumbers_lib_imported = True

except ImportError:
	_sms_phonenumbers_lib_imported = False
	_logger.info(
		"The `phonenumbers` Python module is not available. "
		"Phone number validation will be skipped. "
		"Try `pip3 install phonenumbers` to install it."
	)

def send_whatsapp_msgs(number, msg, get_qr=False, group_name=False):
	global driver
	global wait
	global wait5
	global msg_sent
	unique_user = 'usuario_0'
	try:
		elements  = driver.get(unique_user).find_elements_by_class_name('_20c87')
		if not elements:
			try:
				landing_wrapper_xpath = "//div[contains(@class, 'landing-wrapper')]"
				landing_wrapper = wait5.get(unique_user).until(EC.presence_of_element_located((
					By.XPATH, landing_wrapper_xpath)))
				try:
					elements = driver.get(unique_user).find_elements_by_class_name('_2znac')
					for e in elements:
						e.click()
				except:
					pass
				qr_code_xpath = "//canvas[contains(@aria-label, 'Scan me!')]"
				qr_code = wait5.get(unique_user).until(EC.presence_of_element_located((
					By.XPATH, qr_code_xpath)))
				base64_image = driver.get(unique_user).execute_script("return document.querySelector('canvas').toDataURL('image/png');")
				return {"isLoggedIn": False, 'qr_image': base64_image}
			except NoSuchElementException as e:
				traceback.print_exc()
			except Exception as ex:
				traceback.print_exc()
	except (NoSuchElementException, Exception):
		traceback.print_exc()
		if get_qr:
			return False
	try:
		elements  = driver.get(unique_user).find_elements_by_class_name('_2Zdgs')
		for e in elements:
			e.click()
			time.sleep(7)
	except Exception as e:
		traceback.print_exc()
	if group_name:
		try:
			time.sleep(2)
			inp_elements  = driver.get(unique_user).find_elements_by_class_name('_13NKt')
			inp_element = inp_elements and inp_elements[0]
			if inp_element:
				inp_element.clear()
				inp_element.send_keys(group_name)
				time.sleep(2)
			try:
				selected_contact = driver.get(unique_user).find_element_by_xpath("//span[@title='"+group_name+"']")
				selected_contact.click()
			except (NoSuchElementException, Exception) as e:
				return {'group_not_available': True}
			enter_elements  = driver.get(unique_user).find_elements_by_class_name('_13NKt')
			enter_element = enter_elements and enter_elements[1]
			if enter_element:
				msg = msg.replace('PARTNER', 'Group Members')
				if "\n" in msg:
					for ch in msg:
						if ch == "\n":
							ActionChains(driver.get(unique_user)).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
						else:
							enter_element.send_keys(ch)
					enter_element.send_keys(Keys.ENTER)
				else:
					enter_element.send_keys(msg + Keys.ENTER)
				time.sleep(1)

			return {'result': True}
		except Exception as ex:
			msg_sent = False
			return {'result': False}

	try:
		driver.get(unique_user).find_element_by_id('sender')
	except NoSuchElementException as e:
		msg_sent = False
		script = 'var newEl = document.createElement("div");newEl.innerHTML = "<a href=\'#\' id=\'sender\' class=\'executor\'> </a>";var ref = document.querySelector("div#pane-side");ref.parentNode.insertBefore(newEl, ref.previousSibling);'
		driver.get(unique_user).execute_script(script)
	try:
		driver.get(unique_user).execute_script("var idx = document.getElementsByClassName('executor').length -1; document.getElementsByClassName('executor')[idx].setAttribute(arguments[0], arguments[1]);", "href", "https://api.whatsapp.com/send?phone=" + number + "&text=" + msg.replace('\n', '%0A'))
		time.sleep(2)
		driver.get(unique_user).find_element_by_id('sender').click()

		time.sleep(2)
		inp_elements  = driver.get(unique_user).find_elements_by_class_name('_13NKt')
		inp_element = inp_elements and inp_elements[1]
		if inp_element:
			inp_element.send_keys(Keys.ENTER)
			time.sleep(2)

		msg_sent = True
	except Exception as e:
		msg_sent = False



def browser_session_open(unique_user):
	unique_user_self = 'usuario_0'
	global is_session_open
	global options
	global dir_path
	options[unique_user] = webdriver.ChromeOptions()
	options[unique_user].add_argument('--user-data-dir=' + dir_path + '/.user_data_uid_' + str(unique_user))
	options[unique_user].add_argument('--headless')
	options[unique_user].add_argument('--no-sandbox')
	options[unique_user].add_argument('--window-size=1366,768')
	options[unique_user].add_argument('--enable-logging=stderr')
	options[unique_user].add_argument('--disable-gpu')
	# user_agent = '"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"'
	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36'
	options[unique_user].add_argument('user-agent='+user_agent)
	global driver
	global wait
	global wait5
	capabilities = DesiredCapabilities.CHROME.copy()
	capabilities['acceptSslCerts'] = True
	capabilities['acceptInsecureCerts'] = True
	try:
		e_path = dir_path + '/chromedriver_79'
		chromium_version = subprocess.check_output(['chromium-browser', '--version'], stderr=subprocess.STDOUT)
		chromium_version = chromium_version and chromium_version.split()[1]
		if chromium_version.startswith(b'79.'):
			e_path = dir_path + '/chromedriver_79'
		elif chromium_version.startswith(b'84.'):
			e_path = dir_path + '/chromedriver_84'
	except (subprocess.CalledProcessError, Exception):
		e_path = dir_path + '/chromedriver_79'
		chrome_version = subprocess.check_output(['google-chrome', '--version'], stderr=subprocess.STDOUT)
		chrome_version = chrome_version and chrome_version.split()[2]
		if chrome_version.startswith(b'79.'):
			e_path = dir_path + '/chromedriver_79'
		elif chrome_version.startswith(b'84.'):
			e_path = dir_path + '/chromedriver_84'

	# For portable chrome
	e_path = dir_path + '/chromedriver_79'
	options[unique_user].binary_location = dir_path + '/chrome/chrome'
	driver[unique_user] = webdriver.Chrome(executable_path=e_path, options=options.get(unique_user), desired_capabilities=capabilities)
	wait[unique_user] = WebDriverWait(driver.get(unique_user_self), 10)
	wait5[unique_user] = WebDriverWait(driver.get(unique_user_self), 5)
	driver.get(unique_user).get("https://web.whatsapp.com")
	ixpath = "//div[contains(@id, 'pane-side')]"
	is_session_open[unique_user_self] = True
	try:
		wait.get(unique_user).until(EC.presence_of_element_located((
				By.XPATH, ixpath)))
		script = 'var newEl = document.createElement("div");newEl.innerHTML = "<a href=\'#\' id=\'sender\' class=\'executor\'> </a>";var ref = document.querySelector("div#pane-side");ref.parentNode.insertBefore(newEl, ref.previousSibling);'
		driver.get(unique_user).execute_script(script)
	except Exception as e:
		pass

def _cron_kill_chromedriver():
	unique_user = 'usuario_0'
	global driver
	try:
		driver.get(unique_user).close()
		driver.get(unique_user).quit()
		driver[unique_user] = None
		is_session_open[unique_user] = None
	except Exception as e:
		pass

def get_status():
	unique_user = 'usuario_0'
	global is_session_open
	try:
		driver.get(unique_user).title
		return True
	except WebDriverException:
		is_session_open[unique_user] = False
		return False

 def action_send_msg():
	unique_user = 'usuario_0'
	if not _silenium_lib_imported:
		raise UserError('Silenium is not installed. Please install it.')
	global is_session_open
	global msg_sent
	try:
		if not is_session_open.get(unique_user) or not get_status():
			browser_session_open(unique_user)
	except Exception as e:
		_logger.warning('Error opening Browser %s' % str(e))

	check = {}
	try:
		check = send_whatsapp_msgs(number, self.message.replace('PARTNER', partner.name))
	except:
		_logger.warning('Failed to send Message to WhatsApp number ', number)