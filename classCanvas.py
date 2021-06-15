import numpy as np
from numpy import linalg as LA
import wx

class Canvas(wx.Panel):
  def __init__(self, parent, img):
      self.img = img
      wx.Panel.__init__(self, parent, -1)
      self.Bind(wx.EVT_PAINT, self.on_paint)
      self.Bind(wx.EVT_SIZE, self.on_size)
    
  #da refresh ao dar resize na janela
  def on_size(self, evt):
      self.Refresh()
  
  #desenhar na janela
  def on_paint(self, evt):
      w,h = self.GetClientSize()
      dc = wx.PaintDC(self)
      dc.Clear()
      bmp = self.get_bitmap(w,h)
      dc.DrawBitmap(bmp, 0 ,0)
      
  #transformar em bitmap
  def get_bitmap(self, w, h):
      data = np.zeros((800, 800, 3),np.uint8)

      img2 = []

      #Recebe os vertices do objeto e os transforma em coordenadas da matriz de bitmap
      for i in range(self.img.getQtdVertices()):

        x = round(400 * (self.img.getVertices(i, 0) + 1) - 1)
        y = round(400 * (self.img.getVertices(i, 1) + 1) - 1)

        img_aux = []

        img_aux.append(x)
        img_aux.append(y)

        img2.append(img_aux)

      #Le todas as faces do objeto e atribuimos cada um dos vertices para as variaveis v1, v2 e v3, esses vertices constituem os trinagulos que serão "pintados"
      for i in range(0, self.img.getFacesLen(), 1):

        v1 = []
        v2 = []
        v3 = []

        v1.extend([img2[self.img.getFaces(i, 0)-1][0], img2[self.img.getFaces(i, 0)-1][1]])

        v2.extend([img2[self.img.getFaces(i, 1)-1][0], img2[self.img.getFaces(i, 1)-1][1]])

        v3.extend([img2[self.img.getFaces(i, 2)-1][0], img2[self.img.getFaces(i, 2)-1][1]])

        self.desenha_triangulo(v1, v2, v3, data)
      
      bmp = wx.Bitmap.FromBuffer(800, 800,data)
      return bmp
    
  #"Pinta" a matriz do bitmap
  def desenha_linha(self, curx1, curx2, scanline, data):

    if(curx1 == curx2):
      data[scanline][curx1] = [255, 0, 255]
    else:
      for i in range(curx1-2, curx2+2):
        data[scanline][i] = [255, 0, 255]

  #metodos auxiliares de desenha triangulo: desenha o triangulo de cima
  def desenha_triangulo_cima(self, v1, v2, v3, data):
    invslope1 = float ((v2[0] - v1[0]) / (v2[1] - v1[1]))
    invslope2 = float ((v3[0] - v1[0]) / (v3[1] - v1[1]))

    curx1 = v1[0]
    curx2 = v1[0]

    scanlineY = round(v1[1]) 

    while(scanlineY <= v2[1]):

      self.desenha_linha(round(curx1), round(curx2), scanlineY, data)
      curx1 = curx1 + invslope1
      curx2 = curx2 + invslope2
      scanlineY = scanlineY + 1

  #desenha triangulo de baixo
  def desenha_triangulo_baixo(self, v1, v2, v3, data):
    invslope1 = (v3[0] - v1[0]) / (v3[1] - v1[1])
    invslope2 = (v3[0] - v2[0]) / (v3[1] - v2[1])

    curx1 = v3[0]
    curx2 = v3[0]

    scanlineY = int(v3[1]) 

    while(scanlineY > v1[1]):
      self.desenha_linha(round(curx1), round(curx2), scanlineY, data)
      curx1 = curx1 - invslope1
      curx2 = curx2 - invslope2
      scanlineY = scanlineY - 1

  #preenche as faces de formato triangular (rasterizacao)
  def desenha_triangulo(self, v1, v2, v3, data):

    if(v1[1] == v2[1] and v3[1] == v2[1]):
      v1[1] = v1[1] - 1

    #sort
    if(v1[1] < v2[1]):
      if (v2[1] > v3[1]):
        if (v1[1] < v3[1]):
          v1, v3 = v3, v1
        else:
          v1, v2, v3 = v3, v1, v2
    else:
      if (v2[1] < v3[1]):
        if (v1[1] < v3[1]):
          v1, v2 = v2, v1
        else:
          v1, v2, v3 = v2, v3, v1
      else:
        v1, v3 = v3, v1



    if(v2[1] == v3[1]):
      self.desenha_triangulo_cima(v1, v2, v3, data)
    elif(v1[1] == v2[1]):
      self.desenha_triangulo_baixo(v1, v2, v3, data)
    else:
      v4 = []
      v4.append(int((v1[0] + ((v2[1] - v1[1]) / (v3[1] - v1[1])) * (v3[0] - v1[0]))))
      v4.append(v2[1])
      self.desenha_triangulo_cima(v1, v2, v4, data)
      self.desenha_triangulo_baixo(v2, v4, v3, data)
