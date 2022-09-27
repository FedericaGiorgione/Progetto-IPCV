import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import SlidesControllerWithInterface


tempDir = "temp/"
tempSavedDir = "tempMl/"
note = []


def createImg():
    backgroundImg = cv2.imread("Slides/background.jpg")
    #backgroundImg = cv2.resize(backgroundImg, None, fx=0.1, fy=0.1)
    print("disegno: ", note)
    print("salvataggio nuova foto")
    for i in range(len(note)):
        if i != 0:
             print('salva salva: ', i, ' =  ', note[i])
             backgroundImg = cv2.line(backgroundImg, note[i-1], note[i], (255, 255, 255), 1)
    cv2.imwrite(tempSavedDir + 'number.png', backgroundImg)
    backgroundImg = cv2.resize(backgroundImg, (28, 28))
    cv2.imwrite(tempSavedDir + 'number1.png', backgroundImg)
    print('foto salvataaaa')
    #invochiamo la funzione che prova a leggere il numero scritto
    #readImage()




# mnist = tf.keras.datasets.mnist
# (x_train, y_train), (x_test, y_test) = mnist.load_data()
#
# x_train = tf.keras.utils.normalize(x_train, axis=1)
# x_test = tf.keras.utils.normalize(x_test, axis=1)
#
# model = tf.keras.models.Sequential()
# model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
# model.add(tf.keras.layers.Dense(128, activation='relu'))
# model.add(tf.keras.layers.Dense(128, activation='relu'))
# model.add(tf.keras.layers.Dense(10, activation='softmax'))
#
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#
# model.fit(x_train, y_train, epochs=3)

#model.save('handwritten.model')


################DA SCOMMENTARE######################

def readImage():
    model = tf.keras.models.load_model('handwritten.model')

    try:
        img = cv2.imread(f"tempMl/number1.png")[:,:,0]
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        print(f"This digit is probably a {np.argmax(prediction)}")
        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
    except:
        print("Error!")


###############################################

# model = tf.keras.models.load_model('handwritten.model')
#
# image_number = 1
#
# try:
#     img = cv2.imread(f"tempMl/number1.png")[:,:,0]
#     img = cv2.resize(img, (28, 28))
#     img = np.invert(np.array([img]))
#     prediction = model.predict(img)
#     print(f"This digit is probably a {np.argmax(prediction)}")
#     plt.imshow(img[0], cmap=plt.cm.binary)
#     plt.show()
# except:
#     print("Error!")
# finally:
#     image_number += 1
