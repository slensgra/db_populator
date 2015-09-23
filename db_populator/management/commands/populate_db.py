from django.core.management.base import BaseCommand, CommandError
from django.db import models
from optparse import OptionParser
import logging

from db_populator.modified_ddf import G
from db_populator.modified_ddf import ddf

from db_populator.db_populator_conf import IGNORE
from db_populator.db_populator_conf import REQUIREMENTS

class Command(BaseCommand):
    # returns the log level based on the input provided by the user
    def handle(self, *args, **options):
        if 'verbose' in args:
            logging.disable(logging.DEBUG)
        else:
            logging.disable(logging.CRITICAL)

        self._populate_db()

    def _in_requirements(self, requirements, item):
        for i in requirements:
            if item in i.keys():
                return True
        return False

    def _get_created_classes(self, instance_set):
        return set([type(i) for i in instance_set])

    def _get_pkey(self, model):
        for i in model._meta.fields:
            if i.primary_key:
                return i

    def _has_inner_chain(self, chain):
        for i in chain.keys():
            if type(chain[i]) == dict:
                return True
        return False

    # so in our requirement we have model:{chain}
    def _save_chain(self, model, chain):
        if not self._has_inner_chain(chain):
            assert( len(chain.keys()) == 1 )
            return G(model, **chain)
        else:
            locators = []
            kws = {}
            for i in chain.keys():
                if type(chain[i]) == dict:
                    # we have run into something that we have to recurse over.
                    obj = self._save_chain(list(chain[i].keys())[0], chain[i][list(chain[i].keys())[0]])
                    locators.append((i, obj))
                else:
                    kws[i] = chain[i]
            kws['locators'] = locators
        return G(model, **kws)

        # note that locators will be of the style 'classref':class

    def _find_chain(self, requirements, model):
        for i in range(len(requirements)):
            if model in requirements[i].keys():
                ch = requirements[i]
                requirements.pop(i)
                return ch
        return None

    def _populate_db(self):
        all_models = models.get_models()
        logging.debug("all models: {models}".format(models=all_models))
        logging.debug("created instances: {ci}".format(ci=ddf.get_created_instances()))

        created_instances = set()

        for model in all_models:
            logging.debug("creating instance of {m}".format(m=model))
            if model not in IGNORE and (model not in self._get_created_classes(created_instances) or self._in_requirements(REQUIREMENTS, model)):
                logging.info(" calling G on model: {model}".format(model=model))

                if self._in_requirements(REQUIREMENTS, model):
                    while self._in_requirements(REQUIREMENTS, model):
                        chain = self._find_chain(REQUIREMENTS, model)
                        self._save_chain(list(chain.keys())[0], chain[list(chain.keys())[0]])
                else:
                    G(model)

                for i in ddf.get_created_instances():
                    created_instances.add(i)
                logging.info(" created instances after gen: {ci}".format(ci=len(created_instances)))
