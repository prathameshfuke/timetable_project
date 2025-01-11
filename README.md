# School Timetable Generator

A Python-based automated timetable generation system designed for schools, with specific support for kindergarten and primary classes. The system handles complex scheduling requirements including teacher availability, subject distribution, and fixed activity slots.

## Features

- Generates comprehensive timetables for multiple grades (Jr. KG, Sr. KG, Class I)
- Supports multiple divisions (A, B, C, D) per grade
- Handles fixed activities like Assembly, Library, PE, etc.
- Considers teacher availability and maximum teaching hours
- Manages break times and dispersal periods
- Exports timetables to formatted Excel workbook
- Built-in support for fractional period allocation
- Grade-specific time slots and scheduling patterns

## Requirements

- Python 3.7+
- pandas
- numpy
- xlsxwriter
- typing
- dataclasses

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/school-timetable-generator.git
cd school-timetable-generator
```

2. Install required packages:
```bash
pip install pandas numpy xlsxwriter
```

## Data Setup

The system requires two CSV files in the `data` directory:

### 1. `subject_allotment.csv`
Should contain:
- Grade
- Subject
- PeriodsPerWeek

Example format:
```csv
Grade,Subject,PeriodsPerWeek
Jr. KG,English,5
Jr. KG,Mathematics,4
```

### 2. `teacher_mapping.csv`
Should contain:
- TeacherID
- Name
- Subjects (semicolon-separated)
- Grade (semicolon-separated)
- MaxHoursPerDay

Example format:
```csv
TeacherID,Name,Subjects,Grade,MaxHoursPerDay
T001,John Doe,English;Mathematics,Jr. KG;Sr. KG,6
T002,Jane Smith,Science;EVS,Class I,5
```

## Usage

1. Ensure your data files are properly formatted and placed in the `data` directory.

2. Run the timetable generator:
```bash
python main.py
```

3. The generated timetables will be saved in `output/school_timetables.xlsx`

## Output Format

The program generates an Excel workbook with:
- Separate sheets for each grade and division
- Time slots in rows
- Days of the week in columns
- Formatted cells showing subject and teacher assignments
- Color-coded breaks and special periods
- Proper formatting for readability

## Customization

The system supports customization through:

1. Time Slots: Modify the `time_slots` dictionary in `TimetableGenerator` class
2. Fixed Activities: Adjust the `fixed_activities` dictionary
3. Days: Change the `days` list if needed
4. Break Times: Modify break slots in `_create_empty_timetable` method

## Project Structure

```
school-timetable-generator/
├── data/
│   ├── subject_allotment.csv
│   └── teacher_mapping.csv
├── output/
├── timetable_generator.py
├── main.py
└── README.md
```

## Limitations

- Currently supports specific grade levels (Jr. KG, Sr. KG, Class I)
- Fixed five-day week schedule
- Predefined set of special activities
- Single break time slot per grade level

## Contributing

Feel free to open issues or submit pull requests with improvements. Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- School administrators and teachers who provided valuable input on scheduling requirements
- The pandas and xlsxwriter development teams for their excellent libraries
