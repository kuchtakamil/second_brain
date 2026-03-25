# Sposoby tworzenia Beanów

**Data:** 2025-10-03

---

**User:**

Jakie w spring są sposoby na utworzenie Bean'a oprócz admnotacji podobnych do @Repository, @Component itp?

---

**Assistant:**

W Springu można utworzyć bean na kilka sposobów, nie tylko poprzez adnotacje typu `@Component`, `@Service`, `@Repository`, `@Controller`. Oto główne mechanizmy:  

---

### 1. **Adnotacja `@Bean` w klasie konfiguracyjnej**
Zamiast oznaczać klasę adnotacją komponentową, można utworzyć beana metodą fabrykującą:  

```java
@Configuration
public class AppConfig {

    @Bean
    public MyService myService() {
        return new MyServiceImpl();
    }
}
```

Tutaj metoda `myService()` zwraca instancję obiektu, który będzie beanem w kontekście Springa.

---

### 2. **XML Configuration** (starszy sposób, ale wciąż działa)
W pliku `applicationContext.xml` można zdefiniować bean:

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
           http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="myService" class="com.example.MyServiceImpl"/>
</beans>
```

---

### 3. **Programatyczne rejestrowanie Beanów w kodzie**
Można użyć **`BeanDefinitionRegistry`** albo **`GenericApplicationContext`**:

```java
AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext();
context.registerBean(MyService.class);
context.refresh();
```

Albo przez `BeanDefinitionRegistryPostProcessor`:

```java
@Override
public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) {
    RootBeanDefinition beanDefinition = new RootBeanDefinition(MyServiceImpl.class);
    registry.registerBeanDefinition("myService", beanDefinition);
}
```

---

### 4. **`FactoryBean`**
Jeśli potrzebujesz pełnej kontroli nad tworzeniem obiektu:

```java
public class MyServiceFactoryBean implements FactoryBean<MyService> {
    @Override
    public MyService getObject() {
        return new MyServiceImpl();
    }

    @Override
    public Class<?> getObjectType() {
        return MyService.class;
    }
}
```

Wtedy Spring rejestruje beana na podstawie fabryki.

---

### 5. **Import konfiguracji**
Można zaciągnąć beany z innej konfiguracji:

```java
@Configuration
@Import(OtherConfig.class)
public class AppConfig {
}
```

---

### 6. **Spring Boot – automatyczna rejestracja przez `@Enable...`**
Wiele starterów rejestruje beany przez `@EnableAutoConfiguration`, `@EnableScheduling`, itp., które pod spodem używają **`@Import`** + `ImportSelector`.

---

👉 Czy chcesz, żebym przygotował tabelę porównawczą z krótkim opisem *kiedy który sposób ma sens* (np. `@Bean` vs `@Component` vs programatyczna rejestracja)?