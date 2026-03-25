# Bezpieczne przechowywanie haseł

**Data:** 2024-07-23

---

**User:**

W bazie danych muszę trzymać hasło użytkownika. Nie mogę trzymać hashu, bo muszę używać tego hasła. Jak to zrrobić w bezpieczny sposób?

---

**Assistant:**

Przechowywanie hasła użytkownika w bazie danych w taki sposób, aby było możliwe jego późniejsze użycie, to zadanie wymagające szczególnej ostrożności z punktu widzenia bezpieczeństwa. Oto kilka kroków, które możesz podjąć, aby zminimalizować ryzyko:

1. **Szyfrowanie symetryczne**: Zaszyfruj hasło użytkownika przy użyciu algorytmu szyfrowania symetrycznego, takiego jak AES (Advanced Encryption Standard). Klucz szyfrowania musi być bezpiecznie przechowywany.

2. **Bezpieczne przechowywanie klucza szyfrującego**: Klucz używany do szyfrowania powinien być przechowywany w bezpiecznym miejscu, takim jak:
   - Hardware Security Module (HSM)
   - Specjalizowane usługi w chmurze (np. AWS KMS, Azure Key Vault, Google Cloud KMS)
   - Plik konfiguracyjny, który jest odpowiednio chroniony, np. przez system operacyjny lub inny mechanizm ochrony dostępu

3. **Użycie inicjalizatora (IV)**: W przypadku stosowania AES w trybie, który tego wymaga (np. CBC), generuj losowy inicjalizator (IV) dla każdego zaszyfrowanego hasła i przechowuj go razem z zaszyfrowanym hasłem. IV nie musi być trzymany w tajemnicy, ale musi być unikalny dla każdego szyfrowanego tekstu.

4. **Bezpieczne przesyłanie danych**: Zapewnij, aby dane były przesyłane między klientem a serwerem za pomocą bezpiecznych protokołów, takich jak HTTPS, aby uniemożliwić przechwycenie haseł w trakcie transmisji.

5. **Ochrona bazy danych**: Zadbaj o to, aby baza danych była odpowiednio zabezpieczona:
   - Ogranicz dostęp tylko do autoryzowanych użytkowników i aplikacji.
   - Stosuj mechanizmy monitorowania i logowania prób dostępu.
   - Regularnie aktualizuj oprogramowanie bazy danych.

### Przykład implementacji szyfrowania hasła w Pythonie

Poniżej przedstawiam przykładowy kod w Pythonie, który pokazuje, jak zaszyfrować i odszyfrować hasło przy użyciu biblioteki `cryptography`:

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import os
import base64

# Generowanie klucza szyfrowania
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Szyfrowanie hasła
def encrypt_password(password, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()
    return iv + encrypted_password

# Odszyfrowywanie hasła
def decrypt_password(encrypted_password, key):
    iv = encrypted_password[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted_password[16:]) + decryptor.finalize()
    return decrypted_password.decode()

# Przykładowe użycie
password = "super_secret_password"
salt = os.urandom(16)
key = generate_key("user_master_password", salt)

encrypted_password = encrypt_password(password, key)
print(f"Zaszyfrowane hasło: {encrypted_password}")

decrypted_password = decrypt_password(encrypted_password, key)
print(f"Odszyfrowane hasło: {decrypted_password}")
```

W powyższym kodzie:
- `generate_key` generuje klucz szyfrowania na podstawie hasła użytkownika i soli.
- `encrypt_password` szyfruje hasło za pomocą klucza i zwraca zaszyfrowane hasło.
- `decrypt_password` odszyfrowuje hasło za pomocą klucza.

Pamiętaj, aby zawsze stosować najnowsze i najlepiej sprawdzone praktyki bezpieczeństwa, a także regularnie przeglądać i aktualizować swoje mechanizmy ochrony danych.