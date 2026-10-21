import ast
import os
from pathlib import Path
import socket
from types import SimpleNamespace
import unittest
from unittest.mock import patch


def classes():
    baseline = os.environ.get('MOCK_BASELINE_SOURCE')
    source = Path(baseline or 'app.py').read_text()
    tree = ast.parse(source)
    from mock_agents import BaseLLMAgent, profit_estimate
    namespace = {'BaseLLMAgent': BaseLLMAgent, 'profit_estimate': profit_estimate,
                 'st': SimpleNamespace(info=lambda _: None), 'time': SimpleNamespace(sleep=lambda _: None)}
    nodes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<offline-class-methods>', 'exec'), namespace)
    return namespace


class CompatibilityRegressions(unittest.TestCase):
    def test_helper_must_disclose_mock_and_never_echo_input(self):
        agent = classes()['BaseLLMAgent']('synthetic role')
        marker = 'SYNTHETIC_PRIVATE_INPUT'
        with patch.object(socket, 'create_connection', side_effect=AssertionError('network forbidden')):
            response = agent.call_llm(marker, context=marker)
        self.assertIn('[MOCK]', response)
        self.assertNotIn(marker, response)

    def test_report_refuses_invalid_price_before_division(self):
        agent = classes()['DecisionGenerationAgent']()
        for price in [0, -1, float('nan'), float('inf')]:
            with self.subTest(price_type=type(price).__name__):
                with self.assertRaises(ValueError):
                    agent.generate_report('synthetic', [], price)


@unittest.skipIf(os.environ.get('MOCK_BASELINE_SOURCE'), 'New offline helper checks are not old-source baseline evidence.')
class OfflineMathTests(unittest.TestCase):
    def test_fixed_assumptions_are_only_arithmetic(self):
        from mock_agents import profit_estimate
        estimate = profit_estimate(40)
        self.assertAlmostEqual(estimate['margin'], 15.5)
        self.assertAlmostEqual(estimate['margin_rate'], 38.75)

    def test_boolean_and_string_prices_are_rejected(self):
        from mock_agents import profit_estimate
        for value in [True, False, '40', None]:
            with self.assertRaises(ValueError):
                profit_estimate(value)

    def test_report_carries_mock_boundary(self):
        report = classes()['DecisionGenerationAgent']().generate_report('synthetic', [], 40)
        self.assertIn('MOCK', report)
        self.assertIn('不是选品建议', report)


if __name__ == '__main__':
    unittest.main()
