#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scooters.settings')
    try:
        from django.core.management import execute_from_command_line

        # Workaround for coverage, part one
        # (see https://github.com/django-nose/django-nose/issues/180#issuecomment-93371418)
        is_testing = 'test' in sys.argv
        if is_testing:
            import coverage
            # NOTE: for more precise results, adjust this to be a list of apps
            # for which you want coverage tracking
            source = ['.']
            omit = ['*/tests/*', '*/migrations/*']
            cov = coverage.coverage(source=source, omit=omit)
            cov.erase()
            cov.start()

        execute_from_command_line(sys.argv)

        # Workaround for coverage, part two
        if is_testing:
            cov.stop()
            cov.save()
            print('----------------------------------------------------------------------')
            print('\nCOVERAGE REPORT:')
            cov.report()
            cov.html_report(directory='cover')

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
