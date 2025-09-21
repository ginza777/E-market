from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.management.commands.search_index import Command as SearchIndexCommand
from products.documents import ProductDocument
from products.models import Product
from categories.models import Category
from django.db import connection
import time


class Command(BaseCommand):
    help = 'Test Elasticsearch indexing and search functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-index',
            action='store_true',
            help='Create Elasticsearch index'
        )
        parser.add_argument(
            '--populate-index',
            action='store_true',
            help='Populate Elasticsearch index with existing data'
        )
        parser.add_argument(
            '--test-search',
            action='store_true',
            help='Test search functionality'
        )
        parser.add_argument(
            '--test-indexing',
            action='store_true',
            help='Test indexing performance'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Run all tests'
        )

    def handle(self, *args, **options):
        if options['all']:
            options['create_index'] = True
            options['populate_index'] = True
            options['test_search'] = True
            options['test_indexing'] = True

        if options['create_index']:
            self.create_index()
        
        if options['populate_index']:
            self.populate_index()
        
        if options['test_search']:
            self.test_search()
        
        if options['test_indexing']:
            self.test_indexing()

    def create_index(self):
        """Create Elasticsearch index"""
        self.stdout.write('Creating Elasticsearch index...')
        try:
            search_command = SearchIndexCommand()
            search_command.handle('--create', 'products')
            self.stdout.write(self.style.SUCCESS('Index created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating index: {e}'))

    def populate_index(self):
        """Populate Elasticsearch index with existing data"""
        self.stdout.write('Populating Elasticsearch index...')
        try:
            search_command = SearchIndexCommand()
            search_command.handle('--populate', 'products')
            self.stdout.write(self.style.SUCCESS('Index populated successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error populating index: {e}'))

    def test_search(self):
        """Test search functionality"""
        self.stdout.write('Testing search functionality...')
        
        # Test basic search
        try:
            search = ProductDocument.search()
            results = search.query('match', title='iPhone').execute()
            self.stdout.write(f'Found {len(results)} products matching "iPhone"')
            
            # Test category search
            search = ProductDocument.search()
            results = search.query('match', category__title='Electronics').execute()
            self.stdout.write(f'Found {len(results)} products in Electronics category')
            
            # Test price range search
            search = ProductDocument.search()
            results = search.query('range', price={'gte': 100, 'lte': 500}).execute()
            self.stdout.write(f'Found {len(results)} products in price range 100-500')
            
            self.stdout.write(self.style.SUCCESS('Search tests completed'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Search test failed: {e}'))

    def test_indexing(self):
        """Test indexing performance"""
        self.stdout.write('Testing indexing performance...')
        
        try:
            # Get some products to test with
            products = Product.objects.all()[:10]
            if not products:
                self.stdout.write(self.style.WARNING('No products found. Create some products first.'))
                return
            
            # Test individual indexing
            start_time = time.time()
            for product in products:
                ProductDocument().update(product)
            end_time = time.time()
            
            individual_time = end_time - start_time
            self.stdout.write(f'Individual indexing time: {individual_time:.2f} seconds')
            
            # Test bulk indexing
            start_time = time.time()
            ProductDocument().bulk_update(products)
            end_time = time.time()
            
            bulk_time = end_time - start_time
            self.stdout.write(f'Bulk indexing time: {bulk_time:.2f} seconds')
            
            # Calculate performance improvement
            if individual_time > 0:
                improvement = ((individual_time - bulk_time) / individual_time) * 100
                self.stdout.write(f'Bulk indexing is {improvement:.1f}% faster')
            
            self.stdout.write(self.style.SUCCESS('Indexing performance tests completed'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Indexing test failed: {e}'))

    def get_index_stats(self):
        """Get Elasticsearch index statistics"""
        try:
            from elasticsearch import Elasticsearch
            from django.conf import settings
            
            es_host = settings.ELASTICSEARCH_DSL['default']['hosts']
            es = Elasticsearch(es_host)
            
            # Get index stats
            stats = es.indices.stats(index='products')
            if 'indices' in stats and 'products' in stats['indices']:
                index_stats = stats['indices']['products']
                doc_count = index_stats['total']['docs']['count']
                store_size = index_stats['total']['store']['size_in_bytes']
                
                self.stdout.write(f'Index document count: {doc_count}')
                self.stdout.write(f'Index size: {store_size} bytes')
            else:
                self.stdout.write('No index statistics available')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting index stats: {e}'))
