# Dostęp do bazy danych

**Data:** 2025-07-30

---

**User:**

jestem programistą java i jestem przyzwyczajony do tego że jak czytam coś z bazy danych to dostaję gotowe struktury danych. Czy w pythonie jest podobnie czy dostaję jedynie dostęp do cursora którym można chodzić po danych?

---

**Assistant:**

W Pythonie – tak jak w Javie – możesz pracować z bazą danych na różne sposoby, a to, czy dostajesz gotowe struktury danych czy tylko „surowy” kursor, zależy od wybranej biblioteki i poziomu abstrakcji, na którym chcesz działać.

### 1. **Surowy dostęp (np. `sqlite3`, `psycopg2`, `mysql-connector`)**
Tutaj **dostajesz kursor**, którym możesz iterować po wynikach zapytania. Każdy wiersz to zazwyczaj **krotka (tuple)** lub **słownik (dict)**, w zależności od konfiguracji.

Przykład (SQLite, standardowa biblioteka):

```python
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('SELECT id, name FROM users')

for row in cursor.fetchall():
    print(row)  # np. (1, 'Jan')
```

Można też ustawić `row_factory`, by dostawać słowniki:

```python
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
rows = cursor.execute('SELECT * FROM users')
for row in rows:
    print(dict(row))  # {'id': 1, 'name': 'Jan'}
```

### 2. **Wyższy poziom – biblioteki ORM**

Jeśli chcesz mieć **obiekty zamiast surowych danych**, tak jak w Javie z JPA/Hibernate, to użyj ORM-a. W Pythonie najpopularniejszy to:

- **SQLAlchemy** – dominujący standard, bardzo rozbudowany.
- **Django ORM** – część frameworka Django, ale można użyć samodzielnie.
- **Tortoise ORM**, **Pony ORM** – inne alternatywy.

#### Przykład z SQLAlchemy (w stylu JPA):

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine('sqlite:///test.db')
Session = sessionmaker(bind=engine)
session = Session()

users = session.query(User).all()
for user in users:
    print(user.id, user.name)
```

Tu dostajesz już obiekty `User`, jak w Javie obiekty encyjne.

---

### Podsumowanie

- Jeśli używasz `sqlite3`, `psycopg2` itd. – masz **kursor** i **krotki/słowniki**.
- Jeśli chcesz **struktury danych / obiekty**, użyj **ORM-a** – np. SQLAlchemy.
- W Pythonie masz swobodę wyboru poziomu abstrakcji – od surowych zapytań do pełnych ORM-ów, jak w Javie.

Jeśli chcesz, mogę podpowiedzieć konkretną bibliotekę w zależności od tego, czy robisz coś lekkiego, skryptowego, czy bardziej złożony backend.