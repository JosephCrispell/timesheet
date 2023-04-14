# TODO Add code to get test coverage and update badger in README
# See second answer here for code to get coverage from unitttest: https://stackoverflow.com/questions/29295965/python-coverage-badges-how-to-get-them
# See video here for how to create manual shields.io badge: https://www.youtube.com/watch?v=bNVRxb-MKGo&ab_channel=glebbahmutov
# - Note that will need specific script to set colour thresholds
# - For example: https://img.shields.io/badge/coverage-75%25-green url gives great looking badge

# Generate coverage report: pythontutorial.net/python-unit-testing/python-unittest-coverage/

# See existing tool: https://pypi.org/project/readme-coverage-badger/

#%%
import subprocess

#%%
# Run code coverage calculation
subprocess.run(["python3", "-m", "coverage", "run", "--source=.", "-m", "unittest"])

# Generate the report
coverage_report = subprocess.check_output(["python3", "-m", "coverage", "report"])

# %%

# Grab overall coverage score
coverage_score = float(coverage_report.decode("utf-8").split()[-1][:-1])

# Determine colour
poor_max_threshold = 25
medium_max_threshold = 75
badge_colour = None
if coverage_score < poor_max_threshold:
    badger_colour = "red"
elif coverage_score < medium_max_threshold:
    badge_colour = "orange"
else:
    badge_colour = "green"

# Make badge
badge = f"https://img.shields.io/badge/coverage-{coverage_score}%25-{badge_colour}"
# %%
