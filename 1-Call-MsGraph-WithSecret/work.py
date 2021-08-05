import json
from openpyxl import Workbook
import markdown2
parsed_pages = []


def valid_range(row, start, stop):
    valid = None
    for i in range(start, stop):
        if row[i]:
            valid = [i, row[i]]
    return valid


with open('items.json', 'r') as fp:
    data = json.load(fp)
    for idx, row in enumerate(data):
        if idx == 0:
            continue
        slug = row[0]
        if slug:
            print("Parsed: {0} ---> {1}".format(idx, row[0]))

            page = {
                "slug": slug,
                "type": row[1],
                "title": row[2],
                "description": row[3] and row[3] or None
            }
            if row[7]:
                page["bullets"] = row[7].split('\n')

            if valid_range(row, 4, 6):
                page["offer"] = {
                    "top": row[4],
                    "bottom": row[5],
                    "image": row[6],
                }

            if row[8] or row[12] or row[17] or row[22]:
                page["cta_blocks"] = {}
                if valid_range(row, 8, 11):
                    page["cta_blocks"]['top'] = {
                        "text": row[8],
                        "buttonText": row[9],
                        "bottomText": row[10],
                        "bottomTextMobile": row[11]
                    }
                if valid_range(row, 12, 16):
                    page["cta_blocks"]['cta_1'] = {
                        "cover": row[12],
                        "text": row[13],
                        "buttonText": row[14],
                        "bottomText": row[15],
                        "bottomTextMobile": row[16]
                    }
                if valid_range(row, 17, 21):
                    page["cta_blocks"]['cta_2'] = {
                        "cover": row[17],
                        "text": row[18],
                        "buttonText": row[19],
                        "bottomText": row[20],
                        "bottomTextMobile": row[21]
                    }
                if valid_range(row, 22, 26):
                    page["cta_blocks"]['cta_3'] = {
                        "cover": row[22],
                        "text": row[23],
                        "buttonText": row[24],
                        "bottomText": row[25],
                        "bottomTextMobile": row[26]
                    }

            top_services = row[27]
            if top_services:
                page["top_services"] = []
                for top_service in top_services.split('\n'):
                    parsed_top_service = top_service.split(";")
                    page["top_services"].append({
                        "title": parsed_top_service[0],
                        "suffix": "от",
                        "price": parsed_top_service[1],
                        "affix": "",
                        "image": parsed_top_service[2]
                    })

            services = row[28]
            if services:
                page["services"] = []
                for service in services.split('\n'):
                    parsed_service = service.split(";")
                    page["services"].append({
                        "title": parsed_service[0],
                        "suffix": "от",
                        "price": parsed_service[1],
                        "affix": ""
                    })

            works = row[29]
            if works:
                page["works"] = []
                for work in works.split('\n'):
                    parsed_work = work.split(";")
                    page["works"].append({
                        "photo": parsed_work[0],
                        "alt": parsed_work[1]
                    })
            reviews = row[30]
            if reviews:
                page["reviews"] = []
                for review in reviews.split('\n'):
                    parsed_review = review.split(";")
                    page["reviews"].append({
                        "photo": parsed_review[0],
                        "title": parsed_review[1],
                        "text": parsed_review[2]
                    })
            parsed_pages.append(page)

deploy_pages = []


main_page = list(filter(lambda x: x['type'] == 'основа', parsed_pages))[0]
import copy

deploy_main_page = copy.deepcopy(main_page)
deploy_main_page["slug"] = [deploy_main_page['slug']]
deploy_main_page["title"] = deploy_main_page["title"].format(
    CRASH="Ремонт", TYPE="", BRAND="", DISTRICT="")
deploy_main_page["description"] = deploy_main_page["title"].format(
    CRASH="Ремонт", TYPE="", BRAND="", DISTRICT="")
deploy_main_page["offer"]["top"] = deploy_main_page["offer"]["top"].format(
    CRASH="РЕМОНТ", TYPE="", BRAND="", DISTRICT="")

deploy_pages.append(deploy_main_page)

brand_pages = list(filter(lambda x: x['type'] == 'бренд', parsed_pages))
district_pages = list(filter(lambda x: x['type'] == 'район', parsed_pages))
crash_pages = list(filter(lambda x: x['type'] == 'поломка', parsed_pages))
type_pages = list(filter(lambda x: x['type'] == 'вид', parsed_pages))

