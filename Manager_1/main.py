import json
import os
import re
class SKUManager:
    def __init__(self, brand_settings):
        self.brand_settings = brand_settings

    def generate_variations(self, input_sku, brand_rule):
        input_variations=[input_sku]
        brand_variations = self.create_brand_variations(input_sku, brand_rule)
        blind_variations = self.create_blind_variations(input_sku, brand_rule)
        total_variations = input_variations + brand_variations + blind_variations

        print(f"Total Variations before length {len(total_variations)}")
        total_variations = list(dict.fromkeys(total_variations))
        print(f"Total Variations after length {len(total_variations)}")

        return total_variations



    def create_brand_variations(self, sku, brand_rule):
        cleaned_sku = clean_sku(sku)
        sku_format = brand_rule['sku_format']
        base_parts = sku_format['base']
        base_separator = sku_format.get('base_separator', '')
        color_separator = sku_format.get('color_separator', '')
        complex = brand_rule.get('complex', False)

        article_length = int(base_parts['article'][0].split(',')[0])
        model_length = int(base_parts['model'][0].split(',')[0])
        color_length = int(sku_format['color_extension'][0].split(',')[0])

        article_part = cleaned_sku[:article_length]
        model_part = cleaned_sku[article_length:article_length + model_length]
        color_part = cleaned_sku[article_length + model_length:article_length + model_length + color_length]
        if complex:
            return self.complex(article_length, model_length, cleaned_sku, base_separator)
        # Order: Brand Format with Color, Brand Format without Color
        brand_sku_list=[
                article_part + base_separator + model_part + color_separator + color_part,
                article_part + base_separator + model_part
            ]
        print(f"Brand List before length {len(brand_sku_list)}")
        brand_sku_list = list(dict.fromkeys(brand_sku_list))
        print(f"Brand List after length {len(brand_sku_list)}")
        return brand_sku_list

    def create_blind_variations(self, sku, brand_rule):
        delimiters=["."," ","-","_",""]
        cleaned_sku = clean_sku(sku)
        sku_format = brand_rule['sku_format']
        base_separator = sku_format.get('base_separator', '')
        article_length = int(sku_format['base']['article'][0].split(',')[0])
        model_length = int(sku_format['base']['model'][0].split(',')[0])
        color_length = int(sku_format['color_extension'][0].split(',')[0])
        complex = brand_rule.get('complex', False)
        article_part = cleaned_sku[:article_length]
        model_part = cleaned_sku[article_length:article_length + model_length]
        color_part = cleaned_sku[article_length + model_length:article_length + model_length + color_length]
        if complex:
            return self.complex(article_length, model_length, cleaned_sku, base_separator)
        # Order: No space (Article Model Color), Space (Article Model Color), No space (Article Model), Space (Article Model)
        blind_sku_list=[]
        for base_separator in delimiters:
            for color_separator in delimiters:
                blind_sku_list.extend(
                    [
                        article_part + base_separator + model_part + color_separator + color_part,
                        article_part + base_separator + model_part,
                    ]
                )
        print(f"Blind List before length {len(blind_sku_list)}")
        blind_sku_list = list(dict.fromkeys(blind_sku_list))
        print(f"Blind List after length {len(blind_sku_list)}")
        return blind_sku_list

    def complex(self, article_length, model_length, cleaned_sku, base_separator):
        print(cleaned_sku)
        new_sku = remove_letters_from_end(cleaned_sku)

        article_part = new_sku[:article_length]
        model_part = new_sku[len(new_sku) - model_length:]
        return [
            article_part + base_separator + model_part,
            model_part
        ]
class BrandSettings:
    def __init__(self, settings):
        self.settings = settings

    def get_rules_for_brand(self, brand_name):
        for rule in self.settings['brand_rules']:
            if str(brand_name).lower() in str(rule['names']).lower():
                return rule
        return None
def remove_letters_from_end(s):
    non_letter_index = None
    for i in range(len(s) - 1, -1, -1):
        if not s[i].isalpha():
            non_letter_index = i
            break

    # If there are no non-letter characters, return an empty string
    if non_letter_index is None:
        return s

    # Return the string up to the last non-letter character
    return s[:non_letter_index + 1]

def clean_sku(sku):
    sku = str(sku)
    print(f"Cleaning SKU: {sku}")
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', sku)
    print(f"Cleaned SKU: {cleaned}")
    return cleaned



if __name__=="__main__":
    current_directory=os.getcwd()
    settings_directory=os.path.join(current_directory,"brand_settings.json")
    settings = json.loads(open(settings_directory).read())
    brand_settings = BrandSettings(settings)
    test_settings=brand_settings.get_rules_for_brand("Givenchy")#Temp value needs to be passed in
    test_sku="BB50V9B1UC105"#Temp Value needs to be passed in
    test_SKUManager=SKUManager(test_settings)
    variations=test_SKUManager.generate_variations(test_sku,test_settings)