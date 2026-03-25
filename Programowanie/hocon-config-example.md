# HOCON Config Example.

**Data:** 2023-03-31

---

**User:**

Wygeneruj skomplikowany dowolny plik konfiguracyjny w formacie HOCON

---

**Assistant:**

Oto przykładowy plik konfiguracyjny w formacie HOCON:

```
{
  server {
    host = "localhost"
    port = 8080
    ssl {
      enabled = true
      key-store = "/path/to/keystore"
      key-store-password = "mysecretpassword"
    }
    database {
      url = "jdbc:mysql://localhost:3306/mydb"
      username = "myuser"
      password = "mypassword"
    }
  }
  logging {
    level = "INFO"
    console {
      enabled = true
      pattern = "[%d{HH:mm:ss}] [%level] %message%n"
    }
    file {
      enabled = false
      path = "/var/log/myapp.log"
      max-size = 10MB
      max-history = 5
    }
  }
  security {
    jwt {
      secret = "myjwtsecret"
      expiration-time = 1 hour
      refresh-token-expiration-time = 1 week
    }
    cors {
      allowed-origins = ["https://example.com", "https://www.example.com"]
      allowed-methods = ["GET", "POST", "PUT", "DELETE"]
      allowed-headers = ["Authorization", "Content-Type"]
      allow-credentials = true
      max-age = 86400
    }
  }
}
```

Ten plik konfiguracyjny definiuje serwer HTTP, który słucha na porcie 8080 i wymaga uwierzytelnienia JWT. Serwer używa bazy danych MySQL do przechowywania informacji o użytkownikach. Logowanie odbywa się na poziomie "INFO" i może być zapisywane na konsoli lub w pliku, który ma rozmiar do 10 MB i maksymalnie 5 archiwów. Dodatkowo, serwer jest skonfigurowany, aby obsługiwał CORS, co umożliwia udostępnianie danych między różnymi domenami.