"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import urllib, datetime, json
import csv

from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, Dict
from xblock.fragment import Fragment

from django.template import Context, Template
from .utils import render_template, load_resource, resource_string

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
        scope=Scope.settings
    )

    slide_state = Dict(
        default={},
        help="Dictionary containing state of each slide for this student",
        scope=Scope.user_state
    )

    sessions = Dict(
        default={},
        help="Dictionary containing start time & date and time spent during a session pairs",
        scope=Scope.user_state
    )

    visits = Integer(
        default=0,
        help="Number of times the student visited this XBlock."
    )

    def student_view(self, context=None):
        """
        The primary view of the ConditionalNavigatorXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("templates/conditionalnav.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/conditionalnav.css"))
        frag.add_javascript(self.resource_string("static/js/conditionalnav.js"))
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
