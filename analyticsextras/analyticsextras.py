"""
???
"""

import urllib, datetime, json, csv
from .utils import render_template, load_resource, resource_string
from django.template import Context, Template
from xblock.core import XBlock
from xblock.fields import Scope, Integer, List, String, Boolean, Dict
from xblock.fragment import Fragment

class AnalyticsExtrasXBlock(XBlock):

    display_name = String(
        default="AnalyticsExtras XBlock",
        display_name="AnalyticsExtras XBlock",
        help="",
        scope=Scope.settings
    )

    csv_url = String(
        default="",
        help="URL to CSV containing slide ids and default states",
        scope=Scope.content
    )

    hide_nav_buttons = Boolean(
        default=False,
        help="Hide top navigation buttons in LMS",
        scope=Scope.content
    )

    hide_sequence_bottom = Boolean(
        default=False,
        help="Hide bottom navigation buttons in LMS",
        scope=Scope.content
    )

    sequence_list_staff = Dict(
        default={},
        help="Dictionary of units within subsection and their states, staff override",
        scope=Scope.content
    )

    sequence_list = Dict(
        default={},
        help="Dictionary of units within subsection and their states for the user",
        scope=Scope.user_state
    )

    sessions = List(
        default=[],
        help="List containing data on each session (ie, start time, end time)",
        scope=Scope.user_state
    )



    """

    Functions to build

        number of visits
        send ticks to backend to record time spent per session
        populate sessions
        populate sequence_list
        populate sequence_list_staff


    """

    @staticmethod
    def clear_data(self):
        del self.sessions[:]

    @staticmethod
    def get_student_visits(self):
        return len(self.sessions)

    @staticmethod
    def session_start(self):

        print ("===== Session started at: " + str(datetime.datetime.now()))

        self.sessions.append(
            [str(datetime.datetime.now()), ""]
        )

    @XBlock.json_handler
    def session_end(self, data, suffix=''):

        content = {"msg": "session_ended"}

        print ("===== Session ended at: " + str(datetime.datetime.now()))
        self.sessions[-1][1] = str(datetime.datetime.now())

        return content

    def student_view(self, context=None):

        fragment = Fragment()
        content = {'self': self}

        self.session_start(self)

        fragment.add_content(render_template('templates/analyticsextras.html', content))
        fragment.add_css(load_resource("static/css/analyticsextras.css"))
        fragment.add_javascript(load_resource("static/js/analyticsextras.js"))
        fragment.initialize_js('AnalyticsExtrasXBlock')

        return fragment

    def studio_view(self, context=None):

        fragment = Fragment()
        content = {'self': self}

        fragment.add_content(render_template('templates/analytics_edit.html', content))
        fragment.add_css(load_resource('static/css/analyticsextras_edit.css'))
        fragment.add_javascript(load_resource('static/js/analyticsextras_edit.js'))
        fragment.initialize_js('AnalyticsExtrasXBlockStudio')

        return fragment

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("AnalyticsExtrasXBlock",
             """<vertical_demo>
                <analyticsextras/>
                </vertical_demo>
             """),
        ]