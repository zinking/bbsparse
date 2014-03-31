from django.test import SimpleTestCase
from pageharvest.disqus import *

class DisqusTestCase( SimpleTestCase):
    def setUp(self):
	self.d =  Disqus()

    def test_disqus_can_fetch( self ):
	posts =  self.d.listEditorPosts()
	self.assertTrue( len(posts) > 1 )
