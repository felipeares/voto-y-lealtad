# -*- coding: utf-8 -*-
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
                {'type': 'String', 'name': 'periodo', 'description': ''}
            ]
        }
)

scraperhelper.setPrintTimeTo(True)
browser = scraperhelper.initBrowser()

# output lists
data = []
errors = []

# main script GO!
try:
    browser.get('https://www.camara.cl/camara/diputados.aspx')
    scraperhelper.pt('Get Current Reps Site')
    
    content = browser.find_elements_by_css_selector('li.alturaDiputado h4 a')
    for el in content:
        data.append({
                "prmid":scraperhelper.getQueryParametersFromUrl(el.get_attribute('href')),
                "nombre":str(el.text.replace('SR. ','').replace('SRA. ','')),
                "periodo":"2014-2018"
        })
    
except TimeoutException as ex:
    scraperhelper.pt('PAGE TimeoutException ERROR')
except NoSuchElementException as ex:
    scraperhelper.pt('PAGE NoSuchElementException ERROR')
except StaleElementReferenceException as ex:
    scraperhelper.pt('PAGE StaleElementReferenceException ERROR')
except WebDriverException as ex:
    scraperhelper.pt('PAGE WebDriverException ERROR')

scraperhelper.closeSeleniumBrowser(browser)
scraperhelper.saveToFile('diputados.simple.1418', data, errors)