from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)

    def test_keyword_to_titles(self):
        dummy_metadata = [['a', 1, 2, 3, ['ball', 'apple']], ['b', 1, 2, 3, ['dog', 'cat']]]
        expected_keyword_to_titles_results = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b'],
            'cat': ['b']
            }
        self.assertEqual(keyword_to_titles(dummy_metadata), expected_keyword_to_titles_results)
        dummy_metadata_1 = [['a', 1, 2, 3, ['ball', 'apple']], ['b', 1, 2, 3, ['dog', 'cat']], ['c', 1, 2, 3, ['do', 'cat']], ['d', 1, 2, 3, ['dog', 'cat']]]
        expected_keyword_to_titles_results_repeats = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b', 'd'],
            'do': ['c'],
            'cat': ['b', 'c', 'd']
            }
        self.assertEqual(keyword_to_titles(dummy_metadata_1), expected_keyword_to_titles_results_repeats)
        dummy_metadata_1 = []
        expected_keyword_to_titles_results_empty = {}
        self.assertEqual(keyword_to_titles(dummy_metadata_1), expected_keyword_to_titles_results_empty)
        dummy_metadata = [['a', 1, 2, 3, ['ball', 'DoG']], ['b', 5, 2, 3, ['dog', 'cat']]]
        expected_keyword_to_titles_results_case_sensitivity = {
            'ball': ['a'],
            'DoG': ['a'],
            'dog': ['b'],
            'cat': ['b']
            }
        self.assertEqual(keyword_to_titles(dummy_metadata), expected_keyword_to_titles_results_case_sensitivity)

    def test_title_to_info(self):
        dummy_metadata = [['a', 1, 2, 3, ['ball', 'apple']], ['b', 4, 5, 6, ['dog', 'cat']]]
        expected_title_to_info_results = {
            'a': {'author': 1, 'timestamp': 2, 'length': 3},
            'b': {'author': 4, 'timestamp': 5, 'length': 6}
            }
        self.assertEqual(title_to_info(dummy_metadata), expected_title_to_info_results)
        dummy_metadata_1 = [['a', 1, 2, 3, ['ball', 'apple']], ['b', 5, 4, 3, ['dog', 'cat']], ['c', 1, 4, 8, ['do', 'cat']]]
        expected_title_to_info_results_repeat_info = {
            'a': {'author': 1, 'timestamp': 2, 'length': 3},
            'b': {'author': 5, 'timestamp': 4, 'length': 3},
            'c': {'author': 1, 'timestamp': 4, 'length': 8}
            }
        self.assertEqual(title_to_info(dummy_metadata_1), expected_title_to_info_results_repeat_info)
        dummy_metadata_1 = []
        expected_title_to_info_results_empty = {}
        self.assertEqual(title_to_info(dummy_metadata_1), expected_title_to_info_results_empty)
        dummy_metadata = [['a', 1, 2, 3, ['ball', 'apple']], ['b', 4, 5, 6, ['dog', 'cat']], ['A', 9, 5, 3, ['ball', 'apple']]]
        expected_title_to_info_results_case_sensitivity = {
            'a': {'author': 1, 'timestamp': 2, 'length': 3},
            'b': {'author': 4, 'timestamp': 5, 'length': 6},
            'A': {'author': 9, 'timestamp': 5, 'length': 3}
            }
        self.assertEqual(title_to_info(dummy_metadata), expected_title_to_info_results_case_sensitivity)

    def test_search(self):
        dummy_metadata = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b', 'd'],
            'do': ['c'],
            'cat': ['b', 'c', 'd']
        }
        expected_search_results = ['b', 'c', 'd']
        self.assertEqual(search('cat', dummy_metadata), expected_search_results)
        dummy_metadata = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b', 'd'],
            'do': ['c'],
            'cat': ['b', 'c', 'd']
        }
        expected_search_results_case_sensitive = []
        self.assertEqual(search('Cat', dummy_metadata), expected_search_results_case_sensitive)
        dummy_metadata = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b', 'd'],
            'do': ['c'],
            'cat': ['b', 'c', 'd']
        }
        expected_search_results_substring = []
        self.assertEqual(search('ba', dummy_metadata), expected_search_results_substring)
        dummy_metadata = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b', 'd'],
            'do': ['c'],
            'cat': ['b', 'c', 'd']
        }
        expected_search_results_empty = []
        self.assertEqual(search('', dummy_metadata), expected_search_results_empty)

    def test_article_length(self):
        article_titles = ['a', 'b', 'A']
        title_to_inf = {
            'a': {'author': 1, 'timestamp': 2, 'length': 2},
            'b': {'author': 4, 'timestamp': 5, 'length': 6},
            'A': {'author': 9, 'timestamp': 5, 'length': 3}
            }
        expected_article_length_results = ['a', 'A']
        self.assertEqual(article_length(3, article_titles, title_to_inf), expected_article_length_results)
        article_titles = ['a', 'b', 'A']
        title_to_inf = {
            'a': {'author': 1, 'timestamp': 2, 'length': 3},
            'b': {'author': 4, 'timestamp': 5, 'length': 6},
            'A': {'author': 9, 'timestamp': 5, 'length': 3}
            }
        expected_article_length_filters_none = ['a', 'b', 'A']
        self.assertEqual(article_length(9, article_titles, title_to_inf), expected_article_length_filters_none)
        article_titles = ['a', 'b', 'A']
        title_to_inf = {
            'a': {'author': 1, 'timestamp': 2, 'length': 3},
            'b': {'author': 4, 'timestamp': 5, 'length': 6},
            'A': {'author': 9, 'timestamp': 5, 'length': 3}
            }
        expected_article_length_filters_all = []
        self.assertEqual(article_length(0, article_titles, title_to_inf), expected_article_length_filters_all)
        article_titles = []
        title_to_inf = {}
        expected_article_length_results_empty = []
        self.assertEqual(article_length(6, article_titles, title_to_inf), expected_article_length_results_empty)

    def test_key_by_author(self):
        article_titles = ['a', 'b', 'A']
        title_to_inf = {
            'a': {'author': 1, 'timestamp': 2, 'length': 2},
            'b': {'author': 4, 'timestamp': 5, 'length': 6},
            'A': {'author': 1, 'timestamp': 5, 'length': 3}
            }
        expected_key_by_author_results = {
            1: ['a', 'A'],
            4: ['b']
            }
        self.assertEqual(key_by_author(article_titles, title_to_inf), expected_key_by_author_results)
        article_titles = ['a', 'b', 'A']
        title_to_inf = {
            'a': {'author': 'Ben', 'timestamp': 2, 'length': 3},
            'b': {'author': 'Nevel', 'timestamp': 5, 'length': 6},
            'A': {'author': 'ben', 'timestamp': 5, 'length': 3}
            }
        expected_key_by_author_case_sensitive = {
            'Ben': ['a'],
            'Nevel': ['b'],
            'ben': ['A']
            }
        self.assertEqual(key_by_author(article_titles, title_to_inf), expected_key_by_author_case_sensitive)
        article_titles = []
        title_to_inf = {}
        expected_key_by_author_case_empty = {}
        self.assertEqual(key_by_author(article_titles, title_to_inf), expected_key_by_author_case_empty)

    def test_filter_to_author(self):
        article_titles = ['a', 'b', 'A', 'm']
        title_to_inf = {
            'a': {'author': 'Ben', 'timestamp': 2, 'length': 3},
            'b': {'author': 'Nevel', 'timestamp': 5, 'length': 6},
            'A': {'author': 'ben', 'timestamp': 5, 'length': 3},
            'm': {'author': 'ben', 'timestamp': 8, 'length': 10}
            }
        expected_filter_to_author_results = ['A', 'm']
        self.assertEqual(filter_to_author('ben', article_titles, title_to_inf), expected_filter_to_author_results)
        article_titles = ['a', 'b', 'A', 'm']
        title_to_inf = {
            'a': {'author': 'Ben', 'timestamp': 2, 'length': 3},
            'b': {'author': 'Nevel', 'timestamp': 5, 'length': 6},
            'A': {'author': 'ben', 'timestamp': 5, 'length': 3},
            'm': {'author': 'ben', 'timestamp': 8, 'length': 10}
            }
        expected_filter_to_author_filters_none = []
        self.assertEqual(filter_to_author('Chris', article_titles, title_to_inf), expected_filter_to_author_filters_none)
        article_titles = []
        title_to_inf = {}
        expected_filter_to_author_empty = []
        self.assertEqual(filter_to_author('Chris', article_titles, title_to_inf), expected_filter_to_author_empty)

    def test_filter_out(self):
        article_titles = ['a', 'b', 'c']
        keyword_to_title = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b', 'd'],
            'do': ['c'],
            'cat': ['b', 'c', 'd']
        }
        expected_filter_out_results = ['a', 'c']
        self.assertEqual(filter_out('dog', article_titles, keyword_to_title), expected_filter_out_results)
        article_titles = ['a', 'b', 'c']
        keyword_to_title = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b', 'd'],
            'do': ['c'],
            'cat': ['b', 'c', 'd']
        }
        expected_filter_out_no_match = ['a', 'b', 'c']
        self.assertEqual(filter_out('blue', article_titles, keyword_to_title), expected_filter_out_no_match)
        article_titles = ['a', 'b', 'c']
        keyword_to_title = {
            'ball': ['a'],
            'apple': ['a'],
            'dog': ['b', 'd', 'c', 'a'],
            'do': ['c'],
            'cat': ['b', 'c', 'd']
        }
        expected_filter_out_filters_all = []
        self.assertEqual(filter_out('dog', article_titles, keyword_to_title), expected_filter_out_filters_all)
        article_titles = []
        title_to_inf = {}
        expected_filter_out_results_empty = []
        self.assertEqual(filter_out('car', article_titles, title_to_inf), expected_filter_out_results_empty)

    def test_articles_from_year(self):
        article_titles = ['a', 'b', 'A', 'm']
        title_to_inf = {
            'a': {'author': 'Ben', 'timestamp': 1334671200.0, 'length': 3},
            'b': {'author': 'Nevel', 'timestamp': 1329483600.0, 'length': 6},
            'A': {'author': 'ben', 'timestamp': 1434549600.0, 'length': 3},
            'm': {'author': 'ben', 'timestamp': 1442498400.0, 'length': 10}
            }
        expected_articles_from_year_results = ['a', 'b']
        self.assertEqual(articles_from_year(2012, article_titles, title_to_inf), expected_articles_from_year_results)
        article_titles = ['a', 'b', 'A', 'm']
        title_to_inf = {
            'a': {'author': 'Ben', 'timestamp': 1334671200.0, 'length': 3},
            'b': {'author': 'Nevel', 'timestamp': 1329483600.0, 'length': 6},
            'A': {'author': 'ben', 'timestamp': 1434549600.0, 'length': 3},
            'm': {'author': 'ben', 'timestamp': 1442498400.0, 'length': 10}
            }
        expected_articles_from_year_filters_all = []
        self.assertEqual(articles_from_year(2011, article_titles, title_to_inf), expected_articles_from_year_filters_all)
        article_titles = []
        title_to_inf = {}
        expected_articles_from_year_empty = []
        self.assertEqual(articles_from_year(2012, article_titles, title_to_inf), expected_articles_from_year_empty)


    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_search_integration_test(self, input_mock):
        keyword = 'dog'
        advanced_option = 6

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: ['Black dog (ghost)', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', 'Sun dog']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_article_length_integration_test(self, input_mock):
        keyword = 'music'
        advanced_option = 1
        advanced_response = 5000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Kevin Cadogan', 'Tim Arnold (musician)', 'List of gospel musicians', 'Texture (music)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_key_by_author_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 2

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: {'jack johnson': ['Spain national beach soccer team'], 'Burna Boy': ['Will Johnson (soccer)'], 'Mack Johnson': ['Steven Cohen (soccer)']}\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_filter_to_author_integration_test(self, input_mock):
        keyword = 'music'
        advanced_option = 3
        advanced_response = 'jack johnson'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Noise (music)', '1986 in music', 'Tim Arnold (musician)', 'David Gray (musician)', 'Alex Turner (musician)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_filter_out_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 4
        advanced_response = 'jack'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Will Johnson (soccer)', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)



# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
