from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired

countries = ['Afghanistan', 'Akrotiri and Dhekelia', 'Åland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra',
             'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba',
             'Ashmore and Cartier Islands', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas (the)', 'Bahrain',
             'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan',
             'Bolivia (Plurinational State of)', 'Bonaire', 'Sint Eustatius', 'Saba', 'Bosnia and Herzegovina',
             'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory (the)', 'British Virgin Islands',
             'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burma', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon',
             'Canada', 'Cape Verde', 'Caribbean Netherlands', 'Cayman Islands (the)', 'Central African Republic (the)',
             'Chad', 'Chile', 'China', 'China,The Republic of', 'Christmas Island', 'Clipperton Island',
             'Cocos (Keeling) Islands (the)', 'Colombia', 'Comoros (the)', 'Congo (the Democratic Republic of the)',
             'Congo (the)', 'Cook Islands (the)', 'Coral Sea Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba',
             'Curaçao', 'Cyprus', 'Czechia', "Democratic People's Republic of Korea",
             'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic (the)',
             'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'England', 'Equatorial Guinea', 'Eritrea', 'Estonia',
             'Eswatini', 'Ethiopia', 'Falkland Islands (the) [Malvinas]', 'Faroe Islands (the)', 'Fiji', 'Finland',
             'France', 'French Guiana', 'French Polynesia', 'French Southern Territories (the)', 'Gabon',
             'Gambia (the)', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Great Britain', 'Greece', 'Greenland',
             'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti',
             'Hawaiian Islands', 'Heard Island and McDonald Islands', 'Holy See (the)', 'Honduras', 'Hong Kong',
             'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Ireland', 'Isle of Man',
             'Israel', 'Italy', "Ivory Coast", 'Jamaica', 'Jan Mayen', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan',
             'Kenya', 'Kiribati', "Korea (the Democratic People's Republic of)", 'Korea (the Republic of)', 'Kuwait',
             'Kyrgyzstan', "Lao People's Democratic Republic (the)", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
             'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'North Macedonia', 'Madagascar', 'Malawi', 'Malaysia',
             'Maldives', 'Mali', 'Malta', 'Marshall Islands (the)', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte',
             'Mexico', 'Micronesia (Federated States of)', 'Moldova (the Republic of)', 'Monaco', 'Mongolia',
             'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal',
             'Netherlands (the)', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger (the)', 'Nigeria', 'Niue',
             'Norfolk Island', "North Korea", 'Northern Ireland', 'Northern Mariana Islands (the)', 'Norway', 'Oman',
             'Pakistan', 'Palau', 'Palestine,State of', 'Panama', 'Papua New Guinea', 'Paraguay',
             "People's Republic of China", 'Peru', 'Philippines (the)', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico',
             'Qatar', 'Republic of China', 'Republic of Korea', 'Republic of the Congo', 'Réunion', 'Romania',
             'Russian Federation (the)', 'Rwanda', 'Saba', 'Sahrawi Arab Democratic Republic', 'Saint Barthélemy',
             'Saint Helena', 'Ascension Island', 'Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia',
             'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa',
             'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Scotland', 'Senegal', 'Serbia', 'Seychelles',
             'Sierra Leone', 'Singapore', 'Sint Eustatius', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia',
             'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands',
             'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan (the)', 'Suriname', 'Svalbard', 'Jan Mayen',
             'Sweden', 'Switzerland', 'Syrian Arab Republic (the)', 'Taiwan (Province of China)', 'Tajikistan',
             'Tanzania,the United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga',
             'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands (the)', 'Tuvalu',
             'Uganda', 'Ukraine', 'United Arab Emirates (the)',
             'United Kingdom of Great Britain and Northern Ireland (the)', 'United States Minor Outlying Islands (the)',
             'United States of America (the)', 'United States Virgin Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu',
             'Vatican City', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Virgin Islands (British)',
             'Virgin Islands (U.S.)', 'Wales', 'Wallis and Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
regions = ['Республика Адыгея', 'Башкортостан, Республика Башкортостан', 'Республика Бурятия', 'Республика Алтай',
           'Республика Дагестан', 'Ингушетия, Республика Ингушетия', 'Кабардино-Балкарская Республика',
           'Республика Калмыкия', 'Карачаево-Черкесская Республика', 'Карелия, Республика Карелия', 'Республика Коми',
           'Республика Марий Эл', 'Мордовия, Республика Мордовия', 'Республика Саха (Якутия)',
           'Северная Осетия-Алания, Республика', 'Татарстан, Республика Татарстан', 'Тува', 'Удмуртская Республика',
           'Республика Хакасия', 'чеченская Республика', 'Чувашская Республика', 'Алтайский край', 'Краснодарский край',
           'Красноярский край', 'Приморский край', 'Ставропольский край', 'Хабаровский край', 'Амурская область',
           'Архангельская область', 'астраханская область', 'Белгородская область', 'Брянская область',
           'Владимирская область', 'Волгоградская Область', 'Вологодская область', 'Воронежская область',
           'Ивановская область', 'Иркутская область', 'Калининградская область', 'Калужская область', 'Камчатский край',
           'Кемеровская область', 'Кировская область', 'Костромская область', 'курганская область', 'Курская область',
           'Ленинградская область', 'Липецкая область', 'Магаданская область', 'Московская область',
           'Мурманская область', 'Нижегородская Область', 'Новгородская область', 'Новосибирская область',
           'Омская область', 'Оренбургская область', 'Орловская область', 'Пензенская область', 'Пермский край',
           'Псковская область', 'Ростовская область', 'Рязанская область', 'Самарская область', 'Саратовская область',
           'Сахалинская область', 'Свердловская область', 'Смоленская область', 'Тамбовская Область',
           'Тверская область', 'Томская область', 'Тульская Область', 'Тюменская область', 'Ульяновская область',
           'Челябинская область', 'Забайкальский Край', 'Ярославская область', 'Москва', 'Санкт-Петербург',
           'еврейская автономная область', 'Ненецкий автономный округ', 'Ханты-Мансийский Автономный Округ-Югра',
           'Чукотский автономный округ', 'Ямало-Ненецкий Автономный Округ', 'Республика Крым',
           'Севастополь']


class RegisterForm(FlaskForm):
    label = "Имя"
    first_name = StringField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "type": "name",
        "placeholder": label
    })

    label = "Фамилия"
    last_name = StringField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "type": "surname",
        "placeholder": label
    })

    label = "Страна"
    country = SelectField(label, choices=countries, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "id": "cntry-fld",
        "placeholder": label
    })

    label = "Регион"
    region = SelectField(label, choices=regions, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "display": None,
        "placeholder": label
    })

    label = "Email"
    email = StringField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "type": "email",
        "placeholder": label
    })

    label = "Пароль"
    password = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    label = "Повторите пароль"
    password_again = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "input-str form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    photo = FileField("Выберите изображение", render_kw={
        "class": "form-control-file",
        "id": "photoField"
    })
    label = "OK"
    submit = SubmitField(label, render_kw={
        "class": "",
        "placeholder": label
    })
