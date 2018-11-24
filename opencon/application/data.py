
OCCUPATION_CHOICES = [
    ('undergraduate', 'Undergraduate Student (studying for bachelor’s degree)'),
    ('master', 'Masters / Professional Student (studying for master’s or professional degree)'),
    ('phd', 'PhD Candidate (studying for PhD)'),
    ('postdoc', 'Post-Doc'),
    ('professor', 'Professor / Teacher'),
    ('research', 'Researcher'),
    ('librarian', 'Librarian'),
    ('nonacademic', 'Non-Academic University Staff'),
    ('publisher', 'Publisher'),
    ('government', 'Government Employee / Civil Servant'),
    ('nonprofit', 'Non Profit / NGO Employee'),
    ('journalist', 'Journalist / Blogger'),
    ('doctor', 'Doctor / Medical Professional'),
    ('lawyer', 'Lawyer / Legal Professional'),
    ('philanthropist', 'Philanthropist'),
    ('developer', 'Software / Technology Developer'),
    ('businessman', 'Businessperson / Entrepreneur'),
    ('none', 'None of these describes me'),
]

DEGREE_CHOICES = [
    ('bachelor', 'Bachelor’s Degree (BA, BS, etc.)'),
    ('master', 'Master’s Degree (MBA, MFA, etc.)'),
    ('professional', 'Professional Degree (MD, JD, etc.)'),
    ('phd', 'PhD'),
    ('other_postgraduate', 'Other Postgraduate Degree'),
    ('other_professional', 'Other Professional Certification'),
    ('none', 'None of the above'),
]

EXPERIENCE_CHOICES = [
    ('0', '0 (still in school full time or just starting first career)'),
    ('upto5', '1-5 years'),
    ('upto10', '6-10 years'),
    ('upto15', '11-15 years'),
    ('more16', '16+ years'),
]

FIELDS_OF_STUDY_CHOICES = [
    (None, 'Please select an option below'),
    ('01', 'Agricultural Sciences - Agricultural biotechnology'),
    ('02', 'Agricultural Sciences - Agriculture, forestry, and fisheries'),
    ('03', 'Agricultural Sciences - Animal and dairy science'),
    ('04', 'Agricultural Sciences - Other agricultural sciences'),
    ('05', 'Agricultural Sciences - Veterinary science'),
    ('06', 'Engineering/Technology - Chemical engineering'),
    ('07', 'Engineering/Technology - Civil engineering'),
    ('08', 'Engineering/Technology - Electrical engineering, electronic engineering, information engineering'),
    ('09', 'Engineering/Technology - Environmental biotechnology'),
    ('10', 'Engineering/Technology - Environmental engineering'),
    ('11', 'Engineering/Technology - Industrial Biotechnology'),
    ('12', 'Engineering/Technology - Materials engineering'),
    ('13', 'Engineering/Technology - Mechanical engineering'),
    ('14', 'Engineering/Technology - Medical engineering'),
    ('15', 'Engineering/Technology - Nano-technology'),
    ('16', 'Engineering/Technology - Other engineering and technologies'),
    ('17', 'Humanities - Art (arts, history of arts, performing arts, music)'),
    ('18', 'Humanities - History and archaeology'),
    ('19', 'Humanities - Languages and literature'),
    ('20', 'Humanities - Other humanities'),
    ('21', 'Humanities - Philosophy, ethics and religion'),
    ('22', 'Medicine/Health Sciences - Basic medicine'),
    ('23', 'Medicine/Health Sciences - Clinical medicine'),
    ('24', 'Medicine/Health Sciences - Health biotechnology'),
    ('25', 'Medicine/Health Sciences - Health sciences'),
    ('26', 'Medicine/Health Sciences - Other medical sciences'),
    ('27', 'Natural Sciences - Biological sciences'),
    ('28', 'Natural Sciences - Chemical sciences'),
    ('29', 'Natural Sciences - Computer and information sciences (incl. library and information science)'),
    ('30', 'Natural Sciences - Earth and related environmental sciences'),
    ('31', 'Natural Sciences - Mathematics'),
    ('32', 'Natural Sciences - Other natural sciences'),
    ('33', 'Natural Sciences - Physical sciences'),
    ('34', 'Social Sciences - Economics and business'),
    ('35', 'Social Sciences - Educational sciences'),
    ('36', 'Social Sciences - Law'),
    ('37', 'Social Sciences - Media and communications'),
    ('38', 'Social Sciences - Other social sciences'),
    ('39', 'Social Sciences - Political Science'),
    ('40', 'Social Sciences - Psychology'),
    ('41', 'Social Sciences - Social and economic geography'),
    ('42', 'Social Sciences - Sociology'),
    ('none', 'None of these describe my field of study'),
]

