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

Esta Api possui 3 portas ***POST***.
 - /CadastroImagem
 - /Reconhecimento
 - /ComparaImagens

### /CadastroImagem
Armazena a imagem e as informações em uma lista para futuramente serem utilizadas pela porta **/Reconhecimento**. 

#### Entradas
```json
"url": "<string base64 da imagem>",
"name": "<string>",
"cpf": "<string>"
```
### Saída
Se tudo der certo a mensagem de retorno será:
```json
"message": "Imagem cadastrada com sucesso"
```

### /Reconhecimento
Compara a imagem enviada com as que ja estão salvas na lista.

### Entrada
```json
"url": "<string base64 da imagem>"
```
### Saída
Se a imagem enviada der *match* com alguma da lista ele retornará:
```json
"message": "Pessoa encontrada",
"name" : "<nome da pessoa>",
"cpf": "<cpf da pessoa>",

```

