import re
from typing import Dict, Tuple
from googletrans import Translator

# No translations allowed before modifying
general_re = re.compile(r"(?P<beginning>^.*\t)(?P<en_word>[^\t]+\t)(?P<ending>\t.+$)")


def get_dct_and_enword(input_str) -> Tuple[Dict[str, str] | None, str]:
    match = general_re.match(input_str)
    if match:
        dct = match.groupdict()
        return dct, dct["en_word"]
    else:
        dct = {"default": input_str}
        return dct, ""


def modify_string(dct, translation):
    len_dct = len(dct)
    assert len_dct in [1, 3], f"Wrong dictionary length: {len_dct}"
    if len(dct) == 3:
        return dct["beginning"] + dct["en_word"] + translation + dct["ending"]
    else:
        return dct["default"]


def modify_file(in_fname, out_fname, buffer_len=100):
    """Applies modify_string function to every string in file and writes them to another"""
    translator = Translator()
    translate = lambda text_in: translator.translate(text_in, src="en", dest="ru").text
    assert translate("How you doing, man?") == "Как дела, чувак?", "Translator isn't working"

    with open(in_fname, "r", encoding="utf-8") as in_file:
        with open(out_fname, "w", encoding="utf-8") as out_file:
            lines = in_file.readlines()
            dct_buffer = []
            en_words_buffer = []

            lines_size = len(lines)
            diff = (lines_size - 1) % buffer_len  # This made to be sure of clearing buffer on last iteration
            for i, line in enumerate(lines):
                dct, en_word = get_dct_and_enword(line)
                dct_buffer.append(dct)
                en_words_buffer.append(en_word)

                if (i - diff) % buffer_len == 0:
                    # "a" here just a placeholder, because of translator deleting empty lines
                    string_to_send = "\n".join(word if word != "" else "a" for word in en_words_buffer)
                    translated_list = translate(string_to_send).split("\n")
                    assert len(dct_buffer) == len(translated_list), "Lengths after translation are not equal"

                    for dct_i, translation_i in zip(dct_buffer, translated_list):
                        mod_string = modify_string(dct_i, translation_i)
                        out_file.write(mod_string + ("\n" if not mod_string.endswith("\n") else ""))

                    dct_buffer.clear()
                    en_words_buffer.clear()

                    percent_complete = (i + 1) * 100 / lines_size
                    print("\rProgress: [{:<50}] {:.2f}%".format("=" * int(percent_complete / 2), percent_complete), flush=True, end="")
    print("\nDone!")


def main():
    # modify_file("input.txt", "output.txt")
    modify_file("sample.txt", "output.txt")


if __name__ == "__main__":
    main()
