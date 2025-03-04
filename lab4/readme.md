# COE817 LAB 4

## Description

In this lab, we implement a socket communication program to implement a secure chat system by implementing a server (KDC) is needed for distributing session keys to three clients (A, B, and C). 

## Required Security Features
- Authenticated key distribution between KDC and chat clients
- ALL chat messages need to be encrypted using a blcok cipher such as DES or AES. A digitla signature must be appended to all chat messages.
- Solution to combat replay attacks. 

## Lab Demo

# Summary of Workflow

# Explanation of Code

Your pgroam needs to generate the message of protocol in (1) and display it. Then show TA if the same message M could be received by B and C after decryption and signature verification.

Explain your code and tell how your KDC progfram could successfully forward a message to remainin lcients. For example, if a chat messge is from AA, yourp rogram will ensure that KDC wll forward A's message to B and C only. 

Allow your TA to type in the third message on client C and see if it could be received by A and B. 

Demo your improved protocol and show how your solution could resist replay attack. 


