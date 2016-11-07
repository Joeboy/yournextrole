import requests
from lxml import html

from django.core.management.base import BaseCommand, CommandError
from roles.models import Homonym


class Command(BaseCommand):
    help = 'Import homonyms from http://home.alphalink.com.au/~umbidas/homonym_main.htm'

    def handle(self, *args, **options):
        r = requests.get("http://home.alphalink.com.au/~umbidas/homonym_main.htm")
        tree = html.fromstring(r.content)

        words_created = 0
        words_already = 0

        for cell in tree.xpath('//table[1] / tr / td'):
            word = cell.text_content().strip()
            if len(word):
                h, created = Homonym.objects.get_or_create(word=word)
                if created:
                    words_created += 1
                else:
                    words_already += 1

        self.stdout.write(self.style.SUCCESS('Imported %d words, %d words skipped as already in database.' % (words_created, words_already)))
