# twitter-airflow-data-engineering-project

## Optional Xquik Export Source

The Airflow ETL keeps the existing Tweepy flow by default. To replay a Xquik
tweet export instead, set `XQUIK_EXPORT_PATH` to a JSON, JSONL, or CSV file
before running the DAG task:

```bash
XQUIK_EXPORT_PATH=exports/tweets.json python twitter_etl.py
```

`twitter_etl.py` writes `refined_tweets.csv` by default. Set `X_OUTPUT_PATH` to
choose another destination.

The default Tweepy path now reads credentials from environment variables:

```bash
TWITTER_ACCESS_KEY=... TWITTER_ACCESS_SECRET=... TWITTER_CONSUMER_KEY=... TWITTER_CONSUMER_SECRET=...
```
