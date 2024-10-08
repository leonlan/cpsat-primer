<!-- EDIT THIS PART VIA 00_intro.md -->

# The CP-SAT Primer: Using and Understanding Google OR-Tools' CP-SAT Solver

<!-- START_SKIP_FOR_README -->

![Cover Image](https://raw.githubusercontent.com/d-krupke/cpsat-primer/main/images/logo_1.webp)

<!-- STOP_SKIP_FOR_README -->

_By [Dominik Krupke](https://krupke.cc), TU Braunschweig, with contributions
from Leon Lan, Michael Perk, and others._

<!-- Introduction Paragraph --->

Many [combinatorially difficult](https://en.wikipedia.org/wiki/NP-hardness)
optimization problems can, despite their proven theoretical hardness, be solved
reasonably well in practice. The most successful approach is to use
[Mixed Integer Linear Programming](https://en.wikipedia.org/wiki/Integer_programming)
(MIP) to model the problem and then use a solver to find a solution. The most
successful solvers for MIPs are, e.g., [Gurobi](https://www.gurobi.com/) and
[CPLEX](https://www.ibm.com/analytics/cplex-optimizer), which are both
commercial and expensive (though, free for academics). There are also some open
source solvers, but they are often not as powerful as the commercial ones.
However, even when investing in such a solver, the underlying techniques
([Branch and Bound](https://en.wikipedia.org/wiki/Branch_and_bound) &
[Cut](https://en.wikipedia.org/wiki/Branch_and_cut) on
[Linear Relaxations](https://en.wikipedia.org/wiki/Linear_programming_relaxation))
struggle with some optimization problems, especially if the problem contains a
lot of logical constraints that a solution has to satisfy. In this case, the
[Constraint Programming](https://en.wikipedia.org/wiki/Constraint_programming)
(CP) approach may be more successful. For Constraint Programming, there are many
open source solvers, but they usually do not scale as well as MIP-solvers and
are worse in optimizing objective functions. While MIP-solvers are frequently
able to optimize problems with hundreds of thousands of variables and
constraints, the classical CP-solvers often struggle with problems with more
than a few thousand variables and constraints. However, the relatively new
[CP-SAT](https://developers.google.com/optimization/cp/cp_solver) of Google's
[OR-Tools](https://github.com/google/or-tools/) suite shows to overcome many of
the weaknesses and provides a viable alternative to MIP-solvers, being
competitive for many problems and sometimes even superior.

### Content

Whether you are from the MIP community seeking alternatives or CP-SAT is your
first optimization solver, this book will guide you through the fundamentals of
CP-SAT in the first part, demonstrating all its features. The second part will
equip you with the skills needed to build and deploy optimization algorithms
using CP-SAT.

The first part introduces the fundamentals of CP-SAT, starting with a chapter on
installation. This chapter guides you through setting up CP-SAT and outlines the
necessary hardware requirements. The next chapter provides a simple example of
using CP-SAT, explaining the mathematical notation and its approximation in
Python with overloaded operators. You will then progress to basic modeling,
learning how to create variables, objectives, and fundamental constraints in
CP-SAT.

Following this, a chapter on advanced modeling will teach you how to handle
complex constraints, such as circuit constraints and intervals, with practical
examples. Another chapter discusses specifying CP-SAT's behavior, including
setting time limits and using parallelization. You will also find a chapter on
interpreting CP-SAT logs, which helps you understand how well CP-SAT is managing
your problem. Additionally, there is an overview of the underlying techniques
used in CP-SAT. The first part concludes with a chapter comparing CP-SAT with
other optimization techniques and tools, providing a broader context.

The second part delves into more advanced topics, focusing on general skills
like coding patterns and benchmarking rather than specific CP-SAT features. A
chapter on coding patterns offers basic design patterns for creating
maintainable algorithms with CP-SAT. Another chapter explains how to provide
your optimization algorithm as a service by building an optimization API. There
is also a chapter on developing powerful heuristics using CP-SAT for
particularly difficult or large problems. The second part concludes with a
chapter on benchmarking, offering guidance on how to scientifically benchmark
your model and interpret the results.

### Target Audience

I wrote this book for my computer science students at TU Braunschweig, and it is
used as supplementary material in my algorithm engineering courses. Initially,
we focused on Mixed Integer Programming (MIP), with CP-SAT discussed as an
alternative. However, we recently began using CP-SAT as the first optimization
solver due to its high-level interface, which is much easier for beginners to
grasp. Despite this shift, because MIP is more commonly used, the book includes
numerous comparisons to MIP. Thus, it is designed to be beginner-friendly while
also addressing the needs of MIP users seeking alternatives.

Unlike other books aimed at mathematical optimization or operations research
students, this one, aimed at computer science students, emphasizes coding over
mathematics or business cases, providing a hands-on approach to learning
optimization. The second part of the book can also be interesting for more
advanced users, providing content that I found missing in other books on
optimization.

### Table of Content

**Part 1: The Basics**

1. [Installation](#01-installation): Quick installation guide.
2. [Example](#02-example): A short example, showing the usage of CP-SAT.
3. [Basic Modeling](#04-modelling): An overview of variables, objectives, and
   constraints.
4. [Advanced Modeling](#04B-advanced-modelling): More complex constraints, such
   as circuit constraints and intervals.
5. [Parameters](#05-parameters): How to specify CP-SATs behavior, if needed.
   Timelimits, hints, assumptions, parallelization, ...
6. [Understanding the Log](#understanding-the-log): How to interpret the log
7. [How does it work?](#07-under-the-hood): After we know what we can do with
   CP-SAT, we look into how CP-SAT will do all these things.
8. [Alternatives](#03-big-picture): An overview of the different optimization
   techniques and tools available. Putting CP-SAT into context.

**Part 2: Advanced Topics**

7. [Coding Patterns](#06-coding-patterns): Basic design patterns for creating
   maintainable algorithms.
8. [(DRAFT) Building an Optimization API](#building_an_optimization_api) How to
   build a scalable API for long running optimization jobs.
9. [Large Neighborhood Search](#09-lns): The use of CP-SAT to create more
   powerful heuristics.
10. [Benchmarking your Model](#08-benchmarking): How to benchmark your model and
    how to interpret the results.

### Background

<!-- Background --->

This book assumes you are fluent in Python, and have already been introduced to
combinatorial optimization problems. In case you are just getting into
combinatorial optimization and are learning on your own, I recommend starting
with the free Coursera course,
[Discrete Optimization](https://www.coursera.org/learn/discrete-optimization),
taught by Pascal Van Hentenryck and Carleton Coffrin. This course provides a
comprehensive introduction in a concise format.

For an engaging exploration of a classic problem within this domain,
[In Pursuit of the Traveling Salesman by Bill Cook](https://press.princeton.edu/books/paperback/9780691163529/in-pursuit-of-the-traveling-salesman)
is highly recommended. This book, along with this
[YouTube talk](https://www.youtube.com/watch?v=5VjphFYQKj8) by the author that
lasts about an hour, offers a practical case study of the well-known Traveling
Salesman Problem. It not only introduces fundamental techniques but also delves
into the community and historical context of the field.

Additionally, the article
[Mathematical Programming](https://www.gurobi.com/resources/math-programming-modeling-basics/)
by CP-SAT's competitor Gurobi offers an insightful introduction to mathematical
programming and modeling. In this context, the term "Programming" does not refer
to coding; rather, it originates from an earlier usage of the word "program",
which denoted a plan of action or a schedule. If this distinction is new to you,
it is a strong indication that you would benefit from reading this article.

> **About the Lead Author:** [Dr. Dominik Krupke](https://krupke.cc) is a
> postdoctoral researcher with the
> [Algorithms Division](https://www.ibr.cs.tu-bs.de/alg) at TU Braunschweig. He
> specializes in practical solutions to NP-hard problems. Initially focused on
> theoretical computer science, he now applies his expertise to solve what was
> once deemed impossible, frequently with the help of CP-SAT. This primer on
> CP-SAT, first developed as course material for his students, has been extended
> in his spare time to cater to a wider audience.
>
> **Contributors:** This primer has been enriched by the contributions of
> several individuals. Notably, Leon Lan played a key role in restructuring the
> content and offering critical feedback, while Michael Perk significantly
> enhanced the section on the reservoir constraint. I also extend my gratitude
> to all other contributors who identified and corrected errors, improved the
> text, and offered valuable insights.

> **Found a mistake?** Please open an issue or a pull request. You can also just
> write me a quick mail to `krupked@gmail.com`.

> **Want to contribute?** If you are interested in contributing, please open an
> issue or email me with a brief description of your proposal. We can then
> discuss the details. I welcome all assistance and am open to expanding the
> content. Contributors to any section or similar input will be recognized as
> coauthors.

> **Want to use/share this content?** This tutorial can be freely used under
> [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/). Smaller parts can
> even be copied without any acknowledgement for non-commercial, educational
> purposes.

<!-- START_SKIP_FOR_README -->

> **Why are there so many platypuses in the text?** I enjoy incorporating
> elements in my texts that add a light-hearted touch. The choice of the
> platypus is intentional: much like CP-SAT integrates diverse elements from
> various domains, the platypus combines traits from different animals. The
> platypus also symbolizes Australia, home to the development of a key technique
> in CP-SAT - Lazy Clause Generation (LCG).

<!-- STOP_SKIP_FOR_README -->

---
