from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--mute-audio")  # 将浏览器静音
# chrome_options.add_experimental_option("detach", True)  # 当程序结束时，浏览器不会关闭

# -----如果咋们的linux系统没有安装桌面，下面两句一定要有哦，必须开启无界面浏览器-------
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# ------------------------------------------------------------------------
browser = webdriver.Chrome(options=chrome_options,executable_path='./chromedriver')

browser.get('https://blog.csdn.net/FujLiny')

print('不离鞘' in browser.page_source)
browser.quit()  # 关闭浏览器
