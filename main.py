import Auth
import database
import session
from config import Colors
from emergency import emergency_menu, set_potongan_emergency
from history import lihat_histori
from pemasukan import pemasukan
from pengeluaran import pengeluaran
from tabungan import target_tabungan


def menu_login():
    print("\n WELCOME TO DOMPET ANAK KOST")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    pilih = input("Choose: ")

    if pilih == "1":
        Auth.register()
    elif pilih == "2":
        Auth.login()
    elif pilih == "3":
        print("Thank you for using Dompet Anak kost")
        raise SystemExit
    else:
        print(f"{Colors.RED} Invalid target choice! {Colors.ENDC}")


def menu_utama():
    data = database.get_data()

    print("\n DOMPET ANAK KOS")
    print("User:", session.current_user)
    print("balance:", data["saldo"])
    print("Emergency fund:", data["emergency_fund"])

    print("1. Income")
    print("2. Outcome")
    print("3. Target Savings")
    print("4. Emergency Fund")
    print("5. Set emergency fund")
    print("6. History")
    print("7. Logout")

    pilih = input("Pilih: ")
    if pilih == "1":
        pemasukan()
    elif pilih == "2":
        pengeluaran()
    elif pilih == "3":
        target_tabungan()
    elif pilih == "4":
        emergency_menu()
    elif pilih == "5":
        set_potongan_emergency()
    elif pilih == "6":
        lihat_histori()
    elif pilih == "7":
        database.save()
        print("Logout berhasil!")
        session.current_user = ""
    else:
        print(f"{Colors.RED} Invalid target choice! {Colors.ENDC}")


def main():
    database.load()
    while True:
        if session.current_user == "":
            menu_login()
        else:
            menu_utama()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        database.save()
        print("\n Data saved, exitting the application.")