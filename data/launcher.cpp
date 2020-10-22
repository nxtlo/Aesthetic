// note! this file is for testing only

#include <iostream>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

int main() {
    int res = system("/launcher.py");
    if(res != 0){
        cout << "Exit code:" << res << "/n";
    }
}