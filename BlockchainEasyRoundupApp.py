"""
Author: Hayate Esaki by GrowthLink (Arterect)
Date: 2023/09/10
Description: Blockchain Basics [Introductory] Code
Ver: 1.0.0

"""

import hashlib
import time
import tkinter as tk
from tkinter import simpledialog, messagebox

# ブロックを表現するクラス
class Block:
    def __init__(self, index, previous_hash, timestamp, transaction, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transaction = transaction
        self.hash = hash

# ハッシュを計算する関数
def calculate_hash(index, previous_hash, timestamp, transaction):
    return hashlib.sha256(f'{index}{previous_hash}{timestamp}{transaction}'.encode('utf-8')).hexdigest()

# ジェネシスブロック（最初のブロック）を作成する関数
def create_genesis_block():
    return Block(0, '0', time.time(), "初期トランザクション", calculate_hash(0, '0', time.time(), "初期トランザクション"))

# ブロックチェーンを初期化。最初はジェネシスブロックのみ。
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# ユーザ情報
user_info = {
    "name": "グロース君",
    "level": 2,
    "money": 10000,
}

# 商品のリスト
products = {
    1: {"name": "りんご", "price": 100},
    2: {"name": "ブロックチェーンの基本 [入門]", "price": 4000},
    3: {"name": "成長の木", "price": 8800}
}

def update_status():
    status_name.set(f"名前: {user_info['name']}".ljust(30))
    status_level.set(f"レベル: {user_info['level']}".ljust(30))
    status_money.set(f"現在のお金: {user_info['money']} GTC (GrowthCoin)".ljust(30))

# ユーザーの購入を処理する関数
def user_purchase():
    global previous_block

    product_str = "どれを購入しますか？\n"
    for key, value in products.items():
        product_str += f"{key}. {value['name']} {value['price']} GTC\n"

    chosen_number = simpledialog.askinteger("商品選択", product_str)

    if chosen_number not in products:
        messagebox.showerror("エラー", "正しい番号を入力してください")
        return

    chosen_product = products[chosen_number]["name"]
    amount = products[chosen_number]["price"]

    # 残高チェック
    if user_info['money'] < amount:
        messagebox.showerror("エラー", "所持金額が足りません")
        return

    user_info['money'] -= amount  # 所持金から購入額を引く
    transaction = f"ユーザーが{chosen_product}を購入し、{amount}GTC支払いました。残高は{user_info['money']}GTCです。"
    messagebox.showinfo("購入完了", transaction)

    new_block = Block(len(blockchain), previous_block.hash, time.time(), transaction, calculate_hash(len(blockchain), previous_block.hash, time.time(), transaction))
    blockchain.append(new_block)
    previous_block = new_block
    messagebox.showinfo("情報", f"ブロック#{new_block.index}がブロックチェーンに追加されました!")
    blockchain_history.insert(tk.END, f"ブロック#{new_block.index}: {transaction}")  # 新しいブロックの情報をListboxに追加

    update_status()  # ステータス更新

    choice = messagebox.askyesno("確認", "トランザクションを続行しますか？")

    if not choice:
        app.quit()  # アプリを終了


# GUIアプリの初期化
app = tk.Tk()
app.title("ブロックチェーン簡単丸わかりアプリ")

# ステータスの表示部分
status_name = tk.StringVar()
status_name_label = tk.Label(app, textvariable=status_name, anchor="w")
status_name_label.pack(pady=5, fill=tk.X)

status_level = tk.StringVar()
status_level_label = tk.Label(app, textvariable=status_level, anchor="w")
status_level_label.pack(pady=5, fill=tk.X)

status_money = tk.StringVar()
status_money_label = tk.Label(app, textvariable=status_money, anchor="w")
status_money_label.pack(pady=5, fill=tk.X)

# ブロックチェーンの履歴
history_label = tk.Label(app, text="ブロックチェーンの履歴")
history_label.pack(pady=10)
blockchain_history = tk.Listbox(app, width=80, height=10)
blockchain_history.pack(pady=20)

update_status()  # 初期ステータスの表示

purchase_button = tk.Button(app, text="ショッピング", command=user_purchase)
purchase_button.pack(pady=20)

app.mainloop()