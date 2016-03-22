<<<<<<< HEAD:sources/DBbridge/Cassandra/README_rendimiento.md
### Tiempos De Escritura
#### Recoleción de tweets de un usuario
##### 3400 tweets
Sincrono 31.72 Segundos
Asincrono 9.5 Segundos 

### Comparación RPy
#### Pruebas de Rendimiento
* 5 Nodos Raspberry Pi 2, 2103 ops/s
* 1 Hilo AMD Phenom(tm) II X6 1055T / 8G Ram, 3127 ops/s
* 6 Hilo AMD Phenom(tm) II X6 1055T / 8G Ram, 17408 ops/s

#### Análisis de costes
link análisis https://medium.com/@johnsercel/cassandra-on-raspberrypi-2-a84602953b23
En el análisis anterior no utilizan discos duros, si no las SD, no sé si esto mejorará o empeorará el rendimiento.
Son discos Externos limitados por Usb 2.0 internet dice ->"From experience, I know USB 2.0 copies about 10MB/s on average"( no creo que sea tanto unos 30MB/s)

##### Coste cluster 5 nodos Raspberry Pi 2:
* 5xWestern Digital Elements - Disco duro externo de 1 TB <- 54 €/unidad (quizás sea poca velocidad de rotación)
* 5xRaspberry Pi 2 <- 41 €/unidad
* 5xSanDisk Ultra 32GB <- 13 €/unidad
* 1xTP-LINK 8-Port Gigabit Switch <- 26€
* 1xAnker® Cargador de Mesa (60W, 6 Puertos USB) <- 31€
```
Consumo 30W + o -
Total: 600€ (5G Ram, 5TB datos)
```

##### Coste servidor:
Ya no se puede conseguir mi procesador (normal porque es viejo) así que los precios son con uno un poco mejor y que consume menos.
* 1xAMD FX-6300 100 €
* 1xGigabyte 970A-DS3P - Placa base ATX 63€
* 1xG-Skill Ripjaws - Memoria RAM (16 GB, DDR3 1600MHz) 111€
* 1xWestern Digital Digital Green 4TB 146€ (quizás sea poca velocidad de rotación)
* 1xFuente de alimentación (500W) 42€
```
Consumo CPU 95W, total 200W?

Total(Espero no dejarme nada importante) : 462€ (16G Ram, 4 TB datos)
El rendimiento por los test que he realizado ha de ser mayor.
```
##### Como dato adicional:
* Velocidad de escritura SD 48 MB/s
* Velocidad de escritura HDD 80-90MB/s escritura secuencial

##### Resumen:
* No se si merece la pena, es interesante el poco consumo, pero para eso podríamos usar Intel en vez de AMD.
