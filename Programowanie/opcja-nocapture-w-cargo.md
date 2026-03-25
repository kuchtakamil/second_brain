# Opcja --nocapture w cargo

**Data:** 2025-01-15

---

**User:**

Co robi opcja nocapture w cargo test -- --nocapture

---

**Assistant:**

Opcja `--nocapture` w poleceniu `cargo test` jest używana do wyłączenia przechwytywania wyjścia standardowego (`stdout`) oraz standardowego błędu (`stderr`) w trakcie wykonywania testów. Domyślnie, podczas uruchamiania testów w Rust za pomocą `cargo test`, ich wyjście jest przechwytywane i wyświetlane tylko wtedy, gdy test zakończy się niepowodzeniem. Jeśli test przejdzie pomyślnie, jego wyjście nie jest widoczne.

Kiedy używasz `--nocapture`, możesz zobaczyć wszystkie komunikaty wyjściowe generowane przez testy, nawet jeśli zakończyły się one sukcesem. Jest to szczególnie przydatne podczas debugowania, gdy chcesz zobaczyć informacje diagnostyczne (np. za pomocą `println!`), które normalnie nie byłyby widoczne.

### Przykład

```rust
#[test]
fn example_test() {
    println!("This is a debug message");
    assert_eq!(2 + 2, 4);
}
```

Uruchomienie:

```bash
cargo test -- --nocapture
```

Wyjście (jeśli test przejdzie pomyślnie):

```
running 1 test
This is a debug message
test example_test ... ok
```

Bez `--nocapture` wyjście `println!` nie zostałoby pokazane, jeśli test zakończyłby się sukcesem.

### Podsumowanie
Opcja `--nocapture` ułatwia śledzenie zachowania testów i analizowanie ich wyjścia podczas pracy nad kodem.