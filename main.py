import csv
import time
import os.path


# Функция создания заметки
def create_note():
    title = input("Введите заголовок заметки: ")
    content = input("Введите содержание заметки: ")
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    note = {"id": get_next_id(), "title": title, "content": content, "created_at": created_at}
    return note


# Функция сохранения заметки в файл CSV
def save_note_to_csv(note):
    with open("notes.csv", mode="a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "title", "content", "created_at"])
        writer.writerow(note)


# Функция получения списка заметок из файла CSV
def read_notes_from_csv():
    notes = []
    with open("notes.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            notes.append(row)
    return notes


# Функция создания файла CSV для хранения заметок
def create_csv_file():
    with open("notes.csv", mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "title", "content", "created_at"])
        writer.writeheader()


# Функция получения следующего id для заметки
def get_next_id():
    notes = read_notes_from_csv()
    if not notes:
        return 1
    return int(notes[-1]["id"]) + 1


# Функция вывода списка заметок с их идентификаторами
def list_notes():
    notes = read_notes_from_csv()
    if not notes:
        print("Список заметок пуст.")
        return
    print("Список заметок:")
    for note in notes:
        print(f"{note['id']}. {note['title']}")
        print(note['content'])
        print(note['created_at'])
        print("=" * 30)


# Функция удаления заметки

def delete_note_by_id(note_id):
    # получаем список всех заметок из файла
    notes = read_notes_from_csv()

    # находим индекс заметки с указанным id
    index_to_remove = -1
    for i, note in enumerate(notes):
        if note["id"] == str(note_id):
            index_to_remove = i
            break

    if index_to_remove == -1:
        print(f"Заметка с id {note_id} не найдена.")
        return

    # удаляем заметку из списка
    notes.pop(index_to_remove)

    # перезаписываем файл
    with open("notes.csv", mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "title", "content", "created_at"])
        writer.writeheader()
        writer.writerows(notes)

    print(f"Заметка с id {note_id} удалена.")

# Функция редактирования заметки по ID
def edit_note_by_id():
    id_to_edit = input("Введите ID заметки для редактирования: ")
    notes = read_notes_from_csv()
    for note in notes:
        if note["id"] == id_to_edit:
            new_title = input(f"Введите новый заголовок для заметки (старый: {note['title']}): ")
            new_content = input(f"Введите новое содержание для заметки (старое: {note['content']}): ")
            note["title"] = new_title
            note["content"] = new_content
            note["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

            with open("notes.csv", mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "title", "content", "created_at", "updated_at"])
                writer.writeheader()
                writer.writerows(notes)

            print(f"Заметка с id {id_to_edit} успешно изменена.")
            return

    print(f"Заметка с id {id_to_edit} не найдена.")


# Основной код программы
if not os.path.isfile("notes.csv"):
    create_csv_file()

while True:
    print("1. Создать заметку")
    print("2. Список заметок")
    print("3. Удаление заметок по id")
    print("4. Редактирование заметки")
    print("5. Выход")
    choice = input("Выберите действие: ")
    if choice == "1":
        note = create_note()
        save_note_to_csv(note)
        print("Заметка сохранена.")
    elif choice == "2":
        list_notes()
    elif choice == '3':
        note_id = input("Введите id заметки, которую нужно удалить: ")
        delete_note_by_id(note_id)
    elif choice == "4":
        edit_note_by_id()
    elif choice == '5':
        break
    else:
        print("Некорректный ввод. Попробуйте еще раз.")
