from orator.migrations import Migration


class CreateCardsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('cards') as table:
            table.integer('card_id')
            table.integer('set_id')
            table.string('name')
            table.string('clean_name')
            table.string('image_url')
            table.string('url')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('cards')
