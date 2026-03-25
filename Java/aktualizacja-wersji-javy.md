# Aktualizacja wersji Javy

**Data:** 2023-09-05

---

**User:**

Jeśli po uruchomieniu mvn test otrzymuję 
this version of the Java Runtime only recognizes class file versions up to 52.0 
co powinienem zrobić

---

**Assistant:**

Komunikat "this version of the Java Runtime only recognizes class file versions up to 52.0" sugeruje, że używasz wersji Javy, która nie rozpoznaje plików klas o wersji nowszej niż 52.0. Numer 52.0 odpowiada wersji Java 8.

Oto kilka kroków, które możesz podjąć, aby rozwiązać ten problem:

1. **Zaktualizuj wersję Javy:** Jeśli używasz starszej wersji Javy, zaktualizuj ją do nowszej. Upewnij się, że masz zainstalowaną wersję Javy 8 lub nowszą, która obsługuje nowsze wersje plików klas.

2. **Sprawdź zmienną środowiskową JAVA_HOME:** Upewnij się, że zmienna środowiskowa `JAVA_HOME` wskazuje na poprawną ścieżkę do zainstalowanej wersji Javy. Możesz użyć komendy `echo $JAVA_HOME` (w systemach Unix/Linux) lub `echo %JAVA_HOME%` (w systemach Windows), aby to sprawdzić i dostosować ścieżkę, jeśli jest niepoprawna.

3. **Zaktualizuj projekt Maven:** Jeśli pracujesz nad projektem Maven, sprawdź, czy w pliku `pom.xml` projektu jest właściwa wersja Javy zdefiniowana w sekcji `<properties>`. Możesz dostosować to ustawienie, aby odpowiadało wersji Javy, którą masz zainstalowaną.

4. **Zaktualizuj ustawienia w IDE:** Jeśli używasz środowiska programistycznego, takiego jak IntelliJ IDEA, Eclipse lub inne, upewnij się, że ustawienia projektu odnoszą się do właściwej wersji Javy.

5. **Sprawdź wersję kompilatora:** Upewnij się, że używasz kompatybilnej wersji kompilatora Javy w swoim projekcie. Jeśli korzystasz z Maven, możesz to zrobić w pliku `pom.xml`, w sekcji `<build>`. Na przykład:

   ```xml
   <build>
       <plugins>
           <plugin>
               <groupId>org.apache.maven.plugins</groupId>
               <artifactId>maven-compiler-plugin</artifactId>
               <version>3.8.1</version> <!-- Wersja kompilatora -->
               <configuration>
                   <source>1.8</source> <!-- Wersja źródłowa (np. Java 8) -->
                   <target>1.8</target> <!-- Wersja docelowa -->
               </configuration>
           </plugin>
       </plugins>
   </build>
   ```

Po wykonaniu tych kroków powinieneś być w stanie uruchomić `mvn test` bez problemów związanych z wersją klas plików.