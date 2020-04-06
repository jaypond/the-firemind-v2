from orator import DatabaseManager, Model

config = {
    'postgres': {
        'driver': 'postgres',
        'host': 'localhost',
        'database': 'the_firemind',
        'user': 'jasonmatthewgarcia',
        'password': 'jasonjason3124',
        'prefix': ''
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)