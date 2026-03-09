
from fluentogram import FluentTranslator, TranslatorHub, TranslatorRunner
from fluent_compiler.bundle import FluentBundle  # noqa


class Translator:
    hub: TranslatorHub

    def __init__(self):
        self.hub = TranslatorHub(
            locales_map={
                'en': ('en', 'ru'),
                'ru': ('ru',)
            },
            translators=[
                FluentTranslator(
                    locale='en',
                    translator=FluentBundle.from_files(
                        locale='en-US',
                        filenames=['lexicon/locales/en.ftl']
                    )
                ),
                FluentTranslator(
                    locale='ru',
                    translator=FluentBundle.from_files(
                        locale='ru-RU',
                        filenames=['lexicon/locales/ru.ftl']
                    )
                ),
            ],
            root_locale='ru'
        )

    def __call__(self, lang: str, *args, **kwargs):
        return LocalizedTranslator(
            translator=self.hub.get_translator_by_locale(locale=lang)
        )


class LocalizedTranslator:
    translator: TranslatorRunner

    def __init__(self, translator: TranslatorRunner):
        self.translator = translator

    def get(self, key: str, **kwargs) -> str:
        return self.translator.get(key, **kwargs)