# / District
for district_page in district_pages:
    deploy_district_page = copy.deepcopy(main_page)
    deploy_district_page.update(district_page)
    district_title = " {0}".format(district_page["title"])
    district_page_description = district_page['description'] and markdown2.markdown(district_page['description']) or None
    if district_page_description:
        deploy_district_page['district_block'] = district_page_description
    deploy_district_page["slug"] = [main_page['slug'], district_page['slug']]
    deploy_district_page["title"] = main_page["title"].format(
        CRASH="Ремонт", TYPE="", BRAND="", DISTRICT=district_title)
    deploy_district_page["description"] = main_page["title"].format(
        CRASH="Ремонт", TYPE="", BRAND="", DISTRICT=district_title)
    deploy_district_page["offer"]["top"] = main_page["offer"]["top"].format(
        CRASH="РЕМОНТ", TYPE="", BRAND="", DISTRICT=district_title.upper())

    deploy_pages.append(deploy_district_page)
    deploy_district_page = None


# / Type
for type_page in type_pages:
    deploy_type_page = copy.deepcopy(main_page)
    deploy_type_page.update(type_page)
    type_title = " {0}".format(type_page["title"])
    type_page_description = type_page['description'] and markdown2.markdown(type_page['description']) or None
    if type_page_description:
        deploy_type_page['type_block'] = type_page_description
    deploy_type_page["slug"] = [main_page['slug'], type_page['slug']]
    deploy_type_page["title"] = main_page["title"].format(
        CRASH="Ремонт", TYPE=type_title, BRAND="", DISTRICT="")
    deploy_type_page["description"] = main_page["title"].format(
        CRASH="Ремонт", TYPE=type_title, BRAND="", DISTRICT="")
    deploy_type_page["offer"]["top"] = main_page["offer"]["top"].format(
        CRASH="РЕМОНТ".upper(), TYPE=type_title.upper(), BRAND="", DISTRICT="")

    deploy_pages.append(deploy_type_page)
    deploy_type_page = None

# / crash
for crash_page in crash_pages:
    deploy_crash_page = copy.deepcopy(main_page)
    deploy_crash_page.update(crash_page)
    crash_title = " {0}".format(crash_page["title"])
    crash_page_description = crash_page['description'] and markdown2.markdown(crash_page['description']) or None
    if crash_page_description:
        deploy_crash_page['crash_block'] = crash_page_description
    deploy_crash_page["slug"] = [main_page['slug'], crash_page['slug']]
    deploy_crash_page["title"] = main_page["title"].format(
        CRASH=crash_title, TYPE="", BRAND="", DISTRICT="")
    deploy_crash_page["description"] = main_page["title"].format(
        CRASH=crash_title, TYPE="", BRAND="", DISTRICT="")
    deploy_crash_page["offer"]["top"] = main_page["offer"]["top"].format(
        CRASH=crash_title.upper(), TYPE="", BRAND="", DISTRICT="")

    deploy_pages.append(deploy_crash_page)
    deploy_crash_page = None


# / brand
for brand_page in brand_pages:
    deploy_brand_page = copy.deepcopy(main_page)
    deploy_brand_page.update(brand_page)
    brand_title = " {0}".format(brand_page["title"])
    deploy_brand_page["slug"] = [main_page['slug'], brand_page['slug']]

    deploy_brand_page['brand_block'] = deploy_brand_page['description'] and markdown2.markdown(deploy_brand_page['description']) or None
    deploy_brand_page["title"] = main_page["title"].format(
        CRASH="Ремонт", TYPE="", BRAND=brand_title, DISTRICT="")
    deploy_brand_page["description"] = main_page["title"].format(
        CRASH="Ремонт", TYPE="", BRAND=brand_title, DISTRICT="")
    deploy_brand_page["offer"]["top"] = main_page["offer"]["top"].format(
        CRASH="РЕМОНТ", TYPE="", BRAND=brand_title.upper(), DISTRICT="")
    
    deploy_pages.append(deploy_brand_page)
    deploy_brand_page = None


# Mixings

