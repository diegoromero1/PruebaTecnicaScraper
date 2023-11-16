import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import csv
from unidecode import unidecode


# Función para obtener la URL basada en el año proporcionado por el usuario
def obtener_url():
    ano = input("Ingrese el año para obtener la información (por ejemplo, 2022, 2023, etc.): ")
    url = f'https://www.sii.cl/valores_y_fechas/mepco/mepco{ano}.htm'
    return ano, url


# Función principal para realizar el scraping y guardar los datos
def scrape_sii():
    # Obtener la URL y el año según la entrada del usuario
    ano, url = obtener_url()

    # Realizar la solicitud HTTP
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todas las tablas con la clase 'table table-bordered'
        tablas = soup.find_all('table', {'class': 'table table-bordered'})

        # Verificar si se encontraron tablas en la página
        if tablas:
            # Extraer encabezados de la primera tabla
            encabezados = [th.text.strip() if th.text.strip() else 'Otro' for th in tablas[0].find_all('th')]

            # Corregir el nombre del encabezado 'Vigencia desde'
            encabezados[0] = 'Vigencia'

            # Agregar el encabezado 'Tipo' después de 'Vigencia'
            encabezados.insert(1, 'Tipo')

            # Crear una tabla con PrettyTable
            tabla_resultados = PrettyTable(encabezados)

            # Guardar los datos en un archivo CSV
            with open(f'datos_sii_{ano}.csv', 'w', encoding='utf-8', newline='') as csv_file:
                writer = csv.writer(csv_file)

                # Escribir encabezados en el archivo CSV
                writer.writerow([unidecode(header) for header in encabezados])

                for tabla in tablas:
                    # Extraer la vigencia desde el encabezado
                    vigencia = tabla.find('th', {'colspan': '2'}).text.split("Jueves")[1].strip()

                    # Encontrar todas las filas en la tabla
                    filas = tabla.find_all('tr')

                    for fila in filas:
                        # Buscar el tipo de combustible en el formato <td rowspan="2" style="vertical-align:middle;">...</td>
                        tipo_combustible_elemento = fila.find('td', {'rowspan': '2', 'style': 'vertical-align:middle;'})

                        # Si no se encuentra, buscar en el formato <td style="vertical-align:middle;">...</td>
                        if not tipo_combustible_elemento:
                            tipo_combustible_elemento = fila.find('td', {'style': 'vertical-align:middle;'})

                        if tipo_combustible_elemento:
                            # Extraer el valor correspondiente al tipo de combustible desde el td
                            tipo_combustible_valor = tipo_combustible_elemento.text.strip()

                            # Extraer los valores correspondientes al tipo de combustible desde los td,
                            # ignorando el <td>Impuesto</td>
                            valores_combustible = [
                                td.text.strip() for td in fila.find_all('td', {'class': None}) if
                                td.text.strip() not in ['Impuesto', tipo_combustible_valor]
                            ]

                            # Asegurarse de que la cantidad de valores coincida con la cantidad de encabezados
                            if len(valores_combustible) + 2 == len(encabezados):  # +2 por 'Vigencia' y 'Tipo'
                                # Agregar fila a la tabla PrettyTable
                                tabla_resultados.add_row([vigencia, tipo_combustible_valor] + valores_combustible)

                                # Escribir fila en el archivo CSV
                                writer.writerow(
                                    [unidecode(vigencia), unidecode(tipo_combustible_valor)] + [unidecode(valor) for
                                                                                                valor in
                                                                                                valores_combustible])
                            elif tipo_combustible_valor == 'Otro' and len(valores_combustible) == len(encabezados) - 2:
                                # Manejar el caso específico de "Otro" sin 'Tipo' en los valores
                                # Agregar fila a la tabla PrettyTable
                                tabla_resultados.add_row(
                                    [vigencia, tipo_combustible_valor] + valores_combustible + [''])

                                # Escribir fila en el archivo CSV
                                writer.writerow(
                                    [unidecode(vigencia), unidecode(tipo_combustible_valor)] + [unidecode(valor) for
                                                                                                valor in
                                                                                                valores_combustible] + [
                                        ''])
                            else:
                                print(
                                    f"La cantidad de valores no coincide con la cantidad de encabezados para {tipo_combustible_valor}.")
                                print("Encabezados:", encabezados)
                                print("Valores:", [vigencia, tipo_combustible_valor] + valores_combustible)
                                return

            # Imprimir la tabla
            print(tabla_resultados)

            print(f"Datos extraídos y guardados exitosamente en 'datos_sii_{ano}.csv'.")
        else:
            print("No se encontraron tablas en la página con la clase 'table table-bordered'.")
    else:
        print(f"Error al acceder al sitio web. Código de estado: {response.status_code}")


# Entrada principal del programa
if __name__ == '__main__':
    scrape_sii()
