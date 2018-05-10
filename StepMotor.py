import pigpio

class StepMotor:
	def __init__(self, **kwargs):
		if "pi" in kwargs and "port" in kwargs:
			self.pi = pigpio.pi(kwargs['pi'], kwargs['port'])
		else:
			self.pi = pigpio.pi()

if __name__ == "__main__":
	print("Hello main")

