# coding=utf-8
"""
This module contains sampling related routines
"""
import os

from random import randint
import math
import logging
import random
import pandas as pd
import pyprind
from magellan.utils.generic_helper import get_install_path
import magellan.catalog.catalog_manager as cm

logger = logging.getLogger(__name__)


def _get_stop_words():
    stop_words_set = set()
    install_path = get_install_path()
    dataset_path = os.sep.join([install_path, 'utils'])
    stop_words_file = os.sep.join([dataset_path, 'stop_words.txt'])
    with open(stop_words_file, "rb") as stopwords_file:
        for stop_words in stopwords_file:
            stop_words_set.add(stop_words.rstrip())

    return stop_words_set


# get string column list
def _get_str_cols_list(table):
    if len(table) == 0:
        logger.error('_get_str_cols_list: Size of the input table is 0')
        raise AssertionError('_get_str_cols_list: Size of the input table is 0')

    cols = list(table.columns[table.dtypes == object])
    col_list = []
    for attr_x in cols:
        col_list.append(table.columns.get_loc(attr_x))

    return col_list


# create inverted index from token to position
def _inv_index(table):
    """

    This is inverted index function that builds inverted index of tokens on a table

    """

    # Get the stop words listed by user in the file specified by dataset path
    stop_words = _get_stop_words()

    # Extract indices of all string columns (if any) from the input DataFrame
    str_cols_ix = _get_str_cols_list(table)

    inv_index = dict()
    pos = 0

    # For each row in the DataFrame of the input table, we will fetch all string values from string column indices
    # and will concatenate them. Next step would be to tokenize them using set and remove all the stop words
    # from the list of tokens. Once we have the list of tokens, we will iterate through the list of tokens
    # to identify its position and will create an inverted index.
    for row in table.itertuples(index=False):
        str_val = ''
        for list_item in str_cols_ix:
            str_val += str(row[list_item]).lower() + ' '
        str_val = str_val.rstrip()

        # tokenize them
        str_val = set(str_val.split())
        str_val = str_val.difference(stop_words)

        # building inverted index I from set of tokens
        for token in str_val:
            lst = inv_index.get(token, None)
            if lst is None:
                inv_index[token] = [pos]
            else:
                lst.append(pos)
        pos += 1
    return inv_index


def _probe_index(table_b, y_param, s_tbl_sz, s_inv_index):
    """
    This is probe index function that probes the second table into inverted index to get
    good coverage in the down sampled output

    """

    y_pos = math.floor(y_param / 2)
    h_table = set()
    stop_words = _get_stop_words()
    str_cols_ix = _get_str_cols_list(table_b)

    # Progress Bar
    bar = pyprind.ProgBar(len(table_b))

    # For each tuple x ∈ B', we will probe inverted index I built in the previous step to find all tuples in A
    # (inverted index) that share tokens with x. We will rank these tuples in decreasing order of shared tokens, then
    # take (up to) the top k/2 tuples to be the set P.

    for row in table_b.itertuples(index=False):
        bar.update()
        str_val = ''

        # For all string column in the table, fetch all string values and concatenate them
        for list_ix in str_cols_ix:
            str_val += str(row[list_ix]).lower() + ' '
        str_val = str_val.rstrip()

        # Tokenizing the string value and removing stop words before we start probing into inverted index I
        str_val = set(str_val.split())
        str_val = str_val.difference(stop_words)

        # For each token in the set, we will probe the token into inverted index I to get set of y/2 positive matches
        match = set()
        for token in str_val:
            ids = s_inv_index.get(token, None)
            if ids is not None:
                match.update(ids)

        # Pick y/2 elements from match
        k = min(y_pos, len(match))
        match = list(match)
        smpl_pos_neg = set()

        while len(smpl_pos_neg) < k:
            num = random.choice(match)
            smpl_pos_neg.add(num)

        # Remaining y_param/2 items are selected here randomly. This is to get better coverage from both the input
        # tables
        while len(smpl_pos_neg) < y_param:
            rand_item_num = randint(0, s_tbl_sz - 1)
            smpl_pos_neg.add(rand_item_num)
        h_table.update(smpl_pos_neg)

    return h_table


# down sample of two tables : based on sanjib's index based solution
def down_sample(table_a, table_b, size, y_param):
    """
    This is down sample table function that down samples 2 tables A and B. First it randomly selects size tuples
    from the table B to be table B'. First step is to build an inverted index (token, tuple_id) on table A - say I.
    For each tuple x ∈ B', the algorithm finds a set P of k/2 tuples from A (inverted index) that match x,
    and a set Q of k/2 tuples randomly selected from A \ P. The idea is for A' and B' to share some matches yet be
    as representative of A and B as possible.

    Args:
        table_a (DataFrame): input table A
        table_b (DataFrame): input table B
        size (int): down_sampled size of table B
        y_param (int): down_sampled size of table A should be close to size * y_param

    Returns:
        down sampled tables A and B

    Raises:
        AssertionError :
        1) If any of the input tables are empty or not a DataFrame
        2) If size or y parameter is empty or 0 or not a valid integer value
        3) If output sampled tables are empty or not as per user defined

    Example:
        C, D = mg.down_sample(A, B, b_size, y_param)

    """

    if not isinstance(table_a, pd.DataFrame):
        logger.error('Input table A is not of type pandas DataFrame')
        raise AssertionError('Input table A is not of type pandas DataFrame')

    if not isinstance(table_b, pd.DataFrame):
        logger.error('Input table B is not of type pandas DataFrame')
        raise AssertionError('Input table B is not of type pandas DataFrame')

    if len(table_a) == 0 or len(table_b) == 0:
        logger.error('Size of the input table is 0')
        raise AssertionError('Size of the input table is 0')

    if size == 0 or y_param == 0:
        logger.error('size or y cannot be zero (3rd and 4th parameter of downsample)')
        raise AssertionError('size or y_param cannot be zero (3rd and 4th parameter of downsample)')

    if len(table_b) < size:
        logger.warning('Size of table B is less than b_size parameter - using entire table B')

    # Inverted index built on table A will consist of all tuples in such P's and Q's - central idea is to have
    # good coverage in the down sampled A' and B'.
    s_inv_index = _inv_index(table_a)

    # Randomly select size tuples from table B to be B'
    b_sample_size = min(math.floor(size), len(table_b))
    b_tbl_indices = list(pd.np.random.choice(len(table_b), b_sample_size, replace=False))

    # Probe inverted index to find all tuples in A that share tokens with tuples in B'.
    s_tbl_indices = _probe_index(table_b.ix[b_tbl_indices], y_param,
                                 len(table_a), s_inv_index)
    s_tbl_indices = list(s_tbl_indices)
    l_sampled = table_a.iloc[list(s_tbl_indices)]
    r_sampled = table_b.iloc[list(b_tbl_indices)]

    # update catalog
    cm.copy_properties(table_a, l_sampled)
    cm.copy_properties(table_b, r_sampled)

    return l_sampled, r_sampled
