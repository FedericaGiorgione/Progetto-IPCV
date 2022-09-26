import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import SlidesControllerWithInterface


tempDir = "temp/"
tempSavedDir = "tempSaved/"
note = []


def createImg():
    backgroundImg = cv2.imread("Slides/background.jpg")
    #backgroundImg = cv2.resize(backgroundImg, None, fx=0.1, fy=0.1)
    print("disegno: ", note)
    print("salvataggio nuova foto")
    for i in range(len(note)):
         print('salva salva')
         for j in range(len(note[i])):
             if j != 0:
                 backgroundImg = cv2.line(backgroundImg, note[i][j - 1], note[i][j], (0,0,255), 5)
    cv2.imwrite(tempSavedDir + 'number.png', backgroundImg)
    print('foto salvataaaa')


    # aux = 1
    # while aux <= count:
    #     print("salvataggio nuova foto")
    #     if aux - 1 in arrayNote:
    #         note = arrayNote[aux - 1]
    #         print(note)
    #         for i in range(len(note)):
    #             for j in range(len(note[i])):
    #                 if j != 0:
    #                     blank_image = cv2.line(blank_image, note[i][j - 1], note[i][j], (0,0,0), 5)
    #     cv2.imwrite(tempSavedDir + 'out_img' + str(aux) + '.jpg', blank_image)
    #     aux += 1




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


#########################################################
# model = tf.keras.models.load_model('handwritten.model')
#
# image_number = 1
#
# try:
#     img = cv2.imread(f"image/testMl/digit1.png")[:,:,0]
#     img = np.invert(np.array([img]))
#     prediction = model.predict(img)
#     print(f"This digit is probably a {np.argmax(prediction)}")
#     plt.imshow(img[0], cmap=plt.cm.binary)
#     plt.show()
# except:
#     print("Error!")
# finally:
#     image_number += 1

