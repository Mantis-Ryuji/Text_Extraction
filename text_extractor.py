import os
import glob
import easyocr

# フォルダ下の画像データに対して一括してテキスト抽出をし、extracted_texts.txt として出力する

def text_extractor(path: str, lang_type: str):
    # 対応言語コード一覧（EasyOCR公式リストから一部抜粋）
    supported_langs = [
        'en',     # 英語
        'ja',     # 日本語
        'ch_sim', # 中国語（簡体字）
        'ch_tra', # 中国語（繁体字）
        'ko',     # 韓国語
        'fr',     # フランス語
        'de',     # ドイツ語
        'es',     # スペイン語
        'it',     # イタリア語
        'ru',     # ロシア語
        'vi',     # ベトナム語
        # 必要に応じて追加
    ]

    if lang_type not in supported_langs:
        raise ValueError(f"Unsupported lang_type: '{lang_type}'. Supported languages are: {supported_langs}")

    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    folder_path = path
    file_list = glob.glob(os.path.join(folder_path, '**'), recursive=True)
    file_list = [f for f in file_list if os.path.isfile(f)]

    reader = easyocr.Reader([lang_type])  # 言語指定
    text_list = []

    for file_path in file_list:
        result = reader.readtext(file_path)
        text = " ".join([res[1] for res in result])  # テキストを連結
        text_list.append(text)

    with open("extracted_texts.txt", "w", encoding="utf-8") as f:
        for i, text in enumerate(text_list):
            f.write(f"[{file_list[i]}]\n{text}\n\n")

'''
使い方：
text_extractor("Image", "en") 

出力イメージ：
[Image\S__68509699_0.jpg]
Welcome to OpenAI
This is a test image with text.

[Image\S__68509701_0.jpg]
Invoice No: 12345
Date: 2025-07-04

[Image\S__68509702_0.jpg]
Caution: High Voltage Area
Authorized Personnel Only

[Image\S__68509703_0.jpg]
Machine Learning is fun!
Try different models and augmentations.

[Image\S__68509704_0.jpg]
CONFIDENTIAL
Do not distribute

[Image\S__68509705_0.jpg]
Name: John Doe
Age: 29

[Image\S__68509706_0.jpg]
The quick brown fox jumps over the lazy dog.
'''
  
