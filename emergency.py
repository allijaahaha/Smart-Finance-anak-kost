from datetime import datetime

import database
from config import Colors, BATAS_AMBIL_EMERGENCY
from utils import input_angka


def emergency_menu():
    data = database.get_data()

    print("\n EMERGENCY FUND")
    print("Emergency Fund balance: Rp", data["emergency_fund"])

    ambil = input("Withdraw money? (y/n): ")
    if ambil.lower() == "y":
        jumlah = input_angka(f"Maximum Withdrawal is Rp{BATAS_AMBIL_EMERGENCY} \n Enter amount: Rp")
        alasan = input("Enter reason for withdrawal: ")

        if jumlah > BATAS_AMBIL_EMERGENCY:
            print(f"{Colors.RED} Exceeds maximum withdrawal limit!{Colors.ENDC}")
        elif jumlah > data["emergency_fund"]:
            print(f"{Colors.RED} Emergency fund balance is insufficient! {Colors.ENDC}")
        else:
            data["emergency_fund"] -= jumlah
            data["saldo"] += jumlah
            data["transaksi"].append({
                "tipe": "emergency",
                "tanggal": str(datetime.today().date()),
                "alasan": alasan,
                "jumlah": jumlah
            })
            database.save()
            print(f"{Colors.GREEN} Successfully withdrawn for: {Colors.ENDC}", alasan)


def set_potongan_emergency():
    data = database.get_data()
    data["potongan_emergency"] = input_angka("Enter the new emergency withdrawal limit : Rp")
    database.save()
    print("Emergency withdrawal limit successfully updated!")