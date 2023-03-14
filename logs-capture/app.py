from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json


if __name__ == "__main__":

    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    options = webdriver.ChromeOptions()

    options.add_argument('headless')

    options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)

    driver.get("https://www.lambdatest.com/")

    time.sleep(10)

    logs = driver.get_log("performance")

    with open("network_log.json", "w", encoding="utf-8") as f:
        f.write("[")

        for log in logs:
            network_log = json.loads(log["message"])["message"]

            if("Network.response" in network_log["method"]):

                if network_log['method'] == "Network.responseReceived":
                    mimeType = network_log["params"]["response"]["mimeType"]
                    log_name = network_log["params"]["response"]["url"]
                    status_code = network_log["params"]["response"]["status"]

                    data = {"log_name": log_name, "status_code": status_code, "type": mimeType}
                    f.write(json.dumps(data) + ",")

        f.write("{}]")

    print("Quitting Selenium WebDriver")
    driver.quit()