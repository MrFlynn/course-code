# Asynchronous Python Application Demo
This application serves as a test for a larger application written for another
project. This application generally mirrors the functionality of the app
written for the other project, just without any of the features. The point of
this demo was to explore the feasibility of an application that has several
workers that sleep for long periods, but needs concurrency when those workers
are running. Additionally, this application was to test the ability to safely
shutdown the application during sleep or when the workers are running.
