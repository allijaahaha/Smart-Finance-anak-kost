from datetime import datetime
import database
from config import Colors
from utils import input_tanggal, input_angka


def pilih_sumber():
    print("\n Income")
    print("1. Parents")
    print("2. Side Job")
    print("3. Others")
    print("0. Back to main menu")

    pilih = input("Choose source: ")

    if pilih == "1":
        return "Parents"
    elif pilih == "2":
        return "Side Job"
    elif pilih == "3":
        return input("Other Reason : ")
    elif pilih == "0":
        return None
    else:
        print(f"{Colors.RED}Invalid choice!{Colors.ENDC}")
        return pilih_sumber()


def proses_emergency(data, jumlah):
    if jumlah >= data["potongan_emergency"]:
        data["emergency_fund"] += data["potongan_emergency"]
        jumlah -= data["potongan_emergency"]
        print(f"Rp{data['potongan_emergency']} Added to the emergency fund")
    return jumlah


def cek_locked_target(data, tanggal):
    tanggal_obj = datetime.strptime(tanggal, "%Y-%m-%d")
    for target_item in data["target_list"]:
        deadline_obj = datetime.strptime(target_item["deadline"], "%Y-%m-%d")

        if tanggal_obj > deadline_obj and target_item["tabungan"] < target_item["target"]:
            target_item["locked"] = True
            return target_item
    return None


def proses_locked(data, locked, jumlah, tanggal):
    print(f"{Colors.RED} Target {locked['nama']} Locked! Every income automatically goes to the savings {Colors.ENDC}")
    sisa_target = locked["target"] - locked["tabungan"]
    if jumlah > sisa_target:
        locked["tabungan"] += sisa_target
        data["saldo"] += jumlah - sisa_target
        data["histori_tabungan"].append({
            "tanggal": tanggal,
            "target": locked["nama"],
            "jumlah": sisa_target
        })

        print(f"Rp{sisa_target} added to the savings target")
        print(f"Rp{jumlah - sisa_target} added to the general balance")
    else:
        locked["tabungan"] += jumlah
        data["histori_tabungan"].append({
            "tanggal": tanggal,
            "target": locked["nama"],
            "jumlah": jumlah
        })

        print(f"Rp{jumlah} added to the savings target")
    if locked["tabungan"] >= locked["target"]:
        locked["locked"] = False
        print(f"{Colors.GREEN} CONGRATULATIONS! Target {locked['nama']} finally achieved! {Colors.ENDC}")


def proses_tabungan_biasa(data, jumlah, tanggal):
    while True:
        print("Add to savings target?")
        print("1. Yes")
        print("2. No")

        pilih_tabung = input("Pilih: ")
        if pilih_tabung in ("1", "2"):
            break
        print(f"{Colors.RED}Invalid choice!{Colors.ENDC}")

    if pilih_tabung == "2":
        data["saldo"] += jumlah
        return

    if len(data["target_list"]) == 0:
        print(f"{Colors.RED} No savings targets Yet! {Colors.ENDC}")
        data["saldo"] += jumlah
        return

    available_targets = [t for t in data["target_list"] if t["tabungan"] < t["target"]]

    if len(available_targets) == 0:
        print(f"{Colors.RED} All savings targets have been achieved! {Colors.ENDC}")
        data["saldo"] += jumlah
        return

    print("Pilih target tabungan: ")
    for i, target_item in enumerate(available_targets, 1):
        print(f"{i}. {target_item['nama']} | Rp{target_item['tabungan']}/Rp{target_item['target']}")
    pilih_target = input_angka("Pilih target: ") - 1

    if 0 <= pilih_target < len(available_targets):
        target_item = available_targets[pilih_target]
        sisa_target = target_item["target"] - target_item["tabungan"]

        while True:
            masuk_tabungan = input_angka("Masukkan jumlah yang mau ditabung: Rp")
            if masuk_tabungan > jumlah:
                print(f"{Colors.RED} Amount exceeds income! {Colors.ENDC}")
            elif masuk_tabungan > sisa_target:
                print(f"{Colors.RED} Amount exceeds the remaining targets amount! {Colors.ENDC}")
                print(f"Remaining amount for {target_item['nama']}: Rp{sisa_target}")
            else:
                break

        target_item["tabungan"] += masuk_tabungan
        data["histori_tabungan"].append({
            "tanggal": tanggal,
            "target": target_item["nama"],
            "jumlah": masuk_tabungan
        })

        data["saldo"] += jumlah - masuk_tabungan
        print(f"{Colors.GREEN} Successfully added to {target_item['nama']}!{Colors.ENDC}")

        if target_item["tabungan"] >= target_item["target"]:
            print(f"{Colors.GREEN} CONGRATULATIONS! Target {target_item['nama']} have been achieved! {Colors.ENDC}")
    else:
        print(f"{Colors.RED} Invalid target choice! {Colors.ENDC}")
        data["saldo"] += jumlah


def simpan_histori_pemasukan(data, tanggal, sumber, jumlah_asli, potongan):
    data["transaksi"].append({
        "tipe": "pemasukan",
        "tanggal": tanggal,
        "sumber": sumber,
        "jumlah_asli": jumlah_asli,
        "potongan_emergency": potongan,
        "jumlah_bersih": jumlah_asli - potongan
    })


def pemasukan():
    data = database.get_data()
    while True:
        sumber = pilih_sumber()
        if sumber is None:
            break

        tanggal = input_tanggal()
        jumlah_asli = input_angka("Enter income amount: Rp")

        potongan = 0
        if jumlah_asli >= data["potongan_emergency"]:
            potongan = data["potongan_emergency"]

        jumlah = proses_emergency(data, jumlah_asli)

        locked_target = cek_locked_target(data, tanggal)

        if locked_target:
            proses_locked(data, locked_target, jumlah, tanggal)
        else:
            proses_tabungan_biasa(data, jumlah, tanggal)

        simpan_histori_pemasukan(data, tanggal, sumber, jumlah_asli, potongan)
        database.save()
        print(f"{Colors.GREEN} YAY! Income have been successfully added! {Colors.ENDC}")