import numpy as np
from numpy import linalg as LA

class Imagem():
  def __init__(self, dados):

    self.vertices = [] #vetor de vertices
    self.faces = [] #vetor de faces
    self.normal_face = []
    self.intensidade_face = []
    self.intensidade_vertice = []
    self.faces_por_vertice = []

    #inicializa os atributos de menor e maior X, Y e Z
    self.menorX = float(dados[0][1])
    self.maiorX = float(dados[0][1])

    self.menorY = float(dados[0][2])
    self.maiorY = float(dados[0][2])

    self.menorZ = float(dados[0][3])
    self.maiorZ = float(dados[0][3])
    
    for i in range(len(dados)):
    
      aux = []
      
      #Se a linha comeca com 'v', atribui a matriz de vertices
      if(dados[i][0] == 'v'):
        aux.append(float(dados[i][1]))
        aux.append(float(dados[i][2]))
        aux.append(float(dados[i][3]))
        self.vertices.append(aux)

      #Se a linha comeca com 'f', atribui a matriz de faces
      if(dados[i][0] == 'f'):
        aux.append(int(dados[i][1]))
        aux.append(int(dados[i][2]))
        aux.append(int(dados[i][3]))
        self.faces.append(aux)

    self.normaliza()

  #Funcao para normalizar os vertices
  def normaliza(self):

    self.menorX = 4000
    self.maiorX = -4000
    self.menorY = 4000
    self.maiorY = -4000
    self.menorZ = 4000
    self.maiorZ = -4000

    for i in range(len(self.vertices)):
    
      aux = []
      
      if(float(self.vertices[i][0]) < self.menorX):
        self.menorX = float(self.vertices[i][0])

      if(float(self.vertices[i][0]) > self.maiorX):
        self.maiorX = float(self.vertices[i][0])

      if(float(self.vertices[i][1]) < self.menorY):
        self.menorY = float(self.vertices[i][1])

      if(float(self.vertices[i][1]) > self.maiorY):
        self.maiorY = float(self.vertices[i][1])

      if(float(self.vertices[i][2]) < self.menorZ):
        self.menorZ = float(self.vertices[i][2])

      if(float(self.vertices[i][2]) > self.maiorZ):
        self.maiorZ = float(self.vertices[i][2])

    #calcula a media dos vertices
    mediaX = (self.menorX + self.maiorX)/2
    mediaY = (self.menorY + self.maiorY)/2
    mediaZ = (self.menorZ + self.maiorZ)/2

    #Calcula a distancia entre o menor e o maior ponto de cada orientacao
    distanciaX = (abs(self.menorX) + abs(self.maiorX))
    distanciaY  = (abs(self.menorY) + abs(self.maiorY))
    distanciaZ  = (abs(self.menorZ)+ abs(self.maiorZ))

    distanciaMax = max(distanciaX, distanciaY, distanciaZ)

    #Aplica a transformacao final para deixar os vertices entre -1 e 1
    self.aplica_transformacao([self.escala(2/distanciaMax, 2/distanciaMax, 2/distanciaMax), self.translacao(-mediaX, -mediaY, -mediaZ)])


  #metodos get e set da imagem
  def getQtdVertices(self):
    return len(self.vertices)

  def getVertice(self, x):
    return self.vertices[x]

  def getVertices(self, x, y):
    return self.vertices[x][y]
    
  def getFace(self, x):
    return self.faces[x]

  def getFaces(self, x, y):
    return self.faces[x][y]

  def getFacesLen(self):
    return len(self.faces)

  def getVerticesLen(self):
    return len(self.vertices)

  def setFaces(self, x, y, value):
    self.faces[x][y] = value

  def setVertice(self, x, y, value):
    self.vertices[x][y] = value

  #escreve o objeto em um arquivo.obj
  def write_obj(self, obj):
    with open('{}_NOVO.obj'.format(obj), 'w') as w:

      for i in range(len(self.vertices)):                
        w.write('v {} {} {}'.format(self.vertices[i][0], self.vertices[i][1], self.vertices[i][2]))
        w.write('\n')

      for i in range(len(self.faces)):                
        w.write('f {} {} {}'.format(self.faces[i][0], self.faces[i][1], self.faces[i][2]))
        w.write('\n')
    w.close()

  def aplica_transformacao(self, matriz):

    transformacao = matriz[0]
    #multiplica todas transformções da lista matriz
    for i in range(1, len(matriz)):
      transformacao = np.matmul(transformacao, matriz[i])

    #executa a transformação final em cada vertice
    for i in range(len(self.vertices)):

      aux = []
      aux.append(float(self.vertices[i][0]))
      aux.append(float(self.vertices[i][1]))
      aux.append(float(self.vertices[i][2]))
      aux.append(float(1))
      
      vetor = np.array(aux)
      novo_vetor = np.matmul(transformacao, vetor)

      self.vertices[i][0] = novo_vetor[0]
      self.vertices[i][1] = novo_vetor[1]
      self.vertices[i][2] = novo_vetor[2]

  #gera matriz de escala
  def escala(self, escalaX, escalaY, escalaZ):

    matriz = np.array([[escalaX,      0,      0,    0],
                       [     0, escalaY,      0,    0],
                       [     0,      0, escalaZ,    0],
                       [     0,      0,       0,    1]])


    return matriz

  #gera matriz de translação
  def translacao(self, dx, dy, dz):

    matriz = np.array([[     1,      0,      0,   dx],
                       [     0,      1,      0,   dy],
                       [     0,      0,      1,   dz],
                       [     0,      0,      0,    1]])

    return matriz
  
  #gera matriz de rotação no eixo Z
  def rotacaoZ(self, angulo):
    rad = np.pi * (angulo/180)
    matriz = np.array([[np.cos(rad), -np.sin(rad),           0,       0],
                       [np.sin(rad),  np.cos(rad),           0,       0],
                       [          0,            0,           1,       0],
                       [          0,            0,           0,       1]])

    return matriz

  #gera matriz de rotação no eixo X
  def rotacaoX(self, angulo):

    rad = np.pi * (angulo/180)

    matriz = np.array([[           1,            0,            0,       0],
                       [           0,  np.cos(rad), -np.sin(rad),       0],
                       [           0,  np.sin(rad),  np.cos(rad),       0],
                       [           0,            0,            0,       1]])

    return matriz
    
  #gera matriz de rotação no eixo Y
  def rotacaoY(self, angulo):

    rad = np.pi * (angulo/180)

    matriz = np.array([[  np.cos(rad),           0,  np.sin(rad),       0],
                       [            0,           1,            0,       0],
                       [ -np.sin(rad),           0,  np.cos(rad),       0],
                       [            0,           0,            0,       1]])

    return matriz

  def ordena_faces(self):

    #ordena baseado na média do eixo Z de cada vértice da face
    self.faces.sort(key=self.distancia_z)

  def distancia_z(self, img):
    return (self.getVertices(img[0]-1, 2) + self.getVertices(img[1]-1, 2) + self.getVertices(img[2]-1, 2))/3 


  def calcula_normais(self):

    self.normal_face = []

    #Para cada face com vertices A, B e C. Calcula os vetores AB e AC, e faz o produto vetorial entre eles para achar a normal

    for vertices in self.faces:

      v1 = self.getVertice(vertices[0]-1)
      v2 = self.getVertice(vertices[1]-1)
      v3 = self.getVertice(vertices[2]-1)

      vetor1 = [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]]
      norm = LA.norm(vetor1)
      vetor1 = vetor1/norm

      vetor2 = [v2[0]-v3[0], v2[1]-v3[1], v2[2]-v3[2]]
      norm = LA.norm(vetor2)
      vetor2 = vetor2/norm

      normal = np.cross(vetor1, vetor2)

      self.normal_face.append(normal)

  def calcula_intensidade(self, luz):

    self.intensidade_face = []   

    #calcula a intensidade de cada face a partir da sua normal e do vetor de luz definido anteriormente 

    norm = LA.norm(luz)
    luz = luz/norm

    for normais in self.normal_face:

      norm = LA.norm(normais)
      normais = normais/norm

      produto = luz[0]*normais[0] + luz[1]*normais[1] + luz[2]*normais[2] #L * N

      self.intensidade_face.append(produto)

  def calcula_intensidade_vertice(self):

    #A intensidade de cada vétice é calculada a partir da média da intensidade de todas as faces o qual ela faz parte

    self.intensidade_vertice = [] 
    self.faces_por_vertice = []

    for i in range(self.getQtdVertices()):
      self.faces_por_vertice.append([])

    for i in range(self.getFacesLen()):

      face_atual = self.getFace(i)

      self.faces_por_vertice[face_atual[0]-1].append(i) 
      self.faces_por_vertice[face_atual[1]-1].append(i) 
      self.faces_por_vertice[face_atual[2]-1].append(i) 

    for i in range(len(self.faces_por_vertice)):
      soma = 0
      tamanho = len(self.faces_por_vertice[i])

      for j in range(tamanho):
        soma = soma + self.intensidade_face[self.faces_por_vertice[i][j]]

      media = soma/tamanho

      self.intensidade_vertice.append(media)




#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#
