import os
import requests
import tkinter as tk

from bs4 import BeautifulSoup
from tkinter import messagebox


class MltdImageDownloader(object):
    def __init__(self):
        self.url = 'https://mltd.matsurihi.me/cards'
        self.folder_path_prefix = './MLTDimages'

    def downloader(self):
        try:
            ir = self.en.get()
            if ir.strip() == '':
                messagebox.showerror('錯誤', '請輸入卡片號碼')
                return
            response = requests.get(f'{self.url}/{ir}', headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'})
            if response.status_code != 200:
                messagebox.showerror('錯誤', '找不到該卡片')
                return
            soup = BeautifulSoup(response.text, 'html.parser')
            data = soup.find_all('img', {'class', 'd-block w-100'})
            image_links = [result.get('src') for result in data]
            if image_links == []:
                messagebox.showerror('錯誤', '該卡片不是SSR卡片')
                return
            for index, link in enumerate(image_links):
                if index == 2:
                    break
                folder_path = f'{self.folder_path_prefix}/{ir}/'
                os.makedirs(folder_path, exist_ok=True)
                img = requests.get(link)

                with open(f'MLTDimages\{ir}\\' + str(ir) + str(index+1) + '.jpg', 'wb') as file:
                    file.write(img.content)
                    print(f'DW...{index+1}')

            messagebox.showinfo('提示', f'卡片號{ir}下載完畢')
        except Exception as e:
            messagebox.showerror('錯誤', e)
            return

    def main(self):
        win = tk.Tk()
        win.title('MLTD圖片下載器')

        win.geometry('400x400')
        win.config(background='grey')
        win.attributes('-alpha', 1)
        win.resizable(False, False)

        win.iconbitmap('icon.ico')

        input = tk.Label(text='請輸入卡片號碼')
        input.config(height=1, width=20, bg='grey', fg='white')
        input.pack()

        self.en = tk.Entry()
        self.en.pack()

        btn_enter = tk.Button(text='OK')
        btn_enter.config(height=1, width=10, command=self.downloader)
        btn_enter.pack()

        self.img_show = tk.Label(text='點擊按鈕下載', bg='grey', fg='white')
        self.img_show.pack()

        win.mainloop()


if __name__ == '__main__':
    image_downloader = MltdImageDownloader()
    image_downloader.main()
