# JVM: Pytania Rekrutacyjne

Lista pytań na rozmowę kwalifikacyjną dotyczących **działania Java Virtual Machine (JVM)**. Pytania pogrupowane tematycznie — od architektury ogólnej, przez zarządzanie pamięcią, po kompilację i diagnostykę. Bez odpowiedzi — służą do samodzielnej nauki i przygotowania.

---

## 1. Architektura JVM

1. Z jakich głównych komponentów składa się JVM? Opisz rolę każdego z nich.
2. Czym różni się JVM od JRE i JDK? Jakie jest ich wzajemne powiązanie?
3. Czym jest specyfikacja JVM (JVM Specification) i dlaczego istnieje wiele implementacji JVM (HotSpot, OpenJ9, GraalVM)?
4. Opisz cykl życia programu Java — od kodu źródłowego `.java` do wykonania na JVM.
5. Czym jest bytecode i jaki jest jego format? Dlaczego Java jest uważana za język „write once, run anywhere"?
6. Jakie są różnice między JVM a procesem natywnym systemu operacyjnego?
7. Czym jest stos wywołań JVM (JVM call stack) i jak różni się od stosu systemu operacyjnego?

---

## 2. Class Loading (ładowanie klas)

8. Jak działa mechanizm Class Loading w JVM? Jakie są jego fazy (loading, linking, initialization)?
9. Czym jest hierarchia Class Loaderów? Opisz Bootstrap, Extension (Platform) i Application Class Loader.
10. Na czym polega zasada delegacji rodzicielskiej (parent delegation model)? Dlaczego jest istotna?
11. Kiedy klasa jest ładowana do pamięci — leniwie czy eagerly? Co wyzwala załadowanie klasy?
12. Czym jest faza weryfikacji (verification) w procesie linkowania? Przed czym chroni?
13. Czym jest faza przygotowania (preparation) i rozwiązywania (resolution)?
14. Kiedy następuje inicjalizacja klasy? Jakie instrukcje ją wyzwalają?
15. Czym jest Context Class Loader wątku i do czego służy (np. w kontekście SPI, JNDI)?
16. Jak napisać własny Class Loader? W jakich scenariuszach jest to potrzebne (hot deploy, izolacja modułów)?
17. Czym jest Class Unloading? Kiedy JVM może usunąć załadowaną klasę z pamięci?
18. Jakie problemy mogą wystąpić przy ładowaniu klas (ClassNotFoundException vs NoClassDefFoundError)? Czym się różnią?

---

## 3. Model pamięci JVM (JVM Memory Model)

19. Opisz strukturę pamięci JVM: Heap, Stack, Metaspace, Code Cache, Native Memory.
20. Czym jest Heap i jak jest podzielony (Young Generation, Old Generation)?
21. Czym jest Young Generation i jakie zawiera obszary (Eden, Survivor S0, Survivor S1)?
22. Jak działa mechanizm promocji obiektów z Young do Old Generation? Co to jest tenuring threshold?
23. Czym jest Metaspace i czym różni się od dawnego PermGen (Permanent Generation)?
24. Co przechowuje Metaspace? Dlaczego może dojść do jego przepełnienia?
25. Czym jest Thread Stack i co przechowuje (ramki stosu, zmienne lokalne, stos operandów)?
26. Czym jest Stack Frame i z jakich elementów się składa?
27. Czym jest stos operandów (operand stack) i jak jest wykorzystywany przez interpreter bytecode?
28. Czym jest Code Cache i jaką rolę pełni w kontekście kompilacji JIT?
29. Czym jest Direct Memory (off-heap) i kiedy jest wykorzystywana (np. NIO ByteBuffer)?
30. Czym jest String Pool (pula stringów)? Gdzie fizycznie się znajduje w pamięci JVM?
31. Jakie są limity poszczególnych obszarów pamięci i jak je konfigurować?

---

## 4. Garbage Collection (zbieranie śmieci)

32. Czym jest Garbage Collection i na jakiej podstawie JVM decyduje, że obiekt jest „śmieciem"?
33. Czym jest reachability analysis (analiza osiągalności) i co to są GC Roots?
34. Jakie obiekty mogą być GC Roots? Wymień przykłady.
35. Czym jest Mark-and-Sweep? Opisz ogólny algorytm.
36. Czym jest Mark-Compact i czym różni się od Mark-and-Sweep?
37. Czym jest Copying Collector i jak działa w kontekście Young Generation?
38. Opisz cykl Minor GC — co się dzieje z obiektami w Eden i Survivor spaces?
39. Czym jest Major GC (Full GC) i kiedy jest wywoływany?
40. Czym jest Stop-The-World (STW) pause? Dlaczego jest konieczna i jak wpływa na aplikację?
41. Czym jest Safe Point i Safe Region? Dlaczego JVM musi czekać na osiągnięcie safe pointów?
42. Opisz Garbage Collector G1 (Garbage-First). Czym są regiony (regions) i jak działa mixed collection?
43. Czym jest ZGC? Jakie problemy rozwiązuje i jak osiąga niskie pauzy?
44. Czym jest Shenandoah GC i czym różni się od ZGC?
45. Czym jest Serial GC i Parallel GC? Kiedy mają sens?
46. Czym jest Concurrent Mark-Sweep (CMS) i dlaczego został usunięty?
47. Czym jest Epsilon GC (no-op collector) i jakie ma zastosowania?
48. Czym są Card Tables i Remembered Sets? Jaką rolę pełnią w GC generacyjnym?
49. Czym jest Write Barrier w kontekście Garbage Collectora?
50. Jak odczytywać i interpretować logi GC?
51. Jakie flagi JVM służą do konfiguracji Garbage Collectora?

