import requests
from lxml import html
from urllib.parse import urljoin

from django.core.management.base import BaseCommand, CommandError
from roles.models import AgentNoun


class Command(BaseCommand):
    help = 'Import agent nouns from https://en.wiktionary.org/wiki/Category:English_agent_nouns'

    total_words_created = 0
    total_words_already = 0

    def process_page(self, url):
        r = requests.get(url)
        tree = html.fromstring(r.content)

        words_created = 0
        words_already = 0

        for el in tree.xpath('//div[@class="mw-category-group"] / ul / li / a'):
            word = el.text.strip()
            if len(word):
                h, created = AgentNoun.objects.get_or_create(word=word)
                if created:
                    words_created += 1
                else:
                    words_already += 1

        self.stdout.write(self.style.SUCCESS('Imported %d words, %d words skipped as already in database.' % (words_created, words_already)))
        self.total_words_created += words_created
        self.total_words_already += words_already

        els = tree.xpath('//a[text()="next page"]')
        if els:
            next_url = els[0].attrib['href']
            next_url = urljoin(url, next_url)
            self.process_page(next_url)


    def handle(self, *args, **options):
        self.process_page("https://en.wiktionary.org/wiki/Category:English_agent_nouns")
        self.stdout.write(
            self.style.SUCCESS('Totals: Imported %d words, %d words skipped as already in database.' % (
                self.total_words_created,
                self.total_words_already)
            )
        )
