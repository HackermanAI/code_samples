
program SyntaxHighlighterTest;

{$APPTYPE CONSOLE}
{$MODE OBJFPC} // For Free Pascal compatibility

uses
    SysUtils, Math;

const
    PiApprox = 3.14159;
    MaxItems = 100;

type
    TPerson = record
        Name: string;
        Age: Integer;
        procedure Print;
    end;

    TIntegerArray = array[1..MaxItems] of Integer;
    TFunc = function(x: Double): Double;

var
    i: Integer;
    NameList: array[1..5] of string = ('Alice', 'Bob', 'Charlie', 'Dave', 'Eve');
    Person: TPerson;
    NumList: TIntegerArray;
    Callback: TFunc;

procedure TPerson.Print;
begin
    WriteLn('Name: ', Name);
    WriteLn('Age: ', Age);
end;

function Square(x: Double): Double;
begin
    Result := x * x;
end;

function Factorial(n: Integer): Integer;
begin
    if n <= 1 then
        Result := 1
    else
        Result := n * Factorial(n - 1);
end;

begin
    Person.Name := 'John Doe';
    Person.Age := 30;
    Person.Print;

    Callback := @Square;
    WriteLn('Square of 5: ', Callback(5.0):0:2);

    for i := 1 to 5 do
        WriteLn('Name ', i, ': ', NameList[i]);

    try
        WriteLn('Factorial of 5 is: ', Factorial(5));
    except
        on E: Exception do
        WriteLn('An error occurred: ', E.Message);
    end;
end.
