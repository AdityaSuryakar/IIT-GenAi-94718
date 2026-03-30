def main():
	s = input("Enter numbers (comma-separated): ")

	# Split by comma and strip whitespace; ignore empty tokens
	tokens = [tok.strip() for tok in s.split(',') if tok.strip()]

	even_count = 0
	odd_count = 0
	invalid = 0

	for tok in tokens:
		try:
			n = int(tok)
		except ValueError:
			invalid += 1
			continue

		if n % 2 == 0:
			even_count += 1
		else:
			odd_count += 1

	print("Even numbers:", even_count)
	print("Odd numbers:", odd_count)
	if invalid:
		print(f"Skipped {invalid} invalid entr{'y' if invalid==1 else 'ies'}")


if __name__ == "__main__":
	main()