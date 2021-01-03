from win32com.client import Dispatch
import zipfile
import requests
import os
import download_driver


def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


def chrome_version():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
    res = requests.get(
        "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_"
        + version.split(".")[0]
    )
    return res.content.decode("utf-8")


def unzip_driver(zip_path, location):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(location)
    os.remove(zip_path)


def driver_handler():
    try:
        os.remove(r"./driver/chromedriver.exe")
    except FileNotFoundError as e:
        pass
    version = chrome_version()
    print(version)
    if not os.path.isdir(r"./driver/"):
        os.mkdir(r"./driver/")
    filename = r"./driver/chromedriver.zip"
    url = (
        f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
    )
    print("Downloading....")
    download_driver.start(url, filename)
    unzip_driver(r"./driver/chromedriver.zip", r"./driver/")
    return r"./driver/chromedriver.exe"
