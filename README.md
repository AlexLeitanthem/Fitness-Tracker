# Fitness Tracker Pro

A comprehensive desktop application for tracking fitness workouts, cardio sessions, and body measurements built with Python and PyQt6.

## Features

- **Workout Tracking**: Log strength training exercises with sets, reps, and weights
- **Cardio Sessions**: Track running, cycling, swimming, and other cardio activities
- **Body Measurements**: Record weight, body fat percentage, and body measurements
- **Calendar View**: Visual calendar showing workout history with highlighted dates
- **Exercise Database**: Pre-loaded with common exercises organized by muscle groups
- **Data Management**: Edit, delete, and view workout history
- **File Parser**: Import workout data from text files

## Screenshots

The application features a clean, intuitive interface with:
- Left panel: Calendar view and daily workout log
- Right panel: Exercise selection and data entry forms
- Support for both strength training and cardio exercises

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fitness-tracker-pro
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Adding Workouts

1. Select a date on the calendar
2. Choose a muscle group from the dropdown
3. Select an exercise from the list
4. Add sets with reps and weights
5. Click "Save Workout"

### Adding Cardio

1. Select "Cardio" from the muscle group dropdown
2. Choose a cardio exercise
3. Enter duration, distance, calories, and incline (if applicable)
4. Click "Save Cardio"

### Managing Data

- **View History**: Click on any date in the calendar to see workouts
- **Edit Entries**: Click "Edit" next to any workout in the daily log
- **Delete Entries**: Click "Delete" to remove workouts
- **Calendar Highlights**: Dates with workouts are highlighted in blue

## File Parser

The application includes a file parser that can process text files with workout data. Place text files in the configured directory (default: `D:/Games/FitnessLogs`) with the following formats:

- **Workout**: `Workout: Bench Press, 3 sets, 10 reps, 70kg`
- **Weight**: `Weight: 74.5kg`
- **Cardio**: `Cardio: Running, 30 min, 5 km, 300 kcal`

## Database

The application uses SQLite for data storage. The database file (`fitness_tracker.db`) is created automatically and contains the following tables:

- `exercises`: Pre-loaded exercise database
- `workouts`: Strength training sessions
- `workout_sets`: Individual sets for each workout
- `cardio_sessions`: Cardio activities
- `body_measurements`: Weight and body measurements

## Building Executable

To create a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller "Fitness Tracker Pro.spec"
   ```

The executable will be created in the `dist` folder.

## Project Structure

```
fitness-tracker-pro/
├── main.py                 # Main application file
├── database.py            # Database operations
├── file_parser.py         # Text file parser
├── settings.conf          # Configuration file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
├── venv/                 # Virtual environment
├── build/                # Build artifacts
├── dist/                 # Distribution files
└── fitness_tracker.db    # SQLite database
```

## Dependencies

- **PyQt6**: GUI framework
- **SQLite3**: Database (included with Python)

## Configuration

Edit `settings.conf` to customize:
- File parser directory path
- Database settings
- Application preferences

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute.

## Support

For issues and questions, please create an issue in the repository.

## Version History

- **v1.0**: Initial release with basic workout tracking
- **v1.1**: Added cardio tracking and calendar view
- **v1.2**: Enhanced UI and file parser integration
