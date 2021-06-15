
import classCena as Cena
import classImagem as Imagem
import classCamera as Camera
import classCanvas as Canvas
import wx
from wx import *

#le o arquivo obj
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

  #Le o arquivo .obj e o armazena suas informacoes em uma matriz
  nome_objeto = 'coarseTri.hand'
  mao = read_object(nome_objeto)

  #Atribui a matriz recebida a uma imagem, que armazenara os dados sobre vertices e faces da imagem
  img = Imagem.Imagem(mao)

  #inicializa uma cena
  cena = Cena.Cena() 

  #Coloca quantas imagens for necessario na cena, nessa fase do trabalho iremos trabalhar apenas com uma
  cena.insereObjetos([img])

  #Exemplo de algumas transformacoes possiveis da imagem
  img.aplica_transformacao([img.translacao(3, 0, 0), img.rotacaoZ(30)])
  
  #Posicao da camera
  e_camera = [3 , 3 , 3]
  #Direcao que a camera esta apontando
  g_camera = [0, 0, 0]
 
  t_camera = [0 , -1 , 1]

  #Cria a cena da camera de acordo com os parametros passados
  camera = Camera.Camera(e_camera, g_camera, t_camera)
  #Coloca a cena criada anteriormente nas coordenadas da camera, aplica a projeçao e normaliza a imagem
  camera.posiciona_imagem(cena, 1, 10, 1, 80)

  #retorna a cena em um arquivo de saida
  cena.writeScene("cena_Maos") 

  #Aplica a raterizacao e exibe em uma tela virtual
  app = wx.App(0)
  frame = wx.Frame(None, -1, nome_objeto)
  canvas = Canvas.Canvas(frame, img)
  frame.Show()
  app.MainLoop()

if __name__ == '__main__':
  main()
