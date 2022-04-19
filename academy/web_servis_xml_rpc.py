import xmlrpc.client as client

hostname = 'localhost'
port = '8569'
db_name = 'o15-learn'
username = 'admin'
password = 'admin'

modelsession = 'academy.session'
modelcourse = 'academy.course'

root = f'http://{hostname}:{port}/xmlrpc/2/'
user_id = client.ServerProxy(root + 'common').login(db_name, username, password)
models = client.ServerProxy(f'{root}object')

# прoчитаем
if user_id:
    search_domain = []
    sessions_id = models.execute_kw(db_name, user_id, password, modelsession, 'search', [search_domain])
    session_data = models.execute_kw(db_name, user_id, password, modelsession, 'read',
                                     [sessions_id, ['name', 'number_of_seats']])
    for sd in session_data:
        print(f'Session #{sd["id"]};name={sd["name"]};seats={sd["number_of_seats"]}')
else:
    print("Can't read data of sessions!")

# сoдаем нoвую сессию
if user_id:
    search_domain = [('name', 'ilike', 'Курс румынского языка')]
    course_id = models.execute_kw(db_name, user_id, password, modelcourse, 'search', [search_domain])[0]

    sdat = [{'name': 'Сессия B2', 'course': course_id, 'duration': 3}]
    session_id = models.execute_kw(db_name, user_id, password, modelsession, 'create', sdat)
    print("Created new session")
else:
    print("Error session creating!")
