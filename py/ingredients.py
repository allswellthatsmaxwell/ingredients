import pandas as pd
from scipy import stats

from typing import List, Dict


def map_yes_no(s):
    s = s.lower()
    if s == 'yes':
        return 1
    elif s == 'no':
        return 0
    else:
        raise ValueError(f"Unexpected value: {s}; need 'yes' or 'no'")

def rename(ingredient):
    s = ingredient.lower().strip().strip('.')
    if 'aloe' in s:
        return 'aloe vera'
    elif 'avena sativa' in s:
        return 'avena sativa'
    elif 'capry' in s and 'lycol' in s:
        return 'caprylyl lycol'
    elif 'propylene' in s and 'lycol' in s:
        return 'propylene gylcol'
    elif 'butyrospermum' in s:
        return 'shea butter'
    elif 'tocopherol' in s:  # questionable
        return 'tocopherols'
    elif 'polysorbate' in s:
        return 'polysorbate'
    elif 'jojoba' in s:
        return 'jojoba'
    elif 'fragrance' in s:
        return 'fragrance'
    elif 'decyl glucoside' in s:
        return 'decyl glucoside'
    elif s.startswith('ce') and 'alcohol' in s:
        return 'cetyl alcohol'
    elif 'cocos nucifera' in s:
        return 'cocos nucifera'
    return s


class Ingredients:
    def __init__(self, dat):
        self.dat = dat

    @property
    def ingredient_cols(self) -> List[str]:
        return [c for c in self.dat.columns if "ingredient" in c.lower()]

    @property
    def groups_to_hits(self):
        groups_to_hits = {}
        for brand, groups in self.names_to_groups.items():
            for group in groups:
                if group not in groups_to_hits:
                    groups_to_hits[group] = []
                groups_to_hits[group].append(self.brand_allergy_status[brand])
        return groups_to_hits

    @property
    def stats_dat(self) -> Dict[str, float]:
        rows = []
        for name, hits in self.groups_to_hits.items():
            n = len(hits)
            alpha = sum(hits)
            beta = n - alpha
            mu = round(float(stats.beta(alpha + 1, beta + 1).mean()), 2)
            rows.append((name, mu, alpha, n))
        return (
            pd.DataFrame(rows, columns=['group', 'posterior_mean', 'allergy_hits', 'nproducts'])
            .sort_values('posterior_mean', ascending=False))

    @property
    def names_to_ingredients(self) -> Dict[str, List[str]]:
        names_to_ingredients = {}
        for _, row in self.dat.iterrows():
            brand = row['Brand']
            names_to_ingredients[brand] = []
            for col in self.ingredient_cols:
                ingredient = row[col]
                if not pd.isnull(ingredient):
                    names_to_ingredients[brand].append(rename(ingredient))
        return names_to_ingredients

    @property
    def brand_allergy_status(self) -> Dict[str, str]:
        return dict(zip(self.dat['Brand'],
                        self.dat['Symptoms?'].apply(map_yes_no)))

    @property
    def unique_ingredients(self) -> List[str]:
        unique_ingredients = set()
        for entries in self.names_to_ingredients.values():
            unique_ingredients.update(entries)
        return sorted(set(unique_ingredients))

    @property
    def ingredient_to_group(self) -> Dict[str, str]:
        ingredient_to_group = {}
        for group, ingredients in group_to_ingredients.items():
            for ing in ingredients:
                if ing not in ingredient_to_group:
                    ingredient_to_group[ing] = []
                ingredient_to_group[ing] = group
        return ingredient_to_group

    @property
    def names_to_groups(self):
        names_to_groups = {}
        for name, ingredients in self.names_to_ingredients.items():
            names_to_groups[name] = set([self.ingredient_to_group[ing]
                                         for ing in ingredients])
        return names_to_groups


