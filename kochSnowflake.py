# python example to draw complete Koch curve (snowflake) recursively.
import turtle # https://docs.python.org/3/library/turtle.html

# EXAMPLE of how turtle operates:
# turtle.forward(distance)
# turtle.backward(distance)
# turtle.left(angle)
# turtle.right(angle)


def init_turtle() -> None:
    # defining the speed of the turtle and setting coordinates of the start
    turtle.speed(0)
    turtle.color('blue')
    turtle.penup()
    turtle.backward(side / 2.0)
    turtle.left(90)
    turtle.forward(side / 3.0)
    turtle.right(90)
    turtle.pendown()


# function to create koch snowflake or koch curve
def snowflake(side: int, level: int) -> None:
    """ Recursive function.
        Base case: level == 0 - draws a straight line of length == side.
        Otherwise: level != 0 - splits the side into 3 parts and
            - calls itself for (1/3 x side, level - 1)
            - turns 60 degrees left
            - calls itself for (1/3 x side, level - 1)
            - turns 120 degrees right
            - calls itself for (1/3 x side, level - 1)
            - turns 60 degrees left
            - calls itself for (1/3 x side, level - 1)
    """

    if level == 0:
        turtle.forward(side)
    else:
        side /= 3.0
        snowflake(side, level - 1)
        turtle.left(60)
        snowflake(side, level - 1)
        turtle.right(120)
        snowflake(side, level - 1)
        turtle.left(60)
        snowflake(side, level - 1)



if __name__ == "__main__":
    # initial side
    side = 300.0

    # initialising the turtle
    init_turtle()

    # actual drawing of the snowflake!
    for i in range(3):
        snowflake(side, 4)  # play with the level: from 0 to 4!
        turtle.right(120)

    # controlling the closing windows of the turtle
    turtle.mainloop()
