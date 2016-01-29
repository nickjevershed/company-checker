#!/usr/bin/env python

import Levenshtein
import difflib
from fuzzywuzzy import fuzz
import csv
import simplejson as json
import argparse

# Parse args
parser = argparse.ArgumentParser(description="Match Australian company names against political donors.")
parser.add_argument('input', help='An input CSV file with company names in the first column')
parser.add_argument('output', help="An output file destination")
parser.add_argument('--donors', help="The donors matching file")
parser.add_argument('--contractors', help="The contractors matching file")
parser.add_argument('--register', help="The company register matching file")
parser.add_argument('--threshold', help="The threshold to use for a matched company name", default=90, type=int)
args = parser.parse_args();


#JSON file containing big list of categorised donors

if args.donors:
	donorFile = open(args.donors)
	donors = json.load(donorFile)

# contractFile = open("contractsum.json")
# contractors = json.load(contractFile)

#function to remove common words from names to improve matching algorithm
def stopWords(name):
	words = ["PTY LTD","PTY LTD.","P/L","PTY. LTD.","PTY","proprietary","LIMITED","LTD","Incorporated","inc","inc.","the",".",","," ",")","("]
	for word in words:
		name = name.replace(word.lower(),"")
	return name

#csv reader for donations input, csv writer for output. can output to a SQL database instead for lengthy projects

with open(args.input,'rU') as csvinput:
	with open(args.output, 'w') as csvoutput:
		writer = csv.writer(csvoutput, lineterminator='\n')
		reader = csv.reader(csvinput, lineterminator='\n')

		#Get the headers from the old csv, add to new csv and add our new column header

		headers = reader.next()

		if args.donors:
			headers.append('donor')
			headers.append('donor-ratio')
			headers.append('donor-matches')
			headers.append('first-donor-party')
			headers.append('first-donor-value')

		if args.contractors:
			headers.append('contractor')
			headers.append('contractor-ratio')
			headers.append('contractor-matches')
			headers.append('first-contractor-value')
			headers.append('company-status')

		writer.writerow(headers)

		#loop through the rows in the old csv

		for row in reader:
 			print "Checking", row[0]
			newrows = []
			for x in xrange(0, len(row)):
				newrows.append(row[x])

			if args.donors:
				#check the name against the list of donors
	 			matchList = []
	 			for donor in donors:
	 				companyName = stopWords(row[0].lower().strip())
					donorName = stopWords(donor['cleanName'].lower().strip())
					#print "comparing", companyName, "|", donorName
					ratio = fuzz.ratio(companyName, donorName)

					#because we can get multiple matches, we only want the best match
					if ratio >= args.threshold:
						print 'Donation match found!'
						data = {}
						data["value"] = donor["value"]
						data["matchedDonor"] = donor['cleanName']
						data["ratio"] = ratio
						data['recipient'] = donor['entityName']
						matchList.append(data)

				if matchList:
					#print matchList
					bestMatch = max(matchList,key=lambda item:item['ratio'])
					#print bestMatch
					newrows.append(bestMatch['matchedDonor'])
					newrows.append(bestMatch['ratio'])
					newrows.append(len(matchList))
					newrows.append(bestMatch['recipient'])
					newrows.append(bestMatch['value'])
				else:
					newrows.append("")
					newrows.append("")
					newrows.append("")
					newrows.append("")
					newrows.append("")


			#check the name against the list of contractors
			if args.contractors:
				matchList = []
	 			for contractor in contractors:
	 				companyName = stopWords(row[0].lower().strip())
					contractorName = stopWords(contractor['Supplier Name'].lower())
					ratio = fuzz.ratio(companyName, contractorName)

					#because we can get multiple matches, we only want the best match

					if ratio > 90:
						print 'Contractor match found!'
						data = {}
						data["value"] = contractor["sum"]
						data["matchedContractor"] = contractor['Supplier Name']
						data["ratio"] = ratio
						matchList.append(data)

				if matchList:
					#print matchList
					bestMatch = max(matchList,key=lambda item:item['ratio'])
					#print bestMatch
					newrows.append(bestMatch['matchedContractor'])
					newrows.append(bestMatch['ratio'])
					newrows.append(len(matchList))
					newrows.append(bestMatch['value'])
				else:
					newrows.append("")
					newrows.append("")
					newrows.append("")
					newrows.append("")

			## Check company register
			if args.register:
				with open('comp-reg.csv','rU') as companyCsv:
					companies = csv.reader(companyCsv, lineterminator='\n')
					for company in companies:
						if company[0].lower() == row[0].lower():
							print "Company register match found!"
							newrows.append(company[1])

			#print newrows

			if newrows:
				# print newrows
				writer.writerow(newrows)

