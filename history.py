import database
from config import Colors


def _histori_pemasukan(data):
    print("\n Income History")
    for t in data["transaksi"]:
        if t["tipe"] == "pemasukan":
            print("Date  :", t["tanggal"])
            print("Source   :", t["sumber"])
            print("Income:", f"Rp{t['jumlah_asli']}")
            print("Emergency fund:", f"Rp{t['potongan_emergency']}")
            print("Net Income:", f"Rp{t['jumlah_bersih']}")
            print("============================")


def _histori_pengeluaran(data):
    print("\n Outcome History")
    for t in data["transaksi"]:
        if t["tipe"] == "pengeluaran":
            print("Date  :", t["tanggal"])
            print("Category :", t["alasan"])
            print("Amount   : Rp", t["jumlah"])
            print("======================")


def _histori_emergency(data):
    print("\n Emergency Fund Withdrawal History")
    for t in data["transaksi"]:
        if t["tipe"] == "emergency":
            print("Date :", t["tanggal"])
            print("Reason  :", t["alasan"])
            print("Amount : Rp", t["jumlah"])
            print("======================")


def _histori_tabungan(data):
    print("\n Savings History")
    if len(data["histori_tabungan"]) == 0:
        print(f"{Colors.RED}There's no savings history!{Colors.ENDC}")
        return
    for t in data["histori_tabungan"]:
        print("Date :", t["tanggal"])
        print("Target  :", t["target"])
        print("Amount  : Rp", t["jumlah"])
        print("======================")


def _grafik(data):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print(f"{Colors.RED}matplotlib belum terpasang. Jalankan: pip install matplotlib{Colors.ENDC}")
        return

    transaksi_sorted = sorted(data["transaksi"], key=lambda x: x["tanggal"])

    tanggal_list = []
    pemasukan_list = []
    pengeluaran_list = []
    saldo_list = []
    balance = 0

    for t in transaksi_sorted:
        tanggal_list.append(t["tanggal"])
        if t["tipe"] == "pemasukan":
            pemasukan_list.append(t["jumlah_bersih"])
            pengeluaran_list.append(0)
            balance += t["jumlah_bersih"]
        elif t["tipe"] == "pengeluaran":
            pemasukan_list.append(0)
            pengeluaran_list.append(t["jumlah"])
            balance -= t["jumlah"]
        else:
            pemasukan_list.append(0)
            pengeluaran_list.append(0)
        saldo_list.append(balance)

    x = range(len(tanggal_list))
    plt.figure(figsize=(7, 5))

    plt.bar([i - 0.2 for i in x], pemasukan_list, width=0.4, color='Yellow', alpha=0.3, label='pemasukan')
    plt.bar([i + 0.2 for i in x], pengeluaran_list, width=0.4, color='Green', alpha=0.5, label='pengeluaran')
    plt.plot(x, saldo_list, color='blue', linewidth=2, label='Saldo')
    plt.xticks(x, tanggal_list, rotation=45)
    plt.title("GRAFIK KEUANGAN")
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah Uang (Rp)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()


def lihat_histori():
    data = database.get_data()

    print("\n Transaction History")
    print("1. View income history")
    print("2. View expense history")
    print("3. View emergency fund history")
    print("4. View savings history")
    print("5. Financial Chart")
    print("0. Back to the main menu")

    pilih = input("Pilih histori: ")

    if pilih == "1":
        _histori_pemasukan(data)
    elif pilih == "2":
        _histori_pengeluaran(data)
    elif pilih == "3":
        _histori_emergency(data)
    elif pilih == "4":
        _histori_tabungan(data)
    elif pilih == "5":
        _grafik(data)
    elif pilih == "0":
        return None
    else:
        print(f"{Colors.RED} Invalid target choice!{Colors.ENDC}")