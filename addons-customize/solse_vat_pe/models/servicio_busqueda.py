# -*- encoding: utf-8 -*-
import requests
import logging

from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from io import StringIO
import io
import logging
from PIL import Image
from bs4 import BeautifulSoup
import time
import unicodedata
import os

try:
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver import DesiredCapabilities
	_silenium_lib_imported = True
except ImportError:
	_silenium_lib_imported = False

dir_path = os.path.dirname(os.path.realpath(__file__))

_logger = logging.getLogger(__name__)

STATE = [('ACTIVO', 'ACTIVO'),
		 ('BAJA DE OFICIO', 'BAJA DE OFICIO'),
		 ('BAJA DEFINITIVA', 'BAJA DEFINITIVA'),
		 ('BAJA PROVISIONAL', 'BAJA PROVISIONAL'),
		 ('SUSPENSION TEMPORAL', 'BAJA PROVISIONAL'),
		 ('INHABILITADO-VENT.UN', 'INHABILITADO-VENT.UN'),
		 ('BAJA MULT.INSCR. Y O', 'BAJA MULT.INSCR. Y O'),
		 ('PENDIENTE DE INI. DE', 'PENDIENTE DE INI. DE'),
		 ('OTROS OBLIGADOS', 'OTROS OBLIGADOS'),
		 ('NUM. INTERNO IDENTIF', 'NUM. INTERNO IDENTIF'),
		 ('ANUL.PROVI.-ACTO ILI', 'ANUL.PROVI.-ACTO ILI'),
		 ('ANULACION - ACTO ILI', 'ANULACION - ACTO ILI'),
		 ('BAJA PROV. POR OFICI', 'BAJA PROV. POR OFICI'),
		 ('ANULACION - ERROR SU', 'ANULACION - ERROR SU')]

CONDITION = [('HABIDO', 'HABIDO'),
			 ('NO HABIDO', 'NO HABIDO'),
			 ('NO HALLADO', 'NO HALLADO'),
			 ('PENDIENTE', 'PENDIENTE'),
			 ('NO HALLADO SE MUDO D', 'NO HALLADO SE MUDO D'),
			 ('NO HALLADO NO EXISTE', 'NO HALLADO NO EXISTE'),
			 ('NO HALLADO FALLECIO', 'NO HALLADO FALLECIO'),
			 ('-', 'NO HABIDO'),
			 ('NO HALLADO OTROS MOT', 'NO HALLADO OTROS MOT'),
			 ('NO APLICABLE', 'NO APLICABLE'),
			 ('NO HALLADO NRO.PUERT', 'NO HALLADO NRO.PUERT'),
			 ('NO HALLADO CERRADO', 'NO HALLADO CERRADO'),
			 ('POR VERIFICAR', 'POR VERIFICAR'),
			 ('NO HALLADO DESTINATA', 'NO HALLADO DESTINATA'),
			 ('NO HALLADO RECHAZADO', 'NO HALLADO RECHAZADO')]

URL_CONSULT = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
HEADERS_CPE = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
HTML_PARSER = 'html.parser'

def getDatosDNI(dni):
	try:
		API_ENDPOINT = "http://webexterno.sutran.gob.pe/ConsultaSutran/"
		r = requests.post(url = API_ENDPOINT, data={'TipoConsulta': 1, 'Vehiculo.Placa': dni}) 
		pastebin_url = r.text 
		soup = BeautifulSoup(pastebin_url)
		dni = soup.find_all("div", class_="app")[0].find_all("div", class_="row")[5].find_all("p")[0]
		dni = str(dni).replace("<p>", "").replace("</p>", "").replace("|", "")
		return dni.strip()
	except Exception as e:
		return ""

def getDatosRUC(ruc):
	try:
		url_sunat = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
		session = requests.Session()
		headers = requests.utils.default_headers()
		headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36'
		url_numRnd = session.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorRazonSoc&razSoc=BVA%20FOODS', headers=headers,timeout=12).content
		html_content = BeautifulSoup(url_numRnd, HTML_PARSER)
		content_form = html_content.find_all('form')
		numRnd = content_form[0].find_all('input')[3].get('value')
		data_ruc = {'accion':'consPorRuc','nroRuc':ruc,'numRnd':numRnd,'actReturn':'1','modo':'1'}
		html_doc = session.post(url=url_sunat,data=data_ruc,headers=headers,timeout=(15,20))
		html_info = BeautifulSoup(html_doc.content, 'html.parser')
		#return r.text
		#return extraerDatos(r.text)
		return extraerDatos(html_info)
	except Exception as e:
		return {'error': True, 'message': 'Error al intentar obtener datos'}
		
