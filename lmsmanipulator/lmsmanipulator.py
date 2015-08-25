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

    hide_global_nav_bar = Boolean(
        default=False,
        help="Hide global navigation bar",
        scope=Scope.content
    )

    hide_course_material_bar = Boolean(
        default=False,
        help="Hide course material bar",
        scope=Scope.content
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

    hide_footer = Boolean(
        default=False,
        help="Hide footer",
        scope=Scope.content
    )

    course_url = String(
        default="http://127.0.0.1:8001/",
        help="Course URL. Mandatory field.",
        scope=Scope.content
    )

    location_id = String(
        default="",
        help="Unit URL code. Mandatory field.",
        scope=Scope.content
    )

    csv_url = String(
        default="http://127.0.0.1:8080/sample.csv",
        help="URL to CSV containing slide ids and default states",
        scope=Scope.content
    )

    dev_stuff = Boolean(
        help="Show chx_dev_stuff div in LMS?",
        default=False,
        scope=Scope.content
    )

    course_tree = Dict(
        default={},
        help="JSON-friendly course tree",
        scope=Scope.user_state
    )

    unit_index = Dict(
        default={},
        help="Dictionary containing course ids and their location in the tree above",
        scope=Scope.user_state
    )

    @XBlock.json_handler
    def refresh_navigation(self, data, suffix=''):

        content = {
            "name": "",
            "chapter": "",
            "location_id": self.location_id
        }

        if 'name' in self.course_tree.keys():
            content["name"] = self.course_tree["name"]

        if 'chapter' in self.course_tree.keys():
            content["chapter"] = self.course_tree["chapter"]

        return content

    @staticmethod
    def course_tree_read(csv_url):
        """
        Generate a course dictionary of course_tree, subsections and units based on the structure provided in the CSV file
        located at csv_url.
        """

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

            course_name = csv_reader.next()  # Read course name
            if course_name[0] == "COURSE_NAME":
                course_tree["name"] = course_name[1]

            csv_reader.next() # Skip row with column names

            for row in csv_reader:

                # Add a new chapter to dictionary
                if row[0] != "":
                    course_tree["chapter"][str(current_chapter + 1)] = {
                        "name": row[0],
                        "enabled": (row[5] == "1"),
                        "visible": (row[6] == "1"),
                        "subsection": {}
                    }
                    current_chapter += 1
                    current_subsection = -1

                # Add a new subsection to current chapter
                if row[1] != "":
                    course_tree["chapter"][str(current_chapter)]["subsection"][str(current_subsection + 1)] = {
                        "name": row[1],
                        "enabled": (row[5] == "1"),
                        "visible": (row[6] == "1"),
                        "unit": {}
                    }
                    current_subsection += 1
                    current_unit = 0

                # Add a new unit to current subsection
                if row[2] != "":
                    course_tree["chapter"][str(current_chapter)]["subsection"][str(current_subsection)]["unit"][str(current_unit)] = \
                        {
                            "name": row[2],
                            "url": row[3],
                            "required": (row[4] == "1"),
                            "enabled": (row[5] == "1"),
                            "visible": (row[6] == "1"),
                            "unlocks": row[7].split(';'),
                            "completed": False
                        }

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

    def get_unit_by_location(self, chapter, subsection, unit):
        '''
        Return unit from tree based on its chapter/subsection/unit location
        '''

        result = {
            "data": {},
            "chapter": -1,
            "subsection": -1,
            "unit": -1
        }

        try:

            result["data"] = \
                self.course_tree["chapter"][str(chapter)]["subsection"][str(subsection)]["unit"][str(unit)]
            result["chapter"] = chapter
            result["subsection"] = subsection
            result["unit"] = unit

        except:

            print ("Unit not found in course tree.")

        return result

    def get_unit_by_url(self, url):
        '''
        Return unit from tree based on its url
        '''

        result = {
            "data": {},
            "chapter": "-1",
            "subsection": "-1",
            "unit": "-1"
        }

        try:

            loc = self.unit_index[url]
            result["data"] = self.course_tree["chapter"][str(loc[0])]["subsection"][str(loc[1])]["unit"][str(loc[2])]
            result["chapter"] = str(loc[0])
            result["subsection"] = str(loc[1])
            result["unit"] = str(loc[2])

        except:

            print ("Unit not found in course tree.")

        return result

    @XBlock.json_handler
    def get_unit(self, data, suffix=''):

        result = {}
        tmp = {}

        if data["chapter"] != "" and data["subsection"] != "" and data["unit"] != "":
            tmp = self.get_unit_by_location(int(data["chapter"]), int(data["subsection"]), int(data["unit"]))

        else:
            tmp = self.get_unit_by_url(self.location_id)

        result["chapter"] = tmp["chapter"]
        result["subsection"] = tmp["subsection"]
        result["unit"] = tmp["unit"]
        result.update(tmp["data"])

        return result

    # def for set_unit

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

    def course_tree_refresh(self):
        """
        Read course tree and assign returned values to course_tree and unit_index
        """

        tree = self.course_tree_read(self.csv_url)
        self.course_tree = tree["course_tree"]
        self.unit_index = tree["unit_index"]

        # over here read from the student-specific table and update the units in course_tree with the db stored
        # visible, enabled, completed fields

    def complete(self):

        this_unit = self.get_unit_by_url(self.location_id)

        if this_unit['unit'] != "-1":

            # mark this unit as completed in the tree

            # unlock units specified for this unit
            # update the student-specific table
            for u in this_unit['unlocks']:
                print u

        # run a refresh
        self.course_tree_refresh()

    def student_view(self, context=None):
        """
        The LMS view
        """

        fragment = Fragment()
        content = {
            'self': self
        }

        self.course_tree_refresh()

        print "# ========================================= #"

        print self.location_id

        #self.complete()

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
            self.hide_global_nav_bar = data["hide_global_nav_bar"] == 1
            self.hide_course_material_bar = data["hide_course_material_bar"] == 1
            self.hide_nav_buttons = data["hide_nav_buttons"] == 1
            self.hide_nav = data["hide_nav"] == 1
            self.hide_sequence_bottom = data["hide_sequence_bottom"] == 1
            self.hide_sidebar = data["hide_sidebar"] == 1
            self.toggle_sidebar = data["toggle_sidebar"] == 1
            self.hide_footer = data["hide_footer"] == 1
            self.dev_stuff = data["dev_stuff"] == 1

            if self.hide_sidebar:
                self.toggle_sidebar = False

            self.course_url = data["course_url"]
            self.location_id = data["location_id"]
            self.csv_url = data["csv_url"]

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