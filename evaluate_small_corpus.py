def evaluate():
    f = open('files/qrels.txt', encoding='UTF-8')
    f1 = open('output.txt', encoding='UTF-8')
    queries = set()
    qrels = {}
    '''
    Set up dictionary to store relevant judgements:
    key: Query id
    value is a dictionary:
        key: Doc id
        value: relevant level of document
    '''
    for line in f:
        temp = {}
        if line.strip().split(' ')[0] not in qrels:
            qrels[line.strip().split(' ')[0]] = temp
        if line.strip().split(' ')[0] in qrels:
            qrels[line.strip().split(' ')[0]][line.strip().split(' ')[2]] = line.strip().split(' ')[3]
    index = {}
    '''
    Set up dictionary to store relevant judgements:
    key: Query id
    value is a dictionary:
        key: Doc id
        value: Relevant level of document
    '''
    for line in f1:
        temp = {}
        if line.strip().split(' ')[0] not in index:
            index[line.strip().split(' ')[0]] = temp
        if line.strip().split(' ')[0] in index:
            index[line.strip().split(' ')[0]][line.strip().split(' ')[1]] = line.strip().split(' ')[2]
        queries.add(line.strip().split(' ')[0])
    precision = 0
    # precision = RelRet/Ret
    recall = 0
    # recall = RelRet/Rel
    precision10 = 0
    # P@10 = RelRet/Ret of the top 10 relevant documents for this query
    Rprecision = 0
    # R-precision = RelRet/Ret of the number R of relevant documents for this query
    '''
    Precision and Recall
    '''
    for qid in index:
        relret = {}
        for did in index[qid].keys():
            ret = len(index[qid].keys())
            # The number of relevant documents for the query
            rel = len(qrels[qid].keys())
            # The number of retrieved documents for the query
            if did in qrels[qid].keys():
                relret[len(relret)] = did
                # The number of relevant documents in the retrieved set
        precision = (len(relret) / ret) + precision
        # Total precision
        recall = (len(relret) / rel) + recall
        # Total recall
    '''
    R-precision
    '''
    for qid in index:
        relretR = {}
        for did in dict_slice(index[qid], 0, count_rel(qrels[qid])).keys():
            # Slice dictionaries that store query results according to the number of relevant documents
            # count_rel(qrels[qid]) is the number of relevant documents
            # dict_slice(index[qid], 0, count_rel(qrels[qid])) return the sliced dictionary
            if did in qrels[qid].keys():
                relretR[len(relretR)] = did
        Rprecision = (len(relretR) / len(dict_slice(index[qid], 0, count_rel(qrels[qid])).keys())) + Rprecision
        # Total R-precision
    '''
    P@10
    '''
    for qid in index:
        relret10 = {}
        for did in dict_slice(index[qid], 0, 10).keys():
            # Slice dictionaries that store query results
            # dict_slice(index[qid], 0, 10) return the sliced dictionary
            if did in qrels[qid].keys():
                relret10[len(relret10)] = did
        precision10 = (len(relret10) / len(dict_slice(index, 0, 10))) + precision10
        # Total P@10
    '''
    MAP
    '''
    total_map = 0
    for qid in index:
        map = 0
        # map = Number of related documents up to this document / Number of documents up to this document
        relretM = {}
        for did in index[qid].keys():
            if did in qrels[qid].keys():
                relretM[len(relretM)] = did
                map = len(relretM) / int(index[qid][did]) + map
        total_map = total_map + map / len(qrels[qid])
        # Total map
    '''
    Bpref
    Small corpus does not have unjudged documents
    '''
    total_bpref = 0
    for qid in index:
        n = 0
        bpref = 0
        # Bref  = 1 / R (1 - n ranked higher than r / R) + Bref
        # n is a member of the first R judged non-relevant document
        for did in index[qid].keys():
            if did in qrels[qid].keys():
                # Relevant doc
                if (n / len(qrels[qid])) > 1:
                    bpref = 0 + bpref
                    # (1 - n ranked higher than r / R) can't be less than 0
                else:
                    bpref = (1 - n / len(qrels[qid])) + bpref
                    # calculate (1 - n ranked higher than r / R)

            else:
                # non-relevant document
                n = n + 1
                # n + 1
        total_bpref = bpref / len(qrels[qid]) + total_bpref
        # Calculate total bpref

    avg_precision = precision / len(qrels)
    avg_recall = recall / len(qrels)
    avg_precision10 = precision10 / len(qrels)
    avg_Rprecision = Rprecision / len(qrels)
    avg_map = total_map / len(qrels)
    avg_bpref = total_bpref / len(qrels)
    print("Evaluation results:")
    print(f'Precision    {avg_precision}')
    print(f'Recall       {avg_recall}')
    print(f'Precision@10 {avg_precision10}')
    print(f'R-Precision  {avg_Rprecision}')
    print(f'MAP          {avg_map}')
    print(f'B_pref       {avg_bpref}')
    # Calculate the average of all

def dict_slice(dict, start, end):
    '''
    slice dict
    dict: Target dictionaries
    start: start position
    end: end position
    '''
    keys = dict.keys()
    dict_slice = {}
    for k in list(keys)[start:end]:
        dict_slice[k] = dict[k]
    return dict_slice
    # Return sliced dict


def count_rel(dict1):
    # Calculate number of relevant doc
    count = 0
    for doc_id in dict1:
        if dict1[doc_id] != 0:
            count += 1
    return count

evaluate()
