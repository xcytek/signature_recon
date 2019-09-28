import cv2
import sys
import glob
import scipy.ndimage
import numpy as np
import time


class Check:
    """
    Clase con metodos para procesamiento de convoluciones
    """

    """
    Minimo de Elementos Estructurales a evaluar
    """
    min_struct_elements: int = 50

    """
    Minimo de firmas
    """
    min_signs: int = 15

    def build_elements(self):
        elements = []
        for e in range(self.min_struct_elements):
            elements.append(
                self.calculate_element(e)
            )

        return elements

    @staticmethod
    def calculate_element(index):
        """
        En esta funcion se definen los elementos estructurales que seran
        utilizados para realizar las transposiciones con las firmas
        """
        element = np.zeros(shape=(3, 5, 5))

        if index == 1:
            element[0:3, 2] = 1

        if index == 2:
            element[0:3, 0:5, 2] = 1

        if index == 3:
            for e in range(0, 3):
                np.fill_diagonal(element[e], 1)

        if index == 4:
            for e in range(0, 3):
                np.fill_diagonal(np.flipud(element[e]), 1)

        if index == 5:
            element[0:3, 0:5, 2] = 1
            element[0:3, 2] = 1

        if index == 6:
            for e in range(0, 3):
                np.fill_diagonal(element[e], 1)
                r, c = [0, 4]
                for num in range(0, 5):
                    element[e, r, c] = 1
                    r += 1
                    c -= 1
        if index == 7:
            element[0:3, 0:5, 2] = 1
            element[0:3, 4, 1:2] = 1
            element[0:3, 0, 3:4] = 1

        if index == 8:
            element[0:3, 0:5, 2] = 1
            element[0:3, 0, 0:1] = 1
            element[0:3, 4, 4:5] = 1

        if index == 9:
            c = 0
            for r in range(4, -1, -1):
                if r >= 2:
                    c = r
                else:
                    c += 1
                element[0:3, r, c] = 1

        if index == 10:
            c = 0
            for r in range(0, 5):
                if r < 3:
                    c = r
                else:
                    c -= 1
                element[0:3, r, c] = 1
        if index == 11:
            c = 0
            for r in range(0, 5):
                if r < 3:
                    c = r
                else:
                    c -= 1
                element[0:3, c, r] = 1

        if index == 12:
            c = 0
            for r in range(4, -1, -1):
                if r >= 2:
                    c = r
                else:
                    c += 1
                element[0:3, c, r] = 1

        if index == 13:
            element[0:3, 0:3, 0] = 1
            element[0:3, 4, 2:5] = 1
            element[0:3, 3, 1] = 1

        if index == 14:
            element[0:3, 0:3, 4] = 1
            element[0:3, 4, 0:3] = 1
            element[0:3, 3, 3] = 1

        if index == 15:
            element[0:3, 0, 2:5] = 1
            element[0:3, 2:5, 0] = 1
            element[0:3, 1, 1] = 1

        if index == 16:
            element[0:3, 0, 0:3] = 1
            element[0:3, 2:5, 4] = 1
            element[0:3, 1, 3] = 1

        if index == 17:
            element[0:3, 2] = 1
            element[0:3, 0:5, 4] = 1

        if index == 18:
            element[0:3, 0] = 1
            element[0:3, 0:5, 2] = 1

        if index == 19:
            element[0:3, 2] = 1
            element[0:3, 0:5, 0] = 1

        if index == 20:
            element[0:3, 4] = 1
            element[0:3, 0:5, 2] = 1

        if index == 21:
            element[0:3, 0:3, 0] = 1
            element[0:3, 0:3, 4] = 1
            element[0:3, 3, 1] = 1
            element[0:3, 3, 3] = 1
            element[0:3, 4, 2] = 1

        if index == 22:
            element[0:3, 2:5, 0] = 1
            element[0:3, 2:5, 4] = 1
            element[0:3, 1, 1] = 1
            element[0:3, 1, 3] = 1
            element[0:3, 0, 2] = 1

        if index == 23:
            element[0:3, 0, 0:3] = 1
            element[0:3, 4, 0:3] = 1
            element[0:3, 1, 3] = 1
            element[0:3, 3, 3] = 1
            element[0:3, 2, 4] = 1

        if index == 24:
            element[0:3, 0, 2:5] = 1
            element[0:3, 4, 2:5] = 1
            element[0:3, 1, 1] = 1
            element[0:3, 3, 1] = 1
            element[0:3, 2, 0] = 1

        if index == 25:
            element[0:3, 0:5, 2] = 1
            element[0:3, 0, 1] = 1
            element[0:3, 1, 0] = 1
            element[0:3, 3, 4] = 1
            element[0:3, 4, 3] = 1

        if index == 26:
            element[0:3, 0:5, 2] = 1
            element[0:3, 0, 3] = 1
            element[0:3, 1, 4] = 1
            element[0:3, 3, 0] = 1
            element[0:3, 4, 1] = 1

        if index == 27:
            element[0:3, 2] = 1
            element[0:3, 1, 0] = 1
            element[0:3, 0, 1] = 1
            element[0:3, 4, 3] = 1
            element[0:3, 3, 4] = 1

        if index == 28:
            element[0:3, 2] = 1
            element[0:3, 1, 4] = 1
            element[0:3, 0, 3] = 1
            element[0:3, 3, 0] = 1
            element[0:3, 4, 1] = 1

        if index == 29:
            element[0:3, 0:5, 0] = 1
            element[0:3, 4, 0:2] = 1
            element[0:3, 2:5, 2] = 1
            element[0:3, 2, 2:5] = 1

        if index == 30:
            element[0:3, 0, 0:5] = 1
            element[0:3, 0:3, 0] = 1
            element[0:3, 2, 0:3] = 1
            element[0:3, 2:5, 2] = 1

        if index == 31:
            element[0:3, 0:5, 4] = 1
            element[0:3, 0, 2:5] = 1
            element[0:3, 0:3, 2] = 1
            element[0:3, 2, 0:2] = 1

        if index == 32:
            element[0:3, 4, 0:5] = 1
            element[0:3, 2:5, 0] = 1
            element[0:3, 2, 0:3] = 1
            element[0:3, 0:3, 2] = 1

        if index == 33:
            element[0:3, 0:3, 2] = 1
            element[0:3, 4, 0] = 1
            element[0:3, 3, 1] = 1
            element[0:3, 3, 3] = 1
            element[0:3, 4, 4] = 1

        if index == 34:
            element[0:3, 2, 2:5] = 1
            element[0:3, 0, 0] = 1
            element[0:3, 1, 1] = 1
            element[0:3, 3, 1] = 1
            element[0:3, 4, 0] = 1

        if index == 35:
            element[0:3, 2:5, 2] = 1
            element[0:3, 0, 0] = 1
            element[0:3, 1, 1] = 1
            element[0:3, 1, 3] = 1
            element[0:3, 0, 4] = 1

        if index == 36:
            element[0:3, 2, 0:3] = 1
            element[0:3, 0, 4] = 1
            element[0:3, 1, 3] = 1
            element[0:3, 3, 3] = 1
            element[0:3, 4, 4] = 1

        if index == 37:
            element[0:3, 2, 0:5] = 1
            element[0:3, 2:5, 0] = 1
            element[0:3, 0:3, 4] = 1

        if index == 38:
            element[0:3, 2, 0:5] = 1
            element[0:3, 0:3, 0] = 1
            element[0:3, 2:5, 4] = 1

        if index == 39:
            element[0:3, 0:5, 0] = 1
            element[0:3, 0, 3] = 1
            element[0:3, 1, 2] = 1
            element[0:3, 2, 1] = 1
            element[0:3, 3, 2] = 1
            element[0:3, 4, 3] = 1

        if index == 40:
            element[0:3, 0:5, 4] = 1
            element[0:3, 0, 1] = 1
            element[0:3, 1, 2] = 1
            element[0:3, 2, 3] = 1
            element[0:3, 3, 2] = 1
            element[0:3, 4, 1] = 1

        if index == 41:
            element[0:3, 4, 0:5] = 1
            element[0:3, 1, 0] = 1
            element[0:3, 2, 1] = 1
            element[0:3, 3, 2] = 1
            element[0:3, 2, 3] = 1
            element[0:3, 1, 4] = 1

        if index == 42:
            element[0:3, 0, 0:5] = 1
            element[0:3, 3, 0] = 1
            element[0:3, 2, 1] = 1
            element[0:3, 1, 2] = 1
            element[0:3, 2, 3] = 1
            element[0:3, 3, 4] = 1

        if index == 43:
            element[0:3, 2, 0:5] = 1
            element[0:3, 0:5, 1] = 1
            element[0:3, 0:5, 3] = 1

        if index == 44:
            element[0:3, 0:5, 2] = 1
            element[0:3, 1, 0:5] = 1
            element[0:3, 3, 0:5] = 1

        if index == 45:
            for e in range(0, 3):
                np.fill_diagonal(np.flipud(element[e]), 1)
            element[0:3, 0:5, 4] = 1

        if index == 46:
            for e in range(0, 3):
                np.fill_diagonal(element[e], 1)
            element[0:3, 0:5, 0] = 1

        if index == 47:
            element[0:3, 1:4, 0] = 1
            element[0:3, 4, 1:4] = 1
            element[0:3, 0, 1] = 1
            element[0:3, 3, 4] = 1

        if index == 48:
            element[0:3, 1:4, 4] = 1
            element[0:3, 0, 1:4] = 1
            element[0:3, 1, 0] = 1
            element[0:3, 4, 3] = 1

        if index == 49:
            for e in range(0, 3):
                np.fill_diagonal(element[e], 1)
            element[0:3, 0:5, 4] = 1

        if index == 50:
            element[0:3, 0, 2] = 1
            element[0:3, 1, 1] = 1
            element[0:3, 1, 3] = 1
            element[0:3, 2, 0] = 1
            element[0:3, 2, 4] = 1
            element[0:3, 3, 1] = 1
            element[0:3, 3, 3] = 1
            element[0:3, 4, 2] = 1

        return element


