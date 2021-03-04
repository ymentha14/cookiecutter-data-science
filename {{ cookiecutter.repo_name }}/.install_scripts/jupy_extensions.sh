while IFS= read -r line; do
    jupyter labextension install "$line"
done < requirements/jupy_extensions.txt