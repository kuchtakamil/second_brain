# Perfume marketplace app

**Data:** 2025-08-30

---

**User:**

Chcę przy pomocy narzędzia AI stworzyć web aplikację służącą do sprzedawania i kupowania perfum w różnych ich rodzajach przez internet.
Poniżej podam szczegóły aplikacji. Napisz po angielsku w rozdziałach i podrozdziałach jak powinna działać i wyglądać aplikacja. Możesz lekko sparafrazować moje wypowiedzi.
Zaczni tłumaczenie od teraz:

Kontekst:
Sprzedaż perfum przez prywatne osoby odbywa się na grupach Facebooka. Sprzedający umieszczają posty na grupach gdzie ogłaszają że mają na sprzedaż perfumy nowe, perfumy z ubytkiem obiętości, odlewki czyli perfumy odlane do innych małych dekantów pojemności np. 5ml oraz próbki perfum wydawane przez producentów. Kupujący przeglądają posty na Facebook i kontaktują się ze Sprzedającymi na Messanger lub w komentarzach do postów.
Problem jaki ma rozwiązywać aplikacja:
Przeglądanie postów na Facebook i wyszukiwanie perfum które chce się zakupić jest kłopotliwe. Trudno się wyszukuje perfumy które chce się kupić. Stare posty szybko są zastępowane nowymi więc aby zobaczyć co jest do sprzedania trzeba przewijać dużo stron/postów. Nie można rozróżnić czy szuka się nowego flakonu, ubytkowego czy odlewki. Aplikacja w dalszych planach ma rozwiązywać problem sprzedaży prodróbek. W pierwszym etapie możliwa ma być weryfikacja sprzedawanych perfum przez moderatora - człowiek. W dalszej przyszłości aplikacji LLM na podstawie zdjęć może decydować czy towar jest podróbką. 

1. Użytkownik może się zarejstrować lub zalogować.
2. Każdy użytkownik może być Kupującym oraz Sprzedającym. Aby zostać Sprzedającym nie są potrzebne specjalne uprawnienia w aplikacji. 
3. Każdy użytkownik jako Kupujący może wyświetlać perfumy wystawione na sprzedaż. Może również wyszukać perfumy po nazwie z uwzględnieniem czy szuka nowych perfum, ubytkowych, odlewek czy próbek.
4. Użytkownik jako Sprzedający może sprzedać perfumy jako nowe, ubytkowe, odlewki lub próbki. W ogłoszeniu musi podana być cena, objętość, zdjęcie, opcjonalnie opis.
5. Użytkownik jako kupujący może złożyć prośbę o weryfikacji oryginalności perfum w ogłoszeniu przez moderatora na podstawie zdjęcia. Ocena moderatora jest widoczna w ogłoszeniu dla wszystkich.
6. Istnieje system ocen sprzedających.
7. Każde perfumy a właściwie każde ogłoszenie ma swoje odniesienie do perfum na fragrantica.com. Użytkownik może kliknąć w link do fragrantica aby zapoznać się z profilem perfum na fragrantica.
8. Sprzedający może dodać ogłoszenie korzystając ze specjalnego panelu do dodawania ogłoszeń.
9. Autor aplikacji zarabia na wyświetlanych kontekstowych reklamach. Reklamy nie mogą być natarczywe i przeszkadzać użytkownikowi.

---

**Assistant:**

Here’s a structured English version of your concept, organized into chapters and subchapters for clarity:  

---

# Perfume Marketplace Web Application  

## 1. Context and Motivation  
### 1.1 Current Situation  
At present, the resale and exchange of perfumes among private individuals often takes place in Facebook groups. Sellers post announcements offering different types of perfumes:  
- **New bottles**  
- **Partial bottles** (with some liquid already used)  
- **Decants** (perfume poured into small containers, e.g., 5 ml)  
- **Samples** provided by manufacturers  

Buyers browse posts and contact sellers via Facebook Messenger or post comments.  

### 1.2 Problem Statement  
The process on Facebook is cumbersome:  
- Searching for a specific perfume is difficult.  
- Older posts are quickly pushed down by new ones.  
- Browsing requires endless scrolling.  
- There is no clear distinction between new bottles, partial bottles, decants, or samples.  
- The risk of counterfeit perfumes is high, with no reliable way to verify authenticity.  

### 1.3 Goal of the Application  
The application will streamline the buying and selling of perfumes by providing:  
- A dedicated marketplace with clear categorization.  
- Search and filtering capabilities.  
- Seller verification and moderation.  
- Future AI-driven counterfeit detection based on images.  

---

## 2. User Accounts and Roles  
### 2.1 Registration and Login  
- Users can create an account by registering with an email or social login.  
- Registered users can log in securely.  

### 2.2 User Roles  
- Every user can act as both a **Buyer** and a **Seller**.  
- No special permissions are required to start selling.  

---

