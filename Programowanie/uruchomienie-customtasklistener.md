# Uruchomienie CustomTaskListener

**Data:** 2025-02-03

---

**User:**

  Mam plik o rozszerzeniu bpmn a to część jego zawartości
    <userTask id="DraftNotification" name="Draft Notification">
      <extensionElements>
        <activiti:taskListener event="create" class="com.pl.MyTaskListener"></activiti:taskListener>
        <activiti:taskListener event="create" class="com.pl.CustomTaskListener"></activiti:taskListener>
      </extensionElements>
    </userTask>
    
    Czy CustomTaskListener zostanie uruchomiony a jeśli tak to kiedy?

---

**Assistant:**

Tak, **`CustomTaskListener`** zostanie uruchomiony.  

### Kiedy zostanie uruchomiony?
Obydwa **`taskListener`** są przypisane do zdarzenia **`create`**, co oznacza, że zostaną wywołane **gdy zadanie użytkownika (`userTask`) zostanie utworzone** w silniku workflow Activiti.

### Kolejność wywołania
Silnik Activiti nie gwarantuje konkretnej kolejności uruchamiania `taskListener`-ów dla tego samego zdarzenia. Obydwa `taskListener`-y zostaną wykonane, ale kolejność ich wykonania może zależeć od wewnętrznej implementacji silnika.

Czy `CustomTaskListener` ma jakąś istotną zależność od `MyTaskListener`? Jeśli tak, można rozważyć inną strategię, np. umieszczenie ich w jednej klasie lub przekierowanie logiki.