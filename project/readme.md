# COE817 Network Security Project

The purpose of this project is to design and implement network security protocols for a banking system consisting of a bank server and three ATM client machines. The server establishes a socket listening for connectoin requrests from ATM clients. For each request from an ATM client, the server creates a new thread that will authenticate the user of the ATM and process that user's transactions.

In this project, customers use ATM client machines to deposit, withdrawals, and balance inquiries fromm their accounts in the bank server.. A client needs to register a new account on the server with their username and password. Customers then interact with the ATM client and work as below:

1. The ATM client promps the customer for username and a password which the customer enters at the ATM client for logging in.
2. ATM client communicates with the bank by running an authenticated key distribution protocol (ASsume client and server already have a shared key. The protocol will provide a second layer symmetric key based authentication) that satisfies the following requirements:
- It authenticates the customer to the bank server.
- It authenticates the bank server to the ATM.
- A new symmetric key called Master Secret is created and shared by ATM and the bank server.



# References
