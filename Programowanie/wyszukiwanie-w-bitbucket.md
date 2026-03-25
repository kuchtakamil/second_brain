# Wyszukiwanie w Bitbucket

**Data:** 2025-08-11

---

**User:**

Wyszukiwarka na stronie bitbucket. Chciałbym poszukać wybranej frazy we wszystkich plikach *.java ale nie tych które kończą się na *Test.java

---

**Assistant:**

W Bitbucket (jeśli mówimy o wbudowanej wyszukiwarce kodu w interfejsie webowym), niestety **nie ma pełnej obsługi zaawansowanych wyrażeń w stylu grep** (np. `!` albo regex), więc bezpośrednio „wyszukaj we wszystkich plikach `.java` ale pomiń `*Test.java`” może być trudne.  
To, co możesz zrobić, zależy od wersji i konfiguracji Bitbucketa:

---

### 1. **Jeśli to Bitbucket Cloud (web)**
Wyszukiwarka działa podobnie do GitHubowej i pozwala używać ograniczeń typu:
```
fraza filename:.java
```
ale **nie ma natywnego „NOT” dla filename**. Możesz jedynie:
- Szukać po `.java` i ręcznie odfiltrować wyniki `*Test.java` w wynikach wyszukiwania.
- Lub użyć szerszego zapytania i później przefiltrować lokalnie (np. w IDE).

---

### 2. **Jeśli to Bitbucket Server/Data Center**
W zależności od tego, czy administrator włączył wyszukiwanie w oparciu o Elasticsearch, możliwe jest użycie składni Lucene. Wtedy zapytanie może wyglądać tak:
```
fraza AND filename:*.java NOT filename:*Test.java
```
albo
```
fraza filename:*.java -filename:*Test.java
```
(dokładna składnia zależy od wersji — trzeba sprawdzić w dokumentacji twojej instalacji Bitbucketa).

---

### 3. **Alternatywa — lokalnie przez `grep`**
Jeśli repo masz sklonowane:
```bash
grep -R "fraza" --include="*.java" --exclude="*Test.java" .
```
albo z ripgrep (`rg`):
```bash
rg "fraza" --glob "*.java" --glob "!*Test.java"
```
To jest znacznie szybsze niż czekanie na ograniczenia wyszukiwarki w UI.

---

Chcesz, żebym sprawdził w dokumentacji **dokładną składnię dla Bitbucket Server** i podał gotowy przykład pod twoją wersję?  
To by rozstrzygnęło, czy możesz to zrobić bezpośrednio w UI.