"""Regression checks in a disposable copy; never write to the repository database."""
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class SentinelInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_cwd = Path.cwd()
        cls.temp = tempfile.TemporaryDirectory()
        cls.workspace = Path(cls.temp.name) / 'dashboard'
        shutil.copytree(ROOT, cls.workspace,
                        ignore=shutil.ignore_patterns('.git', '__pycache__', '.venv'))
        os.chdir(cls.workspace)
        sys.path.insert(0, str(cls.workspace))

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(str(cls.workspace))
        os.chdir(cls.original_cwd)
        cls.temp.cleanup()

    def page(self, name):
        app = AppTest.from_file(str(self.workspace / name), default_timeout=90).run()
        self.assertEqual([e.message for e in app.exception], [])
        return app

    def test_existing_pages_render(self):
        pages = ['1_Overview', '3_KPI_Upload', '4_Site_Analytics', '5_Report',
                 '6_Alarms', '7_Settings', '8_Project', 'technology_2G', 'technology_3G',
                 'technology_4G', 'technology_5G', 'technology_VoLTE']
        for name in pages:
            with self.subTest(page=name):
                app = self.page('pages/' + name + '.py')
                self.assertTrue(any('NETWORK OPS' in m.value for m in app.sidebar.markdown))

    def test_briefing_and_case_study_route(self):
        app = self.page('app.py')
        self.assertTrue(any('Operational briefing' in m.value for m in app.markdown))
        app.button(key='sentinel_link_Project').click().run()
        self.assertEqual([e.message for e in app.exception], [])
        self.assertTrue(any('From network signals' in m.value for m in app.markdown))
        app.button(key='project_start').click().run()
        self.assertEqual([e.message for e in app.exception], [])
        self.assertTrue(any('Operational briefing' in m.value for m in app.markdown))

    def test_theme_and_refresh_controls(self):
        app = self.page('pages/7_Settings.py')
        self.assertEqual(app.session_state['dashboard_theme'], 'Dark')
        app.radio(key='settings_theme_selector').set_value('Light').run()
        self.assertEqual([e.message for e in app.exception], [])
        self.assertEqual(app.session_state['dashboard_theme'], 'Light')
        self.assertTrue(any('--s-page:#f4f7fb' in m.value for m in app.markdown))
        app.radio(key='settings_theme_selector').set_value('Dark').run()
        self.assertEqual(app.session_state['dashboard_theme'], 'Dark')

    def test_sidebar_navigation(self):
        app = self.page('app.py')
        app.button(key='sentinel_link_Settings').click().run()
        for name in ['Overview', 'KPI_Upload', 'Site_Analytics', 'Report', 'Alarms', 'Settings']:
            self.assertIsNotNone(app.button(key='sentinel_link_' + name))
        app.button(key='sentinel_link_Overview').click().run()
        self.assertEqual([e.message for e in app.exception], [])
        self.assertTrue(any('Network command centre' in m.value for m in app.markdown))

    def test_technology_navigation_and_charts(self):
        app = self.page('app.py')
        app.button(key='sentinel_link_4G').click().run()
        self.assertGreater(len(app.get('plotly_chart')), 0)
        app.button(key='sentinel_link_5G').click().run()
        self.assertEqual([e.message for e in app.exception], [])
        self.assertTrue(any('5G' in m.value and 'technology-title' in m.value for m in app.markdown))


if __name__ == '__main__':
    unittest.main()
