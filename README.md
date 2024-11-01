 # NC State Jobs Review System
 
This is a Flask App for the NCSU Campus Job Review System with a MongoDB database for storage. Here, students from NCSU can view reviews on all the different jobs that are available on campus. The portal aims to help students better understand the job description and the work experienced by fellow students. The website allows the students to upload reviews for others to view. The anonymity of the students is maintained to allow them to upload honest reviews.

![alt text](https://github.com/ashishjoshi2605/ncsu-campus-jobs-review-system/blob/main/app/static/ProjectUI.png)

New Badges

[![codecov](https://codecov.io/gh/NCSU-SE-2024/PackReview_v3/graph/badge.svg?token=IAgSDGwaDv)](https://codecov.io/gh/NCSU-SE-2024/PackReview_v3)
[![Pylint](https://github.com/NCSU-SE-2024/PackReview_v3/actions/workflows/pylint.yml/badge.svg)](https://github.com/NCSU-SE-2024/PackReview_v3/actions/workflows/pylint.yml)
[![Python Flask Application](https://github.com/NCSU-SE-2024/PackReview_v3/actions/workflows/test-app.yml/badge.svg)](https://github.com/NCSU-SE-2024/PackReview_v3/actions/workflows/test-app.yml)
[![Run tests and upload coverage](https://github.com/NCSU-SE-2024/PackReview_v3/actions/workflows/codecov.yml/badge.svg)](https://codecov.io/gh/NCSU-SE-2024/PackReview_v3)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14026707.svg)](https://doi.org/10.5281/zenodo.14026707)

Old Badges

[![Test Coverage](https://github.com/NCSU-SE-2024/PackReview_v3/actions/workflows/test-app.yml/badge.svg)](https://github.com/NCSU-SE-2024/PackReview_v3/actions/workflows/test-app.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7402242.svg)](https://doi.org/10.5281/zenodo.7402242)
<a href="https://github.com/kunalshah03/PackReview_Part2/graphs/contributors" alt="Contributors"><img src = "https://img.shields.io/github/contributors/kunalshah03/PackReview_Part2"/></a>
![Lint Python](https://github.com/amisha-w/PackTravel/actions/workflows/pylint.yml/badge.svg)
[![codecov](https://codecov.io/gh/amisha-w/PackTravel/branch/main/graph/badge.svg?token=HRFN97UEB7)](https://codecov.io/gh/amisha-w/PackTravel)
![Python Style Checker](https://github.com/amisha-w/PackTravel/actions/workflows/python_style_checker.yml/badge.svg)
<a href="https://github.com/kunalshah03/PackReview_Part2" alt="Repo Size"><img src="https://img.shields.io/github/repo-size/kunalshah03/PackReview_Part2" /></a>
<a href="https://github.com/kunalshah03/PackReview_Part2/blob/main/LICENSE" alt="License"><img src="https://img.shields.io/github/license/kunalshah03/PackReview_Part2" /></a>
<a href="https://github.com/kunalshah03/PackReview_Part2/issues" alt="Open Issues"><img src="https://img.shields.io/github/issues-raw/kunalshah03/PackReview_Part2" /></a>
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/kunalshah03/PackReview_Part2?style=plastic)
<a href="https://github.com/kunalshah03/PackReview_Part2/actions" alt="Build Status"><img src="https://img.shields.io/github/workflow/status/kunalshah03/PackReview_Part2/Build%20main" /></a>
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/kunalshah03/PackReview_Part2)


## Pre-requisites
To run these scripts, you will require Python installed on your PC. Please visit [Python Installers](https://www.python.org/downloads/) to download the lastest python version. Apart from that, other requirements can be installed with the help of requirements.txt.

## Installation
Initially you can check whether your system has python pre-installed or not, usually nowadays in most of the systems, be it Windows or MacOS, python is pre-installed. 

To check whether you have python installed or not, you can open CMD or a Terminal and run the command "python --version". If the CMD shows the version such as Python 3.10 then your system already has python installed and you just need to clone the repository and run the python scripts. 

If this is not the case, then you need to download python installer package from [Python Installers](https://www.python.org/downloads/) based on your system's operating system and install it and you can further clone this repository to execute the scripts.

You can refer [INSTALL.md](https://github.com/NCSU-SE-2024/PackReview_v3/blob/main/install.md) for the complete installation steps based on your OS.

## Poster
![alt text](https://github.com/kunalshah03/PackReview_Part2/blob/main/app/static/Poster.jpg)

## Contribution Code of Conduct

The rules listed below are to be followed by the ones who will be contributing to the code in the repository:

  - Atleast one review/approval is required from any other contributors of the project to merge a commit to the main branch.
  - It is recommended to delete the branch as soon as it is merged to the main branch to avoid stale branches in the repository.
  - It is encouraged to add name tags such as "feature-" or "patch-" in the branches if it is used to add code-patches or features in the project.
  
### Code Coverage Screenshot

![alt text](https://github.com/NCSU-SE-2024/PackReview_v3/blob/main/Data/v3/CoverageReport.png)

### Test Run Screenshot

![alt text](https://github.com/NCSU-SE-2024/PackReview_v3/blob/main/Data/v3/TestRun.png)

### Slack Channel Screenshot

![WhatsApp Image 2022-12-05 at 9 05 34 PM](https://user-images.githubusercontent.com/111834635/205791376-6dc27993-f39e-4737-b5b8-2219ac74df60.jpeg)

### Video demonstrating the old functionalities
https://user-images.githubusercontent.com/60925790/205790268-41892a26-7dfa-4d52-a326-848212b1e4fe.mp4

### Video demonstrating the new functionalities
Add video here

# Quick look at the newly added features

* Top Job Picks for Enhanced Discovery: Users can now explore a curated list of the most highly rated job opportunities based on reviews and recommendations. This feature guides users toward top-rated positions, providing an efficient way to discover high-quality job opportunities at a glance.

* Discussion Forum for Open Career Conversations:
A fully interactive discussion forum allows users to create topics, share insights, and discuss various job-related subjects. This platform enriches the community by enabling users to exchange ideas, seek advice, and build networks directly within the application.

* Advanced Review Updating for Accurate Job Reflections:
Users now have the flexibility to update their job reviews to reflect current experiences and insights. This ensures that job reviews remain relevant and up-to-date, contributing to a more accurate resource for job seekers.

* Enhanced User Experience with Dynamic Warning Messages:
Dynamic warning messages are now integrated in the app, offering real-time feedback on actions. This prevents errors, ensures clarity, and provides a smoother user journey by instantly notifying users of any potential issues.

* Bug Fixes for Seamless Navigation and Consistency:
Numerous bugs, such as issues with pagination, inconsistent page transitions, and absent warning notifications, have been resolved. These fixes improve app stability, ensuring a consistently smooth and reliable user experience.



## Roadmap
* [List of Roadmap and their corresponding open issues](https://github.com/NCSU-SE-2024/PackReview_v3/issues)
  
## Team Members - Project 2
* Anish Dhage
* Gaurav Sheth
* Soham Gundewar


