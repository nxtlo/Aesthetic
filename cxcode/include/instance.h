typedef unsigned int Some;

typedef struct Visitor {
    char *name;
    Some id;
    int date;
} Visitor;

void set_details(char *name, int date, Some id);

void get_details();