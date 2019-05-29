import RPi.GPIO as IO
import time
while 1:
    IO.setmode(IO.BOARD)
    IO.setup(40,IO.OUT)
    IO.output(40,1)
    time.sleep(2)
    IO.cleanup()
    time.sleep(1)


