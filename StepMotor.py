"""
This module is handler for 28BJY-48 stepper motor with ULN2003 driverself.
Contains class: StepMotor which can be used for controlling motor.

28BJY-48 motor needs 4076 steps for full revolution in half-step mode.

Example:
	You can test this class by running module.
	It uses 12, 16, 20, 21 GPIO PINS to control driver.
	Steppper motor should do one full revolution.

		$ python StepMotor.py

Atributes:
	FORWARD (int):	Represents direction of stepper motor movement.
	BACKWARD (int): Represents direction of stepper motor movement.

Todo:
	* Full-step mode handling
"""

import pigpio
import time

FORWARD = 2 	#can be 1 or 2
BACKWARD = -1	#can be -1 or -2

class StepMotor:
	"""Controls stepper motor"""

	def __init__(self, out1, out2, out3, out4, **kwargs):
		"""Method initializes needed arrays and creates connection
		   with appropriate Raspberry Pi through pigpio.

		Args:
			out1 (int): First stepper motor driver PIN.
			out2 (int): Second stepper motor driver PIN.
			out3 (int): Third stepper motor driver PIN.
			out4 (int): Fourth stteper motor driver PIN.
			**kwargs: pi, port
				pi (string): IP address of used Raspberry Pi.
				 	If not given, Raspberry Pi which is running script is used.
				port (int): IP port of used Raspberry Pi.
				 	If not given, Raspberry Pi which is running script is used.

		"""
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


	def _calculate_steps(self, angle):
		""" Private method used for calculate number of steps
			according to given steps.

		Args:
			angle (int): Angle in degrees.

		Returns:
			int: Number of steps.

		"""
		steps = int(4076 * (angle / 360))
		print(steps)
		return steps


	def _move(self, steps):
		"""	Private method which handles motor movement by communicating with driver.
		Methods sends proper signals to driver which performs steps in stepper motor.

		Args:
			steps (int): Number of steps to perform.

		"""
		for i in range(0, steps):
			for pin in range(0, 4):
				if self.sequence[i % 8][pin] != 0:
					self.pi.write(self.step_pins[pin], True)
				else:
					self.pi.write(self.step_pins[pin], False)
			time.sleep(0.001)


	def move_forward_for_angle(self, angle):
		""" Turns motor forward for given angle

		Args:
			angle (int): angle in degrees

		"""
		self.move_forward(self._calculate_steps(angle))


	def move_backward_for_angle(self, angle):
		""" Turns motor backward for given angle

		Args:
			angle (int): angle in degrees

		"""
		self.move_backward(self._calculate_steps(angle))


	def move_forward(self, steps):
		""" Turns motor forward for given steps

		Args:
			steps (int): number of steps

		"""
		self.direction = FORWARD
		self._move(steps)


	def move_backward(self, steps):
		""" Turns motor backward for given steps

		Args:
			steps (int): number of steps

		"""
		self.direction = BACKWARD
		self._move(steps)



if __name__ == "__main__":
	sm = StepMotor(12, 16, 20, 21)
	sm.move_forward(4076)
	sm.move_backward(4076)
	sm.move_forward_for_angle(360)
	sm.move_backward_for_angle(360)
