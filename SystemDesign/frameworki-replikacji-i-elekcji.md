# Frameworki replikacji i elekcji lidera dla własnych serwisów

## Krótkie podsumowanie

Mechanizmy replikacji danych i elekcji lidera kojarzymy głównie z bazami danych (PostgreSQL Streaming Replication, MySQL Group Replication) oraz brokerami wiadomości (Kafka ISR, kontroler). Jednak **nie trzeba pisać tych algorytmów od zera** — istnieją gotowe frameworki i biblioteki, dzięki którym można wbudować te mechanizmy bezpośrednio w swój serwis napisany np. w Javie lub Pythonie.

Kluczowe pojęcia:
*   **Replikacja** — utrzymywanie kopii danych/stanu na wielu węzłach w celu zapewnienia odporności na awarie (fault tolerance) i wysokiej dostępności.
*   **Elekcja lidera (Leader Election)** — proces, w którym grupa węzłów wybiera jeden węzeł jako "lidera", odpowiedzialnego za koordynację operacji (np. zapisy, podejmowanie decyzji).
*   **Consensus (Konsensus)** — algorytm, dzięki któremu rozproszone węzły uzgadniają wspólną wartość (np. kto jest liderem, jaki jest aktualny stan). Najpopularniejsze: **Raft** i **Paxos**.

## Dlaczego to ma znaczenie / Kiedy to stosować?

Potrzebujesz tych mechanizmów, gdy budujesz **stanowy (stateful) serwis rozproszony**, który musi:
*   przetrwać awarię pojedynczego węzła bez utraty danych,
*   zapewnić, że dokładnie jeden węzeł w danym momencie pełni rolę lidera (np. scheduler, koordynator zadań),
*   replikować stan pomiędzy instancjami bez zewnętrznej bazy danych.

Typowe przypadki użycia:
*   Rozproszony scheduler/cron, który nie powinien duplikować zadań
*   Koordynacja dostępu do współdzielonych zasobów (distributed lock)
*   Własny broker wiadomości lub cache z replikacją
*   Serwisy, które muszą utrzymywać spójny stan in-memory pomiędzy węzłami

## Frameworki i biblioteki — przegląd

### 1. Apache ZooKeeper (Java, Python)

**Co to jest:** Rozproszony serwis koordynacyjny, używany m.in. przez Kafka (do wersji 2.8) i Hadoop. Udostępnia prymitywy: elekcję lidera, rozproszone blokady, zarządzanie konfiguracją.

**Jak działa:** ZooKeeper działa jako **zewnętrzny klaster**, a Twój serwis łączy się z nim jako klient. Wykorzystuje algorytm **ZAB (ZooKeeper Atomic Broadcast)** — wariant Paxosa.

```java
// Java — elekcja lidera z Apache Curator (wrapper nad ZooKeeper)
CuratorFramework client = CuratorFrameworkFactory.newClient(
    "zk1:2181,zk2:2181,zk3:2181", new ExponentialBackoffRetry(1000, 3));
client.start();

LeaderSelector selector = new LeaderSelector(client, "/leader-election", 
    new LeaderSelectorListenerAdapter() {
        @Override
        public void takeLeadership(CuratorFramework client) throws Exception {
            System.out.println("Jestem liderem! Rozpoczynam koordynację...");
            // Logika lidera — ta metoda blokuje, dopóki węzeł jest liderem
            Thread.sleep(Long.MAX_VALUE);
        }
    });
selector.autoRequeue(); // automatycznie ponownie startuje w wyborach po utracie lidera
selector.start();
```

```python
# Python — elekcja lidera z kazoo (klient ZooKeeper)
from kazoo.client import KazooClient
from kazoo.recipe.election import Election

zk = KazooClient(hosts='zk1:2181,zk2:2181,zk3:2181')
zk.start()

election = Election(zk, "/leader-election")

def leader_function():
    print("Jestem liderem!")
    # Logika lidera...

election.run(leader_function)
```

