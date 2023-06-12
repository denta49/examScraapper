import json
import time

from get_dictionary import get_dictionary


def compare_dictionaries(urls):
    main_dictionary = {}
    for url in urls:
        for i in range(1):
            print('')
            print('Executing function')
            counter = 0
            time.sleep(3)
            new_dictionary = get_dictionary(url)
            for new_values in new_dictionary:
                if new_values not in main_dictionary:
                    counter += 1
                    main_dictionary[new_values] = new_dictionary[new_values]

            print('Current length: ' + str(len(main_dictionary)))
            print('Found new values: ' + str(counter))
            print('')

    with open("sample.json", "w", encoding='utf8') as outfile:
        json.dump(main_dictionary, outfile, ensure_ascii=False)


compare_dictionaries([''])
