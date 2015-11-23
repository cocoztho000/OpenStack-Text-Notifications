import urllib


class Person(object):

    def __init__(self, name, reviews, username):
        self.name = name
        self.reviews = reviews
        self.username = username


class ProjectPeople(object):
    def __init__(self):
        self.project = ''
        self.people = []

    def add_person(self, person):
        self.people.append(person)


class OpenstackTextUpdates(object):
    def __init__(self):
        pass

    @staticmethod
    def read_doc_to_dict(project, days):
        response = urllib.urlopen('http://russellbryant.net/openstack-stats/' + project + '-reviewers-' + days + '.txt', proxies=None)
        list_response = response.read().split('\n')

        doc_dict = []

        for line in list_response:
            line = line.strip()
            if not line.startswith('|'):
                continue
            else:
                line_elements = line.split('|')
                if line_elements[1].split() == 'Reviewer':
                    continue

                username = line_elements[1].strip()
                username = username.replace(' **', '')
                reviews = line_elements[2]
                reviews = reviews.split()[0]

                if username == 'Reviewer':
                    continue

                doc_dict.append({'username': username,
                                 'reviews': reviews})
        return doc_dict

    @staticmethod
    def validate_project(self, project):
        response = urllib.urlopen('http://russellbryant.net/openstack-stats/' + project + '-reviewers-30.txt', proxies=None)

        if '404' in response:
            return False
        else:
            return True

    @staticmethod
    def validate_user(self, project, username):
        response = urllib.urlopen('http://russellbryant.net/openstack-stats/' + project + '-reviewers-30.txt', proxies=None)
        list_response = response.read().split('\n')

        doc_dict = []

        for line in list_response:
            line = line.strip()
            if not line.startswith('|'):
                continue
            else:
                line_elements = line.split('|')
                if line_elements[1].split() == 'Reviewer':
                    continue

                username = line_elements[1].strip()
                username = username.replace(' **', '')

                if username == username:
                    return True

        return False

# #test = Person(0, 'Tom', 100, 'tjcocozz')
#test = OpenstackTextUpdates()
#print 'Test read_doc'
#print test.read_doc_to_dict('keystone', '30')

#print test.validate_project('keystone1')


