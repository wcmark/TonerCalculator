from PIL import Image

# Tamaño de la hoja de papel de destino en píxeles
tamano_papel = (2480, 3508)

# Abrir imagen original
img = Image.open('imp.jpg')

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
im_grayscale.save('imp_temp.jpg')

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

print("El porcentaje de 'negro' de la totalidad de la imagen es:", black_percentage, "%")