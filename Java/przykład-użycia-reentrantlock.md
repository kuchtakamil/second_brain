# Przykład użycia ReentrantLock

**Data:** 2024-10-06

---

**User:**

W java, podaj przykład użycia ReentrantLock

---

**Assistant:**

`ReentrantLock` w Javie jest klasą, która implementuje mechanizm blokad (ang. *locks*), co pozwala na większą kontrolę nad współbieżnością w porównaniu do synchronizowanych metod i bloków. Poniżej znajduje się przykład użycia `ReentrantLock`:

### Przykład:

```java
import java.util.concurrent.locks.ReentrantLock;

public class BankAccount {
    private double balance;
    private ReentrantLock lock = new ReentrantLock();

    public BankAccount(double initialBalance) {
        this.balance = initialBalance;
    }

    public void deposit(double amount) {
        lock.lock();  // Zablokowanie dostępu do zasobu
        try {
            balance += amount;
            System.out.println(Thread.currentThread().getName() + " deposited: " + amount + " | Balance: " + balance);
        } finally {
            lock.unlock();  // Zawsze zwolnij blokadę w bloku `finally`
        }
    }

    public void withdraw(double amount) {
        lock.lock();  // Zablokowanie dostępu do zasobu
        try {
            if (balance >= amount) {
                balance -= amount;
                System.out.println(Thread.currentThread().getName() + " withdrew: " + amount + " | Balance: " + balance);
            } else {
                System.out.println(Thread.currentThread().getName() + " attempted to withdraw: " + amount + " | Insufficient funds.");
            }
        } finally {
            lock.unlock();  // Zwolnienie blokady
        }
    }

    public double getBalance() {
        lock.lock();
        try {
            return balance;
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) {
        BankAccount account = new BankAccount(1000);

        Runnable task1 = () -> {
            for (int i = 0; i < 5; i++) {
                account.deposit(100);
            }
        };

        Runnable task2 = () -> {
            for (int i = 0; i < 5; i++) {
                account.withdraw(50);
            }
        };

        Thread t1 = new Thread(task1, "Thread 1");
        Thread t2 = new Thread(task2, "Thread 2");

        t1.start();
        t2.start();
    }
}
```

### Wyjaśnienie:

1. `ReentrantLock lock = new ReentrantLock();` — Tworzymy obiekt `ReentrantLock`, który zapewnia mechanizm blokady.
2. `lock.lock()` — Metoda `lock()` blokuje dostęp do sekcji krytycznej, która modyfikuje współdzielone dane.
3. `lock.unlock()` — Po zakończeniu operacji, `unlock()` zwalnia blokadę. Użycie `unlock()` w bloku `finally` gwarantuje, że blokada zostanie zawsze zwolniona, nawet jeśli w sekcji krytycznej wystąpi wyjątek.

Blokady zapewniają większą elastyczność w zarządzaniu współbieżnością w porównaniu do tradycyjnych bloków synchronizacji.