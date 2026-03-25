# RPM Dependency Resolution Issues

**Data:** 2024-01-25

---

**User:**

rpm -i mot-pwvault-app-02.00.00-01.i686.rpm
error: Failed dependencies:
        libc.so.6 is needed by mot-pwvault-app-02.00.00-01.i686
        libc.so.6(GLIBC_2.0) is needed by mot-pwvault-app-02.00.00-01.i686
        libc.so.6(GLIBC_2.1) is needed by mot-pwvault-app-02.00.00-01.i686
        libc.so.6(GLIBC_2.1.2) is needed by mot-pwvault-app-02.00.00-01.i686
        libc.so.6(GLIBC_2.1.3) is needed by mot-pwvault-app-02.00.00-01.i686
        libc.so.6(GLIBC_2.28) is needed by mot-pwvault-app-02.00.00-01.i686
        libcrypto.so.1.1 is needed by mot-pwvault-app-02.00.00-01.i686
        libcrypto.so.1.1(OPENSSL_1_1_0) is needed by mot-pwvault-app-02.00.00-01.i686
        libgcc_s.so.1 is needed by mot-pwvault-app-02.00.00-01.i686
        libgcc_s.so.1(GCC_3.0) is needed by mot-pwvault-app-02.00.00-01.i686
        libm.so.6 is needed by mot-pwvault-app-02.00.00-01.i686
        libstdc++.so.6 is needed by mot-pwvault-app-02.00.00-01.i686
        libstdc++.so.6(CXXABI_1.3) is needed by mot-pwvault-app-02.00.00-01.i686
        libstdc++.so.6(CXXABI_1.3.9) is needed by mot-pwvault-app-02.00.00-01.i686
        libstdc++.so.6(GLIBCXX_3.4) is needed by mot-pwvault-app-02.00.00-01.i686
        libstdc++.so.6(GLIBCXX_3.4.15) is needed by mot-pwvault-app-02.00.00-01.i686
        libstdc++.so.6(GLIBCXX_3.4.20) is needed by mot-pwvault-app-02.00.00-01.i686
        libstdc++.so.6(GLIBCXX_3.4.21) is needed by mot-pwvault-app-02.00.00-01.i686
        libstdc++.so.6(GLIBCXX_3.4.9) is needed by mot-pwvault-app-02.00.00-01.i686

Po iinstalacji
sudo yum install glibc.i686
sudo yum install libstdc++.i686
Próba zainstalowania
rpm -i mot-pwvault-app-02.00.00-01.i686.rpm
daje
error: Failed dependencies:
libc.so.6(GLIBC_2.28) is needed by mot-pwvault-app-02.00.00-01.i686
libcrypto.so.1.1 is needed by mot-pwvault-app-02.00.00-01.i686
libcrypto.so.1.1(OPENSSL_1_1_0) is needed by mot-pwvault-app-02.00.00-01.i686
libstdc++.so.6(CXXABI_1.3.9) is needed by mot-pwvault-app-02.00.00-01.i686
libstdc++.so.6(GLIBCXX_3.4.20) is needed by mot-pwvault-app-02.00.00-01.i686
libstdc++.so.6(GLIBCXX_3.4.21) is needed by mot-pwvault-app-02.00.00-01.i686

---

**Assistant:**

The error messages you're encountering indicate that certain dependencies required by `mot-pwvault-app-02.00.00-01.i686.rpm` are still missing or not at the required versions on your system. You've successfully installed the `glibc.i686` and `libstdc++.i686` packages, which resolved some dependencies, but others remain unresolved.

Here's how you can address the remaining dependency issues:

1. **libc.so.6(GLIBC_2.28)**: This indicates that you need a specific version of GLIBC. You might already have GLIBC installed, but not the required version. You can check your current version using `rpm -q glibc`. If the version is older than 2.28, you'll need to upgrade it. This can be tricky because GLIBC is a core component of Linux systems, and upgrading it might affect other applications. Ensure compatibility with your current system before proceeding.

2. **libcrypto.so.1.1 and libcrypto.so.1.1(OPENSSL_1_1_0)**: These dependencies are related to OpenSSL. You need to install or update the OpenSSL libraries to the required version. You can try installing it with `sudo yum install openssl-libs.i686` or a specific version if required.

3. **libstdc++.so.6(CXXABI_1.3.9), libstdc++.so.6(GLIBCXX_3.4.20), libstdc++.so.6(GLIBCXX_3.4.21)**: These are dependencies related to the GNU Standard C++ Library. Since you've already installed `libstdc++.i686`, it might be that the installed version does not meet the required version criteria. You may need to find and install the specific versions of these libraries.

Remember, managing dependencies for RPM packages manually can be complex, especially when dealing with core libraries like GLIBC and libstdc++. Upgrading these libraries might lead to system instability if not done carefully. Always back up important data before making such changes.

If you have the option to use a package manager like `yum` or `dnf` to install `mot-pwvault-app`, it's generally safer and more convenient, as the package manager automatically resolves dependencies. For instance, you might try `sudo yum localinstall mot-pwvault-app-02.00.00-01.i686.rpm`, which can automatically resolve and install dependencies.

---

**User:**

Więc co mam dalej zrobić

---

**Assistant:**

Rozumiem, że potrzebujesz dalszej pomocy w rozwiązywaniu problemów z zależnościami dla `mot-pwvault-app-02.00.00-01.i686.rpm`. Oto kroki, które możesz podjąć, aby rozwiązać pozostałe problemy z zależnościami:

1. **Aktualizacja GLIBC do wersji 2.28**: 
   - Najpierw sprawdź obecną wersję GLIBC w systemie, wpisując w terminalu: `rpm -q glibc`.
   - Jeśli wersja jest starsza niż 2.28, będziesz musiał ją zaktualizować. Uwaga: Aktualizacja GLIBC może być ryzykowna i wpłynąć na stabilność systemu, dlatego zaleca się zachować ostrożność. Upewnij się, że twoje środowisko (np. dystrybucja Linuxa) jest kompatybilne z nowszą wersją GLIBC.

2. **Instalacja lub aktualizacja OpenSSL (libcrypto)**:
   - Zainstaluj lub zaktualizuj biblioteki OpenSSL do wymaganej wersji, używając komendy: `sudo yum install openssl-libs.i686`. Jeśli to nie zadziała, możesz potrzebować określić konkretną wersję pakietu.

3. **Rozwiązanie problemów z libstdc++**:
   - Sprawdź obecną wersję pakietu libstdc++: `rpm -q libstdc++`.
   - Jeśli wersja nie jest wystarczająca, zaktualizuj ją. Możesz spróbować użyć `sudo yum update libstdc++.i686`, ale może być konieczne znalezienie i instalacja konkretnych wersji tych bibliotek.

Po podjęciu tych kroków, spróbuj ponownie zainstalować pakiet `mot-pwvault-app` używając `rpm -i` lub, co jest bezpieczniejsze, użyj `yum` do instalacji lokalnej, co pozwoli na automatyczne rozwiązanie zależności:

```bash
sudo yum localinstall mot-pwvault-app-02.00.00-01.i686.rpm
```

Jeśli nadal napotykasz problemy, rozważ skontaktowanie się z dostawcą pakietu `mot-pwvault-app` dla wsparcia, ponieważ mogą mieć oni bardziej szczegółowe informacje dotyczące wymagań i zależności ich oprogramowania.