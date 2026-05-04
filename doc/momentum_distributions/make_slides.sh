#!/bin/bash

# Define the final output name
PDF_NAME="slides.pdf"

# 1. Clean up the old presentation PDF 
if [ -f "$PDF_NAME" ]; then
    echo "Deleting old $PDF_NAME..."
    rm -f $PDF_NAME
fi

# 2. Run the python script to generate the slides.tex file
echo "Generating LaTeX source code..."
python3 generate_slides.py

# Check if python script succeeded
if [ $? -ne 0 ]; then
    echo "Error: Python script failed. Exiting."
    exit 1
fi

# 3. Compile the PDF using pdflatex in nonstopmode
echo "Compiling PDF..."
pdflatex -interaction=nonstopmode slides.tex

# Check if pdflatex succeeded
if [ $? -ne 0 ]; then
    echo "Error: LaTeX compilation failed! Please check the terminal output above or slides.log for details."
    exit 1
fi

# 4. Clean up the messy auxiliary files pdflatex leaves behind
echo "Cleaning up LaTeX auxiliary files..."
rm -f slides.aux slides.log slides.nav slides.out slides.snm slides.toc

echo "----------------------------------------"
echo "Success! Your presentation is ready: $PDF_NAME"