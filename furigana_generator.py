import sys
from pathlib import Path
from sudachipy import tokenizer
from sudachipy import dictionary
import re
import argparse

N5_KANJI = set("人一日大年出本中子見国上分生行二間時気十女三前入小後長下学月何来話山高今書五名金男外四先川東聞語九食八水天木六万白七円電父北車母半百土西読千校右南左友火毎雨休午")
N4_KANJI = set("言手自者事思会家的方地目場代私立物田体動社知理同心発作新世度明力意用主通文屋業持道身不口多野考開教近以問正真味界無少海切重集員公画死安親強使朝題仕京足品着別音元特風夜空有起運料楽色帰歩悪広店町住売待古医去台合同味品員問回図地堂場声売夏夕夜太好妹姉始字室家寒屋工市帰広度建引弟弱強待心思急悪意所持教文料旅族早明映春昼暑暗曜有服朝村林森業楽歌止正歩死民池注洋洗海漢牛物特犬理産用田町画界病発県真着知短研私秋究答紙終習考者肉自色英茶菜薬親計試説貸質赤走起転軽近送通進運遠都始終計院送族映買病早質台室可建転医止字工急図黒花英走青答紙歌注赤春館旅験写去研飲肉服銀茶洋兄秋堂週習夏弟鳥犬夕魚借飯駅昼冬姉曜漢牛妹貸勉")

N3_KANJI = set("部彼内実当戦性対関感定政取所現最化民相法全情向平成経信面連原顔機次数美回表声報要変神記和引治決太込受解市期様活頭組指説能葉流然初在調笑議直夫選権利制続石進伝加助点産務件命番落付得好違殺置返論際歳反形光首勝必係由愛都放確過約馬状想官交米配若資常果呼共残判役他術支両乗済供格打御断式師告深存存争覚側飛参突容育構認位達守満消任居予路座客追背観誰息失老良示号職王識警優投局難種念寄商害頼横増差苦収段俺渡与演備申例働景抜遠絶負福球酒君察望婚単押割限戻科求談降妻岡熱浮等末幸草越登類未規精抱労処退費非喜娘逃探犯薬園疑緒静具席速舞宿程気倒寝宅絵破庭婦余訪冷暮腹危許似険財遊雑恐値暗積夢痛富刻鳴欲途曲耳完願罪陽亡散掛昨怒留礼列雪払給敗捕忘晴因折迎悲港責除困閉吸髪束眠易窓祖勤昔便適軽吹候怖辞否遅煙徒欠迷洗互才更歯盗慣晩箱到頂杯皆招寒恥疲貧猫誤努幾賛偶忙泳靴偉")
N2_KANJI = set("軍兵島村門戸武城総団線設勢党史営府巻介蔵造根寺査将改県泉像細谷奥再血算象清技州領橋芸型香量久境階区波移域周接鉄頃材個協各帯歴編裏比坂装省税競囲辺河極防低林導森丸胸陸療諸管仲革担効賞星復片並底温軽録腰著乱章殿布角仏永誌減略準委令刊焼里圧額印池臣庫農板恋羽専逆腕短普岩竹児毛版宇況被岸超豊含植補暴課跡触玉震億肩劇刺述輪浅純薄阪韓固巨講般湯捨衣替央骨齢照層弱築脳航快翌旧筆換群爆捜油叫伸承雲練紹包庁測占混倍乳荒詰栄床則禁順枚厚皮輸濃簡孫丈黄届絡採傾鼻宝患延律希甘湾沈販欧砂尊紅複泊荷枝依幼斬勇昇寿菜季液券祭袋燃毒札狙脇卒副敬針拝浴悩汚灯坊尻涙停了汗郵幅童虫埋舟闇棒貨肌臓塩均湖損膝辛双軒績干姓掘籍珍訓預署漁緑畳咲貿踊封兆柱駐祝炭柔雇乾鋭氷隅冊糸募硬塗憎泥脂粉詞筒掃塔賢拾麦刷卵械皿祈灰召溶磨粒喫机貯匹綿贈凍瓶帽涼秒湿蒸菓耕鉱膚胃挟郊銅鈍貝缶枯滴符畜軟濯隻伺沸曇肯燥零")

KANJI_LEVELS = {
    "N5": N5_KANJI,
    "N4": N4_KANJI.union(N5_KANJI),
    "N3": N3_KANJI.union(N4_KANJI).union(N5_KANJI),
    "N2": N2_KANJI.union(N3_KANJI).union(N4_KANJI).union(N5_KANJI), # N2 includes N3, N4 and N5 kanji
    "N1": set() # N1 means ignore all kanji, handled in is_all_known_kanji
}

def kata_to_hira(text):
    return ''.join(
        chr(ord(char) - 0x60) if 'ァ' <= char <= 'ヴ' else char
        for char in text
    )

def is_all_known_kanji(word, kanji_level):
    if kanji_level is None:
        return False # If no level specified, no kanji are "known" to be ignored
    if kanji_level == "N1":
        return True # If N1 specified, all kanji are considered "known" to be ignored

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
                        help="Specify Kanji level to ignore (e.g., N5, N4, N3, N2, N1). If not specified, furigana will be used everywhere.")
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
