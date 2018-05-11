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


FORWARD = 1
BACKWARD = -1
HALF_STEP = 1
FULL_STEP = 2


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
		self.step_direction = FORWARD
		self.step_speed = HALF_STEP
		self.steps_counter = 0

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
		print(self.step_speed)
		if self.step_speed == FULL_STEP:
			if (self.steps_counter % 8) % 2 != 0:
				self.steps_counter += 1
		counter = 0
		while counter < steps and counter > -steps:
			for pin in range(0, 4):
				if self.sequence[self.steps_counter % 8][pin] != 0:
					self.pi.write(self.step_pins[pin], True)
				else:
					self.pi.write(self.step_pins[pin], False)
			time.sleep(0.001)
			self.steps_counter += self.step_direction * self.step_speed
			counter += self.step_direction


	def _set_speed(self, func_dictionary):
		"""Sets motor speed according dictionary value obtained from kwargs of calling method

		"""
		if 'speed' in func_dictionary:
			self.step_speed = func_dictionary['speed']
			print("siemka")
		else:
			self.step_speed = HALF_STEP


	def move_forward_for_angle(self, angle, **kwargs):
		""" Turns motor forward for given angle

		Args:
			angle (int): angle in degrees

		"""
		self._set_speed(kwargs)
		self.step_direction = FORWARD
		self._move(self._calculate_steps(angle))


	def move_backward_for_angle(self, angle, **kwargs):
		""" Turns motor backward for given angle

		Args:
			angle (int): angle in degrees

		"""
		self._set_speed(kwargs)
		self.step_direction = BACKWARD
		self._move(self._calculate_steps(angle))


	def move_forward(self, steps, **kwargs):
		""" Turns motor forward for given steps

		Args:
			steps (int): number of steps

		"""
		self._set_speed(kwargs)
		self.step_direction = FORWARD
		self._move(steps)


	def move_backward(self, steps, **kwargs):
		""" Turns motor backward for given steps

		Args:
			steps (int): number of steps

		"""
		self._set_speed(kwargs)
		self.step_direction = BACKWARD
		self._move(steps)



if __name__ == "__main__":
	sm = StepMotor(12, 16, 20, 21)
	sm.move_forward(4076, speed=FULL_STEP)
	print("------------------")
	sm.move_backward(4076, speed=FULL_STEP)
	print("------------------")
	sm.move_forward_for_angle(360)
	print("------------------")
	sm.move_backward_for_angle(360, speed=FULL_STEP)
