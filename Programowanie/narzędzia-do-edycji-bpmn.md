# Narzędzia do edycji BPMN

**Data:** 2025-07-29

---

**User:**

Pracuję z prostymi diagramami bpm i do tego czasu uzywałem eclipse z wtyczką activiti. Ale niee wersje eclipse przestały wspierać tę wtyczkę. Jakiego innego narzędzia dość prostego i darmowego mogę użyć by edytowac te diagramy

---

**Assistant:**

Skoro korzystasz z prostych diagramów BPMN i dotąd używałeś Eclipse + Activiti Designer, to poniżej znajdziesz listę darmowych i względnie prostych narzędzi, które mogą być dobrą alternatywą:

---

### 🔧 **1. [bpmn.io / Camunda Modeler (Desktop)]**
- **URL:** [https://bpmn.io](https://bpmn.io)
- **Opis:** Darmowy, open source’owy edytor diagramów BPMN, CMMN i DMN. Rozwijany przez Camunda.
- **Zalety:**
  - Bardzo intuicyjny interfejs.
  - Wspiera eksport/import plików `.bpmn`.
  - Możliwość rozszerzania o własne pluginy.
  - Działa jako aplikacja desktopowa (Camunda Modeler) lub w przeglądarce.
- **Wady:**
  - Nie ma natywnej integracji z Eclipse/IDE.
  - Nie obsługuje uruchamiania procesów, tylko edycję.

---

### 🌐 **2. [ProcessMaker Modeler (Community Edition)]**
- **URL:** [https://www.processmaker.com/open-source/](https://www.processmaker.com/open-source/)
- **Opis:** Webowe narzędzie open source do projektowania procesów BPMN.
- **Zalety:**
  - Ładny interfejs webowy.
  - Możliwość osadzenia modelera we własnej aplikacji.
- **Wady:**
  - Do uruchomienia wymaga środowiska serwerowego.
  - Community Edition ma ograniczenia względem wersji Enterprise.

---

### 💻 **3. [Signavio (obecnie SAP Signavio Process Manager)]**
- **URL:** [https://www.signavio.com/](https://www.signavio.com/)
- **Opis:** Zaawansowane narzędzie BPMN, dostępne jako SaaS.
- **Zalety:**
  - Profesjonalny edytor procesów.
  - Używany w firmach do analizy i optymalizacji procesów.
- **Wady:**
  - Darmowa wersja dostępna tylko jako trial.
  - Bardziej zaawansowane niż może być potrzebne do prostych diagramów.

---

### 🧰 **4. [Modelio (z modułem BPMN)]**
- **URL:** [https://www.modelio.org/](https://www.modelio.org/)
- **Opis:** Open source’owe narzędzie do modelowania UML, BPMN i SysML.
- **Zalety:**
  - Desktopowa aplikacja, bez konieczności działania w przeglądarce.
  - Wspiera BPMN w podstawowym zakresie.
- **Wady:**
  - UI mniej nowoczesny.
  - Może być bardziej złożone niż potrzebujesz.

---

### 🔁 **5. [Yaoqiang BPMN Editor]**
- **URL:** [https://sourceforge.net/projects/bpmn/](https://sourceforge.net/projects/bpmn/)
- **Opis:** Lekki edytor BPMN napisany w Javie, działający jako standalone.
- **Zalety:**
  - Bardzo lekki i prosty.
  - Obsługuje pliki `.bpmn`.
- **Wady:**
  - Projekt nie jest aktywnie rozwijany.
  - UI dość przestarzały.

---

### 🔍 Co polecam?
Jeśli chcesz **proste i stabilne** narzędzie do edycji BPMN, to **Camunda Modeler (bpmn.io)** jest najczęściej wybieranym zamiennikiem dla Activiti Designer. Nie integruje się z IDE, ale jest lekki, intuicyjny i wspiera standard BPMN 2.0.

---

Jeśli chcesz, mogę pomóc w migracji istniejących plików `.bpmn` do Camunda Modeler lub sprawdzić ich kompatybilność.