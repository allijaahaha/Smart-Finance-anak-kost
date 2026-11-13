from datetime import datetime
from config import Colors


def input_tanggal(pesan="Insert date (yyyy-mm-dd): "):
    while True:
        tanggal = input(pesan)
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            return tanggal
        except ValueError:
            print(f"{Colors.RED}Date format is invalid! Please use yyyy-mm-dd{Colors.ENDC}")


def input_angka(pesan):
    while True:
        try:
            angka = int(input(pesan))
            if angka <= 0:
                print(f"{Colors.RED}Amount must be greater than 0!{Colors.ENDC}")
                continue
            return angka
        except ValueError:
            print(f"{Colors.RED}Input must be a positive integer!{Colors.ENDC}")