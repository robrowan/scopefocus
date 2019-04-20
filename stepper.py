
import sys
import time
import RPi.GPIO as GPIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--steps', '-s', help="Number of steps to execute", type= int, default= 4096)
parser.add_argument('--direction', '-d', help="Direction: 1=CW slow, 2=CW fast, -1=CCW slow, -2=CCW fast", type= int, default= 1)
parser.add_argument('--wait', '-w', help="Wait time in ms between steps", type= int, default= 5)
args = parser.parse_args()

# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [17,22,23,24]

# Set all pins as output
for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
       
StepCount = len(Seq)
StepDir = args.direction

# Read wait time from command line
WaitTime = int(args.wait)/float(1000)

# Initialise variables
StepCounter = 0
RemainingSteps = args.steps

# Start main loop
while (RemainingSteps > 0):

  for pin in range(0, 4):
    xpin = StepPins[pin]
    if Seq[StepCounter][pin]!=0:
      GPIO.output(xpin, True)
    else:
      GPIO.output(xpin, False)

  StepCounter += StepDir
  RemainingSteps -= 1

  # If we reach the end of the sequence
  # start again
  if (StepCounter>=StepCount):
    StepCounter = 0
  if (StepCounter<0):
    StepCounter = StepCount+StepDir

  # Wait before moving on
  time.sleep(WaitTime)

GPIO.cleanup()
