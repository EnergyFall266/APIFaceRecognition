from fastapi import FastAPI
from pydantic import BaseModel
import base64
import cv2
from PIL import Image
import io
import face_recognition
import os

class Img2(BaseModel):
    url1: str
    url2: str
class Img(BaseModel):
    url: str
    name: str 
    cpf: str

app = FastAPI()
known_faces = []
@app.post("/CadastroImagem")
async def CadastroImagem(image: Img):
    lista = []

    img = base64.b64decode(image.url)
    imag = Image.open(io.BytesIO(img))
    imag.convert('RGB')
    imag.save(f"{image.name}.jpg")
    img2 = cv2.imread(f"{image.name}.jpg")
    rgb_img = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(rgb_img)[0]
    os.remove(f"{image.name}.jpg")
    lista.append(image.name)
    lista.append(image.cpf)
    lista.append(img_encoding)
    known_faces.append(lista)
    print(known_faces)
    print(len(known_faces))
  


    return {"message": "Sign up successful"}

@app.post("/Reconhecimento")
async def Reconhecimento(image: Img):
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
        result = face_recognition.compare_faces([known_faces[i][2]], img_encoding2)
        print(result[0])
        if(result[0]):
            return {"message": "Person found",
                    "name": known_faces[i][0],
                    "cpf": known_faces[i][1],
                    "distance": face_recognition.face_distance([known_faces[i][2]], img_encoding2)[0]}
            
        i+=1
    if not result[0]:
        return {"message": "Person not found"}

@app.post("/ComparaImagens")
async def ComparaImagens(image: Img2):
    img = base64.b64decode(image.url1)
    imag = Image.open(io.BytesIO(img))
    imag.convert('RGB')
    imag.save("img1.jpg")
    img2 = cv2.imread("img1.jpg")
    rgb_img = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(rgb_img)[0]
    os.remove("img1.jpg")

    img3 = base64.b64decode(image.url2)
    imag2 = Image.open(io.BytesIO(img3))
    imag2.convert('RGB')
    imag2.save("img2.jpg")
    img4 = cv2.imread("img2.jpg")
    rgb_img2 = cv2.cvtColor(img4, cv2.COLOR_BGR2RGB)
    img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
    os.remove("img2.jpg")

    result = face_recognition.compare_faces([img_encoding], img_encoding2)
    if(result[0]):
        return {"message": "Faces are the same"}
    else:
        return {"message": "Faces are not the same"}