import database
from config import Colors, SALDO_MINIMUM_PERINGATAN
from utils import input_tanggal, input_angka

KATEGORI = {
    "1": "Eat",
    "2": "Transportation",
    "3": "Laundry",
    "4": "Hanging out",
}


def pengeluaran():
    data = database.get_data()

    while True:
        print("\n Outcome")
        print("1. Eat")
        print("2. Transportation")
        print("3. Laundry")
        print("4. Hanging out")
        print("5. Others")
        print("0. Back to main menu")

        alasan_pilih = input("Choose outcome: ")

        if alasan_pilih in KATEGORI:
            pengeluaran_nama = KATEGORI[alasan_pilih]
        elif alasan_pilih == "5":
            pengeluaran_nama = input("Other reason : ")
        elif alasan_pilih == "0":
            break
        else:
            print(f"{Colors.RED} Invalid choice! {Colors.ENDC}")
            continue

        tanggal = input_tanggal()
        jumlah = input_angka("Insert amount of outcome: Rp")

        if jumlah > data["saldo"]:
            print(f"{Colors.RED}Insufficient balance!{Colors.ENDC}")
            continue

        data["saldo"] -= jumlah

        data["transaksi"].append({
            "tipe": "pengeluaran",
            "tanggal": tanggal,
            "alasan": pengeluaran_nama,
            "jumlah": jumlah
        })
        database.save()

        if data["saldo"] < SALDO_MINIMUM_PERINGATAN:
            print(f"{Colors.RED} WATCH OUT! Your wallet is on the verge! {Colors.ENDC}")

        print(f"{Colors.GREEN} YAY! Your outcome have been successfully added! {Colors.ENDC}")