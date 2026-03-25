# Biblioteka AWS w Pythonie

**Data:** 2026-02-07

---

**User:**

najpopularniejsza biblioteka klienta AWS w Pythonie to ...

---

**Assistant:**

Najpopularniejsza i **de facto standardowa** biblioteka klienta AWS w Pythonie to:

**boto3**

To jest oficjalny AWS SDK dla Pythona.

---

### Dlaczego właśnie boto3

- rozwijana i utrzymywana bezpośrednio przez AWS
- pełne pokrycie praktycznie wszystkich usług AWS
- aktualizowana natychmiast wraz z nowymi API
- używana w dokumentacji, przykładach i narzędziach AWS
- bazuje na niskopoziomowym `botocore`
- wspiera:
  - clients (niskopoziomowe API 1:1 z AWS)
  - resources (wyższy poziom abstrakcji, bardziej „pythonic”)

---

### Typowy usage

```python
import boto3

s3 = boto3.client("s3")
response = s3.list_buckets()
print(response)
```

lub wyższy poziom:

```python
s3 = boto3.resource("s3")
for bucket in s3.buckets.all():
    print(bucket.name)
```

---

### Co jeszcze warto wiedzieć (praktycznie)

W realnych projektach często używa się razem:

- `boto3` — SDK
- `botocore.exceptions` — obsługa błędów
- `moto` — mockowanie AWS w testach
- `awscli` używa dokładnie tego samego backendu (`botocore`)

---

Jeśli ktoś w Pythonie mówi „AWS SDK”, to **wszyscy rozumieją: boto3**.

---

**User:**

czy kiedyś była wersja boto2?

---

**Assistant:**

Tak. **Była — i była bardzo popularna.**

Nazywała się po prostu:

**boto** (dziś nieformalnie: *boto2*)

---

### Oś czasu

| Okres | Biblioteka | Status |
|---|---|---|
| ~2006–2015 | `boto` | oficjalne AWS SDK dla Pythona (v2) |
| 2015 → dziś | `boto3` | następca, całkowite przepisanie |

`boto3` **nie jest ewolucją** `boto`.  
To był **pełny rewrite od zera** oparty o nową architekturę: **botocore + generowanie klientów z definicji API AWS**.

---

### Dlaczego powstało boto3

`boto` miało poważne problemy architektoniczne:

- ręcznie pisane wsparcie dla usług → wolne tempo dodawania nowych AWS services
- niespójne API między usługami
- dużo „magii”, mało przewidywalności
- trudne do utrzymania przy szybkim rozroście AWS

AWS zmienił podejście:

> Zamiast pisać SDK ręcznie → generujemy je z modeli API.

To właśnie robi **botocore**, na którym stoi `boto3`.

---

### Jak wyglądało boto (v2)

Przykład S3 w boto:

```python
import boto

conn = boto.connect_s3()
for bucket in conn.get_all_buckets():
    print(bucket.name)
```

Brak:
- spójności
- clients/resources
- przewidywalnego API jak w boto3

---

### Status dziś

- `boto` jest **deprecated**
- AWS oficjalnie zaleca migrację od wielu lat
- praktycznie nieużywane w nowych projektach
- spotykane tylko w **starych legacy systemach**

---

### Ciekawostka

Nazwa **boto3** nie oznaczała „mały upgrade”.

W praktyce znaczyło:

> *To jest trzecia próba zrobienia SDK do AWS w Pythonie, tym razem dobrze.*

Dlatego przeskok numeracji był celowy.