import os
import pyodbc

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=REZA-LAPTOP;'
    r'DATABASE=PersonalTasksDB;'
    r'TRUSTED_CONNECTION=yes;'
    r'TrustServerCertificate=yes;'
)


def connect_db():
    try:
        return pyodbc.connect(conn_str)
    except Exception as e:
        print(f"خطا در اتصال به دیتابیس: {e}")
        return None


def execute_query(conn, query, params=None, select=False, many=False):
    cursor = conn.cursor()
    try:
        if many and params:
            cursor.fast_executemany = True
            cursor.executemany(query, params)
        elif params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if select:
            return cursor.fetchall()

        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"خطا در اجرای کوئری: {e}")
        return None
    finally:
        try:
            cursor.close()
        except Exception:
            pass


def main_menu():
    print("\n--- سامانه مدیریت کارهای شخصی ---")
    print("1. مدیریت کاربران (Users)")
    print("2. مدیریت پروژه‌ها (Projects)")
    print("3. مدیریت وظایف (Tasks)")
    print("4. مدیریت برچسب‌ها (Tags)")
    print("5. مدیریت روابط وظایف و برچسب‌ها (TaskTags)")
    print("6. مدیریت یادآورها (Reminders)")
    print("7. خروج")
    return input("انتخاب کنید: ")


def crud_menu(table_name):
    print(f"\n--- عملیات روی جدول {table_name} ---")
    print("1. افزودن رکورد (INSERT)")
    print("2. نمایش رکوردها (SELECT)")
    print("3. ویرایش رکورد (UPDATE)")
    print("4. حذف رکورد (DELETE)")
    print("5. بازگشت به منوی اصلی")
    return input("انتخاب کنید: ")


def _to_int(value):
    try:
        return int(value)
    except Exception:
        return None


def _print_rows(rows):
    if not rows:
        print("نتیجه‌ای یافت نشد.")
        return
    for row in rows:
        print(row)


def manage_users(conn):
    choice = crud_menu("Users")
    if choice == '1':
        username = input("نام کاربری: ")
        email = input("ایمیل: ")
        password = input("رمز عبور: ")
        query = "INSERT INTO Users (username, email, password) VALUES (?, ?, ?)"
        execute_query(conn, query, (username, email, password))
    elif choice == '2':
        query = "SELECT * FROM Users"
        results = execute_query(conn, query, select=True)
        _print_rows(results)
    elif choice == '3':
        user_id = _to_int(input("ID کاربر برای ویرایش: "))
        if user_id is None:
            print("ID نامعتبر")
            return
        new_email = input("ایمیل جدید: ")
        query = "UPDATE Users SET email = ? WHERE user_id = ?"
        execute_query(conn, query, (new_email, user_id))
    elif choice == '4':
        user_id = _to_int(input("ID کاربر برای حذف: "))
        if user_id is None:
            print("ID نامعتبر")
            return
        query = "DELETE FROM Users WHERE user_id = ?"
        execute_query(conn, query, (user_id,))


def manage_projects(conn):
    choice = crud_menu("Projects")
    if choice == '1':
        user_id = _to_int(input("ID کاربر: "))
        name = input("نام پروژه: ")
        description = input("توضیحات: ")
        due_date = input("تاریخ پایان (YYYY-MM-DD): ")
        status = input("وضعیت (not_started, in_progress, etc.): ")
        query = "INSERT INTO Projects (user_id, name, description, due_date, status) VALUES (?, ?, ?, ?, ?)"
        execute_query(conn, query, (user_id, name, description, due_date, status))
    elif choice == '2':
        query = "SELECT * FROM Projects"
        results = execute_query(conn, query, select=True)
        _print_rows(results)
    elif choice == '3':
        project_id = _to_int(input("ID پروژه برای ویرایش: "))
        if project_id is None:
            print("ID نامعتبر")
            return
        new_status = input("وضعیت جدید: ")
        query = "UPDATE Projects SET status = ? WHERE project_id = ?"
        execute_query(conn, query, (new_status, project_id))
    elif choice == '4':
        project_id = _to_int(input("ID پروژه برای حذف: "))
        if project_id is None:
            print("ID نامعتبر")
            return
        query = "DELETE FROM Projects WHERE project_id = ?"
        execute_query(conn, query, (project_id,))


def manage_tasks(conn):
    choice = crud_menu("Tasks")
    if choice == '1':
        project_id_input = input("ID پروژه (اختیاری، خالی برای NULL): ")
        project_id = _to_int(project_id_input) if project_id_input.strip() else None
        user_id = _to_int(input("ID کاربر: "))
        if user_id is None:
            print("ID کاربر نامعتبر")
            return
        title = input("عنوان وظیفه: ")
        description = input("توضیحات: ")
        start_date = input("تاریخ شروع (YYYY-MM-DD): ")
        due_date = input("تاریخ پایان (YYYY-MM-DD): ")
        status = input("وضعیت: ")
        priority = input("اولویت (low, medium, high): ")
        query = "INSERT INTO Tasks (project_id, user_id, title, description, start_date, due_date, status, priority) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        execute_query(conn, query, (project_id, user_id, title, description, start_date, due_date, status, priority))
    elif choice == '2':
        query = "SELECT * FROM Tasks"
        results = execute_query(conn, query, select=True)
        _print_rows(results)
    elif choice == '3':
        task_id = _to_int(input("ID وظیفه برای ویرایش: "))
        if task_id is None:
            print("ID نامعتبر")
            return
        new_status = input("وضعیت جدید: ")
        query = "UPDATE Tasks SET status = ? WHERE task_id = ?"
        execute_query(conn, query, (new_status, task_id))
    elif choice == '4':
        task_id = _to_int(input("ID وظیفه برای حذف: "))
        if task_id is None:
            print("ID نامعتبر")
            return
        query = "DELETE FROM Tasks WHERE task_id = ?"
        execute_query(conn, query, (task_id,))


