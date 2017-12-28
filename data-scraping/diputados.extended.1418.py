# -*- coding: utf-8 -*-
import json

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import imp
import scraperhelper
imp.reload(scraperhelper)

scraperhelper.setOutputDescription(
        'Lista de todos los Diputados para el período 2014-2018',
        {
            'type': 'Dictionary',
            'elements': [
                {'type': 'String', 'name': 'prmid', 'description': ''},
                {'type': 'String', 'name': 'nombre', 'description': ''},
                {'type': 'String', 'name': 'periodo', 'description': ''},
                {'type': 'String', 'name': 'nacimiento', 'description': ''},
                {'type': 'String', 'name': 'profesion', 'description': ''},
                {'type': 'String', 'name': 'telefono', 'description': ''},
                {'type': 'String', 'name': 'correo', 'description': ''},
                {'type': 'String', 'name': 'comuna', 'description': ''},
                {'type': 'String', 'name': 'distrito', 'description': ''},
                {'type': 'String', 'name': 'region', 'description': ''},
                {'type': 'String', 'name': 'periodos', 'description': ''},
                {'type': 'String', 'name': 'comite_parlamentario', 'description': ''}
            ]
        }
)

scraperhelper.setPrintTimeTo(True)
browser = scraperhelper.initBrowser()

# get saved representatives 
diputados = json.load(open('./data/diputados.simple.1418.json'))

# output lists
data = []
errors = []


#GO!
counting = 0
for rep in diputados['data']:
    counting = counting + 1
    saved = False
    rep_extended = {
            "prmid":rep['prmid'],
            "nombre":rep['nombre'],
            "periodo":rep['periodo'],
            "nacimiento":'',
            "profesion":'',
            "telefono":'',
            "correo":'',
            "comuna":'',
            "distrito":'',
            "region":'',
            "periodos":[],
            "comite_parlamentario":''
        }
    
    try:        
        browser.get('https://www.camara.cl/camara/diputado_detalle.aspx?prmid='+str(rep['prmid']))
        
        # Basic Info
        ficha = browser.find_element_by_css_selector('#ficha')
        rep_extended['nacimiento'] = ficha.find_element_by_css_selector('div.birthDate p').text
        rep_extended['profesion'] = ficha.find_element_by_css_selector('div.profession p').text
        
        summary = browser.find_elements_by_css_selector('#ficha .summary')
        location = summary[0].find_elements_by_css_selector('p')        
        rep_extended['comuna'] = location[0].text
        rep_extended['distrito'] = location[1].text
        rep_extended['region'] = location[2].text
        
        periods = summary[1].find_elements_by_css_selector('ul li')
        for pe in periods:
            rep_extended['periodos'].append(pe.text)
        
        commitees= summary[2].find_elements_by_css_selector('p')
        for co in commitees:
            rep_extended['comite_parlamentario'] = rep_extended['comite_parlamentario'] + co.text
        
        rep_extended['telefono'] = ficha.find_element_by_css_selector('div.phones p').text.replace('Teléfono: ','')
        rep_extended['correo'] = ficha.find_element_by_css_selector('li.email a').text        
        
        data.append(rep_extended)
        saved = True
    
    except TimeoutException as ex:
        scraperhelper.pt('PAGE TimeoutException ERROR')
    except NoSuchElementException as ex:
        scraperhelper.pt('PAGE NoSuchElementException ERROR')
    except StaleElementReferenceException as ex:
        scraperhelper.pt('PAGE StaleElementReferenceException ERROR')
    except WebDriverException as ex:
        scraperhelper.pt('PAGE WebDriverException ERROR')
    
    finally:
        scraperhelper.pt('Loaded Representative ' + rep['prmid'])
        if not saved:
            errors.append(rep['prmid'])
            print('----------- WITH ERROR! -------------')

scraperhelper.closeSeleniumBrowser(browser)
scraperhelper.saveToFile('diputados.extended.1418', data, errors)
