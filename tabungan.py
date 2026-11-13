import database
from config import Colors
from utils import input_tanggal, input_angka


def _set_target(data):
    nama = input("What are you saving up for?: ")
    uang = input_angka("Enter target amount: Rp")
    deadline = input_tanggal("Enter deadline (yyyy-mm-dd): ")

    data["target_list"].append({
        "nama": nama,
        "target": uang,
        "deadline": deadline,
        "tabungan": 0,
        "locked": False
    })
    database.save()
    print(f"{Colors.GREEN} Target Successfully added! {Colors.ENDC}")


def _lihat_progress(data):
    if len(data["target_list"]) == 0:
        print(f"{Colors.RED} No savings targets yet! {Colors.ENDC}")
        return

    print("Choose a savings target to view progress:")
    available_targets = [t for t in data["target_list"] if t["tabungan"] < t["target"]]

    if len(available_targets) == 0:
        print(f"{Colors.GREEN} All targets have been achieved! {Colors.ENDC}")
        return

    for i, target_item in enumerate(available_targets, 1):
        print(f"{i}. {target_item['nama']}")

    pilih_target = input_angka("Choose target: ") - 1

    if 0 <= pilih_target < len(available_targets):
        target_item = available_targets[pilih_target]
        sisa = target_item["target"] - target_item["tabungan"]
        print("\n Savings target progress:")
        print("Target:", target_item["nama"])
        print("Deadline:", target_item["deadline"])
        print("Target amount: Rp", target_item["target"])
        print("Have been saved: Rp", target_item["tabungan"])
        print("Remaining: Rp", sisa)

        if target_item["locked"]:
            print(f"{Colors.RED}Status: LOCKED{Colors.ENDC}")
        else:
            print(f"{Colors.GREEN}Status: Normal{Colors.ENDC}")
    else:
        print(f"{Colors.RED} Invalid target choice!{Colors.ENDC}")


def _cairkan(data):
    completed_targets = [t for t in data["target_list"] if t["tabungan"] >= t["target"]]

    if len(completed_targets) == 0:
        print(f"{Colors.RED}No target has been achieved yet!{Colors.ENDC}")
        return

    print("\n COMPLETED TARGETS TO BE CASHED OUT")
    for i, target_item in enumerate(completed_targets, 1):
        print(f"{i}. {target_item['nama']} | Rp.{target_item['tabungan']}")

    pilih_target = input_angka("Choose target: ") - 1

    if 0 <= pilih_target < len(completed_targets):
        target_item = completed_targets[pilih_target]
        data["saldo"] += target_item["tabungan"]
        data["target_list"].remove(target_item)
        database.save()
        print(f"{Colors.GREEN}Rp{target_item['tabungan']} Successfully cashed out!!{Colors.ENDC}")
    else:
        print(f"{Colors.RED}Invalid target choice!{Colors.ENDC}")


def target_tabungan():
    data = database.get_data()

    while True:
        print("\nTARGET SAVINGS")
        print("1. Set target")
        print("2. View progress")
        print("3. Cash out completed target")
        print("0. Back to main menu")

        pilih = input("Choose: ")

        if pilih == "1":
            _set_target(data)
        elif pilih == "2":
            _lihat_progress(data)
        elif pilih == "3":
            _cairkan(data)
        elif pilih == "0":
            break
        else:
            print(f"{Colors.RED} Invalid choice! {Colors.ENDC}")