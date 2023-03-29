from translate import Translator

name_translator = Translator(from_lang='Russian', to_lang='English')


def get_code_name_by_verbose_name(verbose_name: str) -> str:
    """Generates hints for variable names"""
    result_code_name = ''
    translation = name_translator.translate(verbose_name.lower())
    for word in translation.split():
        result_code_name += word.lower() + '_'
    return result_code_name[:-1]


if __name__ == '__main__':
    print(get_code_name_by_verbose_name('Имя'))