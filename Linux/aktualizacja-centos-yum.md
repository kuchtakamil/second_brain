# Aktualizacja CentOS yum

**Data:** 2024-01-25

---

**User:**

centos
yum makecache
co później żeby uaktualnić wszystko?

---

**Assistant:**

Po wykonaniu komendy `yum makecache` w systemie CentOS, która aktualizuje lokalną pamięć podręczną repozytoriów, aby uaktualnić wszystkie pakiety na systemie, powinieneś użyć następującej komendy:

```
sudo yum update
```

To spowoduje sprawdzenie dostępnych aktualizacji dla wszystkich zainstalowanych pakietów i zainstalowanie ich. Jeśli chcesz tylko sprawdzić, czy są dostępne aktualizacje, bez ich instalowania, możesz użyć:

```
sudo yum check-update
```

Pamiętaj, że przed wykonaniem aktualizacji zaleca się wykonanie kopii zapasowej ważnych danych.

---

**User:**

RHEL. Chcę dodać użytkownika kamil do grupy vboxsf

---

**Assistant:**

Aby dodać użytkownika o nazwie "kamil" do grupy "vboxsf" w systemie Red Hat Enterprise Linux (RHEL), możesz użyć poniższej komendy. Ta komenda doda użytkownika do grupy bez usuwania go z obecnych grup, do których należy:

```bash
sudo usermod -a -G vboxsf kamil
```

Oto co robi każdy element komendy:
- `sudo`: Uruchamia komendę z uprawnieniami administratora.
- `usermod`: Narzędzie do modyfikowania kont użytkowników.
- `-a`: Opcja, która oznacza "append" (dodaj), używana do dodawania użytkownika do grupy bez usuwania go z innych grup.
- `-G`: Oznacza grupy, do których użytkownik ma być dodany.
- `vboxsf`: Nazwa grupy, do której dodajesz użytkownika.
- `kamil`: Nazwa użytkownika, którego chcesz dodać do grupy.

Po wykonaniu tej komendy, użytkownik "kamil" będzie członkiem grupy "vboxsf". Aby zmiany weszły w życie, użytkownik "kamil" może potrzebować ponownego zalogowania się do systemu.