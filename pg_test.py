import numpy as np
from numpy import linalg as LA
import wx


class Camera():
  def __init__(self, e, g):

    self.e = e #posicao da camera
    self.g = g #ponto observado

    self.t = [0, -1, 0]

    self.n = [g[0]-e[0], g[1]-e[1], g[2]-e[2]] #vetor normal ao plano de projecao
    norm = LA.norm(self.n)               # n = (g - e) / ( |g - e| )
    self.n = self.n/norm

    self.u = np.cross(self.t, self.n)
    norm = LA.norm(self.u)               # n = (t X n) / ( |t X n| )
    self.u = self.u/norm

    self.v = np.cross(self.n, self.u)

    R = np.array([[self.u[0], self.u[1], self.u[2],        0],
                  [self.v[0], self.v[1], self.v[2],        0],
                  [self.n[0], self.n[1], self.n[2],        0],
                  [        0,         0,         0,        1]]) 

    T = np.array([[        1,         0,         0, -self.e[0]],
                  [        0,         1,         0, -self.e[1]],
                  [        0,         0,         1, -self.e[2]],
                  [        0,         0,         0,         1]]) 

    self.M = np.matmul(R, T)

    #print('{}\n\n{}\n\n{}'.format(self.n, self.u, self.v))

    
  def posiciona_imagem(self, cena):

    for i in range(cena.getQtdObjetos()):

      img = cena.getObjeto(i)

      for j in range(img.getQtdVertices()):

        aux = []
        aux.append(img.getVertices(j, 0))
        aux.append(img.getVertices(j, 1))
        aux.append(img.getVertices(j, 2))
        aux.append(float(1)) 

        vetor = np.array(aux)

        novo_vetor = np.matmul(self.M, vetor)

        #print('{} {}'.format(vetor, novo_vetor))

        img.setVertice(j, 0, novo_vetor[0])
        img.setVertice(j, 1, novo_vetor[1])
        img.setVertice(j, 2, novo_vetor[2])

#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

class Imagem():
  def __init__(self, dados):

    self.vertices = []
    self.faces = []

    self.menorX = float(dados[0][1])
    self.maiorX = float(dados[0][1])

    self.menorY = float(dados[0][2])
    self.maiorY = float(dados[0][2])

    self.menorZ = float(dados[0][3])
    self.maiorZ = float(dados[0][3])
    
    for i in range(len(dados)):
    
      aux = []
      
      if(dados[i][0] == 'v'):
        aux.append(float(dados[i][1]))
        aux.append(float(dados[i][2]))
        aux.append(float(dados[i][3]))
        self.vertices.append(aux)

        if(float(dados[i][1]) < self.menorX):
          self.menorX = float(dados[i][1])

        if(float(dados[i][1]) > self.maiorX):
          self.maiorX = float(dados[i][1])

        if(float(dados[i][2]) < self.menorY):
          self.menorY = float(dados[i][2])

        if(float(dados[i][2]) > self.maiorY):
          self.maiorY = float(dados[i][2])

        if(float(dados[i][3]) < self.menorZ):
          self.menorZ = float(dados[i][3])

        if(float(dados[i][3]) > self.maiorZ):
          self.maiorZ = float(dados[i][3])
          
      if(dados[i][0] == 'f'):
        aux.append(int(dados[i][1]))
        aux.append(int(dados[i][2]))
        aux.append(int(dados[i][3]))
        self.faces.append(aux)

    mediaX = (self.menorX + self.maiorX)/2
    mediaY = (self.menorY + self.maiorY)/2
    mediaZ = (self.menorZ + self.maiorZ)/2

    distanciaX = (abs(self.menorX) + abs(self.maiorX))
    distanciaY  = (abs(self.menorY) + abs(self.maiorY))
    distanciaZ  = (abs(self.menorZ)+ abs(self.maiorZ))

    distanciaMax = max(distanciaX, distanciaY, distanciaZ)

    print(1/distanciaMax)

    self.aplica_transformacao([self.escala(2/distanciaMax, 2/distanciaMax, 2/distanciaMax), self.translacao(-mediaX, -mediaY, -mediaZ)])

    """
    self.menorX = 0
    self.maiorX = 0
    self.menorY = 0
    self.maiorY = 0
    self.menorZ = 0
    self.maiorZ = 0

    for i in range(len(self.vertices)):
    
      aux = []
      
      if(dados[i][0] == 'v'):

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
          

    print('{} {} {} {} {} {}'.format(self.menorX, self.maiorX, self.menorY, self.maiorY, self.menorZ, self.maiorZ))
  """



  def getQtdVertices(self):
    return len(self.vertices)

  def getVertices(self, x):
    return self.vertices[x]

  def getVertices(self, x, y):
    return self.vertices[x][y]
    
  def getFaces(self, x):
    return self.faces[x]

  def getFaces(self, x, y):
    return self.faces[x][y]

  def getFacesLen(self):
    return len(self.faces)

  def getVerticesLen(self):
    return len(self.vertices)

  def getFacesLen(self):
    return len(self.faces)

  def setFaces(self, x, y, value):
    self.faces[x][y] = value

  def setVertice(self, x, y, value):
    self.vertices[x][y] = value

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

    for i in range(1, len(matriz)):
      transformacao = np.matmul(transformacao, matriz[i])

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

  def escala(self, escalaX, escalaY, escalaZ):

    matriz = np.array([[escalaX,      0,      0,    0],
                       [     0, escalaY,      0,    0],
                       [     0,      0, escalaZ,    0],
                       [     0,      0,       0,    1]])


    return matriz

  def translacao(self, dx, dy, dz):

    matriz = np.array([[     1,      0,      0,   dx],
                       [     0,      1,      0,   dy],
                       [     0,      0,      1,   dz],
                       [     0,      0,      0,    1]])

    return matriz
  
  def rotacaoZ(self, angulo):
    rad = np.pi * (angulo/180)
    matriz = np.array([[np.cos(rad), -np.sin(rad),           0,       0],
                       [np.sin(rad),  np.cos(rad),           0,       0],
                       [          0,            0,           1,       0],
                       [          0,            0,           0,       1]])

    return matriz

  def rotacaoX(self, angulo):

    rad = np.pi * (angulo/180)

    matriz = np.array([[           1,            0,            0,       0],
                       [           0,  np.cos(rad), -np.sin(rad),       0],
                       [           0,  np.sin(rad),  np.cos(rad),       0],
                       [           0,            0,            0,       1]])

    return matriz
    
  def rotacaoY(self, angulo):

    rad = np.pi * (angulo/180)

    matriz = np.array([[  np.cos(rad),           0,  np.sin(rad),       0],
                       [            0,           1,            0,       0],
                       [ -np.sin(rad),           0,  np.cos(rad),       0],
                       [            0,           0,            0,       1]])

    return matriz

