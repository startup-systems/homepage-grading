import urllib2
import csv
import re


def fetch():
    """Returns the URL, the response, and the corresponding score."""

    website = 'https://' + username + '.github.io/startup-systems/'
    try:
        response = urllib2.urlopen(website).read()
        Res = 30
    except urllib2.HTTPError:
        try:
            website = 'https://' + username + '.github.io/startup-systems'
            response = urllib2.urlopen(website).read()
            print 'Wrong URL:', website
            Res = 20
        except urllib2.HTTPError:
            try:
                website = 'https://' + username + '.github.io/'
                response = urllib2.urlopen(website).read()
                print 'Wrong URL:',website
                Res = 20
            except urllib2.HTTPError:
                try:
                    website = 'https://' + username + '.github.io/startup_system/'
                    response = urllib2.urlopen(website).read()
                    print 'Wrong URL:',website
                    Res = 20
                except urllib2.HTTPError:
                    try:
                        website = 'https://' + username + '.github.io/startup-systems/helloworld'
                        response = urllib2.urlopen(website).read()
                        print 'Wrong URL:',website
                        Res = 20
                    except urllib2.HTTPError:
                        response = None
                        Res = 0

    return website, response, Res


with open('./cms_grades.csv', 'wb') as cms_outfile:
    cms_csv = csv.writer(cms_outfile)
    # this matches the grading spreadsheet template provided by CMS
    cms_csv.writerow(["NetID", "Grade", "Add Comments"])

    with open('./homepage_grade.csv', 'wb') as outfile:
        grader = csv.writer(outfile)
        grader.writerow(['netID', 'Total', 'username', 'Res', 'ID', 'Photo', 'Bio', 'CSS', 'GA'])

        with open('./ResponseForm.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for row in reader:
                first_name = row[1]
                last_name = row[2]
                netID = row[3]
                username = row[4]

                website, response, Res = fetch()
                if not response:
                    ID = 0
                    Photo = 0
                    Bio = 0
                    CSS = 0
                    GA = 0
                    Total = Res + ID + Photo + Bio + CSS + GA
                    grader.writerow([netID, Total, username, Res, ID, Photo, Bio, CSS, GA])
                    continue

                # External CSS
                try:
                    re.search('href=[\"\'].*\.css', response).group()
                    CSS = 20
                except:
                    CSS = 0
                # ID
                try:
                    re.search(netID, response.lower()).group()
                    ID = 5
                except:
                    ID = 0

                # Photo
                try:
                    re.search('<img', response).group()
                    Photo = 20
                except:
                    try:
                        css_path = re.search('href=[\"\'](?!http).*\.css', response).group()
                        css_file = re.search('".*\.css', css_path).group()[1:]
                        css_url = website + css_file
                        css_response = urllib2.urlopen(css_url).read()
                        re.search('background-image: url', css_response).group()
                        Photo = 20
                    except:
                        Photo = 0

                # Bio
                try:
                    re.search('%s' % first_name, response).group()
                    Bio = 5
                except:
                    try:
                        re.search('%s' % last_name, response).group()
                        Bio = 5
                    except:
                        try:
                            re.search('</p>', response).group()
                            Bio = 5
                        except:
                            Bio = 0

                # Google Analytics Check
                try:
                    re.search('google-analytics.com/analytics.js', response).group()
                    GA = 20
                except:
                    GA = 0


                Total = Res + ID + Photo + Bio + CSS + GA

                reasoning = "Site found, at correct address: {:d}/30. NetID: {:d}/5. Photo: {:d}/20. Bio: {:d}/5. CSS: {:d}/20. Google Analytics: {:d}/20.".format(Res, ID, Photo, Bio, CSS, GA)

                cms_csv.writerow([netID, Total, reasoning])
                grader.writerow([netID, Total, username, Res, ID, Photo, Bio, CSS, GA])
