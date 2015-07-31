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
        default="",
        display_name="AnalyticsExtras XBlock",
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

    csv_url = String(
        default="http://127.0.0.1:8080/FL_insurance_sample.csv",
        help="URL to CSV containing slide ids and default states",
        scope=Scope.content
    )

    sequence_list_staff = Dict(
        default={},
        help="Dictionary of units within subsection and their states, staff override",
        scope=Scope.content
    )

    dev_stuff = Boolean(
        help="Show chx_dev_stuff div in LMS?",
        default=False, scope=Scope.content
    )

    """

    Functions to build

        populate sessions
        populate sequence_list
        populate sequence_list_staff


    """

    @XBlock.json_handler
    def refresh_sequence(self, data, suffix=''):

        content = {"csv_object": ""}

        csv_object = []
        if self.csv_url[:4] == "http" and self.csv_url[-3:] == "csv":

            '''
            states
            v - visible, but must complete
            h - hidden
            s - visible, but skippable
            '''

            print ("-----" + self.csv_url)

            try:

                f = urllib.urlopen(self.csv_url)
                cr = csv.reader(f)

                for r in cr:
                    print (r)

                f.close()

            except:
                print ("CSV reading error.")

            content["csv_object"] = csv_object

        return content

    @XBlock.json_handler
    def aex_init(self, data, suffix=''):

        #self.session_ended = False

        #settings = {
            #"tick_interval": self.tick_interval,
        #}

        settings = {}

        return settings

#    @staticmethod
#    def clear_data(self):
#        del self.sessions[:]

    #def redirect()

    def student_view(self, context=None):
        """
        The LMS view
        """

        fragment = Fragment()
        content = {'self': self}

        fragment.add_content(render_template('templates/analyticsextras.html', content))
        fragment.add_css(load_resource("static/css/analyticsextras.css"))
        fragment.add_javascript(render_template('static/js/analyticsextras.js', content))
        fragment.initialize_js('AnalyticsExtrasXBlock')

        return fragment

    def studio_view(self, context=None):
        """
        The CMS view
        """

        fragment = Fragment()
        content = {'self': self}

        fragment.add_content(render_template('templates/analyticsextras_edit.html', content))
        fragment.add_css(load_resource('static/css/analyticsextras_edit.css'))
        fragment.add_javascript(load_resource('static/js/analyticsextras_edit.js'))
        fragment.initialize_js('AnalyticsExtrasXBlockStudio')

        return fragment

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Course author pressed the Save button in Studio
        """

        result = {}

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

            self.csv_url = data["csv_url"]
            self.sequence_list_staff = data["sequence_list_staff"]

        return result

    @staticmethod
    def workbench_scenarios():
        return [
            ("AnalyticsExtrasXBlock",
             """<vertical_demo>
                <analyticsextras/>
                </vertical_demo>
             """),
        ]