#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#


class scene():
  def __init__(self):
    self.objs = []
    self.vObjn =0

  def insereObjetos(self, objs):
    
    for i in range(0, len(objs)):
      obj = objs[i]
      
      for j in range(0, obj.getFacesLen()):
        faceX = obj.getFaces(j,0)
        faceY = obj.getFaces(j,1)
        faceZ = obj.getFaces(j,2)
        
        obj.setFaces(j,0, faceX+self.vObjn)
        obj.setFaces(j,1, faceY+self.vObjn)
        obj.setFaces(j,2, faceZ+self.vObjn)

      self.vObjn += obj.getVerticesLen()
    self.objs.extend(objs)

  def writeScene(self, name):
    with open('{}_NOVO.obj'.format(name), 'w') as w:
      for obj in self.objs:    

        for i in range(obj.getVerticesLen()):                
          w.write('v {} {} {}'.format(obj.getVertices(i, 0), obj.getVertices(i, 1), obj.getVertices(i, 2)))
          w.write('\n')

        for i in range(obj.getFacesLen()):                
          w.write('f {} {} {}'.format(obj.getFaces(i, 0), obj.getFaces(i, 1), obj.getFaces(i, 2)))
          w.write('\n')
    w.close()

  def getObjeto(self, x):
    return self.objs[x]

  def getQtdObjetos(self):
    return len(self.objs)

#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#


class Canvas(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        
    def on_size(self, evt):
        self.Refresh()
        
    def on_paint(self, evt):
        w,h = self.GetClientSize()
        dc = wx.PaintDC(self)
        dc.Clear()
        bmp = self.get_bitmap(w,h)
        dc.DrawBitmap(bmp, 0 ,0)
        
    def get_bitmap(self, w, h):
        data = np.zeros((500, 500, 3),np.uint8)



        bmp = wx.Bitmap.FromBuffer(500,500,data)
        return bmp

def read_object(obj):

  data = []

  with open('{}.obj'.format(obj), 'r') as r:
    whole_file = r.read()
    lines = whole_file.split('\n')        
    for line in lines:            
      lines_fixed = line.split(' ')
      data.append(lines_fixed)
  r.close()

  data.pop(-1)

  return data

#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#

  
def main():

  nome_objeto = 'coarseTri.hand'
  mao = read_object(nome_objeto)
  img = Imagem(mao)

  cena = scene() 
  cena.insereObjetos([img])

  
  #e_camera = [300, 300, 300]
  #g_camera = [0, 0, 0]


  #camera = Camera(e_camera, g_camera)
  #camera.posiciona_imagem(cena)

  cena.writeScene("cena_Maos") 

  #app = wx.App(0)
  #frame = wx.Frame(None, -1, nome_objeto)
  #canvas = Canvas(frame)
  #frame.Show()
  #app.MainLoop()


if __name__ == '__main__':
  main()