import unittest
import loader

class TestLoader(unittest.TestCase):

    def test_transformLinks(self):
        links = [
            ["All article disambiguation pages","https://en.wikipedia.org/wiki/Category:All_article_disambiguation_pages"],
            ["All disambiguation pages", "https://en.wikipedia.org/wiki/Category:All_disambiguation_pages"],
            ["Disambiguation pages", "https://en.wikipedia.org/wiki/Category:Disambiguation_pages"],
            ["Short description is different from Wikidata", "https://en.wikipedia.org/wiki/Category:Short_description_is_different_from_Wikidata"]
        ]
        linksRealResult = [
            ["All article disambiguation pages","https://en.wikipedia.org/wiki/Category:All_article_disambiguation_pages", 123],
            ["All disambiguation pages", "https://en.wikipedia.org/wiki/Category:All_disambiguation_pages", 123],
            ["Disambiguation pages", "https://en.wikipedia.org/wiki/Category:Disambiguation_pages", 123],
            ["Short description is different from Wikidata", "https://en.wikipedia.org/wiki/Category:Short_description_is_different_from_Wikidata", 123]
        ]
        id = 123
        loader.transformLinks(links, id)
        self.assertEqual(links, linksRealResult)
    
    def test_transformRestrictions(self):
        restrictions = ["edit", "reading"]
        pageTitleKey = "abcdefghijklmnopqrstuvwxyz123456"
        restrictionsRealResult = [
            ["edit", "abcdefghijklmnopqrstuvwxyz123456"],
            ["reading", "abcdefghijklmnopqrstuvwxyz123456"]
        ]
        result = loader.transformRestrictions(restrictions, pageTitleKey)
        self.assertEqual(result, restrictionsRealResult)

if __name__ == '__main__':
    unittest.main()