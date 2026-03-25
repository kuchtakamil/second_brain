# Wyświetlanie obrazka po radio

**Data:** 2025-03-14

---

**User:**

W pliku mustache mam znacznik {{#radios}} pod którym wyświetlam kilka opcji radio buttons.
Przy jednym wybranym radio buttonie chcę wyświetlić jeszcze dodatkowo wybrany obrazek. Jak mogę to ustawić w mustache tak aby tylko pod jednym radio button wyświetlany było obrazek?


---

**Assistant:**

Jasne! W Mustache możesz osiągnąć to bardzo łatwo dzięki warunkowemu renderowaniu bloków (`{{#condition}}...{{/condition}}` i `{{^condition}}...{{/condition}}`). Kluczową sprawą jest dodanie do obiektu danych odpowiedniego pola, które będzie sygnalizować, że dany radio button ma mieć dodatkowy obrazek.

### Przykład:

#### Plik `template.mustache`:
```html
{{#radios}}
  <label>
    <input type="radio" name="option" value="{{value}}">
    {{label}}
  </label>
  
  {{#showImage}}
    <img src="{{imageUrl}}" alt="Dodatkowy obrazek" />
  {{/showImage}}
{{/radios}}
```

#### Dane przekazywane do szablonu (np. w JavaScript):
```js
{
  radios: [
    { value: "a", label: "Opcja A" },
    { value: "b", label: "Opcja B", showImage: true, imageUrl: "b-image.jpg" },
    { value: "c", label: "Opcja C" }
  ]
}
```

W tym przypadku **tylko dla drugiej opcji (B)** zostanie wyrenderowany obrazek, ponieważ tylko tam `showImage` ma wartość `true`.

---

### Alternatywa: jeśli chcesz wyświetlać obrazek **dopiero po zaznaczeniu** radio buttona (czyli dynamicznie w przeglądarce po kliknięciu), to Mustache się do tego nie nadaje bez dodatkowego JavaScriptu — ponieważ Mustache jest tylko silnikiem renderującym statyczny HTML.

W takim przypadku potrzebujesz JS, który będzie nasłuchiwał zmian zaznaczenia i np. pokazywał/ukrywał `<img>` odpowiednio. Jeśli chcesz też taki przykład, daj znać — przygotuję.

Chcesz wersję z JavaScriptem do dynamicznego pokazywania obrazka?

---

**User:**

Ok. Zakładając że plik template.mustache będzie wyglądał tak jak podałeś to czy mogę ustawić parametry modelu w ten sposób 
model.addAttribute("radios", radios);
model.addAttribute("imageUrl", imageUrl);
czyli tak aby informacja o imageUrl była podawana poza atrybutem radios?

---

**Assistant:**

Świetne pytanie – i tutaj niestety **nie do końca tak się da**, jeśli chcesz, by obrazek był renderowany *tylko przy jednym konkretnym radio buttonie*. Już wyjaśniam dlaczego.

### 🔸 Mustache nie pozwala wprost na dostęp do zmiennych *spoza bieżącego kontekstu pętli* (`{{#radios}}...{{/radios}}`) — więc jeśli `imageUrl` i `showImage` nie są w obiekcie danego elementu `radios`, to Mustache ich w tej pętli nie "zobaczy".

Czyli jeśli masz:
```java
model.addAttribute("radios", radios);
model.addAttribute("imageUrl", "b-image.jpg");
```

to w pętli `{{#radios}}` nie masz dostępu do `imageUrl`, bo Mustache patrzy wtedy tylko na zawartość pojedynczego obiektu z `radios`.

---

### ✅ Rozwiązanie poprawne: wbudowanie tych informacji bezpośrednio w elementy `radios`.

Czyli:
```java
List<Map<String, Object>> radios = new ArrayList<>();

Map<String, Object> radioA = new HashMap<>();
radioA.put("value", "a");
radioA.put("label", "Opcja A");
radios.add(radioA);

Map<String, Object> radioB = new HashMap<>();
radioB.put("value", "b");
radioB.put("label", "Opcja B");
radioB.put("showImage", true);
radioB.put("imageUrl", "/images/b-image.jpg");
radios.add(radioB);

model.addAttribute("radios", radios);
```

Wtedy Twój `template.mustache` działa tak jak wcześniej pokazałem:
```html
{{#radios}}
  <label>
    <input type="radio" name="option" value="{{value}}">
    {{label}}
  </label>
  {{#showImage}}
    <img src="{{imageUrl}}" />
  {{/showImage}}
{{/radios}}
```

---

### 🔸 Alternatywne obejście (niewygodne): jeśli naprawdę chcesz trzymać `imageUrl` osobno, musiałbyś np. dodać do każdego `radio` jakiś warunek typu `isSpecial: true`, i potem wyświetlać `imageUrl` w `{{#isSpecial}}<img src="{{/imageUrl}}"{{/isSpecial}}`, ale i tak musisz w każdym elemencie wiedzieć **czy** obrazek ma się pojawić – czyli znowu kończysz na danych w `radios`.

---

Chcesz, żebym pokazał wersję np. z helperem, który modyfikuje listę `radios` automatycznie przed wysłaniem do modelu? Albo jak to jeszcze bardziej uprościć?