# / Type / district
for district_page in district_pages:
    district_title = " {0}".format(district_page["title"])
    district_page_slug = district_page['slug']
    district_page_description = district_page['description'] and markdown2.markdown(district_page['description']) or None
    for type_page in type_pages:
        mix_page = copy.deepcopy(main_page)
        mix_page.update(type_page)
        type_title = " {0}".format(type_page["title"])
        type_page_description = type_page['description'] and markdown2.markdown(type_page['description']) or None
        if district_page_description:
            mix_page['district_block'] = district_page_description
        if type_page_description:
            mix_page['type_block'] = type_page_description
        mix_page["slug"] = [main_page['slug'], type_page['slug'], district_page_slug]
        mix_page["title"] = main_page["title"].format(
            CRASH="Ремонт", TYPE=type_title, BRAND="", DISTRICT=district_title)
        mix_page["description"] = main_page["title"].format(
            CRASH="Ремонт", TYPE=type_title, BRAND="", DISTRICT=district_title)
        mix_page["offer"]["top"] = main_page["offer"]["top"].format(
            CRASH="РЕМОНТ", TYPE=type_title.upper(), BRAND="", DISTRICT=district_title.upper())
        

        deploy_pages.append(mix_page)
        mix_page = None

# / Type / crash
for crash_page in crash_pages:
    crash_title = " {0}".format(crash_page["title"])
    crash_page_slug = crash_page['slug']
    for type_page in type_pages:
        mix_page = copy.deepcopy(main_page)
        mix_page.update(type_page)
        type_title = " {0}".format(type_page["title"])
        mix_page["slug"] = [main_page['slug'], type_page['slug'], crash_page_slug]
        mix_page["title"] = main_page["title"].format(
            CRASH=crash_title, TYPE=type_title, BRAND="", DISTRICT="")
        mix_page["description"] = main_page["title"].format(
            CRASH=crash_title, TYPE=type_title, BRAND="", DISTRICT="")
        mix_page["offer"]["top"] = main_page["offer"]["top"].format(
            CRASH=crash_title.upper(), TYPE=type_title.upper(), BRAND="", DISTRICT="")

        deploy_pages.append(mix_page)
        mix_page = None

# / Type / Brand
for brand_page in brand_pages:
    brand_title = " {0}".format(brand_page["title"])
    brand_page_slug = brand_page['slug']
    for type_page in type_pages:
        type_title = " {0}".format(type_page["title"])
        type_page_slug = type_page['slug']

        mix_page = copy.deepcopy(main_page)
        mix_page.update(type_page)
        mix_page["slug"] = [main_page['slug'], type_page_slug, brand_page_slug]
        mix_page["title"] = main_page["title"].format(
            CRASH="Ремонт", TYPE=type_title, BRAND=brand_title, DISTRICT="")
        mix_page["description"] = main_page["title"].format(
            CRASH="Ремонт", TYPE=type_title, BRAND=brand_title, DISTRICT="")
        mix_page["offer"]["top"] = main_page["offer"]["top"].format(CRASH="Ремонт".upper(
        ), TYPE=type_title.upper(), BRAND=brand_title.upper(), DISTRICT="".upper())

        deploy_pages.append(mix_page)
        mix_page = None

# / Brand / District
for brand_page in brand_pages:
    brand_title = " {0}".format(brand_page["title"])
    brand_page_slug = brand_page['slug']
    for district_page in district_pages:
        district_title = " {0}".format(district_page["title"])
        district_page_slug = district_page['slug']

        mix_page = copy.deepcopy(main_page)
        mix_page.update(district_page)
        mix_page["slug"] = [main_page['slug'], brand_page_slug, district_page_slug]
        mix_page["title"] = main_page["title"].format(
            CRASH="Ремонт", TYPE="", BRAND=brand_title, DISTRICT=district_title)
        mix_page["description"] = main_page["title"].format(
            CRASH="Ремонт", TYPE="", BRAND=brand_title, DISTRICT=district_title)
        mix_page["offer"]["top"] = main_page["offer"]["top"].format(CRASH="Ремонт".upper(
        ), TYPE="", BRAND=brand_title.upper(), DISTRICT=district_title.upper())

        deploy_pages.append(mix_page)
        mix_page = None

