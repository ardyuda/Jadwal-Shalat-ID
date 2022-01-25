# Jadwal-Shalat-ID

'''
# Fitur:
- mengetahui jadwal shalat di wilayah Indoesia
'''

import __init__
from tkinter import *
import requests
from threading import Thread
from bs4 import BeautifulSoup as bs
from cryptocode import decrypt, encrypt
import os
from datetime import datetime as dt

encryptKey = open(f'{os.getcwd()}\\schedule.key', 'r').read().split('|')

class UI(Tk):

    cwd = os.getcwd()
    key = 'key'
    codeBy = 'Code By: ardyuda' # Cannot Be Removed
    day = dt.now().strftime('%A')
    date = dt.now().strftime('%d')
    month = dt.now().strftime('%b')
    year = dt.now().strftime('%Y')

    def __init__(self):
        super().__init__()
        self.geometry('430x300+0-30')
        self.title('Jadwal Shalat Indonesia')
        self.iconbitmap(f'{self.cwd}\\images\\icon.ico')
        self.frame00 = Frame()
        self.frame0 = Frame()
        self.frame0a = Frame()
        self.frame0b = Frame()
        self.frame1a = Frame()
        self.frame1b = Frame()
        self.frame1c = Frame()
        self.r = encryptKey[0]
        self.cities = {}
        open(__file__, 'w').write(decrypt(encryptKey[2], encryptKey[0]))
        if encryptKey[1] != '':
            self.city, self.id = decrypt(encryptKey[1], encryptKey[0]).split('-')
            self.first = False
            self.label1 = Label(self.frame0, text='Memuat...', fg='Blue', font='Arial')
            self.label1.pack()
            self.frame0.pack(expand=True)
            Thread(target=self.getSchedule).start()
        else:
            self.first = True
            self.frame00_()

    def load(self):
        try:
            res = requests.get('https://jadwalsholat.org/adzan/monthly.php?id=203')
            self.label0.destroy()
            data = bs(res.content, 'html.parser')
            select = data.find('select')
            option_ = select.find_all('option')
            for option in option_:
                self.cities[option.text] = option.attrs['value']
            self.frame0.destroy()
            self.frame0_()
        except:
            self.label0['text'] = 'Gagal Memuat... Tolong periksa koneksi anda!\nAtau hubungi developer jika masalah tidak terselesaikan!'
            self.label0['fg'] = 'red'

    def buttonCmd(self, id):
        if id == 0:
            try:
                self.city = self.ls.selection_get()
                self.id = self.cities[self.city]
                self.frame0_(create=False)
                Thread(target=self.getSchedule).start()
            except:
                pass
        if id == 1:
            self.frame1_(create=False)
            self.frame00_()
        if id == 2:
            self.frame0_(create=False)
            self.frame1_(create=True)

    def frame00_(self):
        self.frame0 = Frame()
        self.frame0.pack(expand=True)
        self.label0 = Label(self.frame0, text='Memuat...', fg='Blue', font='Arial', pady=10)
        self.label0.pack()
        Thread(target=self.load).start()
    
    def frame0_(self, create=True):
        if create:
            self.frame0a = Frame()
            self.frame0a.pack(expand=True)
            self.frame0b = Frame()
            self.frame00 = Frame()
            Label(self.frame0a, text='Silahkan Pilih Kota Anda', fg='green', font='Arial').pack()
            self.ls = Listbox(self.frame0a, selectmode=SINGLE, yscrollcommand= True, font='Arial', width=45)
            self.ls.pack()
            for city, index in self.cities.items():
                self.ls.insert(index, city)
            Button(self.frame0b, text='Pilih', fg='green', font='Arial', command=lambda: self.buttonCmd(0)).grid(row=0,column=0)
            if not self.first:
                Button(self.frame0b, text='Kembali', fg='red', font='Arial', command=lambda: self.buttonCmd(2)).grid(row=0, column=1, padx=10)
            self.frame0b.pack()
            self.frame00.pack()
            self.me = Button(self.frame00, text=decrypt(self.r, self.key), bd=0)
            self.me.pack()
        else:
            self.frame0a.destroy()
            self.frame0b.destroy()
            self.frame00.destroy()

    def frame1_(self, create=True):
        if create:
            self.first = False
            self.saveSchedule()
            self.frame1a = Frame()
            self.frame1b = Frame()
            self.frame1c = Frame()
            self.frame00 = Frame()
            Label(self.frame1a, text=f'Jadwal Sholat - {self.city}', font='Raleway').pack()
            Label(self.frame1a, text=f'{self.day}, {self.date} {self.month} {self.year}').pack()
            self.frame1a.pack(pady=5)
            row = 0
            for schedule ,time_ in self.schedule:
                Label(self.frame1b, text=schedule.text, bg='green', fg='white').grid(row=row, column=0, ipadx=65, sticky= 'ew', pady=1, padx=3)
                Label(self.frame1b, text=time_.text, bg='white').grid(row=row, column=1, ipadx=65, sticky='ew', pady=1, padx=3)
                row += 1
            self.frame1b.pack(expand=True, anchor=N)
            Button(self.frame1c, text='Pilih Kota', font='Arial', bg='white', fg='green', command=lambda: self.buttonCmd(1)).pack()
            self.frame1c.pack()
            self.me = Button(self.frame00, text=decrypt(self.r, self.key), bd=0)
            self.me.pack()
            self.frame00.pack()
        else:
            self.frame1a.destroy()
            self.frame1b.destroy()
            self.frame1c.destroy()
            self.frame00.destroy()

    def getSchedule(self):
        try:
            res = requests.get(f'https://jadwalsholat.org/adzan/monthly.php?id={self.id}')
            self.frame0.destroy()
            data = bs(res.content, 'html.parser')
            tr_ = data.find_all('tr')
            for tr in tr_:
                if tr.attrs['class'] == ['table_header']:
                    schedule = tr.find_all('td')
                if tr.attrs['class'] == ['table_highlight']:
                    time_ = tr.find_all('td')
            self.schedule = list(zip(schedule[1:], time_[1:]))
            self.frame1_(create=True)
        except:
            self.label1['text'] = 'Gagal Memuat... Tolong periksa koneksi anda!\nAtau hubungi developer jika masalah tidak terselesaikan!'
            self.label1['fg'] = 'red'''

    def saveSchedule(self):
        encryptKey[1] = encrypt(f'{self.city}-{self.id}', encryptKey[0])
        open(f'{self.cwd}\\schedule.key', 'w').write('|'.join(encryptKey))

                
if __name__ == '__main__':
    app = UI()
    app.mainloop()