import itertools
import multiprocessing as mp
import threading as thr
import time
import webbrowser

# import pyaudio
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font

import requests as rt
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import getDriver

driver = ""
count = 3
clist = ["", "", "", ""]
thlist = []
llist = []
labellist = []
driverlist = []
bfont = ""
new = ""


def senbse(flabel):
    print("i am senbse")
    while True:
        bse = rt.get("https://api.bseindia.com/BseIndiaAPI/api/GetLinknew/w?code=16")
        bon = bse.json()
        bdata = "SENSEX" + "\n " + bon["CurrValue"] + "\n  " + bon["ChgPer"]
        flabel.configure(text=bdata)
        time.sleep(3)


def nsenif(flabel):
    while True:
        response = rt.get("https://www1.nseindia.com/homepage/Indices1.json")
        njon = response.json()
        non = njon["data"][1]
        data = (
            non["name"] + "\n" + non["lastPrice"] + "\n " + non["pChange"] + "%"
        )  # +"\n"+"Closed:"+(njon["status"]).split(".")[1].strip()+"\n"+"Next:"+njon["haltedStatus"].split(":")[1]
        flabel.configure(text=data)
        time.sleep(3)


def bitcoin(flabel):
    ru = 0

    def ruprice():
        nonlocal ru
        response = rt.get("https://www1.nseindia.com/common/json/rbi_rate.json")
        rup = response.json()
        ru = rup["data"][0]["RBI_RT"]

    th = thr.Thread(target=ruprice)
    th.start()
    while True:
        response = rt.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
        bion = response.json()
        th.join()
        data = (
            "BITCOIN"
            + "\n"
            + "%.2f" % (float(bion["lastPrice"]) * float(ru))
            + "\n"
            + bion["priceChangePercent"]
        )
        flabel.configure(text=data)
        time.sleep(3)


def ethereum(flabel):
    ru = 0

    def ruprice():
        nonlocal ru
        response = rt.get("https://www1.nseindia.com/common/json/rbi_rate.json")
        rup = response.json()
        ru = rup["data"][0]["RBI_RT"]

    th = thr.Thread(target=ruprice)
    th.start()
    while True:
        response = rt.get("https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT")
        bion = response.json()
        th.join()
        data = (
            "ETHEREUM"
            + "\n"
            + "%.2f" % (float(bion["lastPrice"]) * float(ru))
            + "\n"
            + bion["priceChangePercent"]
        )
        flabel.configure(text=data)
        time.sleep(3)


def getstock(url, flabel, demo):
    demo.get(url)
    while True:
        data = ""
        innerHTML = demo.execute_script("return document.body.innerHTML")
        page_soup = bs(innerHTML, "html.parser")
        ans = [
            0 if i.text == "" else i.text for i in page_soup.select("div.not_tradedbx")
        ]
        dfe = [i.text for i in page_soup.select("div.pcnsb.div_live_price_wrap")]
        for ind, df, an in zip(["BSE", "NSE"], ans, dfe):
            if df:
                data = data + "\n" + (ind + "\n" + str(df))
            else:
                data = data + "\n" + (ind + "\n" + " ".join(an.strip().split("\n")))
            data = data + ("\n-----------")
        flabel.configure(text=data)
        time.sleep(5)


def checkDriver():
    global driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    try:
        driver = webdriver.Chrome(r"./driver/chromedriver.exe", options=options)
    except Exception as e:
        driver_loc = getDriver.driver_handler()
        driver = webdriver.Chrome(
            chrome_options=options, executable_path=r"./driver/chromedriver.exe"
        )
    driver.close()


def startsel():
    global driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(r"./driver/chromedriver.exe", options=options)
    return driver


