# Assignment 3

This is our solution for Assignment 3 of SoCo at UZH HS 2023.  
https://github.com/C0DECYCLE/PySignment.git

### Exercise 1: Unit Testing
#### General
To insure easy usage of the tests, the tests can be run while beeing in the exercise 1 directory and using the command "pytest".
This was done by this code: "sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../vm/")", which is in relative instead of
accessing a folder through concrete path. This allows every user to easily run the tests.

Use "pytest -v" to get more details of the specific tests themselves.

To see the test coverage, enter "coverage run -m pytest @CODECYCLE RIGHT COMMAND?".

#### 1A Test Assembler
Five simple assembly programs are written to test all the operations. The tests contain the expected output, which was calculated by hand. The test work via file comparison.
Instead of opening a new File for each test the tests the expected output gets written to a shared temporary file in the setup in the assert the contents are compared and in the end the temporary file gets emptied so it can be used for the next test. 
The file creation seems obsolete (which it is), because the test could read the output file and then compare the strings, but we wanted to play around with fixtures, file comparison, setup and teardown.
The translated files get saved to the mx_files directory for exercise 1B

#### 1B Test Virtual Machine
The five produced .mx files get tested with the vm, where the output gets compared to the before, by hand calculated result.
The command "capsys.readouterr().out" to get the terminal output for further comparison. This makes setup and teardown redundant for these tests, improving 
scalability and performance.


#### 1C Test VM Error
@C0DECYCLE

#### 1D Test Coverage
@?

### Exercise 2: Disassembler
@C0DECYCLE

### Exercise 3: New features and Problems - Assembler
#### 3.1 Increment and Decrement
A simple implementation, where the command just had to be added to the architecture, assembler and vm.
Just simply increase or decrease the current value by 1.

#### 3.2 Swap values
Same as in 3.1, a simple where the command just had to be added to the architecture, assembler and vm.
Just simply swap the values of the two registers.

#### 3.3 Reverse array in place
To make the reverse array file easier to read, many comments were added, explaining what different registers represent.
The reversing of the array was accomplished through the following steps:
1. Add length of array.
2. Add numbers to array.
3. "Pointer" at start and end of array.
4. Loop through array, where numbers gets swapped at "pointers".
5. End loop if pointers same index or right < left

Step 5 for uneven array was easier to implement, as one can just subtract right from left, stopping the loop if 0.
For uneven there had to be an extra check before, where if right - left + 1 results in zero, the loop would need to stop.
For this the "loopend" was created.

At all times in the code, two registers had to be "free", as they were needed to swap the values of the array.
These registers were denoted in the code with "temp".

### Exercise 4: Debugger
#### 4.1 Show Memory range
To be able to take multiple arguments a new attribute «multihandlers» is created. 
All the commands contained in this array can take multiple arguments. This makes it easier to later add more multihandlers.

The ensure_length_interact makes sure that the user inputs the right number of arguments. If they fail to do so, the VM doesn’t crash. 
They stay in the interactive shell and get a message on what they did wrong.

The memory command now takes up to two arguments. The Interact method in the vm_extend.py converts the arguments to a list. 
The args that get passed to the handler are None if no argument is passed or a list of arguments (makes it easier to check if args are given). 
Top and bottom are either set to 0 and max if no arguments are given, args[0] and args[0] + 1 if 1 argument is given oder arg[0] and arg[1] if  2 args are given.

This can be tested by running the VM and typing “m M1 M2” in the interactive shell. M1 and M2 are to be written in decimal format. 
The registers are always shown and right below them the range of memory requested will be displayed.

#### 4.2 Breakpoint Addresses
Due to the multihandler attribute this is quickly implemented. 
Just add them to the list and the arguments will be passed to the handlers. 
The address will either be the current IP if there is no argument else the requested memory position. 

This can be tested by running the VM “b M1” in the interactive shell. M1 is to be written in decimal format. 

#### 4.3 Command Completion
The command finder method in the vm_extend.py file intercepts the input, checks if some command starts with the written text and returns the corresponding command or none if there is no such command.

This can be tried by typing the beginning of the available commands in the interactive shell. E.g. br or bre for break.

#### 4.4 Watchpoints
The watchpoints are only important in the str operation since this is the only operation where information gets stored into the RAM. 
The wap operation gets added to the OPS in the architecture.py file. Like with break a new dictionary “watch” is added to the attributes to store the information at the memory of the watch point. 
The “wap” operation code gets substituted in that memory location. If the str operation wants to store something at a location where a Watchpoint sits, the VM goes into stepping mode, displays what memory gets changed and interact with the user. 

To try this run the vm_break.py with the watch.mx file. The watch.mx file stores memory to the RAM at addresses from 31 to 36.
Type “w M1” command in the interactive shell to watch the memory address at M1. M1 is to be written in decimal format. E.g. w 33. 



