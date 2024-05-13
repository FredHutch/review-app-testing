# review-app-testing

## Proof-of-concept of Review Apps

### What are review apps?

A review app is an application that reflects the state of a specific branch in a github repository.
The benefit of a review app is that the entire team can try it out, test it, and offer feedback, without having to build and install the app themselves. Also, it *only* reflects the changes in a single branch. 

Review apps are created automatically. 

### What is this POC?

It's just a simple dynamic web app written in Python's Flask framework.

It is *relatively* easy to create review apps with a simple setup like this.
It becomes a LOT more complicated when there are other moving parts such as 
databases. We may revisit this POC and add some components like that.

You can access the production version of this app (reflecting the `main` branch) at

[https://review-app-testing.fredhutch.org/](https://review-app-testing.fredhutch.org/)

(must be inside the FH network)

### Workflow

One possible workflow is suggested in the first illustration [here](https://docs.gitlab.com/ee/ci/review_apps/).
That's great for production projects, but this is just a proof-of-concept. 

In this project the workflow is as follows:

* Make a new branch off of the `main` branch. Let's say we call it `newfeature`.
* Make some changes to the app. I'd suggest changing the return value of the
[hello](https://github.com/FredHutch/review-app-testing/blob/main/src/review_app_testing/app.py#L21) 
  function, which is what is shown when going to the top-level route (`/`) of the app.
* Commit and push your changes - this will create a remote version of your local `newfeature branch.
* After the app builds in our GitLab instance, you should see the review app at
  `https://testing-review-apps.fredhutch.org/newfeature/` (again, must be inside the FH network).

**Notes**:

* There is nothing at the root of `https://testing-review-apps.fredhutch.org/`. That URL will
  return a 404 Not Found error.
* In general, the review app URL can be obtained by taking the current branch name and putting it at the end of `https://testing-review-apps.fredhutch.org/` and putting another slash (`/`) after that. However, some additional changes are made to the branch name:
    * all uppercase letters are converted to lowercase
    * long branch names are shortened to 63 bytes
    * everything except 0-9 and a-z is replaced with `-`
    * can't start or end with `-`

So to avoid confusion, it's best if your branch name starts out simple - lowercase, short, and without any characters except letters, numbers and dashes. Then you can be sure that it hasn't changed, and it will be easy to find your review app's URL.

It would be more elegant, and better in some ways, if, for a production app `foo.fredhutch.org` there was a preview app called `mybranch.foo.fredhutch.org`. 

This turns out to be tricky to do, because our current
SSL certificates only support one level of wildcards (`*.fredhutch.org` and not `*.*.fredhutch.org`), and it seems many certificate providers do not support that type of certificate for security reasons. You can cobble something together with LetsEncrypt but that is also very fiddly and has a lot of moving parts.

So instead, for any production URL, you can have another URL with nothing at the top, and apps hosted at 
endpoints that resemble the feature branch names.

This means the app to be reviewed has to be robust to variations in how it may be called. 
If an app has a route called `/foo`, then for a branch called `newfeature`, the app has to do the 
same thing whether `/foo` or `/newfeature/foo` is called. Here's an example of how to do that (see more in 
[app.py](https://github.com/FredHutch/review-app-testing/blob/main/src/review_app_testing/app.py) ):

```python
@app.route("/foo")
@app.route("/<branch_name>/foo")
def foo(branch_name=None):
    return "this is the foo endpoint"
```

### How is it done?


The magic happens in [.gitlab-ci.yml](https://github.com/FredHutch/review-app-testing/blob/main/.gitlab-ci.yml) and [docker-compose.yml](https://github.com/FredHutch/review-app-testing/blob/main/docker-compose.yml), but it generally follows the pattern described [here](https://docs.gitlab.com/ee/ci/review_apps/).

Depending on whether we are in the `main` branch or another branch, we set some variables differently and do slightly different things. Rather than do traditional [variable interpolation](https://docs.docker.com/compose/compose-file/12-interpolation/) in the `docker-compose.yml` file, we use `envsubst`. The reason for this is that `docker-compose.yml` isn't sent as-is to the Docker Swarm for deployment - it's fed into a Python script that does further processing with it.

But basically, if you are in `main`, the deployment will go to the production URL. If you're in another branch, a review app will be created in the review app url plus `/branch_name`. 

