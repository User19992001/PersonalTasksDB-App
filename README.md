# PersonalTasksDB-App

این اپلیکیشن ساده کنسول با پایتون برای مدیریت دیتابیس "سامانه مدیریت کارهای شخصی" طراحی شده. عملیات CRUD روی جداول Users, Projects, Tasks, Tags, Reminders, TaskTags را انجام می‌دهد.

## پیش‌نیازها
- Python 3
- کتابخانه pyodbc (pip install pyodbc)
- SQL Server با دیتابیس PersonalTasksDB

## نصب و اجرا
1. کد را دانلود کنید.
2. تنظیمات اتصال در main.py را با سرور خود ویرایش کنید.
3. اجرا: python main.py

## ساختار
- main.py: کد اصلی با منوهای کنسول.
- اتصال به SQL Server با pyodbc.

## محدودیت‌ها
- بدون GUI، فقط کنسول.
- خطاها مدیریت می‌شوند.