group_to_ingredients = ingredient_groups = {
    "Water": [
        "water"
    ],

    "Vitamins": [
        "panthenol",
        "panthenol (vitamin b)",
        "cholecalciferol (vitamin d)",
        "tocopherols",
        "tocopheryl acetate",
        "ascorbic acid",
        "sodium ascorbyl",
        "magnesium ascorbyl phosphate",
        "biotin"
    ],

    "Aloe": [
        "aloe vera"
    ],

    "Acids_and_Salts": [
        "lactic acid",
        "sodium lactate",
        "pca",
        "sodium pca",
        "citric acid",
        "glycolic acid",
        "hyaluronic acid",
        "sodium hyaluronate",
        "linoleic acid",
        "oleic acid",
        "palmitic acid",
        "stearic acid",
        "benzoic acid",
        "sodium benzoate",
        "lauryl lactate",
        "sodium carbonate",
        "sodium hydroxide",
        "ammonium chloride",
        "sodium chloride",
        "phosphate",
        "gluconolactone",
        "vinegar"
    ],

    "Coconut_Derivatives": [
        "cocos nucifera",
        "sodium cocoyl glutamate (coconut source)",
        "cocamidopropyl betaine",
        "cocamidopropyl hydroxysultaine",
        "cocamidopropyl pg-dimonium chloride",
        "cocamide mipa",
        "disodium cocamido mipa sulfosuccinate",
        "coco glucoside",
        "peg-6 caprylic/capric glycerides",
        "sodium cocoyl isethionate"
    ],

    "Citrus_Oils": [
        "citrus aurantium bergamia (bergamot) fruit oil",
        "citrus aurantium dulcis (orange) peel oil",
        "citrus limon (lemon) peel oil",
        "citrus medica limonum (lemon) peel extract",
        "citrus reticulata (tangerine) leaf oil",
        "orange oil",
        "mandarin oil",
        "terpenesandterpenoids,lemon-oil",
        "limonene",
        "citral",
        "lime pearl fruit extract"
    ],

    "Lavender_Herbal_Oils": [
        "lavandula angustifolia (lavender) oil",
        "rosmarinus officinalis (rosemary) leaf oil",
        "rosemary oil"
    ],

    "Preservatives": [
        "phenoxyethanol",
        "methylchloroisothiazolinone",
        "methylisothiazolinone",
        "benzoic acid",
        "sodium benzoate",
        "potassium sorbate",
        "disodium dmdm hydantoin",
        "caprylhydroxamic acid",
        "chlorphenesin",
        "ethylhexylglycerin",
        "disodium edta",
        "tetrasodium edta",
        "tetrasodium glda",
        "tetrasodium glutamate diacetate",
        "trisodium ethylenediamine disuccinate",
        "hydroxyacetophenone"
    ],

    "Cleaning_Agents": [
        "sodium lauryl sulfate",
        "ammonium lauryl sulfate",
        "sodium c14-16 olefin sulfonate",
        "sodium lauroyl methyl lsethionate",
        "sodium cocoyl isethionate",
        "sodium methyl cocoyl taurate",
        "decyl glucoside",
        "sodium methyl 2-sulfolaurate",
        "disodium 2-sulfolaurate",
        "cocamidopropyl betaine",
        "cetyl betaine",
        "betaine",
        "laureth-7",
        "polysorbate",
        "polyglyceryl-3 laurate"
    ],

    "Alcohols": [
        "cetyl alcohol",
        "stearyl alcohol",
        "benzyl alcohol",
        "isopropyl alcohol",
        "2-hexanediol",
        "isopropyl palmitate",
        "benzyl acetate",
        "benzyl benzoate"
    ],

    "Emollients": [
        "petrolatum",
        "white petrolatum",
        "glycerin",
        "glycerin (vegetable)",
        "butylene glycol",
        "propylene gylcol",
        "pentylene glycol",
        "caprylyl lycol",
        "caprylic/capric triglyceride",
        "propanediol",
        "methyl glucose caprate/caprylate/oleate",
        "shea butter",
        "triolein",
        "triethyl citrate"
    ],

    "Essential_Oils": [
        "patchouli oil",
        "pogostemon cablin (patchouli) oil",
        "cedarwood oil",
        "cedar leaf oil",
        "eucalyptus globolus (eucalyptus) leaf oil",
        "mentha piperita (peppermint) oil",
        "cymbopogon schoenanthus (lemongrass) oil",
        "abies alba (fir) leaf oil",
        "amyris oil",
        "basilicum (basil) oil",
        "bois de rose oil",
        "cypress oil",
        "salvia officinalis (sage) oil",
        "olibanum oil",
        "guaiacwood oil",
        "gurjun balsalm oil",
        "melalueca alternifolia (tea tree) leaf oil",
        "menthol",
        "ocimum",
        "chouji yu"
    ],

    "Amino_Acids": [
        "alanine",
        "arginine",
        "l-arginine",
        "aspartic acid",
        "glycine",
        "histidine",
        "isoleucine",
        "phenylalanine",
        "proline",
        "serine",
        "threonine",
        "valine",
        "hydrolyzed pea protein",
        "hydrolyzed quinoa"
    ],

    "Fragrance_Components": [
        "fragrance",
        "parfum (natural)",
        "linalool",
        "geraniol",
        "citronellol",
        "hydroxycitronellal",
        "linalyl acetate",
        "benzyl acetate",
        "benzyl benzoate",
        "tetramethyl acetyloctahydronaphthalenes",
        "methyl ionones",
        "4-tert-butylcyclohexyl acetate",
        "limonene",
        "citral"
    ],

    "Plant_Oils": [
        "persea gratissima (avocado) oil",
        "prunus amygdalus dulcis (sweet almond) oil",
        "ricinus communis (castor) seed oil",
        "carthamus tinctorius (safflower) seed oil",
        "oenothera biennis (evening primrose) oil",
        "glycine soja (soybean) oil",
        "olea europaea (olive) fruit oil",
        "elaeis guineensis (palm kernel) oil",
        "oryza sativa (rice) bran oil",
        "triticum vulgare (wheat) germ oil",
        "vitis vinifera (grape) seed oil",
        "rosa canina fruit oil",
        "pequi fruit oil",
        "sunflower seed oil",
        "oat kernel oil",
        "jojoba",
        "peg-40 hydrogenated castor oil"
    ],

    "Thickeners_Stabilizers": [
        "xanthan gum",
        "carbomer",
        "acrylates copolymer",
        "acrylates/c10-30 alkylacrylate crosspolymer",
        "tara spinosa gum",
        "acacia seyal gum extract",
        "polyquaternium-10",
        "polyquaternium-7",
        "silica",
        "guar hydroxypropyltrimonium chloride",
        "glyceryl oleate",
        "peg-150 pentaerythrityl tetrastearate",
        "phytosteryl canola glycerides",
        "isoceteth-20",
        "stearetf-20"
    ],

    "Plant_Extracts": [
        "equisetum arvense (horsetail) extract",
        "urtica dioica (nettle) extract",
        "arctium lappa (burdock) root extract",
        "arnica montana flower extract",
        "grape seed extract",
        "flax seed extract",
        "baobab seed extract",
        "apium graveolens (celery) seed extract",
        "chamomile recutita (matricaria) flower extract",
        "camellia sinensis (white tea) extract",
        "brassica oleracea acephala leaf (kale) extract",
        "garcinia mangostana (mangosteen) extract",
        "crambe maritima leaf (blue seakale) extract",
        "avena sativa"
    ],

    "Minerals": [
        "silica",
        "kaolin",
        "iron oxides"
    ],

    "Colorants": [
        "iron oxides",
        "caramel",
        "ci 60730 (ext. violet 2)",
        "yellow 6",
        "chlorophyllinum cupreum (chlorophyll)"
    ],

    "Vasodilators_Actives": [
        "benzyl nicotinate"
    ],

    "Quaternary_Ammonium_Compounds": [
        "behentrimonium chloride",
        "distearyldimonium chloride",
        "polyquaternium-7",
        "polyquaternium-10",
        "guar hydroxypropyltrimonium chloride"
    ],

    "Chelating_Agents": [
        "disodium edta",
        "tetrasodium edta",
        "tetrasodium glda",
        "tetrasodium glutamate diacetate",
        "trisodium ethylenediamine disuccinate"
    ],

    "Humectants": [
        "glycerin",
        "glycerin (vegetable)",
        "hyaluronic acid",
        "sodium hyaluronate",
        "propylene gylcol",
        "butylene glycol",
        "trehalose",
        "urea",
        "sodium pca",
        "pca",
        "allantoin"
    ],

    "Sugars_Carbohydrates": [
        "glucose",
        "fructose",
        "maltose",
        "trehalose"
    ],

    "Silicones": [
        "peg-7 dimethicone"
    ],

    "UV_Filters": [
        "benzophenone-4"
    ],

    "Fatty_Acids": [
        "linoleic acid",
        "oleic acid",
        "palmitic acid",
        "stearic acid"
    ],

    "Animal_Derivatives": [
        "caprae lac (goat milk)"
    ],

    "Ferments": [
        "pichia ferment lysate filtrate",
        "saccharomyces/xylinum/black tea ferment"
    ],

    "Alkalizing_Agents": [
        "triethanolamine",
        "sodium hydroxide",
        "theobroma cacao (cocoa pod) potash"
    ],

    "Phospholipids": [
        "phospholipids",
        "lecithin"
    ]
}
