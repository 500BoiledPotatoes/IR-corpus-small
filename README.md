# COMP3009J Information Retrieval
## BM25 Search Engine for both small and large corpus
### Functions
* Implemented BM25 model for query and Precision, Recall, Precision@10, R-Precision, MAP, b_pref for evaluation.
* Automatically build and dump the index to a file, no need to read the whole dataset a second time.

### Instructions
I have implemented both querying and evaluation of the small and large corpus, and have two separate programs to handle them each.
#### Small corpus
##### Project structure
Please copy the `search-small-corpus.py` and `evaluate_small_corpus.py`to the small corpus folder.
The structure of the small corpus should be as follows

```
COMP3009J-corpus-small/
├──documents/
├──files/
│  ├── porter.py
│  ├── qrels.txt
│  ├── queries.txt
│  ├── sample_output.txt
│  ├── stopwords.txt
├──search-small-corpus.py
├──evaluate_small_corpus.py
```

after running this program the index.txt and output.txt should be generated.

```
COMP3009J-corpus-small/
├──documents/
├──files/
│  ├── porter.py
│  ├── qrels.txt
│  ├── queries.txt
│  ├── sample_output.txt
│  ├── stopwords.txt
├──index.txt
├──output.txt
├──search-small-corpus.py
├──evaluate_small_corpus.py
```
##### How to run
In the terminal, type the following commands in turn.\
Access to the small corpus folder:
```
cd COMP3009J-corpus-small
```
Select the appropriate mode by using command line arguments:
```
 python search_small_corpus.py -m interactive
```
Or for automatic mode:
```
python search_small_corpus.py -m automatic
```
Evaluation of query results:
```
python evaluate_small_corpus.py
```
#### Large corpus
##### Project structure
Please copy the `search-large-corpus.py` and `evaluate_large_corpus.py`to the large corpus folder.
The structure of the large corpus should be as follows

```
comp3009j-corpus-large/
├──documents/
├──files/
│  ├── porter.py
│  ├── qrels.txt
│  ├── queries.txt
│  ├── sample_output.txt
│  ├── stopwords.txt
├──search-large-corpus.py
├──evaluate_large_corpus.py
```

after running this program the index.txt and output.txt should be generated.

```
COMP3009J-corpus-small/
├──documents/
├──files/
│  ├── porter.py
│  ├── qrels.txt
│  ├── queries.txt
│  ├── sample_output.txt
│  ├── stopwords.txt
├──index.txt
├──output.txt
├──search-large-corpus.py
├──evaluate_large_corpus.py
```
##### How to run
In the terminal, type the following commands in turn.\
Access to the small corpus folder:
```
cd comp3009j-corpus-large
```
Select the appropriate mode by using command line arguments:
```
python search_large_corpus.py -m interactive
```
Or for automatic mode:
```
python search_large_corpus.py -m automatic
```
Evaluation of query results:
```
python evaluate_large_corpus.py
```

### Output results
* The index file is saved in `index.txt`
* The query result for automatic mode is saved in `output.txt`
* The query result of the interactive mode is output on the `terminal`
* Evaluation results are output at the `terminal`
