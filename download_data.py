import os
import shutil

RAW_NAME = "default_of_credit_card_clients.csv"
SRC_PATH = RAW_NAME
DST_DIR = "data"
DST_PATH = os.path.join(DST_DIR, RAW_NAME)


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    if not os.path.exists(SRC_PATH):
        raise FileNotFoundError(f"Файл {SRC_PATH} не найден."f"Скачай датасет и положи его в корень проекта под этим именем.")
    shutil.copy2(SRC_PATH, DST_PATH)
    print(f"Dataset copied to {DST_PATH}")


if __name__ == "__main__":
    main()