# API Face Recognition

## Instalação

Use o [Anaconda](https://www.anaconda.com/download) para instalar o python e as bibliotecas utilizadas.

```bash
pip install face_recognition
pip install opencv-python
conda install pydantic -c conda-forge
pip install fastapi
pip install uvicorn
conda install conda-forge::pybase64
conda install anaconda::pillow
```

## Utilização

Esta Api possui 3 portas POST
 - /CadastroImagem
 - /Reconhecimento
 - /ComparaImagens

### /CadastroImagem
Armazena a imagem junto as informações para futuramente serem utilizadas para comparação na porta **/Reconhecimento**. 

#### Entradas
```json
"url": "<string base64 da imagem>",
"name": "<string>",
"cpf": "<string>"
```
