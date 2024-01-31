import re

   
all_tags = (['-privet','[privet s kvadrat skobkami]','-poka'])

def get_tags_without_notes(all_tags):
    return [re.sub(r"\[.*?\]",r"", str(i)) for i in all_tags]

print(*get_tags_without_notes(all_tags),sep='\n')