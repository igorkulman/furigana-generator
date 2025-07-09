import sys
from pathlib import Path
from sudachipy import tokenizer
from sudachipy import dictionary
import re
import argparse

N5_KANJI = set("人一日大年出本中子見国上分生行二間時気十女三前入小後長下学月何来話山高今書五名金男外四先川東聞語九食八水天木六万白七円電父北車母半百土西読千校右南左友火毎雨休午")
N4_KANJI = set("言手自者事思会家的方地目場代私立物田体動社知理同心発作新世度明力意用主通文屋業持道身不口多野考開教近以問正真味界無少海切重集員公画死安親強使朝題仕京足品着別音元特風夜空有起運料楽色帰歩悪広店町住売待古医去台合同味品員問回図地堂場声売夏夕夜太好妹姉始字室家寒屋工市帰広度建引弟弱強待心思急悪意所持教文料旅族早明映春昼暑暗曜有服朝村林森業楽歌止正歩死民池注洋洗海漢牛物特犬理産用田町画界病発県真着知短研私秋究答紙終習考者肉自色英茶菜薬親計試説貸質赤走起転軽近送通進運遠都始終計院送族映買病早質台室可建転医止字工急図黒花英走青答紙歌注赤春館旅験写去研飲肉服銀茶洋兄秋堂週習夏弟鳥犬夕魚借飯駅昼冬姉曜漢牛妹貸勉")

KANJI_LEVELS = {
    "N5": N5_KANJI,
    "N4": N4_KANJI.union(N5_KANJI) # N4 includes N5 kanji
}

def kata_to_hira(text):
    return ''.join(
        chr(ord(char) - 0x60) if 'ァ' <= char <= 'ヴ' else char
        for char in text
    )

def is_all_known_kanji(word, kanji_level):
    if kanji_level is None:
        return False # If no level specified, no kanji are "known" to be ignored

    kanji_chars = re.findall(r'[一-龯]', word)
    known_kanji_set = KANJI_LEVELS.get(kanji_level)
    if known_kanji_set is None:
        return False # Should not happen with choices, but as a safeguard

    return all(char in known_kanji_set for char in kanji_chars)

def is_katakana(s):
    return bool(re.fullmatch(r'[ァ-ヴー・]+', s))

def to_ruby_format(text, kanji_level):
    mode = tokenizer.Tokenizer.SplitMode.C
    tokenizer_obj = dictionary.Dictionary().create()
    output_lines = []

    for line in text.splitlines():
        if not line.strip():
            output_lines.append("<p></p>")
            continue

        tagged_line = []
        for m in tokenizer_obj.tokenize(line, mode):
            surface = m.surface()
            reading = kata_to_hira(m.reading_form())

            if is_katakana(surface):
                tagged_line.append(surface)
                continue

            if reading and surface != reading:
                if is_all_known_kanji(surface, kanji_level):
                    tagged_line.append(surface)
                else:
                    tagged_line.append(f"<ruby>{surface}<rt>{reading}</rt></ruby>")
            else:
                tagged_line.append(surface)

        output_lines.append(f"<p>{''.join(tagged_line)}</p>")

    body_content = '\n'.join(output_lines)
    html_output = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Furigana Output</title>
  <style>
    body {{
      font-family: "Yu Gothic", sans-serif;
      font-size: 14pt;
      line-height: 1.7;
      margin: 2cm;
    }}
    ruby rt {{
      font-size: 60%;
    }}
  </style>
</head>
<body>
{body_content}
</body>
</html>"""
    return html_output

def main():
    parser = argparse.ArgumentParser(description="Add furigana to Japanese text.")
    parser.add_argument("input_files", nargs="+", help="Input text files (UTF-8 encoded)")
    parser.add_argument("-k", "--kanji-level", choices=list(KANJI_LEVELS.keys()),
                        help="Specify Kanji level to ignore (e.g., N5, N4). If not specified, furigana will be used everywhere.")
    args = parser.parse_args()

    kanji_level = args.kanji_level

    for input_path_str in args.input_files:
        input_path = Path(input_path_str)
        if not input_path.exists():
            print(f"File not found: {input_path}")
            continue

        text = input_path.read_text(encoding='utf-8')
        html_text = to_ruby_format(text, kanji_level)

        output_path = input_path.with_suffix('.html')
        output_path.write_text(html_text, encoding='utf-8')
        print(f"✅ Furigana HTML saved to: {output_path}")

if __name__ == "__main__":
    main()
