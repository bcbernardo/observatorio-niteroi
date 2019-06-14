# -*- coding: utf-8 -*-

import datetime
import lxml
import selenium
import time


BASE_URL = "http://portais.niteroi.rj.gov.br"
CURR_YEAR = int(d.datetime.now().year)


class MainPage():
    """ Acesso à página principal de despesas do Portal da Transparência
    
    Atributos:
        exercicio (str, opcional): Ano do exercício fiscal. Por padrão,
            é o ano corrente.
        periodo (tuple[str, str], opcional): Periodo do ano para consulta, em
            formato 'DDMM'. Por padrão, inclui todo o período transcorrido.
    """
    
    def __init__(self, exercicio = CURR_YEAR, periodo = ("","")):
        self.year = exercicio
        self.period = periodo
        
        # access main page
        self.driver = selenium.webdriver.Chrome()
        self.driver.get(BASE_URL + "/portal-da-transparencia/despesas")
        self.page = lxml.html.fromstring(self.driver.page_source)
        
        # optionally change year or set a time interval for the query
        if year != CURR_YEAR:
            self.set_year()
        if period != ("", ""):
            self.set_period()
        
    def set_year(self):
        """ Seleciona o ano do exercício fiscal. """
        # make sure the given year is valid and available in the portal
        years_available = page.xpath(
            "//select[@id='exercicioConsulta']/option/text()")
        if self.year not in years_available:
            raise ValueError(
                "O ano deve estar entre {years_available[0]} " + \
                "e {years_available[1]}.")
        # select the given year
        year_field = self.driver.find_element_by_xpath(
            "//select[@id='exercicioConsulta']/" + \
            "option[@text()={self.year}]")
        year_field.click()
        return
    
    def set_period(self):
        """ Seleciona o período de interesse. """
        # validate the given period
        try:
            self.period = str(ddmm for ddmm in self.period)
            start_date, end_date = self.period[0], self.period[1]
            assert int(start_date[0:1]) <= 31
                and int(start_date[2:3]) <= 12
            assert int(end_date[0:1]) <= 31
                and int(end_date[2:3]) <= 12
            assert end_date[2:3] + end_date[0:1] \
                   > start_date[2:3] + start_date[0:1]
        except (TypeError, ValueError, IndexError, AssertionError):
            raise ValueError(
                "As datas de início e fim devem ser informadas como uma " + \
                "dupla no formato ('DDMM', 'DDMM'), respectivamente.")
        # set time filter
        start_date_field = self.driver.find_element_by_id("periodoInicio")
        start_date_field.send_keys(str(self.period[0]))
        end_date_field = self.driver.find_element_by_id("periodoFim")
        end_date_field.send_keys(str(self.period[0]))
        return
        
