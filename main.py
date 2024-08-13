from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import cv2
from PIL import Image
import io
import face_recognition
import os
import time
from typing import List

class ImgComp(BaseModel):
    img1: str
    img2: str
class ImgCad(BaseModel):
    img: str
    name: str 
    cpf: str
class ImgRec(BaseModel):
    img: str


class Info(BaseModel):
    nomFun: str
    fotCol: str
    numCad: int
    tipCol: int
    numEmp: int
    numCpf: int

class Data(BaseModel):
    platform: str
    fotPar: str
    participantes: str

app = FastAPI()
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
known_faces = []

@app.get("/")
async def root():

    return {"message": "Hello World"}

   



# @app.post("/CadastroImagem")
# async def CadastroImagem(images: List[ImgCad]):
#     for image in images:
#         lista = []
#         imgCad = base64.b64decode(image.img)
#         imagCad = Image.open(io.BytesIO(imgCad))
#         imagCad.convert('RGB')
#         imagCad.save(f"{image.name}.jpg")
#         img2Cad = cv2.imread(f"{image.name}.jpg")
#         rgb_imgCad = cv2.cvtColor(img2Cad, cv2.COLOR_BGR2RGB)
#         img_encodingCad = face_recognition.face_encodings(rgb_imgCad)[0]
#         os.remove(f"{image.name}.jpg")
#         lista.append(image.name)
#         lista.append(image.cpf)
#         lista.append(img_encodingCad)
#         known_faces.append(lista)
  


#     return {"message": "Imagem cadastrada com sucesso"}

# @app.post("/Reconhecimento")
# async def Reconhecimento(image: ImgRec):
#     imgRec = base64.b64decode(image.img)
#     imagRec = Image.open(io.BytesIO(imgRec))
#     imagRec.convert('RGB')
#     imagRec.save("imagem.jpg")
#     img2Rec = cv2.imread("imagem.jpg")
#     rgb_img2Rec = cv2.cvtColor(img2Rec, cv2.COLOR_BGR2RGB)
#     img_encoding2Rec = face_recognition.face_encodings(rgb_img2Rec)[0]
#     os.remove("imagem.jpg")
#     if(len(known_faces)==0):
#         return {"message": "Nao ha pessoas cadastradas"}
#     i=0
#     while(i<len(known_faces)):
#         result = face_recognition.compare_faces([known_faces[i][2]], img_encoding2Rec)
#         if(result[0]):
#             return {"message": "Pessoa encontrada",
#                     "name": known_faces[i][0],
#                     "cpf": known_faces[i][1],
#                     }
            
    
#         i+=1
#     if not result[0]:
#         return {"message": "Pessoa nao encontrada"}

@app.post("/ComparaImagens")
async def ComparaImagens(image: ImgComp):
    imgComp = base64.b64decode(image.img1)
    imagComp = Image.open(io.BytesIO(imgComp))
    imagComp.convert('RGB')
    imagComp.save("img1.jpg")
    img2Comp = cv2.imread("img1.jpg")
    rgb_imgComp = cv2.cvtColor(img2Comp, cv2.COLOR_BGR2RGB)
    img_encodingComp = face_recognition.face_encodings(rgb_imgComp)[0]
    os.remove("img1.jpg")


    img3Comp = base64.b64decode(image.img2)
    imag2Comp = Image.open(io.BytesIO(img3Comp))
    imag2Comp.convert('RGB')
    imag2Comp.save("img2.jpg")
    img4Comp = cv2.imread("img2.jpg")
    rgb_img2Comp = cv2.cvtColor(img4Comp, cv2.COLOR_BGR2RGB)
    img_encoding2Comp = face_recognition.face_encodings(rgb_img2Comp)[0]
    os.remove("img2.jpg")

    resultComp = face_recognition.compare_faces([img_encodingComp], img_encoding2Comp)
    if(resultComp[0]):
        return {"message": "Mesma pessoa"}
    else:
        return {"message": "Nao e a mesma pessoa"}

@app.post("/verifica-presenca")
async def VerificaPresenca( data: Data):
    try:
        start_time = time.time()
        imgPres = base64.b64decode(data.fotPar)
        imagPres = Image.open(io.BytesIO(imgPres))
        imagPres.convert('RGB')
        teste = imagPres.rotate(-90) if data.platform == "ios" else imagPres
        teste.save("participante1.jpg")
        img2Pres1 = cv2.imread("participante1.jpg")
        rgb_imgPres1 = cv2.cvtColor(img2Pres1, cv2.COLOR_BGR2RGB)
   
        img_encodingComp1 = face_recognition.face_encodings(rgb_imgPres1)[0]
        os.remove("participante1.jpg")

        img3Comp2 = base64.b64decode(data.participantes)
        imag2Comp2 = Image.open(io.BytesIO(img3Comp2))
        imag2Comp2.convert('RGB')
        imag2Comp2.save("participante2.jpg")
        img4Comp2 = cv2.imread("participante2.jpg")
        rgb_img2Comp2 = cv2.cvtColor(img4Comp2, cv2.COLOR_BGR2RGB)
  
        img_encoding2Comp2 = face_recognition.face_encodings(rgb_img2Comp2)[0]
        os.remove("participante2.jpg")

        resultComp = face_recognition.compare_faces([img_encodingComp1], img_encoding2Comp2)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if(resultComp[0]):
            return {"detail":{"codRet": 0,
                    "msgRet": "Autenticado com sucesso",
                    "tempo": elapsed_time}}
        else:
            return {"detail":{"codRet": 1,
                    "msgRet": "Usuario não Autenticado",
                    "tempo": elapsed_time}}
    except:
        raise HTTPException(status_code=400, detail={"codRet":1, "msgRet":"Erro ao verificar presenca"})
       
    