import unittest

import pandas as pd

from pna.dbi import Dbi
from pna.logic import PhillipinesEmbassyLogic


class TestPhillipinesEmbassyLogic(unittest.TestCase):

    def setUp(self):
        self.logic = PhillipinesEmbassyLogic(dbi=Dbi())

    def test_entity_counts(self):
        df = self.logic.entity_counts()
        self.assertIsInstance(df, pd.DataFrame)
        for column in ['Entity', 'Count']:
            self.assertIn(column, df.columns)

    def test_vector_neighbourhood(self):
        df = self.logic.vector_neighbourhood('China')
        self.assertIsInstance(df, pd.DataFrame)
        for column in ['PC1', 'PC2']:
            self.assertIn(column, df.columns)

    def test_liwc_profile(self):
        df = self.logic.liwc_profile('China')
        self.assertIsInstance(df, pd.DataFrame)
        for column in ['Entity', 'Category', 'NPMI']:
            self.assertIn(column, df.columns)

    def test_sentences(self):
        df = self.logic.sentences('China')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('Sentence', df.columns)

    def test_entity_counts_over_time(self):
        df = self.logic.entity_counts_over_time('China')
        self.assertIsInstance(df, pd.DataFrame)
        for column in ['Entity', 'Date', 'Count']:
            self.assertIn(column, df.columns)

    def test_corpus_volume_over_time(self):
        df = self.logic.corpus_volume_over_time()
        self.assertIsInstance(df, pd.DataFrame)
        for column in ['Date', 'Count']:
            self.assertIn(column, df.columns)

    def test_in_vocab(self):
        self.assertTrue(self.logic.in_vocab('China'))
        self.assertFalse(self.logic.in_vocab('Positive Definite Matrix'))
