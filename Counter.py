"""Class for a tkinter 7-segment display."""

class Counter:
    """This class creates the necessary methods to create a 7-segment display with tkinter."""
    def __init__(self, frame, position_x, position_y, length_segment, width_segment):
        """This method creates a hidden display on a specific tkinter frame."""
        self.frame = frame
        self.length_segment = length_segment
        self.width_segment = width_segment
        self.position_x = position_x
        self.position_y = position_y
        self.all_segments = []

        self.segments_draw_line_info = (
            (0, 0, 1, 0),  # top
            (1, 0, 1, 1),  # upper right
            (1, 1, 1, 2),  # lower right
            (0, 2, 1, 2),  # bottom
            (0, 1, 0, 2),  # lower left
            (0, 0, 0, 1),  # upper left
            (0, 1, 1, 1),  # middle
        )

        self.which_segments_are_on_for_each_digit = (
            (1, 1, 1, 1, 1, 1, 0),  # 0
            (0, 1, 1, 0, 0, 0, 0),  # 1
            (1, 1, 0, 1, 1, 0, 1),  # 2
            (1, 1, 1, 1, 0, 0, 1),  # 3
            (0, 1, 1, 0, 0, 1, 1),  # 4
            (1, 0, 1, 1, 0, 1, 1),  # 5
            (1, 0, 1, 1, 1, 1, 1),  # 6
            (1, 1, 1, 0, 0, 0, 0),  # 7
            (1, 1, 1, 1, 1, 1, 1),  # 8
            (1, 1, 1, 1, 0, 1, 1),  # 9
        )

        for x0, y0, x1, y1 in self.segments_draw_line_info:
            self.all_segments.append(self.frame.create_line(
                self.position_x + x0*self.length_segment, self.position_y + y0*self.length_segment, self.position_x + x1*self.length_segment, self.position_y + y1*self.length_segment,
                width=self.width_segment, fill='red', state='hidden'))

    def reveal_segments(self, digit):
        """Updates the display to the correct digit."""
        for i, segment in enumerate(self.which_segments_are_on_for_each_digit[digit]):
            if segment == 1:
                self.frame.itemconfigure(self.all_segments[i], state='normal')
            else:
                self.frame.itemconfigure(self.all_segments[i], state='hidden')
