import os
import threading
from tkinter import *
import tkinter as tk
import time
import cv2
import pyautogui
import numpy as np
import time
from tkinter import messagebox

stop_thread = False


##########
 
### Cordenadas botão aceitar
x=920
y=712
btnConfirmar = (842, 848)

### imagem aceitar

elemento_imagem = cv2.imread(os.path.abspath("btnAceitar.png"))
largura = elemento_imagem.shape[1]
altura = elemento_imagem.shape[0]
   

def accept_queue():
    ### While verifica se apareceu para aceitar
    print("Executando...")
    while stop_thread == False:
        # Capture a região da tela
        tela = pyautogui.screenshot()
        tela = cv2.cvtColor(np.array(tela), cv2.COLOR_RGB2BGR)

        # Procure pelo elemento na região da tela capturada
        resultado = cv2.matchTemplate(tela[y:y+altura, x:x+largura], elemento_imagem, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        # Defina um limite de correspondência para determinar se o elemento está presente
        limite_correspondencia = 0.2

        if max_val >= limite_correspondencia:
            # O elemento está presente
            print("Elemento encontrado!")
            pyautogui.moveTo(x,y)
            pyautogui.click()
            print("Fila aceita... Verificar se estamos no lobby de runa")
            
            
            
        else:
            # O elemento não está presente, aguarde um pouco e verifique novamente
            time.sleep(1)
            print("Elemento não encontrado. Tentando novamente...")

#########

def thread_function():
 while True:
  if stop_thread:
   break
  print("Aceita fila is running "+time.strftime("%Y-%m-%d às %H:%M:%S"))
  button_start.config(state="disabled")
  button_stop.config(state="active")
  text_exe["fg"] = "green"
  text_exe["text"] = "ON"
  accept_queue()

def confirm_quit():
    result = messagebox.askquestion("Confirmar Saída", "Tem certeza de que deseja sair?")
    if result == "yes":
        stop_loop()
        root.quit()

def stop_loop():
 global stop_thread
 stop_thread = True
 print("Aceita fila desativado")
 button_start.config(state="active")
 button_stop.config(state="disabled")
 text_exe["fg"] = "red"
 text_exe["text"] = "OFF"


def start_loop():
 global stop_thread
 stop_thread = False
 thread = threading.Thread(target=thread_function)
 thread.start()

root = tk.Tk()
root.title("BOT")
root.protocol("WM_DELETE_WINDOW", confirm_quit)
root.geometry("125x100")
root.iconbitmap("robot-icon2.ico")
root.resizable(width=False, height=False)



button_stop = tk.Button(root, text="Stop",  command=stop_loop)
button_stop.pack()

button_start = tk.Button(root, text="Start", command=start_loop)
button_start.pack()

text_exe = Label(root, text="ON...", fg="Green")
text_exe.pack()

thread = threading.Thread(target=thread_function)
thread.start()

root.mainloop()

thread.join()

print("BOT is finished")