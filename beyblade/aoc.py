"""Reference content for the Acknowledgement of Country feature.

Shown on the guide page and inside the event create/edit forms. Custodian names are
those commonly acknowledged for each capital city's central area; boundaries and
preferred spellings can differ, so creators are always pointed to local sources too.
"""

# The default acknowledgement used when an event creator picks the generic option
GENERIC_ACKNOWLEDGEMENT = (
    'We acknowledge the Traditional Custodians of the land on which this tournament takes place, '
    'and recognise their continuing connection to land, waters and culture. '
    'We pay our respects to their Elders past and present.'
)

CAPITAL_CUSTODIANS = [
    ('Brisbane', 'QLD', 'Turrbal and Yuggera (Jagera) peoples'),
    ('Sydney', 'NSW', 'Gadigal people of the Eora Nation'),
    ('Melbourne', 'VIC', 'Wurundjeri Woi-wurrung and Bunurong peoples of the Kulin Nation'),
    ('Canberra', 'ACT', 'Ngunnawal people (the Ngambri people are also recognised)'),
    ('Adelaide', 'SA', 'Kaurna people'),
    ('Perth', 'WA', 'Whadjuk people of the Noongar Nation'),
    ('Hobart', 'TAS', 'muwinina people'),
    ('Darwin', 'NT', 'Larrakia people'),
]

RESOURCES = [
    ('AIATSIS Map of Indigenous Australia',
     'https://aiatsis.gov.au/explore/map-indigenous-australia',
     'Shows the general location of language, social or nation groups. It is a guide only and '
     'does not show exact boundaries.'),
    ('AIATSIS: Welcome to and Acknowledgement of Country',
     'https://aiatsis.gov.au/explore/welcome-country',
     'Explains both protocols and how to find out whose Country you are on.'),
    ('Reconciliation Australia: Acknowledgement of Country and Welcome to Country',
     'https://www.reconciliation.org.au/reconciliation/acknowledgement-of-country-and-welcome-to-country/',
     'Guidance on the difference between the two and how to deliver an acknowledgement.'),
    ('Know Your Country',
     'https://www.knowyourcountry.com.au/',
     'A First Nations-led campaign with help to find out the Country you live, work and play on.'),
    ('Your local council or Aboriginal Land Council',
     None,
     'Councils and Land Councils usually publish the Traditional Owners of their area and the '
     'spelling the local community prefers. This is the most reliable source for a specific venue.'),
]

COMMON_MISTAKES = [
    ('Calling it a Welcome to Country',
     'Only Traditional Owners can give a Welcome to Country. Anyone can give an Acknowledgement, '
     'so an event page should never say it is "welcoming" people to Country.'),
    ('Staying generic when the Traditional Owners are known',
     'A generic acknowledgement is better than none, but naming the specific Traditional Owners of '
     'your venue shows you have taken the time to learn whose Country you are on.'),
    ('Guessing, or treating a map as exact',
     'Boundaries and names can be complex or contested, and maps are only a guide. If you are unsure, '
     'check with the local council or Land Council rather than guessing.'),
    ('Talking about Aboriginal people only in the past tense',
     'Recognise a continuing connection to land, waters and culture, not something that ended. '
     'Avoid phrases like "the people who used to live here".'),
    ('Copy-pasting without meaning it',
     'An acknowledgement read as a box-ticking exercise is tokenistic. Write it in your own words '
     'and keep it sincere; it can be short.'),
    ('Misspelling names',
     'Many groups have more than one accepted spelling. Use the spelling preferred by the local '
     'community, as published by local Aboriginal organisations or the council.'),
    ('Adding phrases you are unsure about',
     'Some wording, such as "Elders past, present and emerging", is widely used but debated. '
     '"Elders past and present" is a safe, respectful choice.'),
]

WRITING_PROMPTS = [
    ('Whose Country is your venue on?',
     'Name the Traditional Owners or Custodians of the specific area, using the list below or the '
     'linked sources.'),
    ('Recognise a continuing connection',
     'Acknowledge their ongoing connection to the land, waters and culture of the area.'),
    ('Pay your respects',
     'Pay respects to Elders past and present.'),
    ('Connect it to your event (optional)',
     'Say something genuine about gathering on this Country, for example that your community is '
     'meeting, playing and competing here.'),
    ('Keep it in your own words',
     'Short and sincere is better than long and generic.'),
]