def manage_tags(conn):
    choice = crud_menu("Tags")
    if choice == '1':
        user_id = _to_int(input("ID کاربر: "))
        name = input("نام برچسب: ")
        color = input("رنگ (hex): ")
        query = "INSERT INTO Tags (user_id, name, color) VALUES (?, ?, ?)"
        execute_query(conn, query, (user_id, name, color))
    elif choice == '2':
        query = "SELECT * FROM Tags"
        results = execute_query(conn, query, select=True)
        _print_rows(results)
    elif choice == '3':
        tag_id = _to_int(input("ID برچسب برای ویرایش: "))
        if tag_id is None:
            print("ID نامعتبر")
            return
        new_color = input("رنگ جدید: ")
        query = "UPDATE Tags SET color = ? WHERE tag_id = ?"
        execute_query(conn, query, (new_color, tag_id))
    elif choice == '4':
        tag_id = _to_int(input("ID برچسب برای حذف: "))
        if tag_id is None:
            print("ID نامعتبر")
            return
        query = "DELETE FROM Tags WHERE tag_id = ?"
        execute_query(conn, query, (tag_id,))


def manage_task_tags(conn):
    choice = crud_menu("TaskTags")
    if choice == '1':
        task_id = _to_int(input("ID وظیفه: "))
        tag_id = _to_int(input("ID برچسب: "))
        if task_id is None or tag_id is None:
            print("ID نامعتبر")
            return
        query = "INSERT INTO TaskTags (task_id, tag_id) VALUES (?, ?)"
        execute_query(conn, query, (task_id, tag_id))
    elif choice == '2':
        query = "SELECT * FROM TaskTags"
        results = execute_query(conn, query, select=True)
        _print_rows(results)
    elif choice == '3':
        task_id = _to_int(input("ID وظیفه: "))
        old_tag_id = _to_int(input("ID برچسب قدیمی: "))
        new_tag_id = _to_int(input("ID برچسب جدید: "))
        if None in (task_id, old_tag_id, new_tag_id):
            print("ID نامعتبر")
            return
        query = "UPDATE TaskTags SET tag_id = ? WHERE task_id = ? AND tag_id = ?"
        execute_query(conn, query, (new_tag_id, task_id, old_tag_id))
    elif choice == '4':
        task_id = _to_int(input("ID وظیفه: "))
        tag_id = _to_int(input("ID برچسب برای حذف: "))
        if task_id is None or tag_id is None:
            print("ID نامعتبر")
            return
        query = "DELETE FROM TaskTags WHERE task_id = ? AND tag_id = ?"
        execute_query(conn, query, (task_id, tag_id))


def manage_reminders(conn):
    choice = crud_menu("Reminders")
    if choice == '1':
        task_id = _to_int(input("ID وظیفه: "))
        if task_id is None:
            print("ID نامعتبر")
            return
        remind_time = input("زمان یادآوری (YYYY-MM-DD HH:MM): ")
        repeat_pattern = input("الگوی تکرار (اختیاری): ")
        notes = input("یادداشت‌ها: ")
        query = "INSERT INTO Reminders (task_id, remind_time, repeat_pattern, notes) VALUES (?, ?, ?, ?)"
        execute_query(conn, query, (task_id, remind_time, repeat_pattern, notes))
    elif choice == '2':
        query = "SELECT * FROM Reminders"
        results = execute_query(conn, query, select=True)
        _print_rows(results)
    elif choice == '3':
        reminder_id = _to_int(input("ID یادآوری برای ویرایش: "))
        if reminder_id is None:
            print("ID نامعتبر")
            return
        new_remind_time = input("زمان جدید: ")
        query = "UPDATE Reminders SET remind_time = ? WHERE reminder_id = ?"
        execute_query(conn, query, (new_remind_time, reminder_id))
    elif choice == '4':
        reminder_id = _to_int(input("ID یادآوری برای حذف: "))
        if reminder_id is None:
            print("ID نامعتبر")
            return
        query = "DELETE FROM Reminders WHERE reminder_id = ?"
        execute_query(conn, query, (reminder_id,))


if __name__ == '__main__':
    conn = connect_db()
    if not conn:
        print("نمی‌توان به دیتابیس متصل شد.")
    else:
        try:
            while True:
                choice = main_menu()
                if choice == '1':
                    manage_users(conn)
                elif choice == '2':
                    manage_projects(conn)
                elif choice == '3':
                    manage_tasks(conn)
                elif choice == '4':
                    manage_tags(conn)
                elif choice == '5':
                    manage_task_tags(conn)
                elif choice == '6':
                    manage_reminders(conn)
                elif choice == '7':
                    print("خروج از برنامه.")
                    break
        finally:
            try:
                conn.close()
            except Exception:
                pass