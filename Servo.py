"""
This module is handler for servomotors.
Contains class: Servo which can be used for controlling servos.

Module was tested with SG90 MicroServo.

Example:
	You can test this class by running module.
	By default it uses GPIO PIN 14 to control servo.
	Servo should do moves do left and right five times.
	After that servo should back to default position.

	$ python Servo.py

Atributes:
	DEFAULT_POSITION (int): Value representing default position of servo.
	MINIMAL_POSITION (int): Value representing maximum left position of servo.
	MAXIMAL_POSITION (int): Value representing maximum right position of servo.

"""

import pigpio, time


DEFAULT_POSITION = 1170
MINIMAL_POSITION = 500
MAXIMAL_POSITION = 2500


class Servo:
	"""Controls servo"""

	def __init__(self, servo_pin, **kwargs):
		""" Method creates appropriate connection with Raspberry Pi,
		   sets GPIO pin for control servo and sets it to default position.

		Args:
			servo_pin (int): servo control PIN.
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

		self.servo_pin = servo_pin
		self.servo_position = 1170

		self.pi.set_servo_pulsewidth(self.servo_pin, self.servo_position)


	def move_to_position(self, position):
		""" Sets servo position to given value

		Given position should be from range: 500, 2500.
		Values out of this range can cause errors.

		Args:
			position (int): Servo position from range 500 to 2500.

		"""
		self.servo_position = position
		self.pi.set_servo_pulsewidth(self.servo_pin, self.servo_position)


	def move_to_default(self):
		""" Sets servo position to default position """

		self.move_to_position(DEFAULT_POSITION)


	def move_left(self, distance=0):
		""" Moves servo to left.

		Args:
			distance (int): How far to left servo should move.

		"""
		if distance == 0 or distance < 0:
			pass

		position = self.servo_position - distance
		if position < MINIMAL_POSITION:
			position = MINIMAL_POSITION

		self.move_to_position(position)


	def move_right(self, distance=0):
		""" Moves servo to right.

		Args:
			distance (int): How far to right servo should move.

		"""
		if distance == 0 or distance < 0:
			pass

		position = self.servo_position + distance
		if position > MAXIMAL_POSITION:
			position = MAXIMAL_POSITION

		self.move_to_position(position)


	def turn_off(self):
		""" Turns off servo.

		It is done by setting servo position to 0.

		"""
		self.pi.set_servo_pulsewidth(self.servo_pin, 0)


if __name__ == "__main__":
	s = Servo(14)
	for i in range(0, 5):
		s.move_to_position(500)
		time.sleep(1)
		s.move_to_position(2500)
		time.sleep(1)
	s.move_to_default()
	s.turn_off()
