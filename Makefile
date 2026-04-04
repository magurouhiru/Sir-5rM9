image: image_bot image_ocr

image_bot:
	docker build -t sir_5rm9_bot:latest -f bot.Dockerfile .

image_ocr:
	docker build -t sir_5rm9_ocr:latest -f ocr.Dockerfile .
