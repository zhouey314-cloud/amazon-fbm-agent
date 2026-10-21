"""Offline demonstration helpers. No provider client, credentials or network."""
import math


class BaseLLMAgent:
    def __init__(self, role, model='MOCK/no-provider'):
        self.role = role
        self.model = model

    def call_llm(self, prompt, context=''):
        # Input is intentionally unused; this is not a model response or analysis.
        return f'[MOCK] [{self.role}] 固定演示输出；未分析输入，未调用模型或真实市场数据。'


def profit_estimate(avg_price):
    """Illustrate fixed assumptions, never a verified profitability estimate."""
    if isinstance(avg_price, bool) or not isinstance(avg_price, (int, float)):
        raise ValueError('MOCK price must be a positive finite number.')
    if not math.isfinite(avg_price) or avg_price <= 0:
        raise ValueError('MOCK price must be a positive finite number.')
    sourcing_cost = avg_price * 0.25
    shipping_cost = 8.50
    margin = avg_price - sourcing_cost - shipping_cost - avg_price * 0.15
    return {'margin': margin, 'margin_rate': margin / avg_price * 100}
