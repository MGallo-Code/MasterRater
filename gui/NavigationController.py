# gui/NavigationController.py

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, QObject

class NavigationController(QObject):
    # Signal to update the central widget in MainWindow
    current_widget_changed = Signal(QWidget)

    def __init__(self):
        super().__init__()
        self.back_stack = []
        self.forward_stack = []

    def push(self, widget: QWidget):
        """
        Push a new widget onto navigation stack, clear forward
        history when new widget is pushed.
        """
        # Append to stack, or create our first widget history with a reset.
        if self.back_stack:
            self.back_stack.append(widget)
        else:
            self.reset(widget)
        
        # Clear forward history
        self.forward_stack.clear()
        self.current_widget_changed.emit(widget)
    
    def pop(self):
        """
        Go back to the previous widget, moves current widget to
        the forward stack.
        """
        if len(self.back_stack) > 1:
            # Move current widget to forward stack
            current_widget = self.back_stack.pop()
            self.forward_stack.append(current_widget)

            # Show the previous widget
            self.current_widget_changed.emit(self.back_stack[-1])
    
    def forward(self):
        """
        Move forward to next widget in our history queue.
        """
        if len(self.forward_stack) > 0:
            next_widget = self.forward_stack.pop()
            self.back_stack.append(next_widget)
            self.current_widget_changed.emit(next_widget)

    def can_go_back(self):
        return len(self.back_stack) > 1
    
    def can_go_forward(self):
        return len(self.forward_stack) > 0
    
    def current_widget(self):
        if len(self.back_stack) > 0:
            return self.back_stack[-1]
        return None
    
    def reset(self, widget: QWidget):
        """
        Reset the navigation controller with new root.
        Clear historical stacks.
        """
        self.back_stack = [widget]
        self.forward_stack.clear()
        self.current_widget_changed.emit(widget)