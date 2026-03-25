# Dla kwadratu o boku A metrów, jak policzyć rozmiar kątowy w odległości D metrów?

**Data:** 11 sty 2026, 18:40:40 CET

---

**User:**

Dla kwadratu o boku A metrów, jak policzyć rozmiar kątowy w odległości D metrów?

---

**Gemini:**

Aby obliczyć rozmiar kątowy kwadratu o boku $A$ znajdującego się w odległości $D$, należy rozróżnić **płaski rozmiar kątowy** (kąt rozwarcia widzenia krawędzi) oraz **kąt bryłowy** (przestrzeń zajmowana przez obiekt w polu widzenia).

### 1. Płaski rozmiar kątowy ($\alpha$)

Przy założeniu, że kwadrat jest ustawiony prostopadle do linii wzroku, a odległość $D$ jest mierzona od obserwatora do środka kwadratu, wykorzystujemy funkcje trygonometryczne.

Kwadrat o boku $A$ możemy podzielić na dwa trójkąty prostokątne, gdzie przyprostokątna przeciwległa to $A/2$, a przyprostokątna przyległa to $D$.

Wzór dokładny na kąt w radianach:
$$\alpha = 2 \cdot \arctan\left(\frac{A}{2D}\right)$$

Aby otrzymać wynik w stopniach, należy pomnożyć go przez $\frac{180}{\pi}$:
$$\alpha\_{deg} = 2 \cdot \arctan\left(\frac{A}{2D}\right) \cdot \frac{180}{\pi}$$

#### Przybliżenie małych kątów

W przypadkach, gdy $D \gg A$ (odległość jest znacznie większa od rozmiaru obiektu), można zastosować przybliżenie $\tan(\theta) \approx \theta$. Wtedy wzór upraszcza się do:
$$\alpha \approx \frac{A}{D} \text{ [rad]}$$

---

### 2. Rozmiar kątowy wzdłuż przekątnej

Należy pamiętać, że kwadrat ma większy rozmiar kątowy mierzony wzdłuż jego przekątnej ($d = A\sqrt{2}$). Wówczas maksymalny kąt rozwarcia $\alpha\_{diag}$ wynosi:
$$\alpha\_{diag} = 2 \cdot \arctan\left(\frac{A\sqrt{2}}{2D}\right)$$

---

### 3. Kąt bryłowy ($\Omega$)

Dla obiektu dwuwymiarowego, jakim jest kwadrat, często bardziej miarodajne jest wyznaczenie kąta bryłowego wyrażonego w steradianach ($sr$). Dla prostokąta (w tym kwadratu) scentrowanego względem osi optycznej, wzór wynosi:

$$\Omega = 4 \arcsin\left( \frac{A^2}{4D^2 + A^2} \right)$$

Dla dużych odległości ($D \gg A$), kąt bryłowy można przybliżyć jako stosunek powierzchni rzutu do kwadratu odległości:
$$\Omega \approx \frac{A^2}{D^2}$$

---

### Implementacja w języku Python

Poniższy kod oblicza oba rodzaje kątów (płaski i bryłowy) przy użyciu standardowej biblioteki `math`.

```
import math

def calculate_angular_size(side_length: float, distance: float):
    """
    Calculates the angular size of a square.
    
    :param side_length: Side A in meters
    :param distance: Distance D in meters
    :return: Dictionary with planar angle (degrees) and solid angle (steradians)
    """
    if distance <= 0:
        raise ValueError("Distance must be greater than zero.")

    # Planar angular size (alpha) using exact formula
    planar_angle_rad = 2 * math.atan(side_length / (2 * distance))
    planar_angle_deg = math.degrees(planar_angle_rad)

    # Diagonal planar angular size
    diagonal = side_length * math.sqrt(2)
    diagonal_angle_deg = math.degrees(2 * math.atan(diagonal / (2 * distance)))

    # Solid angle (Omega)
    # Formula for a rectangle (A=B): 4 * arcsin( (A*B) / sqrt((4D^2 + A^2)(4D^2 + B^2)) )
    # Simplifies for a square:
    solid_angle = 4 * math.asin(side_length**2 / (4 * distance**2 + side_length**2))

    return {
        "planar_angle_degrees": planar_angle_deg,
        "diagonal_angle_degrees": diagonal_angle_deg,
        "solid_angle_steradians": solid_angle
    }

# Example usage:
side_a = 2.0  # 2 meters
dist_d = 10.0 # 10 meters

results = calculate_angular_size(side_a, dist_d)
for key, value in results.items():
    print(f"{key}: {value:.4f}")
```

Czy chciałbyś, abym wyprowadził wzór dla przypadku, w którym kwadrat jest nachylony pod kątem $\theta$ względem płaszczyzny obserwacji?