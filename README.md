### transfer2windy

There are several public places, run by our taxes, which collect and
show measured weather parameters.

Windy on the other hand allow to collect data from own meteo stations.
As tax payer I think it is pretty fair to republish those data at Windy.

This piece of software scrubs data from those sites and transfer them to Windy.
Currently, I use this software to transfer weather data for stations found in `tests/test_main.py`

Supported data sites are:
- `polmil-metar` - [METARs from Polish Military Airports](http://awiacja.imgw.pl/rss/metarmil.php)
- `gddkia` - [Public Roads Service](https://www.traxelektronik.pl/pogoda/drogi/index.php) 
- `armaag` - [Fundacja Agencja Monitoringu Regionalnego Atmosfery Aglomeracji Gdańskiej](https://armaag.gda.pl/index.htm)
- `iopan` - [IOPAN monitoring station in Sopot](http://www.iopan.gda.pl/MarPoLab/wykresy/wykresy.php)

