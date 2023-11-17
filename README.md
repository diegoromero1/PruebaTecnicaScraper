# Proyecto de Web Scraping - SII
- Este proyecto realiza web scraping en el sitio web del Servicio de Impuestos Internos (SII) de Chile 
para obtener información sobre el impuesto específico del petróleo. 
- Los datos extraídos se guardan en un archivo CSV.
- Los datos que se extraen corresponen a la Vigencia ,Componente Base,Componente Variable, Impuesto Específico Resultante y Unidades Tributarias Mensuales 
## Requisitos
- Python
- Paquetes necesarios (instalados mediante `pip install -r requirements.txt`)

## Instalación
1. Clona este repositorio:

   ```bash
   git clone https://github.com/diegoromero1/PruebaTecnicaScraper.git 
   ```
2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```
   
## Uso
- Ejecuta el scraper desde la línea de comandos:

```bash
python ScraperSII.py
```
- EL codigo va a solicitar ingresar un año el cual utilizara para la direccion url
que permitira modificar el url principal para poder ir buscando y extraer los datos por año.
- El codigo tambien solicitara el tipo de combustible a buscar mediante un listado de opciones.
- Como salida se genera una tabla por pantalla y tambien un archivo csv que contendra el año y el
tipo en su nombre donde todos representa que extrajo toda la informacion.