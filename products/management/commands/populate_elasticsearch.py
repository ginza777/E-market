from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.management.commands.search_index import Command as SearchIndexCommand


class Command(BaseCommand):
    help = 'Populate Elasticsearch index with products'

    def handle(self, *args, **options):
        # Create and populate the index
        search_command = SearchIndexCommand()
        search_command.handle('--create', '--populate', 'products')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated Elasticsearch index with products')
        )
