# Resource.pure vs Resource.eval

**Data:** 2023-08-19

---

**User:**

Scala, kiedy używać Resource.pure a Resource.eval

---

**Assistant:**

`cats.effect.Resource` to część biblioteki Cats Effect w języku Scala, która jest używana do zarządzania zasobami, takimi jak pliki, połączenia bazodanowe, sockety itp. W skrócie, `Resource` pomaga w tworzeniu i zwalnianiu zasobów w sposób bezpieczny w kontekście efektów asynchronicznych.

`Resource.pure` i `Resource.eval` to dwie różne metody używane do tworzenia `Resource`. Oto ich krótkie opisy oraz odpowiedzi na pytanie, kiedy używać którego:

1. `Resource.pure`
Metoda `Resource.pure` służy do opakowywania stałego zasobu wewnątrz `Resource`. To oznacza, że zasób jest już dostępny i gotowy do użycia, a `Resource` zapewnia jedynie dodatkową warstwę abstrakcji. Możesz używać `Resource.pure`, kiedy masz już przygotowany zasób, który nie wymaga żadnych obliczeń asynchronicznych ani akwizycji. Na przykład:

```scala
import cats.effect._

val constantResource: Resource[IO, MyResource] = Resource.pure(new MyResource())
```

2. `Resource.eval`
Metoda `Resource.eval` pozwala na opakowanie obliczeń asynchronicznych, które tworzą zasób. To oznacza, że zasób nie jest dostępny od razu, ale zostanie wytworzony w wyniku obliczeń efektu asynchronicznego. Używaj `Resource.eval`, kiedy potrzebujesz wykonać akwizycję zasobu w sposób asynchroniczny lub gdy inicjalizacja zasobu wymaga obliczeń. Na przykład:

```scala
import cats.effect._

val asyncResource: Resource[IO, MyResource] = Resource.eval(IO {
  // Asynchronous resource acquisition or computation
  new MyResource()
})
```

Podsumowując, użyj `Resource.pure`, gdy masz gotowy do użycia zasób, a `Resource.eval`, gdy musisz przeprowadzić asynchroniczne obliczenia w celu uzyskania zasobu.