import unittest

from pna.dbi import NarrativeRepository, NarrativeLabelRepository


class TestNarrativeRepository(unittest.TestCase):

    def test_all(self):
        repo = NarrativeRepository()
        repo.create(code='n1', description='Democracy is failing')
        repo.create(code='n2', description="China's rise is inevitable")
        narratives = repo.all()
        # could have other data inserted by tests, just check these two
        codes = list(narratives.code.unique())
        for code in ['n1', 'n2']:
            self.assertIn(code, codes)

    def test_create(self):
        repo = NarrativeRepository()
        repo.create(code='n3', description='Sinovac works')
        narratives = repo.all()
        codes = list(narratives.code.unique())
        self.assertIn('n3', codes)

    def test_delete(self):
        repo = NarrativeRepository()
        repo.create(code='n4', description='China is your friend')
        narratives = repo.all()
        codes = list(narratives.code.unique())
        self.assertIn('n3', codes)
        repo.delete('n4')
        narratives = repo.all()
        codes = list(narratives.code.unique())
        self.assertNotIn('n4', codes)


class TestNarrativeLabelRepository(unittest.TestCase):

    def setUp(self):
        repo = NarrativeRepository()
        repo.create(code='c1', description='Democracy is failing')
        repo.create(code='c2', description="China's rise is inevitable")

    def test_all(self):
        repo = NarrativeLabelRepository()
        repo.create(narrative_code='c1', annotator='Tim', text='Whatever')
        repo.create(narrative_code='c2', annotator='Tim', text='Something')
        annotations = repo.all()
        self.assertEqual(2, len(annotations))
        self.assertEqual(['c1', 'c2'],
                         list(annotations.narrative_code.unique()))
        self.assertIn('description', annotations.columns)

    def test_create(self):
        pass  # tested in all

    def test_delete(self):
        repo = NarrativeLabelRepository()
        repo.create(narrative_code='c2', annotator='Tim', text='Pfft')
        annotations = repo.all()
        self.assertIn('Pfft', annotations.text.unique())
        repo.delete(narrative_code='c2', annotator='Tim', text='Pfft')
        annotations = repo.all()
        self.assertNotIn('Pfft', annotations.text.unique())
