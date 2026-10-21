import unittest
import pandas as pd
from performance_insights import compare_days, quality, exceptions, summarize


class PerformanceInsightsTests(unittest.TestCase):
    def test_site_coverage_changes_do_not_create_false_traffic_growth(self):
        frame = pd.DataFrame([
            {'time':'2026-01-01','ihs_id':'A','data_4g_mb':100,'availability_4g':98},
            {'time':'2026-01-02','ihs_id':'A','data_4g_mb':120,'availability_4g':99},
            {'time':'2026-01-02','ihs_id':'B','data_4g_mb':900,'availability_4g':100},
        ])
        result = compare_days(frame)
        self.assertEqual(result['matched_sites'], 1)
        self.assertEqual(result['added_sites'], 1)
        self.assertEqual(result['metrics']['data_mb']['delta'], 20)
        self.assertEqual(result['metrics']['availability']['delta'], 1)

    def test_missing_counters_on_one_date_are_excluded_on_both(self):
        frame = pd.DataFrame([
            {'time':'2026-01-01','ihs_id':'A','availability_2g':95,'availability_4g':100},
            {'time':'2026-01-03','ihs_id':'A','availability_2g':96},
        ])
        result = compare_days(frame)
        self.assertEqual(result['gap_days'], 2)
        self.assertEqual(result['metrics']['availability']['delta'], 1)
        self.assertEqual(result['metrics']['availability']['pairs'], 1)

    def test_zero_baseline_and_missing_are_distinct(self):
        frame = pd.DataFrame([
            {'time':'2026-01-01','ihs_id':'A','data_4g_mb':0},
            {'time':'2026-01-02','ihs_id':'A','data_4g_mb':5},
        ])
        result = compare_days(frame)['metrics']
        self.assertEqual(result['data_mb']['previous'], 0)
        self.assertIsNone(result['data_mb']['delta'])
        self.assertIsNone(result['voice_erlang']['current'])
        self.assertIsNone(summarize(pd.DataFrame([{}]))['data_mb'])

    def test_duplicate_records_are_averaged_for_comparisons(self):
        frame = pd.DataFrame([
            {'time':'2026-01-01','ihs_id':'A','data_4g_mb':100},
            {'time':'2026-01-02','ihs_id':'A','data_4g_mb':120},
            {'time':'2026-01-02','ihs_id':'A','data_4g_mb':120},
        ])
        self.assertEqual(compare_days(frame)['metrics']['data_mb']['delta'], 20)
        self.assertEqual(quality(frame)['duplicates'], 1)

    def test_quality_flags_invalid_values_and_age(self):
        frame = pd.DataFrame([
            {'time':'2026-01-01','ihs_id':'A','availability_4g':99},
            {'time':'2026-01-01','ihs_id':'','availability_4g':101},
            {'time':'2026-01-01','ihs_id':None,'availability_4g':None},
        ])
        result = quality(frame, now='2026-01-03')
        self.assertEqual(result['age_days'], 2)
        self.assertEqual(result['invalid_percentages'], 1)
        self.assertEqual(result['missing_site_ids'], 2)
        self.assertEqual(result['percent_completeness'], 33.3)

    def test_no_comparison_without_common_sites_or_dates(self):
        self.assertFalse(compare_days(pd.DataFrame())['available'])
        frame = pd.DataFrame([{'time':'2026-01-01','ihs_id':'A'}, {'time':'2026-01-02','ihs_id':'B'}])
        self.assertFalse(compare_days(frame)['available'])
        self.assertFalse(compare_days(frame.head(1))['available'])

    def test_investigation_rules_use_latest_date_and_ignore_invalid(self):
        frame = pd.DataFrame([
            {'time':'2026-01-01','ihs_id':'OLD','availability_4g':20},
            {'time':'2026-01-02','ihs_id':'CRITICAL','availability_4g':94},
            {'time':'2026-01-02','ihs_id':'WATCH','availability_4g':98},
            {'time':'2026-01-02','ihs_id':'HEALTHY','availability_4g':100},
            {'time':'2026-01-02','ihs_id':'INVALID','availability_4g':-1},
        ])
        result = exceptions(frame)
        self.assertEqual(result['Site'].tolist(), ['CRITICAL','WATCH'])
        self.assertEqual(result['Priority'].tolist(), ['P1','P2'])

    def test_traffic_not_interpreted_as_service_quality(self):
        # Measurements are pure volumes; consumers receive a percentage change,
        # not an invented health score or status.
        frame = pd.DataFrame([
            {'time':'2026-01-01','ihs_id':'A','data_4g_mb':100},
            {'time':'2026-01-02','ihs_id':'A','data_4g_mb':50},
        ])
        self.assertEqual(compare_days(frame)['metrics']['data_mb']['delta'], -50)

if __name__ == '__main__':
    unittest.main()
