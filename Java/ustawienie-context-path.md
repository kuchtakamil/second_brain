# Ustawienie context path

**Data:** 2024-12-06

---

**User:**

chcę w spring mvc ustawić pod jakim url będzie widoczna moja cała aplikacja razem z kontorlerami

---

**Assistant:**

Aby ustawić całą aplikację Spring MVC pod określonym URL-em bazowym, możesz skonfigurować **kontekst aplikacji (context path)**. Dzięki temu wszystkie kontrolery i zasoby będą dostępne pod nowym prefiksem URL. Oto jak to zrobić:

### 1. **Ustawienie `context-path` w pliku `application.properties` lub `application.yml`**
W pliku `application.properties`:
```properties
server.servlet.context-path=/moj-url
```

W pliku `application.yml`:
```yaml
server:
  servlet:
    context-path: /moj-url
```

### 2. **Efekt**
Jeżeli wcześniej miałeś kontroler dostępny pod `/home`, to po ustawieniu `server.servlet.context-path=/moj-url`, będzie on dostępny pod:
```
/moj-url/home
```

### 3. **Konfiguracja w kodzie (opcjonalnie)**
Jeśli wolisz, możesz ustawić `context-path` programowo w konfiguracji Spring Boota:
```java
import org.springframework.boot.web.servlet.server.ConfigurableServletWebServerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Bean
    public ConfigurableServletWebServerFactory webServerFactory() {
        return factory -> factory.setContextPath("/moj-url");
    }
}
```

### 4. **Testowanie**
Uruchom aplikację i odwiedź URL:
```
http://localhost:8080/moj-url
```

### 5. **Spring MVC bez Spring Boot**
Jeśli używasz czystego Spring MVC (bez Spring Boota), musisz skonfigurować to w pliku `web.xml` lub w kodzie:
W pliku `web.xml`:
```xml
<web-app>
    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>/WEB-INF/spring-context.xml</param-value>
    </context-param>

    <servlet>
        <servlet-name>dispatcher</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value></param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/moj-url/*</url-pattern>
    </servlet-mapping>
</web-app>
```

Po tej zmianie cała aplikacja będzie dostępna pod `/moj-url`.