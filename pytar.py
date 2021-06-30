#!/usr/bin/env python3
'''

  PYTAR (aka: PYthon-guiTAR)
------------------------------
  Creds:
    Liz Pringi <epringi@gmail.com>
    Mike Mallett <mike@nerdcore.net>

  This script takes the Guitar Hero guitar and makes it into a multi-purpose
  keytar instrument.  This could potentially be compatible with other 'guitar'
  devices, but current compatibility is only verified for RedOctane Guitar Hero X-plorer.

---  Detected inputs:
guitar.get_axis(x)
  axis 3: whammy bar
  axis 2: twist excellerometer
  axis 4: up-down excellerometer
  axis 5: ??

guitar.get_button(x)
  button 0: green
  button 1: red
  button 2: blue
  button 3: yellow
  button 4: orange
  button 6: back
  button 7: start
  button 8: x-button

guitar.get_hat(x)
  hat 0: numpad + strum (strum only uses value[1])


'''

import pygame
import signal


#-- INIT

# Exit gracefully if SIGINT
def signal_handler(sig, frame):
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# init joystick for guitar input and pygame for event handling of said guitar
pygame.init()
pygame.joystick.init()
pygame.mixer.init()

# Get all the joysticks detected
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# We only want the guitar hero joystick (for now)
for joy in joysticks:
  if joy.get_name().find("Guitar")>=0:
    guitar=joy

# if we didn't find a guitar, then GTFO
if 'guitar' not in locals():
  print("No Guitar Hero device found")
  exit()
else:
  print("Found a Guitar Hero device: ", guitar.get_name(), " - ", guitar.get_guid())


#-- GLOBALS

# For some nice output
class colours:
  red    = '\033[91m'
  blue   = '\033[94m'
  green  = '\033[92m'
  yellow = '\033[93m'
  orange = '\033[95m'
  white  = '\033[1m'
  off    = '\033[0m'

# some human readable values
WHAMMY = 3
GREEN = 0
RED = 1
BLUE = 2
YELLOW = 3
ORANGE = 4
BACK = 6
START = 7
XBUTTON = 8
UP = 1
DOWN = -1

# contains two modes: guitar and sampler
sounds = {
  'guitar': [
    # bass guitar [0]
    {
      # strum down
      UP: {
        'green': pygame.mixer.Sound("samples/bass/bassE.wav"),
        'red': pygame.mixer.Sound("samples/bass/bassA.wav"),
        'yellow': pygame.mixer.Sound("samples/bass/bassD.wav"),
        'blue': pygame.mixer.Sound("samples/bass/bassG.wav"),
        'orange': pygame.mixer.Sound("samples/bass/bassB.wav")
      },
      # strum up
      DOWN: {
        'green': pygame.mixer.Sound("samples/bass/bassA.wav"),
        'red': pygame.mixer.Sound("samples/bass/bassD.wav"),
        'yellow': pygame.mixer.Sound("samples/bass/bassG.wav"),
        'blue': pygame.mixer.Sound("samples/bass/bassB.wav"),
        'orange': pygame.mixer.Sound("samples/bass/bassE.wav"),
      }
    },
    # 6 string guitar [1]
    {
      # strum down
      UP: {
        'green': pygame.mixer.Sound("samples/bass/bassG.wav"),
        'red': pygame.mixer.Sound("samples/bass/bassB.wav"),
        'yellow': pygame.mixer.Sound("samples/bass/bassE.wav"),
        'blue': pygame.mixer.Sound("samples/bass/bassA.wav"),
        'orange': pygame.mixer.Sound("samples/bass/bassD.wav"),
      },
      # strum up
      DOWN: {
        'green': pygame.mixer.Sound("samples/bass/bassB.wav"),
        'red': pygame.mixer.Sound("samples/bass/bassE.wav"),
        'yellow': pygame.mixer.Sound("samples/bass/bassA.wav"),
        'blue': pygame.mixer.Sound("samples/bass/bassD.wav"),
        'orange': pygame.mixer.Sound("samples/bass/bassG.wav"),
      }
    }
  ],
  'sampler': []
}

