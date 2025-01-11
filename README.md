# timetable_project
Automated Timetable Generation System: This Python-based tool automates school timetable creation, ensuring conflict-free scheduling for classes like Jr. KG, Sr. KG, and 1st Standard. It allocates periods based on subject requirements, teacher availability, and school constraints, exporting timetables to Excel.
# Automated Timetable Generation System

**Author**: Prathamesh Fuke  

## Project Description  
This project automates the creation of school timetables for Jr. KG, Sr. KG, and 1st Standard. It ensures conflict-free scheduling based on subject requirements, teacher availability, and school constraints, and outputs the timetable in a structured Excel format.  

## Features  
- Generates timetables for multiple classes and divisions (A, B, C, D).  
- Ensures no scheduling conflicts for teachers or subjects.  
- Adheres to period durations, breaks, and assembly timings.  
- Assigns teachers to subjects based on provided data.  
- Outputs detailed timetables in Excel format for easy access.  

## Requirements  
- Python 3.7+  
- Pandas  
- OpenPyXL  

How to Run
Clone the repository:
bash
Copy code
git clone https://github.com/prathameshfuke/timetable-generator.git  
cd timetable-generator  
Place input files:
Copy the required input files (e.g., teacher-subject mapping) into the data/ folder.

Run the script:
bash
Copy code
python timetable_generator.py  
View the output:
Check the output/ folder for the generated timetables.

Assumptions Made
All teachers are available during the defined school hours.
Breaks and assembly schedules are fixed and uniform.
Subject-period mapping is consistent for all divisions of the same grade.
Future Enhancements
Add a GUI for user-friendly input and timetable visualization.
Support for dynamic constraints like teacher unavailability.
Extend to handle more classes and custom schedules.





Author
Developed by Prathamesh Fuke.
Feel free to reach out for collaboration or suggestions!
