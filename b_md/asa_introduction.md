<title>Asa Introduction</title>

!!! important
    This is page is very much still a work in progress

# Introduction to the Asa programming language


---

<img src="https://raw.githubusercontent.com/Asa-Programming-Language/Asa/refs/heads/dev/media/ASA-Full-light.png" width="50%">

----

## So, you want to use Asa?

Asa is a systems programming language built to be used similarly to C++, but be a good replacement. It aims to improve upon many of the shortcomings of that aging language, without sacrificing performance.

```asa
main :: (){
    printl("Hello World!");
}
```

----

## The Compile Time Define Operator:

One of the operators you will be using most often in Asa is the compile time define. This is defined as the double colon, `:::asa ::`.
It shares many of the characteristics of the set operator (`=`), and sometimes their functionality even overlaps. It can also be compared to the `:::cpp #define` preprocessor keyword from C or C++, although Asa does not have a preprocessor.

Compile time define is used to assign an expression to a name. The most basic example would be:
```asa
x :: 5;
```
!!! note inline
    This code will evaluate to the exact same as `:::asa x = 5;`

Of course, more interesting expressions are better. Let's put a lambda expression on the right side:
```asa
x :: int(){ return 5 }
```
Now this is a function.

### Other uses:

`::` can be used for defining other things as well. Such as structs, modules, and special functions.

#### Defining Structs:

You can create a struct by writing the name, and defining it as a struct expression:

```asa
someStruct :: struct{

}
```

#### Defining Modules:

You can define a module by writing the name, and defining it as a module expression:

```asa
moduleName :: module{

}
```

----

## Structs:

You can create a struct by writing the name, and defining it as a struct expression:

```asa
someStruct :: struct{
    // ...
}
```
Then to create an instance:
```asa
y : someStruct = someStruct();
```

### Struct Members:

Member variables and functions are defined as normal. Functions, though, have slightly different behavior.
For example:

```asa
someStruct :: struct{

    x : int = 10;

    memberFunction :: (v : int){
        this.x = v;
    }
}
```
The difference with functions defined inside of a struct is that that they can only be called with the access operator (`.`), but they can also access members within the struct itself. To do this, you must use the `:::asa this` keyword, which references the instance the function is within.
Then member access is as normal like:
```asa
s : someStruct = someStruct();

printl(s.x); // -> 10

s.memberFunction(3);

printl(s.x); // -> 3

```


### Struct specific functions:

There are some functions that have specific names and functionality for handling structs.

### Create:
```asa
create :: someStruct(){
    // ...
}
```

----

## Expressions:

In Asa, most things you write are "expressions". In other words, the individual components should be able to be evaluated all on their own. For example, take the following function:

```asa
functionName :: (){
}
```

Given the above function, we can split it into its sub-expressions:

The name:
```asa
functionName
```
and a lambda:
```asa
(){}
```

The lambda is simply an unnamed function. You can create one with parentheses containing the function arguments, followed by curly braces containing the body. Like: `:::asa (x : int){}`.
If you want the lambda to have a return value, it should be preceded by the type. Like: `:::asa int(x : int){ return x+1; }`


----

## Special Function Definitions:

Just like in C++, there are some special ways to define functions for certain use cases.

### Operator Overloading:

Operator overloading is used to override builtin behavior or add new behavior to existing or new symbols. For example:

```asa
operator@ :: int(x : int, y : int){
    return x * y;
}

printl(3 @ 1);
// -> Outputs 3
```

Defining an operator overload is done with the following syntax:

```
operator<symbol> :: <return type>(<Left value>, <Right value>){
}
```

The `<symbol>` can be any ASCII special character, and can be a double character as well. Example: `:::asa $` or `:::asa $$`. The only symbols you cannot overload are the compiler define `:::asa ::` and a few punctuation symbols. Also, the list of available symbols is predefined, so some combinations may be missing.


----

## Compiler keywords:

In Asa, there are a number of keywords for modifying the behavior of the compiler during compilation. These all start with the character `:::asa #`. Any compiler keyword is an expression that will be evaluated at ***compile time***.

-----
## `:::asa #import`
One of the most used keywords, used for importing modules by name. For example:
```asa
#import Rendering:Window;
#import Rendering:Drawing:Line;
```
This imports the module `Window` in the directory `modules/Rendering`. The module expression can be more complex, for example sub-directories: `:::asa #import A:B:C:ModuleName;`, which would be in `modules/A/B/C`. You can also wildcard import modules by using the base path followed by an asterisk: `:::asa #import Builtin:*;`, which would import all modules of all files in the directory `modules/Builtin/`.
`#import` looks in multiple locations for the specified module. First, it looks in the local directory from where it is called. If there is a matching module (including all path components), then it will stop there. If it does not find a matching module locally, it will look in the global modules folder, which is installed next to the `asa` executable. This allows you to override builtin modules for specific use cases.

-----
## `:::asa #file`
This is similar to `:::asa #import`, but instead of only including a single module, it loads the entire file. Also, it does so by an explicit path. For example:
```asa
#file "./otherFile.asa";
```
This would compile and import the entire other file at the given path. The path is evaluated relative to the file which `:::asa #file` is in.

-----
## `:::asa #extern`
This is a method to reference external functions from libraries. For example:
```asa
#extern printf :: int32 (s : const *char, ...);
```
The above would allow you to use the `printf` function from the C standard library. `:::asa #extern` use is simply stating the function name and parameters as they are defined, and not including a body.

-----
## `:::asa #inline`
This is a function modifier that tells the compiler it should be in-lined for performance.

-----
## `:::asa #replaceable`
This is a function modifier that tells the compiler another function with the same identity can be defined. While function overloading typically requires a different identity, if `:::asa #replaceable` is used in the original, it can be overloaded without an error. This will effectively delete the `:::asa #replaceable` function and use the newly defined one.

-----
## `:::asa #hideast`
This is a function modifier that just hides the function from showing in the AST verbose output. This is primarily used for compiler development.

-----
## `:::asa #variant`
This is a function modifier that creates variants of the function. For example:
```asa
foo :: ()
    #variant w = 0;
{
    printl(w);
}
```
Then you can use it like so:
```asa
foo<w=7>(); // -> 7
foo<w=2>(); // -> 2
```
This looks like arguments with extra steps, but the main difference is that it permanently creates a completely different function for each combination during the compilation process. So the above would have equivalent code to the following (except for the identities being the same, which would throw an error):
```asa
foo :: (){
    printl(7);
}

foo :: (){
    printl(2);
}
```
This is useful if you want to allow for a function to work with multiple types:
```asa
foo :: T(v : T)
    #variant T = int;
{
    return v * 2;
}
```

-----
## `:::asa #new`
TODO: `:::asa #new` is for manually creating objects from their name, like: `:::asa #new structName`. It should be removed and replaced by an automatic `:::asa create` function addition.

-----
## `:::asa #cast`
TODO: `:::asa #cast` is for manually casting a value to a builtin type, like: `:::asa #cast 5 : float`. It should be removed and replaced by an automatic `:::asa cast` function addition.