# Start script
start_time = time.time()

# Se obtiene el path donde estan los cheques con la firma
path = sys.argv[1]

# Obtener las imagenes dentro del path
images = [f for f in glob.glob(path + "**/*.png", recursive=True)]

# Inicializacion de variables
count = 0
convolutions_list, signatures = [[], []]

# Se hace un loop para realizar el procedimiento de extraccion para cada imagen
for image_name in images:
    # Numerar las imagenes
    count += 1

    # Abrir la imagen binarizada
    binarized_image = cv2.imread(image_name)

    check = Check()
    convolutions = []

    print("##### Firma No. {} #####".format(count))
    """
    Transposicion de los elementos estructurales
    """
    for index, element in enumerate(check.build_elements(), start=1):

        print("EE #{}".format(index))
        convolution = scipy.ndimage.convolve(binarized_image, element, mode='nearest').transpose()
        Channel, W, H = binarized_image.shape
        count_element = 0
        # Contabilizacion de las convoluciones entre los elementos y la imagen binarizada
        for i in range(H):
            for j in range(W):
                for h in convolution[i, j]:
                    if h == 0:
                        count_element += 1

        convolutions.append(count_element)

    convolutions_list.append(convolutions)

"""
Patrones reales por la erosion
"""
final_convolutions = [list(np.append(item, "SI")) for item in convolutions_list]

