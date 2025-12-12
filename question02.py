def main():
	sentence = input("Enter a sentence: ")
	num_characters = len(sentence)
	words = sentence.split()
	num_words = len(words)
	vowels = set("aeiouAEIOU")
	num_vowels = 0
	for ch in sentence:
		if ch in vowels:
			num_vowels += 1

	print("Number of characters:", num_characters)
	print("Number of words:", num_words)
	print("Number of vowels:", num_vowels)


if __name__ == "__main__":
	main()