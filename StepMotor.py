import pigpio
import time

FORWARD = 2 	#can be 1 or 2
BACKWARD = -1	#can be -1 or -2

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


	def move_forward_for_angle(self, angle):
		self.move_forward(self._calculate_steps(angle))


	def move_backward_for_angle(self, angle):
		self.backward(self._calculate_steps(angle))


	def _calculate_steps(self, angle):
		steps = int(4076 * (angle / 360))
		print(steps)
		return steps


	def move_forward(self, steps):
		'''For full revolution step motor does 4076 steps'''
		self.direction = FORWARD
		self._move(steps)


	def move_backward(self, steps):
		self.direction = BACKWARD
		self._move(steps)


	def _move(self, steps):
		for i in range(0, steps):
			for pin in range(0, 4):
				if self.sequence[i % 8][pin] != 0:
					self.pi.write(self.step_pins[pin], True)
				else:
					self.pi.write(self.step_pins[pin], False)
			time.sleep(0.001)



if __name__ == "__main__":
	sm = StepMotor(12, 16, 20, 21)
	sm.move_forward(4076)
