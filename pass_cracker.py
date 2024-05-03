import string
import time
import pyfiglet
import colorama
import tkinter as tk
from tkinter import filedialog
from colorama import Fore, Back, Style
from pyzipper import ZipFile
from zipfile import ZipFile as zp
from rarfile import RarFile
#from pycryptodome.hashlib.sha256 import new as sha256
import random

colorama.init(autoreset=True)
ascii_banner = pyfiglet.figlet_format("Password Cracker")
print(Fore.RED + ascii_banner)

file_path = ""
password_length = 0

def select_file():
    global file_path
    file_path = filedialog.askopenfilename()
    file_format = file_path.split('.')[-1]
    file_format_label.config(text=f'File format: {file_format.upper()}')

def crack():
    global password_length
    password_length = int(password_length_entry.get())

    if file_path == "":
        print(Fore.RED + "Error: No file selected." + Style.RESET_ALL)
        return

    if password_length <= 0:
        print(Fore.RED + "Error: Invalid password length." + Style.RESET_ALL)
        return

    all_characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
        + " "
        + "!"
        + ":"
        + "?"
    )

    def crack_zip(zipped_file, password):
        try:
            zipped_file.extractall(pwd=password.encode())
            return True
        except:
            return False

    def crack_rar(rar_file, password):
        try:
            rar_file.open(pwd=password)
            return True
        except:
            return False

    def crack_pdf(pdf_file, password):
        try:
            pdf_file.decrypt(password)
            return True
        except:
            return False

    def brute_force(file, file_type):
        print(Fore.GREEN + "Starting brute force attack!" + Style.RESET_ALL)
        start_time = time.time()
        total_passwords = len(all_characters) ** password_length
        
        for i in range(total_passwords):
            password = ''.join(
                random.choices(all_characters, k=password_length)
            )

            if file_type == ".zip":
                if crack_zip(file, password):
                    print(Fore.GREEN + f"Password cracked: {password}" + Style.RESET_ALL)
                    return

            elif file_type == ".rar":
                if crack_rar(file, password):
                    print(Fore.GREEN + f"Password cracked: {password}" + Style.RESET_ALL)
                    return

            elif file_type == ".pdf":
                if crack_pdf(file, password):
                    print(Fore.GREEN + f"Password cracked: {password}" + Style.RESET_ALL)
                    return

        print(Fore.RED + "Brute force attack failed." + Style.RESET_ALL)
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.2f} seconds")

    if file_path.endswith(".zip"):
        try:
            with ZipFile(file_path, 'r') as zipped_file:
                brute_force(zipped_file, ".zip")
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)

    elif file_path.endswith(".rar"):
        try:
            with RarFile(file_path, 'r') as rar_file:
                brute_force(rar_file, ".rar")
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)

    elif file_path.endswith(".pdf"):
        try:
            pdf_file = open(file_path, 'rb')
            brute_force(pdf_file, ".pdf")
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)

    else:
        print(Fore.RED + "Invalid file format." + Style.RESET_ALL)

window = tk.Tk()
window.title("Password Cracker GUI")
window.geometry("600x400")

instructions_label = tk.Label(text="1. Select a file\n2. Enter password length\n3. Click 'Crack'")
instructions_label.pack(pady=50)

file_button = tk.Button(window, text="Select file", command=select_file)
file_button.pack(pady=15)

file_format_label = tk.Label(window, text="")
file_format_label.pack()

password_length_label = tk.Label(window, text="Password length:")
password_length_label.pack(pady=15)

password_length_entry = tk.Entry(window)
password_length_entry.pack()

crack_button = tk.Button(window, text="Crack", command=crack)
crack_button.pack(pady=15)

window.mainloop()