## 3. Buyer Features  
### 3.1 Browsing and Searching  
- Buyers can view all listed perfumes.  
- Search functionality allows filtering by:  
  - Perfume name  
  - Type (new bottle, partial bottle, decant, sample)  

### 3.2 Product Listings  
Each listing must contain:  
- Price  
- Volume  
- Photo(s)  
- Optional description  

### 3.3 Authenticity Verification  
- Buyers can request **manual verification** of authenticity by a moderator.  
- The moderator’s decision is displayed publicly in the listing.  
- In future versions, an AI-powered system (LLM with image analysis) will assist in counterfeit detection.  

### 3.4 Seller Ratings  
- Buyers can rate sellers after a transaction.  
- Ratings are visible to all users, helping to build trust.  

---

## 4. Seller Features  
### 4.1 Creating Listings  
Sellers can create an announcement through a dedicated panel, providing:  
- Perfume type (new, partial, decant, sample)  
- Price  
- Volume  
- Image(s)  
- Optional description  

### 4.2 External Reference  
- Each listing is linked to the corresponding perfume profile on **fragrantica.com**, enabling buyers to learn more about the scent.  

---

## 5. Moderation and Fraud Prevention  
### 5.1 Human Moderation  
- Moderators manually review authenticity requests.  
- Their evaluation is visible to all users.  

### 5.2 Future AI Integration  
- An AI module will analyze uploaded images to detect possible counterfeits.  
- This will reduce reliance on human moderators over time.  

---

## 6. Monetization Model  
- The platform generates revenue through **contextual advertisements**.  
- Ads are carefully integrated to remain non-intrusive and avoid disturbing the user experience.  

---

## 7. Summary of Core Workflow  
1. Users register/login.  
2. Sellers create listings with price, volume, and images.  
3. Buyers browse, search, and filter listings.  
4. Buyers may request authenticity verification.  
5. Moderators review and mark verified listings.  
6. Buyers purchase perfumes and rate sellers.  
7. The platform earns revenue through contextual ads.  

---

Czy chcesz, żebym przygotował to także w formie **pełnej specyfikacji funkcjonalnej (SRS)**, np. z rozdziałami: *Functional Requirements*, *Non-Functional Requirements*, *User Stories*?

---

**User:**

Utwórz tekst w postaci markdown w którym będzie opisany stack technologiczny dla aplikacji. Opisz backkend, forntend, aspekty wdrożenia, zaproponuj technologię CI/CD - najlepiej darmową. Plik ma być zwięzły. Sformatuj tekst w rozdziały, podrozdziały i numeracje ale nie opisuj rzeczy pełnymi zdaniami lecz raczej jako deklaracje. Wszystko w języku angielskim.
Dla backend wybierz Java i nowoczesne frameworki dla Java takie jak Springboot. 
Dla frontend wybierz odpowiednią technologię nadającą się dla takiej aplikacji. Preferowane są frameworki które najczęściej stosowane są do tworzenia komercyjnych aplikacji ecommerce.

---

**Assistant:**

```markdown
# Technology Stack for Perfume Marketplace Application

## 1. Backend
### 1.1 Language & Framework
- Java 21+  
- Spring Boot 3.x  
- Spring Data JPA (Hibernate)  
- Spring Security (JWT-based authentication)  
- Spring Web (REST API)  

### 1.2 Database
- PostgreSQL (primary DB)  
- Redis (caching, sessions)  

### 1.3 API & Communication
- RESTful API  
- JSON payloads  
- OpenAPI/Swagger for documentation  

### 1.4 Other Backend Tools
- MapStruct (DTO mapping)  
- Lombok (boilerplate reduction)  
- Flyway (DB migrations)  

---

## 2. Frontend
### 2.1 Framework
- React 18+ with TypeScript  
- Next.js (SSR + SEO optimization)  

### 2.2 UI & Styling
- TailwindCSS  
- shadcn/ui (components library)  
- Axios (API communication)  

### 2.3 State Management
- Redux Toolkit  
- React Query (server state synchronization)  

---

## 3. Deployment & Infrastructure
### 3.1 Containerization
- Docker (containerization)  
- Docker Compose (local development)  

### 3.2 Orchestration (Optional future stage)
- Kubernetes (scalability)  

### 3.3 Cloud Provider
- AWS Free Tier or Azure Free Tier  
- S3 / Blob Storage (images hosting)  

---

## 4. CI/CD
### 4.1 Version Control
- GitHub  

### 4.2 CI/CD Pipeline
- GitHub Actions (free tier)  
- Workflow:  
  1. Build & Test backend (Maven)  
  2. Build frontend (Node.js)  
  3. Run unit tests  
  4. Docker build & push  
  5. Deploy to cloud (AWS/Azure)  

### 4.3 Monitoring & Logging
- Prometheus + Grafana (metrics)  
- ELK Stack (logging)  

---
```  

Chcesz, żebym przygotował też **diagram architektury systemu** (np. w formie ASCII lub schematu do PlantUML), żeby pokazać jak backend, frontend i baza danych współpracują?