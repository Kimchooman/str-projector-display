from cam import *
from fish import *
import threading
import time

camera = camera()
fish_screen = fish_screen()

end_time = 15 * 60 * 60 # Ends the program at 15:00 (3:00 pm)

class alarm:
	def __init__(self,start, time):
		self.start = start
		self.end = start + time

	def check(self):
		if int(time.time()) >= self.end: return True
		
		else: return False

class compile:
    def __init__(self):
        self.alarm = None

    def session(self):

        while True:

            time.sleep(0.03)

            if self.alarm is None:
                t1 = threading.Thread(target=fish_screen.update_AVOID_POINTS, args=(camera.snap(),))
                t1.start()

                self.alarm = alarm(int(time.time()), 5)

            elif self.alarm is not None:
                if t1.isAlive() is False: t1.join()

                if self.alarm.check(): self.alarm = None   

            fish_screen.update()

            if int(time.time()) is end_time: 
                camera.end_session()
                break

run = compile()

run.session()