def gui():
    checkDriver()
    global master, bfont
    master = Tk()
    new_font = Font(family="Times New Roman", size=15)
    newl_font = Font(family="Times New Roman", size=12)
    bfont = Font(family="Times New Roman", size=12)
    chfont = Font(family="Times New Roman", size=12)

    top = Frame(master, relief=RAISED, borderwidth=1)
    top.pack(side=TOP, fill=BOTH)
    mid = Frame(master, relief=RAISED, borderwidth=1)
    mid.pack(fill=BOTH)
    mid1 = Frame(master, relief=RAISED, borderwidth=1)
    mid1.pack(fill=BOTH)
    bot = Frame(master, relief=RAISED, borderwidth=1)
    bot.pack(side=BOTTOM, fill=BOTH)

    def add():
        global count
        txt = e1.get()
        if valider(txt):
            clist.append("")
            print(len(clist))
            count += 1
            clist[count] = StringVar()
            Checkbutton(
                mid1,
                text=txt.upper(),
                offvalue="",
                onvalue=txt,
                variable=clist[count],
                padx=5,
                pady=0,
                font=chfont,
            ).pack()
        else:

            def clear():
                mbox.destroy()

            def callback(event):
                webbrowser.open_new(
                    ("https://www.moneycontrol.com/india/stockpricequote/")
                )  # event.widget.cget

            mbox = Toplevel(master=master)
            mbox.wm_attributes("-topmost", 1)  # Toplevel(master=master)

            mbox.config(width=50, height=10)
            mbox.title("Error")
            Label(mbox, text="Stock is not listed.", font=chfont).grid(
                padx=10, row=0, column=0
            )
            Label(mbox, text="For more help visit", font=chfont).grid(
                padx=10, row=1, column=1
            )
            he = Label(mbox, text="Click Here", fg="blue", font=chfont)
            he.grid(padx=10, row=2, column=1)
            he.bind("<Button-1>", callback)
            Button(
                mbox,
                text="Ok",
                padx=5,
                command=clear,
                fg="white",
                bg="black",
                font=bfont,
            ).grid(row=3, column=1, pady=8, padx=8)

            # messagebox.showerror("Error","Please Enter Listed Stocks\nFor more help visit https://www.moneycontrol.com/india/stockpricequote/")

    Label(top, text="Choose From Option:", font=new_font, padx=5, pady=10).pack()
    Label(mid, text="Add More", padx=5, font=newl_font).pack(side=LEFT)
    e1 = Entry(mid)
    e1.pack(side=LEFT)
    Button(
        mid, text="Add", padx=5, command=add, fg="white", bg="black", font=bfont
    ).pack(side=LEFT, padx=10)

    clist[0] = StringVar()
    Checkbutton(
        mid1,
        text="SENSEX",
        offvalue="",
        onvalue="Sensex",
        variable=clist[0],
        padx=5,
        pady=0,
        font=chfont,
    ).pack()
    clist[1] = StringVar()
    Checkbutton(
        mid1,
        text="NIFTY",
        offvalue="",
        onvalue="Nifty",
        variable=clist[1],
        padx=5,
        pady=0,
        font=chfont,
    ).pack()
    clist[2] = StringVar()
    Checkbutton(
        mid1,
        text="BITCOIN",
        offvalue="",
        onvalue="Bitcoin",
        variable=clist[2],
        padx=5,
        pady=0,
        font=chfont,
    ).pack()
    clist[3] = StringVar()
    Checkbutton(
        mid1,
        text="ETHEREUM",
        offvalue="",
        onvalue="Ethereum",
        variable=clist[3],
        padx=5,
        pady=0,
        font=chfont,
    ).pack()
    # var5 = IntVar()
    # Checkbutton(master, text="SENSEX", variable=var5,font=11,fg="white",bg="black",padx=5,pady=10).(row=1, sticky=W)
    # var6 = IntVar()
    # Checkbutton(master, text="SENSEX", variable=var6,font=11,fg="white",bg="black",padx=5,pady=10).(row=1, sticky=W)

    Button(
        bot,
        text="Quit",
        padx=5,
        command=master.quit,
        fg="white",
        bg="black",
        font=bfont,
    ).pack(side=RIGHT, pady=8, padx=8)
    Button(
        bot, text="Submit", padx=5, command=labcre, fg="white", bg="black", font=bfont
    ).pack(side=RIGHT, padx=8, pady=8)

    master.mainloop()


def labcre():
    global clist, labellist, new
    cdlist = clist.copy()
    for ii in clist:
        ij = ii.get()
        if ij == "":
            cdlist.remove(ii)
            print(ij)
    clist = cdlist.copy()
    labellist = cdlist.copy()

    linkGen(clist)
    new = Tk()
    new.wm_attributes("-topmost", 1)  # Toplevel(master=master)
    master.destroy()

    # except:
    # 	pass
    k = 0
    hi = 5
    wi = 10
    j = 0
    colspan = 1
    xpad = 5
    ypad = 5
    for index, i in enumerate(clist):
        j = index % 2
        k = int((index) / 2)
        try:
            if len(clist) % 2 == 1 and index == len(clist) - 1:
                wi = wi * 2
                colspan = 2
                xpad = xpad * 2.5
        except:
            pass

        labellist[index] = Label(
            new, text=i.get(), bg="black", fg="white", height=hi, width=wi, font=bfont
        )  # , height=hi, width=wi
        (labellist[index]).grid(
            columnspan=colspan, padx=xpad, pady=ypad, row=k, column=j, sticky=W
        )
    Button(
        new, text="Quit", padx=5, command=stopsel, fg="white", bg="black", font=bfont
    ).grid(row=int((len(clist) + (len(clist) % 2)) / 2 + 1), column=j, sticky=E)
    th1 = thr.Thread(target=threadstart)
    th1.start()

    new.mainloop()


def valider(demo):
    import pandas as pd

    data = pd.read_csv("links.csv", names=["company", "links"])
    return (data["company"] == demo).any()


def linkGen(demo):
    global llist
    import pandas as pd

    data = pd.read_csv("links.csv", names=["company", "links"])
    for val in demo:
        temp = data[(data["company"]) == (val.get())]
        llist.append(temp.values)


def threadgen():
    global thlist
    thlist = clist.copy()
    print("i am here")
    # print(llist[0][0])
    count = 0
    for index, demo in enumerate(llist):
        name = demo[0][0]
        link = demo[0][1]
        # print(index,name,link)
        if name == "Sensex":
            thlist[index] = thr.Thread(target=senbse, args=(labellist[index],))
            # thlist[index].start()
        elif name == "Nifty":
            thlist[index] = thr.Thread(target=nsenif, args=(labellist[index],))
            # thlist[index].start()

        elif name == "Bitcoin":
            thlist[index] = thr.Thread(target=bitcoin, args=(labellist[index],))
            # thlist[index].start()

        elif name == "Ethereum":
            thlist[index] = thr.Thread(target=ethereum, args=(labellist[index],))
            # thlist[index].start()

        else:

            thlist[index] = thr.Thread(
                target=getstock, args=(link, labellist[index], driverlist[count])
            )
            count = count + 1


def threadstart():
    global thlist
    drivergen()
    threadgen()
    print(thlist)
    for i in thlist:
        i.start()


def stopsel():
    for i in driverlist:
        i.quit()
    # new.quit()


def drivergen():
    for i in clist:
        if i not in ["Sensex", "Nifty", "Bitcoin", "Ethereum", ""]:
            driverlist.append("")

    for i in range(len(driverlist)):
        driverlist[i] = startsel()


def final():
    checkDriver()
    th1 = mp.Process(target=labcre)
    th2 = mp.Process(target=threadstart)
    th1.start()
    th2.start()


if __name__ == "__main__":
    gui()
