import cv2
import sys
import glob

# Se obtiene el path donde estan los cheques con la firma
path = sys.argv[1]

# Obtener las imagenes dentro del path
images = [f for f in glob.glob(path + "**/*.png", recursive=True)]

# Contador para imagenes
count = 0

# Se hace un loop para realizar el procedimiento de extraccion para cada imagen
for image_name in images:

    # Numerar las imagenes
    count += 1

    # Abrir la imagen original
    original = cv2.imread(image_name)
    final = cv2.imread(image_name)

    # Se convierte a escala de grises
    gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)

    # Se aplica un filtro Gauseano para borrosidad y deteccion de cambios en la imagen (suavicacion)
    gauss = cv2.GaussianBlur(gray, (5, 5), 0)

    # Se detectan los bordes a partir del filtro anterior aplicado.
    # Se utiliza el Metodo Canny, el cual es similar a operadores Prewitt, Laplaceano o Roberts
    canny = cv2.Canny(gauss, 50, 150)

    # Se buscan los bordes dentro de la imagen y se extraen los datos
    (contours, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Se aplican los bordes detectados sobre la imagen original y se guarda solo el area de la firma (parte inferior)
    cv2.drawContours(final, contours, -1, (0, 0, 0), 2)
    crop_original = original[400:400 + 300, 970:970 + 750]
    crop_canny = canny[400:400 + 300, 970:970 + 750]
    crop_gaussian_blur = gauss[400:400 + 300, 970:970 + 750]
    crop_gray = gray[400:400 + 300, 970:970 + 750]
    crop_final = final[400:400 + 300, 970:970 + 750]

    cv2.imwrite(path + '/Resultados/Original/original-' + str(count) + '.png', crop_original)
    cv2.imwrite(path + '/Resultados/Gray/gray-' + str(count) + '.png', crop_gray)
    cv2.imwrite(path + '/Resultados/Gaussian/gaussian-' + str(count) + '.png', crop_gaussian_blur)
    cv2.imwrite(path + '/Resultados/Canny/canny-' + str(count) + '.png', crop_canny)
    cv2.imwrite(path + '/Resultados/Final/final-' + str(count) + '.png', crop_final)

