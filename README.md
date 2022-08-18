# US Stock Price Statistics Data

A 'US' részvényhez az 5 éves napi history forrása: https://www.nasdaq.com/market-activity/futures/us/historical

A feladatot Jupyter Notebookban oldottam meg elsőnek, mert számomra könnyebb úgy dolgozni, hogy közben látom a dataframe vizualizációját.
Próbáltam rövid, és gyors megoldást alkalmazni.
A program végén a matplotlib grafikonok egyfajta ellenőrzések, így látszódik, hogy a kiszámolt értékek helyesek.
Ezután PyCharmban is implementáltam a kódot.

Sajnos még a Unit teszt írásba nem mélyedtem bele, így csak néhány manuális tesztet tudtam elvégezni a programra, azon kívűl, hogy próbáltam
minél stabilabb kódot írni.

- Másik adattáblát betölteni ✓
- Lekérdezés hibakezelése ✓

Milyen tesztet írnék még?
- Adat tisztítás, ha szükséges: ha lennének NaN adatok az adattáblában, ezek kiszűrése (fill)
