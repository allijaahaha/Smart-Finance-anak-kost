import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")          
DATA_USER_FILE = os.path.join(DATA_DIR, "data_user.json")  

POTONGAN_EMERGENCY_DEFAULT = 5000
SALDO_MINIMUM_PERINGATAN = 50000
BATAS_AMBIL_EMERGENCY = 100000

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'