# Thread Scheduling Experiment

This folder contains a program which demonstrates the non-deterministic nature
of thread schedulers. This program outputs all the possible values of some 
variable `count` when threads don't use synchronization or mutexes to prevent
this non-deterministic behavior. An additional example is included that shows 
the behavior when the loop index is also shared between threads.

This script emulates the following C program.
```c
#include <stdio.h> 
#include <pthread.h> 

int count = 0;

void *foo() {
  int i = 0;
  for (; i < 2; i++) {
    count = count * count;
  }
}

void *bar() {
  int i = 0;
  for (; i < 2; i++) {
    count = count - 1;
  }
}

int main() {
  pthread_t thread_id;

  pthread_create(&thread_id, NULL, foo, NULL);
  pthread_create(&thread_id, NULL, bar, NULL);
  pthread_exit(NULL);

  printf("%d", count);

  return 0;
}
```
