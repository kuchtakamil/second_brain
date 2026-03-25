# jak sprawdzić czy dany router może mieć wgrany OpenWRT?

**Data:** 14 sty 2026, 20:25:34 CET

---

**User:**

jak sprawdzić czy dany router może mieć wgrany OpenWRT?

---

**Gemini:**

Sprawdzenie kompatybilności routera z systemem OpenWrt wymaga weryfikacji specyfikacji sprzętowej, ponieważ wsparcie zależy nie tylko od modelu, ale często od konkretnej rewizji sprzętowej (Hardware Revision).

### 1. Oficjalne bazy danych (Primary Check)

Najbardziej wiarygodnym źródłem jest **Table of Hardware (ToH)** oraz **Firmware Selector**.

- **OpenWrt Table of Hardware:** Pozwala na filtrowanie urządzeń po marce, modelu i wersji. Szukaj statusu „supported” lub „wip” (work in progress).
- **OpenWrt Firmware Selector:** Narzędzie to pozwala wpisać nazwę modelu i sprawdzić, czy istnieją gotowe obrazy do pobrania. Jeśli model znajduje się na liście, router jest wspierany.

### 2. Weryfikacja rewizji sprzętowej (Crucial)

Routery tego samego modelu mogą mieć różne wnętrzności (SoC, RAM, Flash) w zależności od daty produkcji. Na naklejce znamionowej routera (pod spodem urządzenia) szukaj oznaczeń typu **Ver: 1.2**, **V2**, **Rev. B1**.

> **Uwaga:** Jeśli ToH podaje wsparcie dla `v1`, a Ty posiadasz `v2`, istnieje duże prawdopodobieństwo, że oprogramowanie nie zadziała lub „ucegli” (brick) urządzenie, dopóki deweloperzy nie dodadzą obsługi nowego chipsetu.

### 3. Analiza specyfikacji technicznej (Advanced)

Jeśli urządzenia nie ma w bazie, możesz ocenić szanse na wsparcie analizując jego architekturę:

- **Procesor (SoC):** \* **MediaTek (Filogic/MT7621/MT7622):** Obecnie najlepsze wsparcie, otwarte sterowniki WiFi.
  - **Qualcomm/Atheros (IPQ40xx/IPQ80xx):** Bardzo dobre wsparcie, stabilne sterowniki.
  - **Broadcom:** Bardzo problematyczne. OpenWrt rzadko wspiera WiFi w chipach Broadcom z powodu braku otwartej dokumentacji i sterowników (tzw. „binary blobs”).
  - **Realtek:** Wsparcie jest ograniczone i często wymaga portów społecznościowych.
- **Pamięć Flash:** \* **Minimum (2026):** 16 MB.
  - **Rekomendowane:** 32 MB lub więcej (NAND Flash).
  - Urządzenia z 8 MB Flash są wycofywane ze wsparcia (tzw. *8/64 warning*), ponieważ nie mieszczą nowoczesnych jąder Linuxa i interfejsu LuCI.
- **Pamięć RAM:** \* **Minimum:** 128 MB.
  - **Rekomendowane:** 256 MB - 512 MB+ dla obsługi OpenVPN/WireGuard, SQM lub systemów AdBlock.

### 4. Sprawdzenie typu bootloadera

Niektóre routery (np. nowsze modele TP-Link, niektóre urządzenia operatorów) mają **zablokowany bootloader** lub wymagają podpisanego cyfrowo oprogramowania. W takim przypadku, nawet jeśli procesor jest wspierany, wgranie OpenWrt może wymagać:

1. Użycia programatora programującego kość Flash bezpośrednio.
2. Wykorzystania luki w oprogramowaniu oryginalnym (exploit).
3. Dostępu przez port szeregowy **UART**.

### 5. Skrypty i narzędzia diagnostyczne

Jeśli masz już dostęp do konsoli routera (np. przez SSH lub Telnet na fabrycznym sofcie), możesz sprawdzić parametry sprzętowe bezpośrednio:

```
# Sprawdzenie modelu procesora
cat /proc/cpuinfo

# Sprawdzenie ilości dostępnej pamięci RAM
free -m

# Lista partycji i rozmiar pamięci Flash
cat /proc/mtd
```

### 6. Źródła społecznościowe

W Polsce niezwykle istotnym źródłem jest portal **eko.one.pl**, prowadzony przez Cezarego Jackiewicza. Zawiera on zoptymalizowane pod polski rynek obrazy OpenWrt oraz bardzo szczegółowe forum, na którym opisywane są problemy z konkretnymi rewizjami routerów dostępnych w polskich sklepach.

---

Czy chciałbyś, abym sprawdził kompatybilność konkretnego modelu routera, który planujesz kupić lub już posiadasz?