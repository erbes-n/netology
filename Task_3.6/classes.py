# Коровы, козы, овцы, свиньи
# Утки, куры, гуси


class Animal:

	def __init__(self, weight):
		self.weight = weight

	def get_feed(self, weight, feed_per_kilo):
		return round(weight * feed_per_kilo, 2)

	def get_voice(self, voice):
		print(voice, "!")


class Cattle(Animal):
	legs = 4
	food = "grass"


class Bird(Animal):
	legs = 2
	food = "grain"


class Pig(Cattle):
	voice = "wiii"
	feed_per_kilo = 1

	def get_feed(self):
		return super().get_feed(self.weight, self.feed_per_kilo)

	def get_voice(self):
		super().get_voice(self.voice)


class Sheep(Cattle):
	voice = "beee"
	feed_per_kilo = 0.1

	def get_feed(self):
		return super().get_feed(self.weight, self.feed_per_kilo)

	def get_voice(self):
		super().get_voice(self.voice)


class Goat(Cattle):
	voice = "mee"
	feed_per_kilo = 0.2

	def get_feed(self):
		return super().get_feed(self.weight, self.feed_per_kilo)

	def get_voice(self):
		super().get_voice(self.voice)


class Cow(Cattle):
	voice = "muu"
	feed_per_kilo = 0.7

	def get_feed(self):
		return super().get_feed(self.weight, self.feed_per_kilo)

	def get_voice(self):
		super().get_voice(self.voice)


class Duck(Bird):
	voice = "quack"
	feed_per_kilo = 0.2

	def get_feed(self):
		return super().get_feed(self.weight, self.feed_per_kilo)

	def get_voice(self):
		super().get_voice(self.voice)


class Chicken(Bird):
	voice = "kwok"
	feed_per_kilo = 0.1

	def get_feed(self):
		return super().get_feed(self.weight, self.feed_per_kilo)

	def get_voice(self):
		super().get_voice(self.voice)


class Goose(Bird):
	voice = "shhh"
	feed_per_kilo = 0.3

	def get_feed(self):
		return super().get_feed(self.weight, self.feed_per_kilo)

	def get_voice(self):
		super().get_voice(self.voice)


pig1 = Pig(5)
print(pig1.get_feed(), "kilo", pig1.food)
pig1.get_voice()

duck1 = Duck(1)
print(duck1.get_feed(), "kilo", duck1.food)
duck1.get_voice()
