# Filtr logów Lua w Envoym.

**Data:** 2023-07-14

---

**User:**

Envoy, mam filtr do logów typu envoy.access_loggers.file i chciałbym w definicji json_format zastosować pewne skrypty Lua. Czy mogę to zrobić?

---

**Assistant:**

Tak, w Envoym możesz użyć skryptów Lua w definicji formatu JSON dla filtrów logów, takich jak `envoy.access_loggers.file`. Envoym obsługuje dynamiczne wyrażenia Lua w konfiguracji, które mogą być używane do manipulowania danymi logów w czasie rzeczywistym.

Aby użyć skryptów Lua w definicji `json_format`, musisz dodać odpowiednią sekcję `lua` do konfiguracji swojego filtra logów. Przykładowa konfiguracja może wyglądać tak:

```yaml
filters:
  - name: envoy.access_loggers.file
    config:
      path: /var/log/envoy/access.log
      format:
        json_format:
          json: |
            {
              "time": "%START_TIME%",
              "method": "%REQ(:METHOD)%",
              "path": "%REQ(X-ENVOY-ORIGINAL-PATH?:PATH)%",
              "status": "%RESPONSE_CODE%",
              "lua_script": "%REQ(Lua:your_lua_script)%"
            }
          lua:
            inline_code: |
              function your_lua_script(request)
                -- Tutaj umieść swój skrypt Lua
                -- Możesz manipulować danymi zapytania (request) i zwrócić wynik jako wartość,
                -- która zostanie wstawiona w polu "lua_script" w logach.

                return "Wynik skryptu Lua"
              end
```

W powyższym przykładzie, w polu `lua_script` w logach zostanie umieszczony wynik działania skryptu Lua, który jest wywoływany przy użyciu `REQ(Lua:your_lua_script)`. Możesz umieścić własny skrypt Lua w sekcji `inline_code` i manipulować danymi zapytania, a następnie zwrócić wynik jako wartość.

Pamiętaj, że musisz mieć włączoną obsługę Lua w konfiguracji Envoym oraz odpowiednio skonfigurowany silnik Lua. Dodatkowo, upewnij się, że używasz odpowiedniej wersji Envoym, która obsługuje skrypty Lua, ponieważ niektóre starsze wersje mogą nie mieć tej funkcjonalności.