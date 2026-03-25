# Regexp dla liter, znaków.

**Data:** 2023-07-27

---

**User:**

w lua napisz regex pasujący do wszystkich dużych i małych liter, wszystkich liczb i znaków - i .

---

**Assistant:**

W Lua nie ma wbudowanej obsługi wyrażeń regularnych tak jak w niektórych innych językach programowania. Jednak możemy skorzystać z biblioteki Lua, która dostarcza wsparcie dla wyrażeń regularnych. W celu użycia wyrażeń regularnych w Lua, musimy najpierw załadować odpowiednią bibliotekę i użyć jej funkcji do dopasowania wzorca.

Poniżej znajduje się przykład kodu Lua, który używa biblioteki `lpeg` do zdefiniowania wyrażenia regularnego pasującego do wszystkich dużych i małych liter, wszystkich liczb oraz znaków '-', '_' i '.'.

```lua
local lpeg = require("lpeg")

local pattern = lpeg.S("a-zA-Z0-9._-")

function check_match(input)
    return lpeg.match(pattern, input) == #input
end

-- Przykłady użycia
print(check_match("Hello123.")) -- true
print(check_match("Hello_123.")) -- true
print(check_match("Hi!")) -- false
```

W tym przykładzie funkcja `check_match` sprawdza, czy cały ciąg znaków pasuje do wzorca `pattern`. Wyrażenie `lpeg.S("a-zA-Z0-9._-")` oznacza, że dopasowuje wszystkie znaki alfanumeryczne (duże i małe litery oraz cyfry) oraz znaki '-', '_' i '.'.

Pamiętaj, że do działania tego przykładu musisz mieć zainstalowaną bibliotekę `lpeg`, która może nie być domyślnie dostępna w standardowej instalacji Lua. Aby zainstalować bibliotekę `lpeg`, możesz skorzystać z menedżera pakietów LuaRocks:

```bash
luarocks install lpeg
```

Po zainstalowaniu biblioteki `lpeg`, powyższy kod powinien działać poprawnie.