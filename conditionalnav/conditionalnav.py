"""
???
"""

import urllib, datetime, json, csv

from .utils import render_template, load_resource, resource_string
from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, Boolean, Dict
from xblock.fragment import Fragment

class ConditionalNavigatorXBlock(XBlock):

    display_name = String(
        default="ConditionalNavigator XBlock",
        display_name="ConditionalNavigator XBlock",
        help="",
        scope=Scope.settings
    )

    csv_url = String(
        default="",
        help="URL to CSV containing slide ids and default states",
        scope=Scope.content
    )

    slide_state = Dict(
        default={},
        help="Dictionary containing state of each slide for this student",
        scope=Scope.user_state
    )

    sessions = List(
        default={},
        help="List containing data on each session (ie, start time, end time)",
        scope=Scope.user_state
    )


    # method for visits

    def student_view(self, context=None):
        """
        The primary view of the ConditionalNavigatorXBlock, shown to students
        when viewing courses.
        """
        frag = Fragment()
        content = {'self': self}

        frag.add_content(render_template('templates/conditionalnav.html', content))
        frag.add_css(load_resource("static/css/conditionalnav.css"))
        frag.add_javascript(load_resource("static/js/conditionalnav.js"))
        frag.initialize_js('ConditionalNavigatorXBlock')

        return frag

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ConditionalNavigatorXBlock",
             """<vertical_demo>
                <conditionalnav/>
                </vertical_demo>
             """),
        ]
