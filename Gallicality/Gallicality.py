import requests
import click
import time
import os
import sys
from PIL import Image
import io
import re
import csv

def ark_query(ark, from_f, to_f):
    """
    From an ark identifier, a beginning folio number (from) and an ending folio number (to),
    saves a list of image URLs located in the given interval, by requesting them
    from Gallica's IIIF API. Also saves in a list the metadata of the given ark identifier.

    :param ark: ark identifier from which images URL will get retrieve.
    :type ark: str
    :param from_f: beginning folio number for the download interval.
    :type from_f: int
    :param to_f: ending folio number for the download interval.
    :type to_f: int
    :return: image URLs list
    :rtype: list
    :return: list of metadata
    :rtype: list
    """

    url_img_list = []
    metadata = []

    url_query = "https://gallica.bnf.fr/iiif/" + ark + "/manifest.json"
    print("Fetching: {0}".format(url_query))
    r = requests.get(url_query)
    data = r.json()

    if r.status_code == 200:
        for label in data['metadata']:
            metadata.append(label)

    if r.status_code == 200:
        for item in data['sequences']:
            for page in item['canvases']:
                for img_data in page["images"]:
                    img_url = img_data["resource"]["@id"]
                    url_img_list.append(img_url)

    if from_f > 0:
        from_f = from_f - 1
    url_img_list = url_img_list[from_f:to_f]

    return url_img_list, metadata


def download_image(url_img_list, metadata, directory_name, tif=False, png=False, output_csv=False):
    """
    Downloads from an image URLs list. Creates a directory, name is specified by user.
    Said directory will be located where the python script is stored. Images will be downloaded
    in said directory. Images will be download by default in JPEG format.
    Uses Pillow library to process image files.

    :param url_img_list: image URLs list, used by the script to do a HTTP request.
    :type url_img_list: list
    :param directory_name: directory name, chosen by the user.
    :type directory_name: str
    :param tif: if true, will download images in TIFF format.
    :type: bool
    :param png: if true, will download images in PNG format.
    :type: bool
    :param output_csv: if true, will create a csv file from ark's metadata. User chooses a specific name.
    :type: bool
    """

    print(url_img_list)
    print("\n")

    pattern = "\/f[0-9]+"

    try:
        os.mkdir(directory_name)
    except FileExistsError as e:
        print("Directory name already exists. Please choose a different one.")
        sys.exit()

    with click.progressbar(url_img_list) as bar:
        for request in bar:
            r = requests.get(request)
            if r.status_code == 200:
                print("\n fetching : {0}".format(request))
                f = io.BytesIO(r.content)
                i = Image.open(f)
                name_result = re.findall(pattern, request)[0]
                name_result = name_result[1:]
                if tif:
                    i.save('./{0}/{1}.tif'.format(directory_name, name_result), 'tiff')
                    print("{0} downloaded in ./{1}/".format(name_result, directory_name))
                    i.close()
                elif png:
                    i.save('./{0}/{1}.png'.format(directory_name, name_result), 'png')
                    print("{0} downloaded in ./{1}/".format(name_result, directory_name))
                    i.close()
                else:
                    i.save('./{0}/{1}.jpg'.format(directory_name, name_result), 'jpeg')
                    print("{0} downloaded in ./{1}/".format(name_result, directory_name))
                    i.close()


            # Couche de sécurité pour ne pas surcharger l'API en cas de téléchargement important
            # Ici, une seconde s'écoule entre chaque requête.
            # Possible de rendre le délai moins long, time.sleep(0.5), par exemple.
            # Possible de le désactiver en commantant la ligne suivante/supprimant.
            # time.sleep(1)

    headers = [dict['label'] for dict in metadata]
    values = [dict['value'] for dict in metadata]

    with open('./{0}/{1}.csv'.format(directory_name, output_csv), 'w') as csv_output:
        f = csv.writer(csv_output, delimiter=",")
        f.writerow(headers)
        f.writerow(values)

@click.group()
def group():
    """
    Command line interface for users that want to download high quality images from Gallica's collection.
    Uses Gallica's IIIF API, from an ark identifier.
    Saves said images by default in JPEG format, in a new directory named by user. Said directory is
    located where the script python is stored.
    Creates a csv file from said ark's metadata in the directory.
    """


@group.command("query")
@click.argument("ark", type=str)
@click.argument("from_f", type=int)
@click.argument("to_f", type=int)
@click.argument("directory_name", type=str)
@click.argument("output_csv", type=str)
@click.option("-t", "--tif", is_flag=True, default=False, help="Download TIFF files instead of JPEG")
@click.option("-p", "--png", is_flag=True, default=False, help="Download PNG files instead of JPEG")
def run(ark, from_f, to_f, directory_name, tif, png, output_csv):
    """
    python get_corpus.py query ark from_f to_f directory_name output_csv
    python get_corpus.py query ark from_f to_f directory_name output_csv -t
    python get_corpus.py query ark from_f to_f directory_name output_csv -p

    To get folio 198 to folio 206 from ark:/12148/btv1b525088021 in JPEG
    in a directory named images_directory_f198_to_f206:
    python get_corpus.py query ark:/12148/btv1b525088021 198 206 images_directory_f198_to_f206
    
    To get the same files, but in TIFF:
    python get_corpus.py query ark:/12148/btv1b525088021 198 206 images_directory_f198_to_f206 -t
    OR
    python get_corpus.py query ark:/12148/btv1b525088021 198 206 images_directory_f198_to_f206 --tif
    
    And so forth.
    """

    url_img_list, metadata = ark_query(ark, from_f, to_f)
    download_image(url_img_list, metadata, directory_name, tif=tif, png=png, output_csv=output_csv)

    print("Download done!")

if __name__ == "__main__":
    group()
