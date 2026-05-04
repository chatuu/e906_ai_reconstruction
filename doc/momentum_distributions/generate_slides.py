import os

def generate_tex():
    # Using a raw string (r"") so we don't have to double-escape LaTeX backslashes
    tex_content = r"""\documentclass{beamer}
\usetheme{Madrid}
\usepackage{graphicx}

% Title Slide Info
\title{Using AI/ML to estimate original muon momenta from reconstructed tracks}
\author{Chethana Johannas}
\date{\today}

\begin{document}

% Title Page
\begin{frame}
    \titlepage
\end{frame}

% Slide 01
\begin{frame}{Input Files Used}
    \begin{itemize}
        \item Currently using Hugo's RS57-70 ROOT file:
        \vspace{0.5cm}
        \item \texttt{roadset57\_70\_R008\_2111v42\_tmp\_noPhys.root}
    \end{itemize}
\end{frame}

% Slide 02
\begin{frame}{Event Selection Applied}
    \begin{itemize}
        \item To ensure high-quality data for training the AI/ML model, we apply a rigorous event selection process.
        \item Specifically, we apply the \textbf{Standard Chuck Cuts}, which are optimized for Drell-Yan (DY) event topologies.
        \item These cuts successfully filter out background noise, target-dump separation ambiguity, and poor-quality tracks to isolate clean dimuon pairs.
    \end{itemize}
\end{frame}

% Slide 03
\begin{frame}{Dimuon $P_{x}$ (GeV)}
    \begin{figure}
        \centering
        % scale image to fit nicely within the beamer frame
        \includegraphics[width=\textwidth,height=0.8\textheight,keepaspectratio]{/home/devuser/github/e906_ai_reconstruction/src/DY_momentum_plots/dpx_kinematics.pdf}
    \end{figure}
\end{frame}

% Slide 04
\begin{frame}{Dimuon $P_{y}$ (GeV)}
    \begin{figure}
        \centering
        \includegraphics[width=\textwidth,height=0.8\textheight,keepaspectratio]{/home/devuser/github/e906_ai_reconstruction/src/DY_momentum_plots/dpy_kinematics.pdf}
    \end{figure}
\end{frame}

% Slide 05
\begin{frame}{Dimuon $P_{z}$ (GeV)}
    \begin{figure}
        \centering
        \includegraphics[width=\textwidth,height=0.8\textheight,keepaspectratio]{/home/devuser/github/e906_ai_reconstruction/src/DY_momentum_plots/dpz_kinematics.pdf}
    \end{figure}
\end{frame}

\end{document}
"""

    output_filename = "slides.tex"
    with open(output_filename, "w") as f:
        f.write(tex_content)
        
    print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    generate_tex()