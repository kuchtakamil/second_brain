# PowerMock Java Compatibility Fix

**Data:** 2025-02-17

---

**User:**

Próbuję uruchomić uni test w intellij i mam taki błąd
org.objenesis.ObjenesisException: java.lang.reflect.InvocationTargetException

	at org.objenesis.instantiator.sun.SunReflectionFactoryHelper.newConstructorForSerialization(SunReflectionFactoryHelper.java:48)
	at org.objenesis.instantiator.sun.SunReflectionFactoryInstantiator.<init>(SunReflectionFactoryInstantiator.java:41)
	at org.objenesis.strategy.StdInstantiatorStrategy.newInstantiatorOf(StdInstantiatorStrategy.java:68)
	at org.objenesis.ObjenesisBase.getInstantiatorOf(ObjenesisBase.java:94)
	at org.powermock.reflect.internal.WhiteboxImpl.newInstance(WhiteboxImpl.java:259)
	at org.powermock.reflect.Whitebox.newInstance(Whitebox.java:139)
	at org.powermock.tests.utils.impl.AbstractTestSuiteChunkerImpl.getPowerMockTestListenersLoadedByASpecificClassLoader(AbstractTestSuiteChunkerImpl.java:95)
	at org.powermock.modules.junit4.common.internal.impl.JUnit4TestSuiteChunkerImpl.createDelegatorFromClassloader(JUnit4TestSuiteChunkerImpl.java:174)
	at org.powermock.modules.junit4.common.internal.impl.JUnit4TestSuiteChunkerImpl.createDelegatorFromClassloader(JUnit4TestSuiteChunkerImpl.java:48)
	at org.powermock.tests.utils.impl.AbstractTestSuiteChunkerImpl.createTestDelegators(AbstractTestSuiteChunkerImpl.java:108)
	at org.powermock.modules.junit4.common.internal.impl.JUnit4TestSuiteChunkerImpl.<init>(JUnit4TestSuiteChunkerImpl.java:71)
	at org.powermock.modules.junit4.common.internal.impl.AbstractCommonPowerMockRunner.<init>(AbstractCommonPowerMockRunner.java:36)
	at org.powermock.modules.junit4.PowerMockRunner.<init>(PowerMockRunner.java:34)
	at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.base/java.lang.reflect.Constructor.newInstance(Constructor.java:490)
	at org.junit.internal.builders.AnnotatedBuilder.buildRunner(AnnotatedBuilder.java:104)
	at org.junit.internal.builders.AnnotatedBuilder.runnerForClass(AnnotatedBuilder.java:86)
	at org.junit.runners.model.RunnerBuilder.safeRunnerForClass(RunnerBuilder.java:70)
	at org.junit.internal.builders.AllDefaultPossibilitiesBuilder.runnerForClass(AllDefaultPossibilitiesBuilder.java:37)
	at org.junit.runners.model.RunnerBuilder.safeRunnerForClass(RunnerBuilder.java:70)
	at org.junit.internal.requests.ClassRequest.createRunner(ClassRequest.java:28)
	at org.junit.internal.requests.MemoizingRequest.getRunner(MemoizingRequest.java:19)
	at org.junit.internal.requests.FilterRequest.getRunner(FilterRequest.java:36)
	at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:50)
	at com.intellij.rt.junit.IdeaTestRunner$Repeater$1.execute(IdeaTestRunner.java:38)
	at com.intellij.rt.execution.junit.TestsRepeater.repeat(TestsRepeater.java:11)
	at com.intellij.rt.junit.IdeaTestRunner$Repeater.startRunnerWithArgs(IdeaTestRunner.java:35)
	at com.intellij.rt.junit.JUnitStarter.prepareStreamsAndStart(JUnitStarter.java:232)
	at com.intellij.rt.junit.JUnitStarter.main(JUnitStarter.java:55)
Caused by: java.lang.reflect.InvocationTargetException
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:566)
	at org.objenesis.instantiator.sun.SunReflectionFactoryHelper.newConstructorForSerialization(SunReflectionFactoryHelper.java:44)
	... 30 more
Caused by: java.lang.IllegalAccessError: class jdk.internal.reflect.ConstructorAccessorImpl loaded by org.powermock.core.classloader.MockClassLoader @192c3f1e cannot access jdk/internal/reflect superclass jdk.internal.reflect.MagicAccessorImpl

---

**Assistant:**

Wygląda na to, że problem wynika z tego, że **PowerMock** nie jest kompatybilny z nowymi wersjami Javy (prawdopodobnie używasz Javy 17 lub nowszej). Błąd **IllegalAccessError** oznacza, że PowerMock próbuje uzyskać dostęp do wewnętrznych klas JDK, które od Javy 16+ są domyślnie niedostępne.

### Jak to naprawić?
#### 1. **Sprawdź wersję Javy**
Upewnij się, jakiej wersji Javy używasz w IntelliJ:  
**File → Project Structure → SDKs**  
Jeśli to **Java 17+**, PowerMock może mieć problem.

#### 2. **Dodaj opcje JVM do testów**
Spróbuj uruchomić testy z dodatkowymi opcjami JVM:
```
--add-opens java.base/jdk.internal.reflect=ALL-UNNAMED
```
W IntelliJ możesz to zrobić tak:
- **Run → Edit Configurations**
- Wybierz swoją konfigurację testową
- W sekcji "VM Options" dodaj:
  ```
  --add-opens java.base/jdk.internal.reflect=ALL-UNNAMED
  ```

#### 3. **Sprawdź wersję PowerMock**
Jeśli używasz starej wersji PowerMock, spróbuj zaktualizować do najnowszej:
```xml
<dependency>
    <groupId>org.powermock</groupId>
    <artifactId>powermock-api-mockito2</artifactId>
    <version>2.0.9</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.powermock</groupId>
    <artifactId>powermock-module-junit4</artifactId>
    <version>2.0.9</version>
    <scope>test</scope>
</dependency>
```
PowerMock nie wspiera JUnit 5, więc jeśli używasz JUnit 5, rozważ przejście na inne rozwiązanie.

#### 4. **Rozważ alternatywę dla PowerMock**
PowerMock jest przestarzały i nie wspiera Javy 17+. Jeśli możesz, spróbuj użyć **Mockito + Mockito-inline**, które od wersji 3 pozwala mockować statyczne metody i konstruktory bez PowerMock:
```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-inline</artifactId>
    <version>5.2.0</version>
    <scope>test</scope>
</dependency>
```
I użyj np. `Mockito.mockStatic()` do mockowania statycznych metod.

---

Spróbuj powyższych kroków i daj znać, czy problem ustąpił! 🚀