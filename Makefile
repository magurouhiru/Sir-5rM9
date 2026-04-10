image: image_bot image_ocr_server

image_bot:
	docker build -t sir_5rm9_bot:latest -f bot.Dockerfile .

image_ocr_server:
	docker build -t sir_5rm9_ocr_server:latest -f ocr_server.Dockerfile .
