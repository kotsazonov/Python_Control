import json
import argparse
from datetime import datetime

NOTES_FILE = "notes.json"

def load_notes():
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = []
    return notes

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)

def add_note(title, body):
    notes = load_notes()
    note = {
        "id": len(notes) + 1,
        "title": title,
        "body": body,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes.append(note)
    save_notes(notes)
    print("Заметка успешно сохранена.")

def list_notes():
    notes = load_notes()
    if notes:
        print("Список заметок:")
        for note in notes:
            print(f"ID: {note['id']}, Заголовок: {note['title']}, Дата/Время: {note['timestamp']}")
    else:
        print("Список заметок пуст.")

def read_note_by_date(date_str):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Некорректный формат даты. Используйте формат YYYY-MM-DD.")
        return

    notes = load_notes()
    filtered_notes = [note for note in notes if datetime.strptime(note["timestamp"], "%Y-%m-%d %H:%M:%S").date() == target_date]

    if filtered_notes:
        print(f"Заметки за {date_str}:")
        for note in filtered_notes:
            print(f"ID: {note['id']}, Заголовок: {note['title']}, Дата/Время: {note['timestamp']}")
    else:
        print(f"Заметок за {date_str} не найдено.")

def edit_note(note_id, title, body):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["body"] = body
            note["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes(notes)
            print(f"Заметка с ID {note_id} успешно отредактирована.")
            return
    print(f"Заметка с ID {note_id} не найдена.")

def delete_note(note_id):
    notes = load_notes()
    new_notes = [note for note in notes if note["id"] != note_id]
    if len(new_notes) < len(notes):
        save_notes(new_notes)
        print(f"Заметка с ID {note_id} успешно удалена.")
    else:
        print(f"Заметка с ID {note_id} не найдена.")

def main():
    parser = argparse.ArgumentParser(description="Консольное приложение для управления заметками")
    parser.add_argument("command", nargs="?", choices=["add", "list", "read", "edit", "delete"], help="Команда для выполнения")
    parser.add_argument("--id", type=int, help="ID заметки")
    parser.add_argument("--title", help="Заголовок заметки")
    parser.add_argument("--msg", help="Тело заметки")
    parser.add_argument("--date", help="Дата для фильтрации записей (формат: YYYY-MM-DD)")

    args = parser.parse_args()

    if args.command == "add":
        if args.title and args.msg:
            add_note(args.title, args.msg)
        else:
            print("Для добавления заметки необходимо указать заголовок (--title) и тело (--msg).")
    elif args.command == "list":
        list_notes()
    elif args.command == "read":
        if args.date:
            read_note_by_date(args.date)
        else:
            print("Для чтения заметок по дате необходимо указать параметр --date.")
    elif args.command == "edit":
        if args.id and args.title and args.msg:
            edit_note(args.id, args.title, args.msg)
        else:
            print("Для редактирования заметки необходимо указать ID (--id), заголовок (--title) и тело (--msg).")
    elif args.command == "delete":
        if args.id:
            delete_note(args.id)
        else:
            print("Для удаления заметки необходимо указать ID (--id).")

if __name__ == "__main__":
    main()