AREA_OF_INTEREST_CHOICES = [
    ('open_access', 'Open Access'),
    ('open_education', 'Open Education'),
    ('open_research', 'Open Research Data'),
    ('open_government', 'Open Government Data'),
    ('open_science', 'Open Research / Open Science'),
    ('open_source', 'Free and Open Source Software'),
]

PARTICIPATION_CHOICES = [
    ('openaccessweek', 'Open Access Week'),
    ('openeducationweek', 'Open Education Week'),
    ('opendataday', 'Open Data Day'),
    ('none', 'None of the above'),
]

VISA_CHOICES = [
    ('local_person', 'I have a U.S. or Canadian passport and/or will already be in the U.S. in November 2016'),
    ('visa_waiver', 'I am eligible to travel to the U.S. under the Visa Waiver Program'),
    ('have_visa', 'I already have a U.S. visa that will be valid through November 2016'),
    ('need_visa', 'I do not have a visa and would need one to travel to the U.S.'),
    ('not_sure', 'I’m not sure'),
]

SKILLS_CHOICES = [
    ('advocacy', 'Advocacy and Policy'),
    ('blogging', 'Blogging'),
    ('comms', 'Communications / Media Relations'),
    ('community', 'Community / Grassroots Organizing'),
    ('socialmedia', 'Social Media Campaigns'),
    ('fudraising', 'Fundraising'),
    ('events', 'Event Logistics'),
    ('volunteers', 'Volunteer Management'),
    ('graphics', 'Graphic Design'),
    ('video', 'Video Editing'),
    ('research', 'Research About Open Access / Open Education / Open Data'),
    ('software', 'Software Development'),
    ('other', 'Other'),
]

EXPENSES_CHOICES = [
    ('transport', 'Transportation to and from Washington, D.C.'),
    ('accomodation', 'Accommodation during the conference'),
    ('conference_fee', 'Conference fee (approx. $300 and includes most meals)'),
    ('visa_fee', 'Visa application fee, if needed (typically $190)'),
    ('none', 'None of the above'),
]

ACKNOWLEDGEMENT_CHOICES = [
    ('ack_privacy', 'I understand that my contact information and other information I provide in this application '
          'will be handled according to OpenCon’s Privacy Policy.'),
    ('ack_share_reviewers', 'I understand that the information I provide in this application will be shared with '
          'members of the OpenCon 2016 Application Review Team for purposes of evaluation.'),
    ('ack_share_sponsors', 'I understand that if I have requested a scholarship, the information I provide in this '
          'application may be shared with sponsors for the purposes of selecting a participant to sponsor.'),
    ('ack_opendata', 'I understand that my responses to the questions marked with a caret (^) may be released '
          'publicly as Open Data under a CC0 license.'),
]

OPT_OUTS_CHOICES = [
    ('no_mailinglists', 'Please DO NOT add me to the OpenCon and Right to Research Coalition mailing lists.'),
    ('no_opportunities', 'Please DO NOT use my application to consider me for future opportunities relating to the '
          'mission of OpenCon (e.g. scholarships to related conferences, events in your area, opportunities for '
          'collaboration).'),
]

