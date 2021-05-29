from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
from pyfiglet import Figlet
from youtube.video_search import SearchQuery
from collector import collect_yt, collect_local


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))


def main():
    '''
    Print logo and begin questions with keyword.
    '''
    fig = Figlet(font='big')
    print(fig.renderText('Keyword Collector'))
    ask_keyword()


def ask_keyword():
    '''
    Ask user what keyword should be collected.
    '''
    questions = [
        {
            'type': 'input',
            'name': 'keyword',
            'message': 'What keyword would you like to collect?'
        }
    ]

    answers = prompt(questions)
    keyword = answers['keyword']
    user_input['keyword'] = keyword.strip()
    ask_audio_source()


def ask_audio_source():
    '''
    Ask user where keywords should be found.

    Options:
        YouTube
        Directory containing local WAV files
    '''
    questions = [
        {
            'type': 'list',
            'name': 'audio_source',
            'message': 'Where would you like to collect keywords from?',
            'choices': [
                {
                    'key': '1',
                    'name': 'YouTube',
                    'value': 'youtube'
                },
                {
                    'key': '2',
                    'name': 'Local WAV files',
                    'value': 'local'
                }
            ]
        }
    ]

    answers = prompt(questions)
    audio_source = answers['audio_source']

    if audio_source == 'youtube':
        ask_yt_options()
    else:
        ask_local_options()


def ask_yt_options():
    '''
    Ask user to enter YouTube options:
        - Desired number of keywords
        - Search query
    '''
    questions = [
        {
            'type': 'input',
            'name': 'query',
            'message': 'What would you like to search for on YouTube?'
        },
        {
            'type': 'input',
            'name': 'quantity',
            'message': 'How many utterances would you like to collect?',
            'validate': NumberValidator
        }
    ]
    answers = prompt(questions)
    
    query = answers['query']
    quantity = int(answers['quantity'])

    keyword = user_input['keyword']

    search_query = SearchQuery(keyword=keyword, query=query)
    search_results = search_query.search()
    collect_yt(search_results, keyword, quantity)
    


def ask_local_options():
    '''
    Ask user location of directory containing WAV files.
    '''
    questions = [
        {
            'type': 'input',
            'name': 'data_dir',
            'message': 'Enter path to directory containing WAV files:'
        }
    ]
    answers = prompt(questions)

    data_dir = answers['data_dir']

    keyword = user_input['keyword']
    collect_local(data_dir, keyword)


if __name__ == "__main__":
    user_input = {}
    main()
