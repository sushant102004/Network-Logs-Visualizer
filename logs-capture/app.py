from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from fastapi import FastAPI
import time
import json

app = FastAPI()

def saveLogs(driver):
    logs = driver.get_log("performance")

    with open('network_log.json', 'a', encoding='utf-8') as f:
        for log in logs:
            network_log = json.loads(log['message'])['message']

            if('Network.response' in network_log['method']):

                if network_log['method'] == 'Network.responseReceived':
                    mimeType = network_log['params']['response']['mimeType']
                    log_name = network_log['params']['response']['url']
                    status_code = network_log['params']['response']['status']

                    data = {'log_name': log_name, 'status_code': status_code, 'type': mimeType}
                    f.write(json.dumps(data) + ',')

        f.write('{}]')

        print('Logs Saved')



def captureNetworkLogs(site: str):
    # Clear network_log.json
    open('network_log.json', 'w').close()

    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')

    # options.add_argument('headless')

    options.add_argument('--ignore-certificate-error')

    driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)

    driver.get('https://' + site)

    time.sleep(10)

    # Saving logs for intial page load
    saveLogs(driver)

    menuLink = driver.find_element(by = By.LINK_TEXT, value = 'Sign up for Free')
    menuLink.click()
    time.sleep(10)
    # Logs for Enterprise page
    saveLogs(driver)

    driver.quit()

    jsonOutput = open('network_log.json')
    result = json.load(jsonOutput)

    return result


@app.get('/capture-logs/{site}')
async def root(site: str):
    result = captureNetworkLogs(site)
    return { 'data' : result }