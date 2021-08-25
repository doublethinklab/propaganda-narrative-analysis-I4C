import json

import pandas as pd

from pna.dbi import Dbi


class Logic:

    def __init__(self, dbi: Dbi):
        self.dbi = dbi

    def entity_counts(self) -> pd.DataFrame:
        raise NotImplementedError

    def vector_neighbourhood(self, anchor: str) -> pd.DataFrame:
        raise NotImplementedError

    def liwc_profile(self, entity: str) -> pd.DataFrame:
        raise NotImplementedError

    def sentences(self, entity: str) -> pd.DataFrame:
        raise NotImplementedError

    def entity_counts_over_time(self, entity: str) -> pd.DataFrame:
        raise NotImplementedError

    def corpus_volume_over_time(self) -> pd.DataFrame:
        raise NotImplementedError

    def in_vocab(self, word: str) -> bool:
        raise NotImplementedError

    def liwc_over_time(self) -> pd.DataFrame:
        raise NotImplementedError


class PhillipinesEmbassyLogic(Logic):

    def __init__(self, dbi: Dbi):
        super().__init__(dbi)
        self.df_entity_counts = pd.read_csv('data/ph_entity_counts.csv')
        self.df_liwc = pd.read_csv('data/ph_npmis.csv')
        with open('data/ph_entity_to_sents.json') as f:
            self.entity_to_sents = json.loads(f.read())
        self.df_entity_attention = pd.read_csv(
            'data/ph_entity_attention_over_time.csv')
        self.df_volume = pd.read_csv('data/ph_tweet_volume.csv')
        self.df_pca = pd.read_csv('data/ph_pca_df.csv')
        with open('data/ph_neighbours.json') as f:
            self.entity_to_neighbours = json.loads(f.read())
        with open('data/ph_vocab.dic') as f:
            self.vocab = json.loads(f.read())
        self.df_liwc_time = pd.read_csv('data/ph_liwc_time.csv')
        self._fix_names()

    def _fix_names(self):
        self.df_entity_counts.rename(
            columns={'entity': 'Entity', 'count': 'Count'},
            inplace=True)
        self.df_liwc.rename(
            columns={'entity': 'Entity', 'cat': 'Category', 'npmi': 'NPMI'},
            inplace=True)
        self.df_entity_attention.rename(
            columns={'entity': 'Entity', 'date': 'Date', 'count': 'Count'},
            inplace=True)
        self.df_volume.rename(
            columns={'date': 'Date', 'tweet': 'Count'},
            inplace=True)
        self.df_pca.rename(
            columns={'pc1': 'PC1', 'pc2': 'PC2'},
            inplace=True)
        self.df_liwc_time.rename(
            columns={
                'date': 'Date',
                'cat': 'Category',
                'count': 'Count',
                'freq': 'Frequency',
                'n': 'Number of Tokens'
            },
            inplace=True)

    def entity_counts(self) -> pd.DataFrame:
        return self.df_entity_counts

    def vector_neighbourhood(self, anchor: str) -> pd.DataFrame:
        neighbours = self.entity_to_neighbours[anchor]
        df = self.df_pca
        df = df[df.token.isin(neighbours + [anchor])]
        return df

    def liwc_profile(self, entity: str) -> pd.DataFrame:
        df = self.df_liwc
        df = df[df.Entity == entity]
        return df

    def sentences(self, entity: str) -> pd.DataFrame:
        sents = self.entity_to_sents[entity]
        df = pd.DataFrame(sents)
        df.date = df.date.apply(lambda x: x.split('T')[0])
        df['Url'] = df['id'].apply(
            lambda x: f'https://twitter.com/chinaembmanila/status/{x}')
        name_map = {
            'date': 'Date',
            'likes': 'Likes',
            'retweets': 'Retweets',
        }
        df.rename(columns=name_map, inplace=True)
        df.drop(columns=['id'], inplace=True)
        df.drop_duplicates(subset='Url', inplace=True)
        return df

    def entity_counts_over_time(self, entity: str) -> pd.DataFrame:
        df = self.df_entity_attention
        df = df[df.Entity == entity].sort_values(by='Date', ascending=True)
        return df

    def corpus_volume_over_time(self) -> pd.DataFrame:
        return self.df_volume

    def in_vocab(self, word: str) -> bool:
        return word in self.entity_to_neighbours

    def liwc_over_time(self) -> pd.DataFrame:
        return self.df_liwc_time