# Mode "guitar" or "sampler"
mode = "guitar"

# toggle value changed with back and start buttons
toggle = 0

# State and sound info for the buttons
buttons = {
  'green': {
    'state': False,
    #'value': colours.green + "green" + colours.off
    #'sound': { 1: sounds['enote'], -1: sounds['bnote'] }
    'sound': {}
  },
  'red': {
    'state': False,
    #'value': colours.red + "red" + colours.off
    #'sound': { 1: sounds['anote'], -1: sounds['enote'] }
    'sound': {}
  },
  'yellow': {
    'state': False,
    #'value': colours.yellow + "yellow" + colours.off
    #'sound': { 1: sounds['dnote'], -1: sounds['anote'] }
    'sound': {}
  },
  'blue': {
    'state': False,
    #'value': colours.blue + "blue" + colours.off
    #'sound': { 1: sounds['gnote'], -1: sounds['dnote'] }
    'sound': {}
  },
  'orange': {
    'state': False,
    #'value': colours.orange + "orange" + colours.off
    #'sound': { 1: sounds['bnote'], -1: sounds['gnote'] }
    'sound': {}
  }
}


#-- MEAT

# set the sounds for the buttons
def set_sounds():
  if mode == "guitar":
    for button, values in buttons.items():
      values['sound'][UP]=sounds['guitar'][toggle][UP][button]
      values['sound'][DOWN]=sounds['guitar'][toggle][DOWN][button]

# initialise the sounds for the buttons
set_sounds()

while True:
  for e in pygame.event.get():

    # Detect depressed buttons :'(
    if e.type == pygame.JOYBUTTONUP and e.button == GREEN:
      buttons['green']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == GREEN:
      buttons['green']['state'] = True
      #print(colours.green + "green note active" + colours.off)

    if e.type == pygame.JOYBUTTONUP and e.button == RED:
      buttons['red']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == RED:
      buttons['red']['state'] = True
      #print(colours.red + "red note active" + colours.off)

    if e.type == pygame.JOYBUTTONUP and e.button == YELLOW:
      buttons['yellow']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == YELLOW:
      buttons['yellow']['state'] = True
      #print(colours.yellow + "yellow note active" + colours.off)

    if e.type == pygame.JOYBUTTONUP and e.button == BLUE:
      buttons['blue']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == BLUE:
      buttons['blue']['state'] = True
      #print(colours.blue + "blue note active" + colours.off)

    if e.type == pygame.JOYBUTTONUP and e.button == ORANGE:
      buttons['orange']['state'] = False
    if e.type == pygame.JOYBUTTONDOWN and e.button == ORANGE:
      buttons['orange']['state'] = True
      #print(colours.orange + "orange note active" + colours.off)

    '''if e.type == pygame.JOYAXISMOTION and e.axis == 3 and e.value < -1.000030518509476:
      buttons['whammy']['state'] = False
    if e.type == pygame.JOYAXISMOTION and e.axis == 3 and e.value > -1.000030518509476:
      buttons['whammy']['state'] = True
      #print(colours.white + "Whammy - alter noise" + colours.off + str(e.value))'''

    # toggle the toggle if the toggle is toggled :|
    if e.type == pygame.JOYBUTTONDOWN and (e.button == BACK or e.button == START):
      toggle ^= 1
      set_sounds()

    # Strum action
    strum_direction = UP

    if e.type == pygame.JOYHATMOTION and e.value[1] != 0 and mode == 'guitar':
      strum_direction = e.value[1]

      # play all the sounds
      for input, attr in buttons.items():
        if attr['state'] == True:
          attr['sound'][UP].stop()
          attr['sound'][DOWN].stop()
          attr['sound'][strum_direction].play()
          #attr['value'].stop()
          #attr['value'].play()
          fadeout = int((guitar.get_axis(3)+1)*1500)
          if fadeout > 0:
            attr['sound'][strum_direction].fadeout(3250-fadeout)

    if e.type == pygame.JOYBUTTONDOWN and e.button == XBUTTON:
      exit()
