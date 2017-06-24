import os.path
import sys

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

import uuid

CLIENT_ACCESS_TOKEN = "75d2f175cd05473fbddba4d6475a49d8"


def add_entity(entity_name, input_entries):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    # some unique session id for user identification
    session_id = uuid.uuid4().hex
    entries = []

    for entry in input_entries:
        entries.append(api.ai.UserEntityEntry(entry, [entry]))
    
    '''
    entries = [
        apiai.UserEntityEntry('Firefox', ['Firefox']),
        apiai.UserEntityEntry('XCode', ['XCode']),
        apiai.UserEntityEntry('Sublime Text', ['Sublime Text'])
    ]
    '''

    user_entities_request = ai.user_entities_request(
        [
            apiai.UserEntity(entity_name, entries, session_id)
        ]
    )

    user_entities_response = user_entities_request.getresponse()

    print 'Upload user entities response: ', (user_entities_response.read())

    



