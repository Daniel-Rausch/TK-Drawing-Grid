from tkinter import Tk, Canvas, PhotoImage, mainloop

from PIL import Image, ImageDraw, ImageTk

from time import sleep
from datetime import datetime

class TKDrawingGrid():

    DEFAULT_COLOR = (255,255,255)

    def __init__(self, width, height, scale, workerfunction, sleeptimeMS):

        self.width = width
        self.height = height
        self._scale = scale
        self._workerfunction = workerfunction
        self._sleeptimeMS = sleeptimeMS

        self.pixels = []
        for _ in range(self.width):
            self.pixels.append( [TKDrawingGrid.DEFAULT_COLOR]*self.height)

        self._root = Tk()
        self._canvas = Canvas(self._root, width = self.width * self._scale, height = self.height * self._scale)
        self._canvas.pack()

        self._root.after(min(max(1,sleeptimeMS),500), self.runWorker)
        self.update()
        self._root.mainloop()


    def runWorker(self):
        self._workerfunction(self)
        self._root.after(max(1,self._sleeptimeMS), self.runWorker)


    def update(self):

        byteList = []
        for j in range(self.height):
            for i in range(self.width):
                for c in range(3):
                    byteList.append(self.pixels[i][j][c])

        pilImage = Image.frombytes("RGB", (self.width, self.height), bytes(byteList))
        pilImage = pilImage.resize((self.width * self._scale, self.height * self._scale), resample=Image.NEAREST)
        self._image = ImageTk.PhotoImage(pilImage)
        self._canvas.create_image(((self.width*self._scale)/2,(self.height*self._scale)/2), image = self._image)


class TestWorker(object):

    def __init__(self):
        self._i = 0

    def run(self, pane):
        pane.pixels[self._i % pane.width][self._i % pane.height] = (100 * (self._i%3), 100 * ((self._i+1)%3), 100 * ((self._i+2)%3))
        pane.update()
        #print(datetime.now())
        self._i += 1


worker = TestWorker()
myPane = TKDrawingGrid(100, 71, 10, worker.run, 0)