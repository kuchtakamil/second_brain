# AWS Fargate i porównanie z AWS Lambda

AWS Fargate to bezserwerowy (serverless) silnik obliczeniowy przeznaczony dla kontenerów, który współpracuje z Amazon Elastic Container Service (ECS) oraz Amazon Elastic Kubernetes Service (EKS). Dzięki niemu nie trzeba prowizjonować, konfigurować ani zarządzać serwerami (instancjami EC2), na których uruchamiane są kontenery. Fargate automatycznie przydziela odpowiednią ilość zasobów obliczeniowych (CPU, RAM) niezbędną do uruchomienia aplikacji.

## Dlaczego to jest ważne i kiedy ma zastosowanie?

Zarządzanie klastrami kontenerów może być skomplikowane i czasochłonne, ponieważ wymaga m.in. łatania systemu operacyjnego, skalowania maszyn wirtualnych w górę i w dół oraz dbania o optymalizację kosztów. AWS Fargate eliminuje te problemy zdejmując z użytkownika obowiązek zarządzania warstwą infrastruktury. Aplikuje się go wtedy, gdy chcemy uruchamiać kontenery (np. aplikacje webowe, mikroserwisy, zadania w tle) i skupić się wyłącznie na ich konfiguracji oraz dostarczaniu kodu.

## Kiedy używać AWS Fargate zamiast AWS Lambda?

Obie usługi (Fargate i Lambda) są bezserwerowe (serverless), jednak różnią się przeznaczeniem i architekturą. Zdecyduj się na AWS Fargate, gdy:

1. **Twój czas wykonywania jest długi (powyżej 15 minut):**
   - AWS Lambda ma twardy limit czasu wykonywania pojedynczej funkcji, który wynosi 15 minut.
   - Kontenery na AWS Fargate mogą działać nieprzerwanie przez dowolnie długi czas.
2. **Aplikacja ma duże wymagania zasobowe:**
   - Lambda ma limity w przydziale zasobów (np. pamięci i procesora dla jednego uruchomienia).
   - Fargate pozwala na przydzielenie i zagwarantowanie większej ilości zasobów na potrzeby bardzo wymagających zadań.
3. **Wymagasz środowiska kontenerowego (Docker):**
   - Jeśli Twoja aplikacja jest już skonteneryzowana w Dockerze i posiada specyficzne zależności systemowe lub wymaga używania niestandardowego systemu operacyjnego.
   - Uruchamianie rozbudowanych aplikacji opartych na językach i frameworkach z dużą ilością zależności.
4. **Masz stały, wysoki lub przewidywalny ruch:**
   - Lambda działa świetnie dla ruchu zmiennego, "szarpanego" (np. wyzwalanie eventami), jednak Fargate w przypadku stałego obciążenia w systemie ciągłym (24/7) może okazać się tańszym i stabilniejszym rozwiązaniem ze względu na uniknięcie problemu tzw. "cold starts" (zimnych startów).

## Główne korzyści z używania AWS Fargate

- **Brak serwerów do zarządzania:** Nie trzeba wybierać typów instancji EC2, pisać skryptów dodających instancje lub zarządzać ich cyklem życia.
- **Bezpieczeństwo z definicji:** Kontenery w Fargate posiadają pełną izolację na poziomie środowiska uruchomieniowego. Nie współdzielą węzła ani kernela systemu z kontenerami innych klientów AWS.
- **Płatność tylko za użycie:** Płacisz wyłącznie za dokładną ilość vCPU, pamięci RAM i przestrzeni dyskowej w czasie realnego działania "Tasków".
- **Skalowalność:** Usługa automatycznie dobierze niezbędną ilość instancji i w płynny sposób weźmie na siebie duże piki zapotrzebowania, zrywając ścisłą zależność od sprzętowej architektury serwera.
