# Latex Project Proposal

This directory contains the necessary files to compile the source code.
It uses [latexmk](https://mgeier.github.io/latexmk.html) (this usually comes with the standard installation of latex on Windows, Ubuntu, and Mac).
Within the directory, there is a ``.latexmkrc`` file that automatically defines some configurations.

## Compile the documents

Run the following command in the root folder:

```
latexmk
```

This will automatically compile the document.

## General requirements

- the report must not exceed 12 pages (excluding the title page, references, and appendix)
- if you use the template, the references will be in IEEE style

## project.cls

Do not change any content in this file unless absolutely necessary.

## project-report.tex

This is the main template to use.
You can add custom packages or commands in this file.

## literature.bib

This is a .bib file containing the references that should be used in your report.

## `src` folder

This folder contains the source files for the necessary sections, figures, and tables.
