
import cv2

# Abre a câmera padrão do computador
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("couldnt find the camera :(")
    exit()

while True:
    # Captura uma imagem da câmera
    sucess, img = camera.read()

    if not sucess: #nao sei pq mas eu ri
        print("error: something in the transmition went wrong :(")
        break

    # Mostra a imagem na tela
    cv2.imshow("camera", img)

    key = cv2.waitKey(1) & 0xFF

    #Q -> sair
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
