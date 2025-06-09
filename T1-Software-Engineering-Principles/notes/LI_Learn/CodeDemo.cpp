#include <iostream>

// ##### Simple print #####
// int main(){
//     std::cout << "hi there!" << std::endl;

//     std::cout << std::endl << std::endl;
//     return(0);
// }

/*
g++ CodeDemo.cpp -o CodeDemo
./CodeDemo
*/

// ##### Simple user input #####
#include <string>
using namespace std;

// int main() {
//     string str; // hold user input
//     cout << "Enter your name: " << flush;
//     cin >> str; // read user input as str
//     cout << "Your name is " << str << "!" << endl; // print user input

//     cout << endl << endl;
//     return(0);
// }

// ##### Simple variables declaration #####
// int a, b = 5;

// int main(){
//     bool my_flag;
//     a = 7;
//     my_flag = false;
//     cout << "a = " << a << endl;
//     cout << "b = " << b << endl;
//     cout << "flag = " << my_flag << endl;
//     cout << endl << endl;
    
//     my_flag = true;
//     cout << "flag = " << my_flag << endl;
//     cout << "a + b = " << a + b << endl;
//     cout << "b - a = " << b - a << endl;
//     unsigned int positive;
//     positive = b - a;
//     cout << "b - a (unsigned) = " << positive << endl;
    
//     cout << endl << endl;
//     return(0);
// }

// ##### Expressions and Assignments #####
// Expressions = operations
// Assignments = variable = value

// ##### Popular operations #####
// + addition
// - subtraction
// * multiplication
// / division
// % remainder

// ##### Type inference #####
// #include <typeinfo>

// int main(){
//     auto a = 8;
//     auto b = 12345678901;
//     auto c = 3.14f;
//     auto d = 3.14;
//     auto e = true;
//     auto f = 'd';
//     auto g = "C++ rocks!";

//     cout << "The type of a is " << typeid(a).name() << endl;
//     cout << "The type of b is " << typeid(b).name() << endl;
//     cout << "The type of c is " << typeid(c).name() << endl;
//     cout << "The type of d is " << typeid(d).name() << endl;
//     cout << "The type of e is " << typeid(e).name() << endl;
//     cout << "The type of f is " << typeid(f).name() << endl;
//     cout << "The type of g is " << typeid(g).name() << endl;

//     cout << endl << endl;
//     return(0);
// }


// ##### Directives #####
// #include <iostream>
// #include <string>
// #include <cstdint>

// #define CAPACITY 5000
// #define DEBUG

// int main(){
//     int32_t large = CAPACITY;
//     uint8_t small = 37;

// #ifdef DEBUG
//     cout << "[About to perform the addition]" << endl;
// #endif

//     large += small;
//     cout << "The large integer is " << large << endl;

//     cout << endl << endl;
//     return(0);
// }

// ##### Arrays #####
// #include <iostream>

// // #define AGE_LENGTH 4 // macro

// int main(){
//     const size_t AGE_LENGTH = 4; // constant
//     int age[AGE_LENGTH];
//     float temperature[] = {31.5, 32.7, 38.9};

//     age[0] = 25;
//     age[1] = 20;
//     age[2] = 19;
//     age[3] = 19;

//     cout << "Age array has " << AGE_LENGTH << " elements." << endl;
//     cout << "Age[0] = " << age[0] << endl;
//     cout << "Age[1] = " << age[1] << endl;
//     cout << "Age[2] = " << age[2] << endl;
//     cout << "Age[3] = " << age[3] << endl;
//     cout << endl;
    
//     cout << "Temp[0] = " << temperature[0] << endl;
//     cout << "Temp[1] = " << temperature[1] << endl;
//     cout << "Temp[2] = " << temperature[2] << endl;

//     cout << endl << endl;
//     return(0);
// }

// ##### Strings #####
#include <iostream>
#include <string>
#include <cstring>

int main(){
    const size_t LENGTH1 = 25;

    char array_str1[LENGTH1] = "Hello guys! ";
    char array_str2[] = "What's up?!";

    string std_str1 = "Hi everybody! ";
    string std_str2 = "How's the going?";

    strncat(array_str1, array_str2, LENGTH1);
    cout << array_str1 << endl;
    cout << std_str1 + std_str2 << endl;
    
    cout << endl << endl;
    return(0);
}

// ##### Type Casting #####
// ...