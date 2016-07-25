import os
import re

word_join = re.compile(r'([a-z0-9])([A-Z])')
filename_re = re.compile(r'(.*)_[^_]+$')


class TemplateNameMixin(object):

    def get_template_names(self):
        if getattr(self, 'template_name', None) is not None:
            return super(TemplateNameMixin, self).get_template_names()
        else:
            # DRY: package & class already define nice template name.
            module, clazz = self.__module__, self.__class__.__name__
            underscored = word_join.sub(r'\1_\2', clazz).lower()

            try:
                directory = module.split('.')[-2]
                filename = filename_re.search(underscored).group(1)
                return [os.path.join(directory, '{}.html'.format(filename))]
            except IndexError:
                return super(TemplateNameMixin, self).get_template_names()

