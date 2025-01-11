import pandas as pd
import numpy as np
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import random
import logging
import os

@dataclass
class Teacher:
    id: str
    name: str
    subjects: List[str]
    grades: List[str]
    max_hours: int
    current_schedule: Dict[str, Set[str]] = None

    def __post_init__(self):
        self.current_schedule = {day: set() for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}

    def is_available(self, day: str, period: str) -> bool:
        return period not in self.current_schedule[day]

    def add_period(self, day: str, period: str):
        self.current_schedule[day].add(period)

class TimetableGenerator:
    def __init__(self, subject_file: str, teacher_file: str):
        self.subjects_df = pd.read_csv(subject_file)
        self.teachers_df = pd.read_csv(teacher_file)
        self.teachers: Dict[str, Teacher] = self._initialize_teachers()
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        # Different time slots for different grades
        self.time_slots = {
            'Jr. KG': [
                ('10:15-10:45', '1st'),
                ('10:45-11:15', '2nd'),
                ('11:15-11:45', '3rd'),
                ('11:45-12:15', '4th'),
                ('12:15-12:45', 'Break'),
                ('12:45-1:15', '5th'),
                ('1:15-1:45', '6th'),
                ('1:45-2:15', '7th'),
                ('2:15-2:20', 'Dispersal')
            ],
            'Sr. KG': [
                ('10:15-10:45', '1st'),
                ('10:45-11:15', '2nd'),
                ('11:15-11:45', '3rd'),
                ('11:45-12:15', '4th'),
                ('12:15-12:45', 'Break'),
                ('12:45-1:15', '5th'),
                ('1:15-1:45', '6th'),
                ('1:45-2:15', '7th'),
                ('2:15-2:20', 'Dispersal')
            ],
            'Class I': [
                ('08:00-08:15', 'Home Room'),
                ('8:15-8:50', '1st'),
                ('8:50-09:25', '2nd'),
                ('09:25-09:45', 'Break'),
                ('09:45-10:15', '3rd'),
                ('10:15-10:45', '4th'),
                ('10:45-11:15', '5th'),
                ('11:15-11:45', '6th'),
                ('11:45-12:15', '7th'),
                ('12:15-12:45', '8th'),
                ('12:45-1:15', 'Break'),
                ('1:15-1:45', '9th'),
                ('1:45-2:15', '10th'),
                ('2:15-2:20', 'Dispersal')
            ]
        }

        self.fixed_activities = {
            'Assembly': {'day': 'Tuesday', 'period': '3rd'},
            'Library': {'day': 'Thursday', 'period': '6th'},
            'Computer Studies': {'day': 'Wednesday', 'period': '4th'},
            'Yoga': {'day': 'Wednesday', 'period': '5th'},
            'KARATE': {'day': 'Thursday', 'period': '5th'},
            'Dance': {'day': 'Wednesday', 'period': '7th'},
            'Clay modelling': {'day': 'Tuesday', 'period': '6th'},
            'Music': {'day': 'Monday', 'period': '5th'},
            'Art': {'day': 'Friday', 'period': '6th'},
            'PE/CCA Sports': {'multiple': True, 'max_per_week': 2}
        }

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _initialize_teachers(self) -> Dict[str, Teacher]:
        teachers = {}
        for _, row in self.teachers_df.iterrows():
            teachers[row['TeacherID']] = Teacher(
                id=row['TeacherID'],
                name=row['Name'],
                subjects=row['Subjects'].split(';'),
                grades=row['Grade'].split(';'),
                max_hours=row['MaxHoursPerDay']
            )
        return teachers

    def _create_empty_timetable(self, grade: str) -> pd.DataFrame:
        times = [slot[0] for slot in self.time_slots[grade]]
        df = pd.DataFrame(index=times, columns=self.days)
        df.index.name = 'Time'

        # Initialize with empty strings
        df.fillna('', inplace=True)

        # Set fixed slots
        for day in self.days:
            if grade == 'Class I':
                df.loc['08:00-08:15', day] = 'Home Room'
            df.loc[df.index[-1], day] = 'Dispersal'

            # Set breaks based on grade
            if grade == 'Class I':
                df.loc['09:25-09:45', day] = 'Break'
                df.loc['12:45-1:15', day] = 'Break'
            else:
                df.loc['12:15-12:45', day] = 'Break'

        return df

    def _get_subjects_for_grade(self, grade: str) -> Dict[str, float]:
        grade_subjects = self.subjects_df[self.subjects_df['Grade'] == grade]
        return dict(zip(grade_subjects['Subject'], grade_subjects['PeriodsPerWeek']))

    def _distribute_subjects(self, grade: str, subjects: Dict[str, float]) -> Dict[str, List[Tuple[str, str]]]:
        """Distribute subjects across the week considering fractional periods"""
        distribution = {day: [] for day in self.days}
        available_slots = self._get_available_slots(grade)

        # First, place fixed activities
        for subject, details in self.fixed_activities.items():
            if subject in subjects and not details.get('multiple', False):
                day = details['day']
                period = details['period']
                time_slot = next((slot[0] for slot in self.time_slots[grade]
                                if slot[1] == period), None)
                if time_slot and time_slot in available_slots[day]:
                    distribution[day].append((subject, time_slot))
                    available_slots[day].remove(time_slot)
                    subjects[subject] -= 1

        # Then distribute regular subjects
        for subject, periods in sorted(subjects.items(), key=lambda x: (-x[1], x[0])):
            remaining = periods
            while remaining > 0:
                # Try to distribute evenly across days
                for day in self.days:
                    if remaining <= 0:
                        break
                    if available_slots[day]:
                        slot = available_slots[day][0]  # Take the first available slot
                        distribution[day].append((subject, slot))
                        available_slots[day].remove(slot)
                        remaining -= 1

        return distribution

    def _get_available_slots(self, grade: str) -> Dict[str, List[str]]:
        """Get available slots for each day excluding breaks and fixed periods"""
        available_slots = {day: [] for day in self.days}

        for day in self.days:
            for time, period in self.time_slots[grade]:
                if period not in ['Home Room', 'Break', 'Dispersal']:
                    available_slots[day].append(time)

        return available_slots

    def generate_timetable(self, grade: str, division: str) -> pd.DataFrame:
        self.logger.info(f"Generating timetable for {grade} Division {division}")

        # Create empty timetable
        timetable = self._create_empty_timetable(grade)

        # Get subjects and their weekly periods
        subjects = self._get_subjects_for_grade(grade)

        # Distribute subjects
        distribution = self._distribute_subjects(grade, subjects)

        # Fill timetable based on distribution
        for day in self.days:
            for subject, time_slot in distribution[day]:
                teacher = self._get_teacher_for_subject(subject, grade, day, time_slot)
                if teacher:
                    timetable.loc[time_slot, day] = f"{subject} ({teacher.name})"
                else:
                    timetable.loc[time_slot, day] = subject

        return timetable

    def _get_teacher_for_subject(self, subject: str, grade: str, day: str, period: str) -> Teacher:
        for teacher in self.teachers.values():
            if (subject in teacher.subjects and
                grade in teacher.grades and
                teacher.is_available(day, period)):
                teacher.add_period(day, period)
                return teacher
        return None

    def format_excel(self, writer: pd.ExcelWriter, sheet_name: str, df: pd.DataFrame):
        """Apply formatting to the Excel worksheet"""
        worksheet = writer.sheets[sheet_name]
        workbook = writer.book

        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'center',
            'align': 'center',
            'border': 1,
            'bg_color': '#D3D3D3'
        })

        cell_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'center',
            'align': 'center',
            'border': 1
        })

        break_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'center',
            'align': 'center',
            'border': 1,
            'bg_color': '#FFE4B5'
        })

        # Set column widths
        worksheet.set_column(0, 0, 15)  # Time column
        worksheet.set_column(1, 5, 20)  # Day columns

        # Set row heights
        for i in range(len(df.index) + 1):
            worksheet.set_row(i, 40)

        # Write headers
        for col_num, value in enumerate(['Time'] + self.days):
            worksheet.write(0, col_num, value, header_format)

        # Write data
        for row_num, index in enumerate(df.index):
            worksheet.write(row_num + 1, 0, index, cell_format)  # Write time
            for col_num, column in enumerate(df.columns):
                cell_value = df.loc[index, column]
                format_to_use = break_format if 'Break' in cell_value else cell_format
                worksheet.write(row_num + 1, col_num + 1, cell_value, format_to_use)

    def generate_all_timetables(self, output_file: str):
        """Generate timetables for all grades and divisions"""
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            for grade in ['Jr. KG', 'Sr. KG', 'Class I']:
                for division in ['A', 'B', 'C', 'D']:
                    timetable = self.generate_timetable(grade, division)
                    sheet_name = f"{grade}-{division}"
                    timetable.to_excel(writer, sheet_name=sheet_name, index=True)
                    self.format_excel(writer, sheet_name, timetable)

        self.logger.info(f"All timetables generated and saved to {output_file}")