# / Brand / Crash
for brand_page in brand_pages:
    brand_title = " {0}".format(brand_page["title"])
    brand_page_slug = brand_page['slug']

    for crash_page in crash_pages:
        crash_title = " {0}".format(crash_page["title"])
        crash_page_slug = crash_page['slug']

        mix_page = copy.deepcopy(main_page)
        mix_page.update(crash_page)
        mix_page["slug"] = [main_page['slug'], brand_page_slug, crash_page_slug]
        mix_page["title"] = main_page["title"].format(
            CRASH=crash_title, TYPE="", BRAND=brand_title, DISTRICT="")
        mix_page["description"] = main_page["title"].format(
            CRASH=crash_title, TYPE="", BRAND=brand_title, DISTRICT="")
        mix_page["offer"]["top"] = main_page["offer"]["top"].format(
            CRASH=crash_title.upper(), TYPE="", BRAND=brand_title.upper(), DISTRICT="")

        deploy_pages.append(mix_page)
        mix_page = None


# / Type / Brand / crash
# for type_page in type_pages:
#     type_title = " {0}".format(type_page["title"])
#     type_page_slug = type_page['slug']
#     for brand_page in brand_pages:
#         brand_title = " {0}".format(brand_page["title"])
#         brand_page_slug = brand_page['slug']

#         for crash_page in crash_pages:
#             crash_title = " {0}".format(crash_page["title"])
#             crash_page_slug = crash_page['slug']

#             mix_page = copy.deepcopy(main_page)
#             mix_page.update(type_page)
#             mix_page["slug"] = [main_page['slug'], type_page_slug, brand_page_slug, crash_page_slug]
#             mix_page["title"] = main_page["title"].format(
#                 CRASH=crash_title, TYPE=type_title, BRAND=brand_title, DISTRICT="")
#             mix_page["description"] = main_page["title"].format(
#                 CRASH=crash_title, TYPE=type_title, BRAND=brand_title, DISTRICT="")
#             mix_page["offer"]["top"] = main_page["offer"]["top"].format(CRASH=crash_title.upper(
#             ), TYPE=type_title.upper(), BRAND=brand_title.upper(), DISTRICT="".upper())

#             deploy_pages.append(mix_page)
#             mix_page = None

# / Brand / district / crash
# for brand_page in brand_pages:
#     brand_title = " {0}".format(brand_page["title"])
#     brand_page_slug = brand_page['slug']
#     for district_page in district_pages:
#         district_title = " {0}".format(district_page["title"])
#         district_page_slug = district_page['slug']
#         for crash_page in crash_pages:
#             crash_title = " {0}".format(crash_page["title"])
#             crash_page_slug = crash_page['slug']

#             mix_page = copy.deepcopy(main_page)
#             mix_page.update(crash_page)
#             mix_page["slug"] = [main_page['slug'], brand_page_slug, district_page_slug, crash_page_slug]
#             mix_page["title"] = main_page["title"].format(
#                 CRASH=crash_title, TYPE="", BRAND=brand_title, DISTRICT=district_title)
#             mix_page["description"] = main_page["title"].format(
#                 CRASH=crash_title, TYPE="", BRAND=brand_title, DISTRICT=district_title)
#             mix_page["offer"]["top"] = main_page["offer"]["top"].format(CRASH=crash_title.upper(
#             ), TYPE="", BRAND=brand_title.upper(), DISTRICT=district_title.upper())

#             deploy_pages.append(mix_page)
#             mix_page = None

print(deploy_pages.__len__())


# with open("remonts.json", 'w') as fp:
#     data = deploy_pages#[:100]
#     print(data.__len__())
#     json.dump(data, fp)

# wb = Workbook()
# ws1 = wb.active
# ws1.title = "0"
# for row in deploy_pages:
#     ws1.append([row["slug"]])
# wb.save(filename="LinksGenerated.xlsx")

page_skeleton = {
    "slug": "",
    "heading": "",
    "heading2": "",
    "bullets": [],
    "seo": {
        "title": "Ремонт холодильников",
        "description": "",
        "siteTitle": "Repair Service в Тольятти"
    },
    "coverImage": "",
    "top_services": [],
    "services": [],
    "faq": [],
    "works": [],
    "reviews": [],
}
