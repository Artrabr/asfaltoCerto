import cv2


class Camera:
    def __init__(self, index=0, window_name="Camera"):
        self.camera = cv2.VideoCapture(index)
        self.window_name = window_name
        self.last_capture = None

    def capturar_frame(self):
        success, frame = self.camera.read()
        if not success:
            raise RuntimeError("Erro ao capturar imagem da câmera")
        return frame

    def exibir_frame(self, frame):
        cv2.imshow(self.window_name, frame)

    def capturar_imagem(self, frame):
        self.last_capture = frame.copy()
        return self.last_capture

    def abrir_camera(self):
        if not self.camera.isOpened():
            self.fechar_camera()
            raise RuntimeError("Não foi possível acessar a câmera")

        print("Pressione ESPAÇO para capturar uma imagem ou Q para sair")

        try:
            while True:
                frame = self.capturar_frame()
                self.exibir_frame(frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                if key == ord(" "):
                    self.capturar_imagem(frame)
                    print("Imagem capturada")
        finally:
            self.fechar_camera()

    def fechar_camera(self):
        self.camera.release()
        cv2.destroyAllWindows()
