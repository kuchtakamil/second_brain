# Dodaj importy Kafka.

**Data:** 2023-03-22

---

**User:**

Dodaj importy do tego kodu
trait Record[K, V] {
  def topic: String
  def key(value: V): K
  def timestamp(value: V): Long
}

object Producer {
  def apply[V] = new ProducerBuilder[V]
  class ProducerBuilder[V] {
    def apply[K](config: Properties)(implicit record: Record[K, V],
                                     keySerializer: Serializer[K],
                                     valueSerializer: Serializer[V]): KafkaProducer[K, V] =
      new KafkaProducer(config, keySerializer, valueSerializer)
  }
}

implicit class KafkaProducerOps[K, V](kafkaProducer: KafkaProducer[K, V]) {
  def send(value: V)(implicit record: Record[K, V]): Future[RecordMetadata] = Future {
    kafkaProducer.send(new ProducerRecord(record.topic, null, record.timestamp(value), record.key(value), value)).get()
  }
}

---

**Assistant:**

Oto importy, które mogą zostać dodane do tego kodu:

```scala
import java.util.Properties
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord, RecordMetadata}
import org.apache.kafka.common.serialization.Serializer
import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global
``` 

Te importy są wymagane do obsługi klas `Properties`, `KafkaProducer`, `ProducerRecord`, `RecordMetadata`, `Serializer`, `Future` oraz `ExecutionContext.Implicits.global`.

---

**User:**

Wypisz nazwy zależności których trzeba użyć aby spełnić te importy

---

**Assistant:**

Oto nazwy zależności (dependencies), które trzeba dodać do projektu, aby móc użyć wymienionych importów:

```scala
libraryDependencies ++= Seq(
  "org.apache.kafka" % "kafka-clients" % "<version>", // org.apache.kafka.clients.producer.KafkaProducer, org.apache.kafka.clients.producer.ProducerRecord, org.apache.kafka.clients.producer.RecordMetadata
  "org.scala-lang.modules" %% "scala-xml" % "<version>", // java.util.Properties
  "org.scala-lang.modules" %% "scala-async" % "<version>" // scala.concurrent.Future
)
``` 

Należy uzupełnić `<version>` o numer wersji bibliotek, które chcemy zainstalować. W tym przypadku potrzebujemy biblioteki Kafka `kafka-clients`, oraz modułów Scala `scala-xml` oraz `scala-async`.