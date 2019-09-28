import cv2
import sys
import glob
import scipy.ndimage

# Se obtiene el path donde estan los cheques con la firma


path = sys.argv[1]

# Obtener las imagenes dentro del path
images = [f for f in glob.glob(path + "**/*.PNG", recursive=True)]

# Contador para imagenes
count = 0

# Se hace un loop para realizar el procedimiento de extraccion para cada imagen
for image_name in images:
    # Numerar las imagenes
    count += 1

    # Abrir la imagen original
    original = cv2.imread(image_name)
    # Se convierte a escala de grises
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    # Se aplica un filtro Gauseano para borrosidad y deteccion de cambios en la imagen (suavicacion)
    gauss = cv2.GaussianBlur(gray, (5, 5), 0)

    #Binarizacion utilizando el metodo thresholding Otsu's Binarization
    ret, image_binarized = cv2.threshold(gauss, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Se corta el area de la firma
    crop_final = image_binarized[650:650 + 380, 1370:1370 + 750]

    # W, H, Channel = crop_final.shape
    cv2.imwrite(path + '/Resultados/Final/final-' + str(count) + '.png', crop_final)
