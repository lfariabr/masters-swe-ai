// # 1. Basic Structure of a C++ Program

#include <iostream> // Header for input/output
using namespace std; // So you can use cout/cin without "std::"

int main () {
    cout << "Hello, World!" << endl;
    return 0;
}
// 	•	#include <iostream>: lets you use cout (print) and cin (input)
// 	•	main(): where execution starts
// 	•	return 0: program ran successfully

// # 2. Variables and Types

int age = 25;
float height = 1.75;
char grade = "A";
string name = "Luis";
bool isStudent = true;

// 	•	we must declare the type of the variable before using it

// # 3. Input/Output
int age;
cout << "Enter your age: ";
cin >> age;
cout << "You are " << age << " years old." << endl;

// 	•	cout: output to user (console out)
// 	•	cin: input from user (console in)

// # 4. Control Structures
// if-else
if (age >= 18) {
    cout << "You are an adult.";
} else {
    cout << "You are a minor.";
}

// for
for (int i =0; i < 5; i++) {
    cout << i << " ";
}

// while
int i = 0;
while (i < 5) {
    cout << i << " ";
    i++;
}

// # 5. Functions
// declaring and defining
int add(int a, int b) {
    return a + b;
}

// calling a function
int result = add(5, 3); // result = 8
cout << "The result is " << result << endl;
