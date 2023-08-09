import re
from googletrans import Translator

first_re = re.compile(
    r"(?P<beginning>^[^\t]+\t4000 EEW Extra\t4000 Essential English Words::[^\t]*\t[^\t]+\t[^\t]*\t)"
    r"(?P<en_word>[^\t]+\t)[^\t]*"
    r"(?P<ending>\t.*$)"
)
second_re = re.compile(
    r"(?P<beginning>^[^\t]+\t4000 EEW\t4000 Essential English Words::[^\t]+\t)"
    r"(?P<en_word>[^\t]+\t)[^\t]*"
    r"(?P<ending>\t.*$)"
)


def modify_string(input_str, translate):
    """Inserts translation if string matches of any regex"""
    match = first_re.match(input_str)
    if not match:
        match = second_re.match(input_str)
    if match:
        dct = match.groupdict()
        return dct["beginning"] + dct["en_word"] + translate(dct["en_word"]) + dct["ending"]
    else:
        return input_str


def modify_file(in_fname, out_fname):
    """Applies modify_string function to every string in file and writes them to another"""
    translator = Translator()
    translate = lambda text_in: translator.translate(text_in, src="en", dest="ru").text
    assert translate("How you doing, man?") == "Как дела, чувак?", "Translator isn't working"

    with open(in_fname, "r", encoding="utf-8") as in_file:
        with open(out_fname, "w", encoding="utf-8") as out_file:
            lines = in_file.readlines()
            for i, line in enumerate(lines):
                mod_string = modify_string(line, translate)
                out_file.write(mod_string + ("\n" if not mod_string.endswith("\n") else ""))
                print(i, mod_string)
            # out_file.writelines(modify_string(line, translate) for line in in_file.readlines())


def main():
    modify_file("input.txt", "output.txt")


if __name__ == "__main__":
    main()
