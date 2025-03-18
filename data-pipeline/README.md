# Pliny Data Pipeline
This is the data pipeline used in Pliny to ingest metadata from Wikipedia data sources, and to extract trends from this data. Although this was used to create Pliny, it was designed to be entirely independent and can thus be used in a standalone manner.
The entry point of the data pipeline is the file `main.py`; you can view details about how to run it with `python3 main.py --help`

## Supported data sources
 When running, you can specify both data sources and data sinks, depending on your use case.

Currently, the following data sources are supported:
* Analytics API - Page names: A wrapper for [this API](https://en.wikipedia.org/w/api.php) with the `allpages` action. This fetches the names of all pages iteratively from the API, accessible through the `PageNameWikiMediaAPI(PageNameDataSource)` class and `--ingest-name-source api` command line argument.
* Data Dump - Page names: A wrapper for [these data dumps](https://dumps.wikimedia.org/other/pageview_complete/) that automatically downloads the required dump for a day, parses it, and allows easy iteration through all page names for a day. Accessible through the `PageNameDumpFile(PageNameDataSource)` class and `--ingest-name-source dump` arg.
* Analytics API - View Count: A wrapper for [this endpoint](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html#get-number-of-page-views-for-a-page), accessible through the `PageViewAPI(PageViewDataSource)` class and `--ingest-view-source api` arg.
* Data Dump - Daily Views: A wrapper for [these data dumps](https://dumps.wikimedia.org/other/pageview_complete/) that automatically downloads the required dump for a day, parses it, and allows easy O(1) access for any page's view count. Accessible through the `PageViewDumpFile(PageViewDataSource)` class and `--ingest-view-source dump` arg.
* MediaWiki API - Edit Data: A wrapper for [this API](https://en.wikipedia.org/w/api.php) with the `revision` action. This fetches and aggregates edit data for a page on a particular day. This is accessible through the `PageRevisionAPI(PageRevisionDataSource)` class and `--ingest-edit-source api` arg.
* Monthly Revision Dump - Edit Data: A wrapper for [these data dumps](https://dumps.wikimedia.org/other/mediawiki_history/) that automatically downloads the required dump for a month, parses it, and allows easy O(1) access for any page's edit data. This is accessible through the `PageRevisionMonthlyDumpFile(PageRevisionDataSource)` class and `--ingest-edit-source dump_monthly` arg.
* Daily Revision Dump - Edit Data: A wrapper for [these data dumps](https://dumps.wikimedia.org/other/incr/enwiki) that automatically downloads the dump for a day, parses it, and allows O(1) access. This is accessible through the `PageRevisionDailyDumpFile(PageRevisionDataSource)` class and `--ingest-edit-source dump_daily` arg.

Each of these can be used independently of eachother based on the use case/data you want.

Currenty, there is only one data sink to write this data to BigQuery. However, if you need additional data sinks (such as writing to a CSV file), it's very easy. The data is internally stored in `IntermediateTableRow[]`, so all that is required is a new class that can take in rows of this data and write it out somewhere.

## Architecture diagram
The architecture of the data pipeline can be visualized as follows:
<img width="724" alt="image" src="https://github.com/user-attachments/assets/a91cfc25-65f0-4407-ad02-bb89aa4f43be" />
