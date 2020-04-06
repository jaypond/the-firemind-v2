from orator.migrations import Migration


class CreatePricesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('prices') as table:
            table.increments('id')
            table.integer('card_id')
            table.float('price').nullable()
            table.enum('card_type', ['Normal', 'Foil'])

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('prices')
