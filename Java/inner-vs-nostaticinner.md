# Inner vs NoStaticInner

**Data:** 2024-02-22

---

**User:**

Jaka jest różnica między dwoma wewnętrznymi klasami
public class Outside {
    private String my;

    public Outside(String my) {
        this.my = my;
    }

    void doit() {
        Inner l = new Inner();

        NoStaticInner nol = new NoStaticInner();
    }

    public static class Inner {
        private String in;
        void doInner() {}
    }

    public class NoStaticInner {
        private String in;

    }
}


---

**Assistant:**

W kodzie, który podałeś, mamy dwie wewnętrzne klasy: `Inner` i `NoStaticInner`. Oto różnice między nimi:

1. **Typ dostępu do klasy zewnętrznej:**
   - `Inner` jest zadeklarowane jako statyczna klasa wewnętrzna (`public static class Inner`). Oznacza to, że można utworzyć instancję tej klasy bez potrzeby utworzenia instancji klasy zewnętrznej `Outside`. Możesz zrobić coś takiego jak `Outside.Inner innerInstance = new Outside.Inner();`.
   - `NoStaticInner` nie jest statyczną klasą wewnętrzną. Oznacza to, że aby utworzyć instancję tej klasy, najpierw musisz utworzyć instancję klasy zewnętrznej `Outside` i na niej utworzyć instancję `NoStaticInner`. Na przykład: `Outside outsideInstance = new Outside(); Outside.NoStaticInner noStaticInnerInstance = outsideInstance.new NoStaticInner();`.

2. **Relacja z obiektem klasy zewnętrznej:**
   - W przypadku klasy `Inner`, nie jest wymagane posiadanie instancji klasy zewnętrznej, aby utworzyć instancję klasy wewnętrznej.
   - W przypadku klasy `NoStaticInner`, aby utworzyć instancję tej klasy, musisz posiadać już instancję klasy zewnętrznej `Outside`.

Ogólnie rzecz biorąc, różnica ta wpływa na to, jak można tworzyć instancje klas wewnętrznych i na to, czy dana klasa wewnętrzna jest związana z konkretną instancją klasy zewnętrznej czy też nie.