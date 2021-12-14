import pyglet
from pyglet import _thread_trace_func, shapes, clock
import random
import math

from pyglet.graphics import draw
size = 1000
window = pyglet.window.Window(width=size, height=size)
batch = pyglet.graphics.Batch()
boids = []

population = 300

coherence = 0.05
seperation = 3
alignment = 0.01
visualRange = 100
velocity= 0.1

def initBoids():
    for i in range(population):
        #x y dx dy 
        boids.append([size*random.random(), size*random.random(), 1,1])
        
def steervector(body, targetx, targety, turnrate):
    body[2] += (body[2]-targetx)*turnrate
    body[3] += (body[3]-targety)*turnrate

def distance(b1,b2):
    return math.sqrt((b1[0]-b2[0])**2 + (b1[1]-b2[1])**2)

def updateb(currentboid):
    #list of boids within visual range
    
    if distance(currentboid,[size/2, size/2]) > size/2:
        targetxpos = currentboid[0] - currentboid[2]
        targetypos = currentboid[1] - currentboid[3]
        steervector(currentboid,2*targetxpos,2*targetypos, 1)
        
    active = []
    for i in boids:
        if distance(i,currentboid) < visualRange and i != currentboid:
            active.append(i)
    if active == []:
        currentboid[0]+=currentboid[2]
        currentboid[1]+=currentboid[3]
        return
    #steer towards center of mass 
    targetxpos = (sum([i[0] for i in active])/len(active))-currentboid[0]
    targetypos = (sum([i[1] for i in active])/len(active))-currentboid[1]
    steervector(currentboid, targetxpos,targetypos,coherence)

    #avoid other boids 
    for i in active:
        if distance(i,currentboid) < seperation:
            targetxpos = currentboid[0]-i[0]
            targetypos = currentboid[1]-i[1]
            steervector(currentboid, targetxpos,targetypos,coherence)
 

    #align with other boids accounting for alignment
    targetxvector = sum([i[2] for i in active])/len(active)
    targetyvector = sum([i[3] for i in active])/len(active)
    steervector(currentboid, targetxvector,targetyvector,alignment)


    currentboid[0]+=currentboid[2]
    currentboid[1]+=currentboid[3]
initBoids()

#(item for sublist in [[i[0],i[1]] for i in boids] for item in sublist)

@window.event
def on_draw():
    window.clear()
    drawboid = [shapes.Circle(x = i[0], y = i[1], radius = 2, color=(255, 0, 0), batch=batch) for i in boids]
    batch.draw()

    
def update(dt):

    for i in boids:
        updateb(i)
    
clock.schedule_interval(update, 1/60.0)
pyglet.app.run()