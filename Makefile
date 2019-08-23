clean:
	find . -type d -name __pycache__ -exec rm -r {} \+

build:
	docker build -t vending-machine:latest .
	docker build -t vending-machine-test:latest -f Dockerfile.test .

run:
	docker run -it --rm vending-machine

test:
	docker run --rm vending-machine-test python -m pytest