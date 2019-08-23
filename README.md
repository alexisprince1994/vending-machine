# vending-machine
Vending machine CLI app. To avoid pollution of the host computer,
and to ensure everything works as expected, this app should be run
inside of a container.

# Instructions
To build the docker image used, run:
`make build`

To run the test suite, run:
`make test`

# Getting started
To get started, run:
`make run`

To see all available commands once inside the container, run:
`python -m vending_machine --help`

All subsequent commands should be issued in the format of:
`python -m vending_machine COMMAND`
