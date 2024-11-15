# Online Bank Account System

![Online Bank Account System]()

Visit the deployed site: [Online Bank Account System](https://online-bank-account-system-0e5e73e47365.herokuapp.com/)


## CONTENTS

* [Introduction](#introduction)
* [Project](#project)
    * [User goals](#user-goals)
    * [Site owner goals](#site-owner-goals)
    * [Pre development](#pre-development)
        * [Flowchart](#flowchart)
    * [Development](#development)
        * [Google sheets](#google-sheets)
        * [Technologies Used](#technologies-used)
            * [Languages Used](#languages-used)
            * [Frameworks, Libraries & Programs Used](#frameworks-libraries--programs-used)
        * [Features](#features)
        * [Future implementations](#future-implementations)
* [Deployment](#deployment)
    * [Heroku](#heroku)
    * [Local Development](#local-development)
        * [How to Fork](#how-to-fork)
        * [How to Clone](#how-to-clone)
* [Testing](#testing)
  * [Solved Bugs](#solved-bugs)
  * [Known Bugs](#known-bugs)
* [Credits](#credits)
  * [Code Used](#code-used)
  * [Content](#content)
  * [Acknowledgments](#acknowledgments)

- - -

## Introduction

## Project

### User goals

### Site owner goals

### Pre development

#### Flowchart

### Development

#### Google sheets

#### Technologies Used

##### Languages Used

##### Frameworks, Libraries & Programs Used

#### Features

#### Future implementations

- - -
## Deployment

### Heroku

The Application has been deployed from GitHub to Heroku by following the steps:

1. Create or log in to your account at heroku.com
2. Create a new app, add a unique app name ( for example corri-construction-p3) and then choose your region
3. Click on create app
4. Go to "Settings"
5. Under Config Vars add the private API key information using key 'CRED' and into the value area copy the API key information added to the .json file.  Also add a key 'PORT' and value '8000'.
6. Add required buildpacks (further dependencies). For this project, set it up so Python will be on top and Node.js on bottom
7. Go to "Deploy" and select "GitHub" in "Deployment method"
8. To connect Heroku app to your Github repository code enter your repository name, click 'Search' and then 'Connect' when it shows below.
9. Choose the branch you want to build your app from
10. If preferred, click on "Enable Automatic Deploys", which keeps the app up to date with your GitHub repository
11. Wait for the app to build. Once ready you will see the “App was successfully deployed” message and a 'View' button to take you to your deployed link.

### Local Development

#### How to Fork

To fork the repository:

1. Log in (or sign up) to Github.
2. Go to the repository for this project, [fariba-kamani/rockScissorsPaperLizardSpock](https://github.com/Fariba-Kamani/rockScissorsPaperLizardSpock). 
3. Click the Fork button in the top right corner.

#### How to Clone

To clone the repository:

1. Log in (or sign up) to GitHub.
2. Go to the repository for this project, [fariba-kamani/rockScissorsPaperLizardSpock](https://github.com/Fariba-Kamani/rockScissorsPaperLizardSpock)
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.

- - -

## Testing

Please refer to [TESTING.md](TESTING.md) file for all testing carried out.

### Solved Bugs

### Known Bugs

  There are no known or unsolved bugs left in the program.

- - -

## Credits

### Code Used

Throughout the entire project development, I utilized the Code Institute course materials for HTML, CSS, and JavaScript. I followed the tutorials for the Love Running and Love Maths walkthrough projects to set up and start my project properly. The links from Code Institute that I relied on through out my project are as follow:

### Content

All other technologies used during the development of this project are mentioned and credited in the [technologies used](#technologies-used) section.

### Acknowledgments

I would like to acknowledge

* My Code Institute mentor, Jubril Akolade, for reviewing my project and inspiring me to improve my website.
* The Code Institute tutor team, who were available and guided me whenever I was stuck troubleshooting issues during the development of my projects.
* My partner and friends, who took the time to test my website on their devices and provided constructive feedback.

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