---

## 5. Rodzaje referencji

52. Jakie są cztery rodzaje referencji w Javie (Strong, Weak, Soft, Phantom)? Czym się różnią?
53. Kiedy GC zbiera obiekty osiągalne jedynie przez Weak Reference?
54. Czym jest Soft Reference i jak JVM decyduje o jej zebraniu? Jak to zależy od ciśnienia pamięciowego?
55. Do czego służy Phantom Reference? Jak współpracuje z ReferenceQueue?
56. Czym jest ReferenceQueue i jak monitorować cykl życia obiektów za jej pomocą?
57. Czym jest Cleaner API (Java 9+) i jak zastępuje mechanizm finalize()?
58. Dlaczego metoda `finalize()` jest deprecated i jakie problemy powoduje?

---

## 6. JIT Compilation (kompilacja Just-In-Time)

59. Czym jest kompilacja JIT i dlaczego JVM nie kompiluje od razu całego kodu do kodu maszynowego?
60. Czym jest interpreter bytecode i jaka jest jego rola w kontekście JIT?
61. Czym jest Tiered Compilation? Opisz poszczególne poziomy (Level 0–4).
62. Czym różni się kompilator C1 (Client) od C2 (Server)?
63. Czym jest próg kompilacji (compilation threshold) i jak JVM decyduje, którą metodę skompilować?
64. Czym jest On-Stack Replacement (OSR)? Kiedy zachodzi?
65. Jakie optymalizacje wykonuje kompilator JIT (inlining, escape analysis, loop unrolling, dead code elimination, devirtualization)?
66. Czym jest Escape Analysis i jak wpływa na alokację obiektów (scalar replacement, stack allocation)?
67. Czym jest deoptymalizacja (deoptimization)? Kiedy JVM musi cofnąć skompilowany kod do interpretowanego?
68. Czym jest metoda „gorąca" (hot method) i „gorąca pętla" (hot loop)?
69. Czym jest Intrinsic w kontekście JVM? Podaj przykłady metod intrinsic.
70. Jak podejrzeć skompilowany przez JIT kod maszynowy (PrintAssembly, JITWatch)?

---

## 7. GraalVM i kompilacja AOT

71. Czym jest GraalVM i czym różni się od standardowego HotSpot JVM?
72. Czym jest kompilacja Ahead-of-Time (AOT) i jakie daje korzyści w porównaniu z JIT?
73. Czym jest Native Image (GraalVM) i jakie nakłada ograniczenia (refleksja, dynamic proxy, JNI)?
74. Czym jest Substrate VM?
75. Jak działa analiza closed-world assumption w kontekście Native Image?
76. Jakie frameworki wspierają natywną kompilację (Quarkus, Micronaut, Spring Native)?

---

## 8. Java Memory Model (JMM) — model pamięci współbieżnej

77. Czym jest Java Memory Model (JMM) i jaki problem rozwiązuje?
78. Czym jest relacja happens-before? Wymień kluczowe reguły happens-before.
79. Czym jest widoczność zmiennych między wątkami (visibility)? Dlaczego zmiana zmiennej w jednym wątku może nie być widoczna w innym?
80. Czym jest reordering instrukcji i kto go wykonuje (kompilator, JIT, procesor)?
81. Jak `volatile` wpływa na model pamięci? Jakie gwarancje daje i czego nie gwarantuje?
82. Jak `synchronized` wpływa na model pamięci (memory barrier / fence)?
83. Czym jest false sharing i jak wpływa na wydajność wielowątkową? Jak go unikać?
84. Czym jest `@Contended` adnotacja i jaki problem rozwiązuje?

---

## 9. Wątki i synchronizacja na poziomie JVM

