# Коровы, козы, овцы, свиньи
# Утки, куры, гуси

class Animal:
	def __init__(self, weight, feed_per_kilo, voice):
		self.weight = weight
		self.feed_per_kilo = feed_per_kilo
		self.voice = voice

	def get_feed(self):
		return round(self.weight * self.feed_per_kilo, 2)

	def get_voice(self):
		print(self.voice, "!")


class Cattle(Animal):
	def __init__(self, weight, feed_per_kilo, voice, legs=4, food="grass"):
		super().__init__(weight, feed_per_kilo, voice)
		self.legs = legs
		self.food = food


class Bird(Animal):
	def __init__(self, weight, feed_per_kilo, voice, legs=2, food="grain"):
		super().__init__(weight, feed_per_kilo, voice)
		self.legs = legs
		self.food = food


class Pig(Cattle):
	def __init__(self, weight, voice="wiii", feed_per_kilo=1):
		super().__init__(weight, feed_per_kilo, voice)


class Sheep(Cattle):
	def __init__(self, weight, voice="beee", feed_per_kilo=0.1):
		super().__init__(weight, feed_per_kilo, voice)


class Goat(Cattle):
	def __init__(self, weight, voice="mee", feed_per_kilo=0.2):
		super().__init__(weight, feed_per_kilo, voice)


class Cow(Cattle):
	def __init__(self, weight, voice="muu", feed_per_kilo=0.7):
		super().__init__(weight, feed_per_kilo, voice)


class Duck(Bird):
	def __init__(self, weight, voice="quack", feed_per_kilo=0.2):
		super().__init__(weight, feed_per_kilo, voice)
		self.voice = voice


class Chicken(Bird):
	def __init__(self, weight, voice="kwok", feed_per_kilo=0.1):
		super().__init__(weight, feed_per_kilo, voice)


class Goose(Bird):
	def __init__(self, weight, voice="shhh", feed_per_kilo=0.3):
		super().__init__(weight, feed_per_kilo, voice)


pig1 = Pig(5)
print(pig1.get_feed(), "kilo", pig1.food)
pig1.get_feed()
pig1.get_voice()

duck1 = Duck(1)
print(duck1.get_feed(), "kilo", duck1.food)
duck1.get_voice()