// Comment

const std = @import("std");

const Point = struct {
    x: f32,
    y: f32,

    pub fn distance(self: Point, other: Point) f32 {
        return std.math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2);
    }
};

fn greet(name: []const u8) void {
    std.debug.print("Hello, {}!\n", .{name});
}

pub fn main() void {
    var stdout = std.io.getStdOut().writer();
    const point1 = Point{ .x = 1.0, .y = 2.0 };
    const point2 = Point{ .x = 4.0, .y = 6.0 };

    const distance = point1.distance(point2);
    _ = stdout.print("Distance: {}\n", .{distance});

    const names = [_][]const u8{"Alice", "Bob", "Charlie"};
    for (names) |name| {
        greet(name);
    }

    const multi_line_string = \\ Hello
                              \\ World
        ;

    var counter: u32 = 0;
    while (counter < 10) : (counter += 1) {
        if (counter % 2 == 0) {
            std.debug.print("{} is even\n", .{counter});
        } else {
            std.debug.print("{} is odd\n", .{counter});
        }
    }

    // Error handling
    const result = try someFunction();
    _ = stdout.print("Result: {}\n", .{result});
}

fn someFunction() !i32 {
    return 42;
}