while IFS= read -r line; do
    jupyter labextension install "$line"
done < ./install_scripts/jupy_extensions.txt
