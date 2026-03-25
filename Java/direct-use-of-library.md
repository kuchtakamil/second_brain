# Direct Use of Library

**Data:** 2023-11-27

---

**User:**

Mam projekt - myProject - który korzysta z gradle. W zależnościach mam bibliotekę A która to z kolei ma zależność do biblioteki B. Czy w moim projekcie myProject mogę bezpośrednio korzystać z biblioteki B?

---

**Assistant:**

Tak, możesz korzystać z biblioteki B bezpośrednio w swoim projekcie myProject, nawet jeśli biblioteka B jest zależnością biblioteki A. Gdy dodajesz bibliotekę A jako zależność w projekcie myProject za pomocą Gradle, Gradle automatycznie rozwiązuje zależności, co oznacza, że biblioteka B również będzie dostępna w twoim projekcie.

Oto przykład, jak to może wyglądać w pliku build.gradle Twojego projektu myProject:

```groovy
dependencies {
    implementation 'grupa:A:1.0.0'
    // Nie musisz dodawać bezpośrednio zależności do biblioteki B, Gradle to zrobi za Ciebie.
}
```

Jeśli biblioteka A zawiera zależność do biblioteki B w swoim pliku build.gradle, to Gradle automatycznie pociągnie również tę zależność do twojego projektu myProject, więc możesz korzystać z klas i funkcji dostępnych w bibliotece B bezpośrednio w kodzie swojego projektu.

---

**User:**

a co gdy do myProject dodam bibliotekę C. Ta biblioteka C ma również zależność do biblioteki B ale w innej wersji. Którą wersję B mogę wtedy wykorzystać w myProject?

---

**Assistant:**

Gdy do projektu myProject dodajesz bibliotekę C, która ma zależność do biblioteki B w innej wersji, może wystąpić sytuacja konfliktu wersji. Gradle stara się rozwiązać te konflikty w sposób elastyczny, ale czasami może być konieczne ręczne określenie wersji biblioteki B, której chcesz użyć w projekcie myProject.

W przypadku konfliktu wersji możesz użyć bloku `configurations` w pliku build.gradle swojego projektu, aby precyzyjnie określić, która wersja biblioteki B ma być używana. Na przykład:

```groovy
configurations {
    preferredB
}

dependencies {
    implementation 'grupa:A:1.0.0'
    implementation 'grupa:C:1.0.0'
    preferredB 'grupa:B:1.2.0' // Wybierz preferowaną wersję biblioteki B
}

configurations.all {
    resolutionStrategy {
        force 'grupa:B:1.2.0' // Ręczne ustalenie wersji biblioteki B
    }
}
```

W powyższym przykładzie, `preferredB` jest dodawane jako nowa konfiguracja, a następnie w bloku `configurations.all`, używamy `resolutionStrategy`, aby wymusić użycie konkretnej wersji biblioteki B. Możesz dostosować wersję w `force` do preferowanej przez Ciebie wersji biblioteki B.

Ważne jest, aby monitorować takie ręczne ustawienia wersji, ponieważ mogą one prowadzić do konfliktów w przyszłości. Staraj się używać najnowszych i kompatybilnych wersji bibliotek, aby uniknąć problemów zgodności.