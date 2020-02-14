Trg dela
=========
Analiziral bom zaposlitvene oglase na strani:
[studentski-servis](https://www.studentski-servis.com/ess/prosta_dela.php).

oglasi.csv vsebujejo:
* Vrsto dela
* Urno postavko
* Regijo
* Št. prostih mest
* Trajanje dela
* Delovnik
* Šifro oglasa
* Naravo dela (začasno delo ali polna zaposlitev)
* Komentar

Delovne hipoteze:
* Vrste dela z najvišjo povprečno urno postavko so programerska dela.
* Bolj gosto poseljene regije imajo višje povprečne urne postavke.
* Obstaja očitna povezava med zaslužkom in delovnikom.

# Navodila za uporabnike
Uporaba je preprosta. Za pridobitev podatkov iz interneta samo poženete 
```python
python data_capture.py
```
kar vam generira nabor podatkov `oglasi.csv` v mapi `data`.

Opomba: trenutno so oglasi.csv že naloženi, tako da ponovno poganjanje ni potrebno in bo podatke po nepotrebnem samo podvojilo.

Natančna analiza teh podatkov se nahaja v `analiza.ipynb`.