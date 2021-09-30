# gtester

## Wrapper around google tests


## What it solves?
It allows you to re-run failed tests as well as to filter those failed tests by using numeric tags 

### How to use it?

* Set which executable file will be executed:
```` 
./gtester.py --exe exe_name
````
* Run all tests:
```
./gtester.py
```
* Run just failing tests:
```
./gtester.py --run_failing
```
* Run several failing tests using tags:
```
./gtester.py --run_failing 1 3
```
## Example
![Demo](demo.gif)
