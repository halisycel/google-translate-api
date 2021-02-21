from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import linecache
import time


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def listToString(s):
    str1 = " "
    return (str1.join(s))


chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver_path = "chromedriver.exe"
browser = webdriver.Chrome(executable_path=driver_path, options=chrome_options)


def main(source_text, config):
    browser.get(
        f"https://translate.google.com/?hl=en&sl={config['sl']}&tl={config['tl']}&text={source_text}&op=translate")
    for i in range(5):
        try:
            element = browser.find_element_by_css_selector(
                "#yDmH0d > c-wiz > div > div.WFnNle > c-wiz > div.OlSOob > c-wiz > div.ccvoYb > div.AxqVh > div.OPPzxe > c-wiz.P6w8m.BDJ8fb.BLojaf > div.dePhmb > div > div.J0lOec > span.VIiyi")

            result = ""
            for t in element.text:
                if t == "\n":
                    pass
                elif t == "\'":
                    result += "’"
                else:
                    result += t

            print({"main_result": result})

            browser.quit()
            exit()
        except Exception as ex:
            if type(ex).__name__ == "NoSuchElementException":
                time.sleep(1)
            else:
                PrintException()


if __name__ == "__main__":
    args = sys.argv
    args.pop(0)

    configurations = {
        "sl": "en",
        "tl": "tr"
    }
    new_args = []

    for i in args:
        if "--sl" in i:
            configurations["sl"] = i[5:]

        elif "--tl" in i:
            configurations["tl"] = i[5:]

        else:
            new_args.append(i)

    text = listToString(new_args)
    main(text, configurations)
