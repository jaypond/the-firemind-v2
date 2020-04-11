from orator import DatabaseManager, Model

config = {
    'postgres': {
        'driver': 'postgres',
        'host': 'database',
        'database': 'the_firemind',
        'user': 'jasonmatthewgarcia',
        'password': 'jasonjason3124',
        'prefix': ''
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)