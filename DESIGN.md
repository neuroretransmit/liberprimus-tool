# Design for Genetic Algorithm/Rule Engine

This document describes the design of the genetic algorithm/rule engine to attack the unknown
ciphertext within Liber Primus.

## Members working on this

neuroretransmit/d4vi, feel free to DM either on Discord.

## Overview

This project aims to quickly build a record of solution attempts and try new ones limited to the
scope of classical cryptography. The new attempts will be carried out by a genetic algorithm that
will intelligently mutate/crossover via a rule engine defined by a finite state machine. The 
rule engine reasoning is to limit parameters being evolved that are unneccessary for the given
crypto scheme. Keys will not be evolved, they will be randomly selected for a wordlist for keyed
algorithms. The wordlist will be compiled from messages, valid decrypts, previous keys, and words 
within the works of what was previously used in Cicada 3301. This will also include loose ends and
numbers for shifts. Each attempt will be stored in a database and have a confidence rating of how
close the decrypted text was to English or Latin.

## Context

A general overview of why this project is necessary.

### The Problem

As it stands, information on solution attempts is compartmentalized, disorganized, and requires 
searching many sources for solutions tried. This is a terribly slow and chaotic methodology and 
requires a centralized source of truth where things that have already been tried can be enumerated 
quickly and kept in a record that can be easily queried.

### Why this project is necessary

Given that all known solutions are using simple/classicical cryptography within the Liber Primus
and keys/shift numbers within past solutions, messages, or puzzle pieces, the enormous search space 
can be limited by creating a generic way to execute these solutions. For pages that have key skips or 
exclusions, a genetic algorithm can attack these nicely. There is very little automation and much more
manual analysis/cribbing as the project currently stands. The genetic algorithm should be able to find 
even partial decryptions by giving it the ability to attempt pages, segments, paragraphs, words, etc.
Lastly, we need a confidence rating of the outcome of an attempt rather than speculation. Each result
will be run through a natural language processing library to show a statistical confidence of that 
portion being either English or Latin. Using this confidence, we can find interesting results even if
the full decrypt was not successful for manual investigation.

## Goals/Non-Goals

A brief description of what this project is and what it is not

### What it is

1. A means to give solvers a way to automate attempts regardless of the cryptography scheme used.
2. A library for others to use in their own work.
3. Consolidation of things attempted and a clear record to not beat a dead horse on previous attempts.
4. (hopefully) a way to move the puzzle forward or find interesting attempts that can be manually moved forward.

### What it is not

1. A solution to the Liber Primus.
2. A means to perpetuate an ego pit for other solvers; we simply need a solution - I do not care about credit
and neither should you.

## Milestones

- All desired classical cryptography schemes implemented
- Manual usage via CLI arguments completed
    - Selecting sub-parts from parents (a paragraph within a page, a word within a sentence, etc.)
    - Specifying a cryptography scheme and its parameters
    - Giving a readout of the language confidence
    - Specify to run the GA and parameters to use within the GA
- Genetic algorithm built and working
    - Intelligent crossover
    - Intelligent mutation
        - A rule engine with a finite state machine backend for tuning crypto parameters intelligently
        - A wordlist for selecting keys
    - Tuning to exclude elitism and other problems
- Database for storing attempts
    - Storage of solutions
    - Solution lookup for evolution to skip things that have been attempted

## Solution

Upon user execution, the flow to the GA loop will be something like the following:

```
Run with "--ga" ->
    Randomly generate solution specs for gene pool
    Enter evolution loop:
        Rank gene pool
        Crossover the most fit for a new offspring
            swap attributes between the most fit to find a new solution
        Mutate the offspring
            if keyed, select a new key from the wordlist - otherwise tune parameters using rule engine
        if solution in database:
            continue/jump back to top of loop without adding to gene pool
        else run solution:
            store results in database
            add to genepool if better than least fit
            prune the least fit
```


