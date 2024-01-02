from fastapi import FastAPI
from pydantic import BaseModel
import base64
import cv2
import numpy as np
import uvicorn
from PIL import Image
import io
import face_recognition
import os
class Img(BaseModel):
    url: str | None = None
    name: str | None = None

app = FastAPI()
known_faces = []
@app.post("/CadastroImage")
async def create_image(image: Img):
    lista = []
    img = base64.b64decode(image.url)
    imag = Image.open(io.BytesIO(img))
    imag.convert('RGB')
    imag.save(f"{image.name}.jpg")
    img2 = cv2.imread(f"{image.name}.jpg")
    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
    os.remove(f"{image.name}.jpg")
    lista.append(image.name)
    lista.append(img_encoding2)
    known_faces.append(lista)
    print(known_faces)
    print(len(known_faces))
  


    return {"message": "Image received"}

@app.post("/Reconhecimento")
async def create_image(image: Img):
    i=0
    while(i<len(known_faces)):
        result = face_recognition.compare_faces([known_faces[i][1]], img_encoding2)
        if(result[0]):
            print("Result: ", result)
            print("Distance: ", face_recognition.face_distance([known_faces[i][1]], img_encoding2))
            print("Name: ", known_faces[i][0])
            break
        i+=1
        if not result[0]:
            print("Not found")
