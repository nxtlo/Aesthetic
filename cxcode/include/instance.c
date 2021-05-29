#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "instance.h"

void set_details(char *name, int date, Some id) {
    Visitor *self;
    self -> date = date;
    self -> id = id;
    strcpy_s(self -> name, 4, name);
}

void get_details() {
    Visitor v;
    set_details("Fate", 2020, 33);
    printf("Name: %s ID: %i Date: %i", v.name, v.id, v.date);
}