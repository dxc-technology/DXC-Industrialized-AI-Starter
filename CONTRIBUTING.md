

## How to contribute

We want to keep it as easy as possible to contribute changes that get things
working in your environment. There are a few guidelines that we need
contributors to follow so that we can have a chance of keeping on top
of things.

## Getting Started

* Make sure you have a [GitHub account](https://github.com/signup/free).
* Submit a ticket for your issue, assuming one does not already exist.
  * DXC Industrialized AI Starter tickets are filed on the GitHub project in [issues tab](https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/issues).
  * Please try to clearly describe the issue, including the steps to reproduce
    any bug.
  * Please include the story of "why" you want to do something.
* Fork the repository on GitHub.
* Glance at the [Git Best Practices][best-practice] document, even if you
  don't read it all yet.

## Making Changes

* Create a topic branch for your work.
  * You should branch off the `master` branch.
  * Name your branch by the type of contribution and target:
	* Generally, the type is `bug`, or `feature`, but if they don't fit pick
  	  something sensible.
  * To create a topic branch based on master:
	`git checkout master && git pull && git checkout -b bug/master/my_contribution`
* Don't work directly on the `master` branch, or any other core branch.
  Your pull request will be rejected unless it is on a topic branch.
* Every commit should do one thing, and only one thing.
* Having too many commits is better than having too few commits.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format.
  If your commit fixes an issue, close it with your commit message (by
  appending, e.g., `fixes #99999`, to the summary).

````
	(#99999) Make the example in CONTRIBUTING imperative and concrete

	Without this patch applied the example commit message in the CONTRIBUTING
	document is not a concrete example.  This is a problem because the
	contributor is left to imagine what the commit message should look like
	based on a description rather than an example.  This patch fixes the
	problem by making the example concrete and imperative.

	The first line is a real life imperative statement with a ticket number
	from our issue tracker.  The body describes the behavior without the patch,
	why this is a problem, and how the patch fixes the problem when applied.
````

* Make sure you have added tests for your changes.
* Run _all_ the tests to assure nothing else was accidentally broken.
  * If possible, run the acceptance tests as well as the unit tests.
  * You can *always* ask for help getting the tests working, or with
	writing tests.

## Branching, and Where Changes Go

Until a stable version of DXC Industrialized AI Starter is shipped, there is only one branch:
`master`.  All changes target that branch.

### Branch and Version Compatibility

Any change to  DXC Industrialized AI Starter branch should strive as much as possible to be compatible
with all released versions of DXC Industrialized AI Starter.  We want to avoid multiple incompatible
versions existing as much as possible.

Until 1.0.0 we are willing to accept backward-incompatible changes if there is
no possible way around it.  Those changes MUST provide a migration strategy
and, if possible, deprecation warnings about the older functionality.

Right now any change committed to `master` must be considered "live".


## Submitting Changes

* Unless your contribution is [trivial][exemption], ensure you have signed the
  [Contributor License Agreement][cla].
* Push your changes to a topic branch in your fork of the repository.
* Submit a pull request to the repository in the Dxc organization.
* Update your ticket to mark that you have submitted code and are ready to be
  reviewed.
  * Mentioning the issue number in the subject will make this happen through
	GitHub magic.
* A committer checks that the pull request is well formed.  If not, they will
  ask that it is fixed:
  1. it is on its own, appropriately named, branch.
  2. it was submitted to an appropriate target branch.
  3. it only has commits relevant to the specific issue.
  4. it has appropriate, clear, and effective commit messages.
* A committer can start a pull request specific discussion; at this point that covers:
  1. Reviewing the code for any obvious problems.
  2. Providing feedback based on personal experience on the subject.
  3. Testing relevant examples on an untested platform.
  4. Thoroughly stepping through the change to understand potential side-effects.
  5. Examining discrepancies between the original issue and the pull request.
  6. Using @mentioning to involve another committer in the discussion.

Anyone can offer their assessment of a pull request, or be involved in the
discussion, but keep in mind that this isn't the time to decide if the pull
request is desired or not.  The only reason it should be rejected at this
point is if someone skipped the earlier steps in the process and submitted
code before any discussion happened.

* Every review should add any specific changes required to the pull request:
  * For comments on specific code, using GitHub line comments.
  * For general changes, include them in the final assessment.
* Every review should end by specifying the type of review, and a vote:
  1. Good to merge.
  2. Good to merge with minor changes (which are specified, or line comments).
  3. Not good to merge without major changes (which are specified).
* Any committer can merge after there is a vote of "good to merge".
   1. Committers are trusted to do the right thing - you can merge your own code, but you should make sure you get appropriate independent review.
   2. Most changes should not merge unless a code review has been completed.
* If the pull request is not reviewed within 14 days, you can ask any committer to execute the merge regardless:
  * This can be blocked at any time by a single constructive vote against
	merging ("Don't merge this, until you change...")
  * This is not stopped by a non-constructive vote (Don't merge this, I have
	not had a chance to look at it yet.")
   * The committer is encouraged to review before merging.


## Becoming a Committer

DXC Industrialized AI Starter is an open project: any contributor can become a committer.  Being a
committer comes with great responsibility: your decisions directly shape the
community, and the effectiveness, of the DXC Industrialized AI Starter project.  You will probably
invest more, and produce less, as a committer than a regular developer
submitting pull requests.

As a committer your code is subject to the same review and commit restrictions
as regular committers. You must exercise greater caution that most people in
what you submit and include in the project.

On the other hand you have several additional responsibilities over and above
those of a regular developer:
1. You are responsible for reviewing and voting on inclusion of code from
   other developers.
   * You are responsible for giving constructive feedback that action can be
     taken on when code isn't quite there yet
2. You are responsible for ensuring that quality, tested code is committed.
3. You are responsible for ensuring that code merges into the
   appropriate branch.
4. You are responsible for ensuring that our community is diverse, accepting,
   and friendly.
5. You are responsible for voting in a timely fashion, where required.

The best way to become a committer is to fulfill those requirements in the
community, so that it is clear that approving you is just a formality.

The process for adding a committer is:
1. A candidate has demonstrated familiarity with the quality guidelines and
   coding standards by submitting at least two pull requests that are accepted
   without modification.
2. The candidate is proposed by an existing committer.
3. A formal vote is held on the project private mailing list.
5. Existing committers vote on the candidate:
   * yes, accept them as a committer.
   * no, do not accept them as a committer.
6. If a majority of existing committers vote positively, the new committer
   is added to the public list of committers, and announced on the mailing list.

Voting on adding a committer is absolutely private, and any feedback to
candidates about why they were not accepted is at the option of the
project leader.

### Removing Committers

Removing a committer happens if they don't live up to their responsibilities,
or if they violate the community standards.  This is done by the project
leader.  The details of why are private, and will not be shared.

[bugs]:            https://github.com/csc/OSSRank/issues
[best-practice]:   http://sethrobertson.github.com/GitBestPractices/
[exemption]:       http://opensource.csc.com/sysworkflow/en/neoclassic/251810809537eb36f73ac23031915862/TrivialPatchExemptionProcess.php
[cla]:             http://opensource.csc.com/sysworkflow/en/neoclassic/251810809537eb36f73ac23031915862/Signing_CLA_Welcome_Page.php


### Security issue notifications
If you discover a potential security issue in this project we ask that you notify DXC Technology Security via email. Please do **not** create a public github issue











