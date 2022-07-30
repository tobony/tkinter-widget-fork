import tkinter
import customtkinter as ck
from PIL import Image, ImageTk 

import os
from os import path


from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


PATH = os.path.dirname(os.path.realpath(__file__))

ck.set_appearance_mode("dark")              
ck.set_default_color_theme("dark-blue")    

class App(ck.CTk):
    
    APP_NAME = "Crypto Data"
    
    WIDTH = 250
    HEIGHT = 100
    
    PRIMARY_BG = '#2d323b'               
    SECONDARY_BG = '#1f242b' 
    
    TEXT_1 = "#26b9c4"
    TEXT_2 = "#bbbbbb"
    TEXT_3 = "#9aa5b5"
    
    def __init__(self, *args, fg_color="default_theme", **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        
        self.title(App.APP_NAME)
        
        self.screenHeight = self.winfo_screenheight()
        self.screenWidth = self.winfo_screenwidth()
               
        self.posX = self.screenWidth - App.WIDTH - 10

        self.overrideredirect(True)

        self.geometry(f'{App.WIDTH}x{App.HEIGHT}+{int(self.screenWidth-App.WIDTH - 20)}+{int(50)}')
        
        self.config(background=App.PRIMARY_BG)
        
        self.frame = ck.CTkFrame(self, fg_color=App.PRIMARY_BG, corner_radius=0)
        self.frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

        self.innerFrame = ck.CTkFrame(self.frame, fg_color=App.PRIMARY_BG, corner_radius=0)
        self.innerFrame.grid(row=0, column=0, pady=0, padx=0, sticky='nswe')
        self.innerFrame.grid_columnconfigure(0, weight=0)
        self.innerFrame.grid_columnconfigure(1, weight=1)
        self.innerFrame.rowconfigure((0, 1, 2, 3), weight=0)
        
        cryptoImage = ImageTk.PhotoImage(Image.open(PATH +  "/ethereum.png").resize((32, 32)))
        self.cryptoBtn = ck.CTkButton(self.innerFrame, text=None, image=cryptoImage, 
                                         width=20, height=20, corner_radius=50, fg_color=App.SECONDARY_BG, bg_color=App.PRIMARY_BG,
                                         hover_color=None, command=None).grid(row=0, column=0, rowspan=4, padx=10, pady=10, ipady=10, ipadx=10, sticky='we')

        self.currentToken = cg.get_price(ids='ethereum', vs_currencies='usd')
        self.currentPrice = round((self.currentToken['ethereum']['usd']), 2)
        
        self.labelPrice = tkinter.Label(self.innerFrame, text=f'${self.currentPrice}', font=("Times New Roman", 26), fg=App.TEXT_2, bg=App.PRIMARY_BG)
        self.labelPrice.grid(row=2, column=1, sticky='wn')
        
        self.labelName = tkinter.Label(self.innerFrame, text=f'Ethereum (ETH)', font=("Times New Roman", 10), fg=App.TEXT_3, bg=App.PRIMARY_BG, justify="left")
        self.labelName.grid(row=1, column=1, sticky='ws')
        
        self.updatePrice()

        self.botFrame = ck.CTkFrame(self, fg_color=App.SECONDARY_BG, height=22, corner_radius=0)
        self.botFrame.pack(side=tkinter.BOTTOM, fill=tkinter.X, expand=False, padx=0, pady=0)
        self.botFrame.grid_columnconfigure((0), minsize=20)
        self.botFrame.grid_columnconfigure((4), minsize=70)
        self.botFrame.grid_rowconfigure(1, minsize=2)

        self.serverLabel = tkinter.Label(self.botFrame, font=("Times New Roman", 10),text='Server Status:', bg=App.SECONDARY_BG, fg=App.TEXT_2)
        self.serverLabel.grid(row=0, column=5, pady=0, padx=0, sticky='nse')

        self.serverStatus = tkinter.Label(self.botFrame, font=("Times New Roman", 10), bg=App.SECONDARY_BG, fg=None)
        self.serverStatus.grid(row=0, column=6, pady=0, padx=0, sticky='nsw')
        
        closeImage = ImageTk.PhotoImage(Image.open(PATH +  "/close.png").resize((10, 10)))
        self.closeBtn = ck.CTkButton(self.botFrame, text=None, image=closeImage, 
                                         width=0, height=0, corner_radius=0, fg_color=App.SECONDARY_BG, bg_color=App.SECONDARY_BG,
                                         hover_color=None, command=self.close).grid(row=0, column=2, sticky='swe')
        
        
        hideImage = ImageTk.PhotoImage(Image.open(PATH +  "/hide.png").resize((10, 10)))
        self.hideBtn = ck.CTkButton(self.botFrame, text=None, image=hideImage, 
                                         width=0, height=0, corner_radius=0, fg_color=App.SECONDARY_BG, bg_color=App.SECONDARY_BG,
                                         hover_color=None, command=self.hideWindow).grid(row=0, column=3, sticky='swe')
        
        
        unhideImage = ImageTk.PhotoImage(Image.open(PATH +  "/unhide.png").resize((10, 10)))
        self.unhideBtn = ck.CTkButton(self.botFrame, text=None, image=unhideImage, 
                                         width=0, height=0, corner_radius=0, fg_color=App.SECONDARY_BG, bg_color=App.SECONDARY_BG,
                                         hover_color=None, command=self.unhideWindow).grid(row=0, column=1, sticky='swe')

        self.server()
        
    def server(self):
        try:
            self.string = list(cg.ping().values())
            if (self.string[0] == "(V3) To the Moon!"):
                self.serverStatus.config(
                    text=f'Operational', fg='#8cc46f')
            else:
                self.serverStatus.config(
                    text=f'{self.string[0]}', fg='#f06371')
            self.serverStatus.after(10000, self.server)
        except:
            self.serverStatus.config(
                text=f'Failed to Connect', fg='#f06371')
            self.serverStatus.after(10000, self.server)
            
    def updatePrice(self):
        self.currentToken = cg.get_price(ids='ethereum', vs_currencies='usd')
        
        self.currentPrice = round((self.currentToken['ethereum']['usd']), 2)
        
        self.labelPrice.config(text=f'$ {self.currentPrice}')
        
        self.labelPrice.after(60000, self.updatePrice)
        
    def hideWindow(self):    
        self.geometry(f'{App.WIDTH}x{App.HEIGHT}+{int(self.posX + (App.WIDTH*.75))}+{int(50)}')
            
    def unhideWindow(self):
        self.geometry(f'{App.WIDTH}x{App.HEIGHT}+{int(self.posX)}+{int(50)}')

    def close(self):
        self.destroy()

    def start(self):
        self.mainloop()
          
if __name__ == "__main__":
    app = App()
    app.start() # Calls the start method, i.e. app mainloop