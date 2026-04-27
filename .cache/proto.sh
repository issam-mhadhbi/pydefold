# VERSION=1.12.3
# url="https://github.com/defold/defold/releases/download/$VERSION/defoldsdk.zip"
# wget $url -O defold.zip 
unzip defold.zip 
protoc="./defoldsdk/ext/bin/$(uname -m)-$(uname | tr '[:upper:]' '[:lower:]')/protoc"
chmod +x "$protoc"
proto_folder="./defoldsdk/share/proto"
python_out="./pydefoldsdk"
mkdir -p "$python_out" || true 
include_google="./defoldsdk/ext/include"
proto_files=(
  $(find "$proto_folder" -type f -name "*.proto")
  $(find "$include_google" -type f -name "*.proto")
)

# Build command as array
cmd=(
  "$protoc"
  -I "$proto_folder"
  -I "$include_google"
  "--python_out=$python_out"
  "${proto_files[@]}"
)

# Print command (like Python print)
echo "Running: ${cmd[*]}"

# Execute it (optional)
"${cmd[@]}"
# i want u to add in every folder that is under python_out a file __init__.py and for every make write to it 
find "$python_out" -type d | while read -r dir; do
    # init_file="$dir/__init__.py"

    # # Create or overwrite the file
    # : > "$init_file"

    # For every .py file in that directory (except __init__.py)
    for pyfile in "$dir"/*.py; do
        [ -e "$pyfile" ] || continue  # skip if no .py files

        filename=$(basename "$pyfile")
        module="${filename%.py}"

        if [ "$module" != "__init__" ]; then
            echo "build module  $module" 
        fi
    done
done