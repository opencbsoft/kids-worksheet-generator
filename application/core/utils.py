import os
import json
import base64
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from selenium import webdriver
import urllib.parse
from datauri import DataURI

import pdfkit
from django.utils.text import slugify


def send_devtools(driver, cmd, params=None):
    if params is None:
        params = {}
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    if response.get('status'):
        raise Exception(response.get('value'))
    return response.get('value')


def selenium_process_html(html_content, output):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')

    capabilities = {
        'browserName': 'chrome',
        'javascriptEnabled': True,
    }
    capabilities.update(chrome_options.to_capabilities())
    driver = webdriver.Remote(settings.SELENIUM_URL, desired_capabilities=capabilities)
    calculated_print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
    }
    made = DataURI.make('text/html', charset='utf-8', base64=True, data=html_content)
    driver.get(made)
    result = send_devtools(driver, "Page.printToPDF", calculated_print_options)
    with open(output, 'wb') as file:
        file.write(base64.b64decode(result['data']))
    driver.quit()
    return True


class Generator(object):
    name = None
    directions = None
    years = [4, 5]
    template = None
    icons_folder = None
    data = None  # Will be populated by generate_data
    content_height = 1450
    selected_icons = None

    def __init__(self, count=10, extra=None):
        if not self.name or not self.directions or not self.template:
            raise Exception('You must have a name, a directions and a template specified')
        if self.selected_icons:
            self.icons = self.selected_icons
        else:
            self.icons = []
            if self.icons_folder:
                if isinstance(self.icons_folder, list):
                    for folder in self.icons_folder:
                        for icon in os.listdir(os.path.join(settings.BASE_DIR, 'core', 'static', folder)):
                            self.icons.append(folder+'/'+str(icon))
                else:
                    for icon in os.listdir(os.path.join(settings.BASE_DIR, 'core', 'static', self.icons_folder)):
                        self.icons.append(self.icons_folder + '/' + str(icon))
        self.count = count
        self.extra = extra
        self.generate_data()

    def generate_data(self):
        """
            This function is used to populate self.data with the possible values
        """
        pass

    def get_context_data(self, iteration):
        """
            This function populates the bare minimum of a context data
        """
        path = 'https://kids.cbsoft.ro/static/'
        context = {
            'path': path,
            'directions': _(self.directions)
        }
        if self.data:
            context['items'] = self.data
        else:
            context['items'] = self.generate_data()
        if self.icons:
            context['icons'] = self.icons
        context['content_height'] = self.content_height
        return context

    def render(self):
        generated = []
        for i in range(0, self.count):
            content = render_to_string(self.template, self.get_context_data(i))
            folder = os.path.join(settings.OUTPUT, slugify(self.name))
            os.makedirs(folder, exist_ok=True)
            if settings.SELENIUM_URL:
                selenium_process_html(content, os.path.join(folder, 'generated{}.pdf'.format(i)))
            else:
                pdfkit.from_string(content, os.path.join(folder, 'generated{}.pdf'.format(i)), options=settings.PDF_OPTIONS)
            generated.append(os.path.join(folder, 'generated{}.pdf'.format(i)))
        return generated
