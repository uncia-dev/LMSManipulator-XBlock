import csv
import json
import datetime
import urllib

course_tree = {}
csv_url = 'http://127.0.0.1:8080/sample.csv'

def course_tree_read(csv_url):

    course_tree = { \
        "time": str(datetime.datetime.now()), \
        "name": "", \
        "chapter": {} \
        }

    try:

        csv_file = urllib.urlopen(csv_url)
        csv_reader = csv.reader(csv_file)        

        current_chapter = -1
        current_subsection = 0
        current_unit = 0

        course_name = csv_reader.next() # Read course name
        if course_name[0] == "COURSE_NAME":
            course_tree["name"] = course_name[1]
        
        csv_reader.next() # Skip row with column names

        for row in csv_reader:

            # Add a new chapter to dictionary
            if row[0] != "":
                course_tree["chapter"][str(current_chapter + 1)] = \
                    {"name": row[0], "subsection": {}}
                current_chapter += 1
                current_subsection = -1

            # Add a new subsection to current chapter
            if row[1] != "":
                course_tree["chapter"][str(current_chapter)]["subsection"][str(current_subsection + 1)] = \
                    {"name": row[1], "unit": {}}
                current_subsection += 1
                current_unit = 0

            # Add a new unit to current subsection
            if row[2] != "":
                course_tree["chapter"][str(current_chapter)]["subsection"][str(current_subsection)]["unit"][str(current_unit)] = \
                    {"name": row[2], "url": row[3], "state": row[4]}
                current_unit += 1

        csv_file.close()

    except:
        print("Something broke in CSV reading, most likely invalid URL.")

    return course_tree

def course_tree_print(course_tree):

    print course_tree["name"] + " (Last Edit: " + course_tree["time"] + ")"
    for chapter in course_tree["chapter"]:
        print "+ " + course_tree["chapter"][chapter]["name"]
        for subsection in course_tree["chapter"][chapter]["subsection"]:
            print "\-+ " + course_tree["chapter"][chapter]["subsection"][subsection]["name"]
            for unit in course_tree["chapter"][chapter]["subsection"][subsection]["unit"]:
                print "  |- " + course_tree["chapter"][chapter]["subsection"][subsection]["unit"][unit]["name"]

course_tree = course_tree_read(csv_url)
course_tree_print(course_tree)
