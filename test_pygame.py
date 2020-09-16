import pygame
from abc import ABC, abstractmethod
from time import sleep


class Snake():
    """
    Объект змеи

    При определении задаются начальные параметры
    """
    def __init__(self, **kwargs):
        """
        Открытие окна
        """
        self.kwargs = {"w": 800, "h": 600, "size": 20, "fps": 30, "amount": 3}
        self.checkArguments(kwargs)

        pygame.init()
        self.game = pygame.display.set_mode((self.kwargs["w"], self.kwargs["h"]))
        self._clock = pygame.time.Clock()

        self.segments = []
        self._white = (255, 255, 255)
        self._black = (0, 0, 0)
        self.createStartSegments()

        self.clickHandler = {
            "Down": (0, 1), "Up": (0, -1), 
            "Left": (-1, 0), "Right": (1, 0)
            }
        self.vector = self.clickHandler["Right"]
        pygame.display.update()

    def checkArguments(self, kwargs):
        """
        Чек входящих аргументов
        """
        for kw in kwargs.keys():
            if kw in self.kwargs:
                self.kwargs[kw] = kwargs[kw]
        
    def main(self):
        """
        Цикл обновления окна
        """
        while 1:
            self._clock.tick(self.kwargs["fps"])
            self.game.fill(self._black)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return
                elif ev.type == pygame.KEYDOWN:
                    self.handlerKeys(ev.key)
            # Движение змеи
            self.move()
            pygame.display.update()

    def move(self):
        self.moveLogic()
        self.moveFirstSegment()

        for segment in self.segments:
            #print(segment)
            #FigureRect(self.game).draw(self._white, segment)
            #segment.move_ip(*self.vector)
            FigureRect(self.game).draw(self._white, segment)

    def handlerKeys(self, key):
        """
        Обработчик нажатий клавиш (стрелок)

        Изменяет вектор направления движения змеи
        """
        if key == pygame.K_DOWN:
            self.vector = self.clickHandler["Down"]
        elif key == pygame.K_UP:
            self.vector = self.clickHandler["Up"]
        elif key == pygame.K_LEFT:
            self.vector = self.clickHandler["Left"]
        elif key == pygame.K_RIGHT:
            self.vector = self.clickHandler["Right"]


    def createStartSegments(self):
        """
        Создание первых 3 сегментов
        """
        for i in range(self.kwargs["amount"]):
            self.segments.append(
                FigureRect().create(
                    i*self.kwargs["size"], 0, 
                    self.kwargs["size"], self.kwargs["size"])
                    )
    
    def restart(self):
        for segment in self.segments:
            del segment
        self.vector = self.clickHandler["Right"]

    def moveLogic(self):
        """
        Механика передвижения - вставка первого сегмента и удаление последнего
        """
        self.segments.insert(0, self.segments[0])

        self.segments.pop()
    
    def moveFirstSegment(self):
        """
        Передвижение головного сегмента согласно направлению
        """
        s = self.kwargs["size"]
        x, y = self.segments[0].x, self.segments[0].y
        self.segments[0] = FigureRect().create(
            x + self.vector[0]*s, y + self.vector[1]*s, s, s
            )
        
        


class Figure(ABC):
    """
    Фабрика для новых объектов-фигур

    Методы создания и отрисовки
    """
    def __init__(self, game=None):
        self.game = game

    @abstractmethod
    def draw(self, *args):
        pass

    @abstractmethod
    def create(self, *args):
        pass


class FigureRect(Figure):
    """
    Сегменты змейки - прямоугольники. Они постоянно отрисовываются
    """
    def draw(self, *args):
        pygame.draw.rect(self.game, args[0], args[1])

    def create(self, *args):
        """
        Создание фигуры
        """ 
        return pygame.rect.Rect(args)


class FigureCircle(Figure):
    """
    Еда в форме кругов
    """
    def draw(self, *args):
        pygame.draw.circle(self.game, args[0], args[1])

    def create(self, *args):
        return


if __name__ == "__main__":
    snake = Snake()
    snake.main()
    
