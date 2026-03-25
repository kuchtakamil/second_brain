# Bezpieczeństwo Jupyter Notebook

**Data:** 2024-01-28

---

**User:**

Na stronie Polynote jest napisane
Polynote allows arbitrary remote code execution, which is necessary for a notebook tool to function. While we'll try to improve safety by adding security measures, it will never be completely safe to run Polynote on your personal computer. For example:

It's possible that other websites you visit could use Polynote as an attack vector. Browsing the web while running Polynote is unsafe.
It's possible that remote attackers could use Polynote as an attack vector. Running Polynote on a computer that's accessible from the internet is unsafe.
Even running Polynote inside a container doesn't guarantee safety, as there will always be privilege escalation and container escape vulnerabilities which an attacker could leverage.
Please be diligent about checking for new releases, as they could contain fixes for critical security flaws.

Please be mindful of the security issues that Polynote causes; consult your company's security team before running Polynote. You are solely responsible for any breach, loss, or damage caused by running this software insecurely.

Czy podobne zagrożenie pojawia się w przypadku używania Jupyter Notebook?

---

**Assistant:**

Nie, zagrożenie podobne do tego opisanego dla Polynote nie występuje bezpośrednio w przypadku używania standardowego Jupyter Notebook. Jupyter Notebook działa lokalnie na twoim komputerze i nie posiada wbudowanej zdolności do zdalnego wykonywania kodu przez domyślne ustawienia.

Jupyter Notebook pozwala na interaktywne tworzenie i udostępnianie notatek zawierających kod, tekst i wyniki obliczeń. Domyślnie uruchamiany jest na lokalnym hoście, a dostęp do interfejsu jest uzyskiwany poprzez przeglądarkę internetową na localhostie.

Jednakże, podobnie jak przy każdym oprogramowaniu, bezpieczeństwo może być zagrożone, jeśli nie zachowasz ostrożności w pewnych sytuacjach:

1. **Kernely zewnętrzne**: Jeśli używasz języków programowania lub kerneli, które pozwalają na zdalne wykonanie kodu (np. przez protokół ZeroMQ), to mogą występować podobne ryzyka. Jednak, jest to zazwyczaj decyzja użytkownika i nie jest domyślną konfiguracją.

2. **Udostępnianie zdalne**: Jeśli masz skonfigurowane zdalne udostępnianie Jupyter Notebook (na przykład poprzez JupyterHub) i nie zabezpieczysz tego dostępu, istnieje ryzyko nieautoryzowanego dostępu.

Ważne jest, aby zawsze zachować ostrożność, aktualizować oprogramowanie i przestrzegać praktyk bezpieczeństwa, zwłaszcza jeśli konfigurujesz zdalny dostęp do swojego środowiska Jupyter Notebook. W przypadku zastosowań biznesowych zawsze warto skonsultować się z zespołem ds. bezpieczeństwa firmy.