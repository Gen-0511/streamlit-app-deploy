# library_manage.py

books = []
members = []
borrow_records = []

# 共通関数
def find_book(book_id):
    return next((book for book in books if book["book_id"] == book_id), None)

def find_member(member_id):
    return next((member for member in members if member["member_id"] == member_id), None)

# Copilot提案による新規関数
def search_books_by_title(keyword):
    print(f"🔍 タイトルに「{keyword}」を含む図書を検索します...")
    found = False
    for book in books:
        if keyword.lower() in book["title"].lower():
            print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 在庫: {book['available_copies']}")
            found = True
    if not found:
        print("❌ 該当する図書は見つかりませんでした。")

def add_book(book_id, title, author, copies):
    if find_book(book_id):
        print(f"⚠️ 図書ID「{book_id}」は既に存在します。")
        return
    books.append({"book_id": book_id, "title": title, "author": author, "copies": copies, "available_copies": copies})
    print(f"✅ 図書「{title}」を追加しました。")

def list_books():
    if not books:
        print("📚 現在、登録されている図書はありません。")
        return
    print("--- 図書一覧 ---")
    for book in books:
        print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")

def search_book(book_id):
    book = find_book(book_id)
    if book:
        print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")
    else:
        print(f"❌ 図書ID「{book_id}」は存在しません。")

def add_member(member_id, name):
    if find_member(member_id):
        print(f"⚠️ 会員ID「{member_id}」は既に存在します。")
        return
    members.append({"member_id": member_id, "name": name})
    print(f"✅ 会員「{name}」を追加しました。")

def list_members():
    if not members:
        print("👥 現在、登録されている会員はいません。")
        return
    print("--- 会員一覧 ---")
    for member in members:
        print(f"ID: {member['member_id']}, 名前: {member['name']}")

def borrow_book(book_id, member_id):
    book = find_book(book_id)
    member = find_member(member_id)

    if not book:
        print(f"❌ 図書ID「{book_id}」は存在しません。")
        return
    if not member:
        print(f"❌ 会員ID「{member_id}」は存在しません。")
        return
    if book["available_copies"] <= 0:
        print(f"⚠️ 図書「{book['title']}」は現在貸出可能な冊数がありません。")
        return

    count = sum(1 for record in borrow_records if record["member_id"] == member_id and not record["returned"])
    if count >= 5:
        print(f"⚠️ 会員「{member['name']}」の貸出上限（5冊）に達しています。")
        return

    borrow_records.append({
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": "2024-11-24",
        "due_date": "2024-12-01",
        "returned": False
    })
    book["available_copies"] -= 1
    print(f"📕 図書「{book['title']}」を会員「{member['name']}」に貸し出しました。返却期限: 2024-12-01")

def list_borrowed_books():
    print("--- 貸出中の図書一覧 ---")
    found = False
    for record in borrow_records:
        if not record["returned"]:
            book = find_book(record["book_id"])
            member = find_member(record["member_id"])
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}")
            found = True
    if not found:
        print("📭 現在、貸出中の図書はありません。")

def return_book(book_id, member_id):
    for record in borrow_records:
        if record["book_id"] == book_id and record["member_id"] == member_id and not record["returned"]:
            record["returned"] = True
            book = find_book(book_id)
            if book:
                book["available_copies"] += 1
                print(f"📗 図書「{book['title']}」が返却されました。")
            return
    print(f"❌ 会員ID「{member_id}」は図書ID「{book_id}」を借りていません。")

def calculate_fines():
    print("--- 延滞料金一覧 ---")
    today = 24  # 日付の簡略化（2024-12-24の「24」）
    due = 1     # 返却期限（2024-12-01の「1」）
    found = False
    for record in borrow_records:
        if not record["returned"]:
            overdue_days = max(today - due, 0)
            fine = overdue_days * 100
            book = find_book(record["book_id"])
            member = find_member(record["member_id"])
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 延滞料金: {fine}円")
            found = True
    if not found:
        print("📭 現在、延滞中の図書はありません。")

def main():
    while True:
        print("\n📘 図書館管理システムメニュー:")
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書をIDで検索")
        print("4: タイトルキーワードで検索")  # ← 新機能メニュー
        print("5: 会員を追加")
        print("6: 会員一覧を表示")
        print("7: 図書を貸し出す")
        print("8: 貸出中の図書一覧を表示")
        print("9: 図書を返却")
        print("10: 延滞料金を計算")
        print("11: 終了")

        try:
            choice = int(input("操作を選択してください（1-11）: "))

            if choice == 1:
                book_id = input("図書ID: ")
                title = input("タイトル: ")
                author = input("著者名: ")
                copies = int(input("冊数: "))
                add_book(book_id, title, author, copies)

            elif choice == 2:
                list_books()

            elif choice == 3:
                book_id = input("検索したい図書ID: ")
                search_book(book_id)

            elif choice == 4:
                keyword = input("検索キーワード: ")
                search_books_by_title(keyword)

            elif choice == 5:
                member_id = input("会員ID: ")
                name = input("名前: ")
                add_member(member_id, name)

            elif choice == 6:
                list_members()

            elif choice == 7:
                book_id = input("貸出図書ID: ")
                member_id = input("会員ID: ")
                borrow_book(book_id, member_id)

            elif choice == 8:
                list_borrowed_books()

            elif choice == 9:
                book_id = input("返却図書ID: ")
                member_id = input("会員ID: ")
                return_book(book_id, member_id)

            elif choice == 10:
                calculate_fines()

            elif choice == 11:
                print("📕 システムを終了します。")
                break

            else:
                print("⚠️ 無効な選択です。1～11を入力してください。")

        except ValueError:
            print("⚠️ 入力は数字でお願いします。")
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")

if __name__ == "__main__":
    main()
