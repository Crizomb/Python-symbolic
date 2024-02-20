import tkinter as tk
from python_symb.Expressions.expr import Expr
from python_symb.MathTypes.symbols import Var


class Visual:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Visual")
        self.root.geometry("1200x1200")

        # Add a canvas on the left side of the window
        self.tree_canvas = tk.Canvas(self.root, width=800, height=800, bg="white")
        self.tree_canvas.pack(side=tk.LEFT, expand=False)

        # Create right frame
        self.right_frame = tk.Frame(self.root, width=300, height=500, background="grey")

        # Add a label with the text "Variables" on top of the right frame, should not take all the space
        self.variables_label = tk.Label(self.right_frame, text="Variables:")
        self.variables_label.pack()

        # Add an entry below the label with default text x y z"
        self.variables_entry = tk.Entry(self.right_frame, width=50)
        self.variables_entry.insert(0, "x y z")
        self.variables_entry.pack()

        # Add a button below the entry with the text "Update variables"
        self.variables_button = tk.Button(self.right_frame, text="Update variables", command=self.update_variables)
        self.variables_button.pack()



        # Add a label with the text "Input" on top of the right frame, should not take all the space
        self.input_label = tk.Label(self.right_frame, text="Input (infix string):")



        # Add a entry below the label with default text "(5+2)*3"
        self.input_entry = tk.Entry(self.right_frame, width=50)
        self.input_entry.insert(0, "(5+2)*3")



        # Add a button below the entry with the text "To Tree"
        self.input_button = tk.Button(self.right_frame, text="To Tree", command=self.show_tree)

        # Pack the widgets, make sure they are not expanding, and all are fixed size


        self.input_label.pack()
        self.input_entry.pack()
        self.input_button.pack()
        self.right_frame.pack(side=tk.LEFT, expand=False)






        self.root.mainloop()

    def update_variables(self):
        # Get the text from the entry
        text = self.variables_entry.get()

        # Create the variables
        variables = text.split()

        for v in variables:
            if v not in Var.instances:
                Var(v)



    def show_tree(self):
        # Get the text from the entry
        text = self.input_entry.get()

        # Clear the canvas
        self.tree_canvas.delete("all")
        tree = Expr.from_infix_str(text)

        # Draw the tree
        self.draw_tree(tree)

    def create_circle(self, x, y, r, color):  # center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.tree_canvas.create_oval(x0, y0, x1, y1, fill=color)

    def draw_tree(self, tree, first_x=400, first_y=50, x_offset=250, y_offset=200, radius=30, fact_mult=0.75):
        print(tree)
        children = tree.children
        n = len(children)
        for i in range(n):
            child = children[i]
            x = first_x + (i - (n - 1) / 2) * x_offset
            y = first_y + y_offset

            #Link the node to the parent
            self.tree_canvas.create_line(first_x, first_y, x, y)
            # Draw the node
            self.draw_tree(child, int(x), y, x_offset*fact_mult, y_offset*fact_mult, radius=radius*fact_mult)

        # Draw the root node
        self.create_circle(first_x, first_y, radius, "red")
        self.tree_canvas.create_text(first_x, first_y, text=str(tree.value))


if __name__ == "__main__":
    Visual()









