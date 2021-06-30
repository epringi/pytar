#!/usr/bin/env python3

import pygame
import signal

# Exit gracefully if SIGINT
def signal_handler(sig, frame):
    exit(0)

signal.signal(signal.SIGINT, signal_handler)


class colours:
  red    = '\033[91m'
  blue   = '\033[94m'
  green  = '\033[92m'
  yellow = '\033[93m'
  orange = '\033[95m'
  white  = '\033[1m'
  off    = '\033[0m'


# init joystick for guitar input and pygame for event handling of said guitar
pygame.init()
pygame.joystick.init()
pygame.mixer.init()

'''thick=mixer.Sound(file)
def fo(s, t):
  s.play()
  s.fadeout(t)

fo(thick, 250)
fo(thick, 750)
fo(thick) 2000)

mixer.music.load(file)
mixer.music.play(4)
mixer.music.queue(file)
mixer.music.play(4)'''

sounds = {
  enote = "enote.wav",
  anote = "anote.wav",
  dnote = "dnote.wav",
  gnote = "gnote.wav",
  bnote = "bnote.wav"
}



# Get all the joysticks detected
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# we only want the guitar hero joystick
for joy in joysticks:
  if joy.get_name().find("Guitar")>=0:
    guitar=joy

# if we didn't find a guitar, then GTFO
if 'guitar' not in locals():
  print("No Guitar Hero device found")
  exit()
else:
  print("Found a Guitar Hero device: ", guitar.get_name(), " - ", guitar.get_guid())

'''  ---  Inputs and Locations
guitar.get_axis(x)
  3: whammy bar
  2: twist excellerometer
  4: up-down excellerometer
  5: ??

guitar.get_button(x)
  0: green
  1: red
  2: blue
  3: yellow
  4: orange
  6: back
  7: start
  8: x-button

guitar.get_hat(x)
  0: numpad + strum (strum only uses value[1])
'''

# State and sound info for the inputs
inputs = {
  'red': {
    'state': False,
    'value': colours.red + "red" + colours.off
  },
  'blue': {
    'state': False,
    'value': colours.blue + "blue" + colours.off
  },
  'yellow': {
    'state': False,
    'value': colours.yellow + "yellow" + colours.off
  },
  'orange': {
    'state': False,
    'value': colours.orange + "orange" + colours.off
  },
  'green': {
    'state': False,
    'value': colours.green + "green" + colours.off
  },
  'whammy': {
    'state': False,
    'value': colours.white + "Whammy" + colours.off
  }
}

while True:
  for e in pygame.event.get():
    if e.type == pygame.JOYBUTTONUP and e.button == 0:
      inputs['green']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == 0:
      inputs['green']['state'] = True
      #print(colours.green + "green note active" + colours.off)

    if e.type == pygame.JOYBUTTONUP and e.button == 1:
      inputs['red']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == 1:
      inputs['red']['state'] = True
      #print(colours.red + "red note active" + colours.off)

    if e.type == pygame.JOYBUTTONUP and e.button == 3:
      inputs['yellow']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == 3:
      inputs['yellow']['state'] = True
      #print(colours.yellow + "yellow note active" + colours.off)

    if e.type == pygame.JOYBUTTONUP and e.button == 2:
      inputs['blue']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == 2:
      inputs['blue']['state'] = True
      #print(colours.blue + "blue note active" + colours.off)

    if e.type == pygame.JOYBUTTONUP and e.button == 4:
      inputs['orange']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == 4:
      inputs['orange']['state'] = True
      #print(colours.orange + "orange note active" + colours.off)

    if e.type == pygame.JOYAXISMOTION and e.axis == 3 and e.value < -1.000030518509476:
      inputs['whammy']['state'] = False
    if e.type == pygame.JOYAXISMOTION and e.axis == 3 and e.value > -1.000030518509476:
      inputs['whammy']['state'] = True
      #print(colours.white + "Whammy - alter noise" + colours.off + str(e.value))

    if e.type == pygame.JOYHATMOTION and e.value[1] != 0:
      #print("strum - make noise")
      sound=""
      for input, attr in inputs.items():
        if attr['state'] == True:
          sound = sound + attr['value'] + " "
      print(sound)

    if e.type == pygame.JOYBUTTONDOWN and e.button == 8:
      exit()
    #if e.type == pygame.JOYAXISMOTION and e.axis == 4:
      #print("drama")
