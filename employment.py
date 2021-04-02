import csv

def sankey(origin, dest, size):
  print("{} [{}] {}".format(origin, size, dest))

labor_force_employment = """
Labor force [138215] Employed
Labor force [4231] Unemployed

Employed [9441] Less than a High School Diploma
' Unemployed [535] Less than a High School Diploma

Employed [34837] High School Graduates
' Unemployed [1324] High School Graduates

Employed [36282] Some College or Associate Degree
' Unemployed [1138] Some College or Associate Degree

Employed [57655] Bachelor's degree and higher
' Unemployed [1234] Bachelor's degree and higher
"""


education_strings = [ "Less than a High School Diploma",
                      "High School Graduates",
                      "Some College or Associate Degree",
                      "Bachelor's degree and higher" ]

industry_string = { 25: "Educational instruction and library occupations",
                    19: "Life, physical, and social science occupations",
                    23: "Legal occupations",
                    29: "Healthcare practitioners and technical occupations",
                    15: "Computer and mathematical occupations",
                    21: "Community and social service occupations",
                    11: "Management occupations",
                    13: "Business and financial operations occupations",
                    17: "Architecture and engineering occupations",
                    27: "Arts, design, entertainment, sports, and media occupations",
                    43: "Office and administrative support occupations",
                    31: "Healthcare support occupations",
                    49: "Installation, maintenance, and repair occupations",
                    33: "Protective service occupations",
                    39: "Personal care and service occupations",
                    53: "Transportation and material moving occupations",
                    51: "Production occupations",
                    41: "Sales and related occupations",
                    47: "Construction and extraction occupations",
                    45: "Farming, fishing, and forestry occupations",
                    35: "Food preparation and serving related occupations",
                    37: "Building and grounds cleaning and maintenance occupations" }
ed_to_industry_map = [{}, {}, {}, {}]


code_ed_distribution = {}
with open('occupation.csv') as csvfile:
  spamreader = csv.reader(csvfile)
  header = 0
  for row in spamreader:
    if header < 3:
      header += 1
      continue
  
    job_code = row[1]
    less_than_hs = float(row[2]) / 100
    hs_grad = float(row[3]) / 100
    some_college_associate = (float(row[4]) + float(row[5])) / 100
    bachelor_and_up = (float(row[5]) + float(row[6]) + float(row[7])) / 100
    code_ed_distribution[job_code] = { "Less than a High School Diploma": less_than_hs,
                                       "High School Graduates": hs_grad,
                                       "Some College or Associate Degree": some_college_associate,
                                       "Bachelor's degree and higher": bachelor_and_up }

with open('Employment Projections.csv') as csvfile:
  spamreader = csv.reader(csvfile)
  header = False
  for row in spamreader:
    if not header:
      header = True
      continue

    # Parse and clean each relevant column

    employment = float(row[2].replace(",", ""))

    name = row[0]
    junk_loc = name.find("    *")
    if junk_loc != -1:
      name = name[:junk_loc]

    job_code = row[1]
    junk_loc = job_code.find("\"")
    if junk_loc != -1:
      job_code = job_code[junk_loc+1:]
    job_code = job_code.replace("\"", "")

    industry_code = job_code
    junk_loc = industry_code.find("-")
    if junk_loc != -1:
      industry_code = float(industry_code[:junk_loc])

    # Process the columns
    for i in range(0, 4):
      if industry_code not in ed_to_industry_map[i]:
        ed_to_industry_map[i][industry_code] = 0
      i_name = education_strings[i]
      ed_proportion = code_ed_distribution[job_code][i_name]
      ed_to_industry_map[i][industry_code] += employment*ed_proportion

print(labor_force_employment)
for i in range(0, 4):
  desc = education_strings[i]
  for industry_code, employment in ed_to_industry_map[i].items():
    industry_desc = industry_string[industry_code]
    sankey(desc, industry_desc, employment)

