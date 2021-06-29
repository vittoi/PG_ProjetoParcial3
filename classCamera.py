import numpy as np
from numpy import linalg as LA

class Camera():
  def __init__(self, e, g, t):

    
    self.e = e #posicao da camera
    self.g = g #ponto observado

    self.t = t #top
    
    # n = (g - e) / ( |g - e| ) é divido em três partes a seguir:
    self.n = [g[0]-e[0], g[1]-e[1], g[2]-e[2]] #vetor normal ao plano de projecao
    norm = LA.norm(self.n)      
    self.n = self.n/norm 

    # n = (t X n) / ( |t X n| )
    self.u = np.cross(self.t, self.n)
    norm = LA.norm(self.u)               
    self.u = self.u/norm

    #Produto vetorial entre n e u
    self.v = np.cross(self.n, self.u)

    #Para a transformação de visualização:
    #Matriz R
    R = np.array([[self.u[0], self.u[1], self.u[2],        0],
                  [self.v[0], self.v[1], self.v[2],        0],
                  [self.n[0], self.n[1], self.n[2],        0],
                  [        0,         0,         0,        1]]) 
  
    #Matriz R
    T = np.array([[        1,         0,         0, -self.e[0]],
                  [        0,         1,         0, -self.e[1]],
                  [        0,         0,         1, -self.e[2]],
                  [        0,         0,         0,         1]]) 

    #Multiplicação das matrizes R e T
    self.M = np.matmul(R, T)
    
  def posiciona_imagem(self, cena, n, f, a, fov):
    #A projeção foi definida pelos parâmetros: ângulo de visão FOV (field of view), razão de aspecto (a), e planos de corte near e far

    radFov = np.pi * ((fov/2)/180) #Converte o Fov para radiano
    tan = np.tan(radFov) #Calcula o valor da tangente 
    print("Aguarde...")

    self.f = f #far
    self.n = n #near

    #Define os valores de algumas partes especificas da matriz
    a11 = 1/a*tan
    a22 = 1/tan
    a33 = -((f+n)/(f-n))
    a34 = -((2*f*n)/(f-n))

    #Matriz de projeção
    Mproj = ([[      a11,            0,          0,          0],
              [        0,           a22,         0,          0],
              [        0,             0,       a33,        a34],
              [        0,             0,        -1,          0]])

    #for para cada objeto da cena
    for i in range(cena.getQtdObjetos()):

      #Recebe cada objeto cena
      img = cena.getObjeto(i)

      #Calcula o vetor normal de cada face
      img.calcula_normais()

      #Calcula a intensidade da luz de acordo com a normal e o vetor da luz
      img.calcula_intensidade(cena.vetor_luz)

      #Calcula a intensidade de luz de cada vertice
      img.calcula_intensidade_vertice()

      img.aplica_transformacao([self.M, Mproj])

      #Ordena as faces para a aplicacao do algoritmo do pintor
      img.ordena_faces()


    cena.normaliza() #Aplica a normalização na cena
