## Historical Swiss film magazines

> The Swiss National Library digitalised several Swiss film magazines from the period before 1945 in two phases, with the technical support of the Department of Film Studies at the Universität Zürich.
>
> Today, they are freely accessible on the e-periodica journal portal of the [ETH-Bibliothek](https://www.e-periodica.ch/). The two digitization projects _Kinema_ and _Historical Swiss Film Magazines_ were realized between 2010-2011 and 2015-2018.

source: [Digitalisierte historische Filmzeitschriften aus der Schweiz (1913–1944)](http://www.film.uzh.ch/d/bibliothek/zeitschriften/historical.html)

### Data

* Journal volumes: [journal_volumes.csv]()
* Journal issues: [journal_issues.csv]()

I compiled this data via the following steps:
1. Retrieved volume-level data and wrote results out to `journal_volumes.csv`
  ```bash
  python3 journal_volumes.py
  ```
2. Used the data in `journal_volumes.csv` to retrieve individual issue info and write it out to `journal_issues.csv`
  ```bash
  python3 journal_issues.py
  ```
3. Resorted the CSVs in Libre Excel.

This could really have been one Python script (there's a some repetition between the two), it worked out this way because I did it in two stages.
