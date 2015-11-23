from flask import Flask, request

from person import OpenstackTextUpdates
from people import People as peaps

import shelve

new_people = shelve.open('new_people')

app = Flask(__name__)

new_people['2342347234'] = {'project': 'keystone',
                            'username': 'tjcocozz',
                            'cycle': '30',
                            'position': 2}
new_people.close()


def initiate_next_step(person_info, text):
    person_keys = person_info.itervalues().next()

    if 'project' not in person_keys:
        project(person_info, text)
    elif 'username' not in person_keys:
        username(person_info, text)
    elif 'cycle' not in person_keys:
        cycle(person_info, text)
    else:
        return "Awesome someone who likes OpenStack as much as me! To stop at" \
               " any time send 'stop'. What project are you interested in?"
        # Send Text 'Awesome someone who likes OpenStack as much as me! To stop at
        # any time send 'stop'. What project are you interested in?'


def project(person_info, sms_project):
    local_new_people = shelve.open('new_people')
    person_keys = person_info.itervalues().next()

    person_number = person_info.keys()[0]

    valid = OpenstackTextUpdates.validate_project(sms_project)

    if not valid:
        new_people.close()
        # Send Text 'The project name you sent was not valid. pls send it again
        return 'The project name you sent was not valid. pls send it again'
    else:
        local_new_people[person_number]['project'] = sms_project
        local_new_people.close()
        return 'Awesome I love sms_project what is your username?'
        # Send Text 'Awesome I love sms_project what is your username?'



def username(person_info, sms_username):
    new_people = shelve.open('new_people')
    person_keys = person_info.itervalues().next()

    person_number = person_info.keys()[0]

    valid = OpenstackTextUpdates.validate_user(sms_username)

    if not valid:
        new_people.close()
        # Send Text 'The username you sent was not valid. pls send it again
        return 'The username you sent was not valid. pls send it again'
    else:
        new_people[person_number]['username'] = sms_username
        new_people.close()
        return 'Welcome sms_username. What Day cycle do you want to be ' \
               'notified about? Your options are "30", "60", "90", "180," "365", "1095"'


def cycle(person_info, sms_cycle):
    new_people = shelve.open('new_people')
    options = ['30', '60', '90', '180', '365', '1095']

    person_number = person_info.keys()[0]

    valid = sms_cycle in options

    if not valid:
        # Send Text 'The cycle you sent was not valid. pls send it again.
        # Your options are '30', '60', '90', '180', '365', '1095'
        new_people.close()
        return "Send Text 'The cycle you sent was not valid. pls send it again.  " \
               "Your options are '30', '60', '90', '180', '365', '1095'"
    else:
        new_people[person_number]['cycle'] = sms_cycle
        tmp_new_person = new_people[person_number]
        peaps.append(tmp_new_person)
        del new_people[person_number]
        #
        #
        # add this person to the db: new_people[person_number])
        #
        #
    return "Your all set up %(username)s. Your in %(position)s" \
           " and will be notified of any change" % {
             'username': tmp_new_person['username'],
             'position': '1'
            }


@app.route("/receive_sms/", methods=['GET','POST'])
def receive_sms():
    # Sender's phone number
    from_number = request.values.get('From')
    # Receiver's phone number - Plivo number
    to_number = request.values.get('To')
    # The text which was received
    text = request.values.get('Text')

    if 'stop' in text:
        pass
        # DELETE USER

    person_info = new_people.get(from_number)
    if person_info:
        initiate_next_step(person_info, text)
    else:
        pass
        # Send Text 'Awesome someone who likes OpenStack as much as me!
        # What project are you interested in?'

    # Print the message
    print 'Message received - From: %s, To: %s, Text: %s' % (from_number, to_number, text)

    return "Message received", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
