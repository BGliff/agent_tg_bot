# agent_tg_bot
Это небольшое тестовое задание

Для запуска проекта:
1) .\venv\Scripts\activate
2) pip install -r .\requirements.txt
3) cd .\src
4) python core.py

Для запуска тестов:
1) cd .\src
2) pytest .\tests

Сборка и запуск Docker-контейнера
1) docker build -t agent-tg-bot-image .
2) docker run -d -p 443:443 agent-tg-bot-image python core.py