def extraerDatos(soup):
	try:
		titulo = soup.find_all('title')
		titulo = titulo[0].get_text()
		if "Celular" in titulo:
			return extraerDatosMovil(soup)
		else:
			return extraerDatosWeb(soup)
	except Exception as e:
		_logger.info('Error al intentar extraer los datos, intentelo denuevo')
		
def extraerDatosWeb(soup):
	try:
		div_info = soup.find_all("div", {"class": "list-group"})
		div_info = div_info[0]
		divs = div_info.find_all("div", {"class": "list-group-item"})

		datos = {'error': False, 'message': 'ok'}
		for div in divs:
			campo = div.find_all("h4", {"class": "list-group-item-heading"})
			campo = (campo[0].get_text()).strip()

			if "n del Contribuyente:" in campo:
				valor = div.find_all("p", {"class": "list-group-item-text"})
				valor = (valor[0].get_text()).strip()
				datos['condicion'] = valor
			elif "Estado del Contribuyente:" in campo:
				valor = div.find_all("p", {"class": "list-group-item-text"})
				valor = (valor[0].get_text()).strip()
				datos['estado'] = valor
			elif "Tipo Contribuyente:" in campo:
				valor = div.find_all("p", {"class": "list-group-item-text"})
				valor = (valor[0].get_text()).strip()
				datos['tipo_contribuyente'] = valor
			elif "n de Comprobante" in campo:
				valor = div.find_all("p", {"class": "list-group-item-text"})
				valor = (valor[0].get_text()).strip()
				datos['sistema_emision'] = valor
			elif "Sistema de Contabilidad:" in campo:
				valor = div.find_all("p", {"class": "list-group-item-text"})
				valor = (valor[0].get_text()).strip()
				datos['sistema_contabilidad'] = valor
			elif "Domicilio Fiscal" in campo:
				valor = div.find_all("p", {"class": "list-group-item-text"})
				valor = (valor[0].get_text()).strip()
				direccion = valor
				completo = direccion.split(' - ')
				if len(completo) > 2:
					datos['distrito'] = completo[len(completo)-1].strip()
					datos['provincia'] = completo[len(completo)-2].strip()
					departamento = completo[len(completo)-3].strip().split(' ')
					datos['departamento'] = departamento[len(departamento)-1].strip()
					for idr in range(0, len(completo)-1):
						completo[idr] = completo[idr].strip()
				else:
					datos['distrito'] = 'LIMA'
					datos['provincia'] = 'LIMA'
					datos['departamento'] = 'LIMA'
				datos['direccion'] = ' - '.join(completo)
			elif "mero de RUC:" in campo:
				valor = div.find_all("h4", {"class": "list-group-item-heading"})
				valor = (valor[1].get_text()).strip()
				razon = valor.split('-')
				datos['razonSocial'] = razon[1].strip()
				datos['ruc'] = razon[0].strip()
		return datos
	except Exception as e:
		return {'error': True, 'message': 'Error al intentar extraer los datos, intentelo denuevo'}

