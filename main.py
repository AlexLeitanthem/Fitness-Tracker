# main.py
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QStackedWidget, QLabel, 
                             QLineEdit, QPushButton, QFormLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QDoubleSpinBox, QSpinBox,
                             QFileDialog, QMessageBox, QComboBox, QCalendarWidget, QDialog,
                             QDialogButtonBox, QAbstractItemView)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat, QColor
import database as db

class EditWorkoutDialog(QDialog):
    def __init__(self, workout_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit: {workout_data['name']}")
        
        layout = QVBoxLayout(self)
        
        self.sets_table = QTableWidget()
        self.sets_table.setColumnCount(3)
        self.sets_table.setHorizontalHeaderLabels(["Set", "Reps", "Weight (kg)"])
        self.populate_table(workout_data['sets'])
        layout.addWidget(self.sets_table)

        set_entry_layout = QHBoxLayout()
        self.reps_input = QSpinBox()
        self.weight_int_input = QSpinBox()
        self.weight_int_input.setRange(0, 500)
        self.weight_dec_input = QComboBox()
        self.weight_dec_input.addItems([".0", ".25", ".5", ".75"])
        add_set_button = QPushButton("Add Set")
        remove_set_button = QPushButton("Remove Selected Set")

        set_entry_layout.addWidget(QLabel("Reps:"))
        set_entry_layout.addWidget(self.reps_input)
        set_entry_layout.addWidget(QLabel("Weight:"))
        set_entry_layout.addWidget(self.weight_int_input)
        set_entry_layout.addWidget(self.weight_dec_input)
        set_entry_layout.addWidget(add_set_button)
        layout.addLayout(set_entry_layout)
        layout.addWidget(remove_set_button)

        add_set_button.clicked.connect(self.add_set)
        remove_set_button.clicked.connect(self.remove_set)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def populate_table(self, sets_data):
        self.sets_table.setRowCount(len(sets_data))
        for i, s in enumerate(sets_data):
            self.sets_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.sets_table.setItem(i, 1, QTableWidgetItem(str(s['reps'])))
            self.sets_table.setItem(i, 2, QTableWidgetItem(str(s['weight'])))
        self.sets_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def add_set(self):
        reps = self.reps_input.value()
        if reps <= 0: return
        
        weight_int = self.weight_int_input.value()
        weight_dec = float(self.weight_dec_input.currentText())
        weight = weight_int + weight_dec

        row = self.sets_table.rowCount()
        self.sets_table.insertRow(row)
        self.sets_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.sets_table.setItem(row, 1, QTableWidgetItem(str(reps)))
        self.sets_table.setItem(row, 2, QTableWidgetItem(str(weight)))
        self.reps_input.setValue(0)
        self.weight_int_input.setValue(0)

    def remove_set(self):
        current_row = self.sets_table.currentRow()
        if current_row >= 0:
            self.sets_table.removeRow(current_row)
            for row in range(self.sets_table.rowCount()):
                self.sets_table.item(row, 0).setText(str(row + 1))

    def get_updated_sets(self):
        updated_sets = []
        for row in range(self.sets_table.rowCount()):
            reps = int(self.sets_table.item(row, 1).text())
            weight = float(self.sets_table.item(row, 2).text())
            updated_sets.append({'reps': reps, 'weight': weight})
        return updated_sets

class EditCardioDialog(QDialog):
    def __init__(self, cardio_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit: {cardio_data['name']}")
        
        layout = QFormLayout(self)
        self.duration_input = QSpinBox()
        self.duration_input.setRange(0, 1000)
        self.duration_input.setValue(cardio_data.get('duration', 0))
        self.distance_input = QDoubleSpinBox()
        self.distance_input.setRange(0, 1000)
        self.distance_input.setValue(cardio_data.get('distance', 0))
        self.calories_input = QSpinBox()
        self.calories_input.setRange(0, 5000)
        self.calories_input.setValue(cardio_data.get('calories', 0))
        self.incline_input = QSpinBox()
        self.incline_input.setRange(0, 15)
        self.incline_input.setValue(cardio_data.get('incline', 0))
        
        layout.addRow("Duration (min):", self.duration_input)
        layout.addRow("Distance (km):", self.distance_input)
        layout.addRow("Calories Burned:", self.calories_input)
        
        self.incline_label = QLabel("Incline (%):")
        layout.addRow(self.incline_label, self.incline_input)
        if cardio_data['name'] not in ["Running", "Walking (Incline)"]:
            self.incline_label.hide()
            self.incline_input.hide()
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_updated_data(self):
        return {
            'duration': self.duration_input.value(),
            'distance': self.distance_input.value(),
            'calories': self.calories_input.value(),
            'incline': self.incline_input.value() if self.incline_input.isVisible() else 0
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Tracker Pro")
        self.setGeometry(100, 100, 1400, 800)
        
        # The main content is now just the WorkoutWidget
        self.setCentralWidget(WorkoutWidget())

class WorkoutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.all_exercises_in_group = []
        self.logs_for_date = []
        
        main_layout = QHBoxLayout(self)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.calendar = QCalendarWidget()
        self.calendar.setMaximumDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.load_workouts_for_selected_date)
        
        self.daily_log_table = QTableWidget()
        self.daily_log_table.setColumnCount(3)
        self.daily_log_table.setHorizontalHeaderLabels(["Exercise", "Details", "Actions"])
        self.daily_log_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.daily_log_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.daily_log_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        left_layout.addWidget(QLabel("<h2>Daily Log</h2>"))
        left_layout.addWidget(self.calendar)
        left_layout.addWidget(self.daily_log_table)
        main_layout.addWidget(left_widget, 2)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 20, 20, 20)
        
        form_layout = QFormLayout()
        self.group_selector = QComboBox()
        self.selected_exercise_label = QLineEdit()
        self.selected_exercise_label.setReadOnly(True)
        self.selected_exercise_label.setPlaceholderText("No Exercise Selected")
        form_layout.addRow(QLabel("<h3>Add New Entry</h3>"))
        form_layout.addRow("Category:", self.group_selector)
        self.exercise_list = QListWidget()
        form_layout.addRow(self.exercise_list)
        form_layout.addRow("Selected:", self.selected_exercise_label)
        right_layout.addLayout(form_layout)

        self.input_stack = QStackedWidget()
        self.strength_widget = QWidget()
        self.cardio_widget = QWidget()
        self.input_stack.addWidget(self.strength_widget)
        self.input_stack.addWidget(self.cardio_widget)
        right_layout.addWidget(self.input_stack)
        self.input_stack.hide()

        strength_layout = QVBoxLayout(self.strength_widget)
        set_entry_layout = QHBoxLayout()
        self.set_reps_input = QSpinBox()
        self.set_weight_int_input = QSpinBox()
        self.set_weight_int_input.setRange(0, 500)
        self.set_weight_dec_input = QComboBox()
        self.set_weight_dec_input.addItems([".0", ".25", ".5", ".75"])
        add_set_button = QPushButton("Add Set")
        set_entry_layout.addWidget(QLabel("Reps:")); set_entry_layout.addWidget(self.set_reps_input)
        set_entry_layout.addWidget(QLabel("Weight:")); set_entry_layout.addWidget(self.set_weight_int_input)
        set_entry_layout.addWidget(self.set_weight_dec_input); set_entry_layout.addWidget(add_set_button)
        strength_layout.addLayout(set_entry_layout)
        self.current_sets_table = QTableWidget()
        self.current_sets_table.setColumnCount(3)
        self.current_sets_table.setHorizontalHeaderLabels(["Set", "Reps", "Weight (kg)"])
        strength_layout.addWidget(self.current_sets_table)
        save_workout_button = QPushButton("Save Workout")
        strength_layout.addWidget(save_workout_button)

        cardio_layout = QFormLayout(self.cardio_widget)
        self.cardio_duration = QSpinBox(); self.cardio_duration.setRange(0, 1000)
        self.cardio_distance = QDoubleSpinBox(); self.cardio_distance.setRange(0, 1000)
        self.cardio_calories = QSpinBox(); self.cardio_calories.setRange(0, 5000)
        self.cardio_incline = QSpinBox(); self.cardio_incline.setRange(0, 15)
        save_cardio_button = QPushButton("Save Cardio")
        cardio_layout.addRow("Duration (min):", self.cardio_duration)
        cardio_layout.addRow("Distance (km):", self.cardio_distance)
        cardio_layout.addRow("Calories Burned:", self.cardio_calories)
        self.cardio_incline_label = QLabel("Incline (%):")
        cardio_layout.addRow(self.cardio_incline_label, self.cardio_incline)
        cardio_layout.addRow(save_cardio_button)

        main_layout.addWidget(right_widget, 1)

        self.group_selector.currentIndexChanged.connect(self.update_exercise_list)
        self.exercise_list.itemClicked.connect(self.select_exercise)
        add_set_button.clicked.connect(self.add_set_to_table)
        save_workout_button.clicked.connect(self.save_workout)
        save_cardio_button.clicked.connect(self.save_cardio)

        self.load_muscle_groups()
        self.load_workouts_for_selected_date()
        self.highlight_dates_with_workouts()

    def load_workouts_for_selected_date(self):
        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        
        strength_logs = db.get_detailed_workouts_by_date(date_str)
        cardio_logs = db.get_cardio_by_date(date_str)
        self.logs_for_date = sorted(strength_logs + cardio_logs, key=lambda x: x['name'])
        
        self.daily_log_table.setRowCount(len(self.logs_for_date))
        for row_idx, log_data in enumerate(self.logs_for_date):
            name = log_data['name']
            details = ""
            if log_data['type'] == 'strength':
                details = ", ".join([f"{s['reps']} reps x {s['weight']}kg" for s in log_data['sets']])
            elif log_data['type'] == 'cardio':
                details = f"{log_data['duration']} min, {log_data['distance']} km, {log_data['calories']} kcal"
                if log_data.get('incline') and log_data['incline'] > 0:
                    details += f", {log_data['incline']}% incline"
            
            self.daily_log_table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.daily_log_table.setItem(row_idx, 1, QTableWidgetItem(details))
            
            actions_widget = QWidget(); actions_layout = QHBoxLayout(actions_widget)
            edit_button = QPushButton("Edit"); delete_button = QPushButton("Delete")
            edit_button.clicked.connect(lambda ch, r=row_idx: self.edit_entry(r))
            delete_button.clicked.connect(lambda ch, r=row_idx: self.delete_entry(r))
            actions_layout.addWidget(edit_button); actions_layout.addWidget(delete_button)
            actions_layout.setContentsMargins(0,0,0,0)
            self.daily_log_table.setCellWidget(row_idx, 2, actions_widget)

    def edit_entry(self, row_index):
        log_data = self.logs_for_date[row_index]
        if log_data['type'] == 'strength':
            dialog = EditWorkoutDialog(log_data, self)
            if dialog.exec():
                updated_sets = dialog.get_updated_sets()
                if updated_sets:
                    db.update_workout(log_data['id'], updated_sets)
        elif log_data['type'] == 'cardio':
            dialog = EditCardioDialog(log_data, self)
            if dialog.exec():
                data = dialog.get_updated_data()
                db.update_cardio_log(log_data['id'], data['duration'], data['distance'], data['calories'], data['incline'])
        self.load_workouts_for_selected_date()

    def delete_entry(self, row_index):
        log_data = self.logs_for_date[row_index]
        confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure?")
        if confirm == QMessageBox.StandardButton.Yes:
            if log_data['type'] == 'strength':
                db.delete_workout(log_data['id'])
            elif log_data['type'] == 'cardio':
                db.delete_cardio_log(log_data['id'])
            self.load_workouts_for_selected_date()
            self.highlight_dates_with_workouts()

    def save_cardio(self):
        exercise = self.selected_exercise_label.text()
        if not exercise: QMessageBox.warning(self, "Input Error", "Please select a cardio exercise."); return
        
        incline = self.cardio_incline.value() if self.cardio_incline.isVisible() else 0
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        db.add_cardio_session(exercise, selected_date, self.cardio_duration.value(), self.cardio_distance.value(), self.cardio_calories.value(), incline)
        
        self.selected_exercise_label.clear()
        self.cardio_duration.setValue(0); self.cardio_distance.setValue(0); self.cardio_calories.setValue(0); self.cardio_incline.setValue(0)
        self.group_selector.setCurrentIndex(0)
        self.input_stack.hide()
        self.load_workouts_for_selected_date()
        self.highlight_dates_with_workouts()

    def select_exercise(self, item):
        self.selected_exercise_label.setText(item.text())
        group = self.group_selector.currentText()
        exercise_name = item.text()
        self.input_stack.show()
        
        if group == "Cardio":
            self.input_stack.setCurrentIndex(1)
            self.cardio_duration.setValue(0); self.cardio_distance.setValue(0); self.cardio_calories.setValue(0); self.cardio_incline.setValue(0)
            if exercise_name in ["Running", "Walking (Incline)"]:
                self.cardio_incline_label.show()
                self.cardio_incline.show()
            else:
                self.cardio_incline_label.hide()
                self.cardio_incline.hide()
        else:
            self.input_stack.setCurrentIndex(0)
            self.current_sets_table.setRowCount(0)
    
    def save_workout(self):
        exercise = self.selected_exercise_label.text()
        if not exercise: QMessageBox.warning(self, "Input Error", "Please select an exercise first."); return
        if self.current_sets_table.rowCount() == 0: QMessageBox.warning(self, "Input Error", "Please add at least one set."); return
        sets_data = []
        for row in range(self.current_sets_table.rowCount()):
            reps = int(self.current_sets_table.item(row, 1).text())
            weight = float(self.current_sets_table.item(row, 2).text())
            sets_data.append({'reps': reps, 'weight': weight})
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        db.add_workout(exercise, selected_date, sets_data)
        self.selected_exercise_label.clear()
        self.current_sets_table.setRowCount(0)
        self.group_selector.setCurrentIndex(0)
        self.input_stack.hide()
        self.load_workouts_for_selected_date()
        self.highlight_dates_with_workouts()

    def highlight_dates_with_workouts(self):
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
        dates_with_logs = db.get_dates_with_workouts()
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor("#d4edff"))
        highlight_format.setForeground(QColor("black"))
        for date_str in dates_with_logs:
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            self.calendar.setDateTextFormat(date, highlight_format)

    def load_muscle_groups(self):
        self.group_selector.clear(); self.group_selector.addItem("--- Select a Category ---")
        self.group_selector.addItems(db.get_all_muscle_groups())
    def update_exercise_list(self):
        group = self.group_selector.currentText()
        self.selected_exercise_label.clear()
        self.input_stack.hide()
        if group and group != "--- Select a Category ---":
            self.exercise_list.clear()
            self.exercise_list.addItems(db.get_exercises_by_group(group))
        else:
            self.exercise_list.clear()
            
    def add_set_to_table(self):
        reps = self.set_reps_input.value()
        if reps <= 0: return
        weight_int = self.set_weight_int_input.value()
        weight_dec = float(self.set_weight_dec_input.currentText())
        weight = weight_int + weight_dec
        row_count = self.current_sets_table.rowCount()
        self.current_sets_table.insertRow(row_count)
        self.current_sets_table.setItem(row_count, 0, QTableWidgetItem(str(row_count + 1)))
        self.current_sets_table.setItem(row_count, 1, QTableWidgetItem(str(reps)))
        self.current_sets_table.setItem(row_count, 2, QTableWidgetItem(str(weight)))
        self.set_reps_input.setValue(0); self.set_weight_int_input.setValue(0)

if __name__ == "__main__":
    db.setup_database()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
