import argparse
import datetime
import importlib

import MySQLdb
import sqlalchemy
from sqlalchemy import insert
from pandas import DataFrame
from Historic_Crypto import HistoricalData
from src.database.dataminer_database import session


def main():
    today = datetime.datetime.utcnow()

    parser = argparse.ArgumentParser(description="sample argument parser")
    parser.add_argument("ticker", nargs='?', default='BTC-USD')
    parser.add_argument("month", nargs='?', default='%02d' % today.month)
    parser.add_argument("day", nargs='?', default='%02d' % today.day)
    parser.add_argument("year", nargs='?', default='%02d' % today.year)
    parser.add_argument("granularity", nargs='?', default=60)
    args = parser.parse_args()

    try:
        module = importlib.import_module('src.models.crypto_pairs.' + args.ticker.lower().replace('-', '_'))
    except:
        exit(1)

    ticker_class = getattr(module, args.ticker.replace('-', '_'))

    for year in range(int(args.year), 2025):
        for month in [args.month]:
            try:
                records: DataFrame = HistoricalData(
                    ticker=args.ticker,
                    granularity=args.granularity,
                    start_date=str(year) + '-' + str(month) + '-01-00-00',
                    end_date=str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '-' + str(today.hour) + '-59').retrieve_data()
            except:
                continue

            for index, row in records.iterrows():
                stmt = (
                    insert(ticker_class).values(
                        timestamp=row.name,
                        low=row['low'],
                        high=row['high'],
                        open=row['open'],
                        close=row['close'],
                        volume=row['volume'])
                )

                try:
                    session.execute(stmt)
                except MySQLdb.IntegrityError:
                    print("already inserted ")
                    print(row)
                except sqlalchemy.exc.IntegrityError:
                    print("already inserted ")
                    print(row)
                finally:
                    session.commit()


if __name__ == '__main__':
    main()
