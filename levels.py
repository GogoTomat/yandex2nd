from player import Player
from platform import Platform
from button import Button
from door import Door
from star import Star
from enemy import Enemy
from spike import Spike

WIDTH = 1200

def load_level(level):
    if level == 1:
        return (
            Player(100, 500),
            [Platform(0,580,WIDTH,20), Platform(200,450,150,20), Platform(400,350,150,20), Platform(600,250,150,20)],
            Button(800,550,40,40, ""),
            Door(1100,480, None),
            [Star(250,430), Star(450,330), Star(650,230)],
            300,
            [Enemy(300,530,40,40,(300,500)), Enemy(700,330,40,40,(700,750))],
            [Spike(500,550,50,30), Spike(550,550,50,30)]
        )
    elif level == 2:
        return (
            Player(100, 500),
            [Platform(0,580,WIDTH,20), Platform(300,400,200,20), Platform(600,300,150,20)],
            Button(400,500,40,40, ""),
            Door(700,450, None),
            [Star(350,380), Star(620,280), Star(720,200)],
            600,
            [Enemy(200,530,40,40,(200,400)), Enemy(600,330,40,40,(600,800))],
            [Spike(200,550,50,30), Spike(400,550,50,30)]
        )
