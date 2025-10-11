
#!/usr/bin/env ruby

# This is a comment

require 'json'

PI = 3.14159
MAX_USERS = 100

class User
    attr_accessor :name, :age

    def initialize(name = "Guest", age = 0)
        @name = name
        @age = age
    end

    def greet
        puts "Hello, #{@name}! You are #{@age} years old."
    end
end

def factorial(n)
    return 1 if n <= 1
        n * factorial(n - 1)
end

def square(x)
    x ** 2
end

users = [
    User.new("Alice", 25),
    User.new("Bob", 30)
]

users.each_with_index do |user, index|
    puts "User ##{index + 1}:"
    user.greet
end

begin
    puts "Factorial of 5 is #{factorial(5)}"
    puts "Square of 9 is #{square(9)}"
    result = JSON.parse('{"status":"ok"}')
    puts "Parsed JSON: #{result['status']}"
rescue StandardError => e
    puts "An error occurred: #{e.message}"
ensure
    puts "Cleanup complete."
end