def extraerDatosMovil(soup):
	try:
		#soup = BeautifulSoup(datos, HTML_PARSER)
		tabla = soup.find_all('table')
		tabla2 = tabla[0]
		trs = tabla2.find_all('tr')
		datos = {'error': False, 'message': 'ok'}
		for tr in trs:
			tds = tr.find_all('td', class_='bg')
			tr_texto = str(tr.get_text())
			if "Condición:" in tr_texto:
				datos['condicion'] = str(tds[0].get_text()).strip()
			elif "Estado:" in tr_texto:
				datos['estado'] = str(tds[0].get_text()).strip()
			elif "Tipo Contribuyente:" in tr_texto:
				datos['tipo_contribuyente'] = str(tds[0].get_text()).strip()
			elif "Sistema de Emisión Electrónica:" in tr_texto:
				datos['sistema_emision'] = str(tds[0].get_text()).strip()
			elif "Sistema de Contabilidad:" in tr_texto:
				datos['sistema_contabilidad'] = str(tds[0].get_text()).strip()
			elif "Domicilio Fiscal:" in tr_texto:
				direccion = str(tds[0].get_text()).strip()
				completo = direccion.split(' - ')
				if len(completo) > 2:
					datos['distrito'] = completo[len(completo)-1].strip()
					datos['provincia'] = completo[len(completo)-2].strip()
					departamento = completo[len(completo)-3].strip().split(' ')
					datos['departamento'] = departamento[len(departamento)-1].strip()
					for idr in range(0, len(completo)-1):
						completo[idr] = completo[idr].strip()
				else:
					datos['distrito'] = 'LIMA'
					datos['provincia'] = 'LIMA'
					datos['departamento'] = 'LIMA'
				datos['direccion'] = ' - '.join(completo)
			elif "RUC:" in tr_texto and tds:
				razon = str(tds[0].get_text()).strip().split(' - ')
				datos['razonSocial'] = razon[1].strip()
				datos['ruc'] = razon[0].strip()
		return datos
	except Exception as e:
		return {'error': True, 'message': 'Error al intentar extraer los datos, intentelo denuevo'}
	
# ::::::::::::::::: Usando API de APIPERU.dev

def get_dni_apiperu(token, dni):
	endpoint = "https://apiperu.dev/api/dni/%s" % dni
	headers = {
		"Authorization": "Bearer %s" % token,
		"Content-Type": "application/json",
	}
	datos_dni = requests.get(endpoint, data={}, headers=headers)
	if datos_dni.status_code == 200:
		datos = datos_dni.json()
		return datos['data']['nombre_completo']
	else:
		return ""

def get_ruc_apiperu(token, ruc):
	endpoint = "https://apiperu.dev/api/ruc/%s" % ruc
	headers = {
		"Authorization": "Bearer %s" % token,
		"Content-Type": "application/json",
	}
	datos_ruc = requests.get(endpoint, data={}, headers=headers)
	if datos_ruc.status_code == 200:
		datos_ruc = datos_ruc.json()
		_logger.info('66666666666666')
		_logger.info(datos_ruc)
		ubigeo = datos_ruc['data']['ubigeo'][2]
		direccion = datos_ruc['data']['direccion_completa'] if 'direccion_completa' in datos_ruc['data'] else ''
		datos = {
			'error': False, 
			'message': 'ok',
			'condicion': datos_ruc['data']['condicion'],
			'estado': datos_ruc['data']['estado'],
			'ubigeo': ubigeo if ubigeo != "-" else "150101",
			'direccion': direccion.split(',')[0],
			'razonSocial': datos_ruc['data']['nombre_o_razon_social'],
			'ruc': datos_ruc['data']['ruc'],
		}
		return datos
	else:
		return {'error': True, 'message': 'Error al intentar obtener datos'}

