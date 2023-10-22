import pyautogui
import pygetwindow as gw
import pyscreeze
import os
import time
from time import sleep
import tkinter as tk
from tkinter import *
import random

# Gerar cupom ---------------------------------------
def gerar_cupom1(total):
    cupom = random.uniform(50, 350)
    return round(cupom, 2) if cupom <= total else None

class CupomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot Cupom")
        self.root.geometry('250x200')
        self.total = 0
        self.cupom_atual = None
        self.count = 0
        self.playing = True 

        self.quant_label = tk.Label(root, text="Quantidade de produto", font=('bold', 10))
        self.quant_label.pack()

        self.quant_entry = tk.Entry(root, text="", font=('bold', 10))
        self.quant_entry.pack()

        self.vl_label = tk.Label(root, text="Preço unitário, use (.)", font=('bold', 10))
        self.vl_label.pack()

        self.vl_entry = tk.Entry(root, text="", font=('bold', 10))
        self.vl_entry.pack()

        self.quant_cupom_label = tk.Label(root, text="Quantidade venda por cupom", font=('bold', 8))
        self.quant_cupom_label.pack()

        self.quant_cupom_entry = tk.Entry(root, text="", font=('bold', 8))
        self.quant_cupom_entry.pack()

        self.label = tk.Label(root, text="", font=('bold', 10))
        self.label.pack()

        self.play_button = tk.Button(root, text="Play", font=('bold', 10), bg='green', fg='white', command=self.play)
        self.play_button.pack(side='left', expand=True, fill='both')

        self.stop_button = tk.Button(root, text="Stop", font=('bold', 10), bg='red', fg='white', command=self.stop)
        self.stop_button.pack(side='left', expand=True, fill='both')

        self.playing = False
        self.cupom_timer = None

    def play(self):
        if not self.playing:
            if self.total == 0:
                self.total = float(self.quant_entry.get()) * float(self.vl_entry.get())
                if self.total is None:
                    return
            self.playing = True
            self.generate_and_display_cupom()

    def stop(self):
        self.playing = False
        if self.cupom_timer:
            self.root.after_cancel(self.cupom_timer)
            self.cupom_timer = None
        self.total = 0
        self.cupom_atual = None
        self.root.destroy()

    def generate_and_display_cupom(self):
        if self.playing:
            if self.count < float(self.quant_cupom_entry.get()):
                self.cupom_atual = gerar_cupom1(self.total)

                if self.cupom_atual is not None:
                    self.total -= self.cupom_atual
                    self.label.config(text=f"Cupom: R$ {self.cupom_atual:.2f}\nValor Total Restante: R$ {self.total:.2f}", font=('bold', 8))
                    print(self.cupom_atual)
                    self.preencher_bloco_notas()
                    self.count += 1
                    self.cupom_timer = self.root.after(300, self.generate_and_display_cupom)

                else:
                    self.label.config(text="Não é possível gerar mais cupons.", font=('red', 'bold', 8))
                    self.playing = False
            else:
                self.count = 0
                self.playing = False
                sleep(15)
                self.root.after(300, self.proxima)

    def start(self):
        self.total = 1
        self.label = tk.Label(self.root, text="Fechamento da venda", font=('bold', 8))
        self.label.pack()
        self.generate_and_display_cupom()

    def preencher_bloco_notas(self):
        def wait(milliseconds):
            time.sleep(milliseconds / 1000.0)

        def switch_window(window_title):
            try:
                window = gw.getWindowsWithTitle(window_title)[0]
                window.activate()
            except IndexError:
                print(f"Janela '{window_title}' não encontrada.")

        initial_window_title = "AnyDesk.exe, 1 894 667 010 - AnyDesk"
        switch_window(initial_window_title)

        actions = [
            ("Mouse left click", "171, 660"),
            ("Wait", "500 ms"),

            ("Key Down", "Ctrl"),
            ("Character(s)", "I"),
            ("Key Up", "Ctrl"),
            ("Wait", "500 ms"),

            ("Text output", "002"),
            ("Wait", "300 ms"),

            ("Left mouse button Down", "637, 500"),
            ("Left mouse button Up", "576, 512"),
            ("Wait", "300 ms"),

            ("Text output", str(self.cupom_atual)),  # Correção aqui
            ("Key press", "Enter"),
            ("Wait", "300 ms"),
            ("Key press", "Enter"),
            ("Wait", "4443 ms"),
        ]

        for action, value in actions:
            if action == "Window change":
                switch_window(value)
            elif action == "Mouse left click":
                x, y = map(int, value.split(','))
                pyautogui.click(x, y)
            elif action == "Wait":
                wait(int(value.split(' ')[0]))
            elif action == "Key Down":
                pyautogui.keyDown(value)
            elif action == "Key Up":
                pyautogui.keyUp(value)
            elif action == "Character(s)":
                pyautogui.typewrite(value)
            elif action == "Text output":
                pyautogui.write(value)
            elif action == "Left mouse button Down":
                x, y = map(int, value.split(','))
                pyautogui.mouseDown(x, y)
            elif action == "Left mouse button Up":
                x, y = map(int, value.split(','))
                pyautogui.mouseUp(x, y)
            elif action == "Key press":
                pyautogui.press(value)

    def proxima(self):
        print('deu certo!!')
        print("Executando a próxima função...")
        sleep(5)
        self.playing = True
        self.generate_and_display_cupom()

if __name__ == "__main__":
    root = tk.Tk()
    app = CupomApp(root)
    root.mainloop()