"""
Generacion de patrones sinteticos positivos por renglon (firma)
"""
convolutions_list = np.array(convolutions_list)
for row in range(50):
    insert_cols = []
    # Calcular valores positivos para cada columna (elemento estructurado)
    for column in range(Check.min_struct_elements):
        vector = convolutions_list[0: Check.min_signs, column]
        ds_mas = np.around((np.sum(vector) + np.std(vector)) / Check.min_signs)
        ds_menos = np.around((np.sum(vector) - np.std(vector)) / Check.min_signs)
        insert_cols.append(
            np.around((ds_mas - ds_menos) * np.random.rand(1)[0] + ds_menos)
        )

    insert_cols.append("SI")
    final_convolutions.append(insert_cols)

"""
Generacion de patrones sinteticos negativos entre 1 y 300
"""
for row in range(50):
    insert_cols = []
    # Numero aleatorio para cada columna (elemento estructurado)
    for column in range(Check.min_struct_elements):
        insert_cols.append(
            np.around(np.random.randint(1, 300))
        )
    insert_cols.append("NO")
    final_convolutions.append(insert_cols)

# Elapsed time
e = int(time.time() - start_time)
print('Time elapsed {:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

# Print data
for item in final_convolutions:
    print(item)

# Write all data set in a CSV file
# Se almacena el set de datos en un archivo CSV
np.savetxt("Firmas.csv", final_convolutions, delimiter=",", fmt='%s')
