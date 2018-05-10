import pigpio
import time

FORWARD = 2
BACKWARD = -1

class StepMotor:
	def __init__(self, out1, out2, out3, out4, **kwargs):
		if "pi" in kwargs and "port" in kwargs:
			self.pi = pigpio.pi(kwargs['pi'], kwargs['port'])
		else:
			self.pi = pigpio.pi()

		self.step_pins = [out1, out2, out3, out4]
		for pin in self.step_pins:
			self.pi.set_mode(pin, pigpio.OUTPUT)

		self.sequence = [[1, 0, 0, 1],
				 [1, 0, 0, 0],
				 [1, 1, 0, 0],
				 [0, 1, 0, 0],
				 [0, 1, 1, 0],
				 [0, 0, 1, 0],
				 [0, 0, 1, 1],
				 [0, 0, 0, 1],]
		self.step_count = len(self.sequence)
		self.direction = FORWARD

	def forward(self, steps):
		for i in range(0, steps * 2):
			for pin in range(0, 4):
				if self.sequence[i % 8][pin] != 0:
					self.pi.write(self.step_pins[pin], True)
				else:
					self.pi.write(self.step_pins[pin], False)
			time.sleep(0.001)


if __name__ == "__main__":
	print("Hello main")
	sm = StepMotor(12, 16, 20, 21)
	sm.forward(4076)