# :::::::::::::::: Uso de selenium
def get_ruc_selenium(ruc):
	global dir_path
	datos_json = {'error': True, 'message': 'error al cargar'}

	capabilities = DesiredCapabilities.CHROME.copy()
	capabilities['acceptSslCerts'] = True
	capabilities['acceptInsecureCerts'] = True
	options_driver = webdriver.ChromeOptions()
	options_driver.add_argument('--no-sandbox')
	options_driver.add_argument('--headless')
	options_driver.add_argument('--window-size=1366,768')
	options_driver.add_argument('--enable-logging=stderr')
	options_driver.add_argument('--disable-gpu')
	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36'
	options_driver.add_argument('user-agent='+user_agent)
	e_path = dir_path + '/../extras/chromedriver_79'
	options_driver.binary_location = dir_path + '/../extras/chrome/chrome'
	driver = webdriver.Chrome(executable_path=e_path, options=options_driver, desired_capabilities=capabilities)
	if not driver:
		return datos_json
	driver.get("https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias")
	elem = driver.find_element_by_name("search1")
	if not elem:
		return datos_json
	elem.clear()
	elem.send_keys(str(ruc))
	elem.send_keys(Keys.RETURN)
	boton = driver.find_element_by_id("btnAceptar")
	if not boton:
		return datos_json
	boton.click()
	time.sleep(1)
	datos = driver.find_elements_by_class_name('list-group-item')
	
	for reg in datos:
		cabecera = reg.find_elements_by_class_name('list-group-item-heading')
		if cabecera:
			cabecera = cabecera[0].text
		else:
			continue
		if "n del Contribuyente:" in cabecera:
			dato = reg.find_elements_by_class_name('list-group-item-text')
			datos_json['condicion'] = dato[0].text
		elif "Estado del Contribuyente:" in cabecera:
			dato = reg.find_elements_by_class_name('list-group-item-text')
			datos_json['estado'] = dato[0].text
		elif "Tipo Contribuyente:" in cabecera:
			dato = reg.find_elements_by_class_name('list-group-item-text')
			datos_json['tipo_contribuyente'] = dato[0].text
		elif "n de Comprobante" in cabecera:
			dato = reg.find_elements_by_class_name('list-group-item-text')
			datos_json['sistema_emision'] = dato[0].text
		elif "Sistema de Contabilidad:" in cabecera:
			dato = reg.find_elements_by_class_name('list-group-item-text')
			datos_json['sistema_contabilidad'] = dato[0].text
		elif "Domicilio Fiscal" in cabecera:
			dato = reg.find_elements_by_class_name('list-group-item-text')
			direccion = dato[0].text
			completo = direccion.split(' - ')
			if len(completo) > 2:
				datos_json['distrito'] = completo[len(completo)-1].strip()
				datos_json['provincia'] = completo[len(completo)-2].strip()
				departamento = completo[len(completo)-3].strip().split(' ')
				datos_json['departamento'] = departamento[len(departamento)-1].strip()
				for idr in range(0, len(completo)-1):
					completo[idr] = completo[idr].strip()
			else:
				datos_json['distrito'] = 'LIMA'
				datos_json['provincia'] = 'LIMA'
				datos_json['departamento'] = 'LIMA'

			dir_c = ' - '.join(completo)
			rem = datos_json['departamento']+' - '+datos_json['provincia']+' - '+datos_json['distrito']
			dir_final = dir_c.replace(rem, '')
			datos_json['direccion'] = dir_final
		elif "mero de RUC:" in cabecera:
			dato = reg.find_elements_by_class_name('list-group-item-heading')
			valor = dato[1].text
			razon = valor.split('-')
			datos_json['razonSocial'] = razon[1].strip()
			datos_json['ruc'] = razon[0].strip()

	if driver:
		driver.close()
	datos_json['error'] = False
	datos_json['message'] = 'ok'
	return datos_json

def get_dni_selenium(nro_dni):
	global dir_path
	datos_json = {'error': True, 'message': 'error al cargar'}

	capabilities = DesiredCapabilities.CHROME.copy()
	capabilities['acceptSslCerts'] = True
	capabilities['acceptInsecureCerts'] = True
	options_driver = webdriver.ChromeOptions()
	options_driver.add_argument('--headless')
	options_driver.add_argument('--no-sandbox')
	options_driver.add_argument('--window-size=1366,768')
	options_driver.add_argument('--enable-logging=stderr')
	options_driver.add_argument('--disable-gpu')
	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36'
	options_driver.add_argument('user-agent='+user_agent)
	e_path = dir_path + '/../extras/chromedriver_79'
	options_driver.binary_location = dir_path + '/../extras/chrome/chrome'
	driver = webdriver.Chrome(executable_path=e_path, options=options_driver, desired_capabilities=capabilities)
	if not driver:
		return ""
	driver.get("https://eldni.com/pe/buscar-por-dni")
	elem = driver.find_element_by_name("dni")
	if not elem:
		return ""
	elem.clear()
	elem.send_keys(str(nro_dni))
	elem.send_keys(Keys.RETURN)
	time.sleep(1)
	time.sleep(1)
	datos = driver.find_elements_by_class_name('table')
	regs = datos[0].find_elements_by_tag_name('td')
	nombre_completo = regs[1].text +', '+regs[2].text+' '+regs[3].text
	if driver:
		driver.close()
	datos_json['error'] = False
	datos_json['message'] = 'ok'
	return nombre_completo