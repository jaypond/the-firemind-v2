from orator.migrations import Migration


class CreateCardSetsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('card_sets') as table:
            table.integer('set_id')
            table.string('name')
            table.boolean('is_supplemental')
            table.datetime('published_on')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('card_sets')
