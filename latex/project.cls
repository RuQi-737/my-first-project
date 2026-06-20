\ProvidesClass{project}[2025/03/24 v1.1 Custom Project Description Class]

% Load KOMA-Script article class
\LoadClass[a4paper, 12pt, oneside]{scrartcl}

% Load essential KOMA-Script and page setup packages
\RequirePackage{scrlayer-scrpage}
\RequirePackage{lastpage}
\KOMAoptions{parskip=half, DIV=12}

% Load essential packages
\RequirePackage[T1]{fontenc}
\RequirePackage{lmodern}
\RequirePackage{geometry}
\geometry{left=2.5cm, right=2.5cm, top=2.5cm, bottom=2cm}

% Increase footnote distance
\setlength{\footskip}{1.5cm}

% Enable graphics and colors
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\definecolor{linkcolor}{RGB}{0, 159, 227}
\definecolor{citecolor}{RGB}{0, 0, 255}
\definecolor{sectionblue}{RGB}{0, 101, 189}

% Enable font settings (Times New Roman)
\RequirePackage{fontspec}
\setmainfont{Times New Roman}
\setlength{\parindent}{0.67cm}

% Enable tabular and numerical formatting
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{array}
\RequirePackage{multirow}
\RequirePackage{rotating}
\RequirePackage{siunitx}
\sisetup{
  group-separator = {,},
  group-minimum-digits = 4
}

% Enable structured lists
\RequirePackage{enumitem}

% Enable glossaries
\RequirePackage[acronym]{glossaries}

% Enable citations and bibliography
\RequirePackage[english]{babel}
\RequirePackage[backend=biber, style=ieee, maxnames=2, minnames=1, date=iso]{biblatex}
\AtBeginBibliography{\small}

% Enable section title formatting
\RequirePackage{titlesec}
\titleformat{\section}
{\color{sectionblue}\normalfont\Large\bfseries}
{\thesection}{1em}{}
\titleformat{\subsection}
{\color{sectionblue}\normalfont\large\bfseries}
{\thesubsection}{1em}{}
\titleformat{\subsubsection}
{\color{sectionblue}\normalfont\normalsize\bfseries}
{\thesubsubsection}{1em}{}

% Enable floating figures and tables
\RequirePackage{float}

% Page numbering setup
\clearpairofpagestyles
\ofoot*{\pagemark}

% Custom page numbering format
\renewcommand{\pagemark}{\usekomafont{pagenumber}Page \thepage\ of \pageref{LastPage}}

% Define user commands for project details
\newcommand{\ProjectTitle}{[Insert Project Title]}
\renewcommand{\author}{[Insert Supervisor Name]}

% Enable hyperlink support
\RequirePackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=citecolor,
  citecolor=citecolor,
  urlcolor=linkcolor,
  pdfborder={0 0 0}
}

% Enable clever cross-referencing
\RequirePackage{cleveref}

\endinput
