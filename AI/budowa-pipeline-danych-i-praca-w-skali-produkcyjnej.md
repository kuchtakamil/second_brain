# Budowa potoków danych (Data Pipelines) i praca z danymi w skali produkcyjnej

## 1. Czym to jest?
Praca z danymi w skali produkcyjnej (Data Engineering w skali) to zestaw praktyk, narzędzi i architektur pozwalających na niezawodne, skalowalne i zautomatyzowane przetwarzanie ogromnych ilości danych. Obejmuje to pobieranie danych ze źródeł (Ingestion), ich transformację (Processing/Transformation) oraz zapis w miejscu docelowym (Storage/Serving). Data pipeline (potok danych) to zautomatyzowany przepływ danych przez te etapy, zapewniający, że biznes otrzymuje informacje w odpowiednim czasie.

## 2. Dlaczego to ma znaczenie?
W środowiskach produkcyjnych (Big Data / Enterprise) dane płyną w sposób ciągły (strumieniowo) lub wsadowo (batchowo) w ogromnych wolumenach (TB/PB). Stawia to specyficzne wyzwania:
- **Niezawodność i Powtarzalność:** Awarie poszczególnych maszyn czy komponentów (procesów) na klastrze nie mogą powodować utraty danych. Obliczenia powinny być idempotentne.
- **Odporność na błędy (Fault tolerance):** Systemy muszą logicznie reagować na wadliwe czy zniekształcone dane wejściowe.
- **Skalowalność i Optymalizacja:** Wzrost ilości danych nie powinien obniżać wydajności do poziomu krytycznego ani wykładniczo zwiększać kosztów infrastruktury chmurowej.
- **Data Quality:** Zapewnienie poprawności, kompletności i aktualności danych trafiających do aplikacji, systemów ML czy raportów.

## 3. Jak to działa? (Architektura i Narzędzia)

Klasyczne podejście do potoków danych dzieli się na kilka etapów (zazwyczaj w paradygmatach **ETL** - Extract, Transform, Load, lub nowszym **ELT**):

### A. Pobieranie / Ekstrakcja danych (Ingestion)
Polega na podłączeniu się do źródeł operacyjnych (bazy SQL/NoSQL, zewnętrzne API, logi serwerowe, systemy e-commerce).
- **Batch Processing:** dane pobierane są cyklicznie, w paczkach (np. co godzinę, co noc). 
- **Stream/Real-time Processing:** zdarzenia są odczytywane i przechwytywane natychmiast po ich wytworzeniu. Narzędzia: **Apache Kafka**, **RabbitMQ**, **AWS Kinesis**.

### B. Przechowywanie (Storage)
Przechowywanie terabajtów informacji w relacyjnych bazach jest z reguły nieefektywne. Typowe struktury w data engineeringu to:
- **Data Lake (Jezioro Danych):** miejsce do przechowywania surowych i nieustrukturyzowanych danych na obiektowych magazynach chmurowych (AWS S3, Google Cloud Storage, Azure Blob Storage, on-prem: HDFS).
- **Data Warehouse (Hurtownia Danych):** wysoce ustrukturyzowane zbiory danych zoptymalizowane pod szybką analitykę i SQL (Google BigQuery, Snowflake, Amazon Redshift).
- **Data Lakehouse:** innowacyjne podejście łączące niski koszt "jezior" z możliwościami ACID i indeksowania hurtowni, np. **Apache Iceberg**, **Delta Lake** (często skojarzone z platformą Databricks).

### C. Przetwarzanie i Transformacja (Processing)
Czyszczenie danych, odfiltrowywanie szumów, rzutowanie formatów i agreagcje do postaci użytecznej analitycznie (często w ramach struktury medalionowej m.in. zasada *Bronze/Silver/Gold*).
- Systemy rozproszone dla Big Data: **Apache Spark** (niekwestionowany standard branżowy), **Apache Flink** (świetny w prawdziwym streamingu strumieniowym).
- W świecie ELT, dla transformacji odbywających się prosto w hurtowni z użyciem SQL wykorzystuje się potężne narzędzie jakim jest **dbt** (Data Build Tool).