HOW_DID_YOU_FIND_OUT_CHOICES = [
    ('websearch', 'Internet Search'),
    ('twitter', 'Twitter'),
    ('facebook', 'Facebook'),
    ('blogpost', 'Blog Post'),
    ('mailinglist', 'E-mail List'),
    ('webcast', 'Webcast'),
    ('poster', 'Poster'),
    ('friend', 'Friend / Colleague'),
    ('organization', 'Organization'),
    ('other', 'Other'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('noanswer', 'Prefer not to answer'),
    ('other', 'I will write my gender in the box below'),
]

COUNTRY_LIST="""
    Afghanistan
    Albania
    Algeria
    Andorra
    Angola
    Antigua and Barbuda
    Argentina
    Armenia
    Aruba
    Australia
    Austria
    Azerbaijan
    Bahamas, The
    Bahrain
    Bangladesh
    Barbados
    Belarus
    Belgium
    Belize
    Benin
    Bhutan
    Bolivia
    Bosnia and Herzegovina
    Botswana
    Brazil
    Brunei
    Bulgaria
    Burkina Faso
    Burma
    Burundi
    Cambodia
    Cameroon
    Canada
    Cape Verde
    Central African Republic
    Chad
    Chile
    China
    Colombia
    Comoros
    Congo, Democratic Republic of the
    Congo, Republic of the
    Costa Rica
    Cote d'Ivoire
    Croatia
    Cuba
    Curacao
    Cyprus
    Czech Republic
    Denmark
    Djibouti
    Dominica
    Dominican Republic
    East Timor
    Ecuador
    Egypt
    El Salvador
    Equatorial Guinea
    Eritrea
    Estonia
    Ethiopia
    Fiji
    Finland
    France
    Gabon
    Gambia
    Georgia
    Germany
    Ghana
    Greece
    Grenada
    Guatemala
    Guinea
    Guinea-Bissau
    Guyana
    Haiti
    Holy See
    Honduras
    Hong Kong
    Hungary
    Iceland
    India
    Indonesia
    Iran
    Iraq
    Ireland
    Israel
    Italy
    Jamaica
    Japan
    Jordan
    Kazakhstan
    Kenya
    Kiribati
    Kosovo
    Kuwait
    Kyrgyzstan
    Laos
    Latvia
    Lebanon
    Lesotho
    Liberia
    Libya
    Liechtenstein
    Lithuania
    Luxembourg
    Macau
    Macedonia
    Madagascar
    Malawi
    Malaysia
    Maldives
    Mali
    Malta
    Marshall Islands
    Mauritania
    Mauritius
    Mexico
    Micronesia
    Moldova
    Monaco
    Mongolia
    Montenegro
    Morocco
    Mozambique
    Namibia
    Nauru
    Nepal
    Netherlands
    Netherlands Antilles
    New Zealand
    Nicaragua
    Niger
    Nigeria
    North Korea
    Norway
    Oman
    Pakistan
    Palau
    Palestinian Territories
    Panama
    Papua New Guinea
    Paraguay
    Peru
    Philippines
    Poland
    Portugal
    Qatar
    Romania
    Russia
    Rwanda
    Saint Kitts and Nevis
    Saint Lucia
    Saint Vincent and the Grenadines
    Samoa
    San Marino
    Sao Tome and Principe
    Saudi Arabia
    Senegal
    Serbia
    Seychelles
    Sierra Leone
    Singapore
    Sint Maarten
    Slovakia
    Slovenia
    Solomon Islands
    Somalia
    South Africa
    South Korea
    South Sudan
    Spain
    Sri Lanka
    Sudan
    Suriname
    Swaziland
    Sweden
    Switzerland
    Syria
    Taiwan
    Tajikistan
    Tanzania
    Thailand
    Timor-Leste
    Togo
    Tonga
    Trinidad and Tobago
    Tunisia
    Turkey
    Turkmenistan
    Tuvalu
    Uganda
    Ukraine
    United Arab Emirates
    United Kingdom
    United States of America
    Uruguay
    Uzbekistan
    Vanuatu
    Venezuela
    Vietnam
    Yemen
    Zambia
    Zimbabwe
    Country Not Listed
"""

COUNTRY_CHOICES = [(None, 'Please select an option below')]
COUNTRY_CHOICES += [((c.strip(), c.strip())) for c in COUNTRY_LIST.strip().split('\n')]
# note "Other" option added to the original list of countries (because of the instructions)
