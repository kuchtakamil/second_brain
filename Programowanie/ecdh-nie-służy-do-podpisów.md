# ECDH nie służy do podpisów

**Data:** 2024-01-11

---

**User:**

Czy ECDH używa się do podpisów?

---

**Assistant:**

Algorytm ECDH (Elliptic Curve Diffie-Hellman) jest używany głównie do bezpiecznego ustanawiania wspólnego klucza między dwoma stronami w kryptografii opartej na krzywych eliptycznych. Jego głównym zastosowaniem jest szyfrowanie i zapewnianie bezpiecznego kanału komunikacji, a nie podpisywanie cyfrowe.

Do celów podpisów cyfrowych wykorzystuje się inne algorytmy oparte na krzywych eliptycznych, takie jak ECDSA (Elliptic Curve Digital Signature Algorithm) lub EdDSA (Edwards-curve Digital Signature Algorithm). Te algorytmy są specjalnie zaprojektowane do tworzenia i weryfikacji podpisów cyfrowych, zapewniając autentyczność, integralność i niezaprzeczalność danych.