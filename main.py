from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import cv2
from PIL import Image
import io
import face_recognition
import timeit
import os
import requests
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
    # platform: str
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



@app.post("/CadastroImagem")
async def CadastroImagem(images: List[ImgCad]):
    for image in images:
        lista = []
        imgCad = base64.b64decode(image.img)
        imagCad = Image.open(io.BytesIO(imgCad))
        imagCad.convert('RGB')
        imagCad.save(f"{image.name}.jpg")
        img2Cad = cv2.imread(f"{image.name}.jpg")
        rgb_imgCad = cv2.cvtColor(img2Cad, cv2.COLOR_BGR2RGB)
        img_encodingCad = face_recognition.face_encodings(rgb_imgCad)[0]
        os.remove(f"{image.name}.jpg")
        lista.append(image.name)
        lista.append(image.cpf)
        lista.append(img_encodingCad)
        known_faces.append(lista)
  


    return {"message": "Imagem cadastrada com sucesso"}

@app.post("/Reconhecimento")
async def Reconhecimento(image: ImgRec):
    imgRec = base64.b64decode(image.img)
    imagRec = Image.open(io.BytesIO(imgRec))
    imagRec.convert('RGB')
    imagRec.save("imagem.jpg")
    img2Rec = cv2.imread("imagem.jpg")
    rgb_img2Rec = cv2.cvtColor(img2Rec, cv2.COLOR_BGR2RGB)
    img_encoding2Rec = face_recognition.face_encodings(rgb_img2Rec)[0]
    os.remove("imagem.jpg")
    if(len(known_faces)==0):
        return {"message": "Nao ha pessoas cadastradas"}
    i=0
    while(i<len(known_faces)):
        result = face_recognition.compare_faces([known_faces[i][2]], img_encoding2Rec)
        if(result[0]):
            return {"message": "Pessoa encontrada",
                    "name": known_faces[i][0],
                    "cpf": known_faces[i][1],
                    }
            
    
        i+=1
    if not result[0]:
        return {"message": "Pessoa nao encontrada"}

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

        # if(data.platform == "ios"):
        #     imgPres = base64.b64decode(data.fotPar)
        #     imagPres = Image.open(io.BytesIO(imgPres))
        #     imagPres.convert('RGB')
        #     teste = imagPres.rotate(-90)
        #     teste.save("participante1.jpg")
        #     img2Pres1 = cv2.imread("participante1.jpg")

        # else:
            # imgPres = base64.b64decode(data.fotPar)
            # imagPres = Image.open(io.BytesIO(imgPres))
            # imagPres.convert('RGB')
            # imagPres.save("participante1.jpg")
            # img2Pres1 = cv2.imread("participante1.jpg")
        imgPres = base64.b64decode(data.fotPar)
        imagPres = Image.open(io.BytesIO(imgPres))
        imagPres.convert('RGB')
        imagPres.save("participante1.jpg")
        img2Pres1 = cv2.imread("participante1.jpg")
        rgb_imgPres1 = cv2.cvtColor(img2Pres1, cv2.COLOR_BGR2RGB)
        # if(len(face_recognition.face_encodings(rgb_imgPres1)) == 0):
        #         return {
        #             "codRet": 1,
        #             "msgRet": "Não foi possivel identificar a pessoa na imagem"
        #             }
        img_encodingComp1 = face_recognition.face_encodings(rgb_imgPres1)[0]
        os.remove("participante1.jpg")

        img3Comp2 = base64.b64decode(data.participantes)
        imag2Comp2 = Image.open(io.BytesIO(img3Comp2))
        imag2Comp2.convert('RGB')
        imag2Comp2.save("participante2.jpg")
        img4Comp2 = cv2.imread("participante2.jpg")
        rgb_img2Comp2 = cv2.cvtColor(img4Comp2, cv2.COLOR_BGR2RGB)
        # if(len(face_recognition.face_encodings(rgb_img2Comp2)) == 0):
        #         return {
        #             "codRet": 1,
        #             "msgRet": "Não foi possivel identificar a pessoa na imagem"
        #             }
        img_encoding2Comp2 = face_recognition.face_encodings(rgb_img2Comp2)[0]
        os.remove("participante2.jpg")

        resultComp = face_recognition.compare_faces([img_encodingComp1], img_encoding2Comp2)
        if(resultComp[0]):
            return {"codRet": 0,
                    "msgRet": "Autenticado com sucesso",}
        else:
            return {"codRet": 1,
                    "msgRet": "Usuario não Autenticado"}
    except:
        raise HTTPException(status_code=400, detail="Erro ao verificar presenca")
       
    # try:
    #     fp = open("log.txt", "a")

    #     start = timeit.default_timer()
    #     listaPessoas = []

    #     if(len(data.participantes)==0 ):
    #         return {
    #             "codRet": "1",
    #             "msgRet": "Não ha pessoas cadastradas"}
    #     if(data.fotPar == ""):
    #         return {
    #             "codRet": "1",
    #             "msgRet": "Não ha imagem para comparar"}
    #     for image in data.participantes:
    #         lista = []
    #         imgVer = base64.b64decode(image.fotCol)
    #         imagVer = Image.open(io.BytesIO(imgVer))
    #         imagVer.convert('RGB')
    #         imagVer.save("imagem.jpg")
    #         img2Ver = cv2.imread("imagem.jpg")
    #         rgb_imgVer = cv2.cvtColor(img2Ver, cv2.COLOR_BGR2RGB)
    #         if(len(face_recognition.face_encodings(rgb_imgVer)) == 0):
    #             return {
    #                 "codRet": 1,
    #                 "msgRet": "Não foi possivel identificar a pessoa na imagem"
    #                 }
    #         img_encodingVer = face_recognition.face_encodings(rgb_imgVer)[0]
    #         os.remove("imagem.jpg")
    #         lista.append(img_encodingVer)
    #         lista.append(image.nomFun)
    #         lista.append(image.numCad)
    #         lista.append(image.tipCol)
    #         lista.append(image.numEmp)
    #         lista.append(image.numCpf)
    #         listaPessoas.append(lista)

    #         stop = timeit.default_timer()
    #         fp.write(f"cadastro: {stop - start}\n")

    #         print('conversao: ', stop - start) 
 
    #     # print(listaPessoas)
    #     # print(data.fotPar)
    #     if(data.platform == "ios"):
    #         imgPres = base64.b64decode(data.fotPar)
    #         imagPres = Image.open(io.BytesIO(imgPres))
    #         imagPres.convert('RGB')
    #         teste = imagPres.rotate(-90)
    #         teste.save("imagem2.jpg")
    #         img2Pres = cv2.imread("imagem2.jpg")

    #     elif(data.platform == "android"):
    #         imgPres = base64.b64decode(data.fotPar)
    #         imagPres = Image.open(io.BytesIO(imgPres))
    #         imagPres.convert('RGB')
    #         # teste = imagPres.rotate(-90)
    #         imagPres.save("imagem2.jpg")
    #         img2Pres = cv2.imread("imagem2.jpg")

    #     else:
    #         return {
    #             "codRet": 1,
    #             "msgRet": "Plataforma não suportada"
    #             }



    #     rgb_img2Pres = cv2.cvtColor(img2Pres, cv2.COLOR_BGR2RGB)
    #     if(len(face_recognition.face_encodings(rgb_img2Pres)) == 0):
    #         return {
    #             "codRet": 1,
    #             "msgRet": "Não foi possivel identificar a pessoa na imagem"
    #             }
    #     img_encoding2Pres = face_recognition.face_encodings(rgb_img2Pres)[0]
    #     os.remove("imagem2.jpg")


    #     start1 = timeit.default_timer()
    #     i=0
    #     while(i<len(listaPessoas)):
    #         resultVer = face_recognition.compare_faces([listaPessoas[i][0]], img_encoding2Pres)
    #         if(resultVer[0]):
    #             stop1 = timeit.default_timer()
    #             fp.write(f"comparacao: {stop1 - start1}\n")
    #             return {"participante":{
    #                 "codRet": 0,
    #                 "msgRet": "Autenticado com sucesso",
    #                 "nomFun": listaPessoas[i][1],
    #                 "numCad": listaPessoas[i][2],
    #                 "tipCol": listaPessoas[i][3],
    #                 "numEmp": listaPessoas[i][4],
    #                 "numCpf": listaPessoas[i][5],
    #                 "tempo": stop1 - start1,

    #             }
    #                     }

    #         i+=1

    #     stop1 = timeit.default_timer()
    #     fp.write(f"comparacao: {stop1 - start1}\n")

    #     print('comparacao: ', stop - start) 
    #     fp.close()
    #     if not resultVer[0]:
    #         return {
    #             "codRet": 1,
    #             "msgRet": "Pessoa não encontrada"
    #             }

    # except:
    #     return {
    #         "codRet": 1,
    #         "msgRet": "Erro ao verificar presenca"
    #         }