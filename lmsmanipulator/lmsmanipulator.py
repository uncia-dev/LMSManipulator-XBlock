"""
???
"""

"""
import urllib, datetime, json, csv, utils

from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, Boolean, Dict
from xblock.fragment import Fragment

from django.template import Context, Template
"""

import urllib, datetime, json, csv, utils
from .utils import render_template, load_resource, resource_string
from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, Boolean, Dict
from xblock.fragment import Fragment

class LMSManipulatorXBlock(XBlock):

    display_name = String(
        default="LMS Manipulator",
        display_name="LMSManipulator XBlock",
        help="",
        scope=Scope.settings
    )

    hide_nav_buttons = Boolean(
        default=False,
        help="Hide top navigation buttons in LMS",
        scope=Scope.content
    )

    hide_nav = Boolean(
        default=False,
        help="Hide the entire navigation bar in LMS.",
        scope=Scope.content
    )

    hide_sequence_bottom = Boolean(
        default=False,
        help="Hide bottom navigation buttons in LMS",
        scope=Scope.content
    )

    hide_sidebar = Boolean(
        default=False,
        help="Hide side bar in LMS",
        scope=Scope.content
    )

    toggle_sidebar = Boolean(
        default=False,
        help="Toggle side bar in LMS",
        scope=Scope.content
    )

    course_url = String(
        default="",
        help="Course URL. Mandatory field.",
        scope=Scope.content
    )

    location_id = String(
        default="",
        help="Unit URL code. Mandatory field.",
        scope=Scope.content
    )

    csv_url = String(
        default="",
        help="URL to CSV containing slide ids and default states",
        scope=Scope.content
    )

    dev_stuff = Boolean(
        help="Show chx_dev_stuff div in LMS?",
        default=False,
        scope=Scope.content
    )

    course_tree = Dict(
        help="Dictionary containing course tree read from specified CSV file",
        default={},
        scope=Scope.content
    )

    course_tree_student = Dict(
        help="Dictionary containing course tree adapted to the student's performance and progress",
        default={},
        scope=Scope.user_state
    )

    unit_index = Dict(
        help="Dictionary containing unit location ids and their index. A reverse of course_tree",
        default={},
        scope=Scope.content
    )

    @XBlock.json_handler
    def refresh_navigation(self, data, suffix=''):

        content = {
            "name": "",
            "chapter": "",
            "location_id": self.location_id
        }

        if self.course_tree_student != {}:

            content["name"] = self.course_tree_student["name"]
            content["chapter"] = self.course_tree["chapter"]

        return content

    @staticmethod
    def course_tree_read(csv_url):
        """
        Generate a course dictionary of course_tree, subsections and units based on the structure provided in the CSV file
        located at csv_url.
        """

        '''
        states
        vc - visible, but must complete
        hc - hidden, but must complete
        vs - visible, but skippable (default if column is blank)
        hs - hidden, but skippable when visible
        '''

        course_tree = {
            "time": str(datetime.datetime.now()),
            "name": "",
            "chapter": {},
        }

        unit_index = {}

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
                    unit_index[row[3]] = [current_chapter, current_subsection, current_unit]
                    current_unit += 1

            csv_file.close()

        except:

            print("Something broke in CSV reading, most likely invalid URL.")

        return {"course_tree": course_tree, "unit_index": unit_index}

    @staticmethod
    def course_tree_print(course_tree):
        """
        Print all course_tree in Python console in a hierarchy structure
        """

        if course_tree != {}:
            print(course_tree["name"] + " (Last Edit: " + course_tree["time"] + ")")
            for chapter in course_tree["chapter"]:
                print("+ " + course_tree["chapter"][chapter]["name"])
                for subsection in course_tree["chapter"][chapter]["subsection"]:
                    print("\-+ " + course_tree["chapter"][chapter]["subsection"][subsection]["name"])
                    for unit in course_tree["chapter"][chapter]["subsection"][subsection]["unit"]:
                        print("  |- " + course_tree["chapter"][chapter]["subsection"][subsection]["unit"][unit]["name"])

    @staticmethod
    def get_time_from_string(str_time):
        """
        Return datetime object generated from string str_time.
        """
        return datetime.datetime.strptime(str_time, '%Y-%m-%d %I:%M:%S.%f')

    @XBlock.json_handler
    def goto_unit(self, data, suffix=''):

        """
        Expected contents in data (must be numbers):

            "chapter"
            "subsection"
            "unit"

        """

        content = {"url": "", "tab": "", "error": ""}

        # TODO Check student course tree to see if student can view the redirect page !!!

        if data["chapter"] != "" and data["subsection"] != "" and data["unit"] != "" and self.course_url != "":

            try:

                # Check if goto unit is in the same chapter and subsection as current unit
                if str(self.unit_index[self.location_id][0]) == data["chapter"] and \
                                str(self.unit_index[self.location_id][1]) == data["subsection"]:

                    # Just specify the tab number if both units are in the same chapter and subsection
                    if self.unit_index[self.location_id][2] != data["unit"]:
                        # must be in the same subsection; switch tab only
                        content["tab"] = data["unit"]

                    # else will not redirect - same unit

                else:

                    # Generate redirect url if unit is not in the same chapter and subsection
                    content["url"] += \
                        self.course_url + \
                        "jump_to/block-v1:edX+DemoX+Demo_Course+type@vertical+block@" + \
                        self.course_tree["chapter"][data["chapter"]]["subsection"][data["subsection"]]["unit"][data["unit"]]["url"]

            except KeyError:
                content["error"] = "LMS Manipulator: Unit not found."

        else:
            content["error"] = "Invalid parameters passed to goto_unit method."

        return content

    """
    TODO:

    set_chapter_visibility(chapter)
    set_subsection_visibility(subsection)
    set_unit_visibility(unit)

    """

    def student_view(self, context=None):
        """
        The LMS view
        """

        fragment = Fragment()
        content = {'self': self}

        if self.course_tree != {}:

            if self.course_tree_student == {}:
                self.course_tree_student = self.course_tree

            else:

                # check if the course tree was updated
                #if self.get_time_from_string(self.course_tree['time']) > self.get_time_from_string(self.course_tree_student['time']):

                    # TODO: do stuff here that retains student settings for each unit
                self.course_tree_student = self.course_tree

        fragment.add_content(render_template('templates/lmsmanipulator.html', content))
        fragment.add_css(load_resource("static/css/lmsmanipulator.css"))
        fragment.add_javascript(render_template('static/js/lmsmanipulator.js', content))
        fragment.initialize_js('LMSManipulatorXBlock')

        return fragment

    def studio_view(self, context=None):
        """
        The CMS view
        """

        fragment = Fragment()
        content = {'self': self}

        fragment.add_content(render_template('templates/lmsmanipulator_edit.html', content))
        fragment.add_css(load_resource('static/css/lmsmanipulator_edit.css'))
        fragment.add_javascript(load_resource('static/js/lmsmanipulator_edit.js'))
        fragment.initialize_js('LMSManipulatorXBlockStudio')

        return fragment

    @XBlock.json_handler
    def studio_save(self, data, suffix=''):
        """
        Course author pressed the Save button in Studio
        """

        result = {'result': 'success'}

        if len(data) > 0:

            self.display_name = data["display_name"]
            self.hide_nav_buttons = data["hide_nav_buttons"] == 1
            self.hide_nav = data["hide_nav"] == 1
            self.hide_sequence_bottom = data["hide_sequence_bottom"] == 1
            self.hide_sidebar = data["hide_sidebar"] == 1
            self.toggle_sidebar = data["toggle_sidebar"] == 1
            self.dev_stuff = data["dev_stuff"] == 1

            if self.hide_sidebar:
                self.toggle_sidebar = False

            self.course_url = data["course_url"]
            self.location_id = data["location_id"]
            self.csv_url = data["csv_url"]

            if self.csv_url[:4] == "http" and self.csv_url[-3:] == "csv":
                tree = self.course_tree_read(self.csv_url)
                self.course_tree = tree["course_tree"]
                self.unit_index = tree["unit_index"]

        return result

    @staticmethod
    def workbench_scenarios():
        return [
            ("LMSManipulatorXBlock",
             """<vertical_demo>
                <lmsmanipulator/>
                </vertical_demo>
             """),
        ]