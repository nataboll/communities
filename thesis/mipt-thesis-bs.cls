\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mipt-thesis}[2019/01/21 Class for the BS thesis in the MIPT]

%%%%%% Class options %%%%%
\DeclareOption*{
    \ClassWarning{myclass}{Unknown option '\CurrentOption'}
}
\ProcessOptions\relax

\LoadClass[a4paper,12pt]{report}
%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%% Useful packages %%%%%
% Math packages, should be loaded before fontenc and babel for Cyrillic
\RequirePackage{amsmath,amsthm,amssymb}
\RequirePackage{mathtext}
% Fonts and lang
\RequirePackage[T1,TS1,T2A]{fontenc}
\RequirePackage{mathptmx}   % Times New Roman font
\RequirePackage[utf8]{inputenc}
\RequirePackage[english,russian]{babel}
% Formatting
\RequirePackage{geometry}
\RequirePackage{setspace}
\RequirePackage{indentfirst}
\RequirePackage{fancyhdr}
%\RequirePackage{nopageno}
\RequirePackage{tocloft}
% Style file with additional packages
\RequirePackage{mipt-thesis}
% Titles
\RequirePackage{titlesec}
%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%% Set up correct formatting %%%%%
\geometry{left=3cm}
\geometry{right=15mm}   % 2cm -> 1.5cm in 2019
\geometry{top=2cm}
\geometry{bottom=2cm}
\linespread{1.25}       % word 1.5 spacing, see
                        % https://tex.stackexchange.com/questions/65849/confusion-onehalfspacing-vs-spacing-vs-word-vs-the-world
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%% Some dark TeX magic %%%%%
\addto\captionsrussian{\renewcommand{\contentsname}{Содержание}}
\addto\captionsrussian{\renewcommand{\listfigurename}{Список иллюстраций}}
\addto\captionsrussian{\renewcommand{\listtablename}{Список таблиц}}
\addto\captionsrussian{\renewcommand{\bibname}{Литература}}
\addto\captionsrussian{\renewcommand{\indexname}{Index}}
\addto\captionsrussian{\renewcommand{\figurename}{Рисунок{}}}
\addto\captionsrussian{\renewcommand{\tablename}{Таблица}}
\addto\captionsrussian{\renewcommand{\partname}{Часть}}
\addto\captionsrussian{\renewcommand{\chaptername}{Глава}}
\addto\captionsrussian{\renewcommand{\appendixname}{Приложение}}
%%% Has no effect since babel package switches tags (see https://tex.stackexchange.com/questions/153182/strange-behaviour-on-redefining-contentsname, /usr/share/texlive/texmf-dist/tex/generic/babel-russian/russianb.ldf (Debian))%%%
%\renewcommand\contentsname{Содержание}
%\renewcommand\listfigurename{Список иллюстраций}
%\renewcommand\listtablename{Список таблиц}
%\renewcommand\bibname{Литература}
%\renewcommand\indexname{Index}
%\renewcommand\figurename{Рис.{}}
%\renewcommand\tablename{Таблица}
%\renewcommand\partname{Часть}
%\renewcommand\chaptername{Глава}
%\renewcommand\appendixname{Приложение}


\def\@part[#1]#2{%
    \ifnum \c@secnumdepth >-2\relax
      \refstepcounter{part}%
      \addcontentsline{toc}{part}{\thepart\hspace{1em}#1}%
    \else
      \addcontentsline{toc}{part}{#1}%
    \fi
    \partmark{#1}%
    {\centering
     \interlinepenalty \@M
     \normalfont
     \ifnum \c@secnumdepth >-2\relax
       \huge\bfseries\boldmath \partname~\thepart
       \par
       \vskip 20\p@
     \fi
     \Huge \bfseries\boldmath #2\par}%
    \@endpart}
\def\@spart#1{%
    {\centering
     \interlinepenalty \@M
     \normalfont
     \Huge \bfseries\boldmath #1\par}%
    \@endpart}

\def\@chapter[#1]#2{\ifnum \c@secnumdepth >\m@ne
                       \if@mainmatter
                         \refstepcounter{chapter}%
                         \typeout{\@chapapp\space\thechapter.}%
                         \addcontentsline{toc}{chapter}%
                                   {\protect\numberline{\thechapter}#2}%
                       \else
                         \addcontentsline{toc}{chapter}{#2}%
                       \fi
                    \else
                      \addcontentsline{toc}{chapter}{#2}%
                    \fi
                    \chaptermark{#1}%
                    \addtocontents{lof}{\protect\addvspace{10\p@}}%
                    \addtocontents{lot}{\protect\addvspace{10\p@}}%
                    \if@twocolumn
                      \@topnewpage[\@makechapterhead{#2}]%
                    \else
                      \@makechapterhead{#2}%
                      \@afterheading
                    \fi}


\def\@makechapterhead#1{%
  \vspace*{50\p@}%
  {\parindent \z@ \raggedright \normalfont
    \ifnum \c@secnumdepth >\m@ne
      \if@mainmatter
        \huge\bfseries\boldmath \@chapapp\space \thechapter
        \par\nobreak
        \vskip 20\p@
      \fi
    \fi
    \interlinepenalty\@M
    \Huge \bfseries\boldmath #1\par\nobreak
    \vskip 40\p@
  }}
\def\@makeschapterhead#1{%
  \vspace*{50\p@}%
  {\parindent \z@ \raggedright
    \normalfont
    \interlinepenalty\@M
    \Huge \bfseries\boldmath  #1\par\nobreak
    \vskip 40\p@
  }}


% \renewcommand\section{\@startsection {section}{1}{\z@}%
%                                    {-3.5ex \@plus -1ex \@minus -.2ex}%
%                                    {2.3ex \@plus.2ex}%
%                              {\normalfont\Large\raggedright}}
% \renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
%                                      {-3.25ex\@plus -1ex \@minus -.2ex}%
%                                      {1.5ex \@plus .2ex}%
%                              {\normalfont\Large\sffamily\itshape\raggedright}}

% No "Глава #" prefix
\titleformat{\chapter}[display]
{\normalfont\bfseries\centering}{}{0pt}{\large}

\titleformat{\section}
{\normalfont\bfseries\centering}{\thesection}{7pt}{}{\large}

\titleformat{\subsection}
{\normalfont\bfseries\centering}{\thesubsection}{7pt}{}{\large}
%%%%%%%% Captions %%%%%%%%%%%%%%%%%%%%%%%%%%
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{#1 --- #2}%
  \ifdim \wd\@tempboxa >\hsize
    #1. #2\par
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%% Right TOC numbering %%%%%
\renewcommand{\cftchapaftersnum}{.}
\renewcommand{\cftsecaftersnum}{.}
\renewcommand{\cftsubsecaftersnum}{.}
%%%%% Center TOC header %%%%%%%
\renewcommand{\cfttoctitlefont}{\hspace*{\fill}\large}
\renewcommand{\cftaftertoctitle}{\hspace*{\fill}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%% Easier references %%%%%
\newcommand{\formref}[1]{(\ref{#1})}
\newcommand{\picref}[1]{рис.~\ref{#1}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Title page is being generated automatically when loading diploma to mipt.ru.

\endinput
