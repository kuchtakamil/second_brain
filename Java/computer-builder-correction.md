# Computer Builder - Correction

**Data:** 2024-02-22

---

**User:**

package inners;

public class Computer {
    //required parameters
    private String HDD;
    private String RAM;
    //optional parameters
    private boolean isGraphicsCardEnabled;
    private boolean isBluetoothEnabled;

    public String getHDD() {
        return HDD;
    }

    public String getRAM() {
        return RAM;
    }

    public boolean isGraphicsCardEnabled() {
        return isGraphicsCardEnabled;
    }
    public boolean isBluetoothEnabled() {
        return isBluetoothEnabled;
    }

    private Computer(ComputerBuilder builder) {
        this.HDD=builder.HDD;
        this.RAM=builder.RAM;
        this.isGraphicsCardEnabled=builder.isGraphicsCardEnabled;
        this.isBluetoothEnabled=builder.isBluetoothEnabled;
    }
    //Builder Class
    public static class ComputerBuilder{

        // required parameters
        private String HDD;
        private String RAM;

        // optional parameters
        private boolean isGraphicsCardEnabled;
        private boolean isBluetoothEnabled;

        public ComputerBuilder(String hdd, String ram){
            this.HDD=hdd;
            this.RAM=ram;
        }

        public ComputerBuilder setGraphicsCardEnabled(boolean isGraphicsCardEnabled) {
            this.isGraphicsCardEnabled = isGraphicsCardEnabled;
            return this;
        }

        public ComputerBuilder setBluetoothEnabled(boolean isBluetoothEnabled) {
            this.isBluetoothEnabled = isBluetoothEnabled;
            return this;
        }

        public Computer build(){
            return new Computer(this);
        }
    }
}

czy możliwe jest aby można było stworzyć obiekt Computer w ten sposób
        Computer comp = omputerBuilder(
                "500 GB", "2 GB").setBluetoothEnabled(true)
                .setGraphicsCardEnabled(true).build();

---

**Assistant:**

W kodzie, który podałeś, występuje literówka w kodzie, ale zakładam, że chodziło ci o "ComputerBuilder" zamiast "omputerBuilder". 

Tak, możliwe jest stworzenie obiektu `Computer` w sposób, który przedstawiłeś, ale potrzebujesz poprawić kilka rzeczy w kodzie. Oto poprawiona wersja:

```java
public class Main {
    public static void main(String[] args) {
        Computer comp = new Computer.ComputerBuilder("500 GB", "2 GB")
                .setBluetoothEnabled(true)
                .setGraphicsCardEnabled(true)
                .build();
    }
}
```

Kilka rzeczy, które zostały poprawione:

1. Użyj `new Computer.ComputerBuilder` zamiast `omputerBuilder`.
2. Usuń zbędne nawiasy z `omputerBuilder("500 GB", "2 GB")`.
3. Dodaj kropkę `.` przed `setBluetoothEnabled(true)`.
4. Popraw kolejność metod, tak aby najpierw były wywoływane metody opcjonalne, a na końcu `build()`.

Po tych poprawkach, powinieneś móc poprawnie utworzyć obiekt `Computer` przy użyciu wzorca budowniczego.