from PIL import Image
import json
from math import floor
import pygame as pg
from pathlib import Path



class Skeleton():
    def __init__(self, x, y):
        # Physics attributes
        self.x = x
        self.y = y
        self.speed = 5

        # Image Attributes
        self.facing_right = True
        self.w = 43
        self.h = 37
        self.scale = 4
        #self.center = (10, 23)

        # State Attributes
        self.state = 0
        self.action = 1
        ''' Not Actions{ Idle : 0, Walk : 1 }
            Actions{ Attack : 2, React : 3}

            => Is performing an action if self.state > self.action  (Last of not actions)
        '''

        # Animation Attributes
        self.walk_animation = []
        self.idle_animation = []
        self.react_animation = []
        self.attack_animation = []

        self.animation_len = {}
        
        self.animation_index = 0
        self.animation_speed = 0.3

        path = str(Path(__file__).resolve().parents[2]).replace("\\", "/") + "/Images/Sprites/Skeleton/"
        print(f"path: {path}")
        self.loadAnimations(path)

        # Debugging Attributes
        self.show_hitbox = False


    def isInAction(self):
        return self.state > self.action


    def showHitbox(self):
        self.show_hitbox = not self.show_hitbox


    def loadAnimations(self, path : str):
        # Idle
        with Image.open(path + "Sprite Sheets/Skeleton Idle.png") as idle_sheet:
            with open(path + "Files/idle_frames.json") as json_data:
                data = json.load(json_data)
                suma = 0
                for frame in data["frames"]:
                    pos = frame["position"]
                    sprite_frame = idle_sheet.crop((pos["x"], pos["y"], pos["x"] + pos["w"], pos["y"] + pos["h"]))
                    data = sprite_frame.tobytes()
                    surface = pg.image.fromstring(data, sprite_frame.size, sprite_frame.mode)
                    self.idle_animation.append(surface)
                    suma += 1
                self.animation_len[0] = suma

        # Walk
        with Image.open(path + "Sprite Sheets/Skeleton Walk.png") as walk_sheet:
            with open(path + "Files/walk_frames.json") as json_data:
                data = json.load(json_data)
                suma = 0
                for frame in data["frames"]:
                    pos = frame["position"]
                    sprite_frame = walk_sheet.crop((pos["x"], pos["y"], pos["x"] + pos["w"], pos["y"] + pos["h"]))
                    data = sprite_frame.tobytes()
                    surface = pg.image.fromstring(data, sprite_frame.size, sprite_frame.mode)
                    self.walk_animation.append(surface)
                    suma += 1
                self.animation_len[1] = suma
        
        # Attack
        with Image.open(path + "Sprite Sheets/Skeleton Attack.png") as attack_sheet:
            with open(path + "Files/attack_frames.json") as json_data:
                data = json.load(json_data)
                suma = 0
                for frame in data["frames"]:
                    pos = frame["position"]
                    sprite_frame = attack_sheet.crop((pos["x"], pos["y"], pos["x"] + pos["w"], pos["y"] + pos["h"]))
                    data = sprite_frame.tobytes()
                    surface = pg.image.fromstring(data, sprite_frame.size, sprite_frame.mode)
                    self.attack_animation.append(surface)
                    suma += 1
                self.animation_len[2] = suma

        # React
        with Image.open(path + "Sprite Sheets/Skeleton React.png") as react_sheet:
            with open(path + "Files/react_frames.json") as json_data:
                data = json.load(json_data)
                suma = 0
                for frame in data["frames"]:
                    pos = frame["position"]
                    sprite_frame = react_sheet.crop((pos["x"], pos["y"], pos["x"] + pos["w"], pos["y"] + pos["h"]))
                    data = sprite_frame.tobytes()
                    surface = pg.image.fromstring(data, sprite_frame.size, sprite_frame.mode)
                    self.react_animation.append(surface)
                    suma += 1
                self.animation_len[3] = suma 


    def Idle(self):
        self.state = 0
        self.animation_index = 0
        self.animation_speed = 0.2


    def Walk(self):
        self.state = 1
        self.animation_index = 0
        self.animation_speed = 0.3


    def Attack(self):
        self.state = 2
        self.animation_index = 0
        self.animation_speed = 0.6


    def React(self):
        self.state = 3
        self.animation_index = 0.2


    def currentAction(self):
        if self.state == 0:
            return "Idle"
        elif self.state == 1:
            return "Walk"
        elif self.state == 2:
            return "Attack"
        elif self.state == 3:
            return "React"
        return None


    def animate(self):
        self.animation_index += self.animation_speed

        if(floor(self.animation_index) > (self.animation_len[self.state] - 1)):
            if self.isInAction():
                self.Walk()
            else:
                self.animation_index -= self.animation_len[self.state]
        

    def display(self, screen):
        index = floor(self.animation_index)

        if self.state == 0:
            img = self.idle_animation[index]
        elif self.state == 1:
            img = self.walk_animation[index]
        elif self.state == 2:
            img = self.attack_animation[index]
        elif self.state == 3:
            img = self.react_animation[index]

        img_offset = (10, 23)

        # Is facing left?
        if self.facing_right: # If so flip images
            upperLeftCorner = (self.x - img_offset[0] * self.scale, self.y - img_offset[1] * self.scale)
        else:
            upperLeftCorner = (self.x - (self.w - img_offset[0]) * self.scale, self.y - img_offset[1] * self.scale)
            img = pg.transform.flip(img, True, False)


        img = pg.transform.scale(img, (self.w * self.scale, self.h * self.scale))

        screen.blit(img, upperLeftCorner)

        if (self.show_hitbox):
            pg.draw.rect(screen, (0, 255, 0), (upperLeftCorner[0], upperLeftCorner[1], self.w * self.scale, self.h * self.scale), 2)



    def setPos(self, x, y):
        self.x = x
        self.y = y

    
    def setSpeed(self, speed):
        self.speed = speed

    
    def setScale(self, scale):
        self.scale = scale


    ''' Movement
    '''

    def moveRight(self):
        self.x += self.speed
        self.facing_right = True

    def moveLeft(self):
        self.x -= self.speed
        self.facing_right = False