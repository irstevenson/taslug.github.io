# Introduction

This is the Jekyll website source for the Tasmanian Linux User Group (TasLUG).

# Usage

The follow details how you can work on the site locally without polluting your local Ruby
environment (similar to Python virtualenvs). It can do this through the use of
[RVM](https://rvm.io/) and [Bundler](https://bundler.io/).

First, ensure you have a version of Ruby >= 2.1.0 - if you have RVM installed, then on entering the
directory it will attempt to set the Ruby version to that specified in `Gemfile`. After which
execute:

    $ gem install bundler

Next, after cloning the repository go into the working folder and:

    $ bundle install --path vendor/bundle

Finally, you should be able to run the site - for local viewing - via:

    $ bundle exec jekyll serve

# Contributions

Contributions are welcome via pull-request. Please review the issues for ideas of what's needed.
