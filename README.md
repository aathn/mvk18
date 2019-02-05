*Temporary project documentation*

# MVK FR24 #
A project within the course Software Engineering for the client Flightradar24 AB (FR24).

## Project Goal ##
The goal of the project is to create a working prototype of a pan/tilt-controllable camera that can capture airplanes flying by and stream the video to a web server with a basic web interface.

## Project Guidelines ##
This is a collection of guidelines regarding the structuring, documentation and workflow of the project useful for everyone contributing.

### Git workflow ###
We will use a git branching model called gitflow.
If you are lazy there is a git extension that enable commands that does every part of the workflow with just one command.

#### Guide ####
A guide to

##### 1. Create feature branch #####
```
$ git checkout -b <feature-name> develop
Switched to a new branch "<feature-name>"

$ git push -u origin <feature-name>
```

##### 2. Commit your code #####
Split up the feature in small commits with good names that describe the change and commit to the feature branch.

Atoms staging functionality is a good way to split work on the same file into multiple commits.

##### 3. Merge finished feature #####
Push your feature branch and create pull request in bitbucket.

Another group member has to review your code and approve the pull request.

After the merge the feature branch can be deleted from Bitbucket in the web GUI.

#### Links ####
- https://nvie.com/posts/a-successful-git-branching-model/
- https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
- https://www.atlassian.com/git/tutorials/making-a-pull-request
- https://www.atlassian.com/git/tutorials/comparing-workflows

### Code Formatting ###
- https://pre-commit.com/
- https://black.readthedocs.io/

### Documentation ###
- http://www.sphinx-doc.org/en/stable/usage/quickstart.html
- http://www.sphinx-doc.org/en/1.6/tutorial.html
