import json

from flask import Flask, request
app = Flask(__name__)

NUM_RESULTS = 10
MOCK_RESULTS = [
    {
        'title': 'Example Site',
        'url': 'http://example.com',
        'description': 'This is an example site.'
    },
    {
        'title': 'Google',
        'url': 'https://google.com',
        'description': 'The most prolific search engine.'
    },
    {
        'title': 'pleatsikas.me',
        'url': 'https://pleatsikas.me',
        'description': 'Nick Pleatsikas\'s personal website.'
    },
    {
        'title': 'Stack Overflow',
        'url': 'stackoverflow.com',
        'description': 'Where programmers go for answers.'
    },
    {
        'title': 'Apple',
        'url': 'apple.com',
        'description': 'They make decent computers, I suppose.'
    },
    {
        'title': 'DuckDuckGo',
        'url': 'duckduckgo.com',
        'description': 'A more private search engine.'
    }
] * NUM_RESULTS


@app.route('/search')
def search():
    results = []
    if ((after := request.args.get('after')) is not None):
        after = int(after)
        results = MOCK_RESULTS[after:after + NUM_RESULTS]
    else:
        results = MOCK_RESULTS[:NUM_RESULTS]

    return json.dumps(results)


if __name__ == '__main__':
    app.run()
