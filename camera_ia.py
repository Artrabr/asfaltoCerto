
import cv2
import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "").strip()

# Open the camera.
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("couldnt find the camera :/")
    exit()


def analyze_image(frame):
    global client

    # Convert the image to JPEG.
    success, buffer = cv2.imencode(".jpg", frame)

    if not success:
        print("error to convert img")
        return

    api_key = GENAI_API_KEY
    if not api_key:
        print("Defina GEMINI_API_KEY para usar a IA")
        return

    if client is None:
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=20000,
                retry_options=types.HttpRetryOptions(attempts=1)
            )
        )

    # Convert the image to bytes.
    image_bytes = buffer.tobytes()

    print("\nAnalisando imagem com IA...")
    start_time = time.perf_counter()

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                ),
                """
                Analise esta imagem.

                caso tenha alguem na imagem 
                identifique qual o sexo da pessoa
                possivel idade
                possivel nascionalidade

                retorne no formato do exemplo e nunca use * sem ser ao redor da saida

                (exemplo)
                *pessoa = {"sexo":"masculino","idade":5,"pais":"inglaterra"}*
                """
            ]
        )

        print("\nRESULTADO DA IA:")
        print(response.text)

    except Exception as error:
        print("analyze error:", error)

    finally:
        elapsed_time = time.perf_counter() - start_time
        print(f"analyze execution time: {elapsed_time:.2f}s")


client = None
print("Câmera iniciada")
print("ESPAÇO = Capturar e analisar")
print("Q = Sair")

while True:
    success, frame = camera.read()

    if not success:
        print("capture error")
        break

    cv2.imshow("AsfaltoCerto - IA", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(" "):
        analyze_image(frame)

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
