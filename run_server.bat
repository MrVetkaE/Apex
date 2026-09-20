@echo off
chcp 65001 > nul
echo ===================================================
echo     ⚡ APEX NUTRITION - Сервер Django запущен!
echo ===================================================
echo.
echo   🌐 Сайт доступен по адресу: http://127.0.0.1:8000/
echo   🛡️ Админ-панель:          http://127.0.0.1:8000/admin/
echo   🔑 Логин админа:          admin
echo   🔒 Пароль админа:         admin123
echo.
echo ===================================================
echo Для остановки нажмите Ctrl + C
echo.
python manage.py runserver 127.0.0.1:8000
pause
