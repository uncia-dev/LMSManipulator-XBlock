import csv
import urllib

chapters = {}
csv_url = 'http://127.0.0.1:8080/sample.csv'

def chapters_read(csv_url):

    csv_file = urllib.urlopen(csv_url)
    csv_reader = csv.reader(csv_file)

    chapters = {}
    current_chapter = -1 # current
    current_subsection = 0
    current_unit = 0

    # Skip line with column names
    csv_reader.next()

    for row in csv_reader:

        # Add a new chapter to dictionary
        if row[0] != "":
            chapters[str(current_chapter + 1)] = \
                {"name": row[0], "subsection": {}}
            current_chapter += 1
            current_subsection = -1

        # Add a new subsection to current chapter
        if row[1] != "":
            chapters[str(current_chapter)]["subsection"][str(current_subsection + 1)] = \
                {"name": row[1], "unit": {}}
            current_subsection += 1
            current_unit = 0

        # Add a new unit to current subsection
        if row[2] != "":
            chapters[str(current_chapter)]["subsection"][str(current_subsection)]["unit"][str(current_unit)] = \
                {"name": row[2], "url": row[3], "state": row[4]}
            current_unit += 1

    csv_file.close()

    return chapters

def chapters_print(chapters):

    for chapter in chapters:

        print "+ " + chapters[chapter]["name"]

        for subsection in chapters[chapter]["subsection"]:

            print "\-+ " + chapters[chapter]["subsection"][subsection]["name"]

            for unit in chapters[chapter]["subsection"][subsection]["unit"]:

                print "  |- " + chapters[chapter]["subsection"][subsection]["unit"][unit]["name"]
