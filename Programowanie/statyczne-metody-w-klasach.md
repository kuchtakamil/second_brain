# Statyczne metody w klasach

**Data:** 2025-10-29

---

**User:**

wklejony poniżej fragmentkodu uznawany jest za napisany poprawnie
import re
from typing import Dict, Optional


class EmailValidator:
    """Single responsibility: Validate email addresses"""
    
    @staticmethod
    def validate(email: str) -> bool:
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


class PasswordValidator:
    """Single responsibility: Validate passwords"""
    
    @staticmethod
    def validate(password: str, min_length: int = 8) -> bool:
        return len(password) >= min_length


class UserRepository:
    """Single responsibility: Store and retrieve users"""
    
    def __init__(self):
        self._users: Dict[int, dict] = {}
        self._next_id = 1
    
    def save(self, email: str, password: str, name: str) -> int:
        user_id = self._next_id
        self._users[user_id] = {
            'email': email,
            'password': password,
            'name': name
        }
        self._next_id += 1
        return user_id
    
    def get_all(self) -> Dict[int, dict]:
        return self._users.copy()


class EmailService:
    """Single responsibility: Send emails"""
    
    def send_welcome_email(self, email: str, name: str):
        print(f"[EMAIL] Sending welcome email to {email}")
        print(f"   Welcome aboard, {name}!")


class UserActivityLogger:
    """Single responsibility: Log user activities"""
    
    def log_creation(self, user_id: int, email: str):
        print(f"[LOG] User {user_id} created with email {email}")


class UserService:
    """Orchestrates user creation - delegates to specialized services"""
    
    def __init__(self, repository: UserRepository, 
                 email_service: EmailService,
                 logger: UserActivityLogger):
        self.repository = repository
        self.email_service = email_service
        self.logger = logger
    
    def create_user(self, email: str, password: str, name: str) -> int:
        # Validate
        if not EmailValidator.validate(email):
            raise ValueError("Invalid email")
        if not PasswordValidator.validate(password):
            raise ValueError("Password too short")
        
        # Save
        user_id = self.repository.save(email, password, name)
        
        # Notify
        self.email_service.send_welcome_email(email, name)
        self.logger.log_creation(user_id, email)
        
        return user_id


class UserReportGenerator:
    """Single responsibility: Generate user reports"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def generate_summary(self) -> str:
        users = self.repository.get_all()
        report = f"Total users: {len(users)}\n"
        for uid, user in users.items():
            report += f"  {uid}: {user['email']}\n"
        return report


if __name__ == "__main__":
    # Setup - each component can be tested/replaced independently
    repository = UserRepository()
    email_service = EmailService()
    logger = UserActivityLogger()
    
    user_service = UserService(repository, email_service, logger)
    report_gen = UserReportGenerator(repository)
    
    # Use
    user_id = user_service.create_user("alice@example.com", "password123", "Alice")
    print(f"[OK] Created user: {user_id}\n")
    
    print(report_gen.generate_summary())
    
    print("\n[OK] BENEFITS:")
    print("- Each class has ONE reason to change")
    print("- Easy to test validators independently")
    print("- Can swap email service without touching other code")
    print("- Can reuse components in other contexts")

Powiedz na jakiej podstawie została podjęta decyzja aby metody w walidatorach (email i password) zrobić jako statyczne ale już metody w  EmailService i w klasie Loggera jako niestatyczne

---

**Assistant:**

Decyzja o tym, że metody w **EmailValidator** i **PasswordValidator** są **statyczne**, a w **EmailService** i **UserActivityLogger** — **niestatyczne**, wynika z różnicy w **charakterze odpowiedzialności** i **potrzebie stanu (state)** w tych klasach.  
Rozbijmy to dokładnie:

---

### 🧩 1. **Walidatory (EmailValidator, PasswordValidator) — metody statyczne**

**Dlaczego statyczne:**
- Walidacja jest **czysto funkcjonalna** — wynik zależy **tylko od argumentów wejściowych** (`email`, `password`), a nie od żadnego wewnętrznego stanu obiektu.
- Nie ma potrzeby tworzenia instancji klasy, bo nie ma tu **żadnego kontekstu ani konfiguracji**.
- To są w zasadzie **utility methods** — mogą być bezpiecznie wywołane zawsze w taki sam sposób, niezależnie od otoczenia.

**Efekt:**
- Prostsze użycie: `EmailValidator.validate(email)`
- Mniejszy narzut — nie trzeba tworzyć obiektu.
- Łatwiejsze testowanie jednostkowe — nie ma zależności.

📘 **Analogicznie:** takie klasy często można by nawet zastąpić modułowymi funkcjami (np. `validate_email(email)`).

---

### 📬 2. **EmailService i UserActivityLogger — metody niestatyczne**

**Dlaczego niestatyczne:**
- Te klasy reprezentują **serwisy z potencjalnym stanem lub zależnościami zewnętrznymi**, np.:
  - `EmailService` może w przyszłości wymagać połączenia SMTP, tokenu API, szablonów wiadomości, itp.
  - `UserActivityLogger` może logować do pliku, bazy danych, systemu zdalnego monitoringu.
- Dzięki metodom instancyjnym można **wstrzykiwać zależności (Dependency Injection)** i **mockować** obiekty w testach.
- To są elementy **infrastruktury**, a nie funkcje czysto obliczeniowe.

**Efekt:**
- Większa elastyczność i możliwość wymiany implementacji (np. `EmailService` → `SendGridEmailService`).
- Zgodność z zasadami SOLID, zwłaszcza z **Dependency Inversion Principle (DIP)**.

---

### 🧠 3. Podsumowanie różnicy

| Klasa | Typ metody | Powód |
|-------|-------------|-------|
| **EmailValidator** | statyczna | brak stanu, czysta funkcja |
| **PasswordValidator** | statyczna | brak stanu, czysta funkcja |
| **EmailService** | niestatyczna | potencjalny stan, zależności zewnętrzne |
| **UserActivityLogger** | niestatyczna | potencjalny stan, integracja z systemem logowania |

---

Czy chcesz, żebym pokazał, jak zmieniłaby się struktura projektu, **gdyby walidatory też były niestatyczne** (np. z Dependency Injection)? — mogę wtedy pokazać konsekwencje projektowe takiej decyzji.