### D. Orkiestracja i Monitorowanie (Orchestration & Observability)
Najważniejszy punkt układanki sprawiający, że zależności układają się w czytelny potok. Troszczy się o kolejność (tworząc graf zależności np. DAGów), podnosi potoki po błędzie i wyzwala alarmy w razie niepowodzenia.
- Narzędzia: **Apache Airflow**, **Dagster**, **Prefect**.

---

## 4. Przykładowa koncepcja (Zarys działania PySpark na Data Lake)
```python
# Pseudo-kod obrazujący krok transformacji w PySpark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

spark = SparkSession.builder.appName("TransactionsETL").getOrCreate()

# 1. Odczyt surowych zdarzeń json (Warstwa Bronze / Data Lake)
raw_df = spark.read.json("s3://moje-jezioro/raw/transactions/date=2026-03-18/")

# 2. Czyszczenie i transformacja (odrzucenie uszkodzonych, wzbogacenie złączeniem itp.)
clean_df = raw_df.filter(col("amount") > 0.0) \
                 .withColumn("processed_at", current_timestamp())

# 3. Zapis gotowych danych pod postacią użyteczną analitycznie 
#    w formacie kolumnowym (Warstwa Silver / Parquet / Delta)
clean_df.write.format("delta") \
        .mode("append") \
        .save("s3://moje-jezioro-delta/silver/transactions/")
```

---

## 5. Lista pytań rekrutacyjnych bez odpowiedzi

Poniżej znajduje się lista propozycji pytań rekrutacyjnych (od Mid po Seniora) sprawdzających głębię wiedzy z zakresu potoków danych:

1. Jaka jest różnica między podejściem **ETL** a **ELT**? W jakich sytuacjach lepiej sprawdzi się jedno, a kiedy drugie?
2. Co oznacza pojęcie "idempotentności" w potokach danych (zwłaszcza w odniesieniu np. do Apache Airflow)? Dlaczego jest to kluczowy koncept przy projektowaniu zadań?
3. Pojawia się problem z bardzo wolno działającym połączniem ogromnej tabeli z inną, nieco mniejszą w Apache Spark. Czym są problemy związane z *Data Skewness* (przechyleniem, skośnością danych) oraz klasycznym *Shuffle*?
4. Wyobraź sobie, że w zadaniu (jobie) Sparka/Hadoop przetwarzającym dane wsadowo za ostatnie pół roku nagle zaczyna wyskakiwać błąd *OOM (Out Of Memory)*. Jakie kroki podejmiesz, by go zdiagnozować i usunąć?
5. Czym różnią się ustrukturyzowane hurtownie danych (Data Warehouse) od jezior danych (Data Lake)? Czym w tym równaniu są "rozwiązania Lakehouse" (np. Delta Lake lub Apache Iceberg)?
6. Wyjaśnij różnice w przetwarzaniu **batch** (wsadowym) a **streaming** (strumieniowym). Jak obsłużyłbyś zjawisko tak zwanego "late arriving data" przy przetwarzaniu w obrębie okien czasowych (np. we Flinku)?
7. Czym kierujesz się dobierając metodę i wiodące klucze partycjonowania przy zapisie danych (np. na S3), gdy wiesz, że przyrost wynosi po kilka Terabajtów miesięcznie?
8. W jaki sposób zapewniasz jakość danych (*Data Quality*) na produkcji, by upewnić się, że niekompletne lub nielogiczne dane nie wypłyną w tabelach docelowych dla dashboardów BI?
9. Którego z popularnych formatów plików (np. CSV, JSON, Parquet, Avro, ORC) użyłbyś do składowania wynikowego, wielotablicowego zbioru danych analitycznych (OLAP) w S3 a którego na poziomie brokera wiadomości jak Kafka? Uzasadnij wybór.
10. Jak rozwiązujesz problem re-procesowania (backfillingu) danych historycznych po zmianach ewolucyjnych w kodzie - kiedy pojawia się potrzeba przeliczenia logiki od nowa za miniony miesiąc bez niszczenia w tym samym czasie dostępu produkcyjnego innym działom?
