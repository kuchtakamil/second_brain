# Jeśli w mieście A mieszka n mieszkańców, w mieście B mieszka m mieszkańców, a wi

**Data:** 7 sty 2026, 23:43:16 CET

---

**User:**

Jeśli w mieście A mieszka n mieszkańców, w mieście B mieszka m mieszkańców, a wiemy że n > m to jak policzyć jaki procent więcej mieszka w A niż w B?

---

**Gemini:**

Aby obliczyć, o ile procent więcej mieszkańców mieszka w mieście A w stosunku do miasta B, należy przyjąć populację miasta B ($m$) jako wartość bazową (100%).

### Wzór matematyczny

Różnicę procentową obliczamy, dzieląc różnicę wartości przez wartość odniesienia, a następnie mnożąc wynik przez 100:

$$P = \frac{n - m}{m} \times 100%$$

Alternatywnie, wzór można zapisać w uproszczonej postaci:

$$P = \left( \frac{n}{m} - 1 \right) \times 100%$$

---

### Przykład obliczeniowy

Załóżmy następujące dane:

- Miasto A ($n$): 150 000 mieszkańców
- Miasto B ($m$): 120 000 mieszkańców

1. Obliczamy różnicę: $150,000 - 120,000 = 30,000$
2. Dzielimy przez bazę ($m$): $30,000 / 120,000 = 0,25$
3. Zamieniamy na procenty: $0,25 \times 100% = 25%$

**Wynik:** W mieście A mieszka o 25% więcej osób niż w mieście B.

---

### Implementacja w języku Python

Poniższy kod realizuje tę logikę, uwzględniając obsługę błędu dzielenia przez zero (przypadek, gdyby miasto B było niezamieszkane):

```
def calculate_percentage_increase(population_a: int, population_b: int) -> float:
    """
    Calculates by what percentage population_a is greater than population_b.
    
    Args:
        population_a (int): Inhabitants in city A (n)
        population_b (int): Inhabitants in city B (m)
        
    Returns:
        float: Percentage increase.
        
    Raises:
        ValueError: If population_b is zero or negative.
    """
    if population_b <= 0:
        raise ValueError("The reference population (city B) must be greater than zero.")
    
    if population_a < population_b:
        # Strictly speaking, the prompt assumes n > m, 
        # but robust code should handle other cases.
        pass

    percentage_diff = ((population_a - population_b) / population_b) * 100
    return percentage_diff

# Example usage:
n = 150000
m = 120000

try:
    result = calculate_percentage_increase(n, m)
    print(f"City A has {result:.2f}% more inhabitants than City B.")
except ValueError as e:
    print(f"Error: {e}")
```

---

### Analiza różnicy między "o ile procent więcej" a "jaki procent stanowi"

W statystyce często mylone są dwa pojęcia:

1. **O ile procent więcej ($n$ względem $m$):** $\frac{n-m}{m} \times 100$
2. **Jaki procent wartości $m$ stanowi $n$:** $\frac{n}{m} \times 100$

Jeśli $n=200$ i $m=100$, to miasto A jest o **100% większe** od B, ale populacja miasta A stanowi **200%** populacji miasta B.

Czy chciałbyś, abym przygotował skrypt w innym języku programowania lub rozbudował ten przykład o wizualizację danych przy użyciu biblioteki Matplotlib?