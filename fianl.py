import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import matplotlib.dates as mdates
import matplotlib.ticker as mticker


import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np




LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)


style.use("ggplot")

f = plt.figure()


exchange = "Bitstamp"
DatCounter = 9000
programName = "btce"
resampleSize = "15Min"
DataPace = "tick"


paneCount = 1

chartLoad = True

darkColor = "#4c072c"
lightColor = "#ffbf00"


def changeExchange(toWhat,pn):
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000
    

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
    


def animate(i):
    global refreshRate
    global DatCounter

    try:
                    if exchange == "BTC-e":
                        a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)

                        dataLink = 'https://btc-e.com/api/3/trades/btc_usd?limit=2000'
                        data = urllib.request.urlopen(dataLink)
                        data = data.readall().decode("utf-8")
                        data = json.loads(data)

                        
                        data = data["btc_usd"]
                        data = pd.DataFrame(data)

                        data["datestamp"] = np.array(data['timestamp']).astype("datetime64[s]")
                        allDates = data["datestamp"].tolist()

                        buys = data[(data['type']=="bid")]
                        buyDates = (buys["datestamp"]).tolist()
                        

                        sells = data[(data['type']=="ask")]
                        sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"]

                        a.clear()

                        a.plot_date(buyDates, buys["price"], lightColor, label="buys")
                        a.plot_date(sellDates, sells["price"], darkColor, label="sells")

                        a2.fill_between(allDates, 0, volume, facecolor = darkColor)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        plt.setp(a.get_xticklabels(), visible = False)
                        
                        

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
                                 ncol=2, borderaxespad=0)

                        title = "BTC-e BTCUSD Prices\nLast Price: "+str(data["price"][1999])
                        a.set_title(title)

                    if exchange == "Bitstamp":
                        a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)

                        dataLink = 'https://www.bitstamp.net/api/transactions/'
                        data = urllib.request.urlopen(dataLink)
                        data = data.readall().decode("utf-8")
                        data = json.loads(data)

                        data = pd.DataFrame(data)

                        data["datestamp"] = np.array(data['date'].apply(int)).astype("datetime64[s]")
                        dateStamps = data["datestamp"].tolist()

                        volume = data["amount"].apply(float).tolist()

                        a.clear()

                        a.plot_date(dateStamps, data["price"], lightColor, label="buys")

                        a2.fill_between(dateStamps, 0, volume, facecolor = darkColor)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        plt.setp(a.get_xticklabels(), visible = False)
                        

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
                                 ncol=2, borderaxespad=0)

                        title = "Bitstamp BTCUSD Prices\nLast Price: "+str(data["price"][0])
                        a.set_title(title)


                    if exchange == "Bitfinex":
                        a = plt.subplot2grid((6,4), (0,0), rowspan = 5, colspan = 4)
                        a2 = plt.subplot2grid((6,4), (5,0), rowspan = 1, colspan = 4, sharex = a)

                        dataLink = 'https://api.bitfinex.com/v1/trades/btcusd?limit=2000'
                        data = urllib.request.urlopen(dataLink)
                        data = data.readall().decode("utf-8")
                        data = json.loads(data)

    
                        data = pd.DataFrame(data)

                        data["datestamp"] = np.array(data['timestamp']).astype("datetime64[s]")
                        allDates = data["datestamp"].tolist()

                        buys = data[(data['type']=="buy")]
                        buyDates = (buys["datestamp"]).tolist()
                        

                        sells = data[(data['type']=="sell")]
                        sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"].apply(float).tolist()

                        a.clear()

                        a.plot_date(buyDates, buys["price"], lightColor, label="buys")
                        a.plot_date(sellDates, sells["price"], darkColor, label="sells")

                        a2.fill_between(allDates, 0, volume, facecolor = darkColor)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
                        plt.setp(a.get_xticklabels(), visible = False)
                        

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
                                 ncol=2, borderaxespad=0)

                        title = "Bitfinex BTCUSD Prices\nLast Price: "+str(data["price"][0])
                        a.set_title(title)

                    if exchange == "Huobi":
                        a = plt.subplot2grid((6,4), (0,0), rowspan = 6, colspan = 4)
                        data = urllib.request.urlopen('http://seaofbtc.com/api/basic/price?key=1&tf=1d&exchange='+programName).read()
                        data = data.decode()

                        data = json.loads(data)

                        dateStamp = np.array(data[0]).astype("datetime64[s]")
                        dateStamp = dateStamp.tolist()

                        df = pd.DataFrame({'Datetime':dateStamp})

                        df['Price'] = data[1]
                        df['Volume'] = data[2]
                        df['Symbol'] = "BTCUSD"

                        df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))

                        df = df.set_index("Datetime")

                        lastPrice = df["Price"][-1]

                        a.plot_date(df['MPLDate'][-4500:], df['Price'][-4500:], lightColor, label="price")

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))

                        title = "Huobi BTCUSD Prices\nLast Price: "+str(lastPrice)
                        a.set_title(title)

                        

                        


                    


    except Exception as e:
                    print("Failed because of:",e)

    
    
    


    
            

class Bitcoin(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        
        tk.Tk.wm_title(self, "Bitcoin Data")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="BTC-e",
                                   command=lambda: changeExchange("BTC-e","btce"))
        exchangeChoice.add_command(label="Bitfinex",
                                   command=lambda: changeExchange("Bitfinex","bitfinex"))
        exchangeChoice.add_command(label="Bitstamp",
                                   command=lambda: changeExchange("Bitstamp","bitstamp"))
        exchangeChoice.add_command(label="Huobi",
                                   command=lambda: changeExchange("Huobi","huobi"))

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, BTCe_Page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("""ALPHA Bitcoin trading application
        use at your own risk. There is no promise
        of warranty."""), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=quit)
        button2.pack()



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()




class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = Bitcoin()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000)
app.mainloop()
        
