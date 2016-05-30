from django.contrib.gis.db import models
from django.contrib.auth.models import User as OrigUser

# Create your models here.


class User(OrigUser):
    institution = models.CharField(max_length=400)
                             

class ProvChange(models.Model):

    changeid = models.IntegerField(null=True)
    bestversion = models.BooleanField(default=False)

    user = models.CharField(max_length=200)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Pending","Pending"),
                                       ("Accepted","Accepted"),
                                       ("NonActive","NonActive"),
                                        ],
                              default="Pending",
                              max_length=40)

    #import pycountries as pc
    source = models.CharField(max_length=400)
    country = models.CharField(choices=[(u'Afghanistan', u'Afghanistan'), (u'\xc5land Islands', u'\xc5land Islands'), (u'Albania', u'Albania'), (u'Algeria', u'Algeria'), (u'American Samoa', u'American Samoa'), (u'Andorra', u'Andorra'), (u'Angola', u'Angola'), (u'Anguilla', u'Anguilla'), (u'Antigua and Barbuda', u'Antigua and Barbuda'), (u'Argentina', u'Argentina'), (u'Armenia', u'Armenia'), (u'Aruba', u'Aruba'), (u'Australia', u'Australia'), (u'Austria', u'Austria'), (u'Azerbaijan', u'Azerbaijan'), (u'The Bahamas', u'The Bahamas'), (u'Bahrain', u'Bahrain'), (u'Bangladesh', u'Bangladesh'), (u'Barbados', u'Barbados'), (u'Belarus', u'Belarus'), (u'Belgium', u'Belgium'), (u'Belize', u'Belize'), (u'Benin', u'Benin'), (u'Bermuda', u'Bermuda'), (u'Bhutan', u'Bhutan'), (u'Bolivia', u'Bolivia'), (u'Bonaire', u'Bonaire'), (u'Bosnia and Herzegovina', u'Bosnia and Herzegovina'), (u'Botswana', u'Botswana'), (u'Bouvet Island', u'Bouvet Island'), (u'Brazil', u'Brazil'), (u'British Indian Ocean Territory', u'British Indian Ocean Territory'), (u'United States Minor Outlying Islands', u'United States Minor Outlying Islands'), (u'British Virgin Islands', u'British Virgin Islands'), (u'Brunei', u'Brunei'), (u'Bulgaria', u'Bulgaria'), (u'Burkina Faso', u'Burkina Faso'), (u'Burundi', u'Burundi'), (u'Cambodia', u'Cambodia'), (u'Cameroon', u'Cameroon'), (u'Canada', u'Canada'), (u'Cape Verde', u'Cape Verde'), (u'Cayman Islands', u'Cayman Islands'), (u'Central African Republic', u'Central African Republic'), (u'Chad', u'Chad'), (u'Chile', u'Chile'), (u'China', u'China'), (u'Christmas Island', u'Christmas Island'), (u'Cocos (Keeling) Islands', u'Cocos (Keeling) Islands'), (u'Colombia', u'Colombia'), (u'Comoros', u'Comoros'), (u'Republic of the Congo', u'Republic of the Congo'), (u'Democratic Republic of the Congo', u'Democratic Republic of the Congo'), (u'Cook Islands', u'Cook Islands'), (u'Costa Rica', u'Costa Rica'), (u'Croatia', u'Croatia'), (u'Cuba', u'Cuba'), (u'Cura\xe7ao', u'Cura\xe7ao'), (u'Cyprus', u'Cyprus'), (u'Czech Republic', u'Czech Republic'), (u'Denmark', u'Denmark'), (u'Djibouti', u'Djibouti'), (u'Dominica', u'Dominica'), (u'Dominican Republic', u'Dominican Republic'), (u'Ecuador', u'Ecuador'), (u'Egypt', u'Egypt'), (u'El Salvador', u'El Salvador'), (u'Equatorial Guinea', u'Equatorial Guinea'), (u'Eritrea', u'Eritrea'), (u'Estonia', u'Estonia'), (u'Ethiopia', u'Ethiopia'), (u'Falkland Islands', u'Falkland Islands'), (u'Faroe Islands', u'Faroe Islands'), (u'Fiji', u'Fiji'), (u'Finland', u'Finland'), (u'France', u'France'), (u'French Guiana', u'French Guiana'), (u'French Polynesia', u'French Polynesia'), (u'French Southern and Antarctic Lands', u'French Southern and Antarctic Lands'), (u'Gabon', u'Gabon'), (u'The Gambia', u'The Gambia'), (u'Georgia', u'Georgia'), (u'Germany', u'Germany'), (u'Ghana', u'Ghana'), (u'Gibraltar', u'Gibraltar'), (u'Greece', u'Greece'), (u'Greenland', u'Greenland'), (u'Grenada', u'Grenada'), (u'Guadeloupe', u'Guadeloupe'), (u'Guam', u'Guam'), (u'Guatemala', u'Guatemala'), (u'Guernsey', u'Guernsey'), (u'Guinea', u'Guinea'), (u'Guinea-Bissau', u'Guinea-Bissau'), (u'Guyana', u'Guyana'), (u'Haiti', u'Haiti'), (u'Heard Island and McDonald Islands', u'Heard Island and McDonald Islands'), (u'Honduras', u'Honduras'), (u'Hong Kong', u'Hong Kong'), (u'Hungary', u'Hungary'), (u'Iceland', u'Iceland'), (u'India', u'India'), (u'Indonesia', u'Indonesia'), (u'Ivory Coast', u'Ivory Coast'), (u'Iran', u'Iran'), (u'Iraq', u'Iraq'), (u'Republic of Ireland', u'Republic of Ireland'), (u'Isle of Man', u'Isle of Man'), (u'Israel', u'Israel'), (u'Italy', u'Italy'), (u'Jamaica', u'Jamaica'), (u'Japan', u'Japan'), (u'Jersey', u'Jersey'), (u'Jordan', u'Jordan'), (u'Kazakhstan', u'Kazakhstan'), (u'Kenya', u'Kenya'), (u'Kiribati', u'Kiribati'), (u'Kuwait', u'Kuwait'), (u'Kyrgyzstan', u'Kyrgyzstan'), (u'Laos', u'Laos'), (u'Latvia', u'Latvia'), (u'Lebanon', u'Lebanon'), (u'Lesotho', u'Lesotho'), (u'Liberia', u'Liberia'), (u'Libya', u'Libya'), (u'Liechtenstein', u'Liechtenstein'), (u'Lithuania', u'Lithuania'), (u'Luxembourg', u'Luxembourg'), (u'Macau', u'Macau'), (u'Republic of Macedonia', u'Republic of Macedonia'), (u'Madagascar', u'Madagascar'), (u'Malawi', u'Malawi'), (u'Malaysia', u'Malaysia'), (u'Maldives', u'Maldives'), (u'Mali', u'Mali'), (u'Malta', u'Malta'), (u'Marshall Islands', u'Marshall Islands'), (u'Martinique', u'Martinique'), (u'Mauritania', u'Mauritania'), (u'Mauritius', u'Mauritius'), (u'Mayotte', u'Mayotte'), (u'Mexico', u'Mexico'), (u'Federated States of Micronesia', u'Federated States of Micronesia'), (u'Moldova', u'Moldova'), (u'Monaco', u'Monaco'), (u'Mongolia', u'Mongolia'), (u'Montenegro', u'Montenegro'), (u'Montserrat', u'Montserrat'), (u'Morocco', u'Morocco'), (u'Mozambique', u'Mozambique'), (u'Myanmar', u'Myanmar'), (u'Namibia', u'Namibia'), (u'Nauru', u'Nauru'), (u'Nepal', u'Nepal'), (u'Netherlands', u'Netherlands'), (u'New Caledonia', u'New Caledonia'), (u'New Zealand', u'New Zealand'), (u'Nicaragua', u'Nicaragua'), (u'Niger', u'Niger'), (u'Nigeria', u'Nigeria'), (u'Niue', u'Niue'), (u'Norfolk Island', u'Norfolk Island'), (u'North Korea', u'North Korea'), (u'Northern Mariana Islands', u'Northern Mariana Islands'), (u'Norway', u'Norway'), (u'Oman', u'Oman'), (u'Pakistan', u'Pakistan'), (u'Palau', u'Palau'), (u'Palestine', u'Palestine'), (u'Panama', u'Panama'), (u'Papua New Guinea', u'Papua New Guinea'), (u'Paraguay', u'Paraguay'), (u'Peru', u'Peru'), (u'Philippines', u'Philippines'), (u'Pitcairn Islands', u'Pitcairn Islands'), (u'Poland', u'Poland'), (u'Portugal', u'Portugal'), (u'Puerto Rico', u'Puerto Rico'), (u'Qatar', u'Qatar'), (u'Republic of Kosovo', u'Republic of Kosovo'), (u'R\xe9union', u'R\xe9union'), (u'Romania', u'Romania'), (u'Russia', u'Russia'), (u'Rwanda', u'Rwanda'), (u'Saint Barth\xe9lemy', u'Saint Barth\xe9lemy'), (u'Saint Helena', u'Saint Helena'), (u'Saint Kitts and Nevis', u'Saint Kitts and Nevis'), (u'Saint Lucia', u'Saint Lucia'), (u'Saint Martin', u'Saint Martin'), (u'Saint Pierre and Miquelon', u'Saint Pierre and Miquelon'), (u'Saint Vincent and the Grenadines', u'Saint Vincent and the Grenadines'), (u'Samoa', u'Samoa'), (u'San Marino', u'San Marino'), (u'S\xe3o Tom\xe9 and Pr\xedncipe', u'S\xe3o Tom\xe9 and Pr\xedncipe'), (u'Saudi Arabia', u'Saudi Arabia'), (u'Senegal', u'Senegal'), (u'Serbia', u'Serbia'), (u'Seychelles', u'Seychelles'), (u'Sierra Leone', u'Sierra Leone'), (u'Singapore', u'Singapore'), (u'Sint Maarten', u'Sint Maarten'), (u'Slovakia', u'Slovakia'), (u'Slovenia', u'Slovenia'), (u'Solomon Islands', u'Solomon Islands'), (u'Somalia', u'Somalia'), (u'South Africa', u'South Africa'), (u'South Georgia', u'South Georgia'), (u'South Korea', u'South Korea'), (u'South Sudan', u'South Sudan'), (u'Spain', u'Spain'), (u'Sri Lanka', u'Sri Lanka'), (u'Sudan', u'Sudan'), (u'Suriname', u'Suriname'), (u'Svalbard and Jan Mayen', u'Svalbard and Jan Mayen'), (u'Swaziland', u'Swaziland'), (u'Sweden', u'Sweden'), (u'Switzerland', u'Switzerland'), (u'Syria', u'Syria'), (u'Taiwan', u'Taiwan'), (u'Tajikistan', u'Tajikistan'), (u'Tanzania', u'Tanzania'), (u'Thailand', u'Thailand'), (u'East Timor', u'East Timor'), (u'Togo', u'Togo'), (u'Tokelau', u'Tokelau'), (u'Tonga', u'Tonga'), (u'Trinidad and Tobago', u'Trinidad and Tobago'), (u'Tunisia', u'Tunisia'), (u'Turkey', u'Turkey'), (u'Turkmenistan', u'Turkmenistan'), (u'Turks and Caicos Islands', u'Turks and Caicos Islands'), (u'Tuvalu', u'Tuvalu'), (u'Uganda', u'Uganda'), (u'Ukraine', u'Ukraine'), (u'United Arab Emirates', u'United Arab Emirates'), (u'United Kingdom', u'United Kingdom'), (u'United States', u'United States'), (u'Uruguay', u'Uruguay'), (u'Uzbekistan', u'Uzbekistan'), (u'Vanuatu', u'Vanuatu'), (u'Venezuela', u'Venezuela'), (u'Vietnam', u'Vietnam'), (u'Wallis and Futuna', u'Wallis and Futuna'), (u'Western Sahara', u'Western Sahara'), (u'Yemen', u'Yemen'), (u'Zambia', u'Zambia'), (u'Zimbabwe', u'Zimbabwe')]
                                        ,
                                       #(c.iso3,c.name) for c in pc.all_countries()],
                                max_length=40)
    date = models.DateField()
    type = models.CharField(choices=[("NewInfo","NewInfo"),
                                       ("PartTransfer","PartTransfer"),
                                       ("FullTransfer","FullTransfer"),
                                       ("Breakaway","Breakaway"), 
                                        ],
                                    max_length=40,)

    # should only show if changetype requires border delimitation...
    transfer_source = models.CharField(max_length=200)
    transfer_reference = models.CharField(max_length=400)
    transfer_geom = models.MultiPolygonField(null=True, blank=True)
    
    fromname = models.CharField(max_length=40)
    fromiso = models.CharField(max_length=40, blank=True)
    fromfips = models.CharField(max_length=40, blank=True)
    fromhasc = models.CharField(max_length=40, blank=True)
    fromcapital = models.CharField(max_length=40, blank=True)
    fromtype = models.CharField(choices=[("Province","Province"),
                                         ("Municipality","Municipality"),
                                         ("District","District"),
                                         ("County","County"),
                                         ("State","State"),
                                         ("Parish","Parish"),
                                         ("Region","Region"),
                                         ("Prefecture","Prefecture"),
                                         ("Department","Department"),
                                         ("Governate","Governate"),
                                         ("Other...","Other...")
                                         ],
                                max_length=40, blank=True)

    toname = models.CharField(max_length=40)
    toiso = models.CharField(max_length=40, blank=True)
    tofips = models.CharField(max_length=40, blank=True)
    tohasc = models.CharField(max_length=40, blank=True)
    tocapital = models.CharField(max_length=40, blank=True)
    totype = models.CharField(choices=[("Province","Province"),
                                         ("Municipality","Municipality"),
                                         ("District","District"),
                                         ("County","County"),
                                         ("State","State"),
                                         ("Parish","Parish"),
                                         ("Region","Region"),
                                         ("Prefecture","Prefecture"),
                                         ("Department","Department"),
                                         ("Governate","Governate"),
                                         ("Other...","Other...")
                                         ],
                                max_length=40, blank=True)
