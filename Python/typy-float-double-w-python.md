# Typy `float` i `double` w Pythonie

## Krótkie podsumowanie
W przeciwieństwie do języków takich jak Java, C++ czy C#, w standardowym Pythonie **nie istnieje oddzielny typ wbudowany `double`**. Wbudowany w język typ zmiennoprzecinkowy to po prostu `float`. Pod spodem jednak, w implementacji CPython (która jest najpopularniejszą implementacją Pythona), typ `float` jest w rzeczywistości zaimplementowany pod maską przy użyciu typu podwójnej precyzji (`double` z języka C), czyli w standardzie IEEE 754 zajmuje on 64 bity (8 bajtów). Zatem z technicznego punktu widzenia, pythonowy wbudowany `float` to dokładnie to samo co dwuprecyzyjny `double` z innych języków.

## Dlaczego to ma znaczenie?
Programiści przychodzący ze środowisk statycznie typowanych (np. C++ lub Java) często szukają rozdzielenia na jedno- i dwuprecyzyjne typy liczb zmiennoprzecinkowych, by móc zoptymalizować wykorzystanie pamięci operacyjnej (np. wybierając 32-bitowego `float` zamiast 64-bitowego `double`). 

W samym Pythonie ta różnica jest na poziomie wbudowanym celowo ukryta. Wiedza ta pozwala na świadome omijanie wielu błędów projektowych:
- Zrozumienie, że domyślne zmienne `float` są relatywnie wysokoprecyzyjne (do 15-17 miejsc po przecinku w zapisie dziesiętnym).
- Świadomość, że używając wbudowanego w język typu zmiennoprzecinkowego nie zaoszczędzisz natywnie pamięci, ponieważ pod spodem zawsze alokowane jest 64 bity danych z odpowiednim rzutowaniem C (w Pythonie narzut na sam nagłówek obiektu to bazowo stałe 24 bajty).
- Pozwala to również zrozumieć kiedy warto sięgnąć po typy tablicowe oferowane np. przez `NumPy` lub wyższej precyzji przez moduł `decimal`.

## Jak to działa w praktyce?
Pythonowy `float` opiera się na specyfikacji IEEE 754, dając nam 53 bity precyzji operacyjnej i określony maksymalny wykładnik dla notacji naukowej.

### Precyzja i zaokrąglenia
Mimo że precyzja pod spodem jest wielka (klasy 64-bit), to ten format wciąż podlega klasycznym problemom reprezentacji binarnej dla ułamków dziesiętnych, których nie da się idealnie przedstawić w systemie dwójkowym.

```python
# Klasyczny problem reprezentacji binarnej dla 0.1
print(0.1 + 0.2 == 0.3)  # Zwróci False!
print(0.1 + 0.2)         # Zwróci 0.30000000000000004
```

### Ograniczenia i zakres pamięciowy
W języku Python można w łatwy sposób podglądnąć limity i parametry silnika w kwestii liczb precyzji wbudowanej za pomocą paczki `sys`:

```python
import sys

info = sys.float_info
print(info.max)       # Ok. 1.7976931348623157e+308 (maksymalna wartość)
print(info.min)       # Ok. 2.2250738585072014e-308 (minimalna wartość nie-zerowa)
print(info.dig)       # 15 (gwarantowana matematyczna precyzja cyfr dziesiętnych)
```

### Sposób na obejście niedokładności - moduł `Decimal`
Kiedy jako developer potrzebujemy stałej precyzji arytmetycznej, gdzie nie mogą pojawić się niespodziewane części tysięczne dla groszy (np. w systemach bankowych i aplikacjach finansowych), korzysta się z modułu `decimal`:

```python
from decimal import Decimal

# Z dokładnością do ścisłej definicji
# (podajemy string w konstruktorze, by uniknąć straty binarnej precyzji już na etapie rzutowania)
a = Decimal("0.1")
b = Decimal("0.2")

print(a + b == Decimal("0.3"))  # Zwróci True
print(a + b)                    # Zwróci 0.3
```

### Sposób na prawdziwe "single-precision" (32 bit) `float`
Jeśli chcesz przetwarzać potężne macierze, a wbudowany ciężki obiekt standardowego CPythona i brak precyzyjnego ograniczenia zajmują w pamięci za dużo przestrzeni, standardem przemysłowym staje się ucieczka do `NumPy`.

```python
import numpy as np

# Prawdziwy, twardy 32-bitowy float
single_float = np.float32(3.14159)

# 64-bitowy "double", tożsamy pod kątem precyzji z bazowym typem float w Pythonie
double_float = np.float64(3.14159)
```

## Podobne pliki
- [Typy danych w Python i zużycie pamięci](typy-danych-w-python-i-zuzycie-pamieci.md)
- [Catastrophic cancellation i pułapki floating point](catastrophic-cancellation-floating-point.md)
- [Ograniczenia typów liczbowych](ograniczenia-typów-liczbowych.md)
