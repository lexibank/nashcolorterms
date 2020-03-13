from pathlib import Path
import pylexibank
from clldutils.misc import slug


SUPPLEMENT = "https://zenodo.org/record/1032450/files/amended%20PNy%20colour%20vocabs%2020171022.xlsx?download=1"


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "nashcolorterms"

    form_spec = pylexibank.FormSpec(
        brackets={"(": ")", "[": "]"},  # characters that function as brackets
        separators=";/,~",  # characters that split forms e.g. "a, b".
        missing_data=('?', '-'),  # characters that denote missing data.
        strip_inside_brackets=True   # do you want data removed in brackets or not?
    )

    def cmd_download(self, args):
        # Note this downloads the raw data:
        # self.raw_dir.download(SUPPLEMENT, "amended PNy colour vocabs 20171022.xlsx")
        # ... but here we just make this a no-op as we're using a hand-edited version
        # for the datafile as relevant information is formatted
        # using color text in Excel, and it seems that openpyxl cannot handle cells with
        # two font styles in them (specifically here red-strike-through text for errors, and 
        # green text for replacements).
        pass


    def cmd_makecldf(self, args):
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="Name")
        
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory="Name"
        )
        
        for row in self.raw_dir.read_csv("amended PNy colour vocabs 20171022-edited.csv", dicts=True):
            lang = row.pop('language').strip()
            for color in ['black', 'white', 'red', 'yellow', 'green', 'brown', 'blue', 'grey', 'orange']:
                if row[color].strip():
                    lex = args.writer.add_forms_from_value(
                        Language_ID=languages.get(lang, lang),
                        Parameter_ID=concepts[color],
                        Value=row[color].strip(),
                        Source=['Haynie2016', 'Nash2017'],
                    )
