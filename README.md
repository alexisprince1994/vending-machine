# vending-machine
Vending machine CLI app. To avoid pollution of the host computer,
and to ensure everything works as expected, this app should be run
inside of a container.

# Instructions
To build the docker image used, run:
`make build`

To run the test suite, run:
`make test`

# Basic Operations
To get started, run:
`make run`

To see all available commands once inside the container, run:
`python -m vending_machine --help`

All subsequent commands should be issued in the format of: `python -m vending_machine COMMAND`.
For example, if you run `python -m vending_machine --help`, you'd see:
```
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

  A simple command line tool

Options:
  --help  Show this message and exit.

Commands:
  add-money        Adding money to the existing vending machine.
  destroy          Destroys the state of the vending machine without...
  dispense-change  Removing the money from the existing vending machine.
  rebuild          Destroys the vending machine (if exists) and rebuilds...
  start            Initiates the state of the vending machine.
  view-balance     Views the current balance you have in the machine.
  view-items       Viewing what items are in the machine.
  view-purchases   Views all purchases.
  ```
  Each command against the machine is outfitted a help command, that you can access with
  `python -m vending_machine COMMAND --help`, for a more in depth help message like this:
  ```
  Usage: __main__.py add-money [OPTIONS] AMOUNT

  Adding money to the existing vending machine. If no machine exists, error
  is thrown.

Options:
  --help  Show this message and exit.
  ``` 

# Getting Started
To get started using the vending machine, you're going to first initiate
the machine, as most other interactions will fail without it.
Running `python -m vending_machine start` will yield a success like message like `SUCCESS: Vending machine created.`.

Once you have a vending machine, you have several different options, like adding money, 
viewing items, purchasing items, and viewing past purchases.

When you're done using the vending machine, you can either `destroy` the machine right away,
or you can `dispense-change` first to get your hard earned money back, then `destroy` it.
If you're just looking to reset your machine, try `rebuild`.