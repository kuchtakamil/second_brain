# Agregowanie wyników po doc_name

**Data:** 2025-07-25

---

**User:**

W wyniku zapytania
select st.type_id, string_agg(temp.doc_name, ',')
from template temp
join service_template st on st.temp_id = st.temp_id
where temp.doc_name like '%sport'
and st.type_id in (34134, 1235432, 345, 123, 3246, 8469, 9948, 42364, 77554, 777)
group by st.type_id

otrzymuję listę 

8469 doc_sport,mydoc_sport,trening_sport,awesome_sport,manual_sport
345 radio_sport,moto_sport,trening_sport,doc_sport
77554 doc_sport,mydoc_sport,trening_sport,awesome_sport,manual_sport
777 extreme_sport,ultra_sport

ale jeśli kolumna string_agg(temp.doc_name, ',') jest taka sama dla wielu type_id chciałbym otrzymać jeden wiersz z wymienionymi type_id po przecinku oraz obok string_agg(temp.doc_name, ',')

---

**Assistant:**

Aby pogrupować wyniki według unikalnej wartości zagregowanej `string_agg(temp.doc_name, ',')` i zebrać odpowiadające jej `type_id`, możesz użyć podzapytania lub CTE (Common Table Expression), np. w taki sposób:

```sql
with base as (
    select 
        st.type_id, 
        string_agg(temp.doc_name, ',' order by temp.doc_name) as doc_names
    from template temp
    join service_template st on st.temp_id = temp.temp_id
    where temp.doc_name like '%sport'
      and st.type_id in (34134, 1235432, 345, 123, 3246, 8469, 9948, 42364, 77554, 777)
    group by st.type_id
)
select 
    string_agg(base.type_id::text, ',' order by base.type_id) as type_ids,
    base.doc_names
from base
group by base.doc_names;
```

### Co się tu dzieje:
- W CTE `base` agregujemy `doc_name` po `type_id`.
- W głównym zapytaniu grupujemy po unikalnych `doc_names` i dla każdego z nich zbieramy `type_id` w `string_agg(...)`.

Dzięki temu otrzymasz wynik jak:

```
type_ids                      | doc_names
-----------------------------|-----------------------------------------------------------
345,8469,77554               | awesome_sport,doc_sport,manual_sport,mydoc_sport,trening_sport
777                          | extreme_sport,ultra_sport
```

Jeśli chcesz zachować dokładną kolejność `doc_name` (np. taką jak była w oryginalnym `string_agg`) — można w `order by` w `string_agg` użyć jakiegoś `id` lub innego pola do uporządkowania.