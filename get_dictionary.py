import requests
from lxml import html


def get_page(url):
    return requests.get(url)


def get_tree(page):
    return html.fromstring(page.content)


def get_examples(tree, url):
    elements = tree.xpath('//p/text()|//br/text()')
    examples = []
    if 'hidden value' in url:
        for ele in elements:
            if ele[0].isdigit():
                if ele[1].isdigit():
                    examples.append(ele[3:].replace('\n', '').replace('\r', '').strip())
                    break
                examples.append(ele[2:].replace('\n', '').replace('\r', '').strip())
        return examples


def get_questions(tree):
    elements = tree.xpath('//td/text()')
    questions = []
    counter = 0
    for ele in elements:
        clean = ele.replace('\n', '').replace(u'\xa0', u' ').strip()
        if clean == '':
            counter += 1
            if counter == 3:
                clean = 'null'
                counter = 0
        else:
            counter = 0
        if not clean.isspace() and len(clean) > 3:
            questions.append(clean)
    return questions


def get_answers(tree):
    elements = tree.xpath('//td[input[substring(@id, string-length(@id) - string-length("d") + 1)  = "d"]]/text()')
    answers = []
    for ele in elements:
        clean = ele.replace('\n', '').replace(u'\xa0', u' ').strip()
        if len(clean) == 3:
            answers.append(clean)
    return answers


def create_examples_dict(examples):
    all_examples = {}
    for example in examples:
        all_examples[f'{example}'] = {}
    return all_examples


def associate_examples_and_questions(examples_dict, questions_array):
    start_number = 0
    end_number = 4
    new_dict = {}

    for example in examples_dict:
        new_dict.update({f'{example}': questions_array[start_number:end_number]})
        start_number += 4
        end_number += 4
    return new_dict


def add_answers(answers, dictionary):
    counter = 0
    new_answers = []

    for values in dictionary.values():
        for value in values:
            new_answers.append(value + ": " + answers[counter])
            counter += 1
    return new_answers


def sort_answers(ready_dictionary):
    new_dict = ready_dictionary
    for key in new_dict:
        answers = new_dict[key]
        sorted_answers = sorted(answers)
        new_dict[key] = sorted_answers
    return new_dict


def get_dictionary(url):
    page = get_page(url)
    tree = get_tree(page)
    examples = get_examples(tree, url)
    questions = get_questions(tree)
    examples_dict = create_examples_dict(examples)
    associated = associate_examples_and_questions(examples_dict, questions)
    answers = get_answers(tree)
    questions_with_answers = add_answers(answers, associated)
    associated_with_answers = associate_examples_and_questions(examples_dict, questions_with_answers)
    sorted_dict = sort_answers(associated_with_answers)
    return sorted_dict