**Wady:** Wymaga utrzymywania **osobnego klastra ZooKeeper** (3–5 węzłów). Dodaje złożoność operacyjną.

---

### 2. etcd + klient (Java, Python, Go)

**Co to jest:** Rozproszony magazyn klucz-wartość używany przez Kubernetes do przechowywania stanu klastra. Posiada wbudowaną elekcję lidera i rozproszone blokady.

**Jak działa:** Podobnie jak ZooKeeper — **zewnętrzny klaster** etcd, do którego łączy się Twój serwis. Wykorzystuje algorytm **Raft**.

```python
# Python — elekcja lidera z etcd3
import etcd3

client = etcd3.client(host='etcd-host', port=2379)

# Lease = "dzierżawa" — lider musi ją odnawiać, inaczej traci przywództwo
lease = client.lease(ttl=10)

# Próba zostania liderem — atomowa operacja put-if-absent
status, _ = client.put_if_not_exists('/service/leader', b'node-1', lease)
if status:
    print("Zostałem liderem!")
    # Odnawiaj lease w tle
else:
    print("Jest już inny lider, czekam...")
    # Watch na klucz /service/leader i czekaj na jego wygaśnięcie
```

**Zalety:** Jeśli już korzystasz z Kubernetes, etcd jest naturalnym wyborem — nie musisz stawiać dodatkowej infrastruktury.

---

### 3. Apache Ratis (Java) — wbudowany Raft

**Co to jest:** Implementacja algorytmu **Raft** w Javie, zaprojektowana do **osadzenia bezpośrednio** w Twoim serwisie. Nie wymaga zewnętrznego klastra.

**Jak działa:** Twój serwis sam staje się węzłem klastra Raft. Ratis zarządza elekcją lidera, replikacją logów i konsensusem. Używa go m.in. Apache Ozone (distributed storage).

```java
// Java — serwis z wbudowanym Raft (Apache Ratis)
RaftProperties properties = new RaftProperties();
RaftServer server = RaftServer.newBuilder()
    .setGroup(RaftGroup.valueOf(
        RaftGroupId.randomId(),
        List.of(peer1, peer2, peer3)))   // 3 węzły klastra
    .setServerId(myPeerId)
    .setProperties(properties)
    .setStateMachine(new MyStateMachine())  // Twoja logika biznesowa
    .build();
server.start();

// MyStateMachine implementuje StateMachine interface
// Raft gwarantuje, że wpisy są replikowane i aplikowane w tej samej kolejności
// na wszystkich węzłach
```

**Kluczowa cecha:** Brak zewnętrznych zależności infrastrukturalnych — Twój serwis **sam jest klastrem**. To podejście jest analogiczne do tego, jak działa Kafka KRaft (od wersji 3.x).

---

### 4. JGroups (Java)

**Co to jest:** Toolkit do komunikacji grupowej w Javie, używany m.in. przez WildFly/JBoss, Infinispan i Hibernate (second-level cache). Oferuje niezawodny multicast, membership detection, elekcję lidera.

```java
// Java — formowanie klastra z JGroups
JChannel channel = new JChannel("udp.xml"); // protokół komunikacji
channel.setReceiver(new ReceiverAdapter() {
    @Override
    public void viewAccepted(View view) {
        // Pierwszy członek widoku to lider (deterministyczna elekcja)
        Address leader = view.getMembers().get(0);
        boolean iAmLeader = leader.equals(channel.getAddress());
        System.out.println("Lider: " + leader + ", ja jestem liderem: " + iAmLeader);
    }

    @Override
    public void receive(Message msg) {
        System.out.println("Otrzymano: " + msg.getObject());
    }
});
channel.connect("my-cluster");
```

**Zalety:** Bardzo dojrzała biblioteka (rozwijana od 1999 r.), lekka, wbudowywana w aplikację. Idealna do klastrowania serwisów Java EE / Jakarta EE.

---

### 5. Atomix / Copycat (Java)

**Co to jest:** Framework do budowy odpornych na awarie rozproszonych systemów w Javie, oparty na algorytmie **Raft**. Oferuje wyżej-poziomowe abstrakcje: rozproszone mapy, zbiory, blokady, elekcję lidera.

```java
// Java — rozproszona mapa i elekcja lidera z Atomix
Atomix atomix = Atomix.builder()
    .withMemberId("node-1")
    .withAddress("10.0.0.1:5679")
    .withMembershipProvider(BootstrapDiscoveryProvider.builder()
        .withNodes(Node.builder().withId("node-1").withAddress("10.0.0.1:5679").build(),
                   Node.builder().withId("node-2").withAddress("10.0.0.2:5679").build())
        .build())
    .build();
atomix.start().join();

// Elekcja lidera
LeaderElection<String> election = atomix.getLeaderElection("my-election");
Leadership<String> leadership = election.run("node-1");
if (leadership.leader().id().equals("node-1")) {
    System.out.println("Jestem liderem!");
}
```

---

### 6. PySyncObj (Python) — wbudowany Raft

**Co to jest:** Lekka biblioteka Pythona implementująca algorytm **Raft**. Pozwala na replikację stanu obiektu Pythona między wieloma węzłami — **bez żadnych zewnętrznych zależności**.

```python
# Python — replikowany licznik z PySyncObj
from pysyncobj import SyncObj, SyncObjConf, replicated

class ReplicatedCounter(SyncObj):
    def __init__(self, self_addr, partners):
        super().__init__(self_addr, partners)
        self.__counter = 0

    @replicated
    def increment(self):
        """Ta metoda jest replikowana na wszystkie węzły w klastrze."""
        self.__counter += 1

    def get_value(self):
        return self.__counter

# Uruchomienie na 3 węzłach:
# Węzeł 1:
counter = ReplicatedCounter('node1:4321', ['node2:4322', 'node3:4323'])
# Węzeł 2:
# counter = ReplicatedCounter('node2:4322', ['node1:4321', 'node3:4323'])

# Zapis (replikowany przez Raft)
counter.increment()
print(counter.get_value())  # Spójna wartość na wszystkich węzłach
```

**Kluczowa cecha:** Ekstremalnie proste API — dekorator `@replicated` automatycznie replikuje wywołania metod. Idealne do prototypowania i mniejszych systemów.

---

## Porównanie podejść

| Kryterium | Zewnętrzny klaster (ZooKeeper/etcd) | Wbudowany Raft (Ratis/PySyncObj/JGroups) |
|---|---|---|
| **Złożoność operacyjna** | Wysoka — osobny klaster do utrzymania | Niska — Twój serwis = klaster |
| **Skalowalność** | Współdzielony przez wiele serwisów | Dedykowany per serwis |
| **Dojrzałość** | Bardzo wysoka (ZK: 2010+, etcd: 2013+) | Zróżnicowana (JGroups: 1999+, Ratis: 2017+) |
| **Elastyczność** | Ograniczona do API koordynatora | Pełna — replika dowolnego stanu |
| **Język** | Wielojęzyczne klienty | Zwykle jeden język (Java/Python) |

## Kiedy co wybrać?

*   **Potrzebujesz tylko elekcji lidera / distributed lock** → ZooKeeper (z Curator) lub etcd
*   **Chcesz replikować stan in-memory bez zewnętrznych zależności** → PySyncObj (Python), Apache Ratis (Java)
*   **Budujesz klaster Java EE / potrzebujesz group communication** → JGroups
*   **Masz już Kubernetes** → etcd (jest już dostępny)
*   **Prototypujesz w Pythonie** → PySyncObj (najprostsze API)

## Powiązane pliki

*   [Twierdzenie CAP](cap-theorem.md)
*   [Kafka, RabbitMQ, ActiveMQ, Redis Pub/Sub — porównanie](kafka-rabbitmq-activemq-redis-pubsub.md)
*   [Pytania rekrutacyjne z System Design](system-design-pytania-rekrutacyjne.md)
