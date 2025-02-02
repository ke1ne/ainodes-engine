# -*- coding: utf-8 -*-
"""A module containing the base class for the Node's content graphical representation. It also contains an example of
an overridden Text Widget, which can pass a notification to it's parent about being modified."""
from typing import List

from PyQt6.QtCore import Qt
from qtpy import QtCore, QtWidgets
from qtpy import QtGui
from qtpy.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit

from ainodes_frontend.node_engine.node_serializable import Serializable


class QDMNodeContentWidget(QWidget, Serializable):
    eval_signal = QtCore.Signal()
    mark_dirty_signal = QtCore.Signal()

    """Base class for representation of the Node's graphics content. This class also provides layout
    for other widgets inside of a :py:class:`~node_engine.node_node.Node`"""
    def __init__(self, node:'Node', parent:QWidget=None):
        """
        :param node: reference to the :py:class:`~node_engine.node_node.Node`
        :type node: :py:class:`~nodeeditor.node_node.Node`
        :param parent: parent widget
        :type parent: QWidget

        :Instance Attributes:
            - **node** - reference to the :class:`~node_engine.node_node.Node`
            - **layout** - ``QLayout`` container
        """
        self.node = node
        super().__init__(parent)

        self.widget_list = []
        self.initUI()

        #sshFile = "ainodes_frontend/qss/nodeeditor-dark.qss"
        #with open(sshFile, "r") as fh:
        #    self.setStyleSheet(fh.read())

    def initUI(self):
        """Sets up layouts and widgets to be rendered in :py:class:`~node_engine.node_graphics_node.QDMGraphicsNode` class.
        """
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Some Title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QDMTextEdit("foo"))

    def setEditingFlag(self, value:bool):
        """
        .. note::

            If you are handling keyPress events by default Qt Window's shortcuts and ``QActions``, you will not
             need to use this method.

        Helper function which sets editingFlag inside :py:class:`~node_engine.node_graphics_view.QDMGraphicsView` class.

        This is a helper function to handle keys inside nodes with ``QLineEdits`` or ``QTextEdits`` (you can
        use overridden :py:class:`QDMTextEdit` class) and with QGraphicsView class method ``keyPressEvent``.

        :param value: new value for editing flag
        """
        self.node.scene.getView().editingFlag = value

    """def serialize(self) -> OrderedDict:
        return OrderedDict([
        ])"""
    def serialize(self) -> dict:
        res = {}
        for item in self.widget_list:
            if isinstance(item, QtWidgets.QLayout):
                for i in range(item.layout().count()):
                    widget = item.layout().itemAt(i)
                    if isinstance(widget, QtWidgets.QWidgetItem):
                        widget = widget.widget()
                        if isinstance(widget, QtWidgets.QComboBox):
                            res[f"{widget.objectName()}"] = widget.currentText()
                            #print(res[f"{widget.objectName()}"])
                        elif isinstance(widget, QtWidgets.QLineEdit):
                            res[f"{widget.objectName()}"] = widget.text()
                        elif isinstance(widget, QtWidgets.QTextEdit):
                            res[f"{widget.objectName()}"] = widget.toPlainText()
                        elif isinstance(widget, QtWidgets.QSpinBox) or isinstance(widget, QtWidgets.QDoubleSpinBox):
                            res[f"{widget.objectName()}"] = str(widget.value())
                        elif isinstance(widget, QtWidgets.QSlider):
                            res[f"{widget.objectName()}"] = str(widget.value())
                        elif isinstance(widget, QtWidgets.QCheckBox):
                            res[f"{widget.objectName()}"] = str(widget.isChecked())
            elif isinstance(item, QtWidgets.QWidget):
                widget = item
                if isinstance(widget, QtWidgets.QComboBox):
                    res[f"{widget.objectName()}"] = widget.currentText()
                    #print(res[f"{widget.objectName()}"])
                elif isinstance(widget, QtWidgets.QLineEdit):
                    res[f"{widget.objectName()}"] = widget.text()
                elif isinstance(widget, QtWidgets.QTextEdit):
                    res[f"{widget.objectName()}"] = widget.toPlainText()
                elif isinstance(widget, QtWidgets.QSpinBox) or isinstance(widget, QtWidgets.QDoubleSpinBox):
                    res[f"{widget.objectName()}"] = str(widget.value())
                elif isinstance(widget, QtWidgets.QSlider):
                    res[f"{widget.objectName()}"] = str(widget.value())
                elif isinstance(widget, QtWidgets.QCheckBox):
                    res[f"{widget.objectName()}"] = str(widget.isChecked())
        return res



    def deserialize(self, data, hashmap={}, restore_id:bool=True) -> bool:
        for item in self.widget_list:
            if isinstance(item, QtWidgets.QLayout):
                for i in range(item.layout().count()):
                    widget = item.layout().itemAt(i)
                    if isinstance(widget, QtWidgets.QWidgetItem):
                        widget = widget.widget()
                        try:
                            value = data[f"{widget.objectName()}"]
                        except:
                            value = None
                        if value is not None:
                            if isinstance(widget, QtWidgets.QComboBox):
                                widget.setCurrentText(str(data[f"{widget.objectName()}"]))
                            elif isinstance(widget, QtWidgets.QLineEdit):
                                widget.setText(str(data[f"{widget.objectName()}"]))
                            elif isinstance(widget, QTextEdit):
                                widget.setPlainText(str(data[f"{widget.objectName()}"]))
                            elif isinstance(widget, QtWidgets.QSpinBox):
                                widget.setValue(int(data[f"{widget.objectName()}"]))
                            elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                                widget.setValue(float(data[f"{widget.objectName()}"]))
                            elif isinstance(widget, QtWidgets.QSlider):
                                widget.setValue(data[f"{widget.objectName()}"])
                            elif isinstance(widget, QtWidgets.QCheckBox):
                                widget.setChecked(bool(data[f"{widget.objectName()}"]))
            elif isinstance(item, QtWidgets.QWidget):
                widget = item
                try:
                    value = data[f"{widget.objectName()}"]
                except:
                    value = None

                if value is not None:
                    if isinstance(widget, QtWidgets.QComboBox):
                        try:
                            widget.setCurrentText(data[f"{widget.objectName()}"])
                        except:
                            pass
                    elif isinstance(widget, QtWidgets.QLineEdit):
                        widget.setText(str(data[f"{widget.objectName()}"]))
                    elif isinstance(widget, QTextEdit):
                        widget.setPlainText(str(data[f"{widget.objectName()}"]))
                    elif isinstance(widget, QtWidgets.QSpinBox):
                        widget.setValue(int(data[f"{widget.objectName()}"]))
                    elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                        widget.setValue(float(data[f"{widget.objectName()}"]))
                    elif isinstance(widget, QtWidgets.QSlider):
                        widget.setValue(data[f"{widget.objectName()}"])
                    elif isinstance(widget, QtWidgets.QCheckBox):
                        if value is not None:
                            widget.setChecked(True) if value == "True" else widget.setChecked(False)
        return True

        """#try:
        for i in range(self.layout().count()):
            layout = self.layout().itemAt(i)
            print(layout)
            if isinstance(layout, QtWidgets.QHBoxLayout) or isinstance(layout, QtWidgets.QVBoxLayout):
                for k in range(layout.count()):
                    widget = layout.itemAt(k).widget()
                    if isinstance(widget, QtWidgets.QComboBox):
                        try:
                            widget.setCurrentText(data[f"{widget.objectName()}"])
                        except:
                            pass
                    elif isinstance(widget, QtWidgets.QLineEdit):
                        widget.setText(str(data[f"{widget.objectName()}"]))
                    elif isinstance(widget, QTextEdit):
                        widget.setPlainText(str(data[f"{widget.objectName()}"]))
                    elif isinstance(widget, QtWidgets.QSpinBox):
                        widget.setValue(int(data[f"{widget.objectName()}"]))
                    elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                        widget.setValue(float(data[f"{widget.objectName()}"]))
                    elif isinstance(widget, QtWidgets.QCheckBox):
                        widget.setChecked(bool(data[f"{widget.objectName()}"]))
            elif isinstance(layout, QtWidgets.QWidgetItem):
                widget = layout.widget()
                print(widget)
                if isinstance(widget, QtWidgets.QComboBox):
                    index = widget.findText(str(data[f"{widget.objectName()}"]))
                    try:
                        widget.setCurrentText(data[f"{widget.objectName()}"])
                    except Exception as e:
                        print(e)
                        continue

                    #if index == -1:
                    #    widget.setCurrentIndex(0)
                    #else:
                    #    widget.setCurrentIndex(index)
                elif isinstance(widget, QtWidgets.QLineEdit):
                    try:
                        widget.setText(str(data[f"{widget.objectName()}"]))
                    except Exception as e:
                        print(e)
                        pass
                elif isinstance(widget, QTextEdit):
                    try:
                        widget.setPlainText(str(data[f"{widget.objectName()}"]))
                    except Exception as e:
                        print(e)
                        pass
                elif isinstance(widget, QtWidgets.QSpinBox):
                    try:
                        widget.setValue(int(data[f"{widget.objectName()}"]))
                    except Exception as e:
                        print(e)
                        pass

                elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                    try:
                        widget.setValue(float(data[f"{widget.objectName()}"]))
                    except Exception as e:
                        print(e)
                        pass

                elif isinstance(widget, QtWidgets.QCheckBox):
                    try:
                        #print(data[f"{widget.objectName()}"])
                        widget.setChecked(bool(data[f"{widget.objectName()}"]))
                    except Exception as e:
                        print(e)
                        pass

                return True
        #except Exception as e:
        #    dumpException(e)
        #    return False"""
    """def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_E:
            print("TRIGGER")
            self.node.markDirty(True)
            self.node.eval()"""

    def create_combo_box(self, items, label_text, accessible_name=None) -> QtWidgets.QComboBox:
        """Create a combo box widget with the given items and label text.

        Args:
            items (list): List of items to be added to the combo box.
            label_text (str): Text for the label of the combo box.

        Returns:
            QtWidgets.QComboBox: A combo box widget.
        """
        combo_box = QtWidgets.QComboBox()
        combo_box.addItems(items)
        combo_box.setObjectName(label_text)
        if accessible_name is not None:
            combo_box.setAccessibleName(accessible_name)
        label = QtWidgets.QLabel(label_text)
        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(label)
        layout.addWidget(combo_box)
        combo_box.layout = layout
        self.widget_list.append(combo_box)
        return combo_box

    def create_line_edit(self, label_text, accessible_name=None, default=None, placeholder=None) -> QtWidgets.QLineEdit:
        """Create a line edit widget with the given label text.

        Args:
            label_text (str): Text for the label of the line edit.

        Returns:
            QtWidgets.QLineEdit: A line edit widget.
        """
        line_edit = QtWidgets.QLineEdit()
        line_edit.setObjectName(label_text)
        if default is not None:
            line_edit.setText(default)
        if accessible_name is not None:
            line_edit.setAccessibleName(accessible_name)
        if placeholder is not None:
            line_edit.setPlaceholderText(placeholder)
        label = QtWidgets.QLabel(label_text)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(line_edit)
        line_edit.layout = layout
        self.widget_list.append(line_edit)
        return line_edit
    def create_text_edit(self, label_text, placeholder="") -> QtWidgets.QTextEdit:
        """Create a line edit widget with the given label text.

        Args:
            label_text (str): Text for the label of the line edit.

        Returns:
            QtWidgets.QLineEdit: A line edit widget.
        """
        line_edit = QtWidgets.QTextEdit()
        line_edit.setPlaceholderText(placeholder)
        label = QtWidgets.QLabel(label_text)
        line_edit.setObjectName(label_text)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(line_edit)
        line_edit.layout = layout
        self.widget_list.append(line_edit)
        return line_edit


    def create_list_view(self, label_text) -> QtWidgets.QListWidget:
        """Create a list widget with the given label text.

        Args:
            label_text (str): Text for the label of the line edit.

        Returns:
            QtWidgets.QListWidget: A list widget.
        """
        list_view = QtWidgets.QListWidget()
        label = QtWidgets.QLabel(label_text)
        list_view.setObjectName(label_text)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(list_view)
        list_view.layout = layout
        self.widget_list.append(list_view)
        return list_view


    def create_label(self, label_text) -> QtWidgets.QLabel:
        """Create a label widget with the given label text.

        Args:
            label_text (str): Text for the label of the label.

        Returns:
            QtWidgets.QLabel: A label widget.
        """
        label = QtWidgets.QLabel(label_text)
        label.setObjectName(label_text)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        label.layout = layout
        self.widget_list.append(label)
        return label

    def create_spin_box(self, label_text, min_val, max_val, default_val, step_value=1, accessible_name=None) -> QtWidgets.QSpinBox:
        """Create a spin box widget with the given label text, minimum value, maximum value, default value, and step value.

        Args:
            label_text (str): Text for the label of the spin box.
            min_val (int): Minimum value of the spin box.
            max_val (int): Maximum value of the spin box.
            default_val (int): Default value of the spin box.
            step_value (int, optional): Step value of the spin box. Defaults to 1.

        Returns:
            QtWidgets.QSpinBox: A spin box widget.
        """
        spin_box = QtWidgets.QSpinBox()
        spin_box.setMinimum(min_val)
        spin_box.setMaximum(max_val)
        spin_box.setValue(default_val)
        spin_box.setSingleStep(step_value)
        spin_box.setObjectName(label_text)
        if accessible_name is not None:
            spin_box.setAccessibleName(accessible_name)
        label = QtWidgets.QLabel(label_text)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(spin_box)
        spin_box.layout = layout
        self.widget_list.append(spin_box)
        return spin_box
    def create_double_spin_box(self, label_text:str, min_val:float =0.0, max_val:float=10.0, step:float=0.01, default_val:float=1.0, accessible_name=None ) -> QtWidgets.QDoubleSpinBox:
        """Create a double spin box widget with the given label text, minimum value, maximum value, step, and default value.

         Args:
             label_text (str): Text for the label of the double spin box.
             min_val (float): Minimum value of the double spin box.
             max_val (float): Maximum value of the double spin box.
             step (float): Step value of the double spin box.
             default_val (float): Default value of the double spin box.

         Returns:
             QtWidgets.QDoubleSpinBox: A double spin box widget.
         """
        double_spin_box = QtWidgets.QDoubleSpinBox()
        double_spin_box.setMinimum(min_val)
        double_spin_box.setMaximum(max_val)
        double_spin_box.setSingleStep(step)
        double_spin_box.setValue(default_val)
        double_spin_box.setObjectName(label_text)
        if accessible_name is not None:
            double_spin_box.setAccessibleName(accessible_name)
        label = QtWidgets.QLabel(label_text)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(double_spin_box)
        double_spin_box.layout = layout
        self.widget_list.append(double_spin_box)
        return double_spin_box

    def create_check_box(self, label_text, checked=False, accessible_name=None) -> QtWidgets.QCheckBox:
        """Create a double spin box widget with the given label text, minimum value, maximum value, step, and default value.

         Args:
             label_text (str): Text for the label of the double spin box.
             min_val (float): Minimum value of the double spin box.
             max_val (float): Maximum value of the double spin box.
             step (float): Step value of the double spin box.
             default_val (float): Default value of the double spin box.

         Returns:
             QtWidgets.QDoubleSpinBox: A double spin box widget.
         """

        check_box = QtWidgets.QCheckBox(label_text)
        check_box.setChecked(checked)
        check_box.setObjectName(label_text)
        if accessible_name is not None:
            check_box.setAccessibleName(accessible_name)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("white"))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor("black"))
        check_box.setPalette(palette)
        self.widget_list.append(check_box)
        return check_box

    def create_button_layout(self, buttons:List[QtWidgets.QPushButton]) -> QtWidgets.QHBoxLayout:
        """Create a horizontal button layout containing the given buttons.

        Args:
            buttons (list): List of buttons to be added to the layout.

        Returns:
            QtWidgets.QHBoxLayout: A horizontal button layout.
        """
        button_layout = QtWidgets.QHBoxLayout()
        for widget in buttons:

            if isinstance(widget, QtWidgets.QCheckBox):
                palette = QtGui.QPalette()
                palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("white"))
                palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor("black"))
                widget.setPalette(palette)
            button_layout.addWidget(widget)
        self.widget_list.append(button_layout)
        return button_layout

    def create_progress_bar(self, label_text, min_val, max_val, default_val) -> QtWidgets.QProgressBar:
        """Create a progress bar widget with the given label text, minimum value, maximum value, and default value.

        Args:
            label_text (str): Text for the label of the progress bar.
            min_val (int): Minimum value of the progress bar.
            max_val (int): Maximum value of the progress bar.
            default_val (int): Default value of the progress bar.

        Returns:
            QtWidgets.QProgressBar: A progress bar widget.
        """
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setMinimum(min_val)
        progress_bar.setMaximum(max_val)
        progress_bar.setValue(default_val)
        progress_bar.setObjectName(label_text)
        label = QtWidgets.QLabel(label_text)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(progress_bar)
        progress_bar.layout = layout
        self.widget_list.append(layout)
        return progress_bar

    def create_main_layout(self, grid=None) -> None:
        """
        Create the main layout for the widget and add items from the widget_list.
        The layout is a QVBoxLayout with custom margins and will be set as the layout for the widget.
        If grid parameter is provided, a QGridLayout with grid number of columns will be created.
        """
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 25)

        if grid:
            # Create a QGridLayout with the specified number of columns
            self.grid_layout = QtWidgets.QGridLayout()
            self.grid_layout.setSpacing(10)  # Adjust the spacing between items

            # Add widgets to the grid layout
            for i, item in enumerate(self.widget_list):
                row = i // grid
                column = i % grid
                if isinstance(item, QtWidgets.QWidget):
                    if isinstance(item, QtWidgets.QComboBox) or isinstance(item, QtWidgets.QLineEdit) or isinstance(item, QtWidgets.QSpinBox) or isinstance(item, QtWidgets.QDoubleSpinBox):
                        self.grid_layout.addLayout(item.layout, row, column)
                    else:
                        self.grid_layout.addWidget(item, row, column)
                elif isinstance(item, QtWidgets.QLayout):
                    self.grid_layout.addLayout(item, row, column)

            self.main_layout.addLayout(self.grid_layout)
        else:
            # Add items to the main layout without a grid
            for item in self.widget_list:
                if isinstance(item, QtWidgets.QLayout):
                    self.main_layout.addLayout(item)
                elif isinstance(item, QtWidgets.QWidget):
                    self.main_layout.addWidget(item)
        #self.deafult_run_button = QtWidgets.QPushButton("Evaluate Node")
        #self.main_layout.addWidget(self.deafult_run_button)
        #self.deafult_run_button.clicked.connect(self.node.evalImplementation)
        self.setLayout(self.main_layout)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        pass
        #event.ignore()
        #print("IGNORE IN CONTENT WIDGET")


class QDMTextEdit(QTextEdit):
    """
        .. note::

            This class is an example of a ``QTextEdit`` modification that handles the `Delete` key event with an overridden
            Qt's ``keyPressEvent`` (when not using ``QActions`` in menu or toolbar)

        Overridden ``QTextEdit`` which sends a notification about being edited to its parent's container :py:class:`QDMNodeContentWidget`
    """
    def focusInEvent(self, event:'QFocusEvent'):
        """Example of an overridden focusInEvent to mark the start of editing

        :param event: Qt's focus event
        :type event: QFocusEvent
        """
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event:'QFocusEvent'):
        """Example of an overridden focusOutEvent to mark the end of editing

        :param event: Qt's focus event
        :type event: QFocusEvent
        """
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)
