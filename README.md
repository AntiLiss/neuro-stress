# Neuro-Stress

Backend-часть веб-приложения для оценки эмоционального состояния сотрудников на основе анализа ЭЭГ данных.

## 🧠 Описание

Система анализирует данные ЭЭГ и предоставляет аналитику по психофизиологическим показателям:
- **Валентность** - степень позитивности/негативности эмоционального состояния
- **Активность** - степень возбуждения нервной системы  
- **Релаксация** - степень расслабленности
- **Сонливость** - степень усталости
- **Стресс** - степень стрессового состояния
- **Концентрация** - степень сосредоточения

## 🏗️ Технологии

- Django + Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- drf-spectacular

## 🚀 Быстрый старт

```bash
git clone https://github.com/AntiLiss/neuro-stress.git
cd neuro-stress
docker compose up
```

Приложение будет доступно по адресу: http://localhost:8000  

Документация: http://localhost:8000/api/docs/

## 📚 API эндпониты

### Основные сущности
- `GET/POST /api/companies/` - Управление компаниями
- `GET/POST /api/departments/` - Управление отделами  
- `GET/POST /api/employees/` - Управление сотрудниками
- `GET/POST /api/eeg-records/` - Записи ЭЭГ
- `GET/POST /api/employee-reports/` - Отчеты по сотрудникам

### Фильтрация
- `GET /api/departments/?company=1` - Отделы компании
- `GET /api/employees/?department=1` - Сотрудники отдела
- `GET /api/eeg-records/?employee=1` - Записи сотрудника

### Пользователи
- `POST /api/users/` - Регистрация
- `POST /api/token/` - Получение JWT токена
- `POST /api/token/refresh/` - Обновление JWT токена
- `GET/PUT/DELETE /api/users/me/` - Управление профилем
