from timetable_generator import TimetableGenerator
import os

def main():
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    generator = TimetableGenerator(
        subject_file='data/subject_allotment.csv',
        teacher_file='data/teacher_mapping.csv'
    )
    generator.generate_all_timetables('output/school_timetables.xlsx')

if __name__ == "__main__":
    main()
