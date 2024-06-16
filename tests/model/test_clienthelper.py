from unittest.mock import patch, MagicMock # for replacing 'input()' with a function that returns a value 
import pytest

from ..fixtures import clienthelper


def test_singleton_instance(clienthelper):
    # test that the singleton instance is created
    assert clienthelper is not None


def test_yes_no_loop(clienthelper):
    # test that the function returns "yes" or "no"

    # replacing 'input()' with a function that returns "yes"
    with patch('builtins.input', return_value="yes"):
        assert clienthelper.yes_no_loop() == "yes"

    # replacing 'input()' with a function that first returns "invalid" and then "no"
    input = MagicMock(side_effect=["invalid", "no"]) # to test that the function asks for a valid option
    with patch('builtins.input', new=input):
        assert clienthelper.yes_no_loop() == "no"
    

def test_print_menu_get_answer(clienthelper):
    # test that the function returns a valid option using a example string:
    options_str = '{"1": "option1", "2": "option2", "3": "option3"}'
    
    # replacing 'input()' with a function that returns "1"
    with patch('builtins.input', return_value="1"): 
        assert clienthelper.print_menu_get_answer(options_str) == "1" 
    
    # replacing 'input()' with a function that first returns "invalid" and then "2"
    input = MagicMock(side_effect=["invalid", "2"]) # to test that the function asks for a valid option
    with patch('builtins.input', new=input):
        assert clienthelper.print_menu_get_answer(options_str) == "2"


def test_print_list(clienthelper):
    # test that the function prints all list items in a string
    list_str = "item1, item2, item3"
    
    # replacing 'print()' with a function that appends the printed string to a list
    printed = [] # start with an empty list
    with patch('builtins.print', side_effect=printed.append):
        clienthelper.print_list(list_str) # instead of printing, append the printed string to the list
        assert printed == ["\n","item1", " item2", " item3"] # the printed string should be split into a list and appended to the list


def test_get_attraction_details_loop(clienthelper):
    pass