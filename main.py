import sys
import ctypes
import os
import subprocess
import customtkinter as ctk
import webbrowser
from PIL import Image
from tkinter import messagebox


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit()

def resource_path(relative_path):
    # Получение пути к ресурсам (для exe и обычного запуска)
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Riot Offline")
        self.geometry("340x430")
        self.resizable(False, False)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self, text="Status now", text_color="gray", font=("TT Interphases Pro", 12)
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        # статус
        self.text_label = ctk.CTkLabel(
            self, text="You’re ONLINE", text_color="green", font=("TT Interphases Pro", 35, "bold")
        )
        self.text_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))

        # Кнопки для Offline и Online режима
        self.offline_button = ctk.CTkButton(
            self, text="Offline", command=self.activate_rule, width=150, height=50
        )
        self.offline_button.grid(row=2, column=0, padx=10, pady=10)

        self.online_button = ctk.CTkButton(
            self, text="Online", command=self.deactivate_rule, width=150, height=50
        )
        self.online_button.grid(row=2, column=1, padx=10, pady=10)

        # Описание режимов
        self.offline_label = ctk.CTkLabel(
            self, text="• no chat/no friend list.", text_color="gray", font=("TT Interphases Pro", 10), wraplength=120
        )
        self.offline_label.grid(row=3, columnspan=1)

        self.online_label = ctk.CTkLabel(
            self, text="• chat/friend list on, just turning off offline mode .", text_color="gray", font=("TT Interphases Pro", 10), wraplength=120
        )
        self.online_label.grid(row=3, column=1, columnspan=3)

        self.online_label2 = ctk.CTkLabel(
            self, text="(may take a while  around min ≈1).",
            text_color="gray", font=("Arial", 10), wraplength=120
        )
        self.online_label2.grid(row=4, column=0, columnspan=1)

        self.online_label3 = ctk.CTkLabel(
            self, text="(may take a while  around min ≈1).",
            text_color="gray", font=("Arial", 10), wraplength=120
        )
        self.online_label3.grid(row=4, column=1, columnspan=3)

        # Настройки внешнего вида
        self.appearance_mode_option_menu = ctk.CTkOptionMenu(
            self, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event, width=130,
        )
        self.appearance_mode_option_menu.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.appearance_mode_option_menu.set("Dark")

        # Логотип и автор
        image_path = resource_path("Image.png")
        logo_path = resource_path("image2.png")
        logo2_path = resource_path("144.png")
        logo3_path = resource_path("155.png")

        self.logo = ctk.CTkImage(dark_image=Image.open(image_path), size=(90, 40))
        self.logo_label = ctk.CTkLabel(master=self, text="", image=self.logo)
        self.logo_label.grid(row=6, column=0, columnspan=2, pady=(20, 0))

        self.author_label = ctk.CTkLabel(
            self, text="©lovely yummy", text_color="gray", font=("TT Interphases Pro", 9, "italic"), wraplength=50)
        self.author_label.grid(row=7, column=0, columnspan=2, pady=(0, 10))

        # Кнопка выхода
        self.exit_button = ctk.CTkButton(
            self, text="Exit", command=self.exit_application, width=100, height=50
        )
        self.exit_button.grid(row=8, column=0, columnspan=2, pady=(0, 10) )

        # Проверить состояние правила при запуске
        self.check_firewall_rule()

        self.author_label3 = ctk.CTkLabel(
            self, text="v 2.2", text_color="gray", font=("TT Interphases Pro", 9, "italic"), wraplength=50)
        self.author_label3.grid(row=8, column=0, pady=(30, 0), sticky="sw")

        self.logo1 = ctk.CTkImage(dark_image=Image.open(logo_path), size=(50, 45))
        self.logo1_label = ctk.CTkLabel(master=self, text="", image=self.logo1)
        self.logo1_label.grid(row=4, column=0, columnspan=2, pady=(0, 0), sticky="n", padx=(0, 0))

        self.logo2 = ctk.CTkImage(dark_image=Image.open(logo2_path), size=(25, 20))
        self.logo2_label = ctk.CTkLabel(master=self, text="", image=self.logo2)
        self.logo2_label.grid(row=6, column=1, columnspan=2, pady=(0, 0), sticky="", padx=(57, 0))

        self.logo3 = ctk.CTkImage(dark_image=Image.open(logo3_path), size=(80, 40))
        self.logo3_label = ctk.CTkLabel(master=self, text="", image=self.logo3)
        self.logo3_label.grid(row=6, column=0, columnspan=1, pady=(0, 0), sticky="", padx=(0, 40))

        self.logo3_label.bind("<Button-1>", self.open_twitch)


        # Надпись Firewall
        self.firewall_label = ctk.CTkLabel(
            self, text="Reminder! Firewall. (ignore if firewall enabled)", text_color="dark orange",
            font=("TT Interphases Pro", 9), wraplength=90)
        self.firewall_label.grid(row=7, column=1, columnspan=3, padx=(52,0), pady=(0, 0))
        self.firewall_label.grid_remove()  # Скрываем надпись при запуске

        # Привязка событий наведения на логотип
        self.logo2_label.bind("<Enter>", self.show_firewall_label)
        self.logo2_label.bind("<Leave>", self.hide_firewall_label)

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def activate_rule(self):
        command = ('netsh advfirewall firewall add rule name="lolchat" '
                   'dir=out remoteport=5223 protocol=TCP action=block')
        self.execute_command(command)

    def deactivate_rule(self):
        command = 'netsh advfirewall firewall delete rule name="lolchat"'
        try:
            subprocess.run(command, shell=True, check=True)
            self.text_label.configure(text="You’re ONLINE", text_color="green")
        except subprocess.CalledProcessError:
            # Если правило не существует, это не ошибка
            self.text_label.configure(text="You’re ONLINE", text_color="green")

    def execute_command(self, command):
        try:
            subprocess.run(command, shell=True, check=True)
            self.check_firewall_rule()
        except subprocess.CalledProcessError as e:
            self.show_error(f"Failed to execute command: {e}")

    def check_firewall_rule(self):
        command = 'netsh advfirewall firewall show rule name="lolchat"'
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if "No rules match" in result.stdout:
                self.text_label.configure(text="You’re ONLINE", text_color="green")
            else:
                self.text_label.configure(text="You’re OFFLINE", text_color="red")
        except Exception as e:
            self.show_error(f"Failed to check firewall rule: {e}")

    def exit_application(self):
        self.destroy()

    def show_firewall_label(self, event=None):
        self.firewall_label.grid()

    def hide_firewall_label(self, event=None):
        self.firewall_label.grid_remove()

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def open_twitch(self, event):
        webbrowser.open("https://twitch.tv/lovelyummy")

if __name__ == "__main__":
    app = App()
    app.mainloop()