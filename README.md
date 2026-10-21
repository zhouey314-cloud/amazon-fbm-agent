# Amazon FBM Agent — MOCK / legacy UI experiment

**No real model API is called.** `BaseLLMAgent.call_llm` returns a fixed
`[MOCK]` string and does not analyze its input. VOC examples, strategies and
cost assumptions are synthetic, hard-coded teaching material. No actual
selection accuracy, review frequencies, customers, sales or profitability is
claimed. This is not procurement or investment advice.

## Offline verification (Python 3.11+)

```sh
python3 -m unittest discover -s tests -v
```

The tests import only offline helpers or AST-extracted class methods, never
the Streamlit UI, real CSVs, model clients or a network provider. They cover
the explicit MOCK label, no input leakage/network use, and positive finite
prices before division. These are deterministic checks, not AI evals.

## Optional local demo

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py --server.address 127.0.0.1
```

Use only synthetic CSVs with optional numeric `价格` and `月销量` columns.
Without a CSV, the UI uses the existing three synthetic rows. The profit
illustration assumes sourcing at 25% of price, a fixed 8.50 shipping cost and
15% commission; real duties, returns, taxes, currency conversion and costs
are absent. Invalid zero/negative/non-finite prices are refused.

Dependency pins record the local verification versions, not a transitive
lock or a general security guarantee. Malformed/large CSV handling, real
providers, real-market datasets, model quality, mobile browsers and human
commercial acceptance remain NOT_TESTED. No API key is needed or requested.
Uploaded data, env files and caches are excluded from Git; do not upload
customer data. No upstream license is changed or newly granted here.
