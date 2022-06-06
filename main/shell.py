import main

while True:
	text = input('>>> ')
	if text.strip() == "": continue
	result, error = main.run('<stdin>', text)

	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			pass
		else:
			print(repr(result))
