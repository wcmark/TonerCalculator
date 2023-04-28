import os
from PIL import Image
import csv

# Tamaño de la hoja de papel de destino en píxeles
tamano_papel = (2480, 3508)

# Establecer el precio estándar de copia según 5% de cobertura de toner
with open('precio_copia.txt', 'r') as txt_precio:
        precio_uno_porciento = int(txt_precio.read()) / 5

def procesar_archivos():
    global img, precio
    # Carpeta que contiene los archivos a procesar
    carpeta = 'archivos_jpg'

    # Obtener la lista de archivos en la carpeta
    archivos = os.listdir(carpeta)

    # abre el archivo csv para escribir en él
    with open('datos.csv', mode='w', newline='') as csvfile:
        # crea un objeto writer de CSV
        writer = csv.writer(csvfile)

        # deja el archivo en blanco
        writer.writerow(['Precios de las imágenes:'])

        # cierra el archivo
        csvfile.close()


    # abre el archivo csv para escribir en él
    with open('datos.csv', mode='a', newline='') as csvfile:
        # crea un objeto writer de CSV
        writer = csv.writer(csvfile)

        # Procesar cada archivo individualmente
        for archivo in archivos:
            # Comprobar que el archivo es una imagen (opcional)
            if archivo.endswith('.jpg') or archivo.endswith('.png'):
                # Abrir imagen original
                ruta_archivo = os.path.join(carpeta, archivo)
                img = Image.open(ruta_archivo)

                def procesar_img():
                    global img, black_percentage, precio
                    # Abrir imagen original
                    ##img = Image.open('imp.jpg')

                    ## Determinar Ancho y Alto de la imagen
                    ancho_img = img.width
                    alto_img = img.height

                    ## Calcular relaciones de aspecto
                    relacion_img = ancho_img / alto_img
                    relacion_pap = tamano_papel[0] / tamano_papel[1]

                    ## Evaluar so es necesario rotar
                    if relacion_img > relacion_pap:
                        img = img.rotate(90, expand=True)

                    ## Volver a calcular dimenciones y relaciones
                    ancho_img = img.width
                    alto_img = img.height

                    ## Calcular relaciones de aspecto
                    relacion_img = ancho_img / alto_img

                    ## Ecalar imagen
                    if relacion_img == relacion_pap:
                        img = img.resize(tamano_papel)
                    else:
                        escalado_ancho = int((tamano_papel[1] / alto_img) * ancho_img )
                        escalado_alto = int(tamano_papel[1])
                        tamano_maximo = (escalado_ancho, escalado_alto)
                        img = img.resize(tamano_maximo)

                    # Crear nueva imagen blanca del tamaño de la hoja de papel
                    imagen_final = Image.new("RGB", tamano_papel, "white")

                    # Pegar imagen escalada en el centro de la hoja de papel
                    posicion = ((tamano_papel[0] - tamano_maximo[0]) // 2, (tamano_papel[1] - tamano_maximo[1]) // 2)
                    imagen_final.paste(img, posicion)

                    im = imagen_final

                    # convertir la imagen a escala de grises
                    im_grayscale = im.convert('L').point(lambda x: 255 - x)
                    
                    # obtener la matriz de píxeles
                    pixels = im_grayscale.load()

                    # sumar los valores de cada píxel en escala de grises
                    sum_grayscale = 0
                    for i in range(im_grayscale.size[0]):
                        for j in range(im_grayscale.size[1]):
                            sum_grayscale += pixels[i,j]

                    # calcular el valor máximo posible
                    max_sum_grayscale = im_grayscale.size[0] * im_grayscale.size[1] * 255

                    # calcular el porcentaje de "negro" de la totalidad de la imagen
                    black_percentage = (sum_grayscale / max_sum_grayscale) * 100

                    # Establecer el precio de la impresion
                    precio = "$" + str(int(round(black_percentage, 0) * precio_uno_porciento))

                procesar_img()
            # escribe datos
            writer.writerow([precio])

        # cierra el archivo
        csvfile.close()

procesar_archivos()

os.startfile('datos.csv')