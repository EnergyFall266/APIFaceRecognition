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
    url: str
    name: str 

app = FastAPI()
known_faces = []
@app.post("/CadastroImage")
async def create_image(image: Img):
    lista = []
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(image.url, "utf-8"))))
    img.save('my-image.jpeg')
        
    # img = base64.b64decode(image.url)
    # imag = Image.open(io.BytesIO(img))
    # imag.convert('RGB')
    # imag.save(f"{image.name}.jpg")
    # img2 = cv2.imread(f"{image.name}.jpg")
    # rgb_img = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    # img_encoding = face_recognition.face_encodings(rgb_img)[0]
    # os.remove(f"{image.name}.jpg")
    # lista.append(image.name)
    # lista.append(img_encoding)
    # known_faces.append(lista)
    # print(known_faces)
    # print(len(known_faces))
  


    return {"message": "Sign up successful"}

@app.post("/Reconhecimento")
async def create_image(image: Img):
    img = base64.b64decode(image.url)
    imag = Image.open(io.BytesIO(img))
    imag.convert('RGB')
    imag.save(f"{image.name}.jpg")
    img2 = cv2.imread(f"{image.name}.jpg")
    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
    os.remove(f"{image.name}.jpg")
    i=0
    while(i<len(known_faces)):
        result = face_recognition.compare_faces([known_faces[i][1]], img_encoding2)
        if(result[0]):
            return {"message": "Person found",
                    "name": known_faces[i][0],
                    "distance": face_recognition.face_distance([known_faces[i][1]], img_encoding2)[0]}
            
        i+=1
    if not result[0]:
        return {"message": "Person not found"}
