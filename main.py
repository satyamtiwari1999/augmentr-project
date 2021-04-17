import pymongo
from flask import Flask, render_template, request

app = Flask(__name__)


# grabbing all the documents which have the keywords in it
def findResult(keywords):
    ''' Function to find all the docs which have these keywords '''
    # creating regex for queries
    regex = ''.join(['.', '*', '(', '|'.join(keywords), ')', '.', '*'])
    # print(regex)
    found_in_grants = []  # title and summary will be stored for the documents
    found_in_case_study = []  # title and link will be stored

    # finding from the database
    # finding in grants collection
    grants_collection = cluster.Assignment.grants

    docs = grants_collection.find({"fund title": {'$regex': regex}})
    for doc in docs:
        found_in_grants.append(tuple([doc['fund title'], doc['summary']]))

    # finding in case_studies collection
    case_study_collection = cluster.Assignment.case_studies

    docs = case_study_collection.find({"title": {'$regex': regex}})
    for doc in docs:
        found_in_case_study.append(tuple([doc['title'], doc['link']]))

    return (found_in_grants, found_in_case_study)


@app.route('/', methods=['GET', 'POST'])
def home():
    global cluster
    cluster = pymongo.MongoClient(
        'mongodb+srv://satyam:{password}@aidb.ftppu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        )
    # if the form is submitted
    grant, case_study = [], []
    if request.method == "POST":
        # split all the relevent keywords
        keywords = request.form['seach_bar'].split()

        # searching the keywords in the database
        grant, case_study = findResult(keywords)
        # print(len(grant))
        # print(len(case_study))
        # print(case_study[0])

    return render_template(
        'index.html',
        grant=grant,
        case_study=case_study,
        len_grant=len(grant),
        len_case=len(case_study)
        )


if __name__ == "__main__":
    # connecting with mongo db
    app.run()