85. Jak JVM mapuje wątki Javy na wątki systemu operacyjnego (model 1:1)?
86. Czym są wirtualne wątki (Project Loom, Java 21) i jak zmieniają model wątków w JVM?
87. Jak działa monitor obiektu (object monitor) w JVM? Co to jest monitor entry i monitor exit?
88. Czym jest biased locking, lightweight locking i heavyweight locking? Jak JVM eskaluje blokady?
89. Czym jest lock coarsening i lock elision (optymalizacje JIT)?
90. Jak JVM obsługuje `wait()`, `notify()` i `notifyAll()` na poziomie monitora?

---

## 10. Bytecode i wykonanie kodu

91. Czym jest bytecode Javy? Jakie są podstawowe instrukcje bytecode (np. `aload`, `invokevirtual`, `getstatic`)?
92. Jakie są rodzaje instrukcji invoke (`invokevirtual`, `invokeinterface`, `invokespecial`, `invokestatic`, `invokedynamic`)?
93. Czym jest `invokedynamic` i jak jest wykorzystywane (lambdy, konkatenacja stringów)?
94. Czym jest Constant Pool w pliku `.class`? Co przechowuje?
95. Jak wygląda struktura pliku `.class`?
96. Jak podejrzeć bytecode klasy (javap, ASM, jclasslib)?
97. Czym jest weryfikator bytecode (bytecode verifier) i jakie reguły sprawdza?

---

## 11. Diagnostyka i narzędzia JVM

98. Jakie są podstawowe narzędzia JVM do diagnostyki (jps, jstack, jmap, jcmd, jstat, jinfo)?
99. Czym jest Thread Dump i jak go odczytać? Jakie stany wątków w nim widać?
100. Czym jest Heap Dump i jak go analizować (Eclipse MAT, VisualVM)?
101. Jak zdiagnozować wyciek pamięci (memory leak) na JVM?
102. Jak zdiagnozować problem z wydajnością GC?
103. Czym jest Java Flight Recorder (JFR) i Java Mission Control (JMC)?
104. Czym jest JMX (Java Management Extensions) i MBeans? Jak monitorować JVM w runtime?
105. Jak zdiagnozować deadlock za pomocą narzędzi JVM?
106. Czym jest safepoint i jak wpływa na czas odpowiedzi aplikacji? Jak go monitorować?

---

## 12. Flagi i strojenie JVM

107. Jakie są najważniejsze flagi JVM i jak je podzielić (`-X`, `-XX`, standardowe)?
108. Jak dobrać rozmiar Heap (`-Xms`, `-Xmx`)? Jakie są konsekwencje zbyt małego lub zbyt dużego Heap?
109. Jak skonfigurować Metaspace (`-XX:MaxMetaspaceSize`)? Kiedy warto to robić?
110. Jak dobrać wielkość Thread Stack (`-Xss`)?
111. Jakie flagi kontrolują zachowanie GC (np. `-XX:+UseG1GC`, `-XX:MaxGCPauseMillis`, `-XX:G1HeapRegionSize`)?
112. Czym są flagi diagnostyczne (`-XX:+PrintCompilation`, `-XX:+PrintGCDetails`, `-XX:+HeapDumpOnOutOfMemoryError`)?
113. Czym jest Ergonomics w JVM — jak JVM automatycznie dobiera parametry?
114. Jak profilować aplikację JVM (async-profiler, JFR, VisualVM)?

---

## 13. Bezpieczeństwo i izolacja w JVM

115. Czym był Security Manager i dlaczego został usunięty?
116. Jak JVM zapewnia bezpieczeństwo typów (type safety) w runtime?
117. Czym jest weryfikacja bytecode i przed jakimi atakami chroni?
118. Jak działa sandboxing w JVM? Czy JVM izoluje kod od systemu operacyjnego?
119. Czym jest `sun.misc.Unsafe` i dlaczego jest problematyczny? Jakie ma zamienniki?

---

## 14. Internals — zaawansowane mechanizmy wewnętrzne

120. Czym jest TLAB (Thread-Local Allocation Buffer) i jak przyspiesza alokację obiektów?
121. Czym jest Object Header w JVM? Co zawiera (mark word, klass pointer)?
122. Ile pamięci zajmuje obiekt w JVM? Jak obliczyć rozmiar obiektu (shallow vs retained size)?
123. Czym jest Compressed Oops i Compressed Class Pointers? Kiedy JVM je włącza?
124. Czym jest Object Alignment i padding?
125. Czym jest pointer tagging / coloured pointers (stosowane w ZGC)?
126. Czym są Safepoints i jak wpływają na counted loops?
127. Czym jest deoptymalizacja spowodowana „uncommon trap"?
128. Jak działa alokacja obiektów w JVM (fast path vs slow path)?

---

## Powiązane materiały

- [Pytania Rekrutacyjne — Java Senior](pytania-rekrutacyjne-java-senior.md)
- [Pytania Rekrutacyjne — Spring 3.0](pytania-rekrutacyjne-spring-3-0.md)
- [Przestrzeń Survivor Garbage Collector](przestrzeń-survivor-garbage-collector